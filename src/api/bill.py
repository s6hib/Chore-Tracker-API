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
    prefix="",
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


@router.get("/get_bill/", tags=["bill"])
def get_bill():
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

class StatusEnum(str, Enum):
    unpaid = 'unpaid'
    paid = 'paid'
    overdue = 'overdue'

class PaymentUpdate(BaseModel):
    roommate_id: int
    status: StatusEnum

@router.patch("/update_bill_status/{bill_id}/payment", tags=["bill"])
def update_bill_status(bill_id: int, payment_update: PaymentUpdate):
    with db.engine.begin() as connection:     
       result = connection.execute(sqlalchemy.text(
           """
            UPDATE bill_list
            SET status =:status
            WHERE bill_id = :bill_id AND roommate_id = :roommate_id
            """

      ), {
          "bill_id" : bill_id, 
          "roommate_id" : payment_update.roommate_id,
          "status" : payment_update.status.value
        })
       if result.rowcount == 0:
           return {"message": "No bill found with the specified ID."}

    return {"message": f"Payment status for roommate {payment_update.roommate_id} on bill {bill_id} updated to {payment_update.status.value}."}

class BillUpdate(BaseModel):
    due_date: Optional[datetime.date] = None
    cost: Optional[float] = None
    bill_type: Optional[BillTypeEnum] = None
    message: Optional[str] = None

@router.patch("/update_bills/{bill_id}", tags=["bill"])
def update_bill(bill_id: int, bill_update: BillUpdate):
    update_fields = {}
    sql_set_clause = []

    if bill_update.due_date is not None:
        sql_set_clause.append("due_date =:due_date")
        update_fields["due_date"] = bill_update.due_date

    if bill_update.cost is not None:
        sql_set_clause.append("cost =:cost")
        update_fields["cost"] = bill_update.cost
    
    if bill_update.bill_type is not None:
        sql_set_clause.append("bill_type = :bill_type")
        update_fields["bill_type"] = bill_update.bill_type.value

    if bill_update.message is not None:
        sql_set_clause.append("message =:message")
        update_fields["message"] = bill_update.message
    
    if not sql_set_clause:
        return {"message": "You are not changing anything~"}

    sql_set_clause_str = ",".join(sql_set_clause)
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            f"""
            UPDATE bill
            SET {sql_set_clause_str}
            WHERE id = :bill_id
            """
        ), {
            "bill_id": bill_id, **update_fields
        })

        if result.rowcount == 0:
            return {"message": "There is no bill with the bill id you provided."}
    return {"message": f"Bill ID: {bill_id} is updated successfully."}