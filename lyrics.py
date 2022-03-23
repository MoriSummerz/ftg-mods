__version__ = (1, 0, 1)

""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
# scope: inline_content
# requires: requests bs4
# meta developer: @morisummermods
from .. import loader, utils  # noqa
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InputTextMessageContent,
)
import logging
from ..inline import GeekInlineQuery, rand  # noqa
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}


def get_lyrics(link):
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    n = "\n"
    try:
        res = f'<b><a href="{link}">{soup.find("div", class_="lyrics-to").get_text()}</a></b>:\n'
        res += f"<i>{''.join([p.get_text() + n for p in soup.find_all('p', class_='mxm-lyrics__content')])}</i>"
        return res
    except Exception:
        return f"Lyrics not available.{n + link}"


def add_protocol(x):
    return x if not x.startswith("//") else f"https:{x}"


class LyricsMod(loader.Module):
    """Songs lyrics from Musixmatch"""

    strings = {"name": "Lyrics"}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def lyricscmd(self, message: Message):
        """Get lyrics"""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text:
            if reply and "My vibe" in reply.raw_text:
                text = reply.raw_text.splitlines()[0][11::]
            else:
                await utils.answer(message, "<b>🚫 Please type name of the song</b>")
                return
        link = "https://www.musixmatch.com/search/"
        page = requests.get(link + quote_plus(text) + "/tracks", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        track = soup.find("li", class_="showArtist")
        if not track:
            await message.edit("No results found")
            return
        link = "https://www.musixmatch.com" + track.find("a", class_="title")["href"]
        # pic = track.find('img')['srcset'].split()[-2]
        await message.edit(get_lyrics(link), link_preview=False)

    async def lyrics_inline_handler(self, query: GeekInlineQuery) -> None:
        """Search song"""
        text = query.args
        if not text:
            return
        endpoint = f"https://www.musixmatch.com/search/{quote_plus(text)}/tracks"
        page = requests.get(endpoint, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        res = [
            InlineQueryResultArticle(
                id=rand(20),
                title=track.find("a", class_="title").get_text(),
                description=", ".join(
                    [i.get_text() for i in track.find_all("a", class_="artist")]
                ),
                input_message_content=InputTextMessageContent(
                    get_lyrics(
                        "https://www.musixmatch.com"
                        + track.find("a", class_="title")["href"]
                    ),
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                ),
                **({"thumb_url": add_protocol(track.find("img")["srcset"].split()[-2])})
                if "has-picture" in str(track)
                else {},
            )
            for track in soup.find_all("li", class_="showArtist")[:10]
        ]
        await query.answer(res, cache_time=0)
