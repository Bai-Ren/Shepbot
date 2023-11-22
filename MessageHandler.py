import websocket
from IrcMessage import IrcMessage
from Logger import Log
import Commands.Test
import Commands.ModTest

command_dict = {"!test" : Commands.Test,
                "!modtest" : Commands.ModTest}

def on_ping(ws: websocket.WebSocketApp, message: IrcMessage):
    Log("PONG " + message.channel)
    ws.send("PONG " + message.channel)

def on_privmsg(ws: websocket.WebSocketApp, message: IrcMessage):
    Log(message.source + " " + message.data + " " + str(message.tags))
    firstWord = message.data.split(" ")[0] 
    if firstWord in command_dict:
        command_dict[firstWord].run(ws, message)

function_dict = {"PING" : on_ping,
                 "PRIVMSG" : on_privmsg}

def on_message(ws: websocket.WebSocketApp, incomingData: str):
    rawMessages = incomingData.splitlines()
    for rawMessage in rawMessages:
        #Log(rawMessage)
        message = IrcMessage(rawMessage)
        if message.command in function_dict:
            function_dict[message.command](ws, message)
        else:
            Log("Didn't recognize command: " + message.command)
