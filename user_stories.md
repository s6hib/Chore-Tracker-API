# User Stories


- As a roommate who likes staying organized, I want to be able to add chores to the chore list so that I can keep track of what needs to be done around the house/apartment.
- As a roommate who wants to avoid clutter, I want to be able to remove chores from the chore list to update the chore list when chores have been completed.
- As a roommate who values fairness in the house, I want to be able to assign specific chores to each roommate to make sure everyone contributes and the workload is evenly distributed.
- As a roommate with a busy schedule, I want to be able to find out how much time each chore takes to complete in order to know how to evenly distribute the workload of the chores that need to be done for my time management.
- As a roommate who prefers structure, I want to identify which chores have the highest priority so we know which ones to tackle first, avoiding procrastination on urgent tasks.
- As a roommate who manages deadlines effectively, I want to set due dates for chores so that I can prioritize and complete tasks that are approaching their deadlines.
- As a roommate who wants to ensure tasks are done correctly, I want to add comments or notes to a chore so I can provide additional instructions or context.
- As a roommate who needs a clear overview, I want to view the entire chore list so that I can see all pending tasks and plan my day accordingly.
- As a roommate who tracks shared expenses, I want to be able to create a bill to evenly distribute the costs among us, ensuring fairness in our financial contributions.
- As a roommate who likes visual feedback, I want to mark chores as completed so that everyone knows which tasks have already been done, keeping things transparent.
- As a roommate who sometimes forgets tasks, I want to receive reminders for upcoming or overdue chores so I don’t miss out on completing important tasks.
- As a roommate who wants to stay on top of my responsibilities, I want to search for chores that are assigned to me so that I can quickly find and focus on my responsibilities.

# User Exceptions

- **Add a chore to the list that already exists** – If a roommate tries to add a chore that already exists, return an error to the user that the chore already exists and reprompt them to enter a different chore.
- **Mark a chore as complete that doesn’t exist** – If a roommate tries to mark a chore that doesn’t exist, return an error to the user that the chore doesn’t exist and reprompt them to enter a different chore to mark as completed.
- **Assign a chore to a roommate that does not exist** – If a roommate tries to assign a chore to a roommate that doesn’t exist, return an error to the user that the roommate doesn’t exist and reprompt them to enter a different roommate to assign the chore to.
- **Assign too many chores to one roommate and not enough to the others** – If a roommate tries to assign too many chores to the same person and the difference in the amount of time for those chores to be completed and every other roommate is over the allotted limit, then return an error and reprompt the user to assign the chore to a different roommate that doesn’t have as heavy of a chore load.
- **Set a due date in the past** – If a roommate tries to set a due date for a chore that has already passed, return an error and ask them to select a valid future date.
- **View a chore list when there are no chores added** – If a roommate tries to view the chore list when there are no chores, return a message stating that the chore list is empty and prompt them to add chores.
- **Exceed maximum character limit for chore descriptions or comments** – If a roommate tries to add a description or comment that exceeds the character limit, return an error and ask them to shorten the input.
- **Invalid Filter Value** – If a roommate tries to filter the chore list using a value that doesn’t exist (e.g., filtering by a non-existent category or roommate), return an error message and show no results.
- **Invalid Search Query** – If a roommate enters an invalid search query (e.g., invalid characters), return an error message and prompt them to enter a valid query.
- **Overpayment of Bill** – If a roommate tries to pay more money than what is assigned in the bill or exceeds the total bill amount, return an error message and prompt them to pay the correct amount.
- **Incomplete Chore Details** – If a roommate tries to add a chore without providing all the required details (e.g., missing title, due date, or assignee), return an error message prompting them to complete all necessary fields.
- **Duplicate Bill Creation** – If a roommate tries to create a bill that already exists, return an error and prompt them to modify the existing bill or create a new one for a different period.
