from pyrogram import filters
from pyrogram.enums import ParseMode
from Krito import pbot
from helper.database import db

@pbot.on_message(filters.command("get_info") & filters.private)
async def get_info_command(client, message):
    user_id = message.from_user.id

    # Initialize response message base
    response_message_base = f"**👩‍💻User ID**: {user_id}\n\n"

    # Attempt to fetch user-specific information from the database
    try:
        template = await db.get_template(user_id)
        upload_type = await db.get_uploadtype(user_id)
        chat_id = await db.get_chat_id(user_id)
        thumbnail = await db.get_thumbnail(user_id)
        exten = await db.get_exten(user_id)

        # Building the response message with Markdown formatting
        response_message = f"{response_message_base}**🗺Template**: {template}\n\n**🎬Upload Type**: {upload_type}\n\n**🎛Extension**: {exten}"

        if chat_id:
            response_message += f"\n\n**🏡Chat ID**: {chat_id}"
        else:
            response_message += "\n\n__**You Don't have Chat ID**__"

        if thumbnail:
            # If thumbnail exists, send the message with the thumbnail and formatted caption in Markdown
            response_message += "\n\n__**For changes use /set_temp, /set_upload, /set_chatid, /set_exten**__"
            await message.reply_photo(photo=thumbnail, caption=response_message, parse_mode="Markdown")
        else:
            # If no thumbnail, send a placeholder message first
            placeholder = await message.reply("Fetching...")
            # Then edit the placeholder message with the detailed information
            response_message += "\n\n__**You Don't have Thumbnail**__\n\n__**For changes use /set_temp, /set_upload, /set_chatid, /set_exten**__"
            await placeholder.edit_text(response_message, parse_mode=ParseMode.Markdown)

    except Exception as e:
        # Print the error to the console for debugging
        print(f"An error occurred: {str(e)}")

        # Handle any errors that occur during the database fetch or message sending
        await message.reply(f"An error occurred: {str(e)}", parse_mode=ParseMode.Markdown)
