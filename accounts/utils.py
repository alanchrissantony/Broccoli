from email.message import EmailMessage
import smtplib
from datetime import datetime
        

from_mail = 'info.broccoli.smtp@gmail.com'
pass_key = 'dlop lbuy hwnz asvu'


def send_otp(email, otp):
    # Generate OTP (Assuming you have a generate function)
    
    # Format current time
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create EmailMessage object
    msg = EmailMessage()
    msg['Subject'] = 'OTP Verification'
    msg['From'] = from_mail
    msg['To'] = email
    msg.set_content(f"{otp} is SECRET One Time Password for your account verification on Broccoli on {time}. OTP valid for 5 mins. Please do not share OTP with anyone.")

    # Connect to SMTP server and send message
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_mail, pass_key)
        server.send_message(msg)


def send_mail(email, subject, content):
    # Generate OTP (Assuming you have a generate function)
    
    # Format current time
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create EmailMessage object
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = email
    msg.set_content(content)

    # Connect to SMTP server and send message
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_mail, pass_key)
        server.send_message(msg)
