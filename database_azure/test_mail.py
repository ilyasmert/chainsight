import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Configuration
SMTP_SERVER         = "smtp.metu.edu.tr"  # Use your SMTP server
SMTP_PORT           = 465  # Use your SMTP port
EMAIL_USER          = "e239915"
EMAIL_PASSWORD      = "Feka_35ciko"
RECIPIENTS          = ["e239915@metu.edu.tr", "e2399152@ceng.metu.edu.tr"]

# Email Details
sender_email = "e239915@metu.edu.tr"
receiver_email = "e2399152@ceng.metu.edu.tr"  # Change this to your email
subject = "Test Email from Python Script"
body = "This is a test email sent via Python SMTP."

# Create Email
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    print("Connecting to SMTP server with SSL...")
    context = ssl._create_unverified_context()  # Ignore SSL errors

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        print("Logging in...")
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        print("Sending email...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully! ✅")

except Exception as e:
    print(f"Error: {e}")
