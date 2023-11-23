import websocket
import IrcMessage

class Command:
    enabled = False
    perms = []
    def check_perms(self, message: IrcMessage) -> bool:
        # broadcaster always allowed
        if message.channel == message.source: # Is broadcaster
            return True 
        # perms = []
        # allow all    
        elif not self.perms: 
            return True  
        # perms = ["mod"]
        # allow mods            
        elif self.perms[0] == "mod":
            return "mod" in message.tags and message.tags["mod"] == "1"
        # perms = ["user1", "user2", "user3"]
        # list of allowed users
        else:
            return message.source in self.perms 

    def should_run(self, message: IrcMessage) -> bool:
        return self.enabled and self.check_perms(message)
    
    def run(self, ws: websocket.WebSocketApp, message: IrcMessage):
        pass

    