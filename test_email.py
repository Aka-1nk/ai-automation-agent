import smtplib
from email.mime.text import MIMEText

# 🔑 Your details
sender = "akankshat2005@gmail.com"
receiver = "akankshat2005@gmail.com"   # can be same or different
password = "fvru vdbx zalz hmex"

try:
    print("Connecting to Gmail...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    print("Logging in...")
    server.login(sender, password)

    print("Creating message...")
    msg = MIMEText("Hello! This is a test email from Python.", "plain", "utf-8")
    msg["Subject"] = "Test Email"
    msg["From"] = sender
    msg["To"] = receiver

    print("Sending email...")
    server.sendmail(sender, receiver, msg.as_string())

    server.quit()
    print("✅ Email sent successfully!")

except Exception as e:
    print("❌ Error:", e)