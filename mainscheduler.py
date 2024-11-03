import time
import os
import subprocess

def monitor_data_file(data_file='data.txt', interval=5):
    """Monitor data.txt for changes and update the schedule accordingly."""
    last_modified_time = os.path.getmtime(data_file)

    while True:
        current_modified_time = os.path.getmtime(data_file)
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            print("Detected changes in data.txt. Updating schedule...")
            update_schedule()
        else:
            print("No changes detected. Waiting...")
        
        time.sleep(interval)  # Check for changes every 'interval' seconds

def update_schedule():
    """Run shedulefinder.py to update the email schedule for all entries."""
    try:
        # Run shedulefinder.py which should handle all entries
        subprocess.run(['python3', 'shedulefinder.py'], check=True)
        print("Schedule updated successfully.")
        send_emails()  # Call the email sender after updating
    except subprocess.CalledProcessError as e:
        print(f"Error while updating schedule: {e}")

def send_emails():
    """Run schedulesent.py to send emails."""
    try:
        subprocess.run(['python3', 'schedulesent.py'], check=True)
        print("Email sending process completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error while sending emails: {e}")

if __name__ == "__main__":
    print("Starting to monitor data.txt for changes...")
    monitor_data_file()
