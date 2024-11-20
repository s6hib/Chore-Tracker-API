# API Specification

### 1. Create a Chore

**Endpoint:** `POST /create_chore`

**Description:** Creates a new chore and assigns it to a roommate with priority, location, frequency, duration(mins) and due date.

**Request Body:**

- **`name`**: *string* (required)  
  The name of the chore.

- **`location_in_house`**: *string* (required)  
  The location within the house where the chore should be performed.

- **`frequency`**: *enum* (required)  
  The frequency of the chore, represented by an enumeration (e.g., "daily", "weekly").

- **`duration_mins`**: *integer* (required)  
  The estimated time required to complete the chore, expressed in minutes.

- **`priority`**: *integer* (required)  
  The priority level of the chore, where `1` is the lowest and `5` is the highest. Must be an integer between 1 and 5.

- **`due_date`**: *string* (required)  
  The due date by which the chore should be completed, formatted as `YYYY-MM-DD`.


**Response:**

- `chore_id`: integer  
  The ID of the created chore.

- `message`: string  
  A confirmation message.

---

### 2. Get All Chores

**Endpoint:** `GET /get_chore`

**Description:** Retrieves a list of all chores, with an optional filter for priority.

**Request (Query Parameters):**

- **`priority`**: *integer* (1–5) (optional)  
  Filter chores based on their priority level. If not provided, chores of all priorities will be returned.

If no query parameters are provided, all chores will be returned.

**Response:**

- **`chores`**: *array of objects*  
  A list of chores that match the provided filters (if any).
  - **`name`**: *string*  
    The name of the chore.

  - **`location_in_house`**: *string*  
    The location within the house where the chore should be performed.

  - **`frequency`**: *string*  
    The frequency of the chore (e.g., "daily", "weekly").

  - **`duration`**: *integer*  
    The estimated time required to complete the chore, expressed in minutes.

  - **`priority`**: *integer*  
    The priority level of the chore (1–5).

  - **`due_date`**: *string*  
    The due date of the chore in the format `YYYY-MM-DD`.

---
## 3. Get Chore History

**Endpoint:** `GET /history`

**Description:** Retrieves a list of completed chores within the past 30 days, including details about who completed each chore and the completion date.

### **Response:**

- **`history`**: *array of objects*  
  A list of completed chores within the past 30 days.

  - **`title`**: *string*  
    The name of the chore.

  - **`completed_by`**: *string*  
    The full name of the roommate who completed the chore, in the format "First Last".

  - **`completion_date`**: *string*  
    The date when the chore was completed, formatted as `YYYY-MM-DD`.

---

### 4. Update Chore Assignment Status

**Endpoint:** `PATCH /{chore_id}/assignments/{roommate_id}/status`

**Description:** Updates the status of a specific chore assignment for a given roommate.

**Request (Path Parameters):**

- **`chore_id`**: *integer*  
  The unique identifier of the chore.

- **`roommate_id`**: *integer*  
  The unique identifier of the roommate assigned to the chore.

**Request Body:**

- **`status`**: *string*  
  The new status of the chore assignment. Allowed values are `pending`, `in_progress`, or `completed`.

**Response:**

- **`message`**: *string*  
  A confirmation message indicating the status update was successful.

- **`chore_id`**: *integer*  
  The ID of the chore that was updated.

- **`roommate_id`**: *integer*  
  The ID of the roommate assigned to the chore.

- **`new_status`**: *string*  
  The updated status of the chore assignment.

**Notes:**

- This endpoint updates only the status of an existing chore assignment.
- Ensure that `chore_id` and `roommate_id` correspond to an existing assignment to avoid errors.

---

### 5. Delete a Chore

**Endpoint:** `DELETE /chores/{id}`

**Description:** Deletes a specific chore from the system.

**Request (Path Parameter):**

- `id`: integer  
  The unique identifier of the chore to be deleted.

**Response:**

- `message`: string  
  A confirmation message indicating whether the chore was successfully deleted.
- `deleted_chore_id`: integer  
  The unique identifier of the deleted chore.

---

### 6. Add Comment to Chore

**Endpoint:** `POST /chores/{id}/comments`

**Description:** Adds a comment to a specific chore.

**Request (Path Parameter):**

- `id`: integer  
  The unique identifier of the chore to which the comment will be added.

**Request Body:**

- `comment_text`: string  
  The text of the comment to be added to the chore.
- `commenter_id`: integer  
  The ID of the roommate (same as `roommate_id`) who is adding the comment.

**Response:**

