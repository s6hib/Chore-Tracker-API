from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import datetime

import sqlalchemy
from src import database as db
import time

router = APIRouter(
    prefix="/chores",
    tags=["chore_assignment"],
    dependencies=[Depends(auth.get_api_key)],
)

class ChoreStatusEnum(str, Enum):
    pending = "pending"
    in_progress = 'in_progress'
    completed = 'completed'


@router.post("/{chore_id}/assignments")
def assign_chore(chore_id: int, roommate_id: int):
    start_time = time.time()

    with db.engine.begin() as connection:
        # Check if chore_id exists in the `chore` table
        chore_exists = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM chore WHERE id = :chore_id"
        ), {"chore_id": chore_id}).fetchone()
        
        if not chore_exists:
            raise HTTPException(status_code=404, detail="Chore not found")

        # Check if roommate_id exists in the `roommate` table
        roommate_exists = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM roommate WHERE id = :roommate_id"
        ), {"roommate_id": roommate_id}).fetchone()
        
        if not roommate_exists:
            raise HTTPException(status_code=404, detail="Roommate not found")

        # Check if this assignment already exists
        existing_assignment = connection.execute(sqlalchemy.text(
            """
            SELECT 1 
            FROM chore_assignment 
            WHERE chore_id = :chore_id AND roommate_id = :roommate_id
            """
        ), {
            "chore_id": chore_id,
            "roommate_id": roommate_id
        }).fetchone()
        
        if existing_assignment:
            raise HTTPException(
                status_code=400, 
                detail="This chore assignment already exists for the specified roommate."
            )
        
        # If both exist, proceed to insert the chore assignment
        connection.execute(sqlalchemy.text(
            """
            INSERT INTO chore_assignment (chore_id, roommate_id, status) 
            VALUES (:chore_id, :roommate_id, 'pending')
            """
        ), {
            "chore_id": chore_id,
            "roommate_id": roommate_id
        })
        
    end_time = time.time()  # End the timer
    execution_time = (end_time - start_time) * 1000  # Time in milliseconds
    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
    return {
        "chore_id": chore_id,
        "roommate_id": roommate_id,
        "status": "pending"
    }


@router.patch("/{chore_id}/assignments/{roommate_id}/status")
def update_chore_status(chore_id: int, roommate_id: int, status_update: ChoreStatusEnum):
    start_time = time.time()

    if (status_update != "pending" and status_update != "in_progress" and status_update != "completed"):
        raise HTTPException(status_code=400, detail="Chore assignment status must be 'pending', 'in_progress', or 'completed'")
    
    with db.engine.begin() as connection:
        # Check if chore_id exists in the `chore` table
        chore_assignment_exists = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM chore_assignment WHERE chore_id = :chore_id AND roommate_id = :roommate_id"
        ), {"chore_id": chore_id, "roommate_id": roommate_id}).fetchone()
        
        if not chore_assignment_exists:
            raise HTTPException(status_code=404, detail="Chore assignment not found")
    
        connection.execute(sqlalchemy.text(
            """
            UPDATE chore_assignment
            SET status = :status
            WHERE chore_id = :chore_id
            AND roommate_id = :roommate_id
            """
        ),
        {
            "status": status_update,
            "chore_id": chore_id,
            "roommate_id": roommate_id
        }
        )

    end_time = time.time()  # End the timer
    execution_time = (end_time - start_time) * 1000  # Time in milliseconds
    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
    return {
        "message": "Chore status updated successfully!", 
        "chore_id" : chore_id, 
        "roommate_id": roommate_id, 
        "new_status": status_update
    }
    

@router.get("/30_day_chore_history")
def get_chore_history():
    # calculate date 30 days ago
    start_time = time.time()
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
                AND c.due_date <= :today
                ORDER BY c.due_date DESC
                '''
            ), {
                "thirty_days_ago": thirty_days_ago,
                "today": datetime.date.today()
            }).fetchall()
        
        history_list = []
        for record in result:
            history_list.append({
                "title": record.chore_name,
                "completed_by": f"{record.first_name} {record.last_name}",
                "completion_date": record.completion_date  # removed strftime formatting to show full date
            })
        
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

        return history_list

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting the chores completed in the last 30 days")


@router.post("/assignments/{chore_id}/rotate")
def rotate_chore(chore_id: int, roommate_id: int):
    start_time = time.time()

    with db.engine.begin() as connection:
    # get the id of the next largest roommate id
        current_chore_assignment = connection.execute(sqlalchemy.text("""
            SELECT roommate_id, chore_id
            FROM chore_assignment
            WHERE roommate_id = :roommate_id AND chore_id = :chore_id
        """), {'roommate_id': roommate_id, "chore_id": chore_id}).fetchone()

        if not current_chore_assignment:
            raise HTTPException(status_code=400, detail="Chore_id and roommate_id combination does not exist in chore_assignment table.")
        
        next_roommate_id = connection.execute(sqlalchemy.text("""
            SELECT id
            FROM roommate
            WHERE id > :roommate_id
            ORDER BY id ASC
            LIMIT 1
        """), {'roommate_id': roommate_id}).fetchone()

        # if there isn't a roommate with a larger id then circle back to the starting id and select that roommate id
        if not next_roommate_id:
            first_roommate_id = connection.execute(sqlalchemy.text("""
                SELECT id
                FROM roommate
                ORDER BY id ASC
                LIMIT 1
            """)).fetchone()

        new_roommate_id = next_roommate_id.id if next_roommate_id.id else first_roommate_id.id

        # update the chore assignment to the 'next roommate' using the id from above
        connection.execute(sqlalchemy.text("""
            UPDATE chore_assignment
            SET roommate_id = :new_roommate_id
            WHERE chore_id = :chore_id
        """), {
            "chore_id": chore_id,
            "new_roommate_id": new_roommate_id
        })

        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
        
        return {
            "message": "Chores Rotated Successfully", 
            "chore_id": chore_id, 
            "new_roommate_id": new_roommate_id,  
        }

@router.get("/chore_assignment")
def get_chore_assignment(roommate_id: Optional[int] = None):
    start_time = time.time()  # Start the timer
    try:
        with db.engine.begin() as connection:
            if roommate_id is not None:
                result = connection.execute(sqlalchemy.text(
                    '''
                    SELECT chore_id, roommate_id, status
                    FROM chore_assignment
                    WHERE roommate_id = :roommate_id
                    ORDER BY roommate_id
                    '''
                ), {"roommate_id": roommate_id}).fetchall()
            else:
                result = connection.execute(sqlalchemy.text(
                    '''
                    SELECT chore_id, roommate_id, status
                    FROM chore_assignment
                    ORDER BY roommate_id
                    '''
                )).fetchall()
        
        chore_list = []
                
        for chore in result:
            chore_list.append({
                "chore_id": chore.chore_id,
                "roommate_id": chore.roommate_id,
                "status": chore.status
                })
            print(chore)
            
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

        return chore_list
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while returning all chores assignments (with specified roommate_id)")
