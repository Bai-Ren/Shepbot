import logging
import boto3
import websocket
from DynamoTable import DynamoTable
from IrcMessage import IrcMessage
from EventsubHandler import EventsubHandler
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa
import TwitchApi

logger = logging.getLogger(f"shepbot.{__name__}")

class ChannelShep:
    def __init__(self, eventsub: EventsubHandler) -> None:
        self.dyn_resource = boto3.resource('dynamodb')
        self.table_counters = DynamoTable(self.dyn_resource, "shepbot-counters-test")
        self.command_dict = {}
        #self.command_dict["!test"] = CommandTest()
        #self.command_dict["!modtest"] = CommandModTest()
        #self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)
        self.eventsub = eventsub
        with open("..\\wvshepread.txt") as file:
            self.user_access_token = file.readline()

    def on_chat(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug("Shep's channel has a message")
        firstWord = message.data.split(" ")[0] 
        if firstWord in self.command_dict:
            self.command_dict[firstWord].run(ws, message)

    def test_api(self):
        response = TwitchApi.get_user_info('wv_shep', self.user_access_token)
        if response is not None:
            id = response.json()['data'][0]['id']
            TwitchApi.get_channel_info(id, self.user_access_token)
            TwitchApi.create_eventsub_subscription("channel.subscribe", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
            TwitchApi.create_eventsub_subscription("channel.subscription.gift", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
            TwitchApi.create_eventsub_subscription("channel.subscription.message", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
        