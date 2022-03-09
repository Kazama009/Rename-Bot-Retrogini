import time

from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import escape_markdown

from bot import START_TIME, dispatcher, updater, LOGGER

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

def start(update:Update, context:CallbackContext):
    uptime = get_readable_time((time.time() - START_TIME))
    name = update.effective_user.first_name

    update._effective_message.reply_text(
        START_TEXT.format(
            escape_markdown(name), escape_markdown(uptime)
        ),

        parse_mode=ParseMode.HTML,
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
    ),   


def help(update:Update, context:CallbackContext):
    update.effective_message.reply_text(
        HELP_TEXT,
        parse_mode=ParseMode.HTML
    )

def main():

    # Handlers
    START_HANDLER = CommandHandler("start", start)
    HELP_HANDLER = CommandHandler("help", help)

    # Dispatchers
    dispatcher.add_handler(START_HANDLER)
    dispatcher.add_handler(HELP_HANDLER)

    LOGGER.info("Rename Bot - Retrogini has successfully started")
    updater.start_polling(timeout=15, read_latency=4)

main()