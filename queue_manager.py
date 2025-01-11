from typing import Optional, Dict

import pika
import json

from Enums.TaskStatus import TaskStatus
from Task import Task


class QueueManager:
    def __init__(self, queue_name: str = 'task_queue'):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        self.task_status_store: Dict[str, Task] = {}

    def publish_task(self, task_data: Task) -> None:
        task_data.status = TaskStatus.ENQUEUED
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(task_data.__dict__()),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        self.task_status_store[task_data.task_id] = task_data

    def consume_task(self) -> Optional[Task]:
        (method_frame, header_frame, body) = (
            self.channel.basic_get(queue=self.queue_name, auto_ack=True))
        if body:
            task = json.loads(body)
            return Task(task['task_id'], task['image_path'], task['image_url'])
        return None

    def get_task_status(self, task_id: str) -> Optional[Task]:
        try:
            self.task_status_store[task_id]
        except KeyError:
            return None

        return self.task_status_store[task_id]
