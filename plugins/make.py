
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server

import sys 


def create_ubot(session_string):
    if session_string == "None":
        print(session_string)
        print("Invalid session string.")
        return None
    try:
        ubot = Client(
            name="renamer",
            api_id=Config.API_ID,
            bot_token=Config.BOT_TOKEN,
            session_string=session_string,
            api_hash=Config.API_HASH,            
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        print("❤️ UBot Connected")
        return ubot
    except Exception as e:
        print('😞 Error While Connecting To Bot')  
        print(e)
        sys.exit()

if __name__ == "__main__":
    ubot = create_ubot(Config.SESSION_STRING) 
    # print(ubot)
    # if ubot:
    #     try:
    #         ubot.run()   
    #     except Exception as e:
    #         print(e)
