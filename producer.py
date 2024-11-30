import sqlite3
import random
import uuid

DB_NAME = 'queues_on_sqlite.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            description TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_task():
    task_id = str(uuid.uuid4())
    description = f"Rozmowa telefoniczna {random.randint(1, 100001)}"
    status = 'pending'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (id, description, status) VALUES (?, ?, ?)
    ''', (task_id, description, status))
    conn.commit()
    conn.close()

    print(f"Zadanie zostało zapisane w bazie danych {DB_NAME}")

if __name__ == "__main__":
    init_db()
    add_task()