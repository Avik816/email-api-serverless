import json
import boto3
import logging

# Configuring logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initializing SES client
ses_client = boto3.client('ses')

def send_email(event, context):
    try:
        body = json.loads(event['body'])
        receiver_email = body['receiver_email']
        subject = body['subject']
        body_text = body['body_text']

        # Validating input
        if not receiver_email or not subject or not body_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "receiver_email, subject, and body_text are required."})
            }

        # Sending email
        response = ses_client.send_email(
            Source='bhekhrajpatwa100@gmail.com',
            Destination={
                'ToAddresses': [
                    receiver_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                    }
                }
            }
        )

        # Returning success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
