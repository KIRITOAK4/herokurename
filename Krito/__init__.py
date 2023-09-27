import os
import logging
import time
import sys

from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__, compose
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
from make import create_ubot
import asyncio

# -------------------------------LIST----------------------------------------
# -------------------------------USER----------------------------------------
SESSION_STRING = os.environ.get("SESSION_STRING", Config.SESSION_STRING)
# -------------------------------VARS-----------------------------------------
ADMIN = os.environ.get("ADMIN", Config.ADMIN)
API_ID = int(os.environ.get("API_ID", Config.API_ID))
API_HASH = os.environ.get("API_HASH", Config.API_HASH)
BOT_TOKEN = os.environ.get("BOT_TOKEN", Config.BOT_TOKEN)
BOT_NAME = os.environ.get("BOT_NAME", Config.BOT_NAME)
BOT_UPTIME = os.environ.get("BOT_UPTIME", Config.BOT_UPTIME)
DB_NAME = os.environ.get("DB_NAME", Config.DB_NAME)
DB_URL = os.environ.get("DB_URL", Config.DB_URL)
FORCE_SUB = os.environ.get("FORCE_SUB", Config.FORCE_SUB)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", Config.LOG_CHANNEL))
Text = os.environ.get("Text", Config.Text)
Text1 = os.environ.get("Text1", Config.Text1)
Text2 = os.environ.get("Text2", Config.Text2)
Text3 = os.environ.get("Text3", Config.Text3)
TOKEN_TIMEOUT = int(os.environ.get("TOKEN_TIMEOUT", Config.TOKEN_TIMEOUT))
WEBHOOK = os.environ.get("WEBHOOK", Config.WEBHOOK)

# -------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/").split()
UTRIGGERS = os.environ.get("TRIGGERS", ".").split()
plugins = dict(root="plugins")

# ------------------------------CONNECTION------------------------------------
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

# -------------------------------RENAMEBOT CLASS--------------------------------
class RenameBot:
    LOGGER = LOGS
    shorteners_list = []

    def __init__(self):
        if os.path.exists('shorteners.txt'):
            with open('shorteners.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    temp = line.strip().split()
                    if len(temp) == 2:
                        self.shorteners_list.append({'domain': temp[0], 'api_key': temp[1]})
