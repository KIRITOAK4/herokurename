import time
from .database import db
from Krito import MAX_PROCESS, COOLDOWN_DURATION

# Define a dictionary to store completed processes for each user
completed_processes = {}

# Define a dictionary to store cooldown timestamps for each user
cooldowns = {}

# Maximum number of processes allowed before cooldown starts
#MAX_PROCESSES = 5

# Cooldown duration in seconds
#COOLDOWN_DURATION = 60  # 60 seconds cooldown


def update_completed_processes(user_id):
    # Check if the user is in the completed_processes dictionary
    if user_id in completed_processes:
        completed_processes[user_id] += 1
    else:
        completed_processes[user_id] = 1


def check_cooldown(user_id):
    # Check if the user has completed the maximum number of processes
    if user_id in completed_processes and completed_processes[user_id] >= MAX_PROCESS:
        # Check if the user is in the cooldown dictionary
        if user_id in cooldowns:
            # Get the timestamp when the user last completed a process
            last_completed_time = cooldowns[user_id]
            # Get the current time
            current_time = time.time()
            # Calculate the time elapsed since the last completed process
            time_elapsed = current_time - last_completed_time
            # Check if the cooldown duration has passed
            if time_elapsed < COOLDOWN_DURATION:
                # User is still on cooldown
                return True, COOLDOWN_DURATION - int(time_elapsed)
        # User has completed the maximum number of processes, start cooldown
        cooldowns[user_id] = time.time()
        completed_processes[user_id] = 0  # Reset completed processes count
    # User is not on cooldown
    return False, 0


def process_and_update_cooldown(user_id):
    try:
        on_cooldown, remaining_time = check_cooldown(user_id)
        if on_cooldown:
            return True, remaining_time  # User is on cooldown
        db.update_user_cooldown_data(user_id)
        return False, 0  # Process completed successfully, not on cooldown
    except Exception as e:
        print(f"Error in processing and updating cooldown: {e}")
        return True, 0  # An error occurred during processing, user is on cooldown


# Example usage:
# user_id = 123  # Replace this with the actual user ID
# on_cooldown, remaining_time = process_and_update_cooldown(user_id)
# if on_cooldown:
#     print(f"You are on cooldown. Please wait for {remaining_time} seconds.")
# else:
#     print("Process completed successfully!")
