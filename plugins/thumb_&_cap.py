from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, ChatPermissions
from helper.database import db
from helper.token import none_admin_utils
from Krito import pbot, ADMIN
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
        if not str(chat_id).startswith('-100'):
            raise ValueError("Chat ID must start with -100")
    except ValueError:
        return await message.reply_text("Invalid chat ID. Please provide a valid integer. And it starts with -100", reply_to_message_id=message.message_id)
    bot_member = await client.get_chat_member(chat_id, client.me.id)
    if not bot_member.status in ("administrator", "creator"):
        return await message.reply_text("I need to be an admin with all permission in the specified chat to set the chat ID.", reply_to_message_id=message.message_id)
    user_member = await client.get_chat_member(chat_id, message.from_user.id)
    if not user_member.status in ("administrator", "creator"):
        return await message.reply_text("You need to be admin in the specified chat to set the chat ID.", reply_to_message_id=message.message_id)
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True
    )
    try:
        await asyncio.wait_for(client.restrict_chat_member(chat_id, client.me.id, permissions), timeout=60)
    except asyncio.TimeoutError:
        await client.leave_chat(chat_id)
        await db.set_chat_id(message.from_user.id, None)
        return await message.reply_text("❌️ Bot was not made an admin in the specified chat within 1 minute. The bot has left the channel, and the chat ID has been set to None.", reply_to_message_id=message.message_id)
    except Exception as e:
        return await message.reply_text(f"Error: {e}", reply_to_message_id=message.message_id)

    await db.set_chat_id(message.from_user.id, chat_id)
    await message.reply_text(f"✅ Chat ID set to: {chat_id}", reply_to_message_id=message.message_id)

@pbot.on_message(filters.private & filters.command('get_chatid'))
async def get_chatid_command(client, message):
    chat_id = await db.get_chat_id(message.from_user.id)
    if chat_id:
        await message.reply_text(f"Your Chat ID: {chat_id}", reply_to_message_id=message.message_id)
    else:
        await message.reply_text("Chat ID not set. Use /set_chatid {chat_id} to set your chat ID.", reply_to_message_id=message.message_id)

@pbot.on_message(filters.private & filters.command('del_chatid'))
async def delete_chatid_command(client, message):
    try:
        await db.delete_chat_id(message.from_user.id)
        print("Chat ID deleted from the database.")
        await message.reply_text("❌️ Chat ID deleted. You can set it again using /set_chatid {chat_id}.", reply_to_message_id=message.message_id)
        print("Reply sent.")
    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(f"Error: {e}")

@pbot.on_message(filters.private & filters.command('clear_status'))
async def clear_status_command(client, message):
    if message.from_user.id not in ADMIN:
        await message.reply_text("You are not authorized to use this command.")
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

    users_with_chat_ids = await db.get_users_with_chat_ids()
    for user_id, chat_id in users_with_chat_ids.items():
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
    await message.reply_text(response, reply_to_message_id=message.message_id)
