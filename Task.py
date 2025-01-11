from Enums.TaskStatus import TaskStatus


class Task:
    def __init__(self, task_id: str = None, image_path: str = None,
                 image_url: str = None, number_of_people: int = None,
                 status: TaskStatus = TaskStatus.NOTFOUND):
        self.task_id = task_id
        self.image_path = image_path
        self.image_url = image_url
        self.number_of_people = number_of_people
        self.status = status

    def __dict__(self):
        return {
            'task_id': self.task_id,
            'image_path': self.image_path,
            'image_url': self.image_url,
            'number_of_people': self.number_of_people,
            'status': self.status.value,
        }
