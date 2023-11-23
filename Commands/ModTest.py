from cgitb import enable
import websocket
import IrcMessage
from .Command import Command 

class CommandModTest(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            ws.send("PRIVMSG #bairen0 :You are mod " + message.source)

    def __init__(self, enabled=True, perms=["mod"]) -> None:
        self.enabled = enabled
        self.perms = perms