from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from pydantic import BaseModel
import time

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
    start_time = time.time()

    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT r.first_name, r.last_name, r.email, r.id
                    FROM roommate r
                    ORDER BY last_name
                    """
                )
            ).fetchall()
        roommate_list = []
        for roommate in result:
            roommate_list.append({
                "first_name": roommate.first_name,
                "last_name": roommate.last_name,
                "email": roommate.email,
                "roommate_id": roommate.id
            })
        
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

        return roommate_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting all roommates.")

@router.post("/")
def create_roommate(new_roommate: Roommate):
    start_time = time.time()
    try:
        with db.engine.begin() as connection:
            # Check if roommate with same email already exists
            existing_roommate = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT id FROM roommate 
                    WHERE email = :email
                    """
                ),
                {"email": new_roommate.email}
            ).fetchone()
            
            if existing_roommate:
                raise HTTPException(
                    status_code=400,
                    detail="A roommate with this email already exists"
                )

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
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
        return "Roommate successfully created", {"First Name": new_roommate.first_name, "Last Name": new_roommate.last_name, "Email": new_roommate.email, "roommate id": roommate_id.id}

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a new roommate.")

@router.delete("/roommates/{roommate_id}")
def remove_roommate(roommate_id: int):
    start_time = time.time()

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
        
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
        
        return {
            "message": "Roommate successfully deleted",
            "data": {
                "roommate_id": roommate_removed.id,
                "first_name": roommate_removed.first_name,
                "last_name": roommate_removed.last_name,
                "email": roommate_removed.email
            }
        }, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while removing a roommate.")
