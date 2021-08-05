# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json

from actions.handles.EsHandle import es_handle

class ActionGetProductFact(Action):

    def name(self) -> Text:
        return "action_product_fact"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product_name = tracker.get_slot("product")
            fact = tracker.get_slot("fact")
            possible_products = es_handle.get_product_fact(product_name, fact)
            text_to_user = []
            if(possible_products == []):
                text_to_user = "Infelizmente não possuímos esse produto em estoque."
            else:
                # just top 3 products
                if(len(possible_products) > 3):
                    possible_products = possible_products[:3]

                # format output to user
                for prod in possible_products:
                    msg = []
                    for key in prod:
                        msg.append(f"{key}: {prod[key]}")
                    msg = " - ".join(msg)
                    text_to_user.append(msg)

                text_to_user = "\n".join(text_to_user)

            dispatcher.utter_message(response="utter_list_products", text=text_to_user)
            slots_to_reset = ["product", "fact"]
            return [SlotSet(slot) for slot in slots_to_reset]

class ActionGetProductPrice(Action):

    def name(self) -> Text:
        return "action_product_price"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product_name = tracker.get_slot("product")
            possible_products = es_handle.get_product_price(product_name)

            if(possible_products == []):
                msg = "Infelizmente não possuímos esse produto em estoque."
            else:
                # just top 3 products
                if(len(possible_products) > 3):
                    possible_products = possible_products[:3]
                msg = [" - ".join(prod.values()) for prod in possible_products]
                msg = "\n".join(msg)
            
            dispatcher.utter_message(response="utter_list_products", text=msg)
            slots_to_reset = ["product"]
            return [SlotSet(slot) for slot in slots_to_reset]

class ActionCheckStock(Action):

    def name(self) -> Text:
        return "action_check_stock"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product_name = tracker.get_slot("product")
            possible_products = es_handle.get_product_price(product_name)

            if(possible_products == []):
                msg = "Infelizmente não possuímos esse produto em estoque."
            else:
                # just top 3 products
                if(len(possible_products) > 3):
                    possible_products = possible_products[:2]
                prods = [" - ".join(prod.values()) for prod in possible_products]
                prods = "\n".join(prods)
                msg = f"Nós temos esse(s) produto(s) em estoque:\n{prods}\nAcesse o link para mais detalhes!"
            
            dispatcher.utter_message(response="utter_list_products", text=msg)
            slots_to_reset = ["product"]
            return [SlotSet(slot) for slot in slots_to_reset]

class ActionGetProductQA(Action):

    def name(self) -> Text:
        return "action_product_qa"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product_name = tracker.get_slot("product")
            question = tracker.get_slot("question")
            answer = es_handle.get_product_qa(product_name, question)
            text_to_user = []

            if(answer == []):
                text_to_user = ["Infelizmente não encontrei esse produto"]
            elif(answer["qa"] == []):
                text_to_user.append("Infelizmente não consegui encontrar resposta para sua pergunta")
            else:
                # format output to user
                msg = [f"Veja o que encontrei sobre o produto {answer['Produto']}:"]
                qa = answer["qa"][0]
                msg.append(f"Pergunta: {qa['question']}")
                msg.append(f"Resposta: {qa['answer']}")
                msg = "\n".join(msg)
                text_to_user.append(msg)
                text_to_user.append('\n')

            if(answer != []):
                text_to_user.append(f"Cheque a página do produto para mais detalhes: {answer.get('url')}")

            text_to_user = "\n".join(text_to_user)
            dispatcher.utter_message(response="utter_list_products", text=text_to_user)
            slots_to_reset = ["product", "question", "fact"]
            return [SlotSet(slot) for slot in slots_to_reset]