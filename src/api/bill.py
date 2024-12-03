from fastapi import HTTPException, APIRouter, Depends, Path
from pydantic import BaseModel, Field
from src.api import auth
import datetime
from enum import Enum
import sqlalchemy
from src import database as db
from typing import Optional

import math
import time

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
def create_bill(cost: float = 0.50, #= Path(..., gt=0, description="Bill cost must be greater than 0"), 
                due_date: datetime.date = datetime.date.today(), 
                bill_type: BillTypeEnum = '', 
                message: Optional[str] = ''):
    
    start_time = time.time()

    if (bill_type != "electricity" and bill_type != "water" and bill_type != "internet"
        and bill_type != "rent" and bill_type != "gas" and bill_type != "trash" and bill_type != "groceries"):
        raise HTTPException(status_code=400, detail="Bill_type must be one of these: electricity, water, internet, rent, gas, trash, or groceries")
    
    if (cost <=0):
        raise HTTPException(status_code=400, detail="Bill cost must be greater than 0")

    with db.engine.begin() as connection:
        add_bill_query = connection.execute(sqlalchemy.text(
            """
            INSERT INTO bill(cost, due_date, bill_type, message)
            VALUES (:cost, :due_date, :bill_type, :message)
            RETURNING id;
            """
        ), 
        {
            "cost": cost,
            "due_date": due_date,
            "bill_type": bill_type,
            "message": message
        }
        )
        bill_id = add_bill_query.scalar_one()

        # Get all roommates and check if any exist
        roommates_result = connection.execute(sqlalchemy.text(
            """
            SELECT id FROM roommate
            """
        ))
        
        if roommates_result.rowcount == 0:
            raise HTTPException(status_code=400, detail="No roommates found to assign the bill.")

        # Fetch all roommates for processing
        roommates = roommates_result.fetchall()
        cost_per_roommate = cost / roommates_result.rowcount

        cost_per_roommate_rounded_down = math.floor(cost_per_roommate * 100) / 100
        cost_per_roommate_rounded_up = math.ceil(cost_per_roommate * 100) / 100
        cents_over_cost = round((cost_per_roommate_rounded_up * roommates_result.rowcount - cost) * 100)

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

    end_time = time.time()  # End the timer
    execution_time = (end_time - start_time) * 1000  # Time in milliseconds
    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
            
    return {
        "status": "success",
        "data": {"bill_id": bill_id},
        "message": "Bill created and assigned to roommates."
    }   

