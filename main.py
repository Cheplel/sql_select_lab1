# Importing SQL Library and Pandas
import sqlite3
from turtle import pd
import pandas as pd
# Connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    salary REAL
)
""")

#Delete old data from the employees table
cursor.execute("DELETE FROM employees")
conn.commit()

employees = [
    ("Jude", "Daniels", "IT", 60000),
    ("Aisha", "Singh", "HR", 55000),
    ("Zane", "Williams", "Finance", 70000),
    ("Liam", "Brown", "IT", 65000),
    ("Mia", "Davis", "Marketing", 58000),
    ("Noah", "Wilson", "Finance", 72000),
    ("Emma", "Taylor", "HR", 56000),
    ("Olivia", "Anderson", "Marketing", 59000),
    ("Ava", "Thomas", "IT", 64000),
    ("Isabella", "Jackson", "Finance", 71000)
]

cursor.executemany(
    """
    INSERT INTO employees (first_name, last_name, department, salary)
    VALUES (?, ?, ?, ?)
    """,
    employees,
)

conn.commit()


# Selecting all data from the employees table
employee_data = pd.read_sql("""SELECT * FROM employees""", conn)
print("---------------------Employee Data---------------------")
print(employee_data)
print("-------------------End Employee Data-------------------")


df_first_five = pd.read_sql("""
SELECT 
    id AS employeeNumber,
    last_name AS lastName
FROM employees
""", conn)
print("---------------------Employee Number and Last Name---------------------")
print(df_first_five)

# Having last name of employees before employee number
df_five_reverse = pd.read_sql(
    "SELECT last_name AS last_name, id AS employee_id FROM employees",
    conn
)
print("---------------------Last Name and ID of Employees---------------------")
print(df_five_reverse)


# Adding a new column to the employees table
cursor.execute("PRAGMA table_info(employees)")
columns = [col[1] for col in cursor.fetchall()]

if "role" not in columns:
    cursor.execute("""
    ALTER TABLE employees
    ADD COLUMN role TEXT
    """)

conn.commit()

cursor.execute("UPDATE employees SET role = 'Software Engineer' WHERE id = 1")
cursor.execute("UPDATE employees SET role = 'HR Manager' WHERE id = 2")
cursor.execute("UPDATE employees SET role = 'Financial Analyst' WHERE id = 3")
cursor.execute("UPDATE employees SET role = 'IT Support' WHERE id = 4")
cursor.execute("UPDATE employees SET role = 'Marketing Specialist' WHERE id = 5")
cursor.execute("UPDATE employees SET role = 'Financial Analyst' WHERE id = 6")
cursor.execute("UPDATE employees SET role = 'HR Manager' WHERE id = 7")
cursor.execute("UPDATE employees SET role = 'Marketing Specialist' WHERE id = 8")
cursor.execute("UPDATE employees SET role = 'IT Support' WHERE id = 9")
cursor.execute("UPDATE employees SET role = 'Financial Analyst' WHERE id = 10")

conn.commit()
print("---------------------Employee Data with Roles---------------------")
employee_data_with_roles = pd.read_sql("""SELECT * FROM employees""", conn)
print(employee_data_with_roles)

# Executive and Non Executive employees
df_executive = pd.read_sql("""
SELECT *,
CASE
    WHEN salary >= 70000 THEN 'Executive'
    ELSE 'Not Executive'
END AS role
FROM employees
""", conn)

print("---------------------Executive Employees---------------------")
print(df_executive)

# Find the length of the last names of employees
df_name_length = pd.read_sql("SELECT last_name FROM employees", conn)
df_name_length['name_length'] = df_name_length.iloc[:, 0].apply(len)
print("---------------------Length of Last Names of Employees---------------------")
print(df_name_length)

# Returning the first 2 letters of each employees job role
df_short_title = pd.read_sql("SELECT role, SUBSTR(role, 1, 2) as short_title FROM employees", conn)
print("---------------------First 2 Letters of Job Roles---------------------")
print(df_short_title)

#New Table Creation
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS orderDetails (
    order_id INTEGER PRIMARY KEY,
    product_name TEXT,
    quantity INTEGER,
    price REAL
)
""")

#Delete old data from the orderDetails table
cursor.execute("DELETE FROM orderDetails")
conn.commit()

order_details_data = [
    (1, "Laptop", 2, 1200.00),
    (2, "Smartphone", 5, 800.00),
    (3, "Headphones", 10, 150.00),
    (4, "Monitor", 3, 300.00),
    (5, "Keyboard", 7, 100.00)
]


cursor.executemany(
    """
    INSERT INTO orderDetails (order_id, product_name, quantity, price)
    VALUES (?, ?, ?, ?)
    """,
    order_details_data
)

conn.commit()

order_details = pd.read_sql("""SELECT * FROM orderDetails;""", conn) 
print("------------------Order Details Data------------------")
print(order_details)
print("----------------End Order Details Data----------------")


# Total amount of all orders
# Total amount of all orders
cursor.execute("""
SELECT SUM(quantity * price)
FROM orderDetails
""")

sum_total_price = cursor.fetchone()

print("---------------------Total Amount of All Orders---------------------")
print(sum_total_price)

# Day, Month, and Year of Orders
cursor.execute("PRAGMA table_info(orderDetails)")
columns = [col[1] for col in cursor.fetchall()]

if "order_date" not in columns:
    cursor.execute("""
    ALTER TABLE orderDetails
    ADD COLUMN order_date TEXT
    """)

conn.commit()

# Add dates to existing orders
order_dates = [
    ("2023-01-15", 1),
    ("2023-02-20", 2),
    ("2023-03-10", 3),
    ("2023-04-05", 4),
    ("2023-05-12", 5)
]

cursor.executemany(
    """
    UPDATE orderDetails
    SET order_date = ?
    WHERE order_id = ?
    """,
    order_dates
)

conn.commit()

# Now select the formatted dates
df_day_month_year = pd.read_sql("""
SELECT
strftime('%d', order_date) AS day,
strftime('%m', order_date) AS month,
strftime('%Y', order_date) AS year
FROM orderDetails
""", conn)

print("---------------------Day, Month, and Year of Orders---------------------")
print(df_day_month_year)

conn.close()