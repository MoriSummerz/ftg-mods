__version__ = (1, 1, 0)

"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# meta developer: @morisummermods
from .. import loader, utils  # noqa
from telethon.tl.types import Message  # noqa
import logging
from telethon.utils import get_display_name  # noqa
from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)


class PicsaverMod(loader.Module):
    """ "Automatic Self-destructing media saver to Saved Messages"""

    strings = {
        "name": "Picsaver",
        "author": "morisummermods"
    }

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        self.enable = db.get(self.strings["name"], "enable", True)
        try:
            await client(JoinChannelRequest(await self.client.get_entity(f"t.me/{self.strings['author']}")))
        except Exception:
            logger.error(f"Can't join {self.strings['author']}")

    async def watcher(self, message: Message) -> None:
        if (
                getattr(message, "media", False)
                and getattr(message.media, "ttl_seconds", False)
                and self.enable
        ):
            media = await self.client.download_media(message.media)
            name = get_display_name(await self.client.get_entity(message.sender_id))
            return await self.client.send_file(
                "me", media, caption=f"Self-destructing media from {name}"
            )

    async def spcmd(self, message: Message):
        """Reply to self-destructing media to save"""
        reply = await message.get_reply_message()
        if (
                not reply
                or not getattr(reply, "media", False)
                or not getattr(reply.media, "ttl_seconds", False)
        ):
            return await message.edit("Reply for self-destructing media !")
        await message.delete()
        media = await self.client.download_media(reply.media)
        name = get_display_name(await self.client.get_entity(reply.sender_id))
        return await self.client.send_file(
            "me", media, caption=f"Self-destructing media from {name}"
        )

    async def pscmd(self, message: Message):
        """Enable/disable automatic self-destructing media save"""
        if self.enable:
            self.enable = False
            self.db.set(self.strings["name"], "enable", False)
            return await utils.answer(message, "<b>Autosave is disabled</b>")
        else:
            self.enable = True
            self.db.set(self.strings["name"], "enable", True)
            return await utils.answer(message, "<b>Autosave is enabled</b>")
