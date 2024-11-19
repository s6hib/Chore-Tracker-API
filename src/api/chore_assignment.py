from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src.api.roommate import Roommate
from src.api.chore import Chore

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/chores",
    tags=["chore_assignment"],
    dependencies=[Depends(auth.get_api_key)],
)

# class ChoreAssignment(BaseModel):
#     chore_id: int
#     roommate_id: int
#     status: str = "pending"

class ChoreStatusUpdate(BaseModel):
    status: str

@router.post("/assign_chore/", tags=["chore_assignment"])
def assign_chore(chore_id: int, roommate_id: int):
    with db.engine.begin() as connection:
         # Check if chore_id exists in the `chore` table
        chore_exists = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM chore WHERE id = :chore_id"
        ), {"chore_id": chore_id}).fetchone()
        
        if not chore_exists:
            raise HTTPException(status_code=404, detail="Chore not found")

        # Check if roommate_id exists in the `roommate` table
        roommate_exists = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM roommate WHERE id = :roommate_id"
        ), {"roommate_id": roommate_id}).fetchone()
        
        if not roommate_exists:
            raise HTTPException(status_code=404, detail="Roommate not found")

        # Check if this assignment already exists
        existing_assignment = connection.execute(sqlalchemy.text(
            """
            SELECT 1 
            FROM chore_assignment 
            WHERE chore_id = :chore_id AND roommate_id = :roommate_id
            """
        ), {
            "chore_id": chore_id,
            "roommate_id": roommate_id
        }).fetchone()
        
        if existing_assignment:
            raise HTTPException(
                status_code=400, 
                detail="This chore assignment already exists for the specified roommate."
            )
        
        # If both exist, proceed to insert the chore assignment
        connection.execute(sqlalchemy.text(
            """
            INSERT INTO chore_assignment (chore_id, roommate_id, status) 
            VALUES (:chore_id, :roommate_id, 'pending')
            """
        ), {
            "chore_id": chore_id,
            "roommate_id": roommate_id
        })
        
    return {
        "chore_id": chore_id,
        "roommate_id": roommate_id,
        "status": "pending"
    }


@router.patch("/{chore_id}/assignments/{roommate_id}/status", tags=["chore_assignment"])
def update_chore_status(chore_id: int, roommate_id: int, status_update: ChoreStatusUpdate):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
            UPDATE chore_assignment
            SET status = :status
            WHERE chore_id = :chore_id
            AND roommate_id = :roommate_id
            """
        ),
        {
            "status": status_update.status,
            "chore_id": chore_id,
            "roommate_id": roommate_id
        }
        )

    return {
        "message": "Chore status updated successfully!", 
        "chore_id" : chore_id, 
        "roommate_id": roommate_id, 
        "new_status": status_update.status 
    }


@router.post("/rotate_chore/", tags=["chore_assignment"])
def rotate_chore(chore_id: int, roommate_id: int):
    for chore in Chore:
        if chore['frequency'] == 'weekly':
            new_roommate_id = roommate_id + 1
            with db.engine.begin() as connection:
                connection.execute(sqlalchemy.text(
                    """
                    UPDATE chore_assignment
                    SET roommate_id = :new_roommate_id
                    WHERE chore_id = :chore_id
                    """
                ),
                {
                    "chore_id": chore_id,
                    "new_roommate_id": new_roommate_id
                }
                )

            return {
                "message": "Chores Rotated Successfully", 
                "chore_id" : chore_id, 
                "new_roommate_id": roommate_id,  
            }