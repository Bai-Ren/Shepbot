import logging
import boto3
import websocket
from DynamoTable import DynamoTable
from IrcMessage import IrcMessage
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa

logger = logging.getLogger(f"shepbot.{__name__}")

class ChannelBairen:
    def __init__(self) -> None:
        self.dyn_resource = boto3.resource('dynamodb')
        self.table_counters = DynamoTable(self.dyn_resource, "shepbot-counters-test")
        self.command_dict = {}
        self.command_dict["!test"] = CommandTest()
        self.command_dict["!modtest"] = CommandModTest()
        self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)

    def on_chat(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug("Bairen's channel has a message")
        firstWord = message.data.split(" ")[0] 
        if firstWord in self.command_dict:
            self.command_dict[firstWord].run(ws, message)
