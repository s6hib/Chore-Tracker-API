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
    1. Deletes everything from the tables
    """
    try:
        with db.engine.begin() as connection:
            # first delete all chore assignments (due to foreign key constraint)
            connection.execute(sqlalchemy.text(
                """
                TRUNCATE TABLE chore_assignment;
                TRUNCATE TABLE roommate;
                TRUNCATE TABLE bill;
                TRUNCATE TABLE bill_list;
                """
            ))
            
            # then delete all chores
            connection.execute(sqlalchemy.text(
                """
                TRUNCATE TABLE chore;
                """
            ))
            
            
        return {"message": "Successfully reset all chores to default state"}
    except Exception as e:
        print(f"An error occurred during reset: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while resetting chores")
