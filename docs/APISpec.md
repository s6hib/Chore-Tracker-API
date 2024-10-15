# API Specification

### 1. Create a Chore

**Endpoint:** `POST /chores`

**Request Body:**

- `title`: string  
  The name of the chore.

- `description`: string  
  A detailed description of the chore.

- `priority`: integer (1–5)  
  The priority level of the chore, where `1` is the lowest and `5` is the highest.

- `duration`: integer (minutes)  
  The estimated time required to complete the chore, expressed in minutes.

- `due_date`: string (YYYY-MM-DD)  
  The due date by which the chore should be completed.

- `assignee_id`: integer  
  The ID of the roommate assigned to this chore.

**Response:**

- `chore_id`: integer  
  The ID of the created chore.

- `message`: string  
  A confirmation message.

---

### 2. Get All Chores

**Endpoint:** `GET /chores`

**Request Query Parameters:**

- `status`: string (optional)  
  Filter chores based on their current status. Predefined values: `pending`, `in_progress`, `completed`. If not provided, chores of all statuses will be returned.

- `assignee_name`: string (optional)  
  Filter chores by the name of the assigned roommate. If provided, this will search based on the assignee's full name.

- `assignee_id`: integer (optional)  
  Filter chores by the `assignee_id` of the assigned roommate. If provided, this will search based on the ID of the assigned roommate.

- `priority`: integer (optional)  
  Filter chores based on their priority level. If not provided, chores of all priorities will be returned.

If no query parameters are provided, all chores will be returned.

**Response:**

- `chores`: array of objects  
  A list of chores that match the provided filters (if any).
  - `id`: integer  
    The unique identifier for the chore.

  - `title`: string  
    The title of the chore.

  - `description`: string  
    A detailed description of the chore.

  - `priority`: integer  
    The priority level of the chore (1–5).

  - `duration`: integer  
    The estimated duration of the chore, expressed in minutes.

  - `due_date`: string  
    The due date of the chore (YYYY-MM-DD).

  - `status`: string  
    The current status of the chore. Predefined values: `pending`, `in_progress`, `completed`.

  - `assignee_id`: integer  
    The ID of the roommate assigned to the chore.

---

### 3. Get Specific Chore

**Endpoint:** `GET /chores/{id}`

**Request Path Parameter:**

- `id`: integer  
  The unique identifier of the chore to be retrieved.

**Response:**

- `id`: integer  
  The unique identifier for the chore.
- `title`: string  
  The title of the chore.
- `description`: string  
  A detailed description of the chore.
- `priority`: integer  
  The priority level of the chore (1–5).
- `duration`: integer  
  The estimated time required to complete the chore, expressed in minutes.
- `due_date`: string  
  The due date by which the chore should be completed (YYYY-MM-DD).
- `status`: string  
  The current status of the chore. Predefined values: `pending`, `in_progress`, `completed`.
- `assignee_id`: integer  
  The ID of the roommate assigned to the chore.
- `comments`: array of objects  
  A list of comments associated with the chore.
  - `comment_text`: string  
    The text of the comment.
  - `commenter_id`: integer  
    The ID of the roommate who made the comment.

---

### 4. Update a Chore

**Endpoint:** `PATCH /chores/{id}`

**Request Path Parameter:**

- `id`: integer  
  The unique identifier of the chore to be updated.

**Request Body:**

The request body supports partial updates. You may include one or more of the following fields to update only specific attributes of the chore:

- `title`: string  
  The name of the chore.
- `description`: string  
  A detailed description of the chore.
- `priority`: integer (1–5)  
  The priority level of the chore, where `1` is the lowest and `5` is the highest.
- `duration`: integer (minutes)  
  The estimated time required to complete the chore, expressed in minutes.
- `due_date`: string (YYYY-MM-DD)  
  The due date by which the chore should be completed.
- `status`: string  
  The current status of the chore. Predefined values: `pending`, `in_progress`, `completed`.

**Response:**

- `message`: string  
  A confirmation message indicating the result of the update.
- `updated_fields`: array of strings  
  A list of the fields that were updated.

---

### 5. Delete a Chore

**Endpoint:** `DELETE /chores/{id}`

**Request Path Parameter:**

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

**Request Path Parameter:**

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

