import os
import sys
import time
import asyncio
import logging
import datetime
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from helper.database import db
from Krito import pbot, ADMIN, LOG_CHANNEL, BOT_UPTIME

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ERROR_LOG_PATH = 'error.log'
NEKOBIN_API_ENDPOINT = 'https://nekobin.com/api/documents'

@pbot.on_message(filters.command(["stats", "status"]))
async def get_stats(bot, message):
    if message.from_user.id not in ADMIN:
        await message.reply_text("You are not authorized to use this command.", reply_to_message_id=message.id)
        return

    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - BOT_UPTIME))    
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇssɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟs.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")

@pbot.on_message(filters.private & filters.command("restart"))
async def restart_bot(b, m):
    if m.from_user.id not in ADMIN:
        await message.reply_text("You are not authorized to use this command.", reply_to_message_id=m.id)
        return
    await m.reply_text("🔄__Restarting...__")
    os.execl(sys.executable, sys.executable, *sys.argv)

@pbot.on_message(filters.command("broadcast") & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    if message.from_user.id not in ADMIN:
        await message.reply_text("You are not authorized to use this command.", reply_to_message_id=message.id)
        return
    await bot.send_message(LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} has started the Broadcast......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ.....!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
            if sts == 400:
                await db.delete_user(user['_id'])
                done += 1
                if not done % 20:
                    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
                    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
                    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
                    
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500

@pbot.on_message(filters.command('paste'))
async def paste_command(client, m):
    try:
        # Read the last 100 lines from the error.log file
        with open(ERROR_LOG_PATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()[-100:]
        log_text = ''.join(lines)
        
        print(f"Log Text: {log_text}")  # Print log text for debugging
        
        process = subprocess.Popen(['curl', '--data-binary', '@-', 'https://nekobin.com'], 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        nekobin_url = process.communicate(input=log_text.encode())[0].decode().strip()
        
        print(f"Nekobin URL: {nekobin_url}")  # Print Nekobin URL for debugging
        
        # Reply with the log text and inline button containing the Nekobin URL
        await m.reply_text("Here is your log text. Click the button for the Nekobin URL.", 
                           reply_markup=InlineKeyboardMarkup(
                               [[InlineKeyboardButton("Nekobin URL", url=nekobin_url)]]
                           ))
    except Exception as e:
        print(f"Error occurred: {e}")  # Print the error for debugging
        await m.reply_text(f"An error occurred: {e}")
        
@pbot.on_message(filters.private & filters.command('clear_status'))
async def clear_status_command(client, message):
    try:
        if message.from_user.id not in ADMIN:
            await message.reply_text("You are not authorized to use this command.", reply_to_message_id=message.id)
            return

        given_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True
        )

        async for user_data in db.get_users_with_chat_ids():
            user_id = user_data['_id']
            chat_id = user_data['chat_id']
            try:
                bot_member = await client.get_chat_member(chat_id, client.me.id)
                user_member = await client.get_chat_member(chat_id, user_id)
            except Exception as e:
                await db.delete_chat_id(user_id, chat_id)
                continue
            if (bot_member.status not in ("administrator", "creator") or
               bot_member.permissions != given_permissions or
               user_member.status not in ("administrator", "creator")):
                await db.update_chat_id(user_id, chat_id, True)
            else:
                await db.delete_chat_id(user_id, chat_id)
        response = "Admin statuses cleared from the database."
        await message.reply_text(response, reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
