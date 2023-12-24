import logging
import logging.config
import rel
import StartupQueue
from ChannelBairen import ChannelBairen
from ChannelShep import ChannelShep
from IrcMessageHandler import IrcMessageHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("shepbot")

def start_channel(channel, handler):
    logger.debug("starting channel")
    new_channel = channel()
    handler.register_channel(new_channel)

if __name__ == "__main__":
    #websocket.enableTrace(True)

    handler = IrcMessageHandler()

    StartupQueue.put(lambda: start_channel(ChannelBairen, handler))
    StartupQueue.put(lambda: start_channel(ChannelShep, handler))

    StartupQueue.pop()

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
