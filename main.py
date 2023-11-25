import logging
import logging.config
import rel
from ChannelBairen import ChannelBairen
from ChannelShep import ChannelShep
from IrcMessageHandler import IrcMessageHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("shepbot")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    bairen = ChannelBairen()
    shep = ChannelShep()

    handler = IrcMessageHandler()

    handler.register_channel(bairen)
    handler.register_channel(shep)
    
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
