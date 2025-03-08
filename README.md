# Coin Price Alert
Monitor cryptocurrency prices and send email alerts when the price reaches a defined threshold.

It fetches real-time prices from the CoinGecko API and sends alerts to you gmail account.

# Usage

1. Install Dependencies
pip install requests python-dotenv

2. Generate a Gmail App Password
- Enable 2-step verification, go to the Security page.
- Under Signing in to Google, find App passwords and click on it.
You may be asked to sign in again for security purposes.

In the App passwords section:
- Select Mail as the app.
- Select Other custom name as the device.
- Enter a name for the app password (e.g., Coin Price Alert).
- Click Generate.
- Google will display a 16-character app password. Copy this password.

3. Configure the .env
Email configuration
EMAIL_FROM=email@example.com
EMAIL_PASSWORD=password
EMAIL_TO=recipient@example.com

Token thresholds (format: THRESHOLD_<TOKEN_NAME>=<PRICE>)
THRESHOLD_BITCOIN=70000
THRESHOLD_ETHEREUM=2000
THRESHOLD_SOLANA=100
THRESHOLD_DOGECOIN=0.5

4. With Docker
Build the image
docker build -t coin-price-alert .

Run the image
docker run -d --name coin-price-alert --env-file .env coin-price-alert

5. Locally
python pricealert.py
