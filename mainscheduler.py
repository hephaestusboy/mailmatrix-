import time
import os
import subprocess
from multiprocessing import Process

def monitor_data_file(data_file='data.txt', interval=20):
    """Monitor data.txt for changes and update the schedule accordingly."""
    last_modified_time = os.path.getmtime(data_file)

    while True:
        current_modified_time = os.path.getmtime(data_file)
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            print("Detected changes in data.txt. Updating schedule...")

            # Start update_schedule and send_emails in separate processes
            update_process = Process(target=update_schedule)
            send_process = Process(target=send_emails)

            update_process.start()
            send_process.start()

            # Do not join the processes here, let them run independently

        else:
            print("No changes detected. Waiting...")
        
        time.sleep(interval)  # Check for changes every 'interval' seconds

def update_schedule():
    """Run shedulefinder.py to update the email schedule for all entries."""
    try:
        subprocess.run(['python3', 'shedulefinder.py'], check=True)
        print("Schedule updated successfully.")
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
