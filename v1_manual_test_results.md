1. Billy Assigns Extra Chores to Himself


Step 1: Billy has a light school schedule this week and decides to take on more house chores. He uses the chore tracker to find high-priority chores. He starts by calling the GET /chore/get_chores/ endpoint with the query parameters priority=5 to filter for high-priority chores. The API responds with a list of three chores: "Mop floors", "Wash dishes", and "clean the bathroom" that have the priority number = 5.  

Get Chores with specific priority number:
curl -X 'GET' \
  'https://chore-tracker-api.onrender.com/chores/get_chore?priority=5' \
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
  },
  {
    "name": "Clean the bathroom",
    "location_in_house": "bathroom",
    "frequency": "weekly",
    "duration": 20,
    "priority": 5,
    "due_date": "2024-11-09"
  }
]

Get All Chores: 
curl -X 'GET' \
  'https://chore-tracker-api.onrender.com/chores/get_chore' \
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
  },
  {
    "name": "take out trash",
    "location_in_house": "kitchen",
    "frequency": "daily",
    "duration": 5,
    "priority": 1,
    "due_date": "2024-11-07"
  },
  {
    "name": "clean your room",
    "location_in_house": "bedroom",
    "frequency": "weekly",
    "duration": 30,
    "priority": 1,
    "due_date": "2024-11-05"
  },
  {
    "name": "mop your room",
    "location_in_house": "bedroom",
    "frequency": "weekly",
    "duration": 30,
    "priority": 1,
    "due_date": "2024-11-05"
  },
  {
    "name": "Clean the bathroom",
    "location_in_house": "bathroom",
    "frequency": "weekly",
    "duration": 20,
    "priority": 5,
    "due_date": "2024-11-09"
  }
]

Step 2: Billy decides to assign both chores to himself. He calls POST /chores/assign_chore/ endpoint, passing in the details for each chore and specifying himself as the roommate to assign the chores to. For each request, he includes the chore_id along with his roommate_id, which the API uses to assign these chores to him. Both chores are now on his personal list with a status of "pending."

Assign Chores:
curl -X 'POST' \
  'https://chore-tracker-api.onrender.com/chores/assign_chore/?chore_id=2&roommate_id=3' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''

{
  "chore_id": 2,
  "roommate_id": 3,
  "status": "pending"
}

Step 3: After washing the dishes, Billy goes back to the chore tracker to mark the "Wash dishes" task as completed. He calls the PATCH /chores/{chore_id}/assignments/{roommate_id}/status endpoint, passing in chore_id=2 and his roommate_id=3 in the query parameters to specify the completed chore. The API responds with "Chore status updated successfully," indicating that the task has been marked as complete.
Update chore status:

curl -X 'PATCH' \
  'https://chore-tracker-api.onrender.com/chores/2/assignments/3/status' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "completed"
}'

{
  "message": "Chore status updated successfully!",
  "chore_id": 2,
  "roommate_id": 3,
  "new_status": "completed"
}

Now, Billy’s roommates can see that he has washed the dishes, and he’ll get to mopping the floors later.