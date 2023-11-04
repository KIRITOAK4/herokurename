import time
from .database import db
from Krito import MAX_PROCESS, COOLDOWN_DURATION

completed_processes = {}
cooldowns = {}

async def update_completed_processes(user_id):
    print("Entered update_completed_processes")
    print(f"MAX_PROCESS: {MAX_PROCESS}")
    print(f"Initial completed_processes: {completed_processes}")
    if user_id in completed_processes:
        completed_processes[user_id] += 1
        print(f"Updated completed_processes for user: {user_id}, Count: {completed_processes[user_id]}")
    else:
        completed_processes[user_id] = 1
        print(f"Set completed_processes for new user: {user_id}, Count: {completed_processes[user_id]}")

async def check_cooldown(user_id):
    print("Entered check_cooldown")
    print(f"MAX_PROCESS: {MAX_PROCESS}")
    print(f"Current completed_processes: {completed_processes}")
    print(f"Current cooldowns: {cooldowns}")
    if completed_processes.get(user_id, 0) >= MAX_PROCESS:
        print(f"User: {user_id} has reached MAX_PROCESS")
        if user_id not in cooldowns:
            cooldown_end_time = time.time() + COOLDOWN_DURATION
            cooldowns[user_id] = cooldown_end_time
            print(f"Initialized cooldown for user: {user_id}, Ends at: {cooldown_end_time}")
        else:
            cooldown_end_time = cooldowns[user_id]
            current_time = time.time()
            print(f"Checked cooldown for user: {user_id}, Current time: {current_time}, Cooldown end time: {cooldown_end_time}")
            if current_time >= cooldown_end_time:
                completed_processes[user_id] = 0
                del cooldowns[user_id]
                print(f"Cooldown completed for user: {user_id}")
                print(f"Updated cooldowns: {cooldowns}")
                return False, 0
            else:
                remaining_time = int(cooldown_end_time - current_time)
                print(f"User: {user_id} is still on cooldown, Remaining time: {remaining_time}")
                return True, remaining_time
    else:
        print(f"No cooldown for user: {user_id}")
        return False, 0

async def process_and_update_cooldown(user_id):
    print("Entered process_and_update_cooldown")
    try:
        on_cooldown, remaining_time = await check_cooldown(user_id)
        print(f"Cooldown check for user: {user_id}, On cooldown: {on_cooldown}, Remaining time: {remaining_time}")
        if on_cooldown:
            return True, remaining_time
        await update_completed_processes(user_id)
        print(f"Updated completed processes for user: {user_id}")
        await db.update_user_cooldown_data(user_id)
        print(f"Updated user cooldown data in DB for user: {user_id}")
        return False, 0
    except Exception as e:
        print(f"Error in processing and updating cooldown: {e}")
        return True, 0
