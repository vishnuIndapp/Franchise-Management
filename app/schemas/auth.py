from pydantic import BaseModel,EmailStr,Field
from typing import Optional



class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6) 
    franchise_code: Optional[str] = Field(None, description="Required for franchise users")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    role: str


class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str 