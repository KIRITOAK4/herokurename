import time
from pyrogram import Client, filters
from bot import bot

@bot.on_message(filters.private & filters.command("p2"))
async def p2_command(client, message):
    start_time = time.time()
    sent_message = await message.reply("Pinging...")
    end_time = time.time()
    rtt = (end_time - start_time) * 50
    await sent_message.edit(f"Pong! RTT: {rtt:.2f} ms")
