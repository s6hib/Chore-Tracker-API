# Roommate Deletion During Bill Creation

**Scenario**: Person A creates a new bill while Person B removes a roommate from the system.

**Sequence of Events**:
1. Person A calls `POST /bills/create_bill` with a $400 electricity bill
2. System inserts new bill into `bill` table with ID #14
3. System queries roommate count (finds 4 roommates: Sahib, Carson, Antony, Sue)
4. System calculates per-person cost ($400 / 4 = $100 each)
5. Meanwhile, Person B removes roommate Sahib from the system
6. System attempts to create bill_list entries, assigning $100 to each roommate
7. Operation fails when trying to create bill_list entry for Sahib (who no longer exists)

**Problem**: Without proper concurrency control:
- The bill gets created but bill assignments fail
- System has inconsistent state: bill exists but no assignments
- Total amount assigned doesn't match original bill amount

This is a good example of a race condition where the system assumes the number of roommates stays the same, but that changes because of other actions happening at the same time.