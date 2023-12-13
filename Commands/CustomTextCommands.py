import logging
import websocket
from Channel import Channel
import IrcMessage
from .Command import Command 

logger = logging.getLogger(f"shepbot.{__name__}")

class CommandCustomTextCommand(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            ws.send(f"PRIVMSG #{message.channel} :{self.message}")
            
    def __init__(self, message:str, enabled=True, perms=[]) -> None:
        self.message = message
        self.enabled = enabled
        self.perms = perms

class CommandCreateCustomTextCommand(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            if len(message.data.split()) < 3:
                logger.info("CreateCustomTextCommand - Incorrect syntax")
                ws.send(f"PRIVMSG #{message.channel} :Incorrect syntax")
                return
            command = message.data.split()[1]
            text = " ".join(message.data.split()[2:])
            if command in self.channel.command_dict:
                logger.info("CreateCustomTextCommand - Command already exists")
                ws.send(f"PRIVMSG #{message.channel} :That command already exists! Update it instead")
                return
            self.channel.command_dict[command] = CommandCustomTextCommand(text)
            ws.send(f"PRIVMSG #{message.channel} :Command created")
            
    def __init__(self, channel:Channel, enabled=True, perms=["mod"]) -> None:
        self.channel = channel
        self.enabled = enabled
        self.perms = perms

class CommandUpdateCustomTextCommand(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            if len(message.data.split()) < 3:
                logger.info("UpdateCustomTextCommand - Incorrect syntax")
                ws.send(f"PRIVMSG #{message.channel} :Incorrect syntax")
                return
            command = message.data.split()[1]
            text = " ".join(message.data.split()[2:])
            if not command in self.channel.command_dict:
                logger.info("UpdateCustomTextCommand - Command does not exist")
                ws.send(f"PRIVMSG #{message.channel} :That command does not exist! Create it instead")
                return
            if not isinstance(self.channel.command_dict[command], CommandCustomTextCommand):
                logger.info(f"UpdateCustomTextCommand - Command is not a custom text command, it's type is {type(self.channel.command_dict[command])}")
                ws.send(f"PRIVMSG #{message.channel} :You can only update a custom text command!")
                return
            self.channel.command_dict[command].message = text
            ws.send(f"PRIVMSG #{message.channel} :Command updated")
            
    def __init__(self, channel:Channel, enabled=True, perms=["mod"]) -> None:
        self.channel = channel
        self.enabled = enabled
        self.perms = perms

class CommandDeleteCustomTextCommand(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            if len(message.data.split()) != 2:
                logger.info("DeleteCustomTextCommand - Incorrect syntax")
                ws.send(f"PRIVMSG #{message.channel} :Incorrect syntax")
                return
            command = message.data.split()[1]
            if not command in self.channel.command_dict:
                logger.info("DeleteCustomTextCommand - Command does not exist")
                ws.send(f"PRIVMSG #{message.channel} :That command does not exist!")
                return
            if not isinstance(self.channel.command_dict[command], CommandCustomTextCommand):
                logger.info("DeleteCustomTextCommand - Command is not a custom text command")
                ws.send(f"PRIVMSG #{message.channel} :You can only delete a custom text command!")
                return
            del self.channel.command_dict[command]
            ws.send(f"PRIVMSG #{message.channel} :Command Deleted")
            
    def __init__(self, channel:Channel, enabled=True, perms=["mod"]) -> None:
        self.channel = channel
        self.enabled = enabled
        self.perms = perms