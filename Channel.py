import logging
import boto3
import websocket
from DynamoTable import DynamoTable
from IrcMessage import IrcMessage
from EventsubHandler import EventsubHandler

logger = logging.getLogger(f"shepbot.{__name__}")

class Channel:
    channel_name = "Base"
    access_token_filename = None

    def __init__(self) -> None:
        self.dyn_resource = boto3.resource('dynamodb')
        self.table_counters = DynamoTable(self.dyn_resource, "shepbot-counters-test")
        self.command_dict = {}
        self.event_dict = {}
        self.ws = None
        self.eventsub = EventsubHandler(self)
        if self.access_token_filename is not None:
            with open(self.access_token_filename) as file:
                self.user_access_token = file.readline()
        else:
            self.user_access_token = None

    def on_chat(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug(f"{self.channel_name} channel has a message")
        firstWord = message.data.split(" ")[0] 
        if firstWord in self.command_dict:
            self.command_dict[firstWord].run(ws, message)

    def on_event(self, notification):
        subscription_id = notification["payload"]["subscription"]["id"]
        if subscription_id in self.event_dict:
            self.event_dict[subscription_id].on_event(notification)

    def on_eventsub_welcome(self):
        pass

    def privmsg(self, message:str):
        if self.ws is None:
            logger.error(f"Websocket not initialized for privmsg on channel: {self.channel_name}")
        else:
            self.ws.send(f"PRIVMSG #{self.channel_name} :{message}")

        

