# API Specification


### Create a Chore

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

### Get All Chores

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
      The due date of the chore (in ISO 8601 format, YYYY-MM-DD).
      
    - `status`: string  
      The current status of the chore. Predefined values: `pending`, `in_progress`, `completed`.
      
    - `assignee_id`: integer  
      The ID of the roommate assigned to the chore.


---

### Get Specific Chore

**Endpoint:** `GET /chores/{id}`  
**Request Parameters:**

- `id`: integer

**Response:**

- `id`: integer
- `title`: string
- `description`: string
- `priority`: integer
- `duration`: integer
- `due_date`: string
- `status`: string
- `assignee_id`: integer
- `comments`: array of objects
  - `comment_text`: string
  - `commenter_id`: integer

---

### Update a Chore

**Endpoint:** `PUT /chores/{id}`  
**Request Parameters:**

- `id`: integer

**Request Body:**

- `title`: string
- `priority`: integer
- `status`: string

**Response:**

- `message`: string
- `updated_fields`: array of strings

---

### Delete a Chore

**Endpoint:** `DELETE /chores/{id}`  
**Request Parameters:**

- `id`: integer

**Response:**

- `message`: string
- `deleted_chore_id`: integer

---

### Add Comment to Chore

**Endpoint:** `POST /chores/{id}/comments`  
**Request Parameters:**

- `id`: integer

**Request Body:**

- `comment_text`: string
- `commenter_id`: integer

**Response:**

- `comment_id`: integer
- `message`: string

---

### Create a Roommate

**Endpoint:** `POST /roommates`  
**Request Body:**

- `first_name`: string
- `last_name`: string
- `chores`: array of integers

**Response:**

- `roommate_id`: integer
- `message`: string

---

### Assign Chore to Roommate

**Endpoint:** `POST /roommates/{id}/chores`  
**Request Parameters:**

- `id`: integer

**Request Body:**

- `chore_id`: integer

**Response:**

- `message`: string
- `assigned_chore_id`: integer

---

### Get All Roommates

**Endpoint:** `GET /roommates`  
**Request Query Parameters:**

- `first_name`: string
- `last_name`: string

**Response:**

- `roommates`: array of objects
  - `id`: integer
  - `first_name`: string
  - `last_name`: string
  - `chores`: array of integers

---

### Get Chores by Roommate

**Endpoint:** `GET /roommates/{id}/chores`  
**Request Parameters:**

- `id`: integer

**Response:**

- `chores`: array of objects
  - `id`: integer
  - `title`: string
  - `description`: string
  - `priority`: integer
  - `duration`: integer
  - `due_date`: string
  - `status`: string

---

### Create a Bill

**Endpoint:** `POST /bills`  
**Request Body:**

- `total_amount`: float
- `roommate_ids`: array of integers
- `due_date`: string

**Response:**

- `bill_id`: integer
- `message`: string
