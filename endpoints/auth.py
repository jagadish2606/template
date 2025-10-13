from fastapi import APIRouter, HTTPException

from schemas.auth import LoginRequest, OTPVerifyRequest
from core.utils.twoF import generate_otp, send_email_otp, send_sms_otp

router = APIRouter()

# Simulate a temporary store (can replace with Redis)
otp_store = {}

@router.post("/login")
def login(data: LoginRequest):
    print(f"data{data}")
    # TODO: Replace with real user verification (DB)
    if data.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    otp = generate_otp()
    otp_store[data.email] = otp

    send_email_otp(data.email, otp)
    # send_sms_otp(data.phone, otp)

    return {"message": "OTP sent to your email and phone."}

@router.post("/verify-otp")
def verify_otp(data: OTPVerifyRequest):
    stored_otp = otp_store.get(data.email)
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # OTP valid — delete it
    del otp_store[data.email]
    return {"message": "2FA successful. User authenticated!"}
