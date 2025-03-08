import os
import time
import requests
import smtplib
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

EMAIL_FROM = os.getenv("EMAIL_FROM")  
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  
EMAIL_TO = os.getenv("EMAIL_TO")  

def load_token_thresholds():
    thresholds = {}
    for key, value in os.environ.items():
        if key.startswith("THRESHOLD_"):
            token = key.replace("THRESHOLD_", "").lower()
            thresholds[token] = float(value)
    return thresholds

# Fetch cryptocurrency prices
def get_crypto_prices(crypto_ids):
    params = {
        "ids": ",".join(crypto_ids),
        "vs_currencies": "usd",
    }
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching prices: {e}")
        return None

def send_email_alert(crypto, price):
    subject = f"{crypto.capitalize()} Price Alert!"
    body = f"The price of {crypto} has reached ${price}."
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, message)
        logging.info(f"Email alert sent for {crypto} at ${price}.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def monitor_prices():
    thresholds = load_token_thresholds()
    if not thresholds:
        logging.error("No token thresholds found in .env file.")
        return

    while True:
        prices = get_crypto_prices(thresholds.keys())
        if prices:
            for crypto, threshold in thresholds.items():
                current_price = prices[crypto]["usd"]
                if current_price >= threshold:
                    logging.info(f"Alert! {crypto.capitalize()} price is now ${current_price}.")
                    send_email_alert(crypto, current_price)
        time.sleep(60)  

if __name__ == "__main__":
    logging.info("Starting Crypto Price Alert Tool...")
    monitor_prices()

