from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src.api.roommate import Roommate
from src.api.chore import Chore

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/assign_chore",
    tags=["chore_assignment"],
    dependencies=[Depends(auth.get_api_key)],
)

class ChoreStatusUpdate(BaseModel):
    status: str

@router.post("/assign_chore/", tags=["chore_assignment"])
def assign_chore(chore_to_assign: Chore, roommate_to_assign: Roommate):
    with db.engine.begin() as connection:
        chore_id = connection.execute(sqlalchemy.text(
            '''SELECT id 
            FROM chore 
            WHERE name = :chore_to_assign_name
                AND location_in_house = :chore_to_assign_location
                AND frequency = :chore_to_assign_frequency
                AND duration_mins = :chore_to_assign_duration
                AND priority = :chore_to_assign_priority
                '''
                ),
                {
                "chore_to_assign_name": chore_to_assign.name,
                "chore_to_assign_location": chore_to_assign.location_in_house,
                "chore_to_assign_frequency": chore_to_assign.frequency,
                "chore_to_assign_duration": chore_to_assign.duration_mins,
                "chore_to_assign_priority": chore_to_assign.priority
                }
        ).fetchone()
        roommate_id = connection.execute(sqlalchemy.text(
            '''SELECT id 
            FROM roommate 
            WHERE first_name = :first_name
                AND last_name = :last_name
                AND email = :email'''
                ),
                {
                "first_name": roommate_to_assign.first_name,
                "last_name": roommate_to_assign.last_name,
                "email": roommate_to_assign.email
                }
        ).fetchone()
        
        connection.execute(sqlalchemy.text(
                """
                INSERT INTO chore_assignment (chore_id, roommate_id) 
                VALUES (:chore_id, :roommate_id, 'pending')
                """
            ),
            {
                "chore_id": chore_id.id,
                "roommate_id": roommate_id.id
            }
        )
        
    return {"chore_id": chore_id.id, "roommate":roommate_id.id, "status": "pending"}