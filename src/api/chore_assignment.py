from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src.api.roommate import Roommate
from src.api.chore import Chore
import datetime

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/chores",
    tags=["chore_assignment"],
    dependencies=[Depends(auth.get_api_key)],
)

# class ChoreAssignment(BaseModel):
#     chore_id: int
#     roommate_id: int
#     status: str = "pending"

# class ChoreStatusUpdate(BaseModel):
#     status: str

@router.post("/{chore_id}/assignments")
def assign_chore(chore_id: int, roommate_id: int):
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
        
    return {
        "chore_id": chore_id,
        "roommate_id": roommate_id,
        "status": "pending"
    }


@router.patch("/{chore_id}/assignments/{roommate_id}/status")
def update_chore_status(chore_id: int, roommate_id: int, status_update: str):
    print(status_update)
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

    return {
        "message": "Chore status updated successfully!", 
        "chore_id" : chore_id, 
        "roommate_id": roommate_id, 
        "new_status": status_update
    }
    

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


@router.post("/assignments/weekly/{chore_id}/rotate")
def rotate_chore(chore_id: int, roommate_id: int):
    try:
        with db.engine.begin() as connection:
            # selects the id of all chores that have a frequency of 'weekly'
            weekly_chores = connection.execute(sqlalchemy.text("""
                SELECT id FROM chore WHERE frequency = :frequency
            """), {"frequency": "weekly"}).all()

            # if there are weekly chores get the id of the next largest roommate id
            if weekly_chores:
                next_result = connection.execute(sqlalchemy.text("""
                    SELECT id
                    FROM roommate
                    WHERE id > :roommate_id
                    ORDER BY id ASC
                    LIMIT 1
                """), {'roommate_id': roommate_id})
                
                next_roommate = next_result.fetchone()

                # if there isn't a roommate with a larger id then circle back to the starting id and select that roommate id
                if not next_roommate:
                    next_roommate = connection.execute(sqlalchemy.text("""
                        SELECT id
                        FROM roommate
                        ORDER BY id ASC
                        LIMIT 1
                    """)).fetchone()

                new_roommate_id = next_roommate.id if next_roommate else roommate_id

                # update the chore assignment to the 'next roommate' using the id from above
                connection.execute(sqlalchemy.text("""
                    UPDATE chore_assignment
                    SET roommate_id = :new_roommate_id
                    WHERE chore_id = :chore_id
                """), {
                    "chore_id": chore_id,
                    "new_roommate_id": new_roommate_id
                })

                return {
                    "message": "Chores Rotated Successfully", 
                    "chore_id": chore_id, 
                    "new_roommate_id": new_roommate_id,  
                }

        return {
            "message": "No weekly chores found", 
            "chore_id": chore_id, 
            "new_roommate_id": roommate_id,  
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while rotating the chore responsibilites.")



@router.post("/assignments/{chore_id}/rotate")
def rotate_chore(chore_id: int, roommate_id: int):
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

        return {
            "message": "Chores Rotated Successfully", 
            "chore_id": chore_id, 
            "new_roommate_id": new_roommate_id,  
        }