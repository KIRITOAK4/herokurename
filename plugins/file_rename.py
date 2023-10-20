from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from helper.token import none_admin_utils
from asyncio import sleep
from PIL import Image
import os, time
from Krito import ubot, pbot
import asyncio

@pbot.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    try:
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
            if ubot.is_connected:
                # Process the file if ubot is active and file size is between 1.9GB and 3.2GB
                await message.reply_text(
                    text=f"**__Please Enter New File Name...__**\n\n**Old File Name** :- `{filename}`",
                    reply_to_message_id=message.id,
                    reply_markup=ForceReply(True)
                )
                await sleep(30)
            else:
                await message.reply_text("Sorry, sir. +4gb not active to process it.")
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
        pass

@pbot.on_message(filters.private & filters.reply)
async def refunc(client, message):
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

        button = [[InlineKeyboardButton("📁 Document", callback_data="upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Video", callback_data="upload_video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Audio", callback_data="upload_audio")])
        await message.reply(
            text=f"**Select The Output File Type**\n**• File Name :-**```{new_name}```",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )

@pbot.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message

    ms = await update.message.edit("Trying To Downloading....")
    try:
        path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", ms, time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds

    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Your Caption Error Except Keyword Argument ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    if media.thumbs or c_thumb:
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    
    value = 1.9 * 1024 * 1024 * 1024  # 1.9 GB in bytes
    if file.file_size > value:
        # If file size is greater than 1.9 GB, use ubot
        fupload = int(-1001682783965) 
        client = ubot
    else:
        # If file size is less than or equal to 1.9 GB, use pbot
        fupload = update.message.chat.id
        client = pbot

    await ms.edit("Trying To Uploading....")
    type = update.data.split("_")[1]

    try:
        if type == "document":
            suc = await client.send_document(
                chat_id=fupload,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )
        elif type == "video":
            suc = await client.send_video(
                chat_id=fupload,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )
        elif type == "audio":
            suc = await client.send_audio(
                chat_id=fupload,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time())
            )

        if client == ubot:
            await pbot.copy_message(
                chat_id=update.message.chat.id,
                from_chat_id=suc.chat.id,
                message_id=suc.message_id
            )
    except FloodWait as e:
        await asyncio.sleep(7)  # Sleep for the required time in seconds
    except Exception as e:
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return await ms.edit(f" Error {e}")

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)
