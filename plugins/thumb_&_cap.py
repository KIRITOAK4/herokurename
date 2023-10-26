from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, ChatPermissions
from helper.database import db
from helper.token import none_admin_utils
from Krito import pbot
from time import time
import asyncio
import traceback
import math

users_data = {}

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
    await mkn.edit("✅️ __**Thumbnail Saved**__", reply_to_message_id=message.id)

@pbot.on_message(filters.private & filters.command('set_chatid'))
async def set_chatid_command(client, message):
    try:
        chat_id = int(message.text.split(" ", 1)[1])
        if not str(chat_id).startswith('-100'):
            raise ValueError("Chat ID must start with -100")

        users_data[message.from_user.id] = {
            "verified": False
        }

        await db.add_chat_id(message.from_user.id, chat_id)
        await message.reply_text("Chat ID has been set successfully. Please use /verify command within 60 seconds.", reply_to_message_id=message.id)
        await asyncio.sleep(60)

        if not users_data[message.from_user.id]["verified"]:
            await client.leave_chat(chat_id)
            del users_data[message.from_user.id]
            await db.delete_chat_id(message.from_user.id)
            await message.reply_text("You didn't use /verify command in time. Chat ID has been unset, and the bot left the channel.", reply_to_message_id=message.id)

    except (ValueError, IndexError):
        error_message = "Invalid command. Use /set_chatid {chat_id}"
        return await message.reply_text(error_message, reply_to_message_id=message.id)

    except Exception as e:
        error_message = f"Please add me to the chat with admin permission to send messages and media: {e}."
        return await message.reply_text(error_message, reply_to_message_id=message.id)

@pbot.on_message(filters.private & filters.command('verify'))
async def verify_command(client, message):
    try:
        print("Starting verification process...")
        
        if message.from_user.id in users_data and not users_data[message.from_user.id]["verified"]:
            print("User is not verified yet. Getting stored chat ID...")
            # Get the stored chat ID for the user from the database (assuming db.get_chat_id exists)
            chat_id = await db.get_chat_id(message.from_user.id)
            print(f"Chat ID retrieved: {chat_id}")
            
            try:
                print("Getting invite link and checking bot and user status...")
                # Get invite link for the chat ID
                invite_link = await client.export_chat_invite_link(chat_id)
                print(f"Invite link retrieved: {invite_link}")
                
                # Check bot and user status using invite link
                chat = await client.get_chat(invite_link)
                bot_member = await client.get_chat_member(chat.id, client.me.id)
                user_member = await client.get_chat_member(chat.id, message.from_user.id)
                print("Membership status retrieved.")
                
                # Get bot's permissions
                bot_permissions = bot_member.permissions
                print(f"Bot permission: {bot_permissions}")
                if bot_member.status in ("administrator", "creator") and user_member.status in ("member", "administrator", "creator"):
                    if bot_permissions.can_send_media_messages and bot_permissions.can_send_messages:
                        users_data[message.from_user.id]["verified"] = True
                        print("Verification successful! User is now verified.")
                        await message.reply_text("Verification successful! You are now verified.")
                    else:
                        print("Verification failed: Bot does not have permission to send media or captions.")
                        await message.reply_text("Bot does not have necessary permissions to send media or captions.")
                else:
                    print("Verification failed: Bot must be admin/creator and user must be member/admin/creator in the specified channel.")
                    await message.reply_text("Verification failed: Bot must be admin/creator and user must be member/admin/creator in the specified channel.")
            except Exception as e:
                print(f"Verification failed: Error occurred - {e}")
                await message.reply_text(f"Error: {e}")
        else:
            print("User is already verified or chat ID is not set.")
            await message.reply_text("You need to set the chat ID using /set_chatid first or you are already verified.")
    except Exception as e:
        print(f"An error occurred while using verify command: {e}")
        await message.reply_text(f"An error occurred while using verify command: {e}")

        chat_id = await db.get_chat_id(message.from_user.id)
        if chat_id:
            await message.reply_text(f"Your Chat ID: {chat_id}")
        else:
            await message.reply_text("Chat ID not set. Use /set_chatid {chat_id} to set your chat ID.", reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@pbot.on_message(filters.private & filters.command('del_chatid'))
async def delete_chatid_command(client, message):
    try:
        await db.delete_chat_id(message.from_user.id)
        await message.reply_text("❌️ Chat ID deleted. You can set it again using /set_chatid {chat_id}.", reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
