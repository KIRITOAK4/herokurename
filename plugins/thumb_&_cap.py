from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from helper.database import db
from helper.token import none_admin_utils
from Krito import pbot
from time import time
import asyncio
import traceback
import math

@pbot.on_message(filters.private & filters.command("ping"))
async def ping(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    start = time()
    sent_message = await message.reply("Pinging...")
    await asyncio.sleep(5)
    end = time()
    duration = (end - start) * 1000
    await sent_message.edit(f"Pong! RTT: {duration:.2f} ms")

@pbot.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    if len(message.command) == 1:
        return await message.reply_text("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ: `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`**")

    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")

@pbot.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    caption = await db.get_caption(message.from_user.id)
    if not caption:
        return await message.reply_text("__**😔 You Don't Have Any Caption**__")

    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("__**❌️ Caption Deleted**__")

@pbot.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    caption = await db.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"**Your Caption:-**\n\n`{caption}`")
    else:
        await message.reply_text("__**😔 You Don't Have Any Caption**__")

@pbot.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("😔 __**You Don't Have Any Thumbnail**__")

@pbot.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return

    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("❌️ __**Thumbnail Deleted**__")

@pbot.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
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
    except Exception as e:
        traceback.print_exc()
        return
    mkn = await message.reply_text("Please Wait ...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)
    await mkn.edit("✅️ __**Thumbnail Saved**__")

@pbot.on_message(filters.private & filters.command('set_chatid'))
async def set_chatid_command(client, message):
    if len(message.command) != 2:
        return await message.reply_text("Invalid command. Use /set_chatid {chat_id}", reply_to_message_id=message.message_id)

    try:
        chat_id = int(message.text.split(" ", 1)[1])
    except ValueError:
        return await message.reply_text("Invalid chat ID. Please provide a valid integer.", reply_to_message_id=message.message_id)

    await db.set_chat_id(message.from_user.id, chat_id)
    await message.reply_text(f"✅ Chat ID set to: {chat_id}", reply_to_message_id=message.message_id)

@pbot.on_message(filters.private & filters.command('get_chatid'))
async def get_chat_id_command(client, message):
    chat_id = await db.get_chatid(message.from_user.id)
    if chat_id is not None:
        await message.reply_text(f"Your Chat ID: {chat_id}", reply_to_message_id=message.message_id)
    else:
        await message.reply_text("Chat ID not set. Use /set_chatid {chat_id} to set your chat ID.", reply_to_message_id=message.message_id)

@pbot.on_message(filters.private & filters.command('del_chatid'))
async def delete_chat_id_command(client, message):
    await db.delete_chatid(message.from_user.id)
    await message.reply_text("❌️ Chat ID deleted. You can set it again using /set_chatid {chat_id}.", reply_to_message_id=message.message_id)

