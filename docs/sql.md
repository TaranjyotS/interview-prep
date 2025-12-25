# SQL

# SQL

### 1. **What is SQL?**

**Answer:**  
SQL (Structured Query Language) is a standardized programming language used for managing and manipulating relational databases. It allows users to create, read, update, and delete (CRUD) data within a database. SQL is essential for querying data, performing data analysis, and managing database structures.

**Example:**

### 2. **What are the different types of SQL commands?**

**Answer:**  
SQL commands are categorized into several types based on their functionality:

1. **DDL (Data Definition Language):** Defines the database structure.
2. `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `COMMENT`, `RENAME`
3. **DML (Data Manipulation Language):** Manipulates data within the database.
4. `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `CALL`
5. **DCL (Data Control Language):** Controls access to data.
6. `GRANT`, `REVOKE`
7. **TCL (Transaction Control Language):** Manages transactions within the database.
8. `COMMIT`, `ROLLBACK`, `SAVEPOINT`

**Example:**

### 3. **What is the difference between** `INNER JOIN` and `OUTER JOIN`?

**Answer:**

* **INNER JOIN:** Returns only the rows that have matching values in both tables.
* **OUTER JOIN:** Returns all rows from one table and the matched rows from the other. If there is no match, NULL values are returned for columns from the other table. There are three types:
* **LEFT OUTER JOIN (LEFT JOIN):** All rows from the left table and matched rows from the right table.
* **RIGHT OUTER JOIN (RIGHT JOIN):** All rows from the right table and matched rows from the left table.
* **FULL OUTER JOIN:** All rows when there is a match in one of the tables.

**Example:**

### 4. **What is a primary key?**

**Answer:**  
A primary key is a column or a set of columns in a table that uniquely identifies each row in that table. It must contain unique values and cannot contain NULLs. Each table should have one primary key.

**Example:**

### 5. **Explain the concept of normalization.**

**Answer:**  
Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables and defining relationships between them. The main goals are to eliminate duplicate data, ensure data dependencies make sense, and simplify the database structure.

**Normal Forms:**

1. **First Normal Form (1NF):** Ensure each column contains atomic (indivisible) values and each entry in a column is of the same data type.
2. **Second Normal Form (2NF):** Meet all requirements of 1NF and ensure that all non-key attributes are fully functionally dependent on the primary key.
3. **Third Normal Form (3NF):** Meet all requirements of 2NF and ensure that there are no transitive dependencies.

**Example:**  
Before Normalization:

After Normalization:

### 6. **What is a foreign key?**

**Answer:**  
A foreign key is a column or a set of columns in one table that establishes a link between data in two tables. It refers to the primary key in another table, ensuring referential integrity by restricting actions that would leave orphaned records.

**Example:**

### 7. **What are indexes and why are they used?**

**Answer:**  
Indexes are database objects that improve the speed of data retrieval operations on a table at the cost of additional storage and maintenance overhead. They work similarly to an index in a book, allowing the database to find rows more quickly without scanning the entire table.

**Types of Indexes:**

* **Unique Index:** Ensures that all values in the indexed column are unique.
* **Composite Index:** An index on multiple columns.
* **Clustered Index:** Determines the physical order of data in a table. Only one per table.
* **Non-Clustered Index:** A separate structure from the data table. Multiple can exist per table.

**Example:**

### 8. **What is a subquery, and how does it differ from a join?**

**Answer:**  
A subquery is a query nested inside another SQL query (such as `SELECT`, `INSERT`, `UPDATE`, or `DELETE`). It is used to perform operations that require multiple steps or conditions.

**Differences between Subquery and Join:**

* **Subquery:** Can be used to perform operations that are not easily achievable with joins, such as selecting records based on aggregated results.
* **Join:** Typically faster and more efficient for combining rows from two or more tables based on related columns.

**Example of Subquery:**

**Example of Join:**

### 9. **Explain the** `GROUP BY` clause and provide an example.

**Answer:**  
The `GROUP BY` clause is used in SQL to arrange identical data into groups. It is often used with aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) to perform calculations on each group.

**Example:**

**Result:**

| DeptID | EmployeeCount |
| --- | --- |
| 1 | 10 |
| 2 | 5 |
| 3 | 8 |

### 10. **What is a** `VIEW` in SQL and why would you use it?

**Answer:**  
A `VIEW` is a virtual table based on the result-set of an SQL statement. It contains rows and columns just like a real table but does not store data physically. Views can simplify complex queries, enhance security by restricting access to specific data, and provide a level of abstraction.

**Example:**

