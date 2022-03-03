""""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummerzxc
    Licensed under the Apache License, Version 2.0
"""
from .. import loader, utils  # noqa
from telethon.tl.types import Message  # noqa
import logging
from asyncio import sleep
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)
letters = {
    " ": "000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000",
    "a": "000000000000\n000001100000\n000011110000\n000111111000\n001110011100\n001100001100\n001100001100\n001111111100\n001111111100\n001100001100\n001100001100\n000000000000",
    "b": "000000000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111000\n001111111000\n001100001100\n001100001100\n001111111100\n001111111000\n000000000000",
    "c": "000000000000\n000111111000\n001111111100\n001100001100\n001100000000\n001100000000\n001100000000\n001100000000\n001100001100\n001111111100\n000111111000\n000000000000",
    "d": "000000000000\n001111111000\n001111111100\n000110001100\n000110001100\n000110001100\n000110001100\n000110001100\n000110001100\n001111111100\n001111111000\n000000000000",
    "e": "000000000000\n001111111000\n001111111000\n001100000000\n001100000000\n001111110000\n001111110000\n001100000000\n001100000000\n001111111000\n001111111000\n000000000000",
    "f": "000000000000\n000111111000\n001111111000\n001100000000\n001100000000\n001111110000\n001111110000\n001100000000\n001100000000\n001100000000\n001100000000\n000000000000",
    "g": "000000000000\n000111111000\n001111111100\n001100000000\n001100000000\n001100111100\n001100111100\n001100001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "h": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n001111111100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "i": "000000000000\n001111111100\n001111111100\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n001111111100\n001111111100\n000000000000",
    "j": "000000000000\n000111111100\n000111111100\n000000011000\n000000011000\n000000011000\n000000011000\n001100011000\n001100011000\n001111111000\n000111110000\n000000000000",
    "k": "000000000000\n001100001100\n001100011100\n001100111000\n001101110000\n001111100000\n001111100000\n001101110000\n001100111000\n001100011100\n001100001100\n000000000000",
    "l": "000000000000\n001100000000\n001100000000\n001100000000\n001100000000\n001100000000\n001100000000\n001100000000\n001100000000\n001111111100\n001111111100\n000000000000",
    "m": "000000000000\n001100001100\n001110011100\n001111111100\n001111111100\n001101101100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "n": "000000000000\n001100001100\n001110001100\n001111001100\n001111101100\n001101111100\n001100111100\n001100011100\n001100001100\n001100001100\n001100001100\n000000000000",
    "o": "000000000000\n000111111000\n001111111100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "p": "000000000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n001100000000\n001100000000\n001100000000\n001100000000\n000000000000",
    "q": "000000000000\n000111111000\n001111111100\n001100001100\n001100001100\n001100001100\n001101101100\n001101111100\n001100111000\n001111111100\n000111101100\n000000000000",
    "r": "000000000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n001100011100\n001100001100\n001100001100\n001100001100\n000000000000",
    "s": "000000000000\n000111111000\n001111111100\n001100001100\n001100000000\n001111111000\n000111111100\n000000001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "t": "000000000000\n001111111100\n001111111100\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000000000000",
    "u": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "v": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001110011100\n000111111000\n000011110000\n000001100000\n000000000000",
    "w": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001101101100\n001111111100\n001111111100\n001110011100\n001100001100\n000000000000",
    "x": "000000000000\n001100001100\n001100001100\n001110011100\n000111011000\n000011110000\n000011110000\n000110111000\n001110011100\n001100001100\n001100001100\n000000000000",
    "y": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111100\n000000001100\n000000001100\n001111111100\n001111111000\n000000000000",
    "z": "000000000000\n001111111100\n001111111100\n000000011100\n000000111000\n000001110000\n000011100000\n000111000000\n001110000000\n001111111100\n001111111100\n000000000000",
    "а": "000000000000\n000001100000\n000011110000\n000111111000\n001110011100\n001100001100\n001100001100\n001111111100\n001111111100\n001100001100\n001100001100\n000000000000",
    "б": "000000000000\n001111111000\n001111111000\n001100000000\n001100000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n000000000000",
    "в": "000000000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111000\n001111111000\n001100001100\n001100001100\n001111111100\n001111111000\n000000000000",
    "г": "000000000000\n000011111100\n000111111100\n000110000000\n000110000000\n000110000000\n000110000000\n000110000000\n000110000000\n000110000000\n000110000000\n000000000000",
    "д": "000000000000\n000001111000\n000011111100\n000111001100\n001110001100\n001100001100\n001111111100\n011111111110\n011100001110\n011000000110\n011000000110\n000000000000",
    "е": "000000000000\n001111111000\n001111111000\n001100000000\n001100000000\n001111110000\n001111110000\n001100000000\n001100000000\n001111111000\n001111111000\n000000000000",
    "ё": "000000000000\n001111111000\n001111111000\n001100000000\n001100000000\n001111110000\n001111110000\n001100000000\n001100000000\n001111111000\n001111111000\n000000000000",
    "ж": "000000000000\n001101101100\n001101101100\n001111111100\n000111111000\n000011110000\n000011110000\n000111111000\n001111111100\n001101101100\n001101101100\n000000000000",
    "з": "000000000000\n000111111000\n001111111100\n001100001100\n000000001100\n000001111000\n000001111000\n000000001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "и": "000000000000\n001100001100\n001100001100\n001100011100\n001100111100\n001101111100\n001111101100\n001111001100\n001110001100\n001100001100\n001100001100\n000000000000",
    "й": "000000000000\n001101101100\n001100001100\n001100011100\n001100111100\n001101111100\n001111101100\n001111001100\n001110001100\n001100001100\n001100001100\n000000000000",
    "к": "000000000000\n001100001100\n001100011100\n001100111000\n001101110000\n001111100000\n001111100000\n001101110000\n001100111000\n001100011100\n001100001100\n000000000000",
    "л": "000000000000\n000001100000\n000011110000\n000111111000\n001110011100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "м": "000000000000\n001100001100\n001110011100\n001111111100\n001111111100\n001101101100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "н": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n001111111100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "о": "000000000000\n000111111000\n001111111100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "п": "000000000000\n001111111100\n001111111100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n000000000000",
    "р": "000000000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n001100000000\n001100000000\n001100000000\n001100000000\n000000000000",
    "с": "000000000000\n000111111000\n001111111100\n001100001100\n001100000000\n001100000000\n001100000000\n001100000000\n001100001100\n001111111100\n000111111000\n000000000000",
    "т": "000000000000\n001111111100\n001111111100\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000000000000",
    "у": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111100\n000000001100\n000000001100\n001111111100\n001111111000\n000000000000",
    "ф": "000000000000\n000111111000\n001111111100\n011001100110\n011001100110\n011001100110\n001111111100\n000111111000\n000001100000\n000001100000\n000001100000\n000000000000",
    "х": "000000000000\n001100001100\n001100001100\n001110011100\n000111011000\n000011110000\n000011110000\n000110111000\n001110011100\n001100001100\n001100001100\n000000000000",
    "ц": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001111111110\n000111111110\n000000000110\n000000000000",
    "ч": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001100001100\n001111111100\n000111111100\n000000001100\n000000001100\n000000001100\n000000000000",
    "ш": "000000000000\n001100001100\n001100001100\n001100001100\n001101101100\n001101101100\n001101101100\n001101101100\n001101101100\n001111111100\n001111111100\n000000000000",
    "щ": "000000000000\n001100001100\n001100001100\n001100001100\n001101101100\n001101101100\n001101101100\n001101101100\n001111111110\n001111111110\n000000000110\n000000000000",
    "ь": "000000000000\n001100000000\n001100000000\n001100000000\n001100000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n000000000000",
    "ъ": "000000000000\n011100000000\n011100000000\n001100000000\n001100000000\n001111111000\n001111111100\n001100001100\n001100001100\n001111111100\n001111111000\n000000000000",
    "ы": "000000000000\n001100001100\n001100001100\n001100001100\n001100001100\n001111101100\n001111111100\n001100011100\n001100011100\n001111111100\n001111101100\n000000000000",
    "э": "000000000000\n000111111000\n001111111100\n001100001100\n000000001100\n000011111100\n000011111100\n000000001100\n001100001100\n001111111100\n000111111000\n000000000000",
    "ю": "000000000000\n011001111100\n011011111110\n011011000110\n011011000110\n011111000110\n011111000110\n011011000110\n011011000110\n011011111110\n011001111100\n000000000000",
    "я": "000000000000\n000111111100\n001111111100\n001100001100\n001100001100\n001111111100\n000111111100\n000000111100\n000001111100\n000011101100\n000111001100\n000000000000",
    ".": "000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000000000000\n000001100000\n000001100000\n000000000000",
    "!": "000000000000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000001100000\n000000000000\n000000000000\n000001100000\n000001100000\n000000000000",
    "💖": "000000000000\n001110011100\n011🤍11111110\n01🤍111111110\n011111111110\n011111111110\n011111111110\n001111111100\n000111111000\n000011110000\n000001100000\n000000000000"
}


