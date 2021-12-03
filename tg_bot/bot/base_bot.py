import asyncio
import logging
from typing import Any, Callable, List

import aiogram.utils.markdown as md
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode, ReplyKeyboardRemove

from ..config import BotConfig

log = logging.getLogger(__name__)


class BaseBot(Bot):
    def __init__(self, config: BotConfig):
        super().__init__(token=config.telegram_token)
        # self.loop = asyncio.get_event_loop()

    async def cancel_handler(self, message: Message, state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return

        log.info("Cancel state %r", current_state)
        await state.finish()
        await message.reply("Cancelled.", reply_markup=ReplyKeyboardRemove())

    async def help_handler(self, message: Message) -> None:
        await message.answer(
            md.text(
                md.bold("Help"),
                md.escape_md("/go - Начать работу!"),
                md.escape_md("/help - Справка"),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    async def _remove_messages(self, chat_id: int, remove_message: List[int]) -> None:
        await asyncio.gather(*(self.delete_message(chat_id, message_id) for message_id in remove_message))

    async def _run_async(self, funcs: List[Callable], args_list: List[List[Any]]) -> None:
        await asyncio.gather(*(func(*args) for func, args in zip(funcs, args_list)))
