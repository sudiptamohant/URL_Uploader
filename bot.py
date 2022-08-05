#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
import os
from pyrogram import Client
from Uploader import (
    APP_ID,
    API_HASH,
    DOWNLOAD_LOCATION,
    TG_BOT_TOKEN
)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    plugins = dict(
        root="Uploader/plugins"
    )
    app = Client(
        "UploaderBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()