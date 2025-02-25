from pymongo import MongoClient
from config import MONGODB_URI
from models.task_model import TaskModel
from bson import ObjectId

class MongoService:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.proactive_assistant  # Database name
        self.tasks_collection = self.db.tasks  # Collection name

    def insert_task(self, task_data: TaskModel):
        """Insert a new task into the database."""
        result = self.tasks_collection.insert_one(task_data)
        return str(result.inserted_id)

    def get_tasks(self, user_id=None):
        """Retrieve tasks for a specific user."""
        query = {"user_id": user_id} if user_id else {}
        tasks = list(self.tasks_collection.find(query))
        return [TaskModel.serialize(task) for task in tasks]

    def get_task_by_id(self, task_id):
        """Retrieve a single task by its ID."""
        task = self.tasks_collection.find_one({"_id": ObjectId(task_id)})
        return TaskModel.serialize(task) if task else None

    def update_task(self, task_id, updates):
        """Update a task by its ID."""
        return self.tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": updates}
        )

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        return self.tasks_collection.delete_one({"_id": ObjectId(task_id)})