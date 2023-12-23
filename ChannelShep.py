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

    def __init__(self) -> None:
        super().__init__()
        #self.command_dict["!test"] = CommandTest()
        #self.command_dict["!modtest"] = CommandModTest()
        self.command_dict["!sniffa"] = CommandSniffa(self.table_counters)

    def on_eventsub_welcome(self):
        self.setup_beans()

    def setup_beans(self):
        retries = 3
        while retries > 0:
            try:
                access_token = self.get_access_token()["access_token"]
                response = TwitchApi.get_user_info('wv_shep', access_token)
                if response is not None:
                    logger.debug(response.text)
                    beans = EventForBeans(self) # One bean counter for all three eventsub types
                    id = response.json()['data'][0]['id']
                    response = TwitchApi.create_eventsub_subscription("channel.subscribe", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = beans
                    response = TwitchApi.create_eventsub_subscription("channel.subscription.message", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = beans
                    response = TwitchApi.create_eventsub_subscription("channel.subscription.gift", "1", {"broadcaster_user_id" : id}, self.eventsub.session_id, access_token)
                    self.event_dict[response.json()['data'][0]['id']] = beans
            except TwitchApi.UnauthorizedException:
                retries -= 1
                self.refresh_access_token()
                continue
            except Exception as e:
                logger.error(f"Unknown exception:{e}")
            break