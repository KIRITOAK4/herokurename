from pyrogram import filters
from Krito import pbot
from helper.database import db

@pbot.on_message(filters.command("get_info") & filters.private)
async def get_info_command(client, message):
    user_id = message.from_user.id

    # Get user-specific information from the database
    template = await db.get_template(user_id)
    upload_type = await db.get_uploadtype(user_id)
    chat_id = await db.get_chat_id(user_id)
    thumbnail = await db.get_thumb(user_id)

    response_message = f"👩‍💻User ID: {user_id}\n🗺Template: {template}\n🎬Upload Type: {upload_type}\n🏡Chat ID: {chat_id}\n\n**For changes use /set_temp, /set_upload, /set_chatid"

    # Send the response message
    await message.reply(response_message)
