import requests # type: ignore[import-untyped]
from lib.utils.similarity_algo import compare_texts
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

bank_check_api_key: str = os.getenv('BANK_RESOLVE_API_KEY', '')
bank_check_api_url: str = os.getenv('BANK_RESOLVE_API', '')

def check_bank_details(name: str, account_number: str, bank_code: str, **kwargs) -> tuple[str, bool]:
    url = f"{bank_check_api_url}?account_number={account_number}&bank_code={bank_code}"

    # Header with bearer token
    headers = {
        "Authorization": f"Bearer {bank_check_api_key}",
        "Content-Type": "application/json",
    }

    try:
        # Make GET request with authentication
        response = requests.get(url, headers=headers)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            returned_name = response.json()["data"]["account_name"]
            if compare_texts(name, returned_name,0.4):  # Return JSON response
                return "Bank account is valid", True
            else:
                return "Bank account is valid but user's fullname is not verified with bank", False
        else:
            # Print error message if request failed
            print("Error:", response.status_code, response.text)
            return response.text, False
    except requests.exceptions.RequestException as e:
        # Print error message if there's an exception
        return str(e), False