### 7. Create a Roommate

**Endpoint:** `POST /roommates`

**Request Body:**

- `first_name`: string  
  The first name of the roommate to be created.
- `last_name`: string  
  The last name of the roommate to be created.
- `chores`: array of integers (optional)  
  A list of chore IDs that this roommate is responsible for. If this array is empty or not provided, the roommate will initially have no assigned chores.

  **Note:** If chores are assigned during roommate creation, the API will verify the validity of each chore ID. If any chore ID is invalid or already assigned to another roommate, an error will be returned.

**Response:**

- `roommate_id`: integer  
  The unique identifier of the created roommate.
- `message`: string  
  A confirmation message indicating that the roommate was successfully created.

---

### 8. Assign Chore to Roommate

**Endpoint:** `POST /roommates/{id}/assignments`

**Request Path Parameter:**

- `id`: integer  
  The unique identifier of the roommate to whom the chore will be assigned.

**Request Body:**

- `chore_id`: integer  
  The unique identifier of the chore to be assigned to the roommate.

  **Note:** The API will verify that the chore ID is valid and not already assigned to another roommate. If the chore is invalid or already assigned, an error will be returned.

**Response:**

- `message`: string  
  A confirmation message indicating the result of the assignment.
- `assigned_chore_id`: integer  
  The unique identifier of the assigned chore.

---

### 9. Get All Roommates

**Endpoint:** `GET /roommates`

**Request Query Parameters:**

- `first_name`: string (optional)  
  The first name of the roommate to filter results. If not provided, all roommates will be returned.
  
- `last_name`: string (optional)  
  The last name of the roommate to filter results. If not provided, all roommates will be returned.

**Response:**

- `roommates`: array of objects  
  A list of roommates matching the filter criteria, or all roommates if no filters are provided.

  - `id`: integer  
    The unique identifier of the roommate.
    
  - `first_name`: string  
    The first name of the roommate.
    
  - `last_name`: string  
    The last name of the roommate.
    
  - `chores`: array of objects  
    A list of chore objects assigned to the roommate.

    - `id`: integer  
      The unique identifier of the chore.
      
    - `name`: string  
      The name or description of the chore.
      
    - `due_date`: string (YYYY-MM-DD) 
      The due date of the chore.

---

### 10. Get Chores by Roommate

**Endpoint:** `GET /roommates/{id}/chores`

**Request Path Parameters:**

- `id`: integer (required)  
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

### 11. Create a Bill

**Endpoint:** `POST /bills`

**Request Body:**

- `total_amount`: float (required)  
  The total amount of the bill.

- `roommate_ids`: array of integers (required)  
  A list of unique identifiers of the roommates responsible for paying the bill.

- `due_date`: string (YYYY-MM-DD) (required)  
  The date by which the bill must be paid.

**Response:**

- `bill_id`: integer  
  The unique identifier of the created bill.

- `message`: string  
  A confirmation message indicating the successful creation of the bill.

---

### 12. Get a Bill 

**Endpoint:** GET /bills

**Request Body:**

- `status`: string (optional)
  Filter bills by their status. Possible values are "paid" or "unpaid".

**Response:**

- `bill_id`: integer
  The unique identifier of the bill
  
- `description`: string
  A brief description of the bill (e.g., "Electricity bill").

- `total_amount`: float
  The total amount of the bill.

- `due_date`: string (YYYY-MM-DD)
  The due date for the bill payment.

- `status`: string
  The current payment status of the bill (e.g., "paid" or "unpaid").

- `roommates`: array of objects
  A list of roommates and their respective payment statuses.
    - `roommate_id `: integer
      The unique identifier of the roommate.
    - `amount_due`: float
      The amount the roommate is responsible for.
    - `status`: string
      The unique identifier of the roommate.
    - `roommate_id `: integer
      The payment status for the roommate (e.g., "paid", "unpaid").
---
  
### 13. Update a Bill 

**Endpoint:** PATCH /bills/{bill_id}

**Request Body:**

- `due_date`: string (YYYY-MM-DD)(optional)
  The new due date for the bill
  
- `description`: string (optional)
  An updated description of the bill.

**Response:**

- `message`: string
  A confirmation message indicating the successful update of the bill
