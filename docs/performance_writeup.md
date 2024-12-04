# **Performance Writeup**

## **Fake Data Modeling**

### **Python Script**
The Python script used to generate the fake data for the service is available here: [fake_data.py](https://github.com/s6hib/Chore-Tracker-API/blob/main/fake_data.py).

### **Final Rows Numbers in Each Table**
The service generates the following number of rows for each table:

| Table                | Number of Rows               | Explanation                                              |
|----------------------|------------------------------|--------------------------------------------------------|
| `roommate`           | **10**                       | Represents a fixed number of roommates in a shared living space, such as a co-living house. |
| `chore`              | **500,000**                | Each roommate is responsible for **500,000 chores**, representing recurring tasks over time (e.g., daily, weekly, monthly chores). |
| `chore_assignment`   | **500,000**                | Each chore is assigned to a specific roommate, mirroring the `chore` table. |
| `bill`               | **41,000**                   | Represents shared expenses such as utilities, rent, and groceries. |
| `bill_list`          | **410,000**                  | Each bill is shared among all **10 roommates**, leading to **10 entries per bill**. |

**Total Rows:**  
`10 (roommate)` + `500,000 (chore)` + `500,000 (chore_assignment)` + `41,000 (bill)` + `410,000 (bill_list)` = **1,451,010 rows**

---

### **Scaling Justification**

This data model reflects the realistic scaling of a roommate tracking service and is designed to accommodate a large dataset while staying logically consistent. These are the reasons why the structure is scalable.

1. **Roommates (10):**
   - A fixed number of roommates ensures that the model realistically represents a typical shared living space in a big house.
   - Keeping the number of roommates small avoids inflating the data artificially while allowing a focus on scaling the complexity of their interactions.

2. **Chores (500,000):**
   - Chores scale naturally with time.
   - This accounts for recurring tasks like cleaning, organizing, and other responsibilities.

3. **Chore Assignments (500,000):**
   - Each chore is assigned to a specific roommate, maintaining a one-to-one relationship with the `chore` table.

4. **Bills (41,000):**
   - Bills are generated monthly or for specific shared expenses (e.g., utilities, rent, groceries). 

   - This model also assumes additional itemized expenses, such as shared meals or one-time purchases, leading to the 50,000 total.

5. **Bill List (410,000):**
   - Each bill is shared among all 10 roommates, resulting in 10 entries per bill:

---

### **Service Scalability**

This service is designed to scale effectively because:
1. **Logical Growth Over Time:**
   - The high number of chores reflects the recurring nature of tasks in a shared space.
   - Bills and their breakdowns represent the complexity of shared financial responsibilities over time.

2. **Realistic Relationships:**
   - The number of roommates is small, which aligns with real-world scenarios.
   - Scaling occurs by increasing the number of records over time, rather than inflating the number of roommates.

3. **Balanced Distribution:**
   - Chores and bills are distributed across all roommates, ensuring a realistic workload and financial split.

---

1. get_chores end points give 8367.33 ms without any priority. 
get_chores gives 1791.10 ms with the priority chosen.
This is the scan before creating the index.  
Seq Scan on chore  (cost=0.00..10490.00 rows=500000 width=57)
Index Scan using chore_pkey on chore  (cost=0.42..8.44 rows=1 width=57)

This EXPLAIN means that the cost range of the query is 0.00 to 11740.00, which is rather expensive, and the number of rows that are returned is 50 thousand.

This is the scan after creating the index on the priority column.
Index Scan using idx_chore_id on chore  (cost=0.42..8.44 rows=1 width=57)
Seq Scan on chore  (cost=0.00..11740.00 rows=100617 width=41)
  ->  Bitmap Index Scan on idx_priority  (cost=0.00..1099.05 rows=100617 width=0)

This is get chores 1725.57 ms
get chores = 7544.33 ms 

The get_chores query was really slow at first because it scanned the whole table to get results. Adding an index on the priority column helped a lot by speeding things up with a better scan method. Then, adding a composite index on priority and due_date made it even faster by letting the database filter and sort much more efficiently. These changes cut the time from 8367.33 to 7544.33 ms for the query without any filters on the priority and from 1791.10 to 1725.57 ms for the query with the filter of priority 1.

2. get 30 day chore history = 144.72 ms b/c chore due dates are set in the future
Sort  (cost=0.01..0.02 rows=0 width=84)
  Sort Key: c.due_date DESC
    ->  Result  (cost=0.00..0.00 rows=0 width=84)
            One-Time Filter: false

This EXPLAIN means that the cost range of the query is 0.01 to 0.02, which is very inexpensive, and the number of rows that are returned is 0 because there aren't any chores that have been completed in the last 30 days because in our fake data we made all chores due in the future.

get 30 day chore history = 41.90 ms
Sort  (cost=0.01..0.02 rows=0 width=84)
  Sort Key: c.due_date DESC
  ->  Result  (cost=0.00..0.00 rows=0 width=84)
        One-Time Filter: false

The get_30_day_chore_history query was slow because it had to sort the table by due_date without any index, so it had to check every row. Adding an index on due_date fixed that by letting the database sort and filter directly, which brought the time down from 144.72 ms to 41.90 ms.

3. get bill =  334.77ms ms
Sort  (cost=3955.28..4057.78 rows=41000 width=39)
  Sort Key: due_date
    ->  Seq Scan on bill  (cost=0.00..814.00 rows=41000 width=39)

This EXPLAIN means that the cost range of the query is 3955.28 to 4057.78, which is moderately expensive, and the number of rows that are returned is 41000 which is the total number of fake bills created.

after adding index:
Index Scan using idx_duedate on bill  (cost=0.29..2383.03 rows=41000 width=39)
get_bill = 305.88 ms

The get_bill query also had issues because it was sorting by due_date without an index, which meant another full table scan. Adding an index on due_date made the query faster by letting the database skip the full scan, reducing the time from 334.77 ms to 305.88 ms. The improvement wasn’t huge, but it still helped make things run smoother.


 