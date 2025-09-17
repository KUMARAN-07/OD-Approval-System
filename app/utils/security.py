import jwt
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRE_HOURS = int(getenv("JWT_EXPIRE_HOURS", 2))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return sample.checkpw(plain_password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return sample.hashpw(password.encode(), sample.gensalt()).decode()


def create_jwt_token(email: str, role: str, user_id: str) -> str:
    """
    user_id = faculty_id for faculty,
              registration_number for students,
              admin_id for admins.
    """
    payload = {
        "sub": email,
        "role": role,
        "uid": user_id,  # ✅ Include unique ID
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
