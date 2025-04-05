import smtplib
import psycopg2
from email.mime.text import MIMEText
import socket
import ssl
from email.mime.multipart import MIMEMultipart
import os

# Database Connection
conn = psycopg2.connect(
    dbname      = "db-chainsight",
    user        = "metuCeng",
    password    = "chainsight-2025",
    host        = "db-chainsight.postgres.database.azure.com",
    port        = "5432"
)
cursor = conn.cursor()

# Fetch the latest schema changes
cursor.execute(
    "SELECT event_type, schema_name, table_name, change_time "
    "FROM schema_changes_log "
    "WHERE event_type IN ('CREATE TABLE','ALTER TABLE','DROP TABLE') "
    "ORDER BY change_time DESC LIMIT 5")
rows = cursor.fetchall()

# Email Configuration
SMTP_SERVER         = "smtp.metu.edu.tr"  # Use your SMTP server
SMTP_PORT           = 465  # Use your SMTP port
EMAIL_USER          = os.getenv("EMAIL_USER")
SENDER_EMAIL        = "e239915@metu.edu.tr"
EMAIL_PASSWORD      = os.getenv("EMAIL_PASSWORD")
RECIPIENTS          = ["e2399152@ceng.metu.edu.tr"]

if EMAIL_USER is None or EMAIL_PASSWORD is None:
    print("Error: Environment variables not set! ❌")
else:
    print(f"Using email: {EMAIL_USER}")  # Debugging (Safe to print username)


if rows:
    message_body = "\n".join([f"{row[3]}: {row[0]} on {row[2]} (Schema: {row[1]})" for row in rows])
    print(message_body)
    msg = MIMEText(message_body)
    msg["Subject"] = "chAInSight Database Notification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)

    context = ssl._create_unverified_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        print("Email sent successfully! ✅")

# Mark processed records (optional)
cursor.execute("DELETE FROM schema_changes_log WHERE change_time < now() - INTERVAL '1 day'")
conn.commit()

cursor.close()
conn.close()