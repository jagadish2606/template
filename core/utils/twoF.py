import random, smtplib, os
from twilio.rest import Client
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def generate_otp():
    return str(random.randint(100000, 999999))

# def send_email_otp(email: str, otp: str):
#     msg = EmailMessage()
#     msg['Subject'] = "Your 2FA Verification Code"
#     msg['From'] = os.getenv("EMAIL_USER")
#     msg['To'] = email
#     msg.set_content(f"Your OTP code is: {otp}")
    
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
#         smtp.send_message(msg)

def send_email_otp(email: str, otp: str):
    msg = EmailMessage()
    msg['Subject'] = "Devora Technologies: Your Secure Login OTP"
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = email
    
    # Professional message content
    msg.set_content(f"""
Hello,

Your One-Time Password (OTP) for logging into your Devora Technologies account is:

    {otp}

This OTP is valid for the next 10 minutes. Please do not share this code with anyone.

If you did not request this OTP, please ignore this email or contact our support team immediately.

Thank you,
Devora Technologies Team
""")
    
    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)
        print(f"OTP sent successfully to {email}")


load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_phone = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

def send_sms_otp(to_phone: str, otp: str):
    message = client.messages.create(
        body=f"Your verification code is {otp}",
        from_=from_phone,
        to=to_phone
    )
    return message.sid
