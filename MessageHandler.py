from IrcMessage import IrcMessage
import websocket

def on_ping(ws, message):
    print("PONG " + message.channel)
    ws.send("PONG " + message.channel)

def on_privmsg(ws, message):
    print(message.source + ":" + message.data)
    words = message.data.split(" ")
    if words[0] == "!test":
        ws.send("PRIVMSG #bairen0 :I see you " + message.source)

def on_message(ws, rawmessage):
    print(rawmessage)
    messages = rawmessage.splitlines()
    for message in messages:
        ircMessage = IrcMessage(message)
        if ircMessage.command == "PING":
            on_ping(ws, ircMessage)
        elif ircMessage.command == "PRIVMSG":
            on_privmsg(ws, ircMessage)

        