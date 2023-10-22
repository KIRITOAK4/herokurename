import time
from .database import db
from Krito import MAX_PROCESS, COOLDOWN_DURATION

completed_processes = {}
cooldowns = {}

async def update_completed_processes(user_id):
    if user_id in completed_processes:
        completed_processes[user_id] += 1
    else:
        completed_processes[user_id] = 1

async def check_cooldown(user_id):
    if completed_processes.get(user_id, 0) >= MAX_PROCESS:
        if user_id not in cooldowns:
            cooldown_end_time = time.time() + COOLDOWN_DURATION
            cooldowns[user_id] = cooldown_end_time
        else:
            cooldown_end_time = cooldowns[user_id]
            current_time = time.time()
            if current_time >= cooldown_end_time:
                completed_processes[user_id] = 0
                del cooldowns[user_id]
                return False, 0
            else:
                remaining_time = int(cooldown_end_time - current_time)
                return True, remaining_time
    else:
        return False, 0

async def process_and_update_cooldown(user_id):
    try:
        on_cooldown, remaining_time = await check_cooldown(user_id)
        if on_cooldown:
            return True, remaining_time
        await update_completed_processes(user_id)
        await db.update_user_cooldown_data(user_id)
        return False, 0
    except Exception as e:
        print(f"Error in processing and updating cooldown: {e}")
        return True, 0
