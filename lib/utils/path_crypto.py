import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timezone
import hmac
import hashlib
import time
from urllib.parse import urlencode
import pytz

load_dotenv()

class Crypto:
    def __init__(self):
        self.api_key = os.getenv("OKX_API_KEY")
        self.secret_key = os.getenv("OKX_SECRET_KEY")
        self.passphrase = os.getenv("OKX_PASSPHRASE")
        self.api_version = os.getenv("OKX_API_VERSION",)
        self.base_url = os.getenv("OKX_URL",)

    def get_pair_price(self, base: str, target: str):
        # API URL
        url = f"{self.base_url}/{self.api_version}/market/ticker"
        
        # Parameters
        params = {
            'instId': f'{base.upper()}-{target.upper()}'
        }

        # API key details
        timestamp = str(time.time())

        # Preparing the signature
        message = timestamp + 'GET' + f'/api/v{self.api_version}/market/ticker?' + urlencode(params)
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

        # Headers
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }

        # Making the request
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code}, Message: {response.text}"
        
    def get_balance(self):
        # API URL
        url = f"{self.base_url}/{self.api_version}/account/balance?ccy=BTC"
    
        # API key details
        # timestamp = datetime.now(pytz.timezone('Europe/Warsaw')).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # timestamp = str(datetime.now(pytz.timezone('Europe/Warsaw')).isoformat())[0:-9] + "Z"
        timestamp = datetime.now(tz=timezone.utc).isoformat()[0:-9] + "Z"

        # Preparing the signature
        message = timestamp + 'GET' + f'/api/{self.api_version}/account/balance?ccy=BTC'
        print(message)
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        print(signature)

        # Headers
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }

        # Making the request
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code}, Message: {response.text}"