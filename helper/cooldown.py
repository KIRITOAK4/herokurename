import time
from .database import db
from Krito import MAX_PROCESS, COOLDOWN_DURATION

completed_processes = {}
cooldowns = {}

print("Dictionaries for completed_processes and cooldowns initialized.")

async def update_completed_processes(user_id):
    completed_processes[user_id] = completed_processes.get(user_id, 0) + 1
    print(f"Completed processes for user {user_id} updated to {completed_processes[user_id]}.")
    if completed_processes[user_id] >= MAX_PROCESS:
        cooldowns[user_id] = time.time() + COOLDOWN_DURATION
        print(f"User {user_id} is now on cooldown until {cooldowns[user_id]}.")

async def check_cooldown(user_id):
    print(f"Checking cooldown for user {user_id}.")
    if user_id in cooldowns:
        time_left = int(cooldowns[user_id] - time.time())
        print(f"Time left for user {user_id}'s cooldown is {time_left}.")
        if time_left <= 0:
            completed_processes[user_id] = 0
            del cooldowns[user_id]
            print(f"Cooldown for user {user_id} has ended.")
            return False, 0
        print(f"User {user_id} is still on cooldown.")
        return True, time_left
    print(f"User {user_id} is not on cooldown.")
    return False, 0

async def process_and_update_cooldown(user_id):
    print(f"Starting process and update cooldown for user {user_id}.")
    on_cooldown, time_left = await check_cooldown(user_id)
    if on_cooldown:
        print(f"User {user_id} cannot proceed because they are on cooldown.")
        return True, time_left
    print(f"User {user_id} is not on cooldown. Proceeding with process update.")
    await update_completed_processes(user_id)
    print(f"Updating user {user_id} cooldown data in the database.")
    await db.update_user_cooldown_data(user_id)
    print(f"Process and cooldown update completed for user {user_id}.")
    return False, 0
