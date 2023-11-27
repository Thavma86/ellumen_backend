

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class extract_company_name_entity(Action):

    def name(self) -> Text:
        return "action_extract_company_name"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         food_entity = next(tracker.get_latest_entity_values('company_name'), None)
         if food_entity:
             dispatcher.utter_message(text=f"""
                                      My name is Fred. I am a new bot built for a 
                                      company called Ellumen.
                                      """)
         else: 
             dispatcher.utter_message(text="Unable to find chosen entity")

         return []
