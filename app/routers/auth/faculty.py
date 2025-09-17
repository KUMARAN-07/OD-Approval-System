# app/routers/auth_faculty.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.schemas.auth import (
    LoginResponse,
    OTPVerificationRequest,
    PasswordChangeRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    FacultyProfileResponse,
)
from app.utils.security import verify_password, hash_password, create_jwt_token
from app.utils.email import send_otp_email
from app.database import get_db
from app.models.faculty import Faculty
from app.models.user_otp import UserOTP, UserRoleEnum
from app.deps.auth import get_current_faculty

router = APIRouter(
    prefix="/auth/faculty",
)


@router.post("/login", response_model=LoginResponse)
def faculty_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.email == form_data.username).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    if not verify_password(form_data.password, faculty.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # If password already set, issue JWT
    if faculty.is_password_reset:
        token = create_jwt_token(
            email=faculty.email,
            role="FACULTY",
            user_id=faculty.faculty_id
        )
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    # First-time login: Send OTP to set password
    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=5)

    db.query(UserOTP).filter_by(
        email=faculty.email,
        role=UserRoleEnum.FACULTY,
        is_used=False
    ).delete()
    db.add(UserOTP(
        email=faculty.email,
        role=UserRoleEnum.FACULTY,
        otp_code=otp,
        otp_expiry=expiry
    ))
    db.commit()

    send_otp_email(faculty.email, otp)
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="OTP sent to your college email. Please verify."
    )


@router.post("/verify-otp")
def verify_faculty_otp(
    request: OTPVerificationRequest,
    db: Session = Depends(get_db)
):
    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.FACULTY,
        otp_code=request.otp,
        is_used=False
    ).first()

    if not otp_record or datetime.utcnow() > otp_record.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    otp_record.is_used = True
    db.commit()
    return {"message": "OTP verified. You may now reset your password."}


@router.post("/change-password")
def change_faculty_password(
    request: PasswordChangeRequest,
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.email == request.email).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.FACULTY,
        otp_code=request.otp,
        is_used=True
    ).first()
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not verified"
        )

    faculty.password_hash = hash_password(request.new_password)
    faculty.is_password_reset = True
    db.commit()
    return {"message": "Password changed successfully. You can now log in."}


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.email == request.email).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=10)

    db.query(UserOTP).filter_by(
        email=faculty.email,
        role=UserRoleEnum.FACULTY,
        is_used=False
    ).delete()
    db.add(UserOTP(
        email=faculty.email,
        role=UserRoleEnum.FACULTY,
        otp_code=otp,
        otp_expiry=expiry
    ))
    db.commit()

    send_otp_email(faculty.email, otp)
    return {"message": "OTP sent to your registered email."}


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.email == request.email).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.FACULTY,
        otp_code=request.otp,
        is_used=False
    ).first()

    if not otp_record or datetime.utcnow() > otp_record.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    otp_record.is_used = True
    faculty.password_hash = hash_password(request.new_password)
    faculty.is_password_reset = True
    faculty.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Password has been reset successfully."}


@router.get(
    "/me",
    response_model=FacultyProfileResponse,
    summary="Get current faculty’s profile"
)
def read_current_faculty(
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    return faculty
