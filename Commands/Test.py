import websocket
import IrcMessage
from .Utilities import should_run

enabled = True
perms = []

def run(ws: websocket.WebSocketApp, message: IrcMessage):
    if should_run(enabled, perms, message):
        ws.send("PRIVMSG #bairen0 :I see you " + message.source)