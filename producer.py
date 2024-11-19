import csv
import random
import uuid

FILENAME = 'tasks.csv'


def add_task():
    task_id = str(uuid.uuid4())
    description = f"Rozmowa telefoniczna {random.randint(1, 100001)}"
    task = {
        'id': task_id,
        'description': description,
        'status': 'pending'
    }

    file_exists = False
    try:
        with open(FILENAME, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=task.keys(), delimiter='|')
        if not file_exists:
            writer.writeheader()
        writer.writerow(task)

    print(f"Zadanie zostało zapisane w pliku {FILENAME}")


if __name__ == "__main__":
    add_task()
