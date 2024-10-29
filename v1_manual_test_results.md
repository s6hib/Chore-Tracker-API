
1. Billy Assigns Extra Chores to Himself

Billy has a light school schedule this week and decided to take on more house chores. He uses the chore tracker to find the uncompleted high-priority chores. He starts by calling GET /chores and passes in the query parameters status=not_complete and priority=high to filter chores. The API returns a list of two chores: "Mop floors" and "Wash dishes."

Billy decides to assign both chores to himself. He calls POST /roommates/2/assignments and passes in the chore_id for both "Mop floors" and "Wash dishes." With the chores now on his personal list, Billy decides to complete one chore before heading to class. He washes the dishes and, once finished, returns to the chore tracker to mark the task as completed. He calls PATCH /chores/1003 with the request body { "status": "complete" } to update the status of the "Wash dishes" chore.

The API responds with "Chore status updated successfully." Now, Billy’s roommates can see that the dishes have been washed, and he’ll mop the floors later.

Get Chores:
curl -X 'GET' \
  'http://127.0.0.1:3000/chore/chores/' \
  -H 'accept: application/json' \
  -H 'access_token: a'

[
  {
    "name": "mop floors",
    "location_in_house": "All rooms",
    "frequency": "weekly",
    "duration": 25,
    "priority": 5,
    "due_date": "2024-10-27"
  },
  {
    "name": "wash dishes",
    "location_in_house": "kitchen",
    "frequency": "daily",
    "duration": 20,
    "priority": 5,
    "due_date": "2024-10-27"
  }
]

Assign Chores:
curl -X 'POST' \
  'http://127.0.0.1:3000/assign_chore/assign_chore/' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "chore_to_assign": {
    "name": "wash dishes",
    "location_in_house": "kitchen",
    "frequency": "daily",
    "duration_mins": 20,
    "priority": 5,
    "due_date": "2024-10-27"
  },
  "roommate_to_assign": {
    "first_name": "Billy",
    "last_name": "Bob",
    "email": "billybob@gmail.com"
  }
}'

{
  "chore_id": 2,
  "roommate": 3,
  "status": "pending"
}

curl -X 'POST' \
  'http://127.0.0.1:3000/assign_chore/assign_chore/' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "chore_to_assign": {
    "name": "mop floors",
    "location_in_house": "All rooms",
    "frequency": "weekly",
    "duration_mins": 25,
    "priority": 5,
    "due_date": "2024-10-27"
  },
  "roommate_to_assign": {
    "first_name": "Billy",
    "last_name": "Bob",
    "email": "billybob@gmail.com"
  }
}'

{
  "chore_id": 1,
  "roommate": 3,
  "status": "pending"
}


Update chore status:

  
