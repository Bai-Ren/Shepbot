import logging
from Channel import Channel

logger = logging.getLogger(f"shepbot.{__name__}")

class EventForBeans():
    def on_event(self, notification):
        match notification["payload"]["subscription"]["type"]:
            case "channel.online":
                self.channel.on_stream_start()
            case _:
                logger.error("Unknown subscription type found when processing bean event")

            
    def __init__(self, channel:Channel) -> None:
        self.channel = channel