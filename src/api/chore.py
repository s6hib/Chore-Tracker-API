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
    due_date: datetime.date

router = APIRouter(
    prefix="/chore",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/chores/", tags=["chore"])
def get_chores():
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            '''SELECT * 
            FROM chore 
            WHERE priority = 5''')).fetchall()
    
    chore_list = []
            
    for chore in result:
        chore_list.append(chore)
        print(chore)
        
    return chore_list

