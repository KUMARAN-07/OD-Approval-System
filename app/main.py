# main.py

from fastapi import FastAPI
import logging
from app.routers.student.event_requests import router as student_event_requests_router
from app.routers.auth import student as auth_student
from app.routers.auth import faculty as auth_faculty
from app.routers.auth import admin as auth_admin
from app.routers.events import faculty_events
from app.routers.student import od_applications as student_od
from app.routers.faculty.od_counsellor import router as counsellor_router
from app.routers.faculty.od_academic_head import router as academic_head_router
from app.routers.faculty.event_requests import router as faculty_event_requests_router

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Register role-based auth routers
app.include_router(auth_student.router, tags=["Student Auth"])
app.include_router(auth_faculty.router, tags=["Faculty Auth"])
app.include_router(auth_admin.router, tags=["Admin Auth"])

# Student OD application routes
app.include_router(student_od.router)
app.include_router(student_event_requests_router)
app.include_router(faculty_event_requests_router)

# Faculty event routes
app.include_router(
    faculty_events.router,
    prefix="/faculty/events",
    tags=["Faculty Events"]
)

# Counsellor (Level-1) OD approval routes
app.include_router(counsellor_router)

# Academic Head (Level-2) OD approval routes
app.include_router(academic_head_router)

# Root route for testing
@app.get("/")
def read_root():
    return {"message": "OD System API is running"}
