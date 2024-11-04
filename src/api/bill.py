from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src.api.roommate import Roommate
from src.api.chore import Chore

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bill",
    tags=["bill"],
    dependencies=[Depends(auth.get_api_key)],
)

class bill(BaseModel):
    bill_type: str
    due_date: str
    roommate: str
    status: str