#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
import time
import requests
import os

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# the Strings used for this "thing"
from Uploader.translation import Translation
from Uploader.helper_funcs.display_progress import anonofile_progress
from Uploader import (
    UPLOADER_LOCATION
)

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
        reply_to_message_id=update.id
    )

@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        reply_markup=Translation.START_BUTTONS,
        reply_to_message_id=update.id
    )

@Client.on_message(filters.command(["about"]))
async def about(bot, update):
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=Translation.ABOUT_BUTTONS,
        reply_to_message_id=update.id
    )

@Client.on_message(filters.media & filters.private)
async def upload(bot, message):
    m = await message.reply("Download You file to my Server...")
    now = time.time()
    sed = await bot.download_media(
            message,
            f"{UPLOADER_LOCATION}/",
            progress=anonofile_progress,
            progress_args=(
                Translation.AONFILE_UPLOAD_SERVER_PROGRESS, 
                m,
                now
            )
        )
    try:
        files = {'file': open(sed, 'rb')}
        await m.edit(Translation.ANONFILE_UPLOAD)
        callapi = requests.post("https://api.anonfiles.com/upload", files=files)
        text = callapi.json()
        output = Translation.ANONFILE_UPLOAD_SUCCESS.format(
            text['data']['file']['metadata']['name'],
            text['data']['file']['metadata']['size']['readable'],
            text['data']['file']['url']['full']
        )
        btn = InlineKeyboardMarkup(
                                [[InlineKeyboardButton("📥 Download 📥", url=f"{text['data']['file']['url']['full']}")]])
        await m.edit(output, reply_markup=btn)
    except Exception:
        await bot.send_message(message.chat.id, text="Something Went Wrong!")
       
    os.remove(sed)