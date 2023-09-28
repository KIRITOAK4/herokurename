import glob
from pathlib import Path
import logging
from Krito import pbot, ubot
import random
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


pbot.start()
ubot.start()
loop = asyncio.get_event_loop()
loop.run_forever()    
