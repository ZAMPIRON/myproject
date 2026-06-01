import sqlite3
from flask import g

DATABASE = "buddy.db"

def get_db():
    # it returns a connection to the database, creating it if it doesn't exist
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        # Permite acessar os dados como dicionários (ex: user["github"])
        g.db.row_factory = sqlite3.Row 
    return g.db

def init_db():
    # inicialize the database with the necessary tables
    db = get_db()
    
    # create users table if it doesn't exist
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            github TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            country TEXT NOT NULL,
            has_idea TEXT DEFAULT 'no',
            pitch TEXT DEFAULT ''
        )
    """)
    db.commit()

def close_db(e=None):
    # it closes the database connection at the end of the request
    db = g.pop("db", None)
    if db is not None:
        db.close()