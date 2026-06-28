import sqlite3

from fastapi import Depends
from typing import Annotated

def get_db():
    connection = sqlite3.connect("database/database.db", check_same_thread=False)
    # Enable column name access for query results
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    try:
        yield cursor, connection
    finally:
        connection.close()

db_dependency = Annotated[tuple[sqlite3.Cursor, sqlite3.Connection], Depends(get_db)]

if __name__ == "__main__":
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    with open("database/tables.sql", "r") as f:
        cursor.executescript(f.read())  
    connection.commit()
