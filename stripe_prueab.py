import stripe

stripe.api_key = "sk_test_51QeuSYEK6Flwy0UPt3HlLUtqY3Wd97E8STkZG3WyHUch5wJVRknAgzqmHss58jb3ODdHjCRXZRxBy2JWr8LgO45M00I6E3gWZQ"

"""def create_payment_intent(amount, currency="eur"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,  # En céntimos
            currency=currency,
            payment_method_types=["card"],
        )
        return intent.client_secret
    except stripe.error.StripeError as e:
        return f"Error: {e.user_message}"

if __name__ == "__main__":
    amount = 1000  # 10.00 dólares en céntimos
    currency = "eur"
    client_secret = create_payment_intent(amount, currency)
    print(f"Client secret: {client_secret}")
"""

steel_ball_run = stripe.Product.create(
  name="Steel Ball Run",
  description="La carrera más larga hecha por la humanidad",
)

steel_ball_run_price = stripe.Price.create(
  unit_amount=1200,
  currency="eur",
  product=steel_ball_run['id'],
)

# Save these identifiers
print(f"Success! Here is your steel ball run product id: {steel_ball_run.id}")
print(f"Success! Here is your steel ball run price id: {steel_ball_run_price.id}")