- `comment_id`: integer  
  The unique identifier of the created comment.
- `message`: string  
  A confirmation message indicating that the comment was successfully added.
- `timestamp`: string (YYYY-MM-DD)  
  The timestamp indicating when the comment was created.

---

### 7. Rotate Chore

**Endpoint:** `POST /chores/rotate_chore/`

**Description:** Rotates weekly chores amongst roommates.

**Request (Path Parameter):**

- **`chore_id`**: *integer*  
  The unique identifier of the chore.

- **`roommate_id`**: *integer*  
  The unique identifier of the roommate assigned to the chore.

**Response:**

- `message`: string  
  A confirmation message indicating that the chore was successfully rotated.
- `chore_id`: integer  
  The unique identifier of the chore that was rotated.
- `new_roommate_id`: integer  
  The unique identifier of the new roommate that the chore got assigned to.

---

### 8. Create Roommate

**Endpoint:** `POST /create_roommate`

**Description:** Creates a new roommate with the provided first name, last name, and email, and returns the details along with a unique roommate ID.

**Request Body:**

- **`first_name`**: *string* (required)  
  The first name of the new roommate.

- **`last_name`**: *string* (required)  
  The last name of the new roommate.

- **`email`**: *string* (required)  
  The email address of the new roommate.

**Response:**

- **`First Name`**: *string*  
  The first name of the newly created roommate.

- **`Last Name`**: *string*  
  The last name of the newly created roommate.

- **`Email`**: *string*  
  The email address of the newly created roommate.

- **`roommate id`**: *integer*  
  The unique identifier (ID) of the newly created roommate.

---

### 9. Assign Chore to Roommate

**Endpoint:** `POST /assign_chore/`

**Description:** Assigns an existing chore to a specified roommate and sets the assignment status to `pending`. If the chore or roommate does not exist, or if the assignment already exists, an error is returned.

**Request (Query Parameters):**

- **`chore_id`**: *integer* (required)  
  The unique identifier of the chore to be assigned.

- **`roommate_id`**: *integer* (required)  
  The unique identifier of the roommate to whom the chore is being assigned.

**Response:**

- **`chore_id`**: *integer*  
  The ID of the assigned chore.

- **`roommate_id`**: *integer*  
  The ID of the roommate to whom the chore is assigned.

- **`status`**: *string*  
  The initial status of the assignment, set to `pending`.

**Errors:**

- **404 Not Found**: Returned if either the `chore_id` or `roommate_id` does not exist in the database.
- **400 Bad Request**: Returned if the chore has already been assigned to the specified roommate.

**Notes:**

- This endpoint only allows assigning an existing chore to an existing roommate.
- The assignment status is initially set to `pending` upon successful assignment.

---

### 10. Get All Roommates

**Endpoint:** `GET /get_roommate`

**Description:** Retrieves a list of all roommates, including their first name, last name, and email address.

**Response:**

- **`roommates`**: *array of objects*  
  A list of roommates.

  - **`first_name`**: *string*  
    The first name of the roommate.

  - **`last_name`**: *string*  
    The last name of the roommate.

  - **`email`**: *string*  
    The email address of the roommate.

---

### 11. Get Chores by Roommate

**Endpoint:** `GET /roommates/{id}/chores`

**Description:** Retrieves all chores assigned to a specific roommate.

**Request (Path Parameter):**

- `id`: integer
  
  The unique identifier of the roommate whose chores are being retrieved.

**Response:**

- `chores`: array of objects  
  A list of chores assigned to the specified roommate.

  - `id`: integer  
    The unique identifier of the chore.
    
  - `title`: string  
    The title or short name of the chore.
    
  - `description`: string  
    A detailed description of the chore.
    
  - `priority`: integer  
    The priority level of the chore (1-5)
    
  - `duration`: integer  
    Estimated time in minutes required to complete the chore.
    
  - `due_date`: string (YYYY-MM-DD)  
    The date by which the chore must be completed.
    
  - `status`: string  
    The current status of the chore (e.g., "pending," "in-progress," "completed").

---

### 12. Create Bill

**Endpoint:** `POST /create_bill`

**Description:** Creates a new bill with a specified cost, due date, type, and message, then assigns the bill to all roommates, splitting the cost evenly among them.

**Request Body:**

- **`cost`**: *float* (required)  
  The total amount of the bill to be split among all roommates.

- **`due_date`**: *string* (required)  
  The due date for the bill, formatted as `YYYY-MM-DD`.

