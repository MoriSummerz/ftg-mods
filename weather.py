__version__ = (1, 1, 0)

"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: inline_content
# requires: requests
# meta developer: @morisummermods
# meta banner: https://i.imgur.com/JR6VqYF.png
# meta pic: https://i.imgur.com/iwoskSb.png

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
rus = "ёйцукенгшщзхъфывапролджэячсмитьбю"

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


class WeatherMod(loader.Module):
    """Weather module"""
    id = 17
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

    async def weathercitycmd(self, message: Message) -> None:
        """Set default city for forecast"""
        if args := utils.get_args_raw(message):
            self.db.set(self.strings['name'], 'city', args)
        await utils.answer(message, f"<b>🏙 Your current city: "
                                    f"<code>{self.db.get(self.strings['name'], 'city', '🚫 Not specified')}</code></b>")
        return

    async def weathercmd(self, message: Message) -> None:
        """Current forecast for provided city"""
        city = utils.get_args_raw(message)
        if not city:
            city = self.db.get(self.strings['name'], 'city', "")
        lang = 'ru' if city and city[0].lower() in rus else 'en'
        req = requests.get(f"https://wttr.in/{city}?m&T&lang={lang}")
        await utils.answer(message, f'<code>{n.join(req.text.splitlines()[:7])}</code>')

    async def weather_inline_handler(self, query: GeekInlineQuery) -> None:
        """Search city"""
        args = query.args
        if not args:
            args = self.db.get(self.strings['name'], 'city', "")
        if not args:
            return
        # req = requests.get(f"https://wttr.in/{quote_plus(args)}?format=j1").json()
        lang = 'ru' if args and args[0].lower() in rus else 'en'
        req = requests.get(f"https://wttr.in/{quote_plus(args)}?format=3")
        await query.answer(
            [
                InlineQueryResultArticle(
                    id=rand(20),
                    title=f"Forecast for {args}",
                    description=req.text,
                    # thumb_url="https://i.ytimg.com/vi/IMLwb8DIksk/maxresdefault.jpg",
                    input_message_content=InputTextMessageContent(
                        f'<code>{n.join(requests.get(f"https://wttr.in/{args}?m&T&lang={lang}").text.splitlines()[:7])}</code>',
                        parse_mode="HTML",
                    ),
                )
            ],
            cache_time=0,
        )
