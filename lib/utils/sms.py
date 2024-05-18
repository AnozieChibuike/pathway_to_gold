from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
service = os.getenv('TWILIO_SERVICE')
if not account_sid and auth_token and service:
    raise KeyError('Missing keys')

client = Client(account_sid, auth_token)

def send_code_to_sms(phone: str) -> tuple[str, bool]:
    try:
        verification = client.verify.v2.services(service).verifications.create(to=phone, channel='sms') # Phone must be a +country_codr
        print(verification.__dict__)
        return 'Otp Sent to' + phone,True
    except Exception as e:
        return "Somethng went wrong", False
    
def verify_code(code: str, phone: str) -> tuple[str, bool]:
    try:
        verification_check = client.verify \
                            .v2 \
                            .services(service) \
                            .verification_checks \
                            .create(to=phone, code=code)
        if not verification_check.__dict__['valid']:
            return "Incorrect otp", False
        return 'Verified', True
    except Exception as e:
        print(e)
        return 'Something went wrong or already verified or expired', False