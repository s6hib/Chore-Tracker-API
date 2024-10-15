## Example Flows

### Billy Assigns Extra Chores to Himself

Billy has a light school schedule this week and decided to take on more house chores. He uses the chore tracker to find the uncompleted high-priority chores. He starts by calling `GET /chores` and passes in the query parameters `status=not_complete` and `priority=high` to filter chores. The API returns a list of two chores: "Mop floors" and "Wash dishes."

Billy decides to assign both chores to himself. He calls `POST /roommates/2/chores` and passes in the `chore_id` for both "Mop floors" and "Wash dishes." With the chores now on his personal list, Billy decides to complete one chore before heading to class. He washes the dishes and, once finished, returns to the chore tracker to mark the task as completed. He calls `PATCH /chores/1003` with the request body `{ "status": "complete" }` to update the status of the "Wash dishes" chore.

The API responds with `"Chore status updated successfully."` Now, Billy’s roommates can see that the dishes have been washed, and he’ll mop the floors later.

### Sarah Tracks Roommate Productivity and Adds Lisa

Sarah is curious about how well her roommates have been managing their chores over the past month. She calls `GET /chores/history` and sets the date range to cover the past 30 days. The API responds with a list of completed chores, including details like the title, the person who completed the task, and the completion date. Sarah notices that Jake completed "Vacuum the living room" on the 5th, and Billy tackled "Clean kitchen" on the 12th.

Impressed with their effort, Sarah decides to add Lisa as a new roommate to help share the workload. She calls `POST /roommates` and provides Lisa’s first name, last name, and a list of chores to assign initially, such as "Take out trash." The system creates Lisa’s profile, and now she’s part of the household chore management.

After adding Lisa, Sarah realizes that the bathroom needs cleaning urgently. She calls `POST /chores` to create a new task titled "Clean the bathroom" with a high priority. She assigns the task to Lisa and sets the due date for the upcoming weekend. The API responds with `"Chore created and assigned to Lisa successfully."` Sarah feels accomplished, knowing the household is better organized.

### Mia Manages Shared Expenses and Creates a Bill

Mia has been keeping track of household expenses and realizes it’s time to split the recent electricity bill among her roommates. To ensure fairness, she creates a new bill using the chore tracker.

Mia starts by calling `POST /bills` with the total amount of $120 and includes her roommates’ IDs: Alice (ID: 1), Bob (ID: 2), and herself (ID: 3). She sets the due date for the bill to the end of the month. The API confirms that the bill has been successfully created and stored in the system.

After creating the bill, Mia calls `GET /bills` to view the current bills and ensure everything is recorded correctly. She sees the newly created electricity bill in the list, showing that each roommate owes $40.

A few days later, Mia receives payment from Alice, so she updates the payment status by calling `PATCH /bills/1/payments` and marking Alice's share as paid. The API responds with a success message.

Later, Bob informs Mia that he might need more time to pay his share. Mia decides to extend the due date for Bob’s payment and updates the bill by calling `PATCH /bills/1` to adjust the due date. The API confirms the update with a success message.

Thanks to the chore tracker, Mia stays on top of shared expenses, ensuring the financial burden is distributed fairly and no one falls behind on payments.
