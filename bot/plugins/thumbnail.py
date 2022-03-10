import os

from pyrogram import filters, Client

from bot import DOWNLOAD_LOCATION
from bot.sql import thumbnail_sql as sql

# Saves Thumbnail
@Client.on_message(filters.photo)
async def save_thumbnail(bot, update):
    if update.media_group_id is not None:
        download_location = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"

        if not os.path.isdir(download_location):
            os.makedirs(download_location)

        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        download_location = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
        await sql.df_thumb(update.from_user.id, update.message_id)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text="Thumbnail Saved ✅ This Is Permanent",
            reply_to_message_id=update.message_id
        )

# Deletes thumbnail
@Client.on_message(filters.command(["del"]))
async def del_thumbnail(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    
    try:
        await sql.del_thumb(update.from_user.id) 
    except:
        pass
    try:
        os.remove(thumb_image_path)
    except:
        pass

    await bot.send_message(
        chat_id=update.chat.id,
        text="Thumbnail cleared succesfully!",
        reply_to_message_id=update.message_id
    )

# Show Thumbnail
@Client.on_message(filters.command(["show"]))
async def show_thumbnail(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        mes = await sql.thumb(update.from_user.id)
        if mes != None:
            m = await bot.get_messages(update.chat.id, mes.msg_id)
            await m.download(file_name=thumb_image_path)
            thumb_image_path = thumb_image_path
        else:
            thumb_image_path = None    
    
    if thumb_image_path is not None:
        try:
            await bot.send_photo(
                chat_id=update.chat.id,
                photo=thumb_image_path,
                reply_to_message_id=update.message_id
            )
        except:
            pass
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text="No thumbnails found!",
            reply_to_message_id=update.message_id
        )