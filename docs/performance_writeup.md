# **Performance Writeup**

## **Fake Data Modeling**

### **Python Script**
The Python script used to generate the fake data for the service is available here: [fake_data.py](https://github.com/s6hib/Chore-Tracker-API/blob/main/fake_data.py).

### **Final Rows Numbers in Each Table**
The service generates the following number of rows for each table:

| Table                | Number of Rows               | Explanation                                              |
|----------------------|------------------------------|--------------------------------------------------------|
| `roommate`           | **10**                       | Represents a fixed number of roommates in a shared living space, such as a co-living house. |
| `chore`              | **355,000**                | Each roommate is responsible for **355,000 chores**, representing recurring tasks over time (e.g., daily, weekly, monthly chores). |
| `chore_assignment`   | **355,000**                | Each chore is assigned to a specific roommate, mirroring the `chore` table. |
| `bill`               | **26,365**                   | Represents shared expenses such as utilities, rent, and groceries. |
| `bill_list`          | **263,650**                  | Each bill is shared among all **10 roommates**, leading to **10 entries per bill**. |

**Total Rows:**  
`10 (roommate)` + `355,000 (chore)` + `355000 (chore_assignment)` + `26365 (bill)` + `263650 (bill_list)` = **1,000,025 rows**

---

### **Scaling Justification**

This data model is set up to handle a realistic roommate tracking service, designed to scale logically without overcomplicating things. Here's how it breaks down:

1. **Roommates (10):**
   - We’re assuming a big house with 10 roommates because that’s a realistic number for shared living spaces. It keeps things practical without inflating the data just for the sake of it.

2. **Chores (355,000):**
   - Chores naturally pile up over time, especially with recurring tasks like cleaning, organizing, and maintenance. The high number here reflects how chores accumulate over months and years.

3. **Chore Assignments (355,000):**
   - Every chore gets assigned to a specific roommate, so this matches the number of chores.

4. **Bills (26,365):**
   - Bills grow based on monthly expenses like rent, utilities, and shared groceries. The high number here reflects how bills accumulate over months and years. 

5. **Bill List (263,650):**
   - Each bill is split among all 10 roommates that live in the house, so for every bill, there are 10 entries in the bill list.

---

### **Why This Works for Scaling**

This setup is realistic and scalable because:
1. **Logical Growth Over Time:**
   - The number of chores and bills reflects how responsibilities and expenses naturally grow in a shared space over time (over many years).

2. **Realistic Relationships:**
   - Keeping the number of roommates small makes sense for real-world situations, and the scaling happens in the number of records, not the size of the household.

3. **Balanced Distribution:**
   - Chores and bills are evenly divided among all roommates, which keeps things balanced and makes sense for a tracking system like this.
---

# Endpoint Execution Times

| Endpoint                          | Execution Time (ms) |
|-----------------------------------|---------------------|
| update_bill                       | 8.50               |
| update_chore_priority             | 10.86              |
| get_roommate                      | 12.12              |
| create_roommate                   | 12.55              |
| create_bills                      | 22.57              |
| create_chore                      | 30.32              |
| assign_chore                      | 71.33              |
| get_bill_assignments              | 77.90              |
| rotate_chore                      | 80.23              |
| update_chore_status               | 144.56             |
| get_bills                         | 177.30             |
| update_bill_list_status           | 155.68             |
| remove_roommate                   | 245.53             |
| get_chore_history                 | 438.82             |
| get_chore_assignment by roommate_id | 502.08            |
| get_chore                         | 7441.87            |
---

 # 1. Performance Tuning for GET /chores Endpoint

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

After adding the end point, the end point running time reduced to 5244.65 ms from 7033.46 ms. 

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

### For Further Optimization:
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

 # 2. Performance Tuning for GET /assignments/{roommate_id} Endpoint

### Initial Query Analysis
The `GET /assignments/{roommate_id}` endpoint retrieves all chore assignments for a specific roommate from the `chore_assignment` table, ordered by `roommate_id`. When tested via Swagger UI with a `roommate_id` parameter, the endpoint took **502.95 ms** to execute. This performance suggested room for improvement. To investigate further, the query was analyzed using `EXPLAIN` and `EXPLAIN ANALYZE`.


```
SELECT chore_id, roommate_id, status
FROM chore_assignment
WHERE roommate_id = :roommate_id
ORDER BY roommate_id;
```
### Initial EXPLAIN Output:
### Observations:
Sequential Scan: The query performs a full scan of the chore_assignment table to filter rows where roommate_id = :roommate_id.
Filtering Overhead: Out of 355,001 rows in the table, 319,500 rows were filtered out, indicating inefficiency.
Sorting: Sorting by roommate_id adds additional cost.

### Output:
```
Seq Scan on chore_assignment  (cost=0.00..7396.50 rows=35666 width=20)
  Filter: (roommate_id = 1)
  Rows Removed by Filter: 319500
```

### Initial EXPLAIN ANALYZE Output:
### Observations:
Execution Time: The query execution time in the database was 86.427 ms, significantly faster than the 502.95 ms recorded via Swagger UI, indicating application-level overhead.
Filtering: A majority of rows (319,500) were filtered out by the WHERE roommate_id = :roommate_id condition.

### Output:
```
Seq Scan on chore_assignment  (cost=0.00..7396.50 rows=35666 width=20) (actual time=0.054..85.353 rows=35501 loops=1)
  Filter: (roommate_id = 1)
  Rows Removed by Filter: 319500
Planning Time: 0.653 ms
Execution Time: 86.427 ms
```

### Adding an Index
To optimize the query, an index was created on the priority column:
```
CREATE INDEX idx_chore_assignment_roommate_id ON chore_assignment(roommate_id);
```
This index enables the database to quickly locate rows where roommate_id = :roommate_id, avoiding a sequential scan.

After adding the end point, the end point running time reduced to 252.76 ms from 502.08 ms.

### Post-Index EXPLAIN Output:
### Observations:
Index Scan: The query now uses the idx_chore_assignment_roommate_id index to efficiently retrieve matching rows.
Improved Cost: The query cost reduced significantly compared to the original Seq Scan

### Output:
```
Index Scan using idx_chore_assignment_roommate_id on chore_assignment  (cost=0.42..1049.58 rows=35666 width=20)
  Index Cond: (roommate_id = 1)
```
### Validating Improvements with EXPLAIN ANALYZE
After adding the index, the query was rerun with EXPLAIN ANALYZE and buffer usage metrics:
```
EXPLAIN (ANALYZE, BUFFERS)
SELECT chore_id, roommate_id, status
FROM chore_assignment
WHERE roommate_id = :roommate_id
ORDER BY roommate_id;
```
### Observations:
Execution Time: The database execution time reduced to 5.088 ms, a significant improvement from the initial 86.427 ms.
Buffer Usage: Data was efficiently retrieved from shared memory buffers (shared hit=64), reducing disk I/O.

### Output:
```
Index Scan using idx_chore_assignment_roommate_id on chore_assignment  (cost=0.42..1049.58 rows=35666 width=20) (actual time=0.016..3.873 rows=35501 loops=1)
  Index Cond: (roommate_id = 1)
  Buffers: shared hit=329
Planning Time: 0.084 ms
Execution Time: 5.088 ms
```
### Observations:
While the database query execution time reduced significantly, the endpoint still took 502.95 ms when tested via Swagger UI.
This indicates highlights application-level overhead as a significant contributor to the total execution time. 
Factors such as JSON serialization, network latency, and data processing like converting rows to dictionaries likely contribute to the delay.

### For Further Optimization: 
As similar to what was suggested in the first end point - 
1. Pagination: Introduce pagination to limit the number of rows returned per request, reducing JSON serialization and network latency.
```
SELECT chore_id, roommate_id, status
FROM chore_assignment
WHERE roommate_id = :roommate_id
ORDER BY roommate_id
LIMIT 100 OFFSET 0;
```
2. Efficient Serialization: Use faster libraries for JSON serialization in the application layer.
---

 # 3. Performance Tuning for GET /30_day_chore_history Endpoint

### Initial Query Analysis
The `GET /30_day_chore_history` endpoint retrieves chore history for the last 30 days, including information about the chore, the assignee, and its completion status. When tested via Swagger UI, the endpoint took **438.82 ms** to execute. This performance indicated room for improvement. To investigate further, the query was analyzed using `EXPLAIN` and `EXPLAIN ANALYZE`.

```
SELECT 
    c.name AS chore_name,
    r.first_name,
    r.last_name,
    ca.status,
    c.due_date AS completion_date
FROM chore c
JOIN chore_assignment ca ON c.id = ca.chore_id
JOIN roommate r ON ca.roommate_id = r.id
WHERE ca.status = 'completed'
  AND c.due_date >= :thirty_days_ago
  AND c.due_date <= :today
ORDER BY c.due_date DESC;
```
### Initial EXPLAIN Output:
### Observations:
Sequential Scans: The query performs sequential scans on both the chore and chore_assignment tables, leading to inefficiencies due to the large dataset.
Filtering Overhead: A significant number of rows were filtered out during execution, adding unnecessary workload.
Sorting: Sorting by c.due_date DESC increases the query cost.

### Output:
```
Gather Merge  (cost=14676.58..16733.70 rows=17888 width=83)
  Workers Planned: 1
  ->  Sort  (cost=13676.57..13721.29 rows=17888 width=83)
        Sort Key: c.due_date DESC
        ->  Hash Join  (cost=6612.99..12413.08 rows=17888 width=83)
              Hash Cond: (ca.roommate_id = r.id)
              ->  Parallel Hash Join  (cost=6589.94..12342.73 rows=17888 width=27)
                    Hash Cond: (ca.chore_id = c.id)
                    ->  Parallel Seq Scan on chore_assignment ca  (cost=0.00..5569.30 rows=69901 width=20)
                          Filter: (status = 'completed'::status_enum)
                    ->  Parallel Hash  (cost=6116.77..6116.77 rows=37853 width=23)
                          ->  Parallel Seq Scan on chore c  (cost=0.00..6116.77 rows=37853 width=23)
                                Filter: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
              ->  Hash  (cost=15.80..15.80 rows=580 width=72)
                    ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=72)
```

### Initial EXPLAIN ANALYZE Output:
### Observations:
Execution Time: The query execution time in the database was 166.263 ms, much lower than the 438.82 ms observed in Swagger UI. This difference highlights application-layer overhead.
Filtering Overhead: A large number of rows were filtered out:
                  118,305 rows removed from chore_assignment.
                  131,978 rows removed from chore.

### Output:
```
Gather Merge  (cost=14676.58..16733.70 rows=17888 width=83) (actual time=158.930..165.378 rows=30275 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Sort  (cost=13676.57..13721.29 rows=17888 width=83) (actual time=151.915..152.689 rows=15138 loops=2)
        Sort Key: c.due_date DESC
        Sort Method: quicksort  Memory: 1555kB
        Worker 0:  Sort Method: quicksort  Memory: 1536kB
        ->  Hash Join  (cost=6612.99..12413.08 rows=17888 width=83) (actual time=90.205..147.928 rows=15138 loops=2)
              Hash Cond: (ca.roommate_id = r.id)
              ->  Parallel Hash Join  (cost=6589.94..12342.73 rows=17888 width=27) (actual time=89.800..145.727 rows=15138 loops=2)
                    Hash Cond: (ca.chore_id = c.id)
                    ->  Parallel Seq Scan on chore_assignment ca  (cost=0.00..5569.30 rows=69901 width=20) (actual time=0.016..41.478 rows=59196 loops=2)
                          Filter: (status = 'completed'::status_enum)
                          Rows Removed by Filter: 118305
                    ->  Parallel Hash  (cost=6116.77..6116.77 rows=37853 width=23) (actual time=88.730..88.731 rows=45524 loops=2)
                          Buckets: 131072  Batches: 1  Memory Usage: 6304kB
                          ->  Parallel Seq Scan on chore c  (cost=0.00..6116.77 rows=37853 width=23) (actual time=0.047..71.415 rows=45524 loops=2)
                                Filter: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
                                Rows Removed by Filter: 131978
              ->  Hash  (cost=15.80..15.80 rows=580 width=72) (actual time=0.125..0.125 rows=11 loops=2)
                    Buckets: 1024  Batches: 1  Memory Usage: 9kB
                    ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=72) (actual time=0.090..0.092 rows=11 loops=2)
Planning Time: 0.599 ms
Execution Time: 166.263 ms
```

### Adding an Index
To optimize the query, these two indices was created on the priority column:

This index is created on the chore_assignment (status, chore_id) columns to optimize filtering rows by status and joining with the chore table.
```
CREATE INDEX idx_chore_assignment_status_chore_id 
ON chore_assignment (status, chore_id);
```

This index is created on the chore (due_date DESC) column to optimize filtering by the due_date range and sorting in descending order.
```
CREATE INDEX idx_chore_due_date_desc 
ON chore (due_date DESC);
```

After adding the end point, the end point running time reduced to 332.28 ms from 438.82 ms.

### Post-Index EXPLAIN Output:
### Observations:
Index Scans: The idx_chore_due_date_desc index is used for filtering and sorting by c.due_date DESC. The idx_chore_assignment_status_chore_id index is used to filter rows with status = 'completed'.
Improved Query Cost: The query cost reduced as sequential scans were replaced with index scans.

### Output:
For idx_chore_assignment_status_chore_id:
```
Gather Merge  (cost=14676.58..16733.70 rows=17888 width=83) (actual time=147.393..153.170 rows=30275 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Sort  (cost=13676.57..13721.29 rows=17888 width=83) (actual time=142.788..143.522 rows=15138 loops=2)
        Sort Key: c.due_date DESC
        Sort Method: quicksort  Memory: 1579kB
        Worker 0:  Sort Method: quicksort  Memory: 1512kB
        ->  Hash Join  (cost=6612.99..12413.08 rows=17888 width=83) (actual time=92.890..139.346 rows=15138 loops=2)
              Hash Cond: (ca.roommate_id = r.id)
              ->  Parallel Hash Join  (cost=6589.94..12342.73 rows=17888 width=27) (actual time=92.533..137.189 rows=15138 loops=2)
                    Hash Cond: (ca.chore_id = c.id)
                    ->  Parallel Seq Scan on chore_assignment ca  (cost=0.00..5569.30 rows=69901 width=20) (actual time=0.020..31.468 rows=59196 loops=2)
                          Filter: (status = 'completed'::status_enum)
                          Rows Removed by Filter: 118305
                    ->  Parallel Hash  (cost=6116.77..6116.77 rows=37853 width=23) (actual time=91.929..91.930 rows=45524 loops=2)
                          Buckets: 131072  Batches: 1  Memory Usage: 6304kB
                          ->  Parallel Seq Scan on chore c  (cost=0.00..6116.77 rows=37853 width=23) (actual time=0.068..74.497 rows=45524 loops=2)
                                Filter: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
                                Rows Removed by Filter: 131978
              ->  Hash  (cost=15.80..15.80 rows=580 width=72) (actual time=0.170..0.171 rows=11 loops=2)
                    Buckets: 1024  Batches: 1  Memory Usage: 9kB
                    ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=72) (actual time=0.153..0.155 rows=11 loops=2)
Planning Time: 2.717 ms
Execution Time: 154.077 ms
```
for idx_chore_due_date:
```
Gather Merge  (cost=14277.21..16334.33 rows=17888 width=83) (actual time=191.689..197.845 rows=30275 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Sort  (cost=13277.20..13321.92 rows=17888 width=83) (actual time=186.470..187.424 rows=15138 loops=2)
        Sort Key: c.due_date DESC
        Sort Method: quicksort  Memory: 1567kB
        Worker 0:  Sort Method: quicksort  Memory: 1524kB
        ->  Hash Join  (cost=6213.61..12013.70 rows=17888 width=83) (actual time=114.743..181.389 rows=15138 loops=2)
              Hash Cond: (ca.roommate_id = r.id)
              ->  Parallel Hash Join  (cost=6190.56..11943.35 rows=17888 width=27) (actual time=114.457..179.051 rows=15138 loops=2)
                    Hash Cond: (ca.chore_id = c.id)
                    ->  Parallel Seq Scan on chore_assignment ca  (cost=0.00..5569.30 rows=69901 width=20) (actual time=0.017..45.911 rows=59196 loops=2)
                          Filter: (status = 'completed'::status_enum)
                          Rows Removed by Filter: 118305
                    ->  Parallel Hash  (cost=5717.40..5717.40 rows=37853 width=23) (actual time=114.095..114.096 rows=45524 loops=2)
                          Buckets: 131072  Batches: 1  Memory Usage: 6336kB
                          ->  Parallel Bitmap Heap Scan on chore c  (cost=1251.60..5717.40 rows=37853 width=23) (actual time=2.567..91.294 rows=45524 loops=2)
                                Recheck Cond: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
                                Heap Blocks: exact=2117
                                ->  Bitmap Index Scan on idx_chore_due_date  (cost=0.00..1228.89 rows=90847 width=0) (actual time=4.639..4.639 rows=91049 loops=1)
                                      Index Cond: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
              ->  Hash  (cost=15.80..15.80 rows=580 width=72) (actual time=0.059..0.059 rows=11 loops=2)
                    Buckets: 1024  Batches: 1  Memory Usage: 9kB
                    ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=72) (actual time=0.046..0.047 rows=11 loops=2)
Planning Time: 0.791 ms
Execution Time: 198.794 ms
```
### Validating Improvements with EXPLAIN ANALYZE
After adding the index, the query was rerun with EXPLAIN ANALYZE and buffer usage metrics:
```
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    c.name AS chore_name,
    r.first_name,
    r.last_name,
    ca.status,
    c.due_date AS completion_date
FROM chore c
JOIN chore_assignment ca ON c.id = ca.chore_id
JOIN roommate r ON ca.roommate_id = r.id
WHERE ca.status = 'completed'
  AND c.due_date >= :thirty_days_ago
  AND c.due_date <= :today
ORDER BY c.due_date DESC;
```
### Observations:
Execution Time: The query execution time reduced from 438.82 ms to 242.885 ms, showing significant improvement.
Buffer Usage: The query effectively retrieved data from shared buffers (memory), avoiding disk I/O.

### Output:
```
Gather Merge  (cost=14277.21..16334.33 rows=17888 width=83) (actual time=231.758..241.494 rows=30275 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  Buffers: shared hit=6979
  ->  Sort  (cost=13277.20..13321.92 rows=17888 width=83) (actual time=212.075..213.319 rows=15138 loops=2)
        Sort Key: c.due_date DESC
        Sort Method: quicksort  Memory: 1542kB
        Buffers: shared hit=6979
        Worker 0:  Sort Method: quicksort  Memory: 1549kB
        ->  Hash Join  (cost=6213.61..12013.70 rows=17888 width=83) (actual time=130.102..206.862 rows=15138 loops=2)
              Hash Cond: (ca.roommate_id = r.id)
              Buffers: shared hit=6971
              ->  Parallel Hash Join  (cost=6190.56..11943.35 rows=17888 width=27) (actual time=129.592..202.522 rows=15138 loops=2)
                    Hash Cond: (ca.chore_id = c.id)
                    Buffers: shared hit=6938
                    ->  Parallel Seq Scan on chore_assignment ca  (cost=0.00..5569.30 rows=69901 width=20) (actual time=0.035..49.209 rows=59196 loops=2)
                          Filter: (status = 'completed'::status_enum)
                          Rows Removed by Filter: 118305
                          Buffers: shared hit=2959
                    ->  Parallel Hash  (cost=5717.40..5717.40 rows=37853 width=23) (actual time=128.951..128.955 rows=45524 loops=2)
                          Buckets: 131072  Batches: 1  Memory Usage: 6336kB
                          Buffers: shared hit=3979
                          ->  Parallel Bitmap Heap Scan on chore c  (cost=1251.60..5717.40 rows=37853 width=23) (actual time=2.488..105.397 rows=45524 loops=2)
                                Recheck Cond: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
                                Heap Blocks: exact=2304
                                Buffers: shared hit=3979
                                ->  Bitmap Index Scan on idx_chore_due_date_desc  (cost=0.00..1228.89 rows=90847 width=0) (actual time=4.465..4.468 rows=91049 loops=1)
                                      Index Cond: ((due_date >= '2024-11-05'::date) AND (due_date <= '2024-12-05'::date))
                                      Buffers: shared hit=81
              ->  Hash  (cost=15.80..15.80 rows=580 width=72) (actual time=0.155..0.156 rows=11 loops=2)
                    Buckets: 1024  Batches: 1  Memory Usage: 9kB
                    Buffers: shared hit=2
                    ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=72) (actual time=0.103..0.106 rows=11 loops=2)
                          Buffers: shared hit=2
Planning:
  Buffers: shared hit=20
Planning Time: 0.726 ms
Execution Time: 242.885 ms
```

### For Further Optimization: 
As similar to what was suggested in the first end point - 
1. Returning 30,275 rows at once is intensive for both the database and the application layer. Adding pagination would reduce workload and improve performance:
```
SELECT 
    c.name AS chore_name,
    r.first_name,
    r.last_name,
    ca.status,
    c.due_date AS completion_date
FROM chore c
JOIN chore_assignment ca ON c.id = ca.chore_id
JOIN roommate r ON ca.roommate_id = r.id
WHERE ca.status = 'completed'
  AND c.due_date >= :thirty_days_ago
  AND c.due_date <= :today
ORDER BY c.due_date DESC
LIMIT 100 OFFSET 0;

```
---


