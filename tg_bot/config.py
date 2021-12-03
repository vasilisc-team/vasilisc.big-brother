import os
from dataclasses import dataclass


@dataclass
class BotConfig:
    telegram_token: str


def get_config() -> BotConfig:
    return BotConfig(telegram_token=os.environ["TG_MSG_TOKEN"])
