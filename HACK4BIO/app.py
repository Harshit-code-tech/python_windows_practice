#app.py
from flask import Flask, request, jsonify
import requests
import google.generativeai as generativeai
import my_key
from typing import Text
import logging
# Configure the Generative AI client
generativeai.configure(api_key=my_key.API_KEY)

# Initialize the model
model = generativeai.GenerativeModel('gemini-1.0-pro-latest')

app = Flask(__name__)

# Rasa server endpoint
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

VALID_LOCATIONS = [
    "India", "China", "Brazil", "Indonesia", "Colombia",
    "Democratic Republic of the Congo", "Peru", "Mexico", "South Africa", "Ethiopia"
]
# Function to handle the combined response from Rasa and Gemini API
def handle_combined_response(user_message):
    # Query Rasa
    rasa_response = query_rasa(user_message)
    rasa_intent = rasa_response[0]['intent']['name']
    
    # Check if Rasa intent is related to biodiversity
    if rasa_intent == 'biodiversity':
        # Generate bioheritage info using Gemini API
        bio_info = generate_bioheritage_info(user_message)
        
        # If bioheritage info is not found or empty, fallback to Rasa response
        if not bio_info:
            return jsonify(rasa_response)
        
        return jsonify({"response": bio_info})
    
    # If Rasa intent is not related to biodiversity, return Rasa response
    return jsonify(rasa_response)

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json.get("message")
    print("Received user message:", user_message)

    if is_bioheritage_query(user_message):
        print("User message is related to bioheritage")
        bio_info = generate_bioheritage_info(user_message)
        return jsonify({"response": bio_info})
    else:
        print("User message is not related to bioheritage")
        rasa_response = query_rasa(user_message)
        return jsonify(rasa_response)

def is_bioheritage_query(user_message):
    bio_keywords = ["animal", "plant", "species", "habitat", "conservation", "nature", "biodiversity"]
    for keyword in bio_keywords:
        if keyword in user_message.lower():
            return True
    return False


def generate_bioheritage_info(user_message):
    user_input = user_message.strip().split(" ")
    if len(user_input) < 2:
        return "Sorry, I couldn't understand your query."

    query_type = user_input[0].lower()
    topic = " ".join(user_input[1:])
    prompts = {
        "bio_condition": f"Tell me about the bio condition of {topic}.",
        "bioheritage": f"Tell me about the bioheritage of {topic}.",
        "animal": f"Tell me about the animal {topic}.",
        "plant": f"Tell me about the plant {topic}.",
        "nature": f"Tell me about nature in {topic}.",
        "biodiversity": f"Tell me about the current biodiversity system in {topic}.",
    }

    if query_type not in prompts:
        return "Did you mean to ask about the 'bio condition' or 'bioheritage' of a location, or perhaps information about a specific animal or plant found there? For example, you could try 'bioheritage of India' or 'what animal is native to India'?"

    if query_type in ["bio_condition", "bioheritage"] and topic.lower() not in VALID_LOCATIONS:
        return f"Sorry, I don't have information about {query_type.replace('_', ' ')} in '{topic}'. Here are some valid locations: {', '.join(VALID_LOCATIONS[:5])} (and more)"

    try:
        response = model.generate_content(prompt=prompts[query_type])
        return response['generated_text']
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an issue while generating information. Please try again later."


def query_rasa(user_message):
    response = requests.post(RASA_ENDPOINT, json={"message": user_message})
    return response.json()

if __name__ == '__main__':
    app.run(port=5055, debug=True)
