from flask import Blueprint, request, jsonify
from bson import ObjectId  # Import ObjectId for serialization

tasks_bp = Blueprint('tasks', __name__)

def get_db():
    from models.task_model import MongoDB  # Import inside the function
    return MongoDB()

# Create Task (POST)
@tasks_bp.route('/', methods=['POST'])
def create_task():
    mongo = get_db()  # Create instance inside the function
    task_data = request.json
    task_id = mongo.insert_task(task_data)
    return jsonify({"task_id": str(task_id.inserted_id)}), 201

# Get All Tasks (GET)
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    mongo = get_db()
    tasks = mongo.get_all_tasks()
    
    # Convert ObjectId to string before returning JSON
    tasks_serializable = [{**task, "_id": str(task["_id"])} for task in tasks]
    
    return jsonify(tasks_serializable), 200

# Update Task (PUT)
@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    mongo = get_db()
    updates = request.json
    mongo.update_task(task_id, updates)
    return jsonify({"message": "Task updated"}), 200

# Delete Task (DELETE)
@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    mongo = get_db()
    mongo.delete_task(task_id)
    return jsonify({"message": "Task deleted"}), 204
