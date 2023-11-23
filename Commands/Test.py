import websocket
import IrcMessage
from .Command import Command 

class CommandTest(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            ws.send("PRIVMSG #bairen0 :I see you " + message.source)
            
    def __init__(self, enabled=True, perms=[]) -> None:
        self.enabled = enabled
        self.perms = perms