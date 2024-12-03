Comments for Jose Espinoza's Review

Schema/API design
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

Code review comments
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


Comments for Salif's Review

Schema/API design
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

Code Review comments
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