### 11. **What is the difference between** `DELETE`, `TRUNCATE`, and `DROP`?

**Answer:**

* **DELETE:**
* Removes rows from a table based on a `WHERE` clause.
* Can be rolled back if used within a transaction.
* Triggers are activated.
* Slower for large tables.
* **TRUNCATE:**
* Removes all rows from a table.
* Cannot be rolled back in some databases.
* Resets table identity.
* Faster than DELETE as it deallocates data pages.
* Triggers are not activated.
* **DROP:**
* Removes the entire table or database.
* All data and the table structure are deleted.
* Cannot be rolled back.
* Triggers are removed.

**Example:**

### 12. **What is a** `CROSS JOIN`?

**Answer:**  
A `CROSS JOIN` returns the Cartesian product of two tables, meaning it combines each row of the first table with every row of the second table. It does not require any condition to join the tables.

**Use Case:**

* Generating combinations of items, such as pairing every product with every customer for testing purposes.

**Example:**

**Result:**  
If `Employees` has 3 rows and `Departments` has 2 rows, the result will have 3 x 2 = 6 rows.

### 13. **Explain the concept of** `ACID` properties in databases.

**Answer:**  
`ACID` stands for Atomicity, Consistency, Isolation, and Durability. These properties ensure reliable processing of database transactions.

1. **Atomicity:** Ensures that all operations within a transaction are completed; if not, the transaction is aborted.
2. **Consistency:** Ensures that a transaction brings the database from one valid state to another, maintaining database invariants.
3. **Isolation:** Ensures that concurrently executing transactions do not interfere with each other.
4. **Durability:** Ensures that once a transaction is committed, it remains so, even in the event of a system failure.

**Example:**  
Consider a bank transfer where money is moved from Account A to Account B:

* **Atomicity:** Both the debit from A and credit to B must occur, or neither.
* **Consistency:** The total money remains the same before and after the transfer.
* **Isolation:** Concurrent transfers do not affect each other.
* **Durability:** Once the transfer is committed, it persists even if the system crashes.

### 14. **What is the** `HAVING` clause, and how is it different from `WHERE`?

**Answer:**  
The `HAVING` clause is used to filter groups created by the `GROUP BY` clause based on a specified condition. Unlike the `WHERE` clause, which filters rows before grouping, `HAVING` filters groups after aggregation.

**Example:**

### 15. **How do you optimize an SQL query?**

**Answer:**  
Optimizing SQL queries involves several strategies to improve performance:

1. **Use Indexes:** Create indexes on columns frequently used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
2. \**Avoid SELECT :* Retrieve only the necessary columns.
3. **Use Proper Joins:** Prefer `INNER JOIN` over `OUTER JOIN` when appropriate.
4. **Limit the Use of Subqueries:** Use joins instead of subqueries where possible.
5. **Optimize WHERE Clauses:** Use efficient conditions and avoid functions on indexed columns.
6. **Use Stored Procedures:** Reduce execution time by compiling queries.
7. **Analyze Query Execution Plans:** Identify and address bottlenecks.
8. **Partition Tables:** Divide large tables into smaller, more manageable pieces.
9. **Use Aggregate Functions Wisely:** Avoid unnecessary calculations in `SELECT` statements.
10. **Avoid Redundant Data:** Ensure the database is normalized to reduce redundancy.

**Example:**

*Explanation:* The optimized query allows the use of an index on `HireDate`, whereas applying the `YEAR()` function prevents index utilization.

---

### 16. **What is SQL?**

**Answer**:   
SQL (Structured Query Language) is a standardized programming language used to manage and manipulate relational databases. It is used to perform tasks such as querying, updating, inserting, and deleting data from a database.

### 17. **What is a Primary Key?**

**Answer**:   
A primary key is a unique identifier for a record in a table. It ensures that each record in the table can be uniquely identified. A table can have only one primary key, and it cannot contain `NULL` values.

**Example**:

### 18. **What is a Foreign Key?**

**Answer**:   
A foreign key is a column (or a set of columns) in a table that is used to create a link between the data in two tables. A foreign key in one table refers to the primary key in another table.

**Example**:

### 19. **What is a JOIN in SQL?**

**Answer**:   
A JOIN clause is used to combine rows from two or more tables based on a related column between them. Types of JOINs include:

* `INNER JOIN`
* `LEFT JOIN`
* `RIGHT JOIN`
* `FULL OUTER JOIN`

**Example (INNER JOIN)**:

### 20. **What is the difference between** `WHERE` and `HAVING`?

**Answer**:

