import sqlite3
import time

DB_NAME = 'queues_on_sqlite.db'


def read_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, status '
                   'FROM tasks ORDER BY timestamp ASC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task_status(task_id: str, new_status: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET status = ? WHERE id = ?
    ''', (new_status, task_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def consume_task():
    tasks = read_tasks()
    for task in tasks:
        task_id, description, status = task
        if status == 'pending':
            print(f"Znaleziono zadanie do wykonania: {description}")
            update_task_status(task_id, 'in_progress')
            print(f"Rozpoczynam zadanie: {description} (id: {task_id})")
            time.sleep(30)
            update_task_status(task_id, 'done')
            print(f"Zakończono zadanie: {description} (id: {task_id})")
            return True
    return False


if __name__ == "__main__":
    print("Consumer uruchomiony.")
    while True:
        print("Sprawdzanie zadań...")
        if not consume_task():
            print("Brak zadań do wykonania. Oczekiwanie...")
        time.sleep(5)
