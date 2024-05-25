from app.models.user import Users
import pyotp
import qrcode
import io
from base64 import b64encode

def generate_qr(user: Users):
    totp = pyotp.TOTP(user.totp_secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name='PathwayToGold')
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    img_b64 = b64encode(buf.read()).decode('utf-8')
    
    return img_b64

def verify_totp_code(user: Users, code: str):
    try:
        totp = pyotp.TOTP(user.totp_secret)
        return ("Verified", totp.verify(code)) if totp.verify(code) else ("Invalid Code", False)
    except Exception as e:
        return (str(e), False)