import os
import random
import re
import logging
from gif import *
from Krito import Text, Text1, Text2, Text3
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO, filename='error.log')
logger = logging.getLogger("GifHandler")
logger.setLevel(level=logging.INFO)

def get_page_gif(page_number):
    try:
        gif = os.listdir('./gif')
        selected_gif = random.choice(gif)
        gif_path = f'./gif/{selected_gif}'
        return gif_path
    except Exception as e:
        logger.error(f"An error occurred in get_page_gif: {e}")
        return None

def get_page_caption(page_number, first_name, last_name, mention, username, id):
    try:
        if page_number == 0:
            page_text = Text
        elif page_number == 1:
            page_text = Text1
        elif page_number == 2:
            page_text = Text2
        elif page_number == 3:
            page_text = Text3
        
        mention = f"[{first_name}](tg://user?id={id})"
        if username:
            username_text = f"@{username}"
        else:
            username_text = ""
        
        cption = page_text.format(first_name=first_name, last_name=last_name, username=username_text, mention=mention, id=id)
        caption = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1](\2)', caption)
        return caption
    except Exception as e:
        logger.error(f"An error occurred in get_page_caption: {e}")
        return None

def get_inline_keyboard(page_number):
    try:
        inline_keyboard = []

        row = []
        if page_number > 0:
            row.append(InlineKeyboardButton("👈", callback_data="previous"))
        if page_number < 3 and (page_number != 4 or Text):
            row.append(InlineKeyboardButton("👉", callback_data="next"))
        inline_keyboard.append(row)

        return inline_keyboard
    except Exception as e:
        logger.error(f"An error occurred in get_inline_keyboard: {e}")
        return None
