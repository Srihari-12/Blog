from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from Backend.schemas.user import EmailRequest, OTPVerifyRequest
from Backend.util.otp_utils import genrate_and_store_otp, verify_otp
from Backend.util.email_utils import send_otp_email
from Backend.util.jwt_utils import create_access_token, verify_token
from Backend.models.user_model import User
from Backend.util.get_db import get_db

router = APIRouter()

# Security scheme that looks for Authorization: Bearer <token>
auth_header = APIKeyHeader(name="Authorization")

@router.post("/send-otp")
def send_otp(request: EmailRequest):
    otp = genrate_and_store_otp(request.email)
    send_otp_email(request.email, otp)
    return {"message": "OTP sent to email"}

@router.post("/verify-otp")
def verify_otp_endpoint(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    if verify_otp(request.email, request.otp):
        # Create user if not exists
        user = db.query(User).filter_by(email=request.email).first()
        if not user:
            user = User(email=request.email)
            db.add(user)
            db.commit()
        # Generate JWT
        token = create_access_token(data={"sub": request.email})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid or expired OTP")

@router.get("/me")
def get_current_user(token: str = Security(auth_header)):
    if token.startswith("Bearer "):
        token = token[7:]
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"email": email}