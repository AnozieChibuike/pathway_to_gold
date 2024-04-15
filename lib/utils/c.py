# import requests
# import json
# import hmac
# import hashlib
# import time
# from urllib.parse import urlencode
# import os
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("OKX_API_KEY")
# secret_key = os.getenv("OKX_SECRET_KEY")
# passphrase = os.getenv("OKX_PASSPHRASE")
# api_version = os.getenv("OKX_API_VERSION",)
# base_url = os.getenv("OKX_URL",)

# def get_pair_price(coin1: str, coin2: str):
#     # API URL
#     url = f"{base_url}/api/v{api_version}/market/ticker"
    
#     # Parameters
#     params = {
#         'instId': f'{coin1}-{coin2}'
#     }

#     # API key details
#     timestamp = str(time.time())

#     # Preparing the signature
#     message = timestamp + 'GET' + f'/api/v{api_version}/market/ticker?' + urlencode(params)
#     signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

#     # Headers
#     headers = {
#         'OK-ACCESS-KEY': api_key,
#         'OK-ACCESS-SIGN': signature,
#         'OK-ACCESS-TIMESTAMP': timestamp,
#         'OK-ACCESS-PASSPHRASE': passphrase,
#         'Content-Type': 'application/json'
#     }

#     # Making the request
#     response = requests.get(url, headers=headers, params=params)
#     print(response)
#     if response.status_code == 200:
#         data = response.json()
#         return data['data'][0]['last']
#     else:
#         return f"Error: {response.status_code}, Message: {response.text}"

# # Usage
# btc_price = get_pair_price('BTC', 'USDT')
# print(f"Current BTC Price: {btc_price}")

from path_crypto import Crypto

client = Crypto()

print(client.get_balance())
