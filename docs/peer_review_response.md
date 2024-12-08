# Comments for Jose Espinoza's Review

## Schema/API design
1. Added description of enum values to schema.sql file. 'daily' is already set as the default frequency.
2. Not able to simplify any of the constraints any further because they are only primary key and foreign key relations. Changed status constraint to be an enum data type rather than a constraint check.
3. Foreign key relations between roommates and bills or chores is unecessary because we implemented chore_assignment and bill_list tables that have the foreign key relations.
4. Default time duration is already set to 0.
5. No sure what is mean by "describe error scenarios like 400 for bad request". Our 400 errors have descriptions to explain the cause of the error to the user when they happen.
6. Added try except to catch errors for frequency not matching one of the enum values. Already created FrequencyEnum to restrict values.
7. Updated error messages to throw proper error codes.
8. Vague comment on ensuring correct json response fields.
9. Already implemented RESTful naming convention.
10. Already have appropriate uniqueness constraints on all tables.
11. Added timestamptz column to all tables. We could include the timestamp of deletions such as a roommate or chore but then we would be storing data that never gets used by our program and is unecessary with the current development of the chore/bill tracker.
12. No composite keys necessary.
13. Table names are normalized using snake caseing.

## Code review comments
1. Added try/except clauses to all endpoints with error descriptions.
2. Added comments to more of the endpoints explaining them.
3. Vague reference to edgecases. Tested edges we could think of to find inconsistencies.
4. Not able to import the enums from the .sql file to our .py files
5. Removed unused imports.
6. Changed update_chore_status to update_chore_priority to better describe what the function is doing.
7. Added more error statements with proper error codes and descriptions to inform user the cause of the error.
8. Refactored repetitive code where applicable.
9. Dictionaries not necessary to replace if else statements
10. Functions are broken down to as simple as possible as most just perform a SQL query and can't be in different functions.
11. Tables can't be joined in existing queries given the relation of the query to the information wanted.
12. Added comments to db operations for clarity.
13. Variables have descriptive names already.
14. Could add constants for the default values but they are each only used once so it is unnecessary at the moment.

------

# Comments for Hunter Lathery's Review

## Schema/API design
1) The current schema supports a roommate having multiple chore assignments.
2) A roommate can be associated with zero, one, or many bills through the bill_list table.
3) Changed API Spec to remove the part that it assigns to a roomate.
4) Modified the frequency_enum definition to include 'no-repeat'
5) The existing `GET /chores` endpoint already provides all chore information.
6) Changed instances of biginit to int.
7) Implemented an endpoint to remove roomates.
8) You can see the status when you assign a chore, update it, and like Hunter said you can view all completed chores already.
9) Separate tables for chores and bills (chore_assignments and bill_list) are better than a unified table as they preserve clear domain separation for their distinct attributes and statuses.
10) We added a drop down where those are your only options.
11) Now specified certain columns where they can not be nullable.
12) Great suggestion that we can implement in the future. As of right now, we cover almost all extremely common bills that almost everyone has with the drop down option, so we won't be missing out on much.

## Code review comments
1) Looks like someone already addressed this. The part Hunter refers to is commented out and chore status is handled as a simple string with direct validation in the update_chore_status endpoint.
2) In `chore_assignment.py` it looks like we don't use `from src.api.roommate import Roommate` and `from src.api.chore import Chore` and in `bill.py` it looks like we don't use `from src.api.roommate import Roommate` so I removed them.
3) Addressed this to handle instances with priority numbers not 1-5.
4) Did this to do the following:
    Resets all chores to initial state:
    1. Deletes all chore assignments
    2. Deletes all chores
    3. Re-inserts default chores
5) Currently allows for people with the same email. Implemented change so that if you try to create a roommate with an email that already exists, you get an error.
6) Added doc strings to some endpoints where further clarification is needed. But like Hunter said, most are self explanatory.
7) Decided not to do this because:
- It provides better error messages (can tell exactly if chore not found vs roommate not found)
- More readable and maintainable code
- The performance difference would be negligible for this use case
- Current implementation follows separation of concerns
8) Implemented
9) Implemented. If one of the values is wrong it will tell you that one specifically is wrong and if both are wrong it'll tell you both of them are wrong. If both are right then it will work as intended.
10) Implemented
11) Done
12) Done

---

### # Comments for Salif's Review

## Schema/API design
1. Changed the name fields in roommate table to not allow them to be NULL
2. Emails are allowed to be the same as name is the more important identifier
3. Added constraints for enum fields
4. Changed ON DELETE CASCADE to ON DELETE SET NULL in order to avoid orphaned data
5. added more descriptive column names
6. Added indexes after testing runtime
7. Made the primary key consistent amongst all tables
8. Implemented RESTful naming conventions previously
9. In some fields having the default value as NULL is fine when they are unique for every person
10. Implemented error handling and better responses
11. This would be a useful feature to add in the future, but not need as of right now
12. Our timestamps are set to UTC time so that there is standardization across the board. This could be addressed at a later date
13. This is a great suggesstion if we ever want this project to go live, or once we have large amounts of data
14. This is a good comment and could be useful esspecially when working in groups
15. Improved query effeciency

## Code Review comments
1. This is a good comment to consider, but not relevent as of now as our service is not live
2. This is also good to consider, but once again not yet relevent as our service is not public
3. This is a great way to add security if our service becomes publicly available
4. Changed the error message to be more friendly
5. Updated queries to be more efficient
6. Updated the casing style in code
7. Added detailed docstrings to code
8. Added logging to make sure clients are adding valid data. More logging can be added in the future
9. Another great way of adding security which is not relevent now
10. This is a good comment to be considered in the future
11. This will remain this way for testing purposes
12. Not applicable, API key authentication is good enough for right now
13. This can be done when our project is scaled to a much larger size
14. Added more error handling
15. This is a good comment to consider for the future