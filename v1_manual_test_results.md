1. Billy Assigns Extra Chores to Himself

Billy has a light school schedule this week and decides to take on more house chores. He uses the chore tracker to find high-priority chores that are not yet completed. He starts by calling the GET /chore/chores/ endpoint with the query parameters status=not_complete and priority=high to filter for uncompleted, high-priority chores. The API responds with a list of two chores: "Mop floors" and "Wash dishes."

Billy decides to assign both chores to himself. He makes two separate requests to the POST /chores/assign_chore/ endpoint, passing in the details for each chore and specifying himself as the roommate to assign the chores to. For each request, he includes the chore details (such as "Mop floors" or "Wash dishes") along with his own information, which the API uses to assign these chores to him. Both chores are now on his personal list with a status of "pending."

After washing the dishes, Billy goes back to the chore tracker to mark the "Wash dishes" task as completed. He calls the PATCH /chores/{chore_id}/assignments/{roommate_id}/status endpoint, passing in chore_id=2 and his roommate_id=3 in the query parameters to specify the completed chore. The API responds with "Chore status updated successfully," indicating that the task has been marked as complete.

Now, Billy’s roommates can see that he has washed the dishes, and he’ll get to mopping the floors later.

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
  'http://127.0.0.1:8000/chores/assign_chore/?chore_id=1&roommate_id=1' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''

{
  "chore_id": 2,
  "roommate_id": 3,
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

curl -X 'POST' \
 'http://127.0.0.1:3000/assign_chore/update_chore_status/?chore_id=1&roommate_id=2' \
 -H 'accept: application/json' \
 -H 'access_token: a' \
 -d ''

{
"chore_id": 2,
"roommate_id": 3,
"status": "completed"
}
