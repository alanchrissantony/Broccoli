from datetime import datetime, timedelta
from email.message import EmailMessage
import pyotp, smtplib



from_mail = 'info.broccoli.smtp@gmail.com'
pass_key = 'dlop lbuy hwnz asvu'

def send(request, email):
    # Generate OTP (Assuming you have a generate function)
    otp = generate(request)
    
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

def verify(request, otp):
    otp_secret_key = request.session['otp_secret_key']
    valid_date = request.session['otp_valid_date']

    if otp_secret_key and valid_date is not None:
        valid_date = datetime.fromisoformat(request.session['otp_valid_date'])

        if valid_date > datetime.now():
            totp = pyotp.TOTP(otp_secret_key, interval=300)
            return totp.verify(otp)




def generate(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)
    return otp
    