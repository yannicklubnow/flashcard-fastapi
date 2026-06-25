import sqlite3

connection = sqlite3.connect("database/database.db")
# Enable column name access for query results
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")

if __name__ == "__main__":
    with open("database/tables.sql", "r") as f:
        cursor.executescript(f.read())  
    connection.commit()
