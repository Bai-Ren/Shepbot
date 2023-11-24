

import json
import logging
import requests
import Config

TWITCH_API_CHANNELS = "https://api.twitch.tv/helix/channels"
TWITCH_API_USERS = "https://api.twitch.tv/helix/users"
TWITCH_API_EVENTSUB = "https://api.twitch.tv/helix/eventsub/subscriptions"

APP_ACCESS_TOKEN = ""
CLIENT_ID = "msgdavcnktpyq1rur1ft1s16bz5crr"

logger = logging.getLogger(f"shepbot.{__name__}")

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
    else:
        logger.error(f"{response.status_code} code while creating eventsub: {response.text}")
        return None
