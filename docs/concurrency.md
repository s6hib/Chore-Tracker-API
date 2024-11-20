# 1. Roommate Deletion During Bill Creation

**Scenario**: Person A creates a new bill while Person B removes a roommate from the system.

**Sequence of Events**:
1. Person A calls `POST /bills/create_bill` with a $400 electricity bill
2. System inserts new bill into `bill` table with ID #14
3. System queries roommate count (finds 4 roommates: Sahib, Carson, Antony, Sue)
4. System calculates per-person cost ($400 / 4 = $100 each)
5. Meanwhile, Person B removes roommate Sahib from the system
6. System attempts to create bill_list entries, assigning $100 to each roommate
7. Operation fails when trying to create bill_list entry for Sahib (who no longer exists)

**Problem**: Without proper concurrency control the entire transaction fails, so inserting the bill gets rolled back.

This is a good example of a race condition where the system assumes the number of roommates stays the same, but that changes because of other actions happening at the same time.

# 2. Roommate Deletion During Chore Rotation

**Scenario**: Weekly chore rotation occurs while someone removes the next assigned roommate.

**Sequence of Events**:
1. System starts weekly chore rotation for "Clean the Kitchen"
2. Current assignment is to Sue 
3. System calculates next assignment should go to Carson 
4. Meanwhile, someone removes Carson from the system
5. System attempts to update chore_assignment with Carson's roommate_id
6. Operation fails due to Carson no longer existing

**Problem**: Without proper concurrency control this transaction fails, so now the rotation gets broken and we have an unassigned chore.

```mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2
    Note over T1, T2: Chore labeled Clean Kitchen is assigned to Roommate Sue (Sue roommate id 1, Carson roommate id 2, Clean Kitchen chore id 1) 
    T1->>Database: Rotate chore "Clean Kitchen" from Sue to next roommate
    T1->>Database: next_result = connection.execute(sqlalchemy.text("""
                SELECT id
                FROM roommate
                WHERE id > :roommate_id
                ORDER BY id ASC
                LIMIT 1
            """), {'roommate_id': roommate_id})
    T2->>Database: Remove Carson from the roommate table
    T2->>Database: DELETE
                FROM roommate
                WHERE id = :roommate_id
                RETURNING id, first_name, last_name, email
    Note over T1, T2: Carson with roommate id 2 no longer exist in the roommate table
    T1->>Database: Assign Clean Kitchen chore to next roommate id after Sue
    T1->>Database: connection.execute(sqlalchemy.text("""
                UPDATE chore_assignment
                SET roommate_id = :new_roommate_id
                WHERE chore_id = :chore_id
            """), {
                "chore_id": chore_id,
                "new_roommate_id": new_roommate_id
            })
    Note over T1, T2: Causes an error because T1 tries to assign a chore to a roommate that doesn't exist in the database anymore.
```
