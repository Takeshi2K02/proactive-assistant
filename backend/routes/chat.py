import logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.token_helper import get_historical_data
from config import SYSTEM_PROMPT
from services.mongo_service import MongoService
from services.task_service import TaskService
from services.gemini_service import GeminiService

# Initialize services
mongo_service = MongoService()
task_service = TaskService(mongo_service)
gemini_service = GeminiService()

# Blueprint for chat routes
chat_bp = Blueprint('chat', __name__)

# Configuration
HISTORICAL_TOKENS_LIMIT = 6000
INITIAL_MESSAGE = "Hello! How can I assist you today?"
messages = []

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_intent(user_input):
    if "add task" in user_input.lower():
        return "Add Task"
    elif "view tasks" in user_input.lower():
        return "View Tasks"
    return "Unknown Intent"

@chat_bp.route('', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_id = request.json.get('user_id', "some_user_id")  # Default user ID

    if not user_input:
        return jsonify({'response': INITIAL_MESSAGE})

    intent = extract_intent(user_input)

    if intent == "Add Task":
        return task_service.add_task(user_input, user_id)

    elif intent == "View Tasks":
        return task_service.view_tasks(user_id)

    # Otherwise, handle with Gemini API
    return gemini_service.process_gemini_response(user_input, messages)