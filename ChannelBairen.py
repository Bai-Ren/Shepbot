import logging
from Channel import Channel
from Commands.Test import CommandTest
from Commands.ModTest import CommandModTest
from Commands.Sniffa import CommandSniffa
from Commands.CustomTextCommands import CommandCreateCustomTextCommand, CommandDeleteCustomTextCommand, CommandUpdateCustomTextCommand
import TwitchApi

logger = logging.getLogger(f"shepbot.{__name__}")

class ChannelBairen(Channel):
    channel_name = "bairen0"

    def __init__(self) -> None:
        super().__init__()
        self.command_dict["!test"] = CommandTest()
        self.command_dict["!modtest"] = CommandModTest()
        self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)
        self.command_dict["!createcommand"] = CommandCreateCustomTextCommand(self)
        self.command_dict["!updatecommand"] = CommandUpdateCustomTextCommand(self)
        self.command_dict["!deletecommand"] = CommandDeleteCustomTextCommand(self)

    def on_eventsub_welcome(self):
        self.test_api()

    def test_api(self):
        retries = 3
        while retries > 0:
            try:
                access_token = self.get_access_token()["access_token"]
                response = TwitchApi.get_user_info('bairen0', access_token)
                if response is not None:
                    logger.debug(response.text)
                    id = response.json()['data'][0]['id']
                    TwitchApi.get_channel_info(id, access_token)
                    TwitchApi.create_eventsub_subscription("channel.chat.notification", "1", {"broadcaster_user_id" : id, "user_id" : id}, self.eventsub.session_id, access_token)
            except TwitchApi.UnauthorizedException:
                retries -= 1
                self.refresh_access_token()
                continue
            except Exception as e:
                logger.error(f"Unknown exception:{e}")
            break