import json
import boto3
from botocore.vendored import requests
import application_constants
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB_TABLE_NAME = "vEvent-User-Attributes"
API_ENDPOINT = "https://yv1x0ke9cl.execute-api.us-east-1.amazonaws.com/prod/events"
API_USER = "stitapplicant"
API_PASS = "zvaaDsZHLNLFdUVZ_3cQKns"

def lambda_handler(event, context):
    logger.info("Request Received: "+json.dumps(event))
    try:
        accessToken = event['headers']['AccessToken']
        emailId = getEmailId(accessToken)
        
        if emailId == None:
            return {
                'body': "ERROR: Email Id Not Found"
            }
        
        category, genre = getPreferences(emailId)
        if category == None or genre == None:
            return {
                'body': "User Prefence not set!"
            }
        genreId = application_constants.getGenreId(genre)
        body = sendRequestToApi(category,genreId)
        
        logger.info("response from api "+str(body))
        return {
            'body': body
        }
    except Exception as e:
        return{
            'body': "ERROR: "+str(e)
        }
    
    
# Hitting external API
def sendRequestToApi(category,genreId):
    response = requests.get(API_ENDPOINT+"?classificationName="+category+"&genreId="+genreId, auth=(API_USER, API_PASS))
    return response.json()
    
# Getting User Preferences - Category & Genre from DynamoDB
def getPreferences(emailId):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.get_item(
        Key={
            'emailId': emailId
        }
    )
    if 'Item' not in response:
        return None, None
    eventPreferences = response['Item']['eventPreferences']
    logger.info("Category found: "+str(eventPreferences['category'])+" Genre Found: "+str(eventPreferences['genre']))
    return eventPreferences['category'], eventPreferences['genre']
    
# Getting EmailId from Cognito using Access Token
def getEmailId(accessToken):
    cognito_client = boto3.client('cognito-idp')
    response = cognito_client.get_user(
        AccessToken=accessToken
    )
    userAttributes = response['UserAttributes']
    for ele in userAttributes:
        if ele['Name'] == 'email':
            logger.info("Email Id found "+str(ele['Value']))
            return ele['Value']
    logger.error("No Email Id Found")
    return None
    
    