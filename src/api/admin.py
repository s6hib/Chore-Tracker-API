from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Resets all chores to initial state:
    1. Deletes all chore assignments
    2. Deletes all chores
    3. Re-inserts default chores
    """
    try:
        with db.engine.begin() as connection:
            # first delete all chore assignments (due to foreign key constraint)
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM chore_assignment;
                DELETE FROM roommate;
                DELETE FROM bill;
                DELETE FROM bill_list;
                """
            ))
            
            # then delete all chores
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM chore;
                """
            ))
            
            # Re-insert default chores
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO chore (name, location_in_house, frequency, duration_mins, priority, due_date)
                VALUES 
                    ('Mop floors', 'Living Room', 'weekly', 30, 3, '2024-11-01'),
                    ('Wash dishes', 'Kitchen', 'daily', 10, 2, '2024-10-28'), 
                    ('Vacuum', 'Living Room', 'weekly', 10, 4, '2024-10-5'),
                    ('Clean Kitchen', 'Kitchen', 'monthly', 30, 3, '2024-10-12');
                """
            ))
            
        return {"message": "Successfully reset all chores to default state"}
    except Exception as e:
        print(f"An error occurred during reset: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while resetting chores")
