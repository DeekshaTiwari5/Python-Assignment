import sqlite3
from prettytable import PrettyTable

# Connect to the database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM books")

# Fetch all results
rows = cursor.fetchall()

# Create a PrettyTable object
table = PrettyTable()
table.field_names = [description[0] for description in cursor.description]

# Add rows to the table
for row in rows:
    table.add_row(row)

# Print the table
print(table)

# Close the connection
conn.close()
