
import IrcMessage

def check_perms(perms: list, message: IrcMessage) -> bool:
    if message.channel[1:] == message.source: # Is broadcaster
        return True
    for perm in perms:
        if perm == "mod":
            if not "mod" in message.tags or not message.tags["mod"] == "1":
                return False
    return True

def should_run(enabled: bool, perms: list, message: IrcMessage) -> bool:
    return enabled and check_perms(perms, message)