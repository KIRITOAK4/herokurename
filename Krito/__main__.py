import logging
import asyncio
from datetime import datetime
from pytz import timezone
from aiohttp import web
from route import web_server
from pyrogram import __version__
from Krito import pbot, ubot, WEBHOOK, ADMIN, LOG_CHANNEL

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main():
    try:
        await pbot.start()
        await ubot.start()

        me = await pbot.get_me()
        logger.info(f"{me.first_name} Is Started.....✨️")
        
        if WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()

        for id in ADMIN:
            try:
                await pbot.send_message(id, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except Exception as e:
                logger.debug(f"Failed to send message to admin {id}: {e}")

        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await pbot.send_message(LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__}`</b>")
            except Exception as e:
                logger.debug(f"Failed to send message to log channel: {e}")

        await asyncio.sleep(60)
    except Exception as main_error:
        logger.error(f"An error occurred in main(): {main_error}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
