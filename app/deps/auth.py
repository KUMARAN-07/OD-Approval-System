from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import SECRET_KEY, ALGORITHM

faculty_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/faculty/login",
    scheme_name="FacultyAuth"
)
student_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/student/login",
    scheme_name="StudentAuth"
)
admin_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/admin/login",
    scheme_name="AdminAuth"
)   

def _decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def get_current_faculty(token: str = Depends(faculty_oauth2_scheme)):
    payload = _decode_token(token)
    if payload.get("role") != "FACULTY":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid faculty token")
    return payload["uid"]  # ✅ returns faculty_id directly


def get_current_student(token: str = Depends(student_oauth2_scheme)):
    payload = _decode_token(token)
    if payload.get("role") != "STUDENT":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid student token")
    return payload["uid"]  # ✅ returns registration_number directly


def get_current_admin(token: str = Depends(admin_oauth2_scheme)):
    payload = _decode_token(token)
    if payload.get("role") != "ADMIN":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
    return payload["uid"]  # ✅ returns admin_id directly
