import logging
import queue

logger = logging.getLogger("shepbot")
__setup_queue = []

def put(function):
    global __setup_queue
    __setup_queue.append(function)

def pop():
    global __setup_queue
    if len(__setup_queue) > 0:
        __setup_queue[0]()
        __setup_queue.pop(0)
    else:
        logger.info("Setup queue empty; setup complete!")