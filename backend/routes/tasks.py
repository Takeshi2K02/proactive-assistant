from flask import Blueprint, request, jsonify

tasks_bp = Blueprint('tasks', __name__)

tasks = []

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    task_data = request.json
    tasks.append(task_data)
    return jsonify({'message': 'Task added successfully!', 'task': task_data}), 201

@tasks_bp.route('/list', methods=['GET'])
def list_tasks():
    return jsonify({'tasks': tasks})