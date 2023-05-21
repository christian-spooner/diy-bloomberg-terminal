import sqlite3

# create a connection to the database
conn = sqlite3.connect("db/equities.db")
# create a cursor object
cursor = conn.cursor()
# create a table
cursor.execute(
    """CREATE TABLE users
                (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"""
)

# insert data into the table
cursor.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)", ("John", "john@example.com")
)

# commit the changes
conn.commit()
# close the connection
conn.close()
