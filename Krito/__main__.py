import glob
from pathlib import Path
import logging
from Krito import pbot, ubot, Config
import random
import asyncio
from pyrogram.raw.all import layer
from pyrogram import __version__ , compose
from datetime import datetime
from pytz import timezone
from aiohttp import web
from route import web_server

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

async def start_clients():
    await pbot.start()
    await ubot.start()

async def main():
    await start_clients()

if __name__ == "__main__":
    asyncio.run(main())
    me = await pbot.get_me()
    pbot.mention = me.mention
    pbot.username = me.username  
    pbot.uptime = Config.BOT_UPTIME     
    if Config.WEBHOOK:
        app = web.AppRunner(await web_server())
        await app.setup()       
        await web.TCPSite(app, "0.0.0.0", 8080).start()     
    print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
    for id in Config.ADMIN:
        try: await pbot.send_message(id, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
        except: pass
    if Config.LOG_CHANNEL:
        try:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            await pbot.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")                                
        except:
            print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")
