#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging

# the Strings used for this "thing"
from Uploader.translation import Translation

from pyrogram import (
    Client,
    filters
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.command(["help"]))
async def help_user(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=Translation.HELP_BUTTONS,
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        reply_markup=Translation.START_BUTTONS,
        reply_to_message_id=update.message_id
    )

@Client.on_message(filters.command(["about"]))
async def about(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=Translation.ABOUT_BUTTONS,
        reply_to_message_id=update.message_id
    )