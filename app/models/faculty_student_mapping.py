# app/models/faculty_student_mapping.py
from sqlalchemy import Column, String, ForeignKey
from app.database import Base

class FacultyStudentMapping(Base):
    __tablename__ = "faculty_student_mapping"

    registration_number = Column(String(20), ForeignKey("students.registration_number", ondelete="CASCADE"), primary_key=True)
    counsellor_id = Column(String(20), ForeignKey("faculty.faculty_id", ondelete="CASCADE"))
