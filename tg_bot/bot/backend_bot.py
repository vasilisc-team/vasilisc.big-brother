import asyncio
import logging
from io import BytesIO
from typing import List, Optional, Tuple

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import MediaGroup, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions

from .base_bot import BaseBot
from ..nn_models import FaceFinder

face_finder = FaceFinder()


class GoState(StatesGroup):
    start = State()
    face = State()
    rubbish = State()
    # light = State()
    # pose = State()


log = logging.getLogger(__name__)


class GoBot(BaseBot):
    async def go_handler(self, message: Message) -> None:
        await GoState.start.set()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        markup.row("ЛИЦА", "МУСОР")
        await message.reply("Выберете действие", reply_markup=markup)

    async def go_handler_process(self, message: Message) -> None:
        if message.text == "ЛИЦА":
            await GoState.face.set()
        elif message.text == "МУСОР":
            await GoState.rubbish.set()
        # elif message.text == "СВЕТ":
        #     await GoState.light.set()
        # elif message.text == "ПОЗЫ":
        #     await GoState.pose.set()
        else:
            await message.reply("Пожалуйста, выберите нужное действие")
            return
        await message.reply("Отправьте фото для анализа", reply_markup=ReplyKeyboardRemove())

    async def go_handler_face(self, message: Message, state: FSMContext) -> None:
        ret = await self._get_img(message)
        if ret:
            buf, upload_status = ret
            result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: face_finder.process_raw(buf.getvalue())
            )
            upload_status.cancel()
            await self._process_result(result, message)
        await state.finish()

    async def go_handler_rubbish(self, message: Message, state: FSMContext) -> None:
        ret = await self._get_img(message)
        if ret:
            buf, upload_status = ret
            result = []
            await asyncio.get_event_loop().run_in_executor(None, lambda: face_finder.process_raw(buf.getvalue()))
            upload_status.cancel()
            await self._process_result(result, message)
        await state.finish()

    async def _get_img(self, message: Message) -> Optional[Tuple[BytesIO, asyncio.Task]]:
        if message.photo is None and message.document is None:
            await message.answer("Пожалуйста, отправьте фото для анализа")
            return None

        upload_status = GoBot._photo_upload_status()

        buf = BytesIO()
        if message.document:
            await message.document.download(buf)
        else:
            await message.photo[-1].download(buf)

        return buf, upload_status

    async def _process_result(self, result: List[bytes], message: Message) -> None:
        if not result:
            await message.answer("Лиц не найдено")
        elif len(result) == 1:
            await self.send_photo(message.chat.id, BytesIO(result[0]))
        else:
            media = MediaGroup()
            for img in result:
                media.attach_photo(BytesIO(img))
            await self.send_media_group(message.chat.id, media)

    @staticmethod
    def _photo_upload_status() -> asyncio.Task:
        async def internal() -> None:
            try:
                while True:
                    await ChatActions.upload_photo(5)
            except asyncio.CancelledError:
                pass

        return asyncio.create_task(internal())