- **`bill_type`**: *enum* (required)  
  The type of bill (e.g., `electricity`, `rent`, `internet`).

- **`message`**: *string* (optional)  
  An optional message associated with the bill.

**Response:**

- **`bill_id`**: *integer*  
  The unique identifier for the created bill.

- **`message`**: *string*  
  A confirmation message indicating the bill has been created and assigned to all roommates.

**Notes:**

- The cost of the bill is divided evenly among all roommates in the database.
- Each roommate is assigned a portion of the bill with a status of `unpaid`.
- If there are no roommates, the request will fail with a `400 Bad Request` error.

---

### 13. Get All Bills

**Endpoint:** `GET /get_bill`

**Description:** Retrieves a list of all bills, including details about each bill's total cost, due date, type, message, and each roommate’s status and name associated with the bill.

**Response:**

- **`bills`**: *array of objects*  
  A list of bills with details for each assignment.

  - **`total_cost`**: *float*  
    The total amount of the bill.

  - **`due_date`**: *string*  
    The due date for the bill, formatted as `YYYY-MM-DD`.

  - **`bill_type`**: *string*  
    The type of the bill (e.g., `electricity`, `rent`, `internet`).

  - **`message`**: *string*  
    An optional message associated with the bill.

  - **`roommate_id`**: *integer*  
    The unique identifier for the roommate assigned to the bill.

  - **`roommate_name`**: *string*  
    The full name of the roommate assigned to the bill.

  - **`status`**: *string*  
    The payment status for the roommate's portion of the bill (e.g., `unpaid`, `paid`).

---

### 14. Get Bill Assignments

**Endpoint:** `GET /{bill_id}/assignments`

**Description:** Retrieves the payment assignments for a specific bill, including each roommate’s assigned amount and payment status.

**Request (Path Parameter):**

- **`bill_id`**: *integer* (required)  
  The unique identifier for the bill whose assignments are being retrieved.

**Response:**

- **`bill_id`**: *integer*  
  The ID of the specified bill.

- **`assignments`**: *array of objects*  
  A list of assignments for the bill, detailing each roommate's payment status and amount due.

  - **`roommate_id`**: *integer*  
    The unique identifier for the roommate assigned to this portion of the bill.

  - **`status`**: *string*  
    The payment status of the roommate's portion (e.g., `unpaid`, `paid`).

  - **`amount`**: *float*  
    The amount owed by the roommate for this bill.

**Errors:**

- **404 Not Found**: Returned if no assignments are found for the specified `bill_id`.

---
  
### 15. Update Bill Assignment Status

**Endpoint:** `PATCH /update_bill_list_status/{bill_id}/payments/{roommate_id}`

**Description:** Updates the payment status of a specific roommate’s assignment for a particular bill. If the status is updated to `paid`, the amount is set to `0`.

**Request (Path Parameters):**

- **`bill_id`**: *integer* (required)  
  The unique identifier for the bill.

- **`roommate_id`**: *integer* (required)  
  The unique identifier for the roommate assigned to the bill.

**Request Body:**

- **`status`**: *string* (required)  
  The new payment status for the roommate's assignment. Allowed values are `paid` or `unpaid`.

**Response:**

- **`message`**: *string*  
  A confirmation message indicating the status update was successful or if no matching bill was found.

**Errors:**

- **404 Not Found**: Returned if no bill assignment is found with the specified `bill_id` and `roommate_id`.

---

### 16. Update Bill Details

**Endpoint:** `PATCH /update_bill/{bill_id}`

**Description:** Updates specified fields for a particular bill, allowing for partial updates to the bill’s `due_date`, `bill_type`, or `message`.

**Request (Path Parameter):**

- **`bill_id`**: *integer* (required)  
  The unique identifier for the bill to be updated.

**Request Body (Partial Updates):**

You may include one or more of the following fields to update specific attributes of the bill:

- **`due_date`**: *string* (optional)  
  The new due date for the bill, formatted as `YYYY-MM-DD`.

- **`bill_type`**: *string* (optional)  
  The type of the bill (e.g., `electricity`, `rent`, `internet`).

- **`message`**: *string* (optional)  
  A new message or note associated with the bill.

**Response:**

- **`message`**: *string*  
  A confirmation message indicating the result of the update or if no changes were made.

**Errors:**

- **404 Not Found**: Returned if no bill is found with the specified `bill_id`.
- **400 Bad Request**: Returned if no update fields are provided in the request.

**Notes:**

- If no fields are provided in the request body, the update will not proceed, and a message will be returned indicating that no changes were made.

