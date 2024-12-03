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

1. get_chores 8367.33 ms (without priorty)
get_chores = 1791.10 ms
Seq Scan on chore  (cost=0.00..10490.00 rows=500000 width=57)
Index Scan using chore_pkey on chore  (cost=0.42..8.44 rows=1 width=57)
Index Scan using idx_chore_id on chore  (cost=0.42..8.44 rows=1 width=57)

Seq Scan on chore  (cost=0.00..11740.00 rows=100617 width=41)
  ->  Bitmap Index Scan on idx_priority  (cost=0.00..1099.05 rows=100617 width=0)
  get chores 1725.57 ms
get chores = 7544.33 ms 

2. get_roommates = 764.80 ms 
  get_roommates 32.93 ms (order by last name)
Sort  (cost=42.42..43.87 rows=580 width=96)
  Sort Key: last_name
  ->  Seq Scan on roommate r  (cost=0.00..15.80 rows=580 width=96)




get 30 day chore history = 144.72 ms b/c chore due dates are set in the future


3. get bill =  334.77ms ms


get bill assignments = 89.35 ms

4. post rotate 