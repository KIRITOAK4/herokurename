import os, asyncio, uuid
from time import time
from pyrogram.types import InlineKeyboardButton
from helper.database import db
from config import Config
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
        if not Config.TOKEN_TIMEOUT:
            return None, button
        userid = message.from_user.id
        if userid in Config.ADMIN:
            return None, button
        data = await db.get_user_data(userid)
        expire = data.get('time')
        is_expired = (expire is None or (time() - expire) > Config.TOKEN_TIMEOUT)
        if is_expired:
            token = data.get('token') if expire is None and 'token' in data else str(uuid.uuid4())
            if expire is not None:
                del data['time']
            data['token'] = token
            await db.update_user_data(userid, data)
            if button is None:
                buttons = [
                    [
                        InlineKeyboardButton(text='Refresh Token', url=shorten_url(f'https://t.me/{Config.BOT_NAME}?start={token}')),
                        InlineKeyboardButton(text='Tutorial', url='https://t.me/hentai_caps/3')
                    ],
                    [
                        InlineKeyboardButton(text='Short Method', url='https://shrtco.de/%F0%9F%91%AD%F0%9F%8C%B2')
                    ]
                ]
                button = buttons
            error_msg = 'Token is expired, refresh your token and try again.'
            return error_msg, button

        return None, button

    except Exception as e:
        print(f"An error occurred in validate_user: {e}")
