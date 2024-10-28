from fastapi import APIRouter, Depends
from src.api import auth
from pydantic import BaseModel
import datetime

import sqlalchemy
from src import database as db


class Chore(BaseModel):
    name: str
    location_in_house: str
    frequency: str
    duration_mins: int
    priority: int
    due_date: datetime.datetime

router = APIRouter(
    prefix="/chore",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/chores/", tags=["chore"])
def get_chores():
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM chore")).fetchall()
            
    for chore in result:
        print(chore)
        
    return "OK"

