import sqlite3
import csv

# Replace 'your_database.db' with the path to your SQLite database file
db_file = 'database1.db'

# Connect to the database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get a list of table names in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Export each table to a CSV file
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()

    with open(f'{table_name}.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # Write column headers
        csv_writer.writerows(data)  # Write table data

# Close the database connection
conn.close()
