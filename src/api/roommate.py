from fastapi import APIRouter, Depends
from src.api import auth
from pydantic import BaseModel

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/roommate",
    tags=["roommate"],
    dependencies=[Depends(auth.get_api_key)],
)

class Roommate(BaseModel):
    first_name: str
    last_name: str
    email: str

@router.get("/roommates/", tags=["roommate"])
def get_roommates():
    
    return "test"

@router.post("/roommates/", tags=["roommate"])
def create_roommate(new_roommate: Roommate):
    print(new_roommate)
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO roommate (first_name, last_name, email) VALUES (:first_name, :last_name, :email);") , [{"first_name": new_roommate.first_name}, {"last_name": new_roommate.last_name}, {"email": new_roommate.email}])
        
    return new_roommate
