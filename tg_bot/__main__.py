import logging

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.utils.executor import start_polling

from .bot import ChatBot, GoState, ReportState
from .config import get_config

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s.%(msecs)03d] %(name)-32s %(levelname)8s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)

TIMEOUT = 120


def main() -> None:
    bot = ChatBot(get_config())
    storage = MemoryStorage()
    disp = Dispatcher(bot=bot, storage=storage)

    # /help command
    disp.register_message_handler(bot.help_handler, commands=["help"])

    # /cancel command
    disp.register_message_handler(bot.cancel_handler, commands=["cancel"], state="*")
    disp.register_message_handler(bot.cancel_handler, Text(equals="cancel", ignore_case=True), state="*")

    # /go command
    disp.register_message_handler(bot.go_handler, commands=["go"])
    disp.register_message_handler(bot.go_handler_process, state=GoState.start)
    disp.register_message_handler(
        bot.go_handler_face, state=GoState.face, content_types=(ContentType.PHOTO, ContentType.DOCUMENT)
    )
    disp.register_message_handler(bot.go_handler_rubbish, state=GoState.rubbish)

    # /report command
    disp.register_message_handler(bot.report_handler, commands=["problem"])
    disp.register_message_handler(bot.report_handler_geo_request, state=ReportState.start)
    disp.register_message_handler(
        bot.report_handler_geo_response, state=ReportState.geo, content_types=ContentType.LOCATION
    )
    disp.register_message_handler(
        bot.report_handler_photo, state=ReportState.photo, content_types=(ContentType.PHOTO, ContentType.DOCUMENT)
    )
    disp.register_message_handler(bot.report_handler_description, state=ReportState.description)

    # run
    start_polling(disp, reset_webhook=False, on_startup=bot.on_startup, on_shutdown=bot.on_shutdown, timeout=TIMEOUT)


if __name__ == "__main__":
    main()
