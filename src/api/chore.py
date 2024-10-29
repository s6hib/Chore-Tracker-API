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
    status: str

router = APIRouter(
    prefix="/chore",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/chores/", tags=["chore"])
def get_chores(
    priority: int,
    status: str
):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            '''SELECT * 
            FROM chore 
            WHERE priority = :priority
            AND status = :status'''), {"priority": priority, "status": status}).fetchall()
    
    chore_list = []
            
    for chore in result:
        chore_list.append(chore)
        
    return chore_list

