import sqlite3

DB_NAME = 'queues_on_sqlite.db'


def read_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')

    tasks = cursor.fetchall()
    for task in tasks:
        print(f"ID: {task[0]}, Description: {task[1]},"
              f"Status: {task[2]}, Timestamp: {task[3]}")

    conn.close()


if __name__ == "__main__":
    read_tasks()
