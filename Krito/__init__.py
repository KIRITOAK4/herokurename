import os
import logging
import time
import sys


logging.basicConfig(level=logging.INFO)

LOGS = logging.getLogger("AnimeBot")
LOGS.setLevel(level=logging.INFO)

from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__ , compose
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
from make import create_ubot
import asyncio

#-------------------------------LIST----------------------------------------
#-------------------------------USER----------------------------------------
SESSION_STRING = os.environ.get("SESSION_STRING",Config.SESSION_STRING)
#-------------------------------VARS-----------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN",Config.BOT_TOKEN)
API_ID = int(os.environ.get("API_ID",Config.API_ID))
API_HASH = os.environ.get("API_HASH",Config.API_HASH)
OWNER = int(os.environ.get("OWNER",1636310615))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL",-1001322925970))
#-------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/").split()
UTRIGGERS = os.environ.get("TRIGGERS", ".").split()
plugins = dict(root="plugins")
#------------------------------CONNECTION------------------------------------
if BOT_TOKEN is not None:
    try:
        pbot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
        LOGS.info("❤️ Bot Connected")
    except Exception as e:
        LOGS.info('😞 Error While Connecting To Bot')    
        print(e)
        sys.exit()            


if SESSION_STRING is not None:
    try:
        ubot = Client("Chizuru", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
        LOGS.info("❤️ UBot Connected")
    except:
        LOGS.info('😞 Error While Connecting To UBot')    
        sys.exit()   