class MagicTextMod(loader.Module):
    """Magic Text generator"""
    strings = {"name": "MagicText",
               "inline_message": "❤️‍🔥 I want to tell you something..."}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        self.symbols = self.db.get(self.strings['name'], 'symbols', '✨💖')

    async def mtsetcmd(self, message: Message):
        """Set the symbols for animation (Separated by space. Example: .mtset ✨ 💖)"""
        text = utils.get_args_raw(message).split()

        if len(text) != 2:
            await message.edit('<b>🚫 Please type only 2 symbols</b>')
            return

        self.db.set(self.strings['name'], 'symbols', text)
        self.symbols = text

        await message.edit('<b>✅ Symbols set successfully</b>')

    async def mtcmd(self, message: Message):
        """Send message with animating text"""
        text = utils.get_args_raw(message)
        text = text.replace("<3", "💖")
        await message.edit(letters[' '].replace("0", self.symbols[0]))
        _last = ""
        for letter in text:
            if _last and _last == letter:
                await sleep(.7)
                continue

            if letter not in letters and _last not in letters:
                await sleep(.7)
                continue

            await message.edit(
                letters.get(letter.lower(), '<b>🚫 Not supported symbol</b>')
                    .replace("0", self.symbols[0])
                    .replace("1", self.symbols[1])
            )

            _last = letter
            await sleep(.7)
        text = text.replace("💖", "<3")

        await message.edit(f"{self.symbols[0]}{self.symbols[1]}<b>{text}</b>{self.symbols[1]}{self.symbols[0]}")

    async def mticmd(self, message: Message) -> None:
        """Send inline message with animating text"""
        text = utils.get_args_raw(message)

        await self.inline.form(self.strings['inline_message'], reply_markup=[[{
            'text': '💖 Open',
            'callback': self.inline__handler,
            'args': (text,),
        }]], force_me=False, message=message, ttl=60 * 60)

    async def inline__handler(self, call: CallbackQuery, args: str) -> None:
        """Inline handler"""
        args = args.replace("<3", "💖")
        await call.edit(letters[' '].replace("0", self.symbols[0]))
        _last = ""

        for letter in args:
            if _last and _last == letter:
                await sleep(.7)
                continue

            if letter not in letters and _last not in letters:
                await sleep(.7)
                continue

            await call.edit(
                letters.get(letter.lower(), '<b>🚫 Not supported symbol</b>')
                    .replace("0", self.symbols[0])
                    .replace("1", self.symbols[1])
            )

            _last = letter
            await sleep(.7)

        args = args.replace("💖", "<3")

        await call.edit(f"{self.symbols[0]}{self.symbols[1]}<b>{args}</b>{self.symbols[1]}{self.symbols[0]}")
        await call.unload()
