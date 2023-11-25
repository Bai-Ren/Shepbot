import json
import logging
from time import sleep
import rel
import websocket

EVENTSUB_WSS = "wss://eventsub.wss.twitch.tv/ws"

logger = logging.getLogger(f"shepbot.{__name__}")

class EventsubHandler:
    def on_welcome(self, ws: websocket.WebSocketApp, data: dict):
        logger.debug("Welcome message")
        if self.old_ws is not None:
            self.old_ws.close()
            self.old_ws = None
        self.active_ws = ws

        if "session" not in data["payload"] or "id" not in data["payload"]["session"]:
            logger.error("No session id provided for eventsubs")
        else:
            self.session_id = data["payload"]["session"]["id"]
            logger.info(f"Got session_id:{self.session_id}")
            self.channel.on_eventsub_welcome()
        
    def on_reconnect(self, ws: websocket.WebSocketApp, data: dict):
        logger.info("Reconnect message received")
        if "reconnect_url" in data["payload"]:
            self.old_ws = ws
            new_ws = websocket.WebSocketApp(data["payload"]["reconnect_url"],
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
            new_ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        else:
            logger.error("No reconnect url provided")

    def on_message(self, ws: websocket.WebSocketApp, incoming_data: str):
        raw_messages = incoming_data.splitlines()
        for raw_message in raw_messages:
            try:
                json_message = json.loads(raw_message)
            except json.JSONDecodeError:
                logger.error(f"Error decoding json {raw_message}")
                return
            if "metadata" in json_message and "payload" in json_message and "message_type" in json_message["metadata"]:
                match json_message["metadata"]["message_type"]:
                    case "session_welcome":
                        self.on_welcome(ws, json_message)
                    case "session_reconnect":
                        self.on_reconnect(ws, json_message)
                    case "session_keepalive":
                        pass
                    case "notification":
                        logger.debug(f"Received notification:{json_message}")
                    case _:
                        message_type = json_message["metadata"]["message_type"]
                        logger.warning(f"Unrecognized message_type:{message_type}")
            else:
                logger.error(f"Message was valid json, but {json_message}")


    def on_error(self, ws: websocket.WebSocketApp, error):
        logger.info(error)

    def on_close(self, ws: websocket.WebSocketApp, close_status_code, close_msg):
        logger.info("### closed ###")

    def on_open(self, ws: websocket.WebSocketApp):
        logger.info("opened connection")

    def __init__(self, channel):
        self.old_ws = None
        self.active_ws = None
        self.session_id = ""
        self.channel = channel
        ws = websocket.WebSocketApp(EVENTSUB_WSS,
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
