__version__ = (1, 2, 0)

"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# meta developer: @morisummermods

import logging

from telethon.tl.types import Message

from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class Top20Mod(loader.Module):
    strings = {"name": "Top20"}

    async def client_ready(self, client, db) -> None:
        if hasattr(self, "hikka"):
            return

        self.db = db
        self.client = client

    async def top20cmd(self, message: Message) -> None:
        words = {}
        await message.edit("Processed 0 messages")
        total = 0
        async for msg in self.client.iter_messages(message.peer_id):
            total += 1
            if total % 500 == 0:
                await message.edit(f"Processed {total} messages")
            if msg.text:
                for word in msg.text.split():
                    if len(word) >= 3:
                        if word.lower() not in words:
                            words[word.lower()] = 0
                        else:
                            words[word.lower()] += 1
        global freq
        freq = sorted(words, key=words.get, reverse=True)
        out = "".join(
            f"Top {i + 1}. {words[freq[i]]} occurrences: {freq[i]}\n" for i in range(20)
        )
        await message.edit(out, parse_mode=None)
