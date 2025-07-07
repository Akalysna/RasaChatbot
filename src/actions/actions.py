from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTellOrder(Action):
    def name(self) -> Text:
        return "action_tell_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pizza = tracker.get_slot("pizza")

        if pizza is None:
            dispatcher.utter_message(text="Je ne connais pas la pizza {pizza}. Voulez-vous voir notre menu ?")
            
        else:
            dispatcher.utter_message(
                response="utter_place_order",
                pizza=pizza
            )
        
        return []   

class ActionTellPizzaPrice(Action):
    def name(self) -> Text:
        return "action_tell_pizza_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the pizza entity from the tracker
        pizza = tracker.get_slot("pizza")
        
        # Define pizza prices
        pizza_prices = {
            "trois fromages": 10,
            "montagnarde": 12,
            "margherita": 9,
            "regina": 11,
            "quatre saisons": 12,
            "chèvre-miel": 11,
            "calzone": 13,
            "hawaïenne": 12,
            "végétarienne": 11,
            "bbq poulet": 12
        }
        
        # Get the price or use a default message
        price = pizza_prices.get(pizza.lower() if pizza else "", None)
        
        if price is not None:
            dispatcher.utter_message(
                response="utter_ask_price",
                pizza=pizza,
                price=price
            )
        else:
            dispatcher.utter_message(text=f"Je ne connais pas le prix de la pizza {pizza}.")
        
        return []
