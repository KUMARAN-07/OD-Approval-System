from typing import Annotated
from pydantic import BaseModel, EmailStr, constr

# Define reusable 6-digit OTP string type
OTPStr = Annotated[str, constr(min_length=6, max_length=6)]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp: OTPStr

class PasswordChangeRequest(BaseModel):
    email: EmailStr
    new_password: str
    otp: OTPStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    otp: OTPStr



class StudentProfileResponse(BaseModel):
    registration_number: str
    name: str
    email: EmailStr
    department: str
    year_of_study: int

    class Config:
        orm_mode = True


class AdminProfileResponse(BaseModel):
    admin_id: str
    name: str
    email: EmailStr
    designation: str
    department: str

    class Config:
        orm_mode = True


class FacultyProfileResponse(BaseModel):
    faculty_id: str
    name: str
    email: EmailStr
    designation: str
    department: str

    class Config:
        orm_mode = True