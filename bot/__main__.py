from bot import *

from pyrogram import Client

def main():

    LOGGER.info("Rename Bot - Retrogini has successfully started")

    plugins = dict(root="bot/plugins")

    pyro = Client(
        "Rename-Bot-Retrogini",
        bot_token=TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    
    pyro.run()

main()
