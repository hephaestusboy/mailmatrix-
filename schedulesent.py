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


def load_email_data(data_file="data1.txt", schedule_file="email_schedule.json"):
    """Load email details and schedule times from data1.txt and email_schedule.json."""
    email_data = []
    with open(data_file, 'r') as file:
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) == 3:
                email = parts[0].split(": ")[1]
                location = parts[1].split(": ")[1].strip("'")
                message = parts[2].split(": ")[1]
                email_data.append({"to_email": email, "location": location, "message": message})

    with open(schedule_file, 'r') as file:
        schedule_times = json.load(file)

    email_schedule = []
    for i, email_info in enumerate(email_data):
        if i < len(schedule_times):
            scheduled_time = datetime.strptime(schedule_times[i]["send_time"], '%Y-%m-%d %H:%M:%S')
            email_schedule.append({
                "to_email": email_info["to_email"],
                "subject": f"Message to {email_info['location']}",
                "body": f"{email_info['message']}\n\nLocation: {email_info['location']}",
                "send_time": scheduled_time
            })

    return email_schedule, schedule_times


def send_email(to_email, subject, body):
    """Send an email using the provided configuration."""
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


def check_network():
    """Check network connectivity."""
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def remove_line_from_data_file(email, data_file):
    """Remove the line from data1.txt corresponding to the given email."""
    with open(data_file, "r") as file:
        lines = file.readlines()

    with open(data_file, "w") as file:
        for line in lines:
            if email not in line:
                file.write(line)


def schedule_emails():
    """Schedule and send emails based on their scheduled times."""
    email_schedule, schedule_times = load_email_data()

    sent_status = {}
    if os.path.exists('email_status.txt'):
        with open('email_status.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    email_id, status = line.strip().split(':', 1)
                    sent_status[email_id] = status

    while True:
        current_time = datetime.now()
        emails_sent_this_cycle = False  # Track if any emails were sent in this cycle

        for email in email_schedule[:]:  # Iterate over a copy of the list
            email_id = f"{email['to_email']}_{email['send_time']}"
            scheduled_time = email['send_time']

            # Check if the scheduled time has passed and the email has not been sent
            if current_time >= scheduled_time and sent_status.get(email_id) != 'sent':
                print(f"Waiting for network connection to send email to {email['to_email']}...")

                # Wait for a network connection before sending
                while not check_network():
                    print("No network connection. Retrying in 5 seconds...")
                    time.sleep(5)

                if send_email(email['to_email'], email['subject'], email['body']):
                    # Update sent status and remove from the schedule
                    sent_status[email_id] = 'sent'
                    email_schedule.remove(email)  # Remove from schedule after sending
                    emails_sent_this_cycle = True

                    with open('email_status.txt', 'a') as f:
                        f.write(f"{email_id}:sent\n")

                    # Remove the corresponding line from data1.txt
                    remove_line_from_data_file(email['to_email'], "data1.txt")

                    # Find and remove the scheduled time entry
                    index_to_remove = next((i for i, entry in enumerate(schedule_times)
                                            if entry['send_time'] == email['send_time'].strftime('%Y-%m-%d %H:%M:%S')), None)
                    if index_to_remove is not None:
                        schedule_times.pop(index_to_remove)

                        with open("email_schedule.json", "w") as f:
                            json.dump(schedule_times, f)

        if not email_schedule:
            print("All scheduled emails have been sent.")
            break
        
        if not emails_sent_this_cycle:
            print("No emails could be sent this cycle.")

        time.sleep(20)  # Wait before checking again

if __name__ == "__main__":
    schedule_emails()
