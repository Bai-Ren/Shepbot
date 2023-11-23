import websocket
from DynamoTable import DynamoTable
import IrcMessage
from .Command import Command 

class CommandSniffa(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            total = self.table.increment_counter("Testcounter", 1)
            ws.send(f"PRIVMSG #bairen0 :Total {total}")
            
    def __init__(self, table: DynamoTable,enabled=True, perms=[]) -> None:
        self.table = table
        self.enabled = enabled
        self.perms = perms