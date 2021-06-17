# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.handles.EsHandle import EsHandle
import json


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []


class ActionGetProducts(Action):

    def name(self) -> Text:
        return "action_list_products"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            handle = EsHandle()
            products = handle.get_products()
            
            products = "\n".join([x[0] for x in products])
            
            dispatcher.utter_message(response="utter_list_products", text=products)

            return []

class ActionGetProductInfoByName(Action):

    def name(self) -> Text:
        return "action_product_info"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            handle = EsHandle()
            product_name = tracker.get_slot("product")
            print(product_name)
            product_info = json.dumps(handle.get_product_by_name(product_name))
            
            dispatcher.utter_message(response="utter_list_products", text=product_info)

            return []
