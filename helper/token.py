import os
import asyncio
import uuid
from time import time
from pyrogram.types import InlineKeyboardButton
from helper.database import db
from Krito import BOT_NAME, TOKEN_TIMEOUT, ADMIN
from shortener import shorten_url

async def none_admin_utils(message):
    try:
        error_msg = []
        error_buttons = None
        token_msg, buttons = await validate_user(message)
        if token_msg is not None:
            error_msg.append(token_msg)
            error_buttons = buttons
        return error_msg, error_buttons
    
    except Exception as e:
        print(f"An error occurred in none_admin_utils: {e}")
 
async def validate_user(message, button=None):
    try:
        if not TOKEN_TIMEOUT:
            return None, button
        userid = message.from_user.id
        if userid in ADMIN:
            return None, button
        data = await db.get_user_data(userid)
        expire = data.get('time')
        is_expired = (expire is None or (time() - expire) > TOKEN_TIMEOUT)
        if is_expired:
            token = data.get('token') if expire is None and 'token' in data else str(uuid.uuid4())
            if expire is not None:
                del data['time']
            data['token'] = token
            await db.update_user_data(userid, data)
            if button is None:
                buttons = [
                    [
                        InlineKeyboardButton(text='Refresh Token', url=shorten_url(f'https://telegram.me/{BOT_NAME}?start={token}')),
                        InlineKeyboardButton(text='Tutorial', url='https://telegram.me/hentai_caps/42')
                    ],
                    [
                        InlineKeyboardButton(text='Short Method', url='https://telegram.me/forward_holder_bot?start=Z2V0LTYxMDk4NDkwMzU5MDUwMA')
                    ]
                ]
                button = buttons
            error_msg = 'Token is expired, refresh your token and try again.'
            return error_msg, button

        return None, button

    except Exception as e:
        print(f"An error occurred in validate_user: {e}")
