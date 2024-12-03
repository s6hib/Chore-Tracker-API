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

@router.post("/")
def create_chore(chore: Chore):
    if (chore.priority != 1 and chore.priority != 2 and chore.priority != 3 and chore.priority != 4 and chore.priority != 5):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 5 inclusive")
    
    if (chore.due_date < datetime.date.today()):
        raise HTTPException(status_code=400, detail="Due date cannot be in the past")
    
    if (chore.frequency != "daily" and chore.frequency != "weekly" and chore.frequency != "biweekly"
        and chore.frequency != "monthly" and chore.frequency != "bimonthly" and chore.frequency != "yearly" ):
        raise HTTPException(status_code=400, detail="Chore frequency must be one of these: daily, weekly, biweekly, monthly, bimonthly, or yearly")
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
                "priority": chore.priority,  # from 1 to 5 only or it will cause an error
                "due_date": chore.due_date
            })
        
        chore_id = result.scalar_one()
        
        return {"message": f"Chore {chore.name} created successully.", "chore_id": chore_id }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a chore")

@router.post("/update_chore_priority")
def update_chore_priority(new_priority: int, chore_id: int):
    if (new_priority != 1 and new_priority != 2 and new_priority != 3 and new_priority != 4 and new_priority != 5):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 5 inclusive")
    
    try:
        with db.engine.begin() as connection:

            chore_id_exists = connection.execute(sqlalchemy.text(
                """
                SELECT id
                FROM chore
                WHERE id = :chore_id;
                """),
                {
                    "chore_id": chore_id
                }).fetchall()
        if not chore_id_exists:
            raise Exception
            
    except Exception as e:
        raise HTTPException(status_code=400, detail="Chore_id does not exist")
    
    print("go here")
            
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

@router.get("/")
def get_chores(priority: Optional[int] = None):
    try:
        with db.engine.begin() as connection:
            if priority is not None:
                if not 1 <= priority <= 5:
                    raise HTTPException(status_code=400, detail="Priority filter must be between 1 and 5")
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
