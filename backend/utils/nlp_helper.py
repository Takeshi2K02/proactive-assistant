def extract_intent_and_entities(gemini_response):
    """
    Extracts intent and entities from the Gemini API response.
    """
    try:
        intent = gemini_response['candidates'][0]['intent']  # Modify based on actual response
        entities = gemini_response['candidates'][0]['entities']  # Modify based on actual response
        return intent, entities
    except KeyError:
        return None, {}