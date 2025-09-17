# app/models/admin.py
from sqlalchemy import Column, String
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    email = Column(String(255), primary_key=True, index=True)
    password_hash = Column(String(255), nullable=False)