from cgitb import enable
import websocket
import IrcMessage
from .Command import Command 

class CommandModTest(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            ws.send(f"PRIVMSG #{message.channel} :You are a mod {message.source}")

    def __init__(self, enabled=True, perms=["mod"]) -> None:
        self.enabled = enabled
        self.perms = perms