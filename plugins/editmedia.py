from pyrogram.types import InlineKeyboardMarkup
from helper.token import none_admin_utils
from Krito import pbot 
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    InputMediaPhoto,
    InputMediaDocument,
    InputMediaVideo,
    InputMediaAnimation,
    InputMediaAudio
)

@pbot.on_message(filters.private & filters.command("editmedia"))
async def edit_media(client, message):
    print("Command received for edit media")
    user_id = message.from_user.id
    print(f"User ID: {user_id}")
    replied_message = message.reply_to_message
    print("Got replied message")

    if not replied_message:
        await message.reply_text("Please reply to a message with media you want to edit or provide a URL.")
        print("User did not provide a URL or reply to a message")
        return

    try:
        none_admin_msg, error_buttons = await none_admin_utils(message)
        print("Checked admin utils")
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            print("User is not admin")
            await client.send_message(
                chat_id=message.chat.id,
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup(error_buttons)
            )
            print("Sent error message to user")
            return
        print("User is admin")
    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply_text(f"An error occurred: {e}")


    # Detect media type and create appropriate InputMedia object
    if replied_message.photo:
        media = InputMediaPhoto(media=replied_message.photo.file_id, caption=replied_message.caption and replied_message.caption.html)
        print("Media type: Photo")
    elif replied_message.document:
        media = InputMediaDocument(media=replied_message.document.file_id, caption=replied_message.caption and replied_message.caption.html)
        print("Media type: Document")
    elif replied_message.video:
        media = InputMediaVideo(media=replied_message.video.file_id, caption=replied_message.caption and replied_message.caption.html)
        print("Media type: Video")
    elif replied_message.animation:
        media = InputMediaAnimation(media=replied_message.animation.file_id, caption=replied_message.caption and replied_message.caption.html)
        print("Media type: Animation")
    elif replied_message.audio:
        media = InputMediaAudio(media=replied_message.audio.file_id, caption=replied_message.caption and replied_message.caption.html)
        print("Media type: Audio")
    else:
        await message.reply_text("Unsupported media type.")
        print("Unsupported media type")
        return

    try:
        url = message.text.split(" ", 1)[1]
        print(f"URL extracted: {url}")
        chatid = None
        msg_id = None

        if "t.me" in url:
            parts = url.split("/")
            print(f"URL parts: {parts}")
            if len(parts) >= 5:
                if "c" in parts[3]:
                    chatid = int("-100" + parts[4])
                    msg_id = int(parts[5])
                    print(f"Chat ID: {chatid}, Message ID: {msg_id}")
                else:
                    chatid = parts[3]
                    msg_id = int(parts[4])
                    print(f"Chat ID: {chatid}, Message ID: {msg_id}")

        if chatid and msg_id:
            try:
                # Check if the user is an admin in the specified channel
                is_admin = await client.get_chat_member(chat_id=chatid, user_id=user_id)
                print(f"Checked if user is admin: {is_admin.status}")
            except UserNotParticipant:
                await message.reply_text("You are not a member of this channel, and hence you can't edit this message.")
                print("User not participant in channel")
                return

            if is_admin.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}:
                # Edit the original message with the new media
                try:
                    await client.edit_message_media(chat_id=chatid, message_id=msg_id, media=media)
                    print("Message edited successfully")
                    await message.reply_text("Message edited successfully.")
                except Exception as e:
                    await message.reply_text(f"Failed to edit message: {str(e)}")
                    print(f"Failed to edit message: {str(e)}")
            else:
                await message.reply_text("You don't have the permission to edit messages in this channel.")
                print("User doesn't have permission to edit messages")
        else:
            await message.reply_text("Invalid URL format.")
            print("Invalid URL format")
    except IndexError:
        await message.reply_text("Please provide a valid URL.")
        print("No URL provided")

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
