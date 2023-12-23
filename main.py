import logging
import logging.config
import rel
from ChannelBairen import ChannelBairen
from ChannelShep import ChannelShep
from IrcMessageHandler import IrcMessageHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("shepbot")

def start_channel(channel, handler):
    new_channel = channel()
    handler.register_channel(new_channel)
    rel.dispatch()

if __name__ == "__main__":
    #websocket.enableTrace(True)
    rel.signal(2, rel.abort)  # Keyboard Interrupt

    handler = IrcMessageHandler()
    rel.dispatch()

    start_channel(ChannelBairen, handler)
    #start_channel(ChannelShep, handler)
    
    rel.dispatch()
