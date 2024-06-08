import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
region_name = os.getenv('AWS_REGION', 'eu-west-1')
pinpoint_APP_ID = os.getenv('AWS_PINPOINT_APP_ID')

# Create an SNS client with specified region and credentials
client = boto3.client(
    'sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

def send_code_to_sms(phone_number: str, message: str, message_type: str = 'TRANSACTIONAL'):
    try:
        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': message_type.capitalize()
                }
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'Message sent successfully', 200
        else:
            return f"Failed to send message: {response.get('StatusMessage','Error')}", response['HTTPStatusCode']
    except Exception  as e:
        return str(e), 500
    
def verify_code(phone: str, code: str):
    ...