* `WHERE` is used to filter records before any grouping (i.e., before `GROUP BY`).
* `HAVING` is used to filter records after grouping.

**Example**:

### 21. **What is the difference between** `DELETE` and `TRUNCATE`?

**Answer**:

* `DELETE` removes rows from a table based on a condition and can be rolled back (if within a transaction). It logs each row deletion.
* `TRUNCATE` removes all rows from a table without logging individual row deletions and is faster, but it cannot be rolled back in many databases.

**Example**:

### 22. **What is an Index in SQL?**

**Answer**:   
An index is a database object that improves the speed of data retrieval operations on a table. However, indexes can slow down `INSERT`, `UPDATE`, and `DELETE` operations.

**Example**:

### 23. **What is the difference between** `INNER JOIN` and `OUTER JOIN`?

**Answer**:

* `INNER JOIN` returns only the rows where there is a match between the tables.
* `OUTER JOIN` (including `LEFT`, `RIGHT`, and `FULL` joins) returns rows even when there is no match in one of the tables.

**Example**:

### 24. **How do you optimize a SQL query?**

**Answer**:

1. Use proper indexing.
2. Avoid `SELECT *` by specifying the columns needed.
3. Avoid `DISTINCT` when not necessary.
4. Use `EXISTS` instead of `IN` for better performance.
5. Write simpler, smaller subqueries.

### 25. **What is normalization?**

**Answer**:   
Normalization is the process of organizing data to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables and defining relationships between them.

### 26. **What are the different types of normalization?**

**Answer**:

1. **1NF (First Normal Form)**: Eliminate duplicate columns and create separate tables for related data.
2. **2NF (Second Normal Form)**: Eliminate partial dependencies by creating separate tables for subsets of data.
3. **3NF (Third Normal Form)**: Remove transitive dependencies where a non-key column depends on another non-key column.

### 27. **What is a subquery in SQL?**

**Answer**:   
A subquery is a query nested within another SQL query. It can be used in `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statements.

**Example**:

### 28. **What is a stored procedure?**

**Answer**:   
A stored procedure is a precompiled collection of SQL statements and optional control-of-flow statements, stored on the database server, that can be reused.

**Example**:

### 29. **What is a trigger in SQL?**

**Answer**:   
A trigger is a special type of stored procedure that automatically executes when certain events occur, such as an `INSERT`, `UPDATE`, or `DELETE`.

**Example**:

### 30. **What is a** `GROUP BY` clause?

**Answer**:   
The `GROUP BY` clause is used to group rows that have the same values in specified columns. It is commonly used with aggregate functions like `COUNT()`, `SUM()`, `AVG()`.

**Example**:

### 31. **What is the** `CASE` statement in SQL?

**Answer**:   
The `CASE` statement allows you to perform conditional logic in SQL queries.

**Example**:

### 32. **What are SQL constraints?**

**Answer**:   
SQL constraints are rules enforced on columns in a table to limit the type of data that can go into a table. Common constraints include:

* `NOT NULL`: Ensures that a column cannot have a NULL value.
* `UNIQUE`: Ensures that all values in a column are unique.
* `CHECK`: Ensures that all values in a column satisfy a specific condition.
* `DEFAULT`: Provides a default value for a column when none is specified.

### 33. **How do you use the** `LIMIT` or `TOP` clause in SQL?

**Answer**:   
The `LIMIT` clause in MySQL (or `TOP` in SQL Server) is used to specify the number of rows to return.

**Example (MySQL)**:

**Example (SQL Server)**:

### 34. **What is a View in SQL?**

**Answer**:   
A view is a virtual table that is based on the result set of an SQL query. Views do not store data themselves but display data from one or more tables.

**Example**:

### 35. **How do you handle NULL values in SQL?**

**Answer**:  
NULL represents a missing or undefined value in SQL. Functions like `IS NULL`, `IS NOT NULL`, and `COALESCE` can be used to handle NULL values.

**Example**:

### 36. **Find duplicate rows in a table.**

*Example*: Find duplicate records based on `column1` and `column2`.

### 37. **Left join and filter out nulls.**

*Example*: Get records from `table_a` that have a matching `id` in `table_b`.

### 38. **Window function for ranking data.**

*Example*: Rank rows in `your_table` based on the `value` column in descending order.

### 39. **Cumulative sum for a column.**

*Example*: Calculate cumulative sum of `value` based on the ordering of `id`.

### 40. **Difference between UNION and UNION ALL.**

1. `UNION`: Removes duplicates.
2. `UNION ALL`: Keeps all duplicates.