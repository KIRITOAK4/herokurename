from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from helper.database import db
from Krito import pbot, FORCE_SUB

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not FORCE_SUB:
        return False
    try:
        user = await client.get_chat_member(FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return True
        else:
            return False
    except UserNotParticipant:
        pass
    return True

@pbot.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    try:
        invite_link = await client.export_chat_invite_link(FORCE_SUB)
    except Exception as e:
        print(f"Error: {e}")
        return await message.reply_text("Failed to get the invite link. Please try again later.")
    
    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=invite_link)]]
    text = "**Sᴏʀʀʏ Dᴜᴅᴇ Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ**"
    
    try:
        user = await client.get_chat_member(FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return await client.send_message(message.from_user.id, text="Sᴏʀʀʏ Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")
    except UserNotParticipant:
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
