__version__ = (2, 3, 1)

""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
# scope: inline_content
# requires: requests bs4 spotipy
# meta developer: @morisummermods
from bs4 import BeautifulSoup
import spotipy
import requests
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InputTextMessageContent,
)
from telethon.tl.types import Message  # noqa
from urllib.parse import quote_plus
from .. import loader  # noqa
import logging
import re

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
    "Host": "api.genius.com",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/99.0.4844.82 Safari/537.36"
}
host = "https://api.genius.com"
n = "\n"


def get_lyrics(song_url, remove_section_headers=False):
    """Uses BeautifulSoup to scrape song info off of a Genius song URL"""
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
    return lyrics


def search(q):
    """Search documents hosted on Genius"""
    req = requests.get(
        f"https://api.genius.com/search"
        f"?text_format=plain"
        f"&q={quote_plus(q)}"
        f"&access_token=uhYUr-qrBp5V3o46lA8vcaL1DKXTWVs5SDsb_0CDCIcKxKLwtapqeqkdNu8JnA6w",
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
    """Add https protocol to link"""
    return x if not x.startswith("//") else f"https:{x}"


def link(url: str) -> InlineKeyboardMarkup:
    """InlineKeyboardButton markup generator"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎵 Full lyrics on Genius", url=url))
    return markup


class LyricsMod(loader.Module):
    """Song lyrics from Genius"""

    strings = {
        "name": "Lyrics",
        "type_name": "<b>🚫 Please type name of the song</b>",
        "genius": "🎵 Full lyrics on Genius",
        "noSpotify": "<b>🚫 Please install SpotifyNow module and proceed auth</b>\n"
        "🌃 Install: <code>.dlmod https://mods.hikariatama.ru/spotify.py</code>",
        "sauth": "<b>🚫 Execute <code>.sauth</code> before using this action.</b>",
        "SpotifyError": "<b>🚫 Spotify error</b>",
        "noResults": "<b>🚫 No results found</b>",
    }

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def lyricscmd(self, message: Message):
        """Get lyrics"""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text:
            if reply:
                try:
                    e = next(
                        entity
                        for entity in reply.entities
                        if type(entity).__name__ == "MessageEntityCode"
                    )
                    text = reply.raw_text[e.offset - 1 : e.offset + e.length]
                except Exception:
                    text = reply.raw_text
            else:
                await utils.answer(message, self.strings["type_name"])
                return
        tracks = search(text)
        if len(tracks) > 0:
            track = tracks[0]
        else:
            await utils.answer(message, self.strings["noResults"])
            return
        await self.inline.form(
            f"Lyrics for <b>{track['title']}</b> by <b>{track['artists']}</b>{n}"
            f"<i>{get_lyrics(track['url'])}"[:4092] + "</i>",
            reply_markup=[[{"text": self.strings["genius"], "url": track["url"]}]],
            force_me=False,
            message=message,
        )

    async def lyrics_inline_handler(self, query: GeekInlineQuery) -> None:
        """Search song"""
        text = query.args
        if not text:
            return
        tracks = search(text)
        if not tracks:
            await query.answer(
                [
                    InlineQueryResultArticle(
                        id="-1",
                        title=self.strings["noResults"],
                        description="Please try again",
                        thumb_url="https://img.icons8.com/stickers/100/000000/nothing-found.png",
                        input_message_content=InputTextMessageContent(
                            f"{self.strings['noResults']} for <code>{text}</code>",
                            parse_mode="HTML",
                        ),
                    )
                ],
                cache_time=0,
            )
            return
        res = [
            InlineQueryResultArticle(
                id=track["id"],
                title=track["title"],
                description=track["artists"],
                thumb_url=add_protocol(track["pic"]),
                input_message_content=InputTextMessageContent(
                    # f"{get_lyrics(tracks['url'])}",
                    f"Lyrics for <b>{track['title']}</b> by <b>{track['artists']}</b>{n}"
                    f"<i>{get_lyrics(track['url'])}"[:4092] + "</i>",
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                ),
                reply_markup=link(track["url"]),
            )
            for track in tracks[:10]
        ]
        await query.answer(res, cache_time=0)

    async def slyricscmd(self, message: Message):
        """Get lyrics from your current Spotify playback (Needs SpotifyNow module)"""
        check = self.db.get("SpotifyNow", "acs_tkn", "404")
        if check == "404":
            await utils.answer(message, self.strings["noSpotify"])
            return
        elif check is None:
            await utils.answer(message, self.strings["sauth"])
            return
        try:
            sp = spotipy.Spotify(
                auth=self.db.get("SpotifyNow", "acs_tkn")["access_token"]
            )
            current_playback = sp.current_playback()
        except Exception:
            await utils.answer(message, self.strings["SpotifyError"])
            return
        try:
            track = current_playback["item"]["name"]
        except Exception:
            track = None
        try:
            artists = [artist["name"] for artist in current_playback["item"]["artists"]]
        except Exception:
            artists = None
        tracks = search(f"{artists} {track}")
        if len(tracks) > 0:
            track = tracks[0]
        else:
            await utils.answer(message, self.strings["noResults"])
            return
        await self.inline.form(
            f"Lyrics for <b>{track['title']}</b> by <b>{track['artists']}</b>{n}"
            f"<i>{get_lyrics(track['url'])}"[:4092] + "</i>",
            reply_markup=[[{"text": self.strings["genius"], "url": track["url"]}]],
            force_me=False,
            message=message,
        )
