from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models.student import Student
from app.models.user_otp import UserOTP, UserRoleEnum
from app.schemas.auth import (
    LoginResponse,
    OTPVerificationRequest,
    PasswordChangeRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    StudentProfileResponse,
)
from app.utils.security import verify_password, hash_password, create_jwt_token
from app.utils.email import send_otp_email
from app.deps.auth import get_current_student

router = APIRouter(
    prefix="/auth/student",
    
)


@router.post("/login", response_model=LoginResponse)
def student_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == form_data.username).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if not verify_password(form_data.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if student.is_password_reset:
        token = create_jwt_token(
            email=student.email,
            role="STUDENT",
            user_id=student.registration_number
        )
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    # First login: Send OTP to set password
    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=5)

    db.query(UserOTP).filter_by(
        email=student.email,
        role=UserRoleEnum.STUDENT,
        is_used=False
    ).delete()

    db.add(UserOTP(
        email=student.email,
        role=UserRoleEnum.STUDENT,
        otp_code=otp,
        otp_expiry=expiry
    ))
    db.commit()

    send_otp_email(student.email, otp)
    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="OTP sent to your college email. Please verify."
    )


@router.post("/verify-otp")
def verify_student_otp(
    request: OTPVerificationRequest,
    db: Session = Depends(get_db)
):
    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.STUDENT,
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
def change_student_password(
    request: PasswordChangeRequest,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == request.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.STUDENT,
        otp_code=request.otp,
        is_used=True
    ).first()
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not verified"
        )

    student.password_hash = hash_password(request.new_password)
    student.is_password_reset = True
    db.commit()
    return {"message": "Password changed successfully. You can now log in."}


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == request.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=10)

    db.query(UserOTP).filter_by(
        email=student.email,
        role=UserRoleEnum.STUDENT,
        is_used=False
    ).delete()

    db.add(UserOTP(
        email=student.email,
        role=UserRoleEnum.STUDENT,
        otp_code=otp,
        otp_expiry=expiry
    ))
    db.commit()

    send_otp_email(student.email, otp)
    return {"message": "OTP sent to your registered email."}


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == request.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    otp_record = db.query(UserOTP).filter_by(
        email=request.email,
        role=UserRoleEnum.STUDENT,
        otp_code=request.otp,
        is_used=False
    ).first()

    if not otp_record or datetime.utcnow() > otp_record.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    otp_record.is_used = True
    student.password_hash = hash_password(request.new_password)
    student.is_password_reset = True
    student.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Password has been reset successfully."}


@router.get(
    "/me",
    response_model=StudentProfileResponse,
    summary="Get current student profile"
)
def read_current_student(
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.registration_number == registration_number).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student
