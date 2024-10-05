import re
import json

# Math functions
def add(x, y):
    """Returns the sum of x and y."""
    return x + y

def div(x, y):
    """Returns the division of x by y. Handles division by zero."""
    try:
        return x / y
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."

def mult(x, y):
    """Returns the product of x and y."""
    return x * y

def sub(x, y):
    """Returns the difference between x and y."""
    return x - y

# Predefined responses stored in a dictionary
responses = {
    "math": ["math", "can you do math", "calculate", "help me add", "help me subtract", "help me multiply", "help me divide"],
    "greeting": ["hello", "hi", "hey"],
    "farewell": ["bye", "goodbye"],
    "how_are_you": ["how are you", "how's it going"],
    "help": ["help", "assist", "support"],
    "addNums": ["add", "add these"]
}

# Response mappings
response_map = {
    "math": "I am happy to help you out! I can add, subtract, multiply, and divide numbers. Just type one of those words to get started!",
    "greeting": "Hi there! How can I assist you today?",
    "farewell": "Goodbye! Have a great day!",
    "how_are_you": "I'm just a computer program, but thanks for asking! How can I help you?",
    "help": "Sure! What do you need help with?",
    "addNums": add,
    "divide_numbers": div,
    "multiply_numbers": mult,
    "subtract_numbers": sub,
}

def match_pattern(user_input):
    """Matches user input to predefined patterns."""
    for key, patterns in responses.items():
        for pattern in patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return key
    return None

def log_conversation(user_input, bot_response):
    """Logs the conversation to a file."""
    with open("chat_log.json", "a") as log_file:
        log_entry = {"user": user_input, "bot": bot_response}
        json.dump(log_entry, log_file)
        log_file.write("\n")

def chatbot_response(user_input):
    """Generates a response based on user input."""
    matched_key = match_pattern(user_input)
   
    if matched_key:
        response = response_map[matched_key]
        if callable(response):
            numbers = re.findall(r'\d+', user_input)
            if len(numbers) == 2:
                x, y = map(float, numbers)
                result = response(x, y)
                return f"The result of the operation is {result}."
            else:
                return "Please provide 2 numbers to perform the operation."
    else:
        response = "I'm sorry, I didn't understand that. Can you rephrase?"

    log_conversation(user_input, response)
    return response

def main():
    """Main function to run the chatbot."""
    print("Welcome to the Chatbot! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
