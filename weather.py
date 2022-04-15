__version__ = (1, 0, 0)

""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under the Apache License, Version 2.0
"""
# scope: inline_content
# requires: requests
# meta developer: @morisummermods
import requests
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InputTextMessageContent,
)
from urllib.parse import quote_plus
from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
from ..inline import GeekInlineQuery, rand  # noqa
from .. import loader  # noqa
from .. import utils  # noqa
import logging
import re

logger = logging.getLogger(__name__)

n = '\n'


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


class WeatherMod(loader.Module):
    """Weather module"""
    id = 0
    strings = {
        "name": "Weather",
        "author": "morisummermods",
    }

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        try:
            channel = await self.client.get_entity(f"t.me/{self.strings['author']}")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error(f"Can't join {self.strings['author']}")
        try:
            post = (await client.get_messages(self.strings["author"], ids=[self.id]))[0]
            await post.react("❤️")
        except Exception:
            logger.error(f"Can't react to t.me/{self.strings['author']}")

    async def weathercmd(self, message: Message) -> None:
        """Current forecast for provided city"""
        city = utils.get_args_raw(message)
        req = requests.get(f"https://wttr.in/{city}?m&T")
        await utils.answer(message, f'<code>{n.join(req.text.splitlines()[:6])}</code>')

    async def new_inline_handler_(self, query: GeekInlineQuery) -> None:
        args = query.args
        req = requests.get(f"https://wttr.in/{quote_plus(args)}?format=j1").json()
        current = req["current_condition"]
        await query.answer(
            [
                InlineQueryResultArticle(
                    id=rand(20),
                    title=f"Forecast for {args}",
                    description="Current forecast",
                    thumb_url="https://i.ytimg.com/vi/IMLwb8DIksk/maxresdefault.jpg",
                    input_message_content=InputTextMessageContent(
                        "Hello world",
                        parse_mode="HTML",
                    ),
                )
            ],
            cache_time=0,
        )

    async def watcher(self, message: Message) -> None:
        pass
