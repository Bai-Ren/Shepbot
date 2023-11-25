import websocket
from DynamoTable import DynamoTable
import IrcMessage
from .Command import Command 

class CommandSniffa(Command):
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        if self.should_run(message):
            total = self.table.increment_counter("sniffas", message.channel, 1)
            ws.send(f"PRIVMSG #{message.channel} :Total sniffas: {total}")
            
    def __init__(self, table: DynamoTable,enabled=True, perms=[]) -> None:
        self.table = table
        self.enabled = enabled
        self.perms = perms