import json
import requests

def lambda_handler(event, context):
    try:
        url = "https://www.gold-api.com/get?symbol=XAU&base=USD"
        response = requests.get(url, timeout=5)
        data = response.json()

        gold_price = data.get("price")
        if gold_price:
            message = f"The current gold price is ${float(gold_price):,.2f} per ounce."
        else:
            message = "Sorry, I couldn't get the latest gold price."

    except Exception as e:
        print("Error:", e)
        message = "There was an error getting the gold price. Please try again later."

    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": event["sessionState"]["intent"]["name"],
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }
