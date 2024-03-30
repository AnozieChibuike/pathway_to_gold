from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = None

if not SECRET_KEY:
    raise NotImplementedError(
        "SECRET KEY missing in config, set one now with <FLASK_SECRET>"
    )


def generate_token(email: str):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str, user: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        return {"status": "success"}, 200, True
    except jwt.ExpiredSignatureError:
        return {"status": "error", "reason": "code expired"}, 400, False
    except jwt.InvalidTokenError:
        return {"status": "error", "reason": "Invalid token"}, 400, False
    except:
        return {"status": "error", "reason": "Unable to decode the token"}, 400, False
