#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import contextlib
import math
import time

from Uploader import (
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR
)


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.0) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        progress = "[{0}{1}] \nP: {2}%\n".format(''.join([FINISHED_PROGRESS_STR for _ in range(math.floor(percentage / 5))]), ''.join([UN_FINISHED_PROGRESS_STR for _ in range(20 - math.floor(percentage / 5))]), round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(humanbytes(current), humanbytes(total), humanbytes(speed), estimated_total_time if estimated_total_time != '' else "0 s")

        with contextlib.suppress(Exception):
            await message.edit(f"{ud_type}\n {tmp}")


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )

    return tmp[:-2]

def anonofile_time_data(start_time):
    end = time.time()
    now = end - start_time
    now_time = now
    day = now_time // (24 * 3600)
    now_time = now_time % (24 * 3600)
    hour = now_time // 3600
    now_time %= 3600
    minutes = now_time // 60
    now_time %= 60
    seconds = now_time
    if(day!=0):
        return "%dd %dh %dm %ds" % (day, hour, minutes, seconds)
    if(hour!=0):
        return "%dh %dm %ds" % (hour, minutes, seconds)
    else:
        return "%dm %ds" % (minutes, seconds)


async def anonofile_progress(current, total, up_msg, message, start_time):
    with contextlib.suppress(Exception):
        await message.edit(text=f"{up_msg} {current * 100 / total:.1f}% in {anonofile_time_data(start_time)}")