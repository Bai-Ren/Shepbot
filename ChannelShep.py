import logging
from Channel import Channel
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa
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
        self.test_api()

    def test_api(self):
        response = TwitchApi.get_user_info('wv_shep', self.user_access_token)
        if response is not None:
            id = response.json()['data'][0]['id']
            TwitchApi.get_channel_info(id, self.user_access_token)
            TwitchApi.create_eventsub_subscription("channel.chat.notification", "1", {"broadcaster_user_id" : id, "user_id" : id}, self.eventsub.session_id, self.user_access_token)
            