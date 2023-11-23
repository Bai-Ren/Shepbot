import logging
import websocket
import Config
from IrcMessage import IrcMessage
from ChannelShep import ChannelShep

logger = logging.getLogger(f"shepbot.{__name__}")

channel_dict = {}

def on_ping(ws: websocket.WebSocketApp, message: IrcMessage):
    logger.debug("PONG " + message.channel)
    ws.send("PONG " + message.channel)

def on_privmsg(ws: websocket.WebSocketApp, message: IrcMessage):
    logger.debug(f"Chat in Channel:{message.channel} Sender:{message.source} Message:{message.data}")
    if message.channel not in channel_dict:
        logger.error("Not from a channel we are listening to")
    else:
        channel_dict[message.channel].on_chat(ws, message)

def on_notice(ws: websocket.WebSocketApp, message: IrcMessage):
    if message.data == "Login authentication failed":
        logger.critical("Login failed")

def on_001(ws: websocket.WebSocketApp, message: IrcMessage):
    logger.debug("Authenticated successfully")

def on_ignored_command(ws: websocket.WebSocketApp, message: IrcMessage):
    logger.debug(f"Recieved {message.command} silently ignoring")

function_dict = {"PING" : on_ping,
                 "PRIVMSG" : on_privmsg,
                 "NOTICE" : on_notice,
                 "001" : on_001,
                 "002" : on_ignored_command,
                 "003" : on_ignored_command,
                 "004" : on_ignored_command,
                 "375" : on_ignored_command,
                 "372" : on_ignored_command,
                 "376" : on_ignored_command,
                 "JOIN" : on_ignored_command,
                 "353" : on_ignored_command,
                 "366" : on_ignored_command}


def on_message(ws: websocket.WebSocketApp, incoming_data: str):
    raw_messages = incoming_data.splitlines()
    for raw_message in raw_messages:
        logger.debug(raw_message)
        irc_message = IrcMessage(raw_message)
        if irc_message.command in function_dict:
            function_dict[irc_message.command](ws, irc_message)
        else:
            logger.warning("Didn't recognize command: " + irc_message.command)

def on_error(ws: websocket.WebSocketApp, error):
    logger.info(error)

def on_close(ws: websocket.WebSocketApp, close_status_code, close_msg):
    logger.info("### closed ###")

def on_open(ws: websocket.WebSocketApp):
    logger.info("Opened connection")
    with open(Config.oauth_file) as file:
        oauth = file.readline()
    with open(Config.nickname_file) as file:
        nick = file.readline()
    ws.send("CAP REQ twitch.tv/tags")
    ws.send(f"PASS oauth:{oauth}")
    ws.send(f"NICK {nick}")
    ws.send(f"JOIN #{Config.channel_name}")

def messageHandlerInit():
    channel_dict["bairen0"] = ChannelShep()
