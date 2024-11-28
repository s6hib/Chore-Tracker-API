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

@router.post("/{chore_id}/assignments")
def assign_chore(chore_id: int, roommate_id: int):
    try:
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
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while assigning the chore to a roommate")


@router.patch("/{chore_id}/assignments/{roommate_id}/status")
def update_chore_status(chore_id: int, roommate_id: int, status_update: ChoreStatusUpdate):
    try:
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
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the chore status")

@router.post("/assignments/weekly/{chore_id}/rotate")
def rotate_chore(chore_id: int, roommate_id: int):
    try:
        with db.engine.begin() as connection:
            # selects the id of all chores that have a frequency of 'weekly'
            weekly_chores = connection.execute(sqlalchemy.text("""
                SELECT id FROM chore WHERE frequency = :frequency
            """), {"frequency": "weekly"}).all()

            # if there are weekly chores get the id of the next largest roommate id
            if weekly_chores:
                next_result = connection.execute(sqlalchemy.text("""
                    SELECT id
                    FROM roommate
                    WHERE id > :roommate_id
                    ORDER BY id ASC
                    LIMIT 1
                """), {'roommate_id': roommate_id})
                
                next_roommate = next_result.fetchone()

                # if there isn't a roommate with a larger id then circle back to the starting id and select that roommate id
                if not next_roommate:
                    next_roommate = connection.execute(sqlalchemy.text("""
                        SELECT id
                        FROM roommate
                        ORDER BY id ASC
                        LIMIT 1
                    """)).fetchone()

                new_roommate_id = next_roommate.id if next_roommate else roommate_id

                # update the chore assignment to the 'next roommate' using the id from above
                connection.execute(sqlalchemy.text("""
                    UPDATE chore_assignment
                    SET roommate_id = :new_roommate_id
                    WHERE chore_id = :chore_id
                """), {
                    "chore_id": chore_id,
                    "new_roommate_id": new_roommate_id
                })

                return {
                    "message": "Chores Rotated Successfully", 
                    "chore_id": chore_id, 
                    "new_roommate_id": new_roommate_id,  
                }

        return {
            "message": "No weekly chores found", 
            "chore_id": chore_id, 
            "new_roommate_id": roommate_id,  
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rotating the chore responsibilites.")
