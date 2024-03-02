from pyrogram import filters
from pyrogram import Client
from telegraph import Telegraph
from Krito import pbot
from helper.database import db

# Assuming telegraph_image_paste function is defined in the same file
async def image_paste(filepath: str) -> str:
    telegraph = Telegraph(domain="graph.org")
    try:
        image_url = await telegraph.upload_file(filepath)
        return "https://graph.org/" + image_url[0]["src"]
    except Exception as error:
        print(f"Error uploading image to Telegraph: {error}")
        return "Something went wrong while posting the image."

@pbot.on_message(filters.command("get_info") & filters.private)
async def get_info_command(client, message):
    user_id = message.from_user.id

    # Get user-specific information from the database
    template = await db.get_template(user_id)
    upload_type = await db.get_uploadtype(user_id)
    chat_id = await db.get_chat_id(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    exten = await db.get_exten(user_id)

    response_message = f"👩‍💻User ID: {user_id}\n🗺Template: {template}\n🎬Upload Type: {upload_type}\n🎛Extension: {exten}"

    if chat_id:
        response_message += f"\n🏡Chat ID: {chat_id}"
    else:
        response_message += "\n__**You Don't have Chat ID**__"

    if thumbnail:
        graph_url = await image_paste(thumbnail)
        response_message += f"\n🗳Thumbnail: [View Thumbnail]({graph_url})"
    else:
        response_message += "\n__**You Don't have Thumbnail**__"

    response_message += "\n\n**For changes use /set_temp, /set_upload, /set_chatid"
    await message.reply(response_message)
