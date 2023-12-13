import logging
from Channel import Channel
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa
from Events.Beans import EventForBeans
import TwitchApi

logger = logging.getLogger(f"shepbot.{__name__}")

class ChannelShep(Channel):
    channel_name = "wv_shep"
    access_token_filename = "..\\wvshepread.txt"

    def __init__(self) -> None:
        super().__init__()
        #self.command_dict["!test"] = CommandTest()
        #self.command_dict["!modtest"] = CommandModTest()
        self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)

    def on_eventsub_welcome(self):
        self.setup_beans()

    def setup_beans(self):
        response = TwitchApi.get_user_info('wv_shep', self.user_access_token)
        if response is not None:
            beans = EventForBeans(self) # One bean counter for all three eventsub types
            id = response.json()['data'][0]['id']
            TwitchApi.get_channel_info(id, self.user_access_token)
            response = TwitchApi.create_eventsub_subscription("channel.subscribe", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
            self.event_dict[response.json()['data'][0]['id']] = beans
            response = TwitchApi.create_eventsub_subscription("channel.subscription.message", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
            self.event_dict[response.json()['data'][0]['id']] = beans
            response = TwitchApi.create_eventsub_subscription("channel.subscription.gift", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, self.user_access_token)
            self.event_dict[response.json()['data'][0]['id']] = beans
            