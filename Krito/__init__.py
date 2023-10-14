import os
import logging
import sys
import re
import time
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')

logging.basicConfig(level=logging.INFO, filename='error.log')
LOGS = logging.getLogger("RenameBot")
LOGS.setLevel(level=logging.INFO)

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
SESSION_STRING = os.environ.get("SESSION_STRING","BQGBULgAiW4wQDzETBV_EZLNF_RCeijAf4APdW_HgvvxdKMCEuYVuRTmPlYcor85blc9vcOr3P_8UtLzrSlTe1emlXiyRH7WIPzPJwU5ovFa_WAb_gOrHvmpPG6BJgqIg0BiLcBpkJxLy_1BqW6kv1emin_MFIWEEqPUvY7cdNj2UU07JqP6kcJuwzy41x5Rgtxr12YLWvjdVvS7MeWPDaKjKYmuiFQpEhUMAD4ilklL-PheyIO-Du46ueq-Z5Mqrurx44eLdE5Z0wjr91fMjMz_H5ZjoHoB4W9rWgaxszlBClzkHFVZocB6UwY2-CC6TuYiRdq-q088Mi2nI-cfVSObuOVXDAAAAAFF")
ubot = None

# -------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/ .").split()
UTRIGGERS = os.environ.get("TRIGGERS", ".").split()
plugins = dict(root="plugins")

# ------------------------------CONNECTION------------------------------------
if BOT_TOKEN is not None:
    try:
        pbot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
        LOGS.info("❤️ PBot Connected")
        pbot.start()
    except Exception as e:
        LOGS.info('😞 Error While Connecting To Bot')
        LOGS.exception(e)
        sys.exit()

    if isinstance(SESSION_STRING, str) and SESSION_STRING != "None":
        try:
            LOGS.info("Before creating ubot")
            ubot = Client("Chizuru", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
            LOGS.info("After creating ubot")
            LOGS.info("❤️ UBot Connected")
        except Exception as e:
            LOGS.error(f'Error occurred in connecting UBot: {str(e)}')
            LOGS.exception(e)
            sys.exit()
    else:
        LOGS.error("SESSION_STRING is not provided or set to 'None'. Please provide a valid session string.")
        sys.exit()
