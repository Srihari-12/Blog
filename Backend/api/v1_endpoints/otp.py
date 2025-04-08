from fastapi import APIRouter, Depends, HTTPException
from Backend.schemas.user import EmailRequest, OTPVerifyRequest
from Backend.util.otp_utils import genrate_and_store_otp, verify_otp
from Backend.util.email_utils import send_otp_email
from Backend.util.jwt_utils import create_access_token
from Backend.models.user_model import User
from Backend.util.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/send-otp")
def send_otp(request: EmailRequest):
    otp = genrate_and_store_otp(request.email)
    send_otp_email(request.email, otp)
    return {"message": "OTP sent"}

@router.post("/verify-otp")
def verify(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    if verify_otp(request.email, request.otp):
        user = db.query(User).filter_by(email=request.email).first()
        if not user:
            user = User(email=request.email)
            db.add(user)
            db.commit()
        token = create_access_token(request.email)
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid OTP")
