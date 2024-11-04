from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bill",
    tags=["bill"],
    dependencies=[Depends(auth.get_api_key)],
)

class bill(BaseModel):
    cost: float
    due_date: datetime.date
    bill_type: str
    message: str
    roommate: str
    status: str

@router.get("/bills/", tags=["bill"])
def get_bills():
    with db.engine.begin() as connection:
       result = connection.execute(sqlalchemy.text(
            '''SELECT cost, due_date, bill_type, message,
            b.roommate_id, b.status
            FROM bill 
            JOIN bill_list b ON b.bill_id = bill.id''')).fetchall() 
       
    bill_list = []
            
    for bill in result:
        bill_list.append({
            "cost": bill.cost,
            "due_date": bill.due_date,
            "bill_type": bill.bill_type,
            "message": bill.message,
            "roommate_id": bill.roommate,
            "status": bill.status
            })
        print(bill)
        
    return bill_list

#@router.get("/bills/", tags=["bill"])
#def patch_bills():
    #with db.engine.begin() as connection:
       #result = connection.execute(sqlalchemy.text()).fetchall() 

