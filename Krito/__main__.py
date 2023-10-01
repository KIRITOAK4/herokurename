
import asyncio
from datetime import datetime
from pytz import timezone
from aiohttp import web
from Krito import pbot, create_ubot, WEBHOOK, BOT_UPTIME, ADMIN, LOG_CHANNEL
from route import web_server
from pyrogram import __version__

pbot.start()

success = create_ubot()  # Attempt to create ubot
if success != "None":
    ubot = success
    ubot.start()
try:
  pbot.send_message(LOG_CHANNEL, text='Bot Started')
except:
    pass

loop = asyncio.get_event_loop() 
loop.run_forever()
