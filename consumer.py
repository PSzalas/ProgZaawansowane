import csv
import time

FILENAME = 'tasks.csv'


def read_tasks():
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.DictReader(file, delimiter='|')
            return list(reader)
    except FileNotFoundError:
        return []


def update_task_status(task_id: str, new_status: str):
    tasks = read_tasks()
    updated = False

    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=tasks[0].keys() if tasks else [],
                                delimiter='|')
        if tasks:
            writer.writeheader()
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = new_status
                    updated = True
                writer.writerow(task)
    return updated


def consume_task():
    tasks = read_tasks()
    for task in tasks:
        if task['status'] == 'pending':
            print(f"Znaleziono zadanie do wykonania: "
                  f"{task['description']}")
            update_task_status(task['id'], 'in_progress')
            print(f"Rozpoczynam zadanie: "
                  f"{task['description']} (id: {task['id']})")
            time.sleep(30)
            update_task_status(task['id'], 'done')
            print(f"Zakończono zadanie: "
                  f"{task['description']} (id: {task['id']})")
            return True
    return False


if __name__ == "__main__":
    print("Consumer uruchomiony.")
    while True:
        print("Sprawdzanie zadań...")
        if not consume_task():
            print("Brak zadań do wykonania. Oczekiwanie...")
        time.sleep(5)
