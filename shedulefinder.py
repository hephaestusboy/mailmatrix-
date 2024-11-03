import time
import json
from datetime import datetime, timedelta
import subprocess

def add_minutes(minutes):
    """Add a specified number of minutes to the current time."""
    current_time = datetime.now()
    new_time = current_time + timedelta(minutes=minutes)
    return new_time  # Return the new time

def run_script():
    """Run traveltime.py and capture its output."""
    result = subprocess.run(['python3', 'traveltime.py'], capture_output=True, text=True)
    return result.stdout.strip()  # Return the output as a string

def update_schedule_json(new_entry):
    """Update the email_schedule.json file with a new entry."""
    # Read existing schedule data
    try:
        with open('email_schedule.json', 'r') as file:
            schedule_data = json.load(file)
    except FileNotFoundError:
        schedule_data = []  # Start with an empty list if the file doesn't exist

    # Add the new entry to the schedule data
    schedule_data.append(new_entry)

    # Write updated schedule data back to the JSON file
    with open('email_schedule.json', 'w') as file:
        json.dump(schedule_data, file, indent=4)

if __name__ == "__main__":
    print("Starting to monitor data.txt for changes...")

    last_line_count = 0  # Initialize last line count
    
    while True:
        time.sleep(10)  # Check every 10 seconds
        
        # Check the current line count in data.txt
        with open('data.txt', 'r') as file:
            current_lines = file.readlines()
            current_line_count = len(current_lines)

        # If the line count has changed, process the new entries
        if current_line_count > last_line_count:
            print("Detected changes in data.txt. Updating schedule...")
            for i in range(last_line_count, current_line_count):
                output = run_script()
                if output:
                    try:
                        minutes_to_add = int(abs(float(output)))
                        new_sent_time = add_minutes(minutes_to_add)
                        print(f"\nNew sent time is {new_sent_time}")

                        # Prepare the new entry
                        new_entry = {"send_time": new_sent_time.strftime('%Y-%m-%d %H:%M:%S')}
                        print(new_entry)
                        update_schedule_json(new_entry)

                    except ValueError as ve:
                        print(f"Error processing time: {ve}")
                else:
                    print("No output from traveltime.py.")
                    
            # Update the last line count to the current line count
            last_line_count = current_line_count
        else:
            # If no new lines are detected, exit the loop
            print("No new changes detected. Exiting...")
            break
