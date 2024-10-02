# app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Negotiation Chatbot API")

# In-memory store for negotiations (use a database for production)
negotiations = {}


class NegotiationResponse(BaseModel):
    message: str
    bot_message: str = None  # For responses specifically from the bot
    user_message: str = None  # For user messages


class UserOffer(BaseModel):
    negotiation_id: str
    user_offer: float


class NegotiationResponse(BaseModel):
    message: str


class NegotiationBot:
    def __init__(self, product_name, base_price):
        self.product_name = product_name
        self.base_price = base_price

        # Configure the generative AI model
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

    def respond_to_offer(self, user_offer):
        prompt = f"""
        You are a negotiation bot selling {self.product_name}.
        The base price is ${self.base_price}.
        The user has offered ${user_offer}.
        Provide a reasonable counteroffer or accept the offer if it's close enough to the base price.
        Respond in a friendly, professional manner.
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

    bot_reply = bot.respond_to_offer(offer.user_offer)
    return NegotiationResponse(message=bot_reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
