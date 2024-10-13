# API Specification

---

### Create a Chore

**Endpoint:** `POST /chores`  
**Request Body:**

- `title`: string
- `description`: string
- `priority`: integer
- `duration`: integer
- `due_date`: string
- `assignee_id`: integer

**Response:**  
Creates a new chore in the database.

---

### Get All Chores

**Endpoint:** `GET /chores`  
**Request Query Parameters:**

- `status`: string
- `assignee`: string or integer
- `priority`: integer

**Response:**  
Returns a list of chores with the specified filters.

---

### Get Specific Chore

**Endpoint:** `GET /chores/{id}`  
**Request Parameters:**

- `id`: integer

**Response:**  
Returns the details of a specific chore, including associated comments.

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
Updates the specified chore in the database.

---

### Delete a Chore

**Endpoint:** `DELETE /chores/{id}`  
**Request Parameters:**

- `id`: integer

**Response:**  
Confirms the deletion of the specified chore.

---

### Add Comment to Chore

**Endpoint:** `POST /chores/{id}/comments`  
**Request Parameters:**

- `id`: integer

**Request Body:**

- `comment_text`: string
- `commenter_id`: integer

**Response:**  
Adds a comment to the specific chore.

---

### Create a Roommate

**Endpoint:** `POST /roommates`  
**Request Body:**

- `first_name`: string
- `last_name`: string
- `chores`: array of integers

**Response:**  
Creates a new roommate in the database with a unique ID.

---

### Assign Chore to Roommate

**Endpoint:** `POST /roommates/{id}/chores`  
**Request Parameters:**

- `id`: integer

**Request Body:**

- `chore_id`: integer

**Response:**  
Adds the chore(s) from the chore list to a specific roommate's list of chores they are responsible for completing.

---

### Get All Roommates

**Endpoint:** `GET /roommates`  
**Request Query Parameters:**

- `first_name`: string
- `last_name`: string

**Response:**  
Returns a list of all roommates with the specified filters.

---

### Get Chores by Roommate

**Endpoint:** `GET /roommates/{id}/chores`  
**Request Parameters:**

- `id`: integer

**Response:**  
Returns the list of chores assigned to the specific roommate.

---

### Create a Bill

**Endpoint:** `POST /bills`  
**Request Body:**

- `total_amount`: float
- `roommate_ids`: array of integers
- `due_date`: string

**Response:**  
Creates a bill for the specified roommates and stores it in the database.
