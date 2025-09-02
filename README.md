# Zavrsni Backend

## Overview
This is a FastAPI backend for a medication reminder web application. It supports user registration, authentication (JWT), medication management, reminders, and admin approval workflows. The backend uses PostgreSQL, SQLAlchemy ORM, Alembic migrations, and supports both user and admin roles.

## Features
- User registration and login (JWT authentication)
- Admin and user role separation
- Medication management (users can request new meds, admin approves)
- Reminder scheduling and email notifications
- CRUD operations for users, medications, and reminders
- Import medications and active substances from Excel
- Secure API endpoints (role-based access)
- Docker-ready structure

## Project Structure
```
src/
    api/                # FastAPI routers
    models/             # SQLAlchemy models
    schemas/            # Pydantic schemas
    services/           # Business logic/services
    db/                 # Database config and migrations
    utils/              # Utility functions (auth, dependencies, mail)
    main.py             # FastAPI app entry point
```

## Setup Instructions
### 1. Clone the repository
```sh
git clone <repo-url>
cd zavrsni-backend
```

### 2. Create and activate a virtual environment
```sh
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root with your settings:
```
DATABASE_URL=postgresql://user:password@localhost:5432/zavrsni
SECRET_KEY=your_jwt_secret
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
```

### 5. Run Alembic migrations
```sh
alembic upgrade head
```

### 6. Start the backend
```sh
uvicorn src.main:app --reload
```

## API Endpoints
- `/auth/register` - Register new user
- `/auth/login` - Login and get JWT token
- `/user/me` - Get/update/delete own user info
- `/user` - Admin: get all users
- `/lijek` - Get all medications
- `/lijek` (POST) - Request new medication (user)
- `/lijek/{id}/approve` - Approve medication (admin)
- `/lijek/requests` - Get all requested meds (admin)
- `/korisnik-lijek` - Get all reminders for logged-in user
- `/korisnik-lijek/{lijek_id}` - Get/update/delete reminder for user

## Importing Medications from Excel
- Use the provided service to import medications and active substances from Excel files. Imported medications are automatically set as accepted.

## Reminder Scheduler
- Reminders are processed via APScheduler and sent to users via email.
- Scheduler runs in the background and checks for due reminders every minute.

## Docker Support
- Add a `Dockerfile` and `docker-compose.yml` for containerized deployment (not included by default).

## Testing
- Use pytest for unit and integration tests.
- Example: `pytest src/tests/`

## License
MIT

## Author
pgrasic
