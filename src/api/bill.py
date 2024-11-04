from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import datetime
from enum import Enum
import sqlalchemy
from src import database as db
from src.api.roommate import Roommate
from typing import List, Optional

router = APIRouter(
    prefix="/bill",
    tags=["bill"],
    dependencies=[Depends(auth.get_api_key)],
)

class BillTypeEnum(str, Enum):
    electricity = 'electricity'
    water = 'water'
    internet = 'internet'
    rent = 'rent'
    gas = 'gas'
    trash = 'trash'
    groceries = 'groceries'

class Bill(BaseModel):
    cost: float
    due_date: datetime.date
    bill_type: BillTypeEnum
    message: Optional[str]

@router.post("/create_bill", tags=["bill"])
def create_bill(bill_to_assign: bill):
    with db.engine.begin() as connection:
        add_bill_query = connection.execute(sqlalchemy.text(
            """
            INSERT INTO bill(cost, due_date, bill_type, message)
            VALUES (:cost, :due_date, :bill_type, :message)
            RETURNING id;
            """
        ), 
        {
            "cost": bill_to_assign.cost,
            "due_date": bill_to_assign.due_date,
            "bill_type": bill_to_assign.bill_type.value,
            "message": bill_to_assign.message
        }
        )
        bill_id = add_bill_query.scalar_one()

        connection.execute(sqlalchemy.text(
            """
            INSERT INTO bill_list (roommate_id, bill_id, status)
            SELECT id, :bill_id, 'unpaid'
            FROM roommate
            """
        ),{
            "bill_id": bill_id
        })
            
    return {
        "bill_id": bill_id,
        "message": "Bill created and assigned to roommates."
    }   


@router.get("/bills/", tags=["bill"])
def get_bills():
    with db.engine.begin() as connection:
       result = connection.execute(sqlalchemy.text(
            '''SELECT cost, due_date, bill_type, message,
            b.roommate_id, b.status, (r.first_name || ' ' || r.last_name) AS fullname
            FROM bill 
            JOIN bill_list b ON b.bill_id = bill.id
            JOIN roommate r ON r.id = b.roommate_id ''')).fetchall() 

    bill_list = []

    for bill in result:
        bill_list.append({
            "cost": bill.cost,
            "due_date": bill.due_date,
            "bill_type": bill.bill_type,
            "message": bill.message,
            "roommate_id": bill.roommate_id,
            "roommate_name": bill.fullname,
            "status": bill.status
            })
        print(bill)

    return bill_list


#@router.get("/bills/", tags=["bill"])
#def patch_bills():
    #with db.engine.begin() as connection:
       #result = connection.execute(sqlalchemy.text(
      # '''UPDATE bill SET due_date?

      # '''))
       
   
