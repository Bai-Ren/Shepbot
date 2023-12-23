
import json
import logging
import boto3
import urllib
from botocore.exceptions import ClientError
import requests

__session = boto3.session.Session()
__client = __session.client(service_name='secretsmanager')
__client_secret = None

logger = logging.getLogger(f"shepbot.{__name__}")

TWITCH_OAUTH_TOKEN = "https://id.twitch.tv/oauth2/token"
REDIRECT_URI = "http://localhost"

def get_channel_secret(channel_name:str):
    return get_secret(f"shepbot/{channel_name}")

def get_client_secret():
    global __client_secret
    if __client_secret is not None:
        return __client_secret
    secret = get_secret('shepbot/client')
    __client_secret = secret
    return secret

def refresh_secret(secret_name:str):
    response = get_secret(secret_name)
    new_secret = refresh_secret_with_refresh_token(response['refresh_token'])
    update_secret(secret_name, json.dumps(new_secret))
    return new_secret

def refresh_channel_secret(channel_name:str):
    return refresh_secret(f"shepbot/{channel_name}")
    return {}

def create_token_from_code(code: str):
    secret = get_client_secret()
    response = requests.post(TWITCH_OAUTH_TOKEN,
                             params={'client_id' : secret['ClientId'],
                                     'client_secret' : secret['ClientSecret'],
                                     'code' : code,
                                     'grant_type' : 'authorization_code',
                                     'redirect_uri' : REDIRECT_URI})
    if response.status_code == 200:
        logger.debug(f"Successfully created token")
        return response.json()
    else:
        logger.error(f"Failed to create token: {response.text}")

def refresh_secret_with_refresh_token(refresh_token: str):
    secret = get_client_secret()
    response = requests.post(TWITCH_OAUTH_TOKEN,
                             params={'grant_type' : 'refresh_token',
                                     'refresh_token' : refresh_token,
                                     'client_id' : secret['ClientId'],
                                     'client_secret' : secret['ClientSecret']},
                             headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    if response.status_code == 200:
        logger.debug(f"Successfully refreshed token")
        return response.json()
    else:
        logger.error(f"Failed to refresh token: {response.text}")
    
def get_secret(secret_name:str):
    try:
        get_secret_value_response = __client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def update_secret(secret_name:str, secret:str):
    try:
        __client.update_secret(
            SecretId=secret_name,
            SecretString=secret
        )
    except ClientError as e:
        raise e

def create_secret(secret_name:str, secret:str, description:str):
    try:
        __client.create_secret(
            Name=secret_name,
            SecretString=secret,
            Description=description
        )
    except ClientError as e:
        raise e