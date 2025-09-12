#SMTP setup for email.
import os
import smtplib

# Read credentials from environment variables instead of hardcoding
sender_email = os.getenv('')
sender_password = os.getenv('')
receiver_email = os.getenv('SMTP_RECEIVER_EMAIL')

if not sender_email or not sender_password or not receiver_email:
    raise RuntimeError('Please set SMTP_SENDER_EMAIL, SMTP_SENDER_PASSWORD, and SMTP_RECEIVER_EMAIL environment variables.')

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, 'Hello, this is a test email')
except smtplib.SMTPAuthenticationError as auth_err:
    raise RuntimeError('Authentication failed. If using Gmail, enable 2-Step Verification and create an App Password, then set it as SMTP_SENDER_PASSWORD.') from auth_err
