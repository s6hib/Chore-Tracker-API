workflow 2. Sarah Tracks Roommate Productivity and Adds Lisa

Step 1: Sarah wants to see how her roommates have managed their chores over the past month. She calls GET /chores/history with a date range covering the last 30 days. The API responds with a list of completed chores, including the title, the person who completed it, and the date of completion. Sarah notices that Sue mopped the floors on the 27th, and Antony washed dished on the 27th.

GET Chore History
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/history' \
 -H 'accept: application/json' \
 -H 'access_token: a'

[
{
"title": "mop floors",
"completed_by": "sue sue",
"completion_date": "2024-10-27"
},
{
"title": "mop floors",
"completed_by": "sue sue",
"completion_date": "2024-10-27"
},
{
"title": "mop floors",
"completed_by": "sue sue",
"completion_date": "2024-10-27"
},
{
"title": "wash dishes",
"completed_by": "Antony LeGoat",
"completion_date": "2024-10-27"
}
]

Step 2: To help share the workload, Sarah adds a new roommate, Lisa. She calls POST /roommates with Lisa’s first name, last name, and an initial chore assignment: "Take out trash." The system creates Lisa’s profile, and she’s now part of the household chore management.

Create Roommate
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/create_roommates/' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
"first_name": "Lisa",
"last_name": "Smith",
"email": "Lsmith@gmail.com"
}'

Step 3: After adding Lisa, Sarah realises the bathroom needs immediate attention. She creates a new chore by calling POST /chores with the title "Clean the bathroom," setting a high priority, assigning it to Lisa, and adding a due date for the upcoming weekend. The API responds with "Chore created and assigned to Lisa successfully."

Create Chore
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/chores/create_chore' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Clean the bathroom",
"location_in_house": "bathroom",
"frequency": "weekly",
"duration_mins": 20,
"priority": 5,
"due_date": "2024-11-09"
}'

{
"message": "Chore Clean the bathroom created successully.",
"chore_id": 9
}

Assign Chore
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/chores/assign_chore/?chore_id=9&roommate_id=10' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -d ''
{
"chore_id": 9,
"roommate_id": 10,
"status": "pending"
}

workflow 3. Sue Manages Shared Expenses and Creates a Bill

Step 1: Sue needs to split the recent electricity bill among her roommates. She calls POST /bills with the total amount of $130 and includes all the roommate IDs in the house. She sets the due date for the bill at the end of the month. The API confirms the bill was created successfully.

Create Bill
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/bills/create_bill' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
"cost": 130,
"due_date": "2024-11-06",
"bill_type": "electricity",
"message": "pay for oct electricity!"
}'

{
"bill_id": 7,
"message": "Bill created and assigned to roommates."
}

Step 2: To verify everything is recorded, Sue calls GET /bills and sees the new electricity bill, showing that each roommate needs to pay the bill evenly.

GET Bills with specific bill_id
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/bills/7/assignments' \
 -H 'accept: application/json' \
 -H 'access_token: a'

{
"bill_id": 7,
"assignments": [
{
"roommate_id": 1,
"status": "unpaid",
"amount": 26
},
{
"roommate_id": 2,
"status": "unpaid",
"amount": 26
},
{
"roommate_id": 3,
"status": "unpaid",
"amount": 26
},
{
"roommate_id": 4,
"status": "unpaid",
"amount": 26
},
{
"roommate_id": 10,
"status": "unpaid",
"amount": 26
}
]
}

GET All Bills
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/bills/get_bill' \
 -H 'accept: application/json' \
 -H 'access_token: a'

[
{
"total_cost": 130,
"due_date": "2024-11-05T00:00:00+00:00",
"bill_type": "electricity",
"message": "pay for oct electricity!",
"roommate_id": 1,
"roommate_name": "Antony LeGoat",
"status": "unpaid"
},
{
total_cost": 130,
"due_date": "2024-11-05T00:00:00+00:00",
"bill_type": "electricity",
"message": "pay for oct electricity!",
"roommate_id": 2,
"roommate_name": "sue sue",
"status": "unpaid"
},
{
total_cost": 130,
"due_date": "2024-11-05T00:00:00+00:00",
"bill_type": "electricity",
"message": "pay for oct electricity!",
"roommate_id": 3,
"roommate_name": "Billy Bob",
"status": "unpaid"
},
{
total_cost": 130,
"due_date": "2024-11-05T00:00:00+00:00",
"bill_type": "electricity",
"message": "pay for oct electricity!",
"roommate_id": 4,
"roommate_name": "Lisa Olander",
"status": "unpaid"
},
{
total_cost": 130,
"due_date": "2024-11-05T00:00:00+00:00",
"bill_type": "electricity",
"message": "pay for oct electricity!",
"roommate_id": 10,
"roommate_name": "Lisa Smith",
"status": "unpaid"
}
]

Step 3: A few days later, Alice pays her share. Sue updates the payment status by calling PATCH /bills/1/payments and marking Antony's portion as paid. The API confirms the update with a success message.

UPDATE Bill Status
curl -X 'PATCH' \
 'https://chore-tracker-api.onrender.com/update_bill_status/2/payment' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
"roommate_id": 1,
"status": "paid"
}'

{
"message": "Payment status for roommate 1 on bill 4 updated to paid."
}

Step 4: Later, Bob tells Sue he needs more time to pay. Sue updates the due date by calling PATCH /bills/1 to extend the deadline. The API responds with a confirmation that the due date was successfully updated.

UPDATE BILL
curl -X 'PATCH' \
 'https://chore-tracker-api.onrender.com/update_bills/2' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
"due_date": "2024-12-01",
"cost": 120,
"bill_type": "electricity",
"message": "pay by updated due date"
}'

{
"message": "Bill ID: 4 is updated successfully."
}

With the chore tracker, Sue stays on top of household expenses, ensuring everyone pays their share and the financial burden is managed fairly.
