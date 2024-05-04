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
import base64

load_dotenv()


class Crypto:
    def __init__(self):
        self.api_key = os.getenv("OKX_API_KEY")
        self.secret_key = os.getenv("OKX_SECRET_KEY")
        self.passphrase = os.getenv("OKX_PASSPHRASE")
        self.api_version = os.getenv("OKX_API_VERSION","v5")
        self.base_url = os.getenv("OKX_URL","https://www.okx.com")
    
    def set_headers(self, timestamp: str, signature: str) -> dict[str,str]:
        headers = {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
        }
        return headers
    
    def create_signature(self,timestamp, method, request_path, body) -> str:
        message = timestamp + method + request_path + (body if body else '')
        hmac_key = bytes(self.secret_key, encoding='utf-8')
        message = bytes(message, encoding='utf-8')

        sign = hmac.new(hmac_key, message, hashlib.sha256).digest()
        signature = base64.b64encode(sign).decode('utf-8')
        return signature

    def get_pair_price(self, base: str, target: str = 'usdt'):
        # API URL
        request_path = f"/api/{self.api_version}/market/ticker"
        
        # Parameters
        params = {
            'instId': f'{base.upper()}-{target.upper()}'
        }
        method = 'GET'
        body = ''

        # API key details
        timestamp = str(time.time())

        # Preparing the signature
        signature = self.create_signature(timestamp, method, request_path, body)

        # Headers
        headers = self.set_headers(timestamp, signature)

        # Making the request
        response = requests.get(self.base_url + request_path, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code}, Message: {response.text}"
        
    def get_server_time(self):
        timestamp = datetime.now(tz=timezone.utc).isoformat()[0:-9] + "Z"
        return timestamp
        
    def get_balance(self):
        # API URL
        method = 'GET'
        request_path = f'/api/{self.api_version}/account/balance?ccy=BTC'
        body = ''
        timestamp = self.get_server_time()
        signature = self.create_signature(timestamp, method, request_path, body)

        # Create the required headers
        headers = self.set_headers(timestamp, signature)
        # Make the request
        response = requests.get(self.base_url + request_path, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: {response.status_code}, Message: {response.text}"
        
    def check_deposits(self):
        method = 'GET'
        request_path = f'/api/{self.api_version}/account/deposit/history'
        body = ''
        timestamp = self.get_server_time()
        signature = self.create_signature(timestamp, method, request_path, body)

        headers = self.set_headers(timestamp, signature)
        response = requests.get(self.base_url + request_path, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, Message: {response.text}"

client: Crypto = Crypto()