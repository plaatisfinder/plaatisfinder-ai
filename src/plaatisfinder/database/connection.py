from pathlib import Path
import sqlite3

DB_PATH = Path("data/database.db")


def get_connection():

    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn