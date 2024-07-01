# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Example bioheritage data (replace with a real data source)
bioheritage_data = {
    "new york": [
        "New York has a diverse range of urban wildlife.",
        "Central Park hosts many species of birds.",
        "Efforts are ongoing to maintain green spaces."
    ],
    "amazon rainforest": [
        "The Amazon Rainforest is home to a vast array of wildlife.",
        "It is known for its high biodiversity.",
        "Conservation efforts are crucial to preserve its ecosystem."
    ],
    "australia": [
        "Australia has unique flora and fauna.",
        "The Great Barrier Reef is a significant bioheritage site.",
        "Efforts are focused on protecting endangered species."
    ]
}

class ActionBioLocation(Action):

    def name(self) -> Text:
        return "action_bio_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        if location:
            location = location.lower()
            if location in bioheritage_data:
                bio_info = bioheritage_data[location]
                response = f"Here are three points about the bioheritage of {location.title()}:\n"
                for point in bio_info:
                    response += f"- {point}\n"
            else:
                response = f"Sorry, I don't have information about the bioheritage of {location.title()}."
        else:
            response = "Please provide a location to get bioheritage information."

        dispatcher.utter_message(text=response)
        return [SlotSet("location", None)]
