#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
import asyncio
import json
import os
import shutil
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from Uploader import (
    DOWNLOAD_LOCATION,
    TG_MAX_FILE_SIZE,
    HTTP_PROXY
)
from Uploader.helper_funcs.display_progress import (
    progress_for_pyrogram,
    humanbytes
)
from Uploader.helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots
from Uploader.helper_funcs.extract_link import get_link
from Uploader.helper_funcs.run_cmnd import run_shell_command
from Uploader.helper_funcs.ran_text import random_char
# the Strings used for this "thing"
from Uploader.translation import Translation


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def youtube_dl_call_back(bot, update):
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
    thumb_image_path = DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + f'{ranom}' + ".jpg"
    save_ytdl_json_path = DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + f'{ranom}' + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except FileNotFoundError:
        await update.message.delete()
        return False

    youtube_dl_url, \
        custom_file_name, \
        youtube_dl_username, \
        youtube_dl_password = get_link(
            update.message.reply_to_message
        )
    if not custom_file_name:
        custom_file_name = str(response_json.get("title")) + \
            "_" + youtube_dl_format + "." + youtube_dl_ext
    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START
    )
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][:1021]
            # escape Markdown and special characters
    tmp_directory_for_each_user = os.path.join(
        DOWNLOAD_LOCATION,
        str(update.from_user.id),
        random_char(5)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(
        tmp_directory_for_each_user,
        custom_file_name
    )
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory
        ]
    else:
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = f"{youtube_dl_format}+bestaudio"
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory
        ]
    if HTTP_PROXY is not None:
        command_to_exec.append("--proxy")
        command_to_exec.append(HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.extend(("--no-warnings", "--restrict-filenames"))
    logger.info(command_to_exec)
    start = datetime.now()
    t_response, e_response = await run_shell_command(command_to_exec)
    logger.info(e_response)
    logger.info(t_response)
    if e_response and Translation.YTDL_ERROR_MESSAGE in e_response:
        error_message = e_response.replace(
            Translation.YTDL_ERROR_MESSAGE,
            ""
        )
        await update.message.edit_caption(
            caption=error_message
        )
        return False
    if t_response:
        # logger.info(t_response)
        os.remove(save_ytdl_json_path)
        end_one = datetime.now()
        time_taken_for_download = (end_one - start).seconds
        file_size = TG_MAX_FILE_SIZE + 1
        download_directory_dirname = os.path.dirname(download_directory)
        download_directory_contents = os.listdir(download_directory_dirname)
        for download_directory_c in download_directory_contents:
            current_file_name = os.path.join(
                download_directory_dirname,
                download_directory_c
            )
            file_size = os.stat(current_file_name).st_size

            if file_size == 0:
                await update.message.edit(text="File Not found 🤒")
                asyncio.create_task(clendir(tmp_directory_for_each_user))
                return

            if file_size > TG_MAX_FILE_SIZE:
                await update.message.edit_caption(
                    caption=Translation.RCHD_TG_API_LIMIT.format(
                        time_taken_for_download,
                        humanbytes(file_size)
                    )
                )

            else:
                is_w_f = False
                images = await generate_screen_shots(
                    current_file_name,
                    tmp_directory_for_each_user,
                    is_w_f,
                    "",
                    300,
                    9
                )
                logger.info(images)
                await update.message.edit_caption(
                    caption=Translation.UPLOAD_START
                )
                # get the correct width, height, and duration
                # for videos greater than 10MB
                # ref: message from @BotSupport
                width = 0
                height = 0
                duration = 0
                if tg_send_type != "file":
                    metadata = extractMetadata(createParser(current_file_name))
                    if metadata is not None and metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                # get the correct width, height, and duration
                # for videos greater than 10MB
                if os.path.exists(thumb_image_path):
                    # https://stackoverflow.com/a/21669827/4723940
                    Image.open(thumb_image_path).convert(
                        "RGB"
                    ).save(thumb_image_path)
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    if tg_send_type == "vm":
                        height = width
                else:
                    thumb_image_path = None
                start_time = time.time()
                # try to upload file
                if tg_send_type == "audio":
                    await update.message.reply_audio(
                        audio=current_file_name,
                        caption=description,
                        parse_mode="HTML",
                        duration=duration,
                        # performer=response_json["uploader"],
                        # title=response_json["title"],
                        # reply_markup=reply_markup,
                        thumb=thumb_image_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "file":
                    await update.message.reply_document(
                        document=current_file_name,
                        thumb=thumb_image_path,
                        caption=description,
                        parse_mode="HTML",
                        # reply_markup=reply_markup,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "vm":
                    await update.message.reply_video_note(
                        video_note=current_file_name,
                        duration=duration,
                        length=width,
                        thumb=thumb_image_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                elif tg_send_type == "video":
                    await update.message.reply_video(
                        video=current_file_name,
                        caption=description,
                        parse_mode="HTML",
                        duration=duration,
                        width=width,
                        height=height,
                        supports_streaming=True,
                        # reply_markup=reply_markup,
                        thumb=thumb_image_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Translation.UPLOAD_START,
                            update.message,
                            start_time
                        )
                    )
                else:
                    logger.info("Did this happen? :\\")
                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                try:
                    shutil.rmtree(tmp_directory_for_each_user)
                except:
                    pass
                await update.message.edit_caption(
                    caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
                        time_taken_for_download, time_taken_for_upload)

                )

                logger.info(f"[OK] Downloaded in: {str(time_taken_for_download)}")
                logger.info(f"[OK] Uploaded in: {str(time_taken_for_upload)}")
            #
            shutil.rmtree(
                tmp_directory_for_each_user,
                ignore_errors=True
            )
            asyncio.create_task(clendir(thumb_image_path))
            asyncio.create_task(clendir(tmp_directory_for_each_user))

            await update.message.delete()


async def clendir(directory):
    try:
        shutil.rmtree(directory)
    except:
        pass
    try:
        os.remove(directory)
    except:
        pass
