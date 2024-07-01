from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import os

def call_gemini_api(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": prompt}
    response = requests.post("https://asia-south1-aiplatform.googleapis.com", headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        return data.get("generated_text", "")
    else:
        return None

class ActionGreet(Action):
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Hi there! How can I help you today?")
        return []

class ActionLocalFlora(Action):
    def name(self):
        return "action_local_flora"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="Could you please specify the location you are interested in?")
            return []

        prompt = f"Describe the typical flora found in {location}"
        response = call_gemini_api(prompt)
        if response:
            dispatcher.utter_message(text="Sure, let me access some information and tell you. Here's what I found about the local plants:")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find information about the local flora. Would you like to try with a different area?")
        return []

class ActionLocalFauna(Action):
    def name(self):
        return "action_local_fauna"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="Could you please specify the location you are interested in?")
            return []

        prompt = f"List some interesting animals that live in {location}"
        response = call_gemini_api(prompt)
        if response:
            dispatcher.utter_message(text="This region is home to a diverse range of fauna. Here's what I found:")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find information about the local fauna. Would you like to know about something else?")
        return []

class ActionHistoricalSites(Action):
    def name(self):
        return "action_historical_sites"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="Could you please specify the location you are interested in?")
            return []

        prompt = f"What are some historical landmarks near {location}"
        response = call_gemini_api(prompt)
        if response:
            dispatcher.utter_message(text="This area has a rich history. Here's what I found about some historical landmarks:")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find information about historical sites in that specific location. Would you like to try with a different area?")
        return []

class ActionConservationEfforts(Action):
    def name(self):
        return "action_conservation_efforts"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        if location:
            prompt = f"How can I help conserve the environment in {location}"
        else:
            prompt = "What are some conservation efforts happening around the world?"
        response = call_gemini_api(prompt)
        if response:
            dispatcher.utter_message(text="Conservation efforts are crucial for our bioheritage. Here's what I found:")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find information about conservation efforts in that location. You can visit general websites like [Nature Conservancy](https://www.nature.org/en-us/) to learn more.")
        return []

class ActionFallback(Action):
    def name(self):
        return "action_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Sorry, I am not sure what you mean. Can you rephrase your question?")
        return []
