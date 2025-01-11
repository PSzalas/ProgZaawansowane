from enum import Enum


class TaskStatus(Enum):
    NOTFOUND = "Not Found"
    ENQUEUED = "Enqueued"
    COMPLETED = "Completed"
