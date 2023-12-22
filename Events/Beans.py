import logging
from Channel import Channel

logger = logging.getLogger(f"shepbot.{__name__}")

class EventForBeans():
    def add(self, increment):
        self.total += increment
        if self.total >= self.bean_threshold:
            total_beans = self.total // self.bean_threshold
            self.total -= total_beans * self.bean_threshold
            logger.info(f"Need to get {total_beans} beans with {self.total} leftover points")
            if total_beans == 1:
                self.channel.privmsg(f"ARF you owe us a bean")
            else:
                self.channel.privmsg(f"ARF you owe us {total_beans} beans")
        else:
            logger.info(f"No beans needed, but {self.total} accrued points")

    def on_event(self, notification):
        match notification["payload"]["subscription"]["type"]:
            case "channel.subscribe":
                if not notification["payload"]["event"]["is_gift"]: #should be counted in channel.subscription.gift
                    self.add(self.sub_value[notification["payload"]["event"]["tier"]])
            case "channel.subscription.gift":
                self.add(self.sub_value[notification["payload"]["event"]["tier"]] * notification["payload"]["event"]["total"])
            case "channel.subscription.message":
                self.add(self.sub_value[notification["payload"]["event"]["tier"]])
            case "channel.cheer":
                self.add(self.bit_value * self.sub_value[notification["payload"]["event"]["bits"]])
            case _:
                logger.error("Unknown subscription type found when processing bean event")

            
    def __init__(self, channel:Channel, bean_threshold = 5, tier1_sub_value = 1, tier2_sub_value = 2, tier3_sub_value = 5, bit_value = 0) -> None:
        self.channel = channel
        self.total = 0
        self.bean_threshold = bean_threshold
        self.sub_value = {'1000' : tier1_sub_value,
                          '2000' : tier2_sub_value,
                          '3000' : tier3_sub_value}
        self.bit_value = bit_value
