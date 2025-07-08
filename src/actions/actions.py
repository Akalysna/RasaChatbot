from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re

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
        if not pizza:
            dispatcher.utter_message(text="Je n'ai pas compris de quelle pizza vous parlez.")
            dispatcher.utter_message(text="Voici notre menu :")
            dispatcher.utter_message(response="utter_ask_menu")
            return []
            
        # Normaliser le nom de la pizza en minuscules et sans accents
        pizza_lower = pizza.lower()
        
        # Définir les prix des pizzas avec leurs variantes d'orthographe
        pizza_patterns = {
            r'trois\s*fromages?|3\s*fromages?': 10,
            r'montagnarde': 12,
            r'margherita': 9,
            r'r[eé]gina': 11,
            r'quatre\s*saisons?|4\s*saisons?': 12,
            r'ch[èe]vres?[\s-]miels?': 11,  # Gère chèvre-miel, chevre miel, etc.
            r'calzone': 13,
            r'hawa[ïi]enne': 12,
            r'v[ée]g[ée]tarienne': 11,
            r'bbq\s*poulet|barbecue\s*poulet|poulet\s*bbq|poulet\s*barbecue': 12
        }
        
        # Chercher une correspondance avec les motifs regex
        price = None
        matched_pizza = None
        
        for pattern, pizza_price in pizza_patterns.items():
            if re.fullmatch(pattern, pizza_lower, re.IGNORECASE):
                price = pizza_price
                # Récupérer le nom canonique de la pizza
                if 'trois' in pattern or '3' in pattern:
                    matched_pizza = 'trois fromages'
                elif 'quatre' in pattern or '4' in pattern:
                    matched_pizza = 'quatre saisons'
                elif 'chèvre' in pattern or 'chevre' in pattern:
                    matched_pizza = 'chèvre-miel'
                elif 'bbq' in pattern or 'barbecue' in pattern:
                    matched_pizza = 'BBQ poulet'
                else:
                    matched_pizza = next((p for p in [
                        'montagnarde', 'margherita', 'regina', 
                        'calzone', 'hawaïenne', 'végétarienne'
                    ] if re.search(p, pattern, re.IGNORECASE)), pizza)
                break
        
        if price is not None:
            dispatcher.utter_message(
                response="utter_ask_price",
                pizza=matched_pizza,
                price=price
            )
        else:
            dispatcher.utter_message(text=f"Je ne connais pas le prix de la pizza {pizza}.")
            dispatcher.utter_message(text="Voici notre menu :")
            dispatcher.utter_message(response="utter_ask_menu")
        
        return []
