import sqlite3

# Connect to Sqlite
connection = sqlite3.connect("student.db")

# Create a cursor object to insert record, create table

cursor = connection.cursor()


# Create the table

table_info = """
    Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25));
"""

cursor.execute(table_info)

# Insert some records

cursor.execute('''Insert Into STUDENT values('Foo', 'DSA', 'A')''')
cursor.execute('''Insert Into STUDENT values('bar', 'DS', 'B')''')
cursor.execute('''Insert Into STUDENT values('foo2', 'DA', 'C')''')
cursor.execute('''Insert Into STUDENT values('baar', 'DMC', 'A')''')


# Display the records

print("The inserted records are ")
data = cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

# Close the connection
    
connection.commit()
connection.close()