import json
import boto3
import logging
import application_constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DYNAMODB_TABLE_NAME = "vEvent-User-Attributes"

def lambda_handler(event, context):
    logger.info("Request Received: "+json.dumps(event))
    try:
        accessToken = event['headers']['AccessToken']
        category = event['body']['category']
        # Validating category
        isValidCategory = application_constants.isValidCategory(category.lower())
        genre = event['body']['genre']
        # Validating Genre
        isValidGenre = application_constants.isValidGenre(genre.lower())
        if isValidCategory is False:
            return {
            'body': "Invalid Category! Please choose a valid Category from "+str(application_constants.categoryList)
        }
        if isValidGenre is False:
            return {
            'body': "Invalid Genre! Please choose a valid Genre"
        }
        
        emailId = getEmailId(accessToken)
        isUpdated = updatePreferences(emailId,category,genre)
        if isUpdated is False:
            return {
            'body': "Updating to DynamoDb Failed! Please try again later"
        }

        return {
            'body': "User Preferences set!"
        }
    except Exception as e:
        return{
            'body': "ERROR: "+str(e)
        }
    
    

def updatePreferences(emailId,category,genre):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    details = {
        "category":category,
        "genre":genre
    }
    response = table.update_item(
        Key={
            'emailId': emailId
            },
        UpdateExpression= 'SET eventPreferences =  :details',
        ExpressionAttributeValues= {
          ':details': details
        }
    )

    logger.info("Response from DB: "+str(response))
    return True


def getEmailId(accessToken):
    cognito_client = boto3.client('cognito-idp')
    response = cognito_client.get_user(
        AccessToken=accessToken
    )
    logger.info("Response from Cognito: "+str(response))
    userAttributes = response['UserAttributes']
    for ele in userAttributes:
        if ele['Name'] == 'email':
            logger.info("Email Found from Cognito: "+str(ele['Value']))
            return ele['Value']
    return None