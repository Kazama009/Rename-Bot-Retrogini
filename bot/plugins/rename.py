import os
import time
import math
import asyncio

from pyrogram import Client, filters
from pyrogram.types import  ForceReply


from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from PIL import Image

from bot import *
from bot.sql.thumbnail_sql import *



async def force_name(bot, message):

    await bot.send_message(
        message.reply_to_message.from_user.id,
        "Enter new name for media\n\nNote : Extension not required",
        reply_to_message_id=message.reply_to_message.message_id,
        reply_markup=ForceReply(True)
    )


@Client.on_message(filters.private & filters.reply & filters.text)
async def cus_name(bot, message):
    
    if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        asyncio.create_task(rename_doc(bot, message))     
    else:
        print('No media present')


async def rename_doc(bot, message):
    
    mssg = await bot.get_messages(
        message.chat.id,
        message.reply_to_message.message_id
    )    
    
    media = mssg.reply_to_message

    
    if media.empty:
        await message.reply_text('Why did you delete that 😕', True)
        return
        
    filetype = media.document or media.video or media.audio or media.voice or media.video_note
    try:
        actualname = filetype.file_name
        splitit = actualname.split(".")
        extension = (splitit[-1])
    except:
        extension = "mkv"

    await bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=message.reply_to_message.message_id,
        revoke=True
    )

    file_name = message.text
    description = CUSTOM_CAPTION_UL_FILE.format(newname=file_name)
    download_location = DOWNLOAD_LOCATION + "/"

    sendmsg = await bot.send_message(
        chat_id=message.chat.id,
        text=DOWNLOAD_START,
        reply_to_message_id=message.message_id
        )

    c_time = time.time()
    the_real_download_location = await bot.download_media(
        message=media,
        file_name=download_location,
        progress=progress_for_pyrogram,
        progress_args=(
        DOWNLOAD_START,
        sendmsg,
        c_time
        )
    )

    if the_real_download_location is not None:
        try:
            await bot.edit_message_text(
                text=SAVED_RECVD_DOC_FILE,
                chat_id=message.chat.id,
                message_id=sendmsg.message_id
            )
        except:
            await sendmsg.delete()
            sendmsg = await message.reply_text(SAVED_RECVD_DOC_FILE, quote=True)

        new_file_name = download_location + file_name + "." + extension
        os.rename(the_real_download_location, new_file_name)
        try:
            await bot.edit_message_text(
                text=UPLOAD_START,
                chat_id=message.chat.id,
                message_id=sendmsg.message_id
                )
        except:
            await sendmsg.delete()
            sendmsg = await message.reply_text(UPLOAD_START, quote=True)

        thumb_image_path = download_location + str(message.from_user.id) + ".jpg"
        if not os.path.exists(thumb_image_path):
            mes = await thumb(message.from_user.id)
            if mes != None:
                m = await bot.get_messages(message.chat.id, mes.msg_id)
                await m.download(file_name=thumb_image_path)
                thumb_image_path = thumb_image_path
            else:
                thumb_image_path = None                    
        else:
            width = 0
            height = 0
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)
            img.resize((320, height))
            img.save(thumb_image_path, "JPEG")

            c_time = time.time()
            await bot.send_document(
                chat_id=message.chat.id,
                document=new_file_name,
                thumb=thumb_image_path,
                caption=description,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    UPLOAD_START,
                    sendmsg, 
                    c_time
                )
            )

            try:
                os.remove(new_file_name)
            except:
                pass                 
            try:
                os.remove(thumb_image_path)
            except:
                pass  
            try:
                await bot.edit_message_text(
                    text=AFTER_SUCCESSFUL_UPLOAD_MSG,
                    chat_id=message.chat.id,
                    message_id=sendmsg.message_id,
                    disable_web_page_preview=True
                )
            except:
                await sendmsg.delete()
                await message.reply_text(AFTER_SUCCESSFUL_UPLOAD_MSG, quote=True)

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):

    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n\n⭕️Progress: {2}%\n".format(
            ''.join(["▣" for i in range(math.floor(percentage / 5))]),
            ''.join(["▢" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\n\n️⭕️Speed: {2}/s\n\n⭕️ETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]