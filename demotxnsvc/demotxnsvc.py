import json

def lambda_handler(event, context):
    """
    Lambda function that returns a "Hello World" message.
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps('Hello from Lambda transaction service mock!')
    }