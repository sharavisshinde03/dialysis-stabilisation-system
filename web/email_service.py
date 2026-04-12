import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email, subject, body):
    try:
        print("📧 Attempting to send email...")
        print("EMAIL:", EMAIL_ADDRESS)
        print("PASSWORD:", EMAIL_PASSWORD)

        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            print("🔐 Logging in to Gmail SMTP...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            print("📨 Sending message...")
            server.send_message(msg)

        print("✅ Email sent successfully")

    except Exception as e:
        import traceback
        print("❌ Email failed")
        traceback.print_exc()