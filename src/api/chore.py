from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from pydantic import BaseModel, Field
import datetime
from enum import Enum
import sqlalchemy
from src import database as db
from typing import Optional
import time

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
    priority: int = Field(..., ge=1, le=5, description="Priority must be between 1 and 5")
    due_date: datetime.date

router = APIRouter(
    prefix="/chores",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def create_chore(name: str, location_in_house: str, frequency: FrequencyEnum, duration_mins: int, priority: int, due_date: datetime.date = datetime.date.today()):
    start_time = time.time()  # Start the timer

    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
    if (priority != 1 and priority != 2 and priority != 3 
        and priority != 4 and priority != 5):
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 5 inclusive")
    
    if (due_date < datetime.date.today()):
        raise HTTPException(status_code=400, detail="Due date cannot be in the past")
    
    if (frequency != "daily" and frequency != "weekly" and frequency != "biweekly"
        and frequency != "monthly" and frequency != "bimonthly" and frequency != "yearly" ):
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
                "name": name,
                "location_in_house": location_in_house,
                "frequency": frequency.value,
                "duration_mins": duration_mins,
                "priority": priority, # from 1 to 5 only or it will cause an error
                "due_date": due_date
            })
        
        chore_id = result.scalar_one()

        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
            
        return {"message": f"Chore {name} created successully.", "chore_id": chore_id }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a chore")

@router.post("/update_chore_priority")
def update_chore_priority(new_priority: int, chore_id: int):
    start_time = time.time()  # Start the timer

    if (new_priority != 1 and new_priority != 2 and new_priority != 3 
        and new_priority != 4 and new_priority != 5):
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

            end_time = time.time()  # End the timer
            execution_time = (end_time - start_time) * 1000  # Time in milliseconds
            print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

        return {f"message: Chore priority updated successfully, Chore[chore_id: {chore_id}, name:{chore.name}, location_in_house:{chore.location_in_house}, frequency:{chore.frequency}, duration_mins:{chore.duration_mins}, priority:{chore.priority}, due_date:{chore.due_date}]" }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the chore priority")

@router.get("/")
def get_chores(priority: Optional[int] = None):
    start_time = time.time()  # Start the timer
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
            
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
        
        return chore_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while returning all chores (with specified priority)")
