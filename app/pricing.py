class Pricing:
    def __init__(self, base_price):
        self.base_price = base_price

    def get_counter_offer(self, user_offer, user_sentiment):
        try:
            # Try converting user_offer to a float
            user_offer = float(user_offer)
        except ValueError:
            # If the conversion fails, you can decide what to do here
            print("Invalid offer. Please enter a numeric value.")
            return self.base_price

        # Continue with the pricing logic after conversion
        if user_offer >= self.base_price * 0.9:
            return user_offer
        else:
            return self.base_price * 0.95
