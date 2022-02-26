""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
# requires: pyqrcode pypng
import pyqrcode
import qrtools
import io
from .. import loader, utils
from telethon.tl.types import *
import logging

logger = logging.getLogger(__name__)


@loader.tds
class QRMod(loader.Module):
    """QR code generator"""
    strings = {"name": "QR"}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def qrcmd(self, message: Message) -> None:
        """Generate QR code"""
        reply = await message.get_reply_message()
        text = reply.raw_text if reply else utils.get_args_raw(message)
        if not text:
            await message.edit('❌ Please type text or reply to text')
        await message.delete()
        qr = pyqrcode.create(text.encode('utf-8'), encoding='utf-8')
        buffer = io.BytesIO()
        qr.png(buffer, scale=10)
        buffer.name = "image.png"
        await self.client.send_file(message.peer_id, buffer.getvalue(), caption='Generated QR code',
                                    reply_to=message.reply_to_msg_id)
