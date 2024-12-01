from fastapi import HTTPException, APIRouter, Depends, Path
from pydantic import BaseModel, Field
from src.api import auth
import datetime
from enum import Enum
import sqlalchemy
from src import database as db
from src.api.roommate import Roommate
from typing import Optional

import math

router = APIRouter(
    prefix="/bills",
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
    # TEMPORARY COMMENT TO EXPLAIN THE NEW CHANGE REGARDING VALIDATION, WILL REMOVE LATER:

    # Field(...): Adds additional constraints and metadata to the cost field
    # ...: indicates the field is required (no default value at the moment)
    # gt=0: ensures the cost value must be greater than 0
    # description: take a guess what this field is for :P
    cost: float = Field(..., gt=0, description="Bill cost must be greater than 0")
    due_date: datetime.date
    bill_type: BillTypeEnum
    message: Optional[str]

@router.post("/")
def create_bill(bill_to_assign: Bill):
    try:
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

            roommates = connection.execute(sqlalchemy.text(
                """
                SELECT id FROM roommate
                """
            )).fetchall()

            num_roommates = len(roommates)
            if num_roommates == 0:
                raise HTTPException(status_code=400, detail="No roommates found to assign the bill.")
            cost_per_roommate = bill_to_assign.cost / num_roommates

            cost_per_roommate_rounded_down = math.floor(cost_per_roommate * 100) / 100

            cost_per_roommate_rounded_up = math.ceil(cost_per_roommate * 100) / 100

            cents_over_cost = round((cost_per_roommate_rounded_up * num_roommates - bill_to_assign.cost) * 100)

            print(f"cents over cost {cents_over_cost}")

            for roommate in roommates:
                if cents_over_cost > 0:
                    cost = cost_per_roommate_rounded_down
                    cents_over_cost -= 1
                else:
                    cost = cost_per_roommate_rounded_up
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO bill_list (roommate_id, bill_id, status, amount)
                    VALUES (:roommate_id, :bill_id, 'unpaid', :cost_per_roommate)
                    """
                    ),{
                        "roommate_id": roommate.id,
                        "bill_id": bill_id,
                        "cost_per_roommate" : cost
                    })

            print(f"cost per roommate {cost_per_roommate}")
                
        return {
            "status": "success",
            "data": {"bill_id": bill_id},
            "message": "Bill created and assigned to roommates."
        }   
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a new bill")

@router.get("/", tags=["bill"])
def get_bills():
    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                '''SELECT cost AS total_cost, due_date, bill_type, message,
                b.roommate_id, b.status, (r.first_name || ' ' || r.last_name) AS fullname
                FROM bill 
                JOIN bill_list b ON b.bill_id = bill.id
                JOIN roommate r ON r.id = b.roommate_id ''')).fetchall() 

        if not result:
            return {
                "status": "success",
                "data": [],
                "message": "No bills found"
            }

        bill_list = []
        for bill in result:
            bill_list.append({
                "total_cost": bill.total_cost,
                "due_date": bill.due_date,
                "bill_type": bill.bill_type,
                "message": bill.message,
                "roommate_id": bill.roommate_id,
                "roommate_name": bill.fullname,
                "status": bill.status
                })
            print(bill)

        return {
            "status": "success",
            "data": bill_list,
            "message": None
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting all bills")

@router.get("/{bill_id}/assignments")
def get_bill_assignments(
    bill_id: int = Path(..., gt=0, description="The ID of the bill to get assignments for")
):
    try:
        with db.engine.begin() as connection:
            # Query all assignments for the specified bill_id
            result = connection.execute(sqlalchemy.text(
                """
                SELECT roommate_id, status, amount
                FROM bill_list
                WHERE bill_id = :bill_id
                """
            ), {"bill_id": bill_id}).fetchall()

            # If no assignments are found, return an error
            if not result:
                raise HTTPException(status_code=404, detail="No assignments found for this bill.")
        
        bill_assignments = []
        for bill in result:
            bill_assignments.append({
                "roommate_id": bill.roommate_id,
                "status": bill.status,
                "amount": bill.amount
            })

        print(bill_assignments)
        
        return {
            "status": "success",
            "data": {"bill_id": bill_id, "assignments": bill_assignments},
            "message": None
        }
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting bill assignments")

class StatusEnum(str, Enum):
    unpaid = 'unpaid'
    paid = 'paid'
    overdue = 'overdue'

class PaymentUpdate(BaseModel):
    status: StatusEnum

@router.patch("/{bill_id}/payments/{roommate_id}")
def update_bill_list_status(
    bill_id: int = Path(..., gt=0, description="The ID of the bill to update"),
    roommate_id: int = Path(..., gt=0, description="The ID of the roommate to update"),
    payment_update: PaymentUpdate = None
):
    try:
        with db.engine.begin() as connection:     
            # validate bill_id and roommate_id exist
            exists = connection.execute(sqlalchemy.text(
                """
                SELECT 1 FROM bill_list 
                WHERE bill_id = :bill_id AND roommate_id = :roommate_id
                """
            ), {
                "bill_id": bill_id,
                "roommate_id": roommate_id
            }).first()
            
            if not exists:
                raise HTTPException(status_code=404, detail="Bill assignment not found for the specified bill and roommate")

            result = connection.execute(sqlalchemy.text(
            """
                UPDATE bill_list
                SET status =:status,
                    amount = CASE WHEN :status = 'paid' THEN 0 ELSE amount END
                WHERE bill_id = :bill_id AND roommate_id = :roommate_id
                """
            ), {
                "bill_id" : bill_id, 
                "roommate_id" : roommate_id,
                "status" : payment_update.status.value
            })

        return {
            "status": "success",
            "data": None,
            "message": f"Payment status for roommate id {roommate_id} on bill id {bill_id} updated to {payment_update.status.value}."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the bill status")


class BillUpdate(BaseModel):
    due_date: Optional[datetime.date] = Field(None, example="YYYY-MM-DD")  # Placeholder for date
    #cost: Optional[float] = Field(None, example=0.0)  # Placeholder for a cost value
    bill_type: Optional[BillTypeEnum] = Field(None, example="string")  # Placeholder for Enum
    message: Optional[str] = Field(None, example="string")  # Placeholder for a message

    class Config:
        schema_extra = {
            "example": {
                "due_date": "2024-12-31",      # Example date format
                #"cost": 0.0,                 # Example cost
                "bill_type": "string",         # Placeholder to show it's a string field
                "message": "string"            # Placeholder for a generic text field
            }
        }

@router.patch("/bills/{bill_id}", response_model=dict)
def update_bill(
    bill_id: int = Path(..., gt=0, description="The ID of the bill to update"),
    bill_update: BillUpdate = None
):
    update_fields = {}
    sql_set_clause = []

    if bill_update.due_date is not None:
        sql_set_clause.append("due_date =:due_date")
        update_fields["due_date"] = bill_update.due_date

    # if bill_update.cost is not None:
    #     sql_set_clause.append("cost =:cost")
    #     update_fields["cost"] = bill_update.cost
    
    if bill_update.bill_type is not None:
        sql_set_clause.append("bill_type = :bill_type")
        update_fields["bill_type"] = bill_update.bill_type.value

    if bill_update.message is not None:
        sql_set_clause.append("message =:message")
        update_fields["message"] = bill_update.message
    
    if not sql_set_clause:
        return {
            "status": "success",
            "data": None,
            "message": "No changes requested"
        }

    sql_set_clause_str = ",".join(sql_set_clause)
    
    try:
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
                raise HTTPException(status_code=404, detail="No bill found with the specified ID")

        return {
            "status": "success",
            "data": None,
            "message": f"Bill ID: {bill_id} updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the bill information")
