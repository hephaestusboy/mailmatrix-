import time
import json
from datetime import datetime, timedelta
import traveltime  # Import the traveltime module

def add_minutes(minutes):
    """Add a specified number of minutes to the current time."""
    current_time = datetime.now()
    new_time = current_time + timedelta(minutes=minutes)
    return new_time

def update_schedule_json(new_entry):
    """Update the email_schedule.json file with a new entry."""
    try:
        with open('email_schedule.json', 'r') as file:
            schedule_data = json.load(file)
    except FileNotFoundError:
        schedule_data = []

    schedule_data.append(new_entry)

    with open('email_schedule.json', 'w') as file:
        json.dump(schedule_data, file, indent=4)

if __name__ == "__main__":
    print("Starting to monitor data.txt for changes...")

    # Run calculations in traveltime
    traveltime.main()  # Ensure travel times are calculated

    # Access the shared attribute
    travel_times = traveltime.travel_times

    for time_str in travel_times:
        try:
            minutes_to_add = int(abs(float(time_str)))
            new_sent_time = add_minutes(minutes_to_add)
            print(f"\nNew sent time is {new_sent_time}")

            new_entry = {"send_time": new_sent_time.strftime('%Y-%m-%d %H:%M:%S')}
            print(new_entry)
            update_schedule_json(new_entry)

        except ValueError as ve:
            print(f"Error processing time: {ve}")
