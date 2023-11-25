import logging
import rel
import websocket
import Config
from IrcMessage import IrcMessage
from ChannelShep import ChannelShep
from ChannelBairen import ChannelBairen

IRC_WSS = "wss://irc-ws.chat.twitch.tv"

logger = logging.getLogger(f"shepbot.{__name__}")

class IrcMessageHandler:
    def on_ping(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug("PONG " + message.channel)
        ws.send("PONG " + message.channel)

    def on_privmsg(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug(f"Chat in Channel:{message.channel} Sender:{message.source} Message:{message.data}")
        if message.channel not in self.channel_dict:
            logger.error("Not from a channel we are listening to")
        else:
            self.channel_dict[message.channel].on_chat(ws, message)

    def on_notice(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if message.data == "Login authentication failed":
            logger.critical("Login failed")

    def on_001(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug("Authenticated successfully")

    def on_ignored_command(self, ws: websocket.WebSocketApp, message: IrcMessage):
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


    def on_message(self, ws: websocket.WebSocketApp, incoming_data: str):
        raw_messages = incoming_data.splitlines()
        for raw_message in raw_messages:
            irc_message = IrcMessage(raw_message)
            if irc_message.command in self.function_dict:
                self.function_dict[irc_message.command](self, ws, irc_message)
            else:
                logger.warning("Didn't recognize command: " + irc_message.command)

    def on_error(self, ws: websocket.WebSocketApp, error):
        logger.info(error)

    def on_close(self, ws: websocket.WebSocketApp, close_status_code, close_msg):
        logger.info("### closed ###")

    def on_open(self, ws: websocket.WebSocketApp):
        logger.info("Opened connection")
        with open(Config.oauth_file) as file:
            oauth = file.readline()
        with open(Config.nickname_file) as file:
            nick = file.readline()
        ws.send("CAP REQ twitch.tv/tags")
        ws.send(f"PASS oauth:{oauth}")
        ws.send(f"NICK {nick}")
        ws.send(f"JOIN #{Config.channel_name}")

    def __init__(self, channel_dict: dict={}):
        self.channel_dict = channel_dict
        ws = websocket.WebSocketApp(IRC_WSS,
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
