from app.negotiation import NegotiationBot

product_name = "Headphones"
base_price = 100.0
negotiation_bot = NegotiationBot(product_name, base_price)

# Simulate user offer
user_offer = 85.0

# Negotiation loop
while True:
    bot_reply = negotiation_bot.respond_to_offer(user_offer)
    print(f"Bot: {bot_reply}")

    # Simulate user input
    user_response = input("You: ")

    if user_response.lower() == "accept":
        print("Negotiation successful!")
        break
    elif user_response.lower() == "reject":
        print("Negotiation failed.")
        break
