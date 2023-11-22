import websocket
import IrcMessage
from .Utilities import should_run

enabled = True
perms = ["mod"]

def run(ws: websocket.WebSocketApp, message: IrcMessage):
    if should_run(enabled, perms, message):
        ws.send("PRIVMSG #bairen0 :You are mod " + message.source)