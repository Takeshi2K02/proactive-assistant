import requests
from flask import Blueprint, request, jsonify

chat_bp = Blueprint('chat', __name__)

GEMINI_API_KEY = 'AIzaSyAKogh4AqTsQESzHoGqIketpNnhMmZoPNI'
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@chat_bp.route('', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    # Prepare the payload for Gemini API request
    payload = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }
    
    # Set the headers
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Send the POST request to Gemini API
    response = requests.post(
        GEMINI_URL, 
        params={'key': GEMINI_API_KEY}, 
        headers=headers, 
        json=payload
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Log the full response for debugging
        gemini_response = response.json()
        print("Gemini Response: ", gemini_response)  # Log for debugging

        # Extract the text from the response structure
        try:
            gemini_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': gemini_text})
        except KeyError:
            return jsonify({'error': 'Unexpected response format from Gemini API'}), 500
    else:
        # Log the error for debugging
        print("Error Response: ", response.text)  # Log for debugging
        return jsonify({'error': 'Error in Gemini API request', 'details': response.text}), 500

# from flask import Blueprint, request, jsonify
# import requests
# import markdown

# chat_bp = Blueprint('chat', __name__)

# GEMINI_API_KEY = 'AIzaSyAKogh4AqTsQESzHoGqIketpNnhMmZoPNI'
# GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# @chat_bp.route('', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
    
#     # Prepare the payload for Gemini API request
#     payload = {
#         "contents": [{
#             "parts": [{"text": user_input}]
#         }]
#     }
    
#     # Set the headers
#     headers = {
#         'Content-Type': 'application/json',
#     }
    
#     # Send the POST request to Gemini API
#     response = requests.post(
#         GEMINI_URL, 
#         params={'key': GEMINI_API_KEY}, 
#         headers=headers, 
#         json=payload
#     )

#     # Check if the request was successful
#     if response.status_code == 200:
#         gemini_response = response.json()

#         try:
#             gemini_text = gemini_response['candidates'][0]['content']['parts'][0]['text']

#             # If the response contains Markdown, convert it to HTML
#             html_response = markdown.markdown(gemini_text)  # Converts Markdown to HTML
            
#             return jsonify({'response': html_response})
#         except KeyError:
#             return jsonify({'error': 'Unexpected response format from Gemini API'}), 500
#     else:
#         return jsonify({'error': 'Error in Gemini API request', 'details': response.text}), 500

