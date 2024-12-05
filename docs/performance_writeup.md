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

# Performance Tuning for GET /chores Endpoint

### Initial Query Analysis
The GET /chores endpoint retrieves all rows from the chore table, sorted by priority.
When tested via Swagger UI with no priority filter applied, the endpoint took 7033.46 ms to execute.
This slow performance indicated the need for optimization. To test further, the query was analyzed using EXPLAIN and EXPLAIN ANALYZE.

```
SELECT id, name, location_in_house, frequency, duration_mins, priority, due_date
FROM chore
ORDER BY priority;
```
### Initial EXPLAIN Output:
### Observations:
1. Sequential Scan: The query performs a full scan of all 355,000 rows in the chore table, as there was no index on the priority column.
2. Sorting: The entire result set is sorted in-memory, further increasing the query cost.

### Output:
```
 Sort  (cost=52308.99..53196.49 rows=355000 width=49)
   Sort Key: priority
   ->  Seq Scan on chore  (cost=0.00..7448.00 rows=355000 width=49)
```

### Initial EXPLAIN ANALYZE Output:
### Observations:
Execution Time: The query took 249.034 ms in the database, significantly lower than the time measured via Swagger UI. 
The difference is likely due to application-level overhead, including network latency and JSON serialization.
Sorting Method: Sorting required 22 MB of disk space, adding to the query's cost.

### Output:
```
 Sort  (cost=52308.99..53196.49 rows=355000 width=49) (actual time=204.425..238.510 rows=355004 loops=1)
   Sort Key: priority
   Sort Method: external merge  Disk: 22000kB
   ->  Seq Scan on chore  (cost=0.00..7448.00 rows=355000 width=49) (actual time=0.197..106.692 rows=355004 loops=1)
 Planning Time: 0.320 ms
 Execution Time: 249.034 ms
```

### Adding an Index
To optimize the query, an index was created on the priority column:
```
CREATE INDEX idx_chore_priority ON chore(priority);
```
This index enables the database to retrieve rows in the order of priority without requiring a full table scan or external sorting.

### Post-Index EXPLAIN Output:
### Observations:
Index Scan: The query now uses the idx_chore_priority index to retrieve rows efficiently, avoiding the need for a sequential scan or additional sorting.

### Output:
```
Index Scan using idx_chore_priority on chore  (cost=0.42..21624.55 rows=355004 width=49)
```
### Validating Improvements with EXPLAIN ANALYZE
After adding the index, the query was rerun with EXPLAIN ANALYZE and buffer usage metrics:
```
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, name, location_in_house, frequency, duration_mins, priority, due_date
FROM chore
ORDER BY priority;
```
### Output:
### Observations:
Execution Time: The query execution time in the database reduced to 171.010 ms, an improvement from the initial 249.034 ms.
Buffer Usage: Data was retrieved efficiently from shared memory buffers (shared hit=19791), minimizing disk I/O.

### Output:
```
Index Scan using idx_chore_priority on chore  (cost=0.42..21624.55 rows=355004 width=49) (actual time=0.235..158.117 rows=355004 loops=1)
   Buffers: shared hit=19791
 Planning Time: 0.649 ms
 Execution Time: 171.010 ms
```
### Observations:
While the database query execution time reduced significantly, the endpoint still took 7033.46 ms when tested via Swagger UI.
This discrepancy highlights application-level overhead as a significant contributor to the total execution time. 
Factors such as JSON serialization, network latency, and processing large result sets likely contribute to the delay.

### Recommendations for Further Optimization:
1. Pagination: Introduce pagination to limit the number of rows returned per request, reducing JSON serialization and network latency.
```
SELECT id, name, location_in_house, frequency, duration_mins, priority, due_date
FROM chore
ORDER BY priority
LIMIT 100 OFFSET 0;
```
2. Efficient Serialization: Use faster libraries for JSON serialization in the application layer.
3. Asynchronous Processing: Optimize endpoint performance by using asynchronous processing if supported by the framework.
---

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


 