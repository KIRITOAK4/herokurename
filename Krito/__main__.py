import glob
from pathlib import Path
import logging
from Krito import pbot, ubot
import random
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

async def main():
    await pbot.start()
    await ubot.start()
    await asyncio.gather(pbot.idle(), ubot.idle())

if __name__ == "__main__":
    asyncio.run(main())
