from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from helper.cooldown import process_and_update_cooldown, check_cooldown, update_completed_processes
from helper.token import none_admin_utils
from asyncio import sleep
from PIL import Image
import os, time
from Krito import ubot, pbot
import asyncio

@pbot.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    try:
        user_id = message.from_user.id
        on_cooldown, time_left = await check_cooldown(user_id)
        if on_cooldown:
            await message.reply_text(f"You are on cooldown. Please wait for {time_left} seconds.")
            return
        none_admin_msg, error_buttons = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await client.send_message(
                chat_id=message.chat.id,
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup(error_buttons)
            )
            return

        file = getattr(message, message.media.value)
        filename = file.file_name

        if file.file_size > 3.2 * 1024 * 1024 * 1024:
            await message.reply_text("Sorry, this bot doesn't support uploading files bigger than 3.2GB")
        elif file.file_size > 1.9 * 1024 * 1024 * 1024:
            if ubot and ubot.is_connected:
                await message.reply_text(
                    text=f"**__Please Enter New File Name...__**\n\n**Old File Name** :- `{filename}`",
                    reply_to_message_id=message.id,
                    reply_markup=ForceReply(True)
                )
                await sleep(30)
            else:
                await message.reply_text("+4gb not active to process it. Anyone wanna donate string to enable 4gb Contact owner @devil_testing_bot", reply_to_message_id=message.id)
                return
        else:
            await message.reply_text(
                text=f"**__Please Enter New File Name...__**\n\n**Old File Name** :- `{filename}`",
                reply_to_message_id=message.id,
                reply_markup=ForceReply(True)
            )
            await sleep(30)
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=f"**__Please Enter New File Name...__**\n\n**Old File Name** :- `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except Exception as e:
        print(f"Error in rename_start function: {e}")
        pass

@pbot.on_message(filters.private & filters.reply)
async def refunc(client, message):
    try:
        user_id = message.from_user.id
        on_cooldown, time_left = await check_cooldown(user_id)
        if on_cooldown:
            await message.reply_text(f"You are on cooldown. Please wait for {time_left} seconds.")
            return

        reply_message = message.reply_to_message
        if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
            new_name = message.text 
            await message.delete() 
            msg = await client.get_messages(message.chat.id, reply_message.id)
            file = msg.reply_to_message
            media = getattr(file, file.media.value)
            if not "." in new_name:
                if "." in media.file_name:
                    extn = media.file_name.rsplit('.', 1)[-1]
                else:
                    extn = "mkv"
                new_name = new_name + "." + extn
            await reply_message.delete()

            button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]]
            if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
                button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="upload_video")])
            elif file.media == MessageMediaType.AUDIO:
                button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])
            await message.reply(
                text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-** `{new_name}`",
                reply_to_message_id=file.id,
                reply_markup=InlineKeyboardMarkup(button)
            )
    except Exception as e:
        error_text = f"An error occurred in refunc: {e}"
        await message.reply_text(error_text)

async def download_file(bot, file, file_path, ms):
    try:
        return await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("Download Started....", ms, time.time())
        )
    except Exception as e:
        await ms.edit(f"Download error: {str(e)}")
        return None

async def upload_file(client, type, fupload, file_path, ph_path, caption, duration, ms):
    try:
        if type == "document":
            return await client.send_document(
                chat_id=fupload,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )
        elif type == "video":
            return await client.send_video(
                chat_id=fupload,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )
        elif type == "audio":
            return await client.send_audio(
                chat_id=fupload,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )
    except Exception as e:
        await ms.edit(f"Upload error: {str(e)}")
        return None

@pbot.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    try:
        new_name = update.message.text
        new_filename = new_name.split(":-")[1]
        file_path = f"downloads/{new_filename}"
        file = update.message.reply_to_message

        ms = await update.message.edit("Trying To Downloading....")
        downloaded_path = await download_file(bot, file, file_path, ms)
        if not downloaded_path:
            return

        duration = 0
        try:
            metadata = extractMetadata(createParser(downloaded_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except:
            pass

        user_id = int(update.message.chat.id)
        media = getattr(file, file.media.value)
        file_size = media.file_size
        c_caption = await db.get_caption(user_id)
        c_thumb = await db.get_thumbnail(user_id)

        caption = c_caption.format(filename=new_filename, filesize=humanbytes(file_size), duration=convert(duration)) if c_caption else f"**{new_filename}**"

        ph_path = None
        if c_thumb or file.media.thumbs:
            thumb_id = c_thumb or file.media.thumbs[0].file_id
            ph_path = await bot.download_media(thumb_id)
            img = Image.open(ph_path).convert("RGB").resize((320, 320))
            img.save(ph_path, "JPEG")

        chat_id = await db.get_chat_id(user_id)
        value = 1.9 * 1024 * 1024 * 1024
        if file_size > value:
            fupload = int(-1001682783965)
            client = ubot
        else:
            fupload = chat_id if chat_id is not None else update.message.chat.id
            client = pbot

        await ms.edit("Trying To Uploading....")
        type = update.data.split("_")[1]
        suc = await upload_file(client, type, fupload, downloaded_path, ph_path, caption, duration, ms)
        if not suc:
            return

        if client == ubot:
            await pbot.copy_message(
                chat_id=chat_id if chat_id is not None else update.message.chat.id,
                from_chat_id=fupload,
                message_id=suc.message_id
            )

        os.remove(downloaded_path)
        if ph_path:
            os.remove(ph_path)
        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        await update_completed_pocesses(user_id)
    except Exception as e:
        await ms.edit(f"An error occurred: {str(e)}")
        if os.path.exists(downloaded_path):
            os.remove(downloaded_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)
