# OD System Backend

A FastAPI-based backend for managing On-Duty (OD) applications, event requests, and faculty/student workflows.

## Project Structure

```OD_backend/
├── app/
│   ├── models/
│   │   ├── admin.py
│   │   ├── event_request.py
│   │   ├── event.py
│   │   ├── faculty_student_mapping.py
│   │   ├── faculty.py
│   │   ├── od_application.py
│   │   ├── student.py
│   │   └── user_otp.py
│   ├── repositories/
│   │   ├── events.py
│   │   └── od_applications.py
│   ├── routers/
│   │   ├── auth/
│   │   │   ├── admin.py
│   │   │   ├── faculty.py
│   │   │   └── student.py
│   │   ├── events/
│   │   │   └── faculty_events.py
│   │   ├── faculty/
│   │   │   ├── od_academic_head.py
│   │   │   └── od_counsellor.py
│   │   └── student/
│   │       └── od_applications.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── event.py
│   │   └── od_application.py
│   ├── services/
│   │   ├── events.py
│   │   └── od_applications.py
│   └── utils/
│       ├── database.py
│       ├── email.py
│       ├── security.py
│       └── validators.py
└── main.py
```

## Features

- **Authentication:** Role-based JWT authentication for students, faculty, and admins.
- **Event Management:** Faculty can create, update, and delete events.
- **OD Applications:** Students can apply for OD; counsellors and academic heads review applications.
- **Event Requests:** Students submit event requests; faculty review and approve/reject.
- **Email Notifications:** Configurable via `.env`.

## Setup

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd OD_backend
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Edit `.env` for database, JWT, and email settings.

4. **Run database migrations**
   - Ensure your MySQL server is running and the database exists.
   - Use Alembic or SQLAlchemy to create tables (not included in this repo).

5. **Start the server**
   ```sh
   uvicorn app.main:app --reload
   ```

## Usage

- **API Documentation:** Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.
- **Authentication:** Use login endpoints to obtain JWT tokens for each role.
- **Student Endpoints:**
  - `/student/od/apply` — Apply for OD
  - `/student/event-requests/` — Submit event request
- **Faculty Endpoints:**
  - `/faculty/events/` — Manage events
  - `/faculty/event-requests/pending` — Review event requests

## Development

- **Password Hashing:** Use `bcrypt.py` to generate password hashes for DB insertion.
- **Testing:** Add unit tests in the `tests/` directory (not included).

## License

MIT License

---

**Note:** For full details on each endpoint and workflow, see the [app/routers](app/routers) and [app/services](app/services) modules.
