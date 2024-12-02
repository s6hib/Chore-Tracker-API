from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from pydantic import BaseModel

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/roommates",
    tags=["roommate"],
    dependencies=[Depends(auth.get_api_key)],
)

class Roommate(BaseModel):
    first_name: str
    last_name: str
    email: str

@router.get("/")
def get_roommates():
    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT r.first_name, r.last_name, r.email
                    FROM roommate r
                    """
                )
            ).fetchall()
        roommate_list = []
        for roommate in result:
            roommate_list.append({
                "first_name": roommate.first_name,
                "last_name": roommate.last_name,
                "email": roommate.email
            })
        
        return roommate_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting all roommates.")

@router.post("/")
def create_roommate(new_roommate: Roommate):
    try:
        with db.engine.begin() as connection:
            roommate_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO roommate (first_name, last_name, email) 
                    VALUES (:first_name, :last_name, :email)
                    RETURNING id
                    """
                ),
                {
                    "first_name": new_roommate.first_name,
                    "last_name": new_roommate.last_name,
                    "email": new_roommate.email
                }
            ).fetchone()
        return {"First Name": new_roommate.first_name, "Last Name": new_roommate.last_name, "Email": new_roommate.email, "roommate id": roommate_id.id}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a new roommate.")

@router.delete("/roommates/{roommate_id}")
def remove_roommate(roommate_id: int):
    try:
        with db.engine.begin() as connection:
            roommate_removed = connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM roommate
                WHERE id = :roommate_id
                RETURNING id, first_name, last_name, email
                """
            ),
            {
                "roommate_id": roommate_id
            }
        ).fetchone()
        if not roommate_removed:
                raise HTTPException(status_code=404, detail="Roommate not found")
        
        return "Roommate successfully deleted", {
            "roommate_id": roommate_removed.id,
            "First Name": roommate_removed.first_name,
            "Last Name": roommate_removed.last_name,
            "Email": roommate_removed.email
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while removing a roommate.")