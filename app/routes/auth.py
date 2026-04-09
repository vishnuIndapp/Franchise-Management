from app.core.database import get_db
from app.services.auth_service import login_user, get_users
from app.services.otp_service import send_otp,verify_otp
from app.schemas.auth import LoginRequest, LoginResponse,SendOTPRequest,VerifyOTPRequest
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password,verify_password
from app.core.config import settings
from jose import jwt
router= APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db=Depends(get_db)):
    token = login_user(db, request.email, request.password, request.franchise_code)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")    
    return LoginResponse(access_token=token["access_token"],refresh_token=token["refresh_token"], token_type="bearer",role=token["role"])



@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return {
        "count": len(users),
        "data": users
    }


@router.post("/send-otp")
def send_otp_api(request: SendOTPRequest):
    sucess = send_otp(request.email)
    if not sucess:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP")
    return {"message": "OTP sent successfully"}


@router.post("/verify-otp")
def verify_otp_api(request: VerifyOTPRequest):
    valid = verify_otp(request.email, request.otp)
    if not valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
    return {"message": "OTP verified successfully"}