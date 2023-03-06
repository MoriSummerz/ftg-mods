__version__ = (1, 0, 1)
"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

from asyncio import sleep

from .. import loader, utils


class TimerBotMod(loader.Module):
    strings = {"name": "TimeBot"}

    async def client_ready(self, client, db) -> None:
        if hasattr(self, "hikka"):
            return

        self.db = db
        self.client = client

    async def timebcmd(self, message):
        """Пример ввода: .timeb <задержка появления текста в минутах> <текст>"""
        args = utils.get_args(message)
        if not args:
            self.db.set(self.strings["name"], "state", False)
            await utils.answer(message, "<b>Модуль TimeBot остановлен!</b>")
            return

        await utils.answer(
            message,
            (
                "<b>Модуль TimeBot запущен!\n\n"
                "Чтобы его остановить, используй <code>.timeb</code></b>"
            ),
        )

        try:
            time = float(args[0]) * 60
        except ValueError:
            await utils.answer(message, "<b>Введите корректную задержку!</b>")
            return

        text = " ".join(utils.get_args_raw(message).split()[1:])
        self.db.set(self.strings["name"], "state", True)

        while self.db.get(self.strings["name"], "state"):
            await message.respond(text)
            await sleep(0.1)
            await sleep(time)
