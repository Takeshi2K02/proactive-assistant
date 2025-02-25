import requests
from flask import jsonify
from config import SYSTEM_PROMPT, GEMINI_API_KEY

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
HISTORICAL_TOKENS_LIMIT = 6000

class GeminiService:
    def process_gemini_response(self, user_input, messages):
        historical_data = self.get_historical_data(messages)

        conversation_parts = [{"text": SYSTEM_PROMPT}]
        for message in historical_data:
            conversation_parts.append({"text": f"User: {message['question']}."})
            conversation_parts.append({"text": f"Assistant: {message['answer']}."})

        conversation_parts.append({"text": f"User: {user_input}."})

        payload = {"contents": [{"parts": conversation_parts}]}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            GEMINI_URL,
            params={'key': GEMINI_API_KEY},
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return self.format_gemini_response(response, user_input, messages)
        else:
            return jsonify({'error': 'Error in Gemini API request', 'details': response.text}), 500

    def get_historical_data(self, messages):
        return messages[-HISTORICAL_TOKENS_LIMIT:] if len(messages) > HISTORICAL_TOKENS_LIMIT else messages

    def format_gemini_response(self, response, user_input, messages):
        try:
            gemini_response = response.json()
            gemini_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            messages.append({"question": user_input, "answer": gemini_text})
            return jsonify({'response': gemini_text})
        except KeyError:
            return jsonify({'error': 'Unexpected response format from Gemini API'}), 500