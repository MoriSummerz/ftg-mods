""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
from .. import loader, utils
from telethon.tl.types import *
import logging

logger = logging.getLogger(__name__)


@loader.tds
class Top20Mod(loader.Module):
    strings = {"name": "Top20"}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def top20cmd(self, message: Message) -> None:

        words = {}
        await message.edit("Processed 0 messages")
        total = 0
        async for msg in self.client.iter_messages(message.peer_id):
            total += 1
            if total % 500 == 0:
                await message.edit("Processed {} messages".format(total))
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
            "Top {}. {} occurrences: {}\n".format(i + 1, words[freq[i]], freq[i])
            for i in range(20)
        )

        await message.edit(out, parse_mode=None)
