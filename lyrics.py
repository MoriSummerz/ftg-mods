__version__ = (2, 0, 1)

""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
# scope: inline_content
# requires: requests bs4
# meta developer: @morisummermods
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InputTextMessageContent,
)
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
from telethon.tl.types import Message  # noqa
import re
from .. import loader  # noqa

try:
    from ..inline import GeekInlineQuery, rand  # noqa
    from .. import utils  # noqa
except ImportError:
    from ..inline.types import GeekInlineQuery  # noqa
    from .. import utils  # noqa
    from ..utils import rand  # noqa

logger = logging.getLogger(__name__)

api_headers = {
    "User-Agent": "CompuServe Classic/1.22",
    "Accept": "application/json",
    "Host": "api.genius.com"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
host = "https://api.genius.com"
n = "\n"


def get_lyrics(song_url, remove_section_headers=False):
    page = requests.get(song_url, headers=headers)
    html = BeautifulSoup(page.text.replace("<br/>", "\n"), "html.parser")
    lyrics = "\n".join(
        [
            p.get_text()
            for p in html.find_all("div", attrs={"data-lyrics-container": "true"})
        ]
    )
    # Remove [Verse], [Bridge], etc.
    lyrics = re.sub(r"(\[.*?\])", "</i><b>\g<1></b><i>", lyrics)
    if remove_section_headers:
        lyrics = re.sub(r"(\[.*?\])*", "", lyrics)
        lyrics = re.sub("\n{2}", "\n", lyrics)
    if not lyrics:
        return "<b>🚫 Couldn't find the lyrics</b>"
    return f"<i>{lyrics}</i>"


def search(q):
    req = requests.get(
        f"https://api.genius.com/search?text_format=plain&q={quote_plus(q)}&access_token=uhYUr-qrBp5V3o46lA8vcaL1DKXTWVs5SDsb_0CDCIcKxKLwtapqeqkdNu8JnA6w",
        headers=api_headers,
    ).json()

    return [
        {
            "artists": hit["result"]["artist_names"].replace("\u200b", ""),
            "title": hit["result"]["title"].replace("\u200b", ""),
            "pic": hit["result"]["header_image_thumbnail_url"],
            "url": hit["result"]["url"],
            "id": hit["result"]["id"],
        }
        for hit in req["response"]["hits"]
    ]


def add_protocol(x):
    return x if not x.startswith("//") else f"https:{x}"


class LyricsMod(loader.Module):
    """Songs lyrics from Genius"""

    strings = {"name": "Lyrics"}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def lyricscmd(self, message: Message):
        """Get lyrics"""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text:
            if reply:
                if "My vibe" in reply.raw_text:
                    text = reply.raw_text.splitlines()[0][11::]
                else:
                    text = reply.raw_text
            else:
                await utils.answer(message, "<b>🚫 Please type name of the song</b>")
                return
        tracks = search(text)
        if len(tracks) > 0:
            track = tracks[0]
        else:
            await utils.answer(message, "<b>🚫 No results found</b>")
            return
        # pic = track.find('img')['srcset'].split()[-2]
        await utils.answer(message, get_lyrics(track["url"]), link_preview=False)

    async def lyrics_inline_handler(self, query: GeekInlineQuery) -> None:
        """Search song"""
        text = query.args
        if not text:
            return
        tracks = search(text)
        if not tracks:
            return
        res = [
            InlineQueryResultArticle(
                id=track["id"],
                title=track["title"],
                description=track["artists"],
                thumb_url=add_protocol(track["pic"]),
                input_message_content=InputTextMessageContent(
                    # f"{get_lyrics(tracks['url'])}",
                    f"Lyrics for <b>{track['title']}</b> by <b>{track['artists']}</b>{n}{get_lyrics(track['url'])}",
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                ),
            )
            for track in tracks[:10]
        ]
        await query.answer(res, cache_time=0)
