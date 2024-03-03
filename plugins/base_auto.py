import logging
from pyrogram import filters
from Krito import pbot
from helper.database import db
from pyrogram.types import InlineKeyboardMarkup

@pbot.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Caption__**")

    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("__**✅ Caption Saved**__")

@pbot.on_message(filters.private & filters.photo)
async def addthumbs(client, message):

    mkn = await message.reply_text("Please Wait ...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)
    await mkn.edit("✅️ __**Thumbnail Saved**__")
    
available_templates = [
    "[S{season} Ep{episode}] {capitalized_filename}",
    "[s{season} ep{episode}] {capitalized_filename}",
    "[S{season} EP{episode}] {capitalized_filename}",
    "[Season{season} Episode{episode}] {capitalized_filename}",
    "[Ep{episode}] {capitalized_filename}",
    "[SEASON{season} EPISODE{episode}] {capitalized_filename}"
]

@pbot.on_message(filters.command("set_temp") & filters.private)
async def set_template_command(client, message):
    user_id = message.from_user.id

    # Get the template from the command arguments
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        # If no template is provided, show available templates
        templates_list = "\n".join([f"{i+1}. {template}" for i, template in enumerate(available_templates)])
        await message.reply(f"Available templates:\n{templates_list}\n\nUsage: /set_temp <template_number>")
        return

    try:
        # Extract the selected template number
        selected_template_number = int(command_parts[1]) - 1
        selected_template = available_templates[selected_template_number]

        # Update the user's template in the database
        await db.set_template(user_id, selected_template)

        # Notify the user about the template update
        await message.reply(f"Template set to:\n{selected_template}")

    except (ValueError, IndexError) as e:
        logger.error(f"Error setting template for user {user_id}: {e}")
        await message.reply("An error occurred. Please try again.")

@pbot.on_message(filters.command("set_upload") & filters.private)
async def set_upload_command(client, message):
    user_id = message.from_user.id

    # Get the upload mode from the command arguments
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        # If no mode is provided, show available modes
        await message.reply("Available modes:\n1. document\n2. video\n\nUsage: /set_upload <mode_number>")
        return

    try:
        # Extract the selected mode number
        selected_mode_number = int(command_parts[1])

        # Validate the selected mode number
        if selected_mode_number not in [1, 2]:
            raise ValueError("Invalid mode number. Please select a valid mode.")

        # Map mode number to mode name
        upload_modes = {1: "document", 2: "video"}
        selected_mode = upload_modes[selected_mode_number]

        # Update the user's upload mode in the database
        await db.set_uploadtype(user_id, selected_mode)

        # Notify the user about the upload mode update
        await message.reply(f"Upload mode set to: {selected_mode}")

    except ValueError as e:
        logger.error(f"Error setting upload mode for user {user_id}: {e}")
        await message.reply("An error occurred. Please try again.")

@pbot.on_message(filters.command("set_exten") & filters.private)
async def set_exten_command(client, message):
    user_id = message.from_user.id

    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.reply("Available modes:\n1. mkv\n2. mp4\n3. mp3\n4. apk\n5. txt\n\nUsage: /set_exten <mode_number>")
        return

    try:
        selected_mode_number = int(command_parts[1])

        if selected_mode_number not in [1, 2, 3, 4, 5]:
            raise ValueError("Invalid mode number. Please select a valid mode.")

        exten_modes = {1: "mkv", 2: "mp4", 3: "mp3", 4: "apk", 5: "txt"}
        selected_mode = exten_modes[selected_mode_number]

        await db.set_exten(user_id, selected_mode)
        await message.reply(f"Extension mode set to: {selected_mode}")

    except ValueError as e:
        logger.error(f"Error setting exten mode for user {user_id}: {e}")
        await message.reply("An error occurred. Please try again.")

