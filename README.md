# Student Management System

## Description
A Django-based Student Management System with REST APIs for managing users (Admin, Teachers, Students), courses, enrollments, schedules, and notifications.
This repository contains a working core data model, admin APIs and a user login endpoint (JWT-based). The project uses Django REST Framework and drf-yasg for API docs.

## Features
- Multi-role user model (admin, teacher, student)
- Courses, enrollments and course schedules models
- Notifications model (per-user notifications)
- Admin-focused APIs for user management, courses, teacher & student profiles
- User login (email + password) which returns JWT access & refresh tokens
- Swagger / Redoc OpenAPI docs via drf-yasg

## Tech stack / dependencies
- Python 3.8+ (project was created for Django 5.x)
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt
- drf-yasg (Swagger / OpenAPI)
- Optional: PostgreSQL for production (project settings read DB details from environment)

## Notes about dependencies
This repository does not provide a pinned `requirements.txt`. If you need reproducible installs please create/commit one (pip freeze > requirements.txt) or add a minimal list before deploying.

## Project structure (important files & apps)
```
Student Management System/
├── core/                          # Core app - Models and Admin
│   ├── models.py                 # User, Course, Enrollment, Schedule, Notification models
│   ├── views.py                  # Core views
│   ├── admin.py                  # Django admin configuration
│   └── migrations/               # Database migrations
├── user/                         # User app
│   ├── views.py                 # User-related views
│   ├── serializer.py            # User serializers
│   └── urls.py                  # User URL patterns
├── Student_Management_System/   # Project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── manage.py                    # Django management command
├── db.sqlite3                   # Database (development)
└── README.md                    # This file
```

## Database models (implemented)

### User
- Implemented as a custom `core.User` model (AUTH_USER_MODEL) with roles: `admin`, `teacher`, `student`.
- Key fields: username, email, first_name, last_name, role, joined_date, enrollment_year, batch, roll_number, is_active, is_staff

### Course
- Course information and management
- Fields: title, description, duration (hours), created_at, updated_at
- Relations: Many-to-Many with Teachers and Students through junction tables

### CourseTeacher
- Links teachers to courses
- Ensures unique assignment of teacher to course
- Tracks assignment date

### Enrollment
- Student enrollment in courses
- Status: Active, Completed, Dropped
- Prevents duplicate enrollments of the same student in the same course
- Tracks enrollment and update dates

### CourseSchedule
- Schedule details for courses
- Fields: day_of_week, start_time, end_time, location
- Supports multiple schedules per course

### Notification
- Notification system for users
- Types: General, Course, Enrollment, Account
- Fields: title, message, is_read, email_sent status
- Can relate to specific courses or enrollments

## Quickstart — local development

The project settings are configured to load database credentials from environment variables (PostgreSQL by default) but there is a `db.sqlite3` file in the repository for a fast local start. Two options:

Option A — Quick local (use the existing SQLite DB as-is):

1. Create & activate a virtual environment

```powershell
# from project root (Windows PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies (if you have a requirements file, otherwise install commonly used packages):

```powershell
pip install django djangorestframework djangorestframework-simplejwt drf-yasg python-dotenv
```

3. Run the development server

```powershell
python manage.py runserver
```

Option B — Configure PostgreSQL (production-like / recommended for deployments)

1. Create a `.env` file with your database and email settings (the project expects these environment variables to be set):

```env
SECRET_KEY=replace-me
DBNAME=your_db_name
USER=your_db_user
PASSWORD=your_db_password
HOST=127.0.0.1
PORT=5432

# Optional email settings used in settings.py
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=top-secret
DEFAULT_FROM_EMAIL=no-reply@example.com
```

2. Install PostgreSQL client binders and other deps:

```powershell
pip install psycopg2-binary
```

3. Run migrations and start the server

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- pip and virtual environment

### Step 1: Clone and Setup Virtual Environment
```bash
# Navigate to project directory
cd "Student Management System"

# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows PowerShell)
venv\Scripts\Activate.ps1
```

## Important: requirements.txt
If you plan to run this on another machine or CI, add a `requirements.txt` to the repo. The project’s README previously referenced `requirements.txt` but the repository currently does not contain one.

### Step 3: Environment configuration
Environment configuration should be stored in a `.env` file (not committed). The `settings.py` reads DB and email settings from environment variables.
```
DBNAME=your_database_name
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432
```

### Example .env (recommended)
Create a `.env` file in the repo root and DO NOT commit this file (it's ignored via .gitignore).
```env
# Django / security
SECRET_KEY=replace_with_a_secure_random_string

