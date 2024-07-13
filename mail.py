# File: mail.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import getenv

def send_mail(email):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(getenv('EMAIL_USERNAME'), getenv('EMAIL_PASSWORD'))

    sender_email = getenv('EMAIL_USERNAME')
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Greetings from John Maxwell"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """Hi There,

    This is a simple salutation email from John Maxwell a DevOps intern in HNG cohort 11. Have a great day!

    Best regards,
    John Maxwell"""
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
