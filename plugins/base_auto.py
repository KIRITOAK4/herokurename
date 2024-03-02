from pyrogram import filters
from Krito import pbot
from helper.database import db

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

    # Extract the selected template number
    try:
        selected_template_number = int(command_parts[1]) - 1
        selected_template = available_templates[selected_template_number]
    except (ValueError, IndexError):
        await message.reply("Invalid template number. Please select a valid template.")
        return

    # Update the user's template in the database
    await db.set_template(user_id, selected_template)

    # Notify the user about the template update
    await message.reply(f"Template set to:\n{selected_template}")


@pbot.on_message(filters.command("set_upload") & filters.private)
async def set_upload_command(client, message):
    user_id = message.from_user.id

    # Get the upload mode from the command arguments
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        # If no mode is provided, show available modes
        await message.reply("Available modes:\n1. Document\n2. Video\n\nUsage: /set_upload <mode_number>")
        return

    # Extract the selected mode number
    try:
        selected_mode_number = int(command_parts[1])
    except ValueError:
        await message.reply("Invalid mode number. Please select a valid mode.")
        return

    # Validate the selected mode number
    if selected_mode_number not in [1, 2]:
        await message.reply("Invalid mode number. Please select a valid mode.")
        return

    # Map mode number to mode name
    upload_modes = {1: "Document", 2: "Video"}
    selected_mode = upload_modes[selected_mode_number]

    # Update the user's upload mode in the database
    await db.set_uploadtype(user_id, selected_mode)

    # Notify the user about the upload mode update
    await message.reply(f"Upload mode set to: {selected_mode}")
