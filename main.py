import logging
import logging.config
import rel
from IrcMessageHandler import messageHandlerInit
from EventsubHandler import EventsubHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("shepbot")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    eventsub = EventsubHandler()
    messageHandlerInit()

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
