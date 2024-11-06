from fastapi import APIRouter, Depends
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

@router.get("/get_roommate", tags=["roommate"])
def get_roommates():
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

@router.post("/create_roommate", tags=["roommate"])
def create_roommate(new_roommate: Roommate):
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
