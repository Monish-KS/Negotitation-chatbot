import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class NegotiationBot:
    def __init__(self, product_name, base_price):
        self.product_name = product_name
        self.base_price = base_price

        # Configure the generative AI model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

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


# Create a NegotiationBot instance
product_name = "Headphones"
base_price = 100.0
negotiation_bot = NegotiationBot(product_name, base_price)

# Negotiation loop
while True:
    # Get user offer
    user_offer = float(input("Enter your offer (or 'quit' to end): "))

    if user_offer == "quit":
        print("Negotiation ended.")
        break

    # Get bot response based on user offer
    bot_reply = negotiation_bot.respond_to_offer(user_offer)
    print(f"Bot: {bot_reply}")

    # Handle user acceptance/rejection
    user_response = input("Do you accept this offer? (yes/no): ").lower()
    if user_response == "yes":
        print("Negotiation successful!")
        break
    elif user_response == "no":
        print("Negotiation continues...")
    else:
        print("Invalid input. Please answer 'yes' or 'no'.")
