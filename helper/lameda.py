import os, random, re
from gif import *
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_page_gif(page_number):
    gif = os.listdir('./gif')
    selected_gif = random.choice(gif)
    gif_path = f'./gif/{selected_gif}'
    return gif_path

def get_page_caption(page_number, first_name, last_name, mention, username, id):
    if page_number == 0:
        page_text = Config.Text
    elif page_number == 1:
        page_text = Config.Text1
    elif page_number == 2:
        page_text = Config.Text2
    elif page_number == 3:
        page_text = Config.Text3
        
    username = f"@{username}" if username else None
    mention = f"[{first_name}](tg://user?id={id})"
    cption = page_text.format(first_name=first_name, last_name=last_name, username=username, mention=mention, id=id)
    caption = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1](\2)', cption)
    return caption

def get_inline_keyboard(page_number):
    inline_keyboard = []

    row = []
    if page_number > 0:
        row.append(InlineKeyboardButton("👈 Previous", callback_data="previous"))
    if page_number < 3 and (page_number != 4 or Config.Text):
        row.append(InlineKeyboardButton("Next 👉", callback_data="next"))
    inline_keyboard.append(row)

    return inline_keyboard
