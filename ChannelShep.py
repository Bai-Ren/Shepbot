import logging
import websocket
from Channel import Channel
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa
from Events.Beans import EventForBeans
from IrcMessage import IrcMessage
import TwitchApi

logger = logging.getLogger(f"shepbot.{__name__}")

class ChannelShep(Channel):
    channel_name = "wv_shep"

    def __init__(self) -> None:
        super().__init__()
        #self.command_dict["!test"] = CommandTest()
        #self.command_dict["!modtest"] = CommandModTest()
        self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)

    def on_eventsub_welcome(self):
        self.setup_beans()
        self.setup_online()

    def on_stream_start(self):
        self.beans.total = 0

    def setup_beans(self):
        retries = 3
        while retries > 0:
            try:
                access_token = self.get_access_token()["access_token"]
                response = TwitchApi.get_user_info(self.channel_name, access_token)
                if response is not None:
                    self.beans = EventForBeans(self) # One bean counter for all three eventsub types
                    id = response.json()['data'][0]['id']
                    response = TwitchApi.create_eventsub_subscription("channel.subscribe", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = self.beans
                    response = TwitchApi.create_eventsub_subscription("channel.subscription.message", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = self.beans
                    response = TwitchApi.create_eventsub_subscription("channel.subscription.gift", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = self.beans
            except TwitchApi.UnauthorizedException:
                retries -= 1
                self.refresh_access_token()
                continue
            except Exception as e:
                logger.error(f"Unknown exception:{e}")
            break
    
    def setup_online(self):
        retries = 3
        while retries > 0:
            try:
                access_token = self.get_access_token()["access_token"]
                response = TwitchApi.get_user_info(self.channel_name, access_token)
                if response is not None:
                    id = response.json()['data'][0]['id']
                    response = TwitchApi.create_eventsub_subscription("channel.online", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = self.beans
            except TwitchApi.UnauthorizedException:
                retries -= 1
                self.refresh_access_token()
                continue
            except Exception as e:
                logger.error(f"Unknown exception:{e}")
            break

    def on_chat(self, ws: websocket.WebSocketApp, message: IrcMessage):
        logger.debug(f"{self.channel_name} channel has a message")
        firstWord = message.data.split(" ")[0] 
        if firstWord in self.command_dict:
            self.command_dict[firstWord].run(ws, message)
        else:
            words = message.data.lower().replace(".","").split(" ")
            if "stinky" in words or "stimky" in words:
                self.privmsg(f"@{message.source} 😐")
