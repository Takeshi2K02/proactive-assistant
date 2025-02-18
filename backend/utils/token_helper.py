import tiktoken  # Ensure you have this installed: pip install tiktoken

def count_tokens(text):
    """Returns the number of tokens in a given text."""
    encoder = tiktoken.get_encoding("cl100k_base")  # Change encoding if needed
    return len(encoder.encode(text))

def get_historical_data(messages, max_tokens):
    """Retrieves historical messages without exceeding token limits."""
    historical_data = []
    total_tokens = 0

    for message in reversed(messages):  
        question_tokens = count_tokens(message['question'])
        answer_tokens = count_tokens(message['answer'])

        if total_tokens + question_tokens + answer_tokens <= max_tokens:
            historical_data.append(message)
            total_tokens += question_tokens + answer_tokens
        else:
            break

    return historical_data