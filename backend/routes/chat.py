import requests
from flask import Blueprint, request, jsonify
from utils.token_helper import get_historical_data, count_tokens
from config import SYSTEM_PROMPT

chat_bp = Blueprint('chat', __name__)

GEMINI_API_KEY = 'AIzaSyAKogh4AqTsQESzHoGqIketpNnhMmZoPNI'
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Configuration
HISTORICAL_TOKENS_LIMIT = 6000  # Adjust as needed
INITIAL_MESSAGE = "Hello! How can I assist you today?"  # Initial bot response

messages = []  # Store chat history

@chat_bp.route('', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # If there's no user input, return the initial message
    if not user_input:
        return jsonify({'response': INITIAL_MESSAGE})

    # Get historical data (excluding system prompt)
    historical_data = get_historical_data(messages, HISTORICAL_TOKENS_LIMIT)

    # Prepare conversation history (System prompt + historical data + new input)
    conversation_parts = [{"text": SYSTEM_PROMPT}]  # System prompt first
    for message in historical_data:
        conversation_parts.append({"text": f"User: {message['question']}"})
        conversation_parts.append({"text": f"Assistant: {message['answer']}"})

    # Add new user input
    conversation_parts.append({"text": f"User: {user_input}"})

    # Prepare payload
    payload = {
        "contents": [{"parts": conversation_parts}]
    }

    # Set headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Send request to Gemini API
    response = requests.post(
        GEMINI_URL, 
        params={'key': GEMINI_API_KEY}, 
        headers=headers, 
        json=payload
    )

    # Process response
    if response.status_code == 200:
        gemini_response = response.json()
        print("Gemini Response: ", gemini_response)  # Log for debugging
        
        try:
            gemini_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            
            # Ensure only user messages are stored, NOT system prompt
            messages.append({"question": user_input, "answer": gemini_text})
            
            return jsonify({'response': gemini_text})
        except KeyError:
            return jsonify({'error': 'Unexpected response format from Gemini API'}), 500
    else:
        print("Error Response: ", response.text)  # Log for debugging
        return jsonify({'error': 'Error in Gemini API request', 'details': response.text}), 500