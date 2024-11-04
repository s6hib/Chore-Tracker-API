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
    bill_type: str
    message: str
    roommate: str
    status: str

@router.post("/create_bill", tags=["bill"])
def create_bill(bill_to_assign: Bill):
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
        bill_id = add_bill_query.scalar_one

        
        add_bill_list_query = connection.execute(sqlalchemy.text(
            """
            INSERT INTO bill_list(bill_id, roommate_id, status)
            VALUES (:bill_id, :roommate_id, :status)
            """
        ){
            "bill_id": bill_id,
            "roommate_id": roommate_id,
            "status": "unpaid"
        })
            
    return {
        "bill_id": bill_id,
        "message": "Bill created and assigned to roommates."
    }   

        