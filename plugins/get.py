import asyncio
from pyrogram import filters
from pyrogram.enums import ParseMode
from Krito import pbot
from helper.database import db

format_str = '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
┃   **👩‍💻User ID**: {response_message_base}         ┃
┃                                      ┃
┃   **🗺Template**: {template}   ┃
┃                                      ┃
┃   **🎬Upload Type**: {upload_type}    ┃
┃                                      ┃
┃   ** 🎛Extension**: {exten}          ┃
┃                                      ┃
┃   **📮Chat ID**: {chat_id}          ┃
┃                                      ┃
┃   **🏡Thumbnail**: {thumbnail_status}      ┃
┃                                      ┃
┃ For changes use /set_temp, /set_upload, /set_chatid, /set_exten ┃
┃                                      ┃
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
'''

@pbot.on_message(filters.command("get_info") & filters.private)
async def get_info_command(client, message):
    user_id = message.from_user.id

    # Attempt to fetch user-specific information from the database
    try:
        template = await db.get_template(user_id)
        upload_type = await db.get_uploadtype(user_id)
        chat_id = await db.get_chat_id(user_id)
        thumbnail = await db.get_thumbnail(user_id)
        exten = await db.get_exten(user_id)

        # Building the response message with Markdown formatting
        response_message_base = f"**👩‍💻User ID**: {user_id}\n\n"
        thumbnail_status = '✅' if thumbnail else '❌'
        formatted_message = format_str.format(response_message_base=response_message_base, template=template, upload_type=upload_type, exten=exten, chat_id=chat_id, thumbnail_status=thumbnail_status)

        if not chat_id:
            formatted_message = formatted_message.replace('**📮Chat ID**: ', '**📮Chat ID**: ❌__**Chat id is missing**__')

        if thumbnail:
            # If thumbnail exists, send the message with the thumbnail and formatted caption in Markdown
            await message.reply_photo(photo=thumbnail, caption=formatted_message, parse_mode=ParseMode.MARKDOWN)
        else:
            placeholder = await message.reply("Fetching...")
            await asyncio.sleep(2.5)
            await placeholder.edit_text(formatted_message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
