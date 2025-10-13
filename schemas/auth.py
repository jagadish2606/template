from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
