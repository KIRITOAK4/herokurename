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
    force_subs = FORCE_SUB.split()  # Split FORCE_SUB values by spaces
    buttons = []
    text = "**Sᴏʀʀʏ Dᴜᴅᴇ Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ**"

    for force_sub in force_subs:
        try:
            invite_link = await client.export_chat_invite_link(force_sub)
            button = [InlineKeyboardButton(text=f"📢 Join Update Channel {force_sub} 📢", url=invite_link)]
            buttons.extend(button)
        except Exception as e:
            print(f"Error: {e}")
            return await message.reply_text("Failed to get the invite link. Please try again later.")

    try:
        user = await client.get_chat_member(FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return await client.send_message(message.from_user.id, text="Sᴏʀʀʏ Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")
    except UserNotParticipant:
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup([buttons]))

    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup([buttons]))