# Database
DBNAME=your_database_name
USER=your_db_user
PASSWORD=your_db_password
HOST=127.0.0.1
PORT=5432

# Email (used by admin-create-user to send password)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=secure-password
DEFAULT_FROM_EMAIL=no-reply@example.com

# Optional: allow DEBUG override in .env for local testing
DEBUG=True
```

### Step 4: Run migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Start Development Server
```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000/`

- Access Django admin at: `http://localhost:8000/admin/` (standard Django admin)
- Access Django admin at: `http://localhost:8000/admin/`
- Manage Users, Courses, Teachers, Enrollments, Schedules, and Notifications


## API overview (what is implemented)

- Swagger UI: GET `/swagger/` (interactive API docs)
- Redoc: GET `/redoc/`
- Admin panel: `/admin/` (Django admin UI)

User/API endpoints currently wired in the code (match the implementation):

- POST `/api/user/login/` — user login (email + password) — returns JSON with `access` and `refresh` JWT tokens and basic user info.

Admin-only endpoints (permission class `IsCustomAdmin` required — user.role must be `admin`):

- POST `/api/admin/create-user/` — admin creates a user (username, email, role, first/last name). This _is_ present in `admin.views.AdminCreateUserView`.
- GET `/api/admin/user-list/` — list users (supports `?role=teacher` or `?role=student` to filter)
- `/api/admin/courses/` — ModelViewSet for courses (list, create, retrieve, update, partial_update, destroy)
- `/api/admin/teachers/` — read-only list/detail of users with role `teacher` including their `courses`
- `/api/admin/students/` — admin student CRUD endpoints

Note: The README previously claimed a public register endpoint at `/api/user/register/` — there is no such endpoint in the current code. If you want public self-registration, add a registration view/route.

Notes about admin endpoints: the project contains an admin view to create users programmatically (admin/create-user) but the admin API URL is not currently exposed in `admin/urls.py` or included in the project's `urls.py`. If you want an admin API endpoint, add a path such as `/api/admin/create-user/` in `admin/urls.py` and include it in the project URLs.

## Authentication
- Login returns JWT access & refresh tokens. Include tokens in HTTP requests using the Authorization header like `Authorization: Bearer <access_token>`

Notes and examples:

- If you're using the Swagger / OpenAPI "Authorize" dialog with a Bearer/http bearer scheme, paste ONLY the JWT token (no `Bearer ` prefix). The UI will add the `Bearer ` prefix for you.
- If your Swagger settings use an apiKey field instead, paste the full header value (e.g. `Bearer <your_token>`).

curl example:

```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/some-protected-endpoint/
```

Postman: use a header named `Authorization` with value `Bearer <your_token>` or use the Authorization tab -> Bearer Token field and paste only the token there.

## Configuration Details

### Settings (settings.py)
- **DEBUG**: Currently set to True (change for production)
- **ALLOWED_HOSTS**: Empty (configure for production)
- **Authentication**: JWT via djangorestframework-simplejwt
- **Database**: PostgreSQL configuration from environment variables
- **Custom User Model**: `core.User` as AUTH_USER_MODEL

## Development Notes
- User roles: admin, teacher, student
- Database uses PostgreSQL with environment-based configuration
- SQLite fallback available for quick testing
- All models include timestamp fields (created_at/updated_at where applicable)

## Tests
There are placeholder `tests.py` files in the apps; actual test coverage is not implemented. Running `python manage.py test` will currently run zero tests. Consider adding unit tests for views/serializers and API endpoints.

## Suggestions / notes from this code review
- README referenced `requirements.txt` and a `/api/user/register/` endpoint that do not exist — both have been corrected in this file.
- There are no tests implemented yet — adding tests is recommended.
- `settings.py` contains a hard-coded SECRET_KEY — move that to `.env` and keep it out of source control.
- The project currently expects PostgreSQL in `settings.py` (via environment variables) but a `db.sqlite3` is present for quick local usage — choose one consistent approach for contributors / CI.

## Usage
- Activate virtual environment:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- Run migrations:
  ```bash
  python manage.py migrate
  ```
- Start development server:
  ```bash
  python manage.py runserver
  ```

If you want, I can also:

- add a `requirements.txt` with the most common dependencies,
- implement a lightweight `register` endpoint,
- add initial unit tests for the login flow and admin create-user endpoints.

