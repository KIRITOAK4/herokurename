from helper.database import db
from Krito import pbot
from pyrogram.enums import ChatMemberStatus
from pyrogram import Client, Message
users_data = {}

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

    except (ValueError, IndexError) as e:
        error_message = f"Error: {e}"
        await message.reply_text(error_message, reply_to_message_id=message.id)
    except Exception as e:
        error_message = f"Error: {e}"
        await message.reply_text(error_message, reply_to_message_id=message.id)
    finally:
        try:
            if not users_data[message.from_user.id]["verified"]:
                del users_data[message.from_user.id]
                await db.delete_chat_id(message.from_user.id)
        except Exception as e:
            error_message = f"Error: {e}"
            await message.reply_text(error_message, reply_to_message_id=message.id)

@pbot.on_message(filters.private & filters.command('verify'))
async def verify_command(client, message):
    try:
        if message.from_user.id in users_data and not users_data[message.from_user.id]["verified"]:
            chat_id = await db.get_chat_id(message.from_user.id)
            try:
                bot_member = await client.get_chat_member(chat_id, "me")
                user_member = await client.get_chat_member(chat_id, message.from_user.id)

                if bot_member.status == ChatMemberStatus.ADMINISTRATOR and (user_member.status == ChatMemberStatus.ADMINISTRATOR or user_member.status == ChatMemberStatus.OWNER):
                    users_data[message.from_user.id]["verified"] = True
                    await message.reply_text("Verification successful! You are now verified.")
                else:
                    await message.reply_text("Bot or user does not have appropriate status in the specified chat.")
            except Exception as e:
                await message.reply_text(f"Error: {e}")
        else:
            await message.reply_text("You need to set the chat ID using /set_chatid first or you are already verified.")
    except Exception as e:
        await message.reply_text(f"An error occurred while using verify command: {e}")

@pbot.on_message(filters.private & filters.command('get_chatid'))
async def get_chatid_command(client, message):
    try:
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
