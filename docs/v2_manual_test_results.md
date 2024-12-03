# Workflow 2: Sarah Tracks Roommate Productivity and Adds Lisa

### Step 1: Retrieve Chore History
Sarah wants to see how her roommates managed their chores over the past month. She calls the `GET /chores/history` endpoint with a date range covering the last 30 days. The API responds with a list of completed chores, including the title, the person who completed it, and the date of completion.

**GET Chore History Request:**
```bash
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/history' \
 -H 'accept: application/json' \
 -H 'access_token: a'
```

**Response:**
```json
[
  {
    "title": "mop floors",
    "completed_by": "Sue Sue",
    "completion_date": "2024-10-27"
  },
  {
    "title": "wash dishes",
    "completed_by": "Antony LeGoat",
    "completion_date": "2024-10-27"
  }
]
```

### Step 2: Add a New Roommate
To help share the workload, Sarah adds a new roommate, Lisa, with an initial chore assignment of "Take out trash." She calls the `POST /roommates` endpoint with Lisa's details.

**Create Roommate Request:**
```bash
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
```

### Step 3: Assign a New Chore
Sarah creates a new chore, "Clean the bathroom," assigning it to Lisa with a high priority and a due date for the upcoming weekend.

**Create Chore Request:**
```bash
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
```

**Response:**
```json
{
  "message": "Chore 'Clean the bathroom' created successfully.",
  "chore_id": 9
}
```

**Assign Chore Request:**
```bash
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/chores/assign_chore/?chore_id=9&roommate_id=10' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -d ''
```

**Response:**
```json
{
  "chore_id": 9,
  "roommate_id": 10,
  "status": "pending"
}
```

---

# Workflow 3: Sue Manages Shared Expenses and Creates a Bill

### Step 1: Create a New Bill
Sue needs to split the recent electricity bill among her roommates. She calls `POST /bills` with the total amount of $130, the due date, and includes all roommate IDs.

**Create Bill Request:**
```bash
curl -X 'POST' \
 'https://chore-tracker-api.onrender.com/bills/create_bill' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
       "cost": 130,
       "due_date": "2024-11-06",
       "bill_type": "electricity",
       "message": "pay for Oct electricity!"
     }'
```

**Response:**
```json
{
  "bill_id": 2,
  "message": "Bill created and assigned to roommates."
}
```

### Step 2: Retrieve Bill Assignments
Sue calls `GET /bills` to see the new electricity bill and verify each roommate's payment amount.

**GET Bill Assignments Request:**
```bash
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/bills/7/assignments' \
 -H 'accept: application/json' \
 -H 'access_token: a'
```

**Response:**
```json
{
  "bill_id": 2,
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
```

### Step 3: Retrieve All Bills
Sue retrieves all bills to confirm details like the due date and total cost.

**GET All Bills Request:**
```bash
curl -X 'GET' \
 'https://chore-tracker-api.onrender.com/bills/get_bill' \
 -H 'accept: application/json' \
 -H 'access_token: a'
```

**Response:**
```json
[
  {
    "total_cost": 130,
    "due_date": "2024-11-05T00:00:00+00:00",
    "bill_type": "electricity",
    "message": "pay for Oct electricity!",
    "roommate_id": 1,
    "roommate_name": "Antony LeGoat",
    "status": "unpaid"
  },
  {
    "total_cost": 130,
    "due_date": "2024-11-05T00:00:00+00:00",
    "bill_type": "electricity",
    "message": "pay for Oct electricity!",
    "roommate_id": 2,
    "roommate_name": "Sue Sue",
    "status": "unpaid"
  },
  {
    "total_cost": 130,
    "due_date": "2024-11-05T00:00:00+00:00",
    "bill_type": "electricity",
    "message": "pay for Oct electricity!",
    "roommate_id": 3,
    "roommate_name": "Billy Bob",
    "status": "unpaid"
  },
  {
    "total_cost": 130,
    "due_date": "2024-11-05T00:00:00+00:00",
    "bill_type": "electricity",
    "message": "pay for Oct electricity!",
    "roommate_id": 4,
    "roommate_name": "Lisa Olander",
    "status": "unpaid"
  },
  {
    "total_cost": 130,
    "due_date": "2024-11-05T00:00:00+00:00",
    "bill_type": "electricity",
    "message": "pay for Oct electricity!",
    "roommate_id": 10,
    "roommate_name": "Lisa Smith",
    "status": "unpaid"
  }
]
```

### Step 4: Update Payment Status
A few days later, Antony pays his share. Sue updates his payment status by calling `PATCH /bills/update_bill_list_status/2/payment/1`.

**Update Payment Status Request:**
```bash
curl -X 'PATCH' \
 'https://chore-tracker-api.onrender.com/update_bill_list_status/2/payment/1' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
       "status": "paid"
     }'
```

**Response:**
```json
{
  "message": "Payment status for roommate 3 on bill 2 updated to paid."
}
```

### Step 5: Update Bill Type
Later, Sue realizes the bill type is incorrect and changes it from electricity to gas.

**Update Bill Type Request:**
```bash
curl -X 'PATCH' \
 'https://chore-tracker-api.onrender.com/update_bills/2' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -H 'Content-Type: application/json' \
 -d '{
       "due_date": "2024-12-01",
       "bill_type": "gas",
       "message": "pay by due date"
     }'
```

**Response:**
```json
{
  "message": "Bill ID: 2 is updated successfully."
}
```

With this chore and expense tracker, Sue efficiently manages household responsibilities, ensuring fair expense distribution and tracking of chore assignments.
