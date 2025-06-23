# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionRecommendByCuisine(Action):
    def name(self) -> Text:
        return "action_recommend_by_cuisine"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cuisine = tracker.get_slot("cuisine")

        recommendations = {
            "indonesia": "🇮🇩 Rekomendasi Indonesia: Nasi Gudeg, Rendang, Soto Ayam, Gado-gado",
            "chinese": "🇨🇳 Rekomendasi Chinese: Nasi Goreng Hongkong, Dimsum, Sweet & Sour, Capcay",
            "japanese": "🇯🇵 Rekomendasi Japanese: Sushi, Ramen, Teriyaki, Tempura",
            "western": "🍔 Rekomendasi Western: Burger, Pizza, Pasta, Steak",
            "korean": "🇰🇷 Rekomendasi Korean: Kimchi Fried Rice, Bulgogi, Bibimbap, Korean BBQ",
        }

        message = recommendations.get(
            cuisine.lower(),
            "Maaf, cuisine tersebut belum tersedia. Coba Indonesia, Chinese, Japanese, atau Western.",
        )
        dispatcher.utter_message(text=message)
        return []


class ActionRecommendByMood(Action):
    def name(self) -> Text:
        return "action_recommend_by_mood"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        mood = tracker.get_slot("mood")

        mood_foods = {
            "happy": "😊 Mood Happy: Ice Cream, Pizza, Burger, Chocolate Cake - makanan fun!",
            "sad": "😢 Mood Sad: Comfort food seperti Bubur Ayam, Sup Hangat, Mie Rebus",
            "stress": "😤 Mood Stress: Teh Hangat, Oatmeal, Salad Segar, Dark Chocolate",
            "tired": "😴 Mood Tired: Energizing food: Pisang, Kacang Almond, Smoothie Buah",
            "excited": "🎉 Mood Excited: Spicy food! Ayam Geprek, Seblak, Mie Pedas",
        }

        message = mood_foods.get(
            mood.lower(), "Mood apapun, makanan enak selalu bikin bahagia! 😋"
        )
        dispatcher.utter_message(text=message)
        return []


class ActionRecommendByPrice(Action):
    def name(self) -> Text:
        return "action_recommend_by_price"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        price = tracker.get_slot("price_range")

        price_recommendations = {
            "murah": "💰 Budget Friendly: Indomie Goreng (5K), Nasi Gudeg (15K), Bakso (10K), Es Teh (3K)",
            "sedang": "💸 Medium Range: Ayam Geprek (25K), Nasi Padang (30K), Mie Ayam (20K)",
            "mahal": "💎 Premium: Steak (150K), Sushi (200K), Fine Dining (300K+)",
            "affordable": "👍 Affordable: Nasi Pecel (12K), Soto (15K), Gado-gado (18K)",
        }

        if not price:
            text = tracker.latest_message.get("text", "").lower()
            if any(word in text for word in ["murah", "cheap"]):
                price = "murah"
            elif any(word in text for word in ["sedang", "medium"]):
                price = "sedang"
            elif any(word in text for word in ["mahal", "expensive"]):
                price = "mahal"

        message = price_recommendations.get(
            price.lower(), "Berapa budget yang kamu punya? Murah, sedang, atau mahal?"
        )
        dispatcher.utter_message(text=message)

        return [SlotSet("price_range", price)] if price else []
