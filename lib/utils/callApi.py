import requests
import json
import hmac
import hashlib
import time
from urllib.parse import urlencode

api_key = 'e88f7971-3d1f-4799-9fa5-f004fafeb39c'
secret_key = '63726540F675B8753FA4A77AD3A848D0'
passphrase = 'Sweetest2005@'

def get_btc_price():
    # API URL
    url = "https://www.okx.com/api/v5/market/ticker"
    
    # Parameters
    params = {
        'instId': 'BTC-USDT'
    }

    # API key details
    timestamp = str(time.time())

    # Preparing the signature
    message = timestamp + 'GET' + '/api/v5/market/ticker?' + urlencode(params)
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    # Headers
    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

    # Making the request
    response = requests.get(url, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}, Message: {response.text}"

# Usage
btc_price = get_btc_price()
print(f"Current BTC Price: {btc_price}")
