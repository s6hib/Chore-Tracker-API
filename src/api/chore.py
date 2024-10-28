import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/chore",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/chores/", tags=["chore"])
def get_chores():
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM chore")).fetchall()
            
    chores = [dict(row) for row in result]

    print(chores)
    return "OK"

