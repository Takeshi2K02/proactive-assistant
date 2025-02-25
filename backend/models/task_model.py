from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="proactive_assistant"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_task(self, task_data):
        return self.db.tasks.insert_one(task_data)

    def get_tasks(self, user_id):
        return list(self.db.tasks.find({"user_id": user_id}))


class TaskModel:
    def __init__(self, task_description, user_id, status="pending", priority_level="medium", 
                 due_date=None, context_tags=None, notes=""):
        self.task_description = task_description
        self.user_id = user_id
        self.status = status
        self.priority_level = priority_level
        self.due_date = due_date
        self.creation_timestamp = datetime.now()
        self.context_tags = context_tags if context_tags else []
        self.notes = notes

    def to_dict(self):
        """Convert the task model to a dictionary for MongoDB storage."""
        return {
            "task_description": self.task_description,
            "user_id": self.user_id,
            "status": self.status,
            "priority_level": self.priority_level,
            "due_date": self.due_date,
            "creation_timestamp": self.creation_timestamp,
            "context_tags": self.context_tags,
            "notes": self.notes
        }

    @staticmethod
    def from_dict(data):
        """Convert a MongoDB document to a TaskModel instance."""
        return TaskModel(
            task_description=data.get("task_description", "Unknown Task"),
            user_id=data.get("user_id"),
            status=data.get("status", "pending"),
            priority_level=data.get("priority_level", "medium"),
            due_date=data.get("due_date"),
            context_tags=data.get("context_tags", []),
            notes=data.get("notes", "")
        )

    @staticmethod
    def serialize(task):
        """Serialize a task document for API response."""
        return {
            "task_id": str(task["_id"]) if isinstance(task["_id"], ObjectId) else task["_id"],
            "task_description": task.get("task_description", "Unknown Task"),
            "status": task.get("status", "pending"),
            "priority_level": task.get("priority_level", "medium"),
            "due_date": task.get("due_date", "No due date"),
            "creation_timestamp": task.get("creation_timestamp", ""),
            "context_tags": task.get("context_tags", []),
            "notes": task.get("notes", "")
        }