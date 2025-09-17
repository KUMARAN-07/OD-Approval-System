# app/routers/auth_admin.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import LoginResponse, AdminProfileResponse
from app.utils.security import verify_password, create_jwt_token
from app.database import get_db
from app.models.admin import Admin
from app.deps.auth import get_current_admin

router = APIRouter(
    prefix="/auth/admin",
)


@router.post("/login", response_model=LoginResponse)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # form_data.username holds the email
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    if not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_jwt_token(
        email=admin.email,
        role="ADMIN",
        user_id=admin.admin_id
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=AdminProfileResponse,
    summary="Get current admin’s profile"
)
def read_current_admin(
    admin_id: str = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin
