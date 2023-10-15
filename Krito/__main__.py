import logging
import asyncio
from datetime import datetime
from pytz import timezone
from aiohttp import web
from route import web_server
from pyrogram import __version__
from Krito import pbot, ubot, WEBHOOK, ADMIN, LOG_CHANNEL

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

pbot.start()
ubot.start()
loop = asyncio.get_event_loop()
loop.run_forever()    
