import time

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message 
from pyrogram import Client, filters

from bot import *

START_TEXT = '''
Hey <b>{}</b> 
I am one of the creations of <b>Retrogini</b>
Just send me file and I'll rename it!
Thumbnail support also available

» <b>Uptime:</b> <code>{}</code>
'''

HELP_TEXT = '''
It's not that complicated 😅

<b>Thumbnail Support</b>
Send me any pic to save it as a thumbnail!

<b>Rename</b>
Send any file 
Send me the name that you want to rename as
If any Thumbnail is saved I will send the renamed file with thumbnail
Else as a normal file'''

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@Client.on_message(filters.command(["start"], prefixes=["/", ".", "?"]))
async def start(_, message):  
    uptime = get_readable_time((time.time() - START_TIME))
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention, uptime),
        reply_markup=InlineKeyboardMarkup(

            [
                [
                    InlineKeyboardButton(
                        text="Support",
                        url="https://t.me/RetroginiBots",
                    ),

                    InlineKeyboardButton(
                        text="Source",
                        url="https://github.com/Kazama009/Rename-Bot-Retrogini",
                    ),
                ],
            ],
        ),
    )   

@Client.on_message(filters.command(["help"], prefixes=["/", ".", "?"]))
async def help(_, message):  
    await message.reply_text(
        HELP_TEXT
    )