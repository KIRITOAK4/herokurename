import time
from .database import db
from Krito import MAX_PROCESS, COOLDOWN_DURATION

completed_processes = {}
cooldowns = {}

async def update_completed_processes(user_id):
    completed_processes[user_id] = completed_processes.get(user_id, 0) + 1
    if completed_processes[user_id] >= MAX_PROCESS:
        cooldowns[user_id] = time.time() + COOLDOWN_DURATION
        
async def check_cooldown(user_id):
    if user_id in cooldowns:
        time_left = int(cooldowns[user_id] - time.time())
        if time_left <= 0:
            completed_processes[user_id] = 0
            del cooldowns[user_id]
            return False, 0
        return True, time_left
    return False, 0

async def process_and_update_cooldown(user_id):
    on_cooldown, time_left = await check_cooldown(user_id)
    if on_cooldown:
        return True, time_left
    await update_completed_processes(user_id)
    await db.update_user_cooldown_data(user_id)
    return False, 0
