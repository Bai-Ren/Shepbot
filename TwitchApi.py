

import json
import logging
import requests
import Config
from SecretsManager import refresh_secret, get_secret

TWITCH_API_CHANNELS = "https://api.twitch.tv/helix/channels"
TWITCH_API_USERS = "https://api.twitch.tv/helix/users"
TWITCH_API_EVENTSUB = "https://api.twitch.tv/helix/eventsub/subscriptions"

APP_ACCESS_TOKEN = ""
CLIENT_ID = "85u5coaa5b5k1chrm4me4ao0mofat1"

logger = logging.getLogger(f"shepbot.{__name__}")

class UnauthorizedException(Exception):
    pass

def validate_and_refresh_channel_secret(channel_name:str):
    return validate_and_refresh_secret(f"shepbot/{channel_name}")

def validate_and_refresh_secret(secret_name:str):
    retries = 3
    while retries > 0:
        try:
            access_token = get_secret(secret_name)["access_token"]
            get_user_info('pb_shepbot', access_token)
            return access_token
        except UnauthorizedException:
            retries -= 1
            refresh_secret(secret_name)
            continue
        except Exception as e:
            retries -= 1
            logger.error(f"Unknown exception:{e}")
    if retries == 0:
        logger.critical(f"Failed to refresh and validate secret:{secret_name}")
        return None

def generate_headers(access_token: str = None) -> dict:
    if access_token is None:
        access_token = APP_ACCESS_TOKEN
    return {'Authorization' : f'Bearer {access_token}', 'Client-Id' : CLIENT_ID}

def get_channel_info(channel: str, access_token: str):
    response = requests.get(TWITCH_API_CHANNELS,
                            params={'broadcaster_id' : channel},
                            headers=generate_headers(access_token))
    if response.status_code == 200:
        logger.debug(f"Get channel info success: {response.text}")
        return response
    elif response.status_code == 401:
        raise UnauthorizedException()
    else:
        logger.error(f"{response.status_code} code while getting channel info: {response.text}")
        return None

def get_user_info(channel: str, access_token: str):
    response = requests.get(TWITCH_API_USERS,
                            params={'login' : channel},
                            headers=generate_headers(access_token))
    if response.status_code == 200:
        logger.debug(f"Get user info success: {response.text}")
        return response
    elif response.status_code == 401:
        raise UnauthorizedException()
    else:
        logger.error(f"{response.status_code} code while getting user info: {response.text}")
        return None
    
def create_eventsub_subscription(type: str, version: str, condition: object, session_id: str, access_token: str):
    transport = {'method' : 'websocket', 'session_id' : session_id}
    logger.debug(f"type : {type}, version : {version}, condition : {condition}, transport : {transport}")
    response = requests.post(TWITCH_API_EVENTSUB,
                             json={'type' : type, 'version' : version, 'condition' : condition, 'transport' : transport},
                             headers=generate_headers(access_token))
    if response.status_code == 202:
        logger.debug(f"Create eventsub success: {response.text}")
        return response
    elif response.status_code == 401:
        raise UnauthorizedException()
    else:
        logger.error(f"{response.status_code} code while creating eventsub: {response.text}")
        return None
