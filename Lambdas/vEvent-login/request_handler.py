import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

APP_CLIENT_ID = "4ospbu2ujc4ua603mdveub19et"

def lambda_handler(event, context):
    logger.info("Request Received: "+json.dumps(event))
    isAuthenticated = False
    res = {}
    try:
        body = event['body']
        bodyJson = json.loads(body)
        emailId = bodyJson['emailId']
        password = bodyJson['password']
        cognito_client = boto3.client('cognito-idp')
        
    
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': emailId,
                'PASSWORD': password
            },
            ClientId=APP_CLIENT_ID,
        )
        logger.info("Response from Cognito : "+json.dumps(response))
        # Taking out JWT token & AccessToken
        idToken = response['AuthenticationResult']['IdToken']
        accessToken = response['AuthenticationResult']['AccessToken']
        isAuthenticated=True
    except Exception as e:
        logger.error("Error : "+str(e))
        res = {
            'isAuthenticated' : isAuthenticated,
            'message' : e.args
        }
    
    if isAuthenticated is True:
        res = {
            'isAuthenticated':isAuthenticated,
            'idToken' : idToken,
            'accessToken':accessToken
        }
        return {
            'statusCode': 200,
            'body': json.dumps(res)
        }
    
    
    return {
        'statusCode': 403,
        'body': json.dumps(res)
    }
