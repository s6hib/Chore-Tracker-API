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

- `status`: string
- `assignee`: string or integer
- `priority`: integer

**Response:**

- `chores`: array of objects
  - `id`: integer
  - `title`: string
  - `description`: string
  - `priority`: integer
  - `duration`: integer
  - `due_date`: string
  - `status`: string
  - `assignee_id`: integer

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
