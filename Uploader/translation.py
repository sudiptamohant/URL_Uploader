from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation:
    START_TEXT = (
    "Hi {} ,\n\n"
    "I'm a Telegram URL Uploader Bot!"
    )
    
    ABOUT_TEXT = (
        "**Creater:** [Divarion-D](https://t.me/Divarion_D)\n\n"
        "**Language:** [Python3](https://www.python.org)\n\n"
        "**Library:** [Pyrogram](https://docs.pyrogram.org)\n\n"
        "**Source Code:** [Click here](https://github.com/Divarion-D/URL_Uploader)"
    )

    HELP_TEXT = (
        "Send Me Any Direct Download Link\n"
        "I Can Upload To Telegram as File/Video"
    )

    FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size might be approximate</a> \nIf you want to set custom thumbnail, send photo before or quickly after tapping on any of the below buttons.\nYou can use /deletethumbnail to delete the auto-generated thumbnail."
    SET_CUSTOM_USERNAME_PASSWORD = """If you want to download premium videos, provide in the following format:
URL | filename | username | password"""
    DOWNLOAD_START = "trying to download"
    UPLOAD_START = "trying to upload"
    RCHD_TG_API_LIMIT = "I cannot upload files greater than 1.95GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG = "Please rate me if you find me useful. https://t.me/tlgrmcbot?start=anydl_bot-bot"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in {} seconds. \nPlease rate me if you find me useful. https://t.me/tlgrmcbot?start=anydl_bot-bot \nUploaded in {} seconds."
    SAVED_CUSTOM_THUMB_NAIL = "Custom video / file thumbnail saved. This image will be used in the video / file."
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ Custom thumbnail cleared succesfully."
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
    SAVED_RECVD_DOC_FILE = "Document Downloaded Successfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_VOID_FORMAT_FOUND = "no-one gonna help you\n<b>YouTubeDL</b> said: {}"
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    YTDL_ERROR_MESSAGE = (
        "please report this issue on https://yt-dl.org/bug . "
        "Make sure you are using the latest version; see "
        " https://yt-dl.org/update  on how to update. "
        "Be sure to call yt-dlp with the --verbose flag "
        "and include its complete output."
    )
    ISOAYD_PREMIUM_VIDEOS = "video is only available for registered users"


    START_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('❓ Help', callback_data='help'),
            InlineKeyboardButton('🦊 About', callback_data='about')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('🦊 About', callback_data='about')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('❓ Help', callback_data='help')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )