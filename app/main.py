# app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from negotiation_1 import NegotiationBot
from textblob import TextBlob

load_dotenv()

app = FastAPI(title="Negotiation Chatbot API")


negotiations = {}


class NegotiationResponse(BaseModel):
    message: str
    bot_message: str = None  
    user_message: str = None  

class UserOffer(BaseModel):
    negotiation_id: str
    user_offer: float
    user_message: str 


class NegotiationResponse(BaseModel):
    message: str


class InitiateNegotiationRequest(BaseModel):
    negotiation_id: str
    product_name: str
    base_price: float


def analyze_sentiment(user_message: str) -> str:

    analysis = TextBlob(user_message)

    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"


class NegotiationBot:
    def __init__(self, product_name, base_price):
        self.product_name = product_name
        self.base_price = base_price


        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    def initiate_negotiation(self):
        prompt = f"""
        You are a negotiation bot initiating a conversation about selling {self.product_name}.
        The base price is ${self.base_price}.
        Introduce yourself and invite the user to make an offer.
        Respond in a friendly, professional manner.
        """
        return self.get_gemini_response(prompt)

    def respond_to_offer(self, user_offer, sentiment):
        prompt = f"""
        You are a negotiation bot selling {self.product_name}.
        The base price is ${self.base_price}.
        The user has offered ${user_offer} and their sentiment is {sentiment}.
        Provide a reasonable counteroffer or accept the offer if it's close enough to the base price.
        Respond in a friendly, professional manner considering the user's sentiment.
        """
        return self.get_gemini_response(prompt)


    def get_gemini_response(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


@app.post("/initiate", response_model=NegotiationResponse)
def initiate_negotiation(request: InitiateNegotiationRequest):
    if request.negotiation_id in negotiations:
        raise HTTPException(status_code=400, detail="Negotiation ID already exists.")

    bot = NegotiationBot(request.product_name, request.base_price)
    initial_message = bot.initiate_negotiation()
    negotiations[request.negotiation_id] = bot

    return NegotiationResponse(message=initial_message)


@app.post("/offer", response_model=NegotiationResponse)
def make_offer(offer: UserOffer):
    bot = negotiations.get(offer.negotiation_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Negotiation ID not found.")

 
    sentiment = analyze_sentiment(offer.user_message)
    bot_reply = bot.respond_to_offer(
        offer.user_offer, sentiment
    )  

    return NegotiationResponse(message=bot_reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
