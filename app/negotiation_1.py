import os
from pricing import Pricing
from sentiment import analyze_sentiment
from google.cloud import aiplatform
from google.oauth2 import service_account


from dotenv import load_dotenv

load_dotenv()

import requests
import os


class NegotiationBot:
    def __init__(self, product_name, base_price):
        self.product_name = product_name
        self.pricing = Pricing(base_price)
        self.conversation_history = []
        self.user_sentiment = None
        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )  

    def respond_to_offer(self, user_offer):
       
        self.user_sentiment = analyze_sentiment(user_offer)

       
        self.conversation_history.append({"role": "customer", "content": user_offer})

      
        prompt = self.construct_prompt(user_offer)
        bot_reply = self.get_gemini_response(prompt)

        self.conversation_history.append({"role": "supplier", "content": bot_reply})

        return bot_reply

    def get_gemini_response(self, prompt):
        url = "https://gemini-api.ai.google.com/v1/generateContent"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "model": "gemini-1.5-flash-latest",  
        }

        response = requests.post(url, headers=headers, json=payload)

   
        if response.status_code == 200:
            return response.json().get("content", "")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Sorry, I couldn't process your request."

    def construct_prompt(self, user_offer):
        counter_offer = self.pricing.get_counter_offer(user_offer, self.user_sentiment)
        system_prompt = f"You are a supplier negotiating the price of {self.product_name}. Your current offer is ${counter_offer:.2f}. The customer's offer was: {user_offer}. What is your response?"

        return system_prompt
