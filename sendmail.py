import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Set up the SMTP server and port
    smtp_server = "smtp.gmail.com"  # Use "smtp.gmail.com" for Gmail
    port = 587  # For TLS

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
    finally:
        server.quit()

# Usage example
send_email("thisisatestmail19@gmail.com", "tgzlfmejkwiuzlqr", "mathewalan414@gmail.com", "Test Subject", "Hello, this is a test email.")
