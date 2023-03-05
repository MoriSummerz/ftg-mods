__version__ = (1, 0, 0)

"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# meta developer: @morisummermods
# meta banner:

import asyncio
import logging

import requests
from telethon.tl.types import Message

from .. import loader, utils  # noqa
from ..inline.types import InlineCall  # noqa

logger = logging.getLogger(__name__)


@loader.tds
class ChatGPT(loader.Module):
    """ChatGPT AI API interaction"""

    strings = {
        "name": "ChatGPT",
        "no_args": "<b>🚫 No arguments provided</b>",
        "question": "<b>👤 Question:</b> {question}\n",
        "answer": "<b>🤖 Answer:</b> {answer}",
        "loading": "<code>Loading...</code>",
        "no_api_key": "<b>🚫 No API key provided</b>\n"
                      "<i>ℹ️ Get it from official OpenAI website and add it to config</i>",
    }

    strings_ru = {
        "no_args": "<b>🚫 Не указаны аргументы</b>",
        "question": "<b>👤 Вопрос:</b> {question}\n",
        "answer": "<b>🤖 Ответ:</b> {answer}",
        "loading": "<code>Загрузка...</code>",
        "no_api_key": "<b>🚫 Не указан API ключ</b>\n"
                      "<i>ℹ️ Получите его на официальном сайте OpenAI и добавьте в конфиг</i>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                "API key from OpenAI",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )

    async def _make_request(self, method: str, url: str, headers: dict, data: dict) -> dict:
        resp = await utils.run_sync(
            requests.request,
            method,
            url,
            headers=headers,
            json=data,
        )
        return resp.json()

    async def _get_chat_completion(self, prompt: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config["api_key"]}'
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        resp = await self._make_request(
            method="POST",
            url="https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=data,
        )
        return resp["choices"][0]["message"]['content']

    @loader.command(
        ru_doc="<вопрос> - Спросить вопрос",
    )
    async def gpt(self, message: Message):
        """<question> - Ask a question"""
        if self.config["api_key"] == "":
            return await utils.answer(message, self.strings("no_api_key"))

        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("no_args"))

        await utils.answer(
            message,
            "\n".join(
                [
                    self.strings("question").format(question=args),
                    self.strings("answer").format(answer=self.strings("loading")),
                ]
            ),
        )
        answer = await self._get_chat_completion(args)
        await utils.answer(
            message,
            "\n".join(
                [
                    self.strings("question").format(question=args),
                    self.strings("answer").format(answer=answer),
                ]
            ),
        )
