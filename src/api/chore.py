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
        chore_list.append({
            "name": chore.name,
            "location_in_house": chore.location_in_house,
            "frequency": chore.frequency,
            "duration": chore.duration_mins,
            "priority": chore.priority,
            "due_date": chore.due_date
            })
        print(chore)
        
    return chore_list

@router.get("/chores/history", tags=["chore"])
def get_chore_history():
    # calculate date 30 days ago
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            '''
            SELECT 
                c.name as chore_name,
                r.first_name,
                r.last_name,
                ca.status,
                c.due_date as completion_date
            FROM chore c
            JOIN chore_assignment ca ON c.id = ca.chore_id
            JOIN roommate r ON ca.roommate_id = r.id
            WHERE ca.status = 'completed'
            AND c.due_date >= :thirty_days_ago
            ORDER BY c.due_date DESC
            '''
        ), {
            "thirty_days_ago": thirty_days_ago
        }).fetchall()
    
    history_list = []
    for record in result:
        history_list.append({
            "title": record.chore_name,
            "completed_by": f"{record.first_name} {record.last_name}",
            "completion_date": record.completion_date.strftime("%-d")  # just the day number
        })
    
    return history_list
