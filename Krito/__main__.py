import logging
import asyncio
from datetime import datetime
from pytz import timezone
from aiohttp import web
from Krito import pbot, ubot, WEBHOOK, BOT_UPTIME, ADMIN, LOG_CHANNEL
from route import web_server
from pyrogram.raw.all import layer
from pyrogram import __version__, compose

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)  # Changed logging level to INFO

async def start_clients():
    await pbot.start()
    await ubot.start()

async def main():
    try:
        await start_clients()
        me = await pbot.get_me()
        pbot.mention = me.mention
        pbot.username = me.username  
        pbot.uptime = BOT_UPTIME     
        if WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8080).start()     
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        for id in ADMIN:
            try: 
                await pbot.send_message(id, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
            except Exception as e:
                print(f"Failed to send message to admin {id}: {e}")
        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await pbot.send_message(LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")                                
            except Exception as e:
                print(f"Failed to send message to log channel: {e}")
    except Exception as e:
        print(f"An error occurred during startup: {e}")

if __name__ == "__main__":
    asyncio.run(main())
   #asyncio.get_event_loop().run_until_complete(main())

