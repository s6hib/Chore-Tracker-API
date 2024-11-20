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

``` mermaid
sequenceDiagram
    participant PersonA
    participant Database
    participant PersonB

    Note over PersonA, PersonB: Scenario - Person A creates a new bill while Person B removes a roommate from the system
    PersonA->>Database: POST /bills/create_bill with $400 electricity bill
    Database->>PersonA: Inserts new bill into the bill table with ID #14
    PersonA->>Database: Query roommate counts by selecting all the roommate IDs (finds 4 roommates: Sahib, Carson, Antony, Sue)
    PersonA->>Database: Calculate per-person cost ($400/4 = $100 each)
    PersonB->>Database: Remove Sahib from the roommate table
    Database-->>PersonB: DELETE FROM roommate WHERE ID = :roommate_id RETURNING details
    Note over PersonA, PersonB: Sahib no longer exists in the roommate table
    PersonA->>Database: Attempt to insert bill_list entries, assigning $100 to each roommate
    Database-->>PersonA: Error occurs when trying to create bill_list entry for Sahib
    Note over PersonA, PersonB: Transaction fails and inserting the bill is rolled back
```

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

``` mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2

    Note over T1, T2: Chore "Clean Kitchen" is assigned to Sue (Sue: ID 1, Carson: ID 2, Chore: ID 1)
    T1->>Database: Rotate chore "Clean Kitchen" to next roommate
    T1->>Database: Query roommate with ID > :roommate_id (ORDER BY ID ASC LIMIT 1)
    T2->>Database: Remove Carson from the roommate table
    T2->>Database: DELETE FROM roommate WHERE ID = :roommate_id RETURNING details
    Note over T1, T2: Carson (ID 2) no longer exists in the roommate table
    T1->>Database: Assign "Clean Kitchen" chore to next roommate
    T1->>Database: UPDATE chore_assignment with new_roommate_id
    Note over T1, T2: Error occurs because the roommate no longer exists
```

# 3. Chore Assignment at the Same Time

**Scenario**: Two roommates simultaneously try to assign the same chore to different roommates.

**Sequence of Events**:
1. Roommate A checks if "Kitchen Cleaning" chore is assigned (result: unassigned)
2. Roommate B checks if "Kitchen Cleaning" chore is assigned (result: unassigned)
3. Roommate A assigns chore to Roommate Carson
4. Roommate B assigns chore to Roommate Antony

**Problem**: Without concurrency control:
- Same chore gets assigned to multiple people
- Duplicate chore assignments
- Confusion in who is doing what chore