import os, random, asyncio, pdb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import db
from Krito import pbot
from Krito import ADMIN
from helper.token import none_admin_utils
from time import time
from uuid import uuid4
from helper.lameda import get_page_gif, get_page_caption, get_inline_keyboard
from helper.knockers import handle_callback

page_number = [0]

@pbot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        pdb.set_trace()  # Add debugger here
        userid = message.from_user.id
        data = await db.get_user_data(userid)
        input_token = None
        if len(message.command) > 1:
            input_token = message.command[1]
        
        if userid in ADMIN: 
            caption = get_page_caption(page_number[0], message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.mention, message.from_user.id)
            inline_keyboard = get_inline_keyboard(page_number[0])
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await message.reply_video(
                video=get_page_gif(page_number[0]),
                caption=caption,
                supports_streaming=True,
                disable_notification=True,
                reply_markup=reply_markup
            )
            return

        if 'token' not in data or data['token'] != input_token:
            gif_url = 'https://graph.org/file/f6e6beb62a16a46642fb4.mp4'
            caption = '**Token is either used or invalid.**'
            await message.reply_video(
                video=gif_url,
                caption=caption,
                supports_streaming=True
            )
            return
        
        data['token'] = str(uuid4())
        data['time'] = time()
        await db.update_user_data(userid, data)

        caption = get_page_caption(page_number[0], message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.mention, message.from_user.id)
        inline_keyboard = get_inline_keyboard(page_number[0])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await message.reply_video(
            video=get_page_gif(page_number[0]),
            caption=caption,
            supports_streaming=True,
            disable_notification=True,
            reply_markup=reply_markup
        )
        
    except Exception as e:
        pdb.set_trace()  # Add debugger here
        print(f"An error occurred while executing start: {e}")

@pbot.on_callback_query()
async def callback_query(client, callback_query):
    try:
        pdb.set_trace()  # Add debugger here
        await handle_callback(callback_query, page_number, callback_query.from_user)
    except Exception as e:
        pdb.set_trace()  # Add debugger here
        print(f"An error occurred while handling callback in start query: {e}")
