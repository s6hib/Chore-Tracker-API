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

**Isolation Solution**: 
In this scenario, we can use a SERIALIZABLE isolation level because we're doing multiple reads and writes that depend on each other. Here's why:

1. We first read the roommate count to calculate costs
2. Then we write multiple bill_list entries based on that count
3. If someone deletes a roommate between these steps, we get an error

With SERIALIZABLE, the transaction would lock the roommate table during bill creation. This would prevent the deletion of a roommate from happening in the middle of the bill creation process. It's also worth noting that a SERIALIZABLE isolation level is not the best because it's sometimes not worth the performance hit, but in this case we can live with it.

``` mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2

    Note over T1, T2: Scenario - Person A creates a new bill while Person B removes a roommate from the system
    T1->>Database: POST /bills/create_bill with $400 electricity bill
    T1->>Database: Inserts new bill # 14 into the bill table
    Database->>Database: Query roommate counts by selecting all the roommate IDs (finds 4 roommates: Sahib, Carson, Antony, Sue)
    Database->>Database: Calculate per-person cost ($400/4 = $100 each)
    T2->>Database: Remove Sahib from the roommate table
    Database-->>T2: DELETE FROM roommate WHERE ID = :roommate_id RETURNING details
    Note over T1, T2: Sahib no longer exists in the roommate table
    T1->>Database: Attempt to insert bill_list entries, assigning $100 to each roommate
    Database-->>T1: Error occurs when trying to create bill_list entry for Sahib
    Note over T1, T2: Transaction fails and inserting the bill is rolled back
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

**Isolation Solution**:
For chore rotation, REPEATABLE READ is our best bet. Here's why:
1. We're doing a SELECT to find the next roommate, then an UPDATE to assign the chore
2. We need to make sure the roommate we selected still exists when we do the UPDATE
3. But we don't need to lock the whole roommate table like SERIALIZABLE would

REPEATABLE READ is perfect because it ensures that if we read a roommate's info, that info stays consistent throughout our transaction. If someone tries to delete Carson while we're rotating chores, either:
- Our transaction completes first and Carson gets the chore (then he can be deleted)
- The delete happens first and our rotation picks the next available roommate

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

**Isolation Solution**:
For this one, READ COMMITTED is actually enough, but we need to add a unique constraint:
1. We don't need super strict isolation because we're just doing one write
2. Instead, we could add a unique constraint on chore_id in the chore_assignment table
3. This way, if two people try to assign the same chore, the database will only let one succeed

This is a lot better than using SERIALIZABLE because:
- It's faster (no need to lock tables)
- It's simpler (let the database handle it with constraints)
- It still prevents the problem (can't have duplicate assignments)

Plus, if the second assignment fails, we can just show a message like "Sorry, someone already claimed that chore!" which is exactly what we want anyway.

``` mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2

    Note over T1, T2: Scenario - Two roommates simultaneously try to assign the same chore
    T1->>Database: Assign "Kitchen Cleaning" chore to Roommate Carson 
    T2->>Database: Assign "Kitchen Cleaning" chore Roommate Antony
    Database->>Database: Checks for chore assignment from T1 in chore (result: unassigned)
    Database->>Database: Checks for chore assignment from T2 in chore (result: unassigned)
    Database-->>T1: Return success message
    Database-->>T2: Return success message
    Note over T1, T2: Problem - Now same chore gets assigned to multiple people
    Note over T1, T2: Duplicate chore assignments cause confusion
```