Comments for Jose Espinoza's Review
Schema/API design
1. Added description of enum values to schema.sql file. 'daily' is already set as the default frequency.
2. Not able to simplify any of the constraints any further because they are only primary key and foreign key relations. Changed status constraint to be an enum data type rather than a constraint check.
3. Foreign key relations between roommates and bills or chores is unecessary because we implemented chore_assignment and bill_list tables that have the foreign key relations.
4. Default time duration is already set to 0.
5. No sure what is mean by "describe error scenarios like 400 for bad request". No 400 errors occured in our testing or testing done by the peer reviewing.
6. Added try except to catch errors for frequency not matching one of the enum values. Already created FrequencyEnum to restrict values.
7. Updated error messages to throw proper error codes.
8. Vague comment on ensuring correct json response fields.
9. Already implemented RESTful naming convention.
10. Already have appropriate uniqueness constraints on all tables.
11. Added timestamptz column to all tables. We could include the timestamp of deletions such as a roommate or chore but then we would be storing data that never gets used by our program and is unecessary with the current development of the chore/bill tracker.
12. No composite keys necessary.
13. Table names are normalized using snake caseing.
