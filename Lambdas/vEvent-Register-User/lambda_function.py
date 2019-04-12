import json
import boto3
import application_constants
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

USER_POOL_ID = "us-east-1_U6ll4eQrN"
APP_CLIENT_ID = "4ospbu2ujc4ua603mdveub19et"
DYNAMODB_TABLE_NAME = "vEvent-User-Attributes"


def lambda_handler(event, context):
    # TODO implement
    try:
        emailId = event['emailId']
        password = event['password']
        category = event['event']['category']
        genre = event['event']['genre']
        logger.info("Genre found is "+genre)
        # Validating category
        isValidCategory = application_constants.isValidCategory(category.lower())
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

    
        isRegestered = registerUser(emailId, password)
        isInserted = insertIntoDB(emailId, category, genre)
    except Exception as e:
        return {
        'body': "Exception"+str(e)
        }

    return {
        'body': "User Registered! Please verify your email address by clicking the link on verification email!"
    }
    
    
def registerUser(emailId, password):
    cognito_client = boto3.client('cognito-idp')
    # setPassword(emailId, password, cognito_client)
    response = cognito_client.sign_up(
        ClientId=APP_CLIENT_ID,
        Username=emailId,
        Password=password
    )
    logger.info("Response from Cognito: "+str(response))
    

    
def insertIntoDB(emailId, category, genre):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    response = table.put_item(
        Item={
            'emailId': emailId,
            'eventPreferences': {
                "category":category,
                "genre":genre
            },
        }
    )
    logger.info("Response from DB: "+str(response))
    
    
    
    
    
