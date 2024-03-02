from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from helper.database import db
from Krito import pbot

@pbot.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    # Removed the unused none_admin_utils function

    caption = await db.get_caption(message.from_user.id)
    if not caption:
        return await message.reply_text("__**😔 You Don't Have Any Caption**__")

    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("__**❌️ Caption Deleted**__")

@pbot.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    # Removed the unused none_admin_utils function

    caption = await db.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"**Your Caption:-**\n\n`{caption}`")
    else:
        await message.reply_text("__**😔 You Don't Have Any Caption**__")

@pbot.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    # Removed the unused none_admin_utils function

    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("❌️ __**Thumbnail Deleted**__")

