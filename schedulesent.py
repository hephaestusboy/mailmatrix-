import smtplib
import os
import socket
import time
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'thisisatestmail19@gmail.com'
EMAIL_PASSWORD = 'tgzlfmejkwiuzlqr'

# Function to load email data from data.txt and scheduling times from email_schedule.json
def load_email_data(data_file="data.txt", schedule_file="email_schedule.json"):
    email_schedule = []

    # Load email details from data.txt
    with open(data_file, 'r') as file:
        email_data = []
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) != 3:  # Ensure there are exactly 3 parts
                print(f"Skipping malformed line: '{line.strip()}'")
                continue  # Skip malformed lines

            try:
                email = parts[0].split(": ")[1]
                location = parts[1].split(": ")[1].strip().strip("'")  # Strip single quotes if any
                message = parts[2].split(": ")[1]
                email_data.append({"to_email": email, "location": location, "message": message})
            except IndexError:
                print(f"Malformed line details: '{line.strip()}'")

    # Load send times from email_schedule.json
    with open(schedule_file, 'r') as file:
        schedule_times = json.load(file)

    # Combine email details with schedule times
    for i, email_info in enumerate(email_data):
        if i < len(schedule_times):
            try:
                scheduled_time = datetime.strptime(schedule_times[i]["send_time"], '%Y-%m-%d %H:%M:%S')
                email_schedule.append({
                    "to_email": email_info["to_email"],
                    "subject": f"Message from {email_info['location']}",
                    "body": f"{email_info['message']}\n\nLocation: {email_info['location']}",
                    "send_time": scheduled_time
                })
            except ValueError:
                print(f"Error parsing send_time for email: {schedule_times[i]['send_time']}")

    return email_schedule



# Function to send an email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent to {to_email} at {datetime.now()}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

# Function to check network connectivity
def check_network():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

# Function to schedule and send emails
def schedule_emails():
    # Load the email schedule from data.txt and email_schedule.json
    email_schedule = load_email_data()

    # Load the status of sent emails
    sent_status = {}
    if os.path.exists('email_status.txt'):
        with open('email_status.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    email_id, status = line.split(':', 1)
                    sent_status[email_id] = status

    # Check and send each email at the scheduled time
    while email_schedule:
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
        
        for email in email_schedule[:]:  # Iterate over a copy of the list
            email_id = f"{email['to_email']}_{email['send_time']}"
            scheduled_time = datetime.strptime(str(email['send_time']), '%Y-%m-%d %H:%M:%S')
            
            # Check if the scheduled time has passed and if the email has not been sent
            if current_time >= scheduled_time and sent_status.get(email_id) != 'sent':
                print(f"Waiting for network connection to send email to {email['to_email']}...")
                
                # Wait for a network connection before sending
                while not check_network():
                    print("No network connection. Retrying in 5 seconds...")
                    time.sleep(5)
                
                # Send the email
                if send_email(email['to_email'], email['subject'], email['body']):
                    sent_status[email_id] = 'sent'
                    email_schedule.remove(email)  # Remove from schedule after sending

                    # Update the status file
                    with open('email_status.txt', 'a') as f:
                        f.write(f"{email_id}:sent\n")

        # Stop the loop if all emails have been sent
        if not email_schedule:
            print("All scheduled emails have been sent.")
            break

        time.sleep(20)  # Check every 20 seconds

if __name__ == "__main__":
    schedule_emails()
