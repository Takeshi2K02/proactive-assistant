import logging
from flask import jsonify
from datetime import datetime

class TaskService:
    def __init__(self, mongo_service):
        self.mongo_service = mongo_service

    def add_task(self, user_input, user_id):
        task_details = user_input.replace("add task", "").strip()
        task_data = {
            "task_description": task_details,
            "user_id": user_id,
            "status": "pending",
            "priority_level": "medium",
            "due_date": None,
            "creation_timestamp": datetime.now(),
            "context_tags": [],
            "notes": ""
        }
        self.mongo_service.insert_task(task_data)
        logging.info("Task added to MongoDB for user %s: %s", user_id, task_details)
        return jsonify({'response': f"Task '{task_details}' added."})

    def view_tasks(self, user_id):
        task_list = self.mongo_service.get_tasks(user_id)
        logging.info("Retrieved task list for user %s: %s", user_id, task_list)

        if not task_list:
            return jsonify({'response': "You have no tasks."})

        task_descriptions = [
            (
                f"Task ID: {task['task_id']}, "
                f"Description: {task['task_description']}, "
                f"Status: {task['status']}, "
                f"Priority: {task['priority_level']}, "
                f"Due Date: {task.get('due_date', 'No due date')}, "
                f"Created On: {task.get('creation_timestamp', '')}, "
                f"Tags: {', '.join(task.get('context_tags', []))}, "
                f"Notes: {task['notes']}"
            )
            for task in task_list
        ]
        
        return jsonify({'response': "Here are your tasks: " + "; ".join(task_descriptions)})