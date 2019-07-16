from notification.console import Console
from notification.provider import Noop
from notification.spark import Spark


class NotificationFactory:
    @staticmethod
    def instance(config):
        if config["provider"] == "spark":
            return Spark(config["spark"])
        elif config["provider"] == "console":
            return Console(config["console"])
        return Noop()
