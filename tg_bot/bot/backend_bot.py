import asyncio
import json
import logging
from base64 import b64encode
from dataclasses import dataclass, field
from io import BytesIO
from typing import Dict, List, Optional, Tuple, TypedDict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    MediaGroup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
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


class ReportState(StatesGroup):
    start = State()
    geo = State()
    photo = State()
    description = State()


class ReportDataJson(TypedDict):
    latitude: float
    longitude: float
    image: str
    description: str


@dataclass
class ReportData:
    type: str
    latitude: float = field(default=0)
    longitude: float = field(default=0)
    image: str = field(default="")
    description: str = field(default="")

    def to_dict(self) -> ReportDataJson:
        return ReportDataJson(
            latitude=self.latitude,
            longitude=self.longitude,
            image=self.image,
            description=self.description,
        )


log = logging.getLogger(__name__)


class GoBot(BaseBot):
    FILE_STORAGE = "report_data.json"

    def __init__(self, *args, **kwargs):  # type: ignore
        self.report_data: Dict[str, List[ReportDataJson]] = dict(rubbish=[], lights=[])
        super().__init__(*args, **kwargs)

    async def on_startup(self, disp: Dispatcher) -> None:
        # TODO: this real need?
        await super().on_startup(disp)

    async def on_shutdown(self, disp: Dispatcher) -> None:
        with open(self.FILE_STORAGE, "w", encoding="utf-8") as output_fd:
            json.dump(self.report_data, output_fd, ensure_ascii=False)
        log.debug("Report data saved successfully")
        await super().on_shutdown(disp)

    async def go_handler(self, message: Message) -> None:
        await GoState.start.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        keyboard.row("ЛИЦА", "МУСОР")
        await message.reply("Выберете действие", reply_markup=keyboard)

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

    async def report_handler(self, message: Message) -> None:
        await ReportState.start.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
        keyboard.row("МУСОР", "ОСВЕЩЕНИЕ")
        await message.reply("Пожалуйста, выберите категорию", reply_markup=keyboard)

    async def report_handler_geo_request(self, message: Message, state: FSMContext) -> None:
        if message.text == "МУСОР":
            report_type = "rubbish"
        elif message.text == "ОСВЕЩЕНИЕ":
            report_type = "lights"
        else:
            await message.reply("Пожалуйста, выберите категорию")
            return
        report_data = ReportData(report_type)

        await ReportState.geo.set()
        keyboard = ReplyKeyboardMarkup()
        button = KeyboardButton("Поделится геокоординатами", request_location=True)
        keyboard.add(button)
        await message.reply("Поделитесь вашей геолокацией", reply_markup=keyboard)

        async with state.proxy() as data:
            data[message.chat.id] = report_data

    async def report_handler_geo_response(self, message: Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            report_data: ReportData = data[message.chat.id]

            report_data.latitude = message.location.latitude
            report_data.longitude = message.location.longitude

            await message.answer("Пожалуйста, отправьте фото", reply_markup=ReplyKeyboardRemove())
            await ReportState.photo.set()

    async def report_handler_photo(self, message: Message, state: FSMContext) -> None:
        ret = await self._get_img(message)
        if ret:
            buf, upload_status = ret
            upload_status.cancel()
            async with state.proxy() as data:
                report_data: ReportData = data[message.chat.id]
                report_data.image = b64encode(buf.getbuffer()).decode("utf-8")
                if message.caption:
                    report_data.description = message.caption
                    await message.reply("Благодарим за помощь в улучшении качества оказания услуг")
                    self.report_data[report_data.type].append(report_data.to_dict())
                    del data[message.chat.id]
                    await state.finish()
                else:
                    await ReportState.description.set()
                    await message.reply("Кратко опишите проблему")

    async def report_handler_description(self, message: Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            report_data: ReportData = data[message.chat.id]
            report_data.description = message.text
            await message.reply("Благодарим за помощь в улучшении качества оказания услуг")
            self.report_data[report_data.type].append(report_data.to_dict())
            del data[message.chat.id]
            await state.finish()

    async def _get_img(self, message: Message) -> Optional[Tuple[BytesIO, asyncio.Task]]:
        if message.photo is None and message.document is None:
            await message.answer("Пожалуйста, отправьте фото")
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
