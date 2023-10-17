import os
import logging
import sys
import re
import time
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')

logging.basicConfig(level=logging.DEBUG, filename='error.log')
LOGS = logging.getLogger("RenameBot")
LOGS.setLevel(level=logging.DEBUG)

# -------------------------------VARS-----------------------------------------
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '2009088107').split()]
API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6202042878:AAEyVJeHHOgc5-s6h3IArLUOoS7kIBRl-xU")
BOT_NAME = os.environ.get("BOT_NAME", "ya_typobot")
BOT_UPTIME = time.time()
DB_NAME = os.environ.get("DB_NAME", "Refun")
DB_URL = os.environ.get("DB_URL", "mongodb+srv://Movieh:movieh@cluster0.0nyllpw.mongodb.net/?retryWrites=true&w=majority")
FORCE_SUB = os.environ.get("FORCE_SUB", "kirigayaakash")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1001682783965))
TOKEN_TIMEOUT = int(os.environ.get("TOKEN_TIMEOUT", 86400))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))

Text = os.environ.get("Text", "https://t.me/beluga0_01/1517")
Text1 = os.environ.get("Text1", "https://t.me/beluga0_01/1516")
Text2 = os.environ.get("Text2", "https://t.me/beluga0_01/1518")
Text3 = os.environ.get("Text3", "https://t.me/beluga0_01/1519")
# -------------------------------USER----------------------------------------
SESSION_STRING = os.environ.get("SESSION_STRING", "BQGBULgAHPuTHhS9431uNmWB-mmCdnIixN4Yhhsmly07p8PjyG9yyvzd2ooioT97ay7v5soM21Lahgdh2x8qk3FhDSoC2ZhBBp0qMnanneTUhnVdKoBaejwPuMXykZTS0_Tm4LuQDKtXRKBkrrUdCmjKBhaXY9MN1Ah4dAJr01Ed8Im3Ojs3SRprNT6VfJ3B5h1U0cAtah9f4ddcugmwn2V-7iY26nJy8FmlKJJvN2WsXObKwt5i4IYkRsRgP3nnxUsxNXjTBl1RKndBU_hP_TT_pKcrEbMT4lhljQKEc8bLF_qYQ3ceafCHJwqcAmiaiZjHlAq16kUWwq8o_1NdF40kLqh5owAAAAFF4ZRqAA")
# -------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/ .").split()
UTRIGGERS = os.environ.get("TRIGGERS", ".").split()
plugins = dict(root="plugins")

# ------------------------------CONNECTION------------------------------------
if BOT_TOKEN is not None:
    try:
        pbot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
        LOGS.debug("❤️ PBot Connected")
        pbot.start()
    except Exception as e:
        LOGS.debug('😞 Error While Connecting To pBot')
        LOGS.exception(e)
        sys.exit()

if isinstance(SESSION_STRING, str) and SESSION_STRING != "None":
    try:
        ubot = Client("Chizuru", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
        LOGS.debug("❤️ UBot Connected")
    except Exception as e:
        LOGS.debug('😞 Error While Connecting To uBot')
        LOGS.exception(e)
        sys.exit()
            
