from queue_manager import QueueManager
from tasks import process_image_task
from tasks import RESULTS_DIR
import os
import time

queue_manager = QueueManager()


while True:
    task = queue_manager.consume_task()
    if not task:
        time.sleep(1)  # Wait for new task
        continue

    task_id = task.task_id
    try:
        print(f"Processing task: {task_id}")
        processed_image = process_image_task(task)
        result_filename = f"[{task_id}]-[{processed_image.person_count}].jpg"
        os.rename(processed_image.result_path,
                  f"{RESULTS_DIR}/{result_filename}")

        print(f"Task {task_id} completed. Result saved as {result_filename}.")
    except Exception as e:
        print(f"Task {task_id} failed: {e}")
