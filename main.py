import logging
import logging.config
import websocket
import rel
import Config
import IrcMessageHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("shepbot")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    IrcMessageHandler.messageHandlerInit()
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv",
                              on_open=IrcMessageHandler.on_open,
                              on_message=IrcMessageHandler.on_message,
                              on_error=IrcMessageHandler.on_error,
                              on_close=IrcMessageHandler.on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
