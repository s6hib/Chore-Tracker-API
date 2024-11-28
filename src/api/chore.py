from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from pydantic import BaseModel
import datetime
from enum import Enum
import sqlalchemy
from src import database as db
from typing import Optional

class FrequencyEnum(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    biweekly = 'biweekly'
    monthly = 'monthly'
    bimonthly = 'bimonthly'
    yearly = 'yearly'

class Chore(BaseModel):
    name: str
    location_in_house: str
    frequency: FrequencyEnum
    duration_mins: int
    priority: int
    due_date: datetime.date

router = APIRouter(
    prefix="/chores",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create_chore/")
def create_chore(chore: Chore):
    if (chore.priority != 1 or chore.priority != 2 or chore.priority != 3 
        or chore.priority != 4 or chore.priority != 5):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 5 inclusive")
    if (chore.priority != "daily" or chore.priority != "weekly" or chore.priority != "biweekly"
        or chore.priority != "monthly" or chore.priority != "bimonthly" or chore.priority != "yearly" ):
        raise HTTPException(status_code=500, detail="Chore frequency must be one of these: daily, weekly, biweekly, monthly, bimonthly, yearly")
    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                """
                INSERT into chore(name, location_in_house, frequency, duration_mins, priority, due_date)
                VALUES (:name, :location_in_house, :frequency, :duration_mins, :priority, :due_date)
                RETURNING id
                """
            ),{
                "name": chore.name,
                "location_in_house": chore.location_in_house,
                "frequency": chore.frequency.value,
                "duration_mins": chore.duration_mins,
                "priority": chore.priority, # from 1 to 5 only or it will cause an error
                "due_date": chore.due_date
            })
        
        chore_id = result.scalar_one()
        
        return {"message": f"Chore {chore.name} created successully.", "chore_id": chore_id }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a chore")

@router.post("/update_chore_priority", tags=["chore"])
def update_chore_priority(new_priority: int, chore_id: int):
    if (chore.priority != 1 or chore.priority != 2 or chore.priority != 3 
        or chore.priority != 4 or chore.priority != 5):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 5 inclusive")
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(
                """
                UPDATE chore 
                SET priority = :new_priority
                WHERE id = :chore_id;
                """
            ),{
                "new_priority": new_priority,
                "chore_id": chore_id
            })
            chore = connection.execute(sqlalchemy.text(
                """
                SELECT name, location_in_house, frequency, duration_mins, priority, due_date
                FROM chore
                WHERE id = :chore_id;
                """
            ),{
                "chore_id": chore_id
            }).fetchone()

        return {f"message: Chore priority updated successfully, Chore[chore_id: {chore_id}, name:{chore.name}, location_in_house:{chore.location_in_house}, frequency:{chore.frequency}, duration_mins:{chore.duration_mins}, priority:{chore.priority}, due_date:{chore.due_date}]" }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the chore priority")

@router.get("/get_chores/")
def get_chores(priority: Optional[int] = None):
    try:
        with db.engine.begin() as connection:
            if priority is not None:
                result = connection.execute(sqlalchemy.text(
                    '''
                    SELECT name, location_in_house, frequency, duration_mins, priority, due_date
                    FROM chore
                    WHERE priority = :priority
                    '''
                ), {"priority": priority}).fetchall()
            else:
                result = connection.execute(sqlalchemy.text(
                    '''
                    SELECT name, location_in_house, frequency, duration_mins, priority, due_date
                    FROM chore
                    '''
                )).fetchall()
        
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
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while returning all chores (with specified priority)")

@router.get("/30_day_chore_history")
def get_chore_history():
    # calculate date 30 days ago
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    
    try:
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
                "completion_date": record.completion_date  # removed strftime formatting to show full date
            })
        
        return history_list

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting the chores completed in the last 30 days")