@router.get("/")
def get_bills():
    start_time = time.time()
    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                '''SELECT id AS bill_id, cost AS total_cost, due_date, bill_type, message
                FROM bill
                ORDER BY due_date''')).fetchall() 

        if not result:
            return {
                "status": "success",
                "data": [],
                "message": "No bills found"
            }

        bill_list = []
        for bill in result:
            bill_list.append({
                "bill_id": bill.bill_id,
                "total_cost": bill.total_cost,
                "due_date": bill.due_date,
                "bill_type": bill.bill_type,
                "message": bill.message
                })
           
        
        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

        return {
            "status": "success",
            "data": bill_list,
            "message": "Get all the bills in the database!"
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while getting all bills")

@router.get("/{bill_id}/assignments")
def get_bill_assignments(
    bill_id: int = Path(..., gt=0, description="The ID of the bill to get assignments for")):

    start_time = time.time()

    with db.engine.begin() as connection:
        # Query all assignments for the specified bill_id
        result = connection.execute(sqlalchemy.text(
            """
            SELECT roommate_id, CONCAT(first_name, ' ', last_name) AS full_name, status, amount
            FROM bill_list
            JOIN roommate
                ON roommate.id = bill_list.roommate_id
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
            "name": bill.full_name,
            "status": bill.status,
            "amount": bill.amount
        })

    print(bill_assignments)

    end_time = time.time()  # End the timer
    execution_time = (end_time - start_time) * 1000  # Time in milliseconds
    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")
    
    return {
        "status": "success",
        "data": {"bill_id": bill_id, "assignments": bill_assignments},
        "message": f"Get all the bill assignments of bill id: {bill_id}"
    }

class StatusEnum(str, Enum):
    unpaid = 'unpaid'
    paid = 'paid'
    overdue = 'overdue'


@router.patch("/{bill_id}/payments/{roommate_id}")
def update_bill_list_status(
    bill_id: int = Path(..., gt=0, description="The ID of the bill to update"),
    roommate_id: int = Path(..., gt=0, description="The ID of the roommate to update"),
    payment_update: StatusEnum = ''
):
    
    start_time = time.time()

    if (payment_update != "paid" and payment_update != "unpaid" and payment_update != "overdue"):
        raise HTTPException(status_code=400, detail="payment_update must be one of these: unpaid, paid, overdue")

    with db.engine.begin() as connection:     
        # Check both IDs first and collect any errors
        validation_errors = []
        
        # Check if bill exists
        bill_exists = connection.execute(sqlalchemy.text(
            """
            SELECT 1 FROM bill 
            WHERE id = :bill_id
            """
        ), {
            "bill_id": bill_id
        }).first()
        
        if not bill_exists:
            validation_errors.append(f"Bill with ID {bill_id} not found")

        # Check if roommate exists
        roommate_exists = connection.execute(sqlalchemy.text(
            """
            SELECT 1 FROM roommate 
            WHERE id = :roommate_id
            """
        ), {
            "roommate_id": roommate_id
        }).first()
        
        if not roommate_exists:
            validation_errors.append(f"Roommate with ID {roommate_id} not found")

        # If we have any validation errors, raise them now
        if validation_errors:
            raise HTTPException(status_code=404, detail=". ".join(validation_errors))

        # Only check for assignment if both IDs exist
        assignment_exists = connection.execute(sqlalchemy.text(
            """
            SELECT 1 FROM bill_list 
            WHERE bill_id = :bill_id AND roommate_id = :roommate_id
            """
        ), {
            "bill_id": bill_id,
            "roommate_id": roommate_id
        }).first()
        
        if not assignment_exists:
            raise HTTPException(status_code=404, detail=f"No bill assignment found for bill ID {bill_id} and roommate ID {roommate_id}")

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
            "status" : payment_update
        })

    end_time = time.time()  # End the timer
    execution_time = (end_time - start_time) * 1000  # Time in milliseconds
    print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

    return {
        "status": "success",
        "data": None,
        "message": f"Payment status for roommate id {roommate_id} on bill id {bill_id} updated to {payment_update}."
    }


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
    due_date: datetime.date = datetime.date.today(),
    bill_type: BillTypeEnum = '',
    message: str = ''
):
    start_time = time.time()

    if (bill_type != "electricity" and bill_type != "water" and bill_type != "internet"
        and bill_type != "rent" and bill_type != "gas" and bill_type != "trash" and bill_type != "groceries"):
        raise HTTPException(status_code=400, detail="Bill_type must be one of these: electricity, water, internet, rent, gas, trash, or groceries")
    
    update_fields = {}
    sql_set_clause = []

    if due_date is not None:
        sql_set_clause.append("due_date =:due_date")
        update_fields["due_date"] = due_date

    # if cost is not None:
    #     sql_set_clause.append("cost =:cost")
    #     update_fields["cost"] = cost
    
    if bill_type is not None:
        sql_set_clause.append("bill_type = :bill_type")
        update_fields["bill_type"] = bill_type

    if message is not None:
        sql_set_clause.append("message =:message")
        update_fields["message"] = message
    
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

        end_time = time.time()  # End the timer
        execution_time = (end_time - start_time) * 1000  # Time in milliseconds
        print(f" Endpoint Name Execution Time: {execution_time:.2f} ms")

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
