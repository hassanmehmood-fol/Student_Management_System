# Student Management System

## 📋 Overview

A comprehensive Django-based Student Management System with REST APIs for managing users (Admin, Teachers, Students), courses, enrollments, schedules, and notifications. Built with Django REST Framework, JWT authentication, and asynchronous email notifications using Celery and Redis.

## ✨ Key Features

- **Multi-Role User Management**: Admin, Teacher, and Student roles with role-based access control
- **Course Management**: Create, manage, and assign courses to teachers
- **Student Enrollment**: Manage student enrollments with status tracking (active, completed, dropped)
- **Course Scheduling**: Schedule courses with day, time, and location details
- **Notifications System**: Per-user notifications with categorization (general, course, enrollment, account)
- **Asynchronous Email Notifications**: Automated email sending via Celery and Redis
- **JWT Authentication**: Secure token-based authentication for all API endpoints
- **API Documentation**: Interactive Swagger/Redoc docs via drf-yasg
- **Database Flexibility**: PostgreSQL for production, SQLite for development

## 🛠️ Tech Stack

- **Python 3.8+** with Django 5.x
- **Django REST Framework** - RESTful API development
- **djangorestframework-simplejwt** - JWT authentication
- **drf-yasg** - Swagger/OpenAPI documentation
- **Celery** - Asynchronous task queue
- **Redis** - Message broker and result backend
- **PostgreSQL** - Production database
- **SQLite** - Development database

---

## 📦 Project Structure

```
Student Management System/
├── admin/                              # Admin app - User and course management
│   ├── views.py                       # Admin API views
│   ├── serializers.py                 # Serializers for admin operations
│   ├── urls.py                        # Admin URL routes
│   ├── task.py                        # Celery email tasks
│   ├── permissions.py                 # Admin permissions
│   └── migrations/                    # Database migrations
│
├── core/                               # Core app - Models
│   ├── models.py                      # User, Course, Enrollment, Schedule, Notification models
│   ├── admin.py                       # Django admin configuration
│   ├── views.py                       # Core views
│   └── migrations/                    # Database migrations
│
├── user/                               # User app - Authentication
│   ├── views.py                       # Login API view
│   ├── serializer.py                  # Login serializer
│   ├── urls.py                        # User URL routes
│   ├── permissions.py                 # Custom permissions
│   └── migrations/                    # Database migrations
│
├── teacher/                            # Teacher app - Teacher-specific APIs
│   ├── views.py                       # Teacher profile and course management
│   ├── serializers.py                 # Teacher serializers
│   ├── urls.py                        # Teacher URL routes
│   ├── permissions.py                 # Teacher permissions
│   └── migrations/                    # Database migrations
│
├── students/                           # Student app - Student-specific APIs
│   ├── views.py                       # Student profile and enrollment views
│   ├── serializers.py                 # Student serializers
│   ├── urls.py                        # Student URL routes
│   ├── permissions.py                 # Student permissions
│   └── migrations/                    # Database migrations
│
├── Student_Management_System/         # Project configuration
│   ├── settings.py                    # Django settings, Celery config
│   ├── urls.py                        # Main URL configuration
│   ├── celery.py                      # Celery initialization
│   ├── asgi.py                        # ASGI configuration
│   └── wsgi.py                        # WSGI configuration
│
├── manage.py                          # Django management command
├── db.sqlite3                         # Development database
└── README.md                          # This file
```

---

## 📊 Database Models

### User Model
- **Custom Authentication Model** (AUTH_USER_MODEL)
- **Fields**: username, email, first_name, last_name, role, joined_date, enrollment_year, batch, roll_number, department, is_active, is_staff
- **Roles**: admin, teacher, student
- **Key Methods**: User creation and superuser creation via UserManager

### Course Model
- **Fields**: title, description, duration (hours), created_at, updated_at
- **Relations**: Many-to-Many with Teachers (through CourseTeacher) and Students (through Enrollment)
- **Functionality**: Complete course lifecycle management

### CourseTeacher Model
- **Purpose**: Links teachers to courses
- **Constraints**: Unique constraint on (teacher, course) pair
- **Fields**: teacher (FK), course (FK), assigned_at
- **Use Case**: Assign specific teachers to specific courses

### Enrollment Model
- **Purpose**: Manages student enrollment in courses
- **Status Choices**: active, completed, dropped
- **Fields**: student (FK), course (FK), status, enrolled_at, updated_at
- **Constraints**: Unique constraint on (student, course) pair
- **Tracking**: Maintains enrollment history with timestamps

### CourseSchedule Model
- **Purpose**: Define course schedule and location
- **Fields**: course (FK), teacher (FK), day_of_week, start_time, end_time, location
- **Days**: Monday through Sunday
- **Constraints**: Unique constraint on (course, teacher, day_of_week, start_time, end_time)
- **Use Case**: Multi-section scheduling, timetable management

### Notification Model
- **Purpose**: In-app notifications for users
- **Types**: general, course, enrollment, account
- **Fields**: user (FK), notif_type, title, message, is_read, email_sent, created_at, related_course (FK), related_enrollment (FK)
- **Tracking**: Tracks read status and email delivery status

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Redis (for Celery task queue)
- pip and virtual environment

### Step 1: Clone and Setup Virtual Environment

```powershell
# Navigate to project directory
cd "Student Management System"

# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows PowerShell)
venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
pip install django djangorestframework djangorestframework-simplejwt drf-yasg python-dotenv celery redis psycopg2-binary
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root (do NOT commit this file):

```env
# Django / Security
SECRET_KEY=your-secure-secret-key-here

# Database Configuration
DBNAME=your_database_name
USER=your_db_user
PASSWORD=your_database_password
HOST=127.0.0.1
PORT=5432

# Email Configuration (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Optional
DEBUG=True
```

### Step 4: Run Database Migrations

```powershell
python manage.py migrate
```

### Step 5: Create Superuser

```powershell
python manage.py createsuperuser
```

### Step 6: Start Development Server

```powershell
python manage.py runserver
```

Server available at `http://localhost:8000/`

---

## 🔧 Celery & Redis Configuration

### What is Celery?
Celery is an asynchronous task queue that allows long-running operations (like sending emails) to be executed in the background without blocking the main application.

### What is Redis?
Redis is an in-memory data store used as a message broker for Celery. It manages the task queue and stores task results.

### Configuration Details

**Location**: `Student_Management_System/settings.py`

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'
```

### Celery Initialization

**Location**: `Student_Management_System/celery.py`

```python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Student_Management_System.settings')

app = Celery('Student_Management_System')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Auto-discovers @shared_task decorators in all apps
```

### Email Tasks (Celery)

**Location**: `admin/task.py`

Available async email tasks:

1. **send_user_credentials_email** - Sends login credentials when admin creates a user
2. **send_enrollment_email** - Notifies student and teachers when enrollment is created
3. **send_unenrollment_email** - Notifies student and teachers when enrollment is removed
4. **send_teacher_assignment_email** - Notifies teacher when assigned to a course

### How to Run Celery Worker (Development)

```powershell
# Start Celery worker
celery -A Student_Management_System worker --loglevel=info
```

### How to Run Celery Beat (Scheduled Tasks - Optional)

For periodic tasks (if needed in future):

```powershell
celery -A Student_Management_System beat --loglevel=info
```

---

## 🐳 Docker & Docker Compose Setup

### Running with Docker Compose

Docker allows containerization of the application with all dependencies (Django, PostgreSQL, Redis, Celery).

### Dockerfile Example

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "Student_Management_System.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Docker Compose Configuration Example

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DBNAME}
      POSTGRES_USER: ${USER}
      POSTGRES_PASSWORD: ${PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis Cache & Message Broker
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Django Web Server
  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      - DBNAME=${DBNAME}
      - USER=${USER}
      - PASSWORD=${PASSWORD}
      - HOST=db
      - PORT=5432
      - EMAIL_HOST=${EMAIL_HOST}
      - EMAIL_PORT=${EMAIL_PORT}
      - EMAIL_USE_TLS=${EMAIL_USE_TLS}
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
      - DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  # Celery Worker
  celery:
    build: .
    command: celery -A Student_Management_System worker --loglevel=info
    environment:
      - DBNAME=${DBNAME}
      - USER=${USER}
      - PASSWORD=${PASSWORD}
      - HOST=db
      - PORT=5432
      - EMAIL_HOST=${EMAIL_HOST}
      - EMAIL_PORT=${EMAIL_PORT}
      - EMAIL_USE_TLS=${EMAIL_USE_TLS}
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
      - DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

### Running with Docker Compose

```powershell
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache
```

---

## 🔐 Authentication & Authorization

### JWT (JSON Web Tokens)

**Authentication Flow**:
1. User logs in with email and password at `POST /api/user/login/`
2. Server returns `access_token` and `refresh_token`
3. Client includes token in Authorization header: `Authorization: Bearer <access_token>`

**JWT Configuration** (settings.py):

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Role-Based Permissions

**Available Roles**:
- **admin** - Full system access
- **teacher** - Can manage assigned courses and students
- **student** - Can view enrolled courses and profile

**Permission Classes**:
- `IsCustomAdmin` - Admin-only access
- `IsTeacherAndOwner` - Teacher-only access to own profile
- `IsStudent` - Student-only access

---

## 📡 API Overview

### Public Endpoints
- `POST /api/user/login/` - User login (returns JWT tokens)

### Admin Endpoints (requires admin role)
- `POST /api/admin/create-user/` - Create user (student/teacher)
- `GET /api/admin/user-list/` - List users (supports role filtering)
- `GET /api/admin/courses/` - List courses
- `POST /api/admin/courses/` - Create course
- `GET /api/admin/courses/{id}/` - Course details
- `PUT /api/admin/courses/{id}/` - Update course
- `DELETE /api/admin/courses/{id}/` - Delete course
- `POST /api/admin/enroll-student/` - Enroll student in course
- `POST /api/admin/unenroll-student/` - Remove student from course
- `POST /api/admin/assign-teacher/` - Assign teacher to course

### Teacher Endpoints (requires teacher role)
- `GET /api/teacher/profile/` - Get teacher profile
- `PUT /api/teacher/profile/` - Update teacher profile
- `GET /api/teacher/courses/` - List assigned courses
- `GET /api/teacher/courses/{id}/` - Course details with enrolled students

### Student Endpoints (requires student role)
- `GET /api/students/profile/` - Get student profile
- `PUT /api/students/profile/` - Update student profile
- `GET /api/students/enrolled-courses/` - List enrolled courses

### Documentation
- `GET /swagger/` - Interactive API documentation (Swagger UI)
- `GET /redoc/` - Alternative API documentation (ReDoc)
- `GET /admin/` - Django admin panel

---

## 📧 Email Configuration

### Setting Up Gmail SMTP

1. Enable 2-Step Verification on your Google Account
2. Generate App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select Mail and Windows Computer
   - Copy the generated 16-character password
3. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   ```

### Email Events Triggered

1. **User Registration** - Admin creates new user → Credentials sent to email
2. **Course Enrollment** - Student enrolled in course → Notifications sent to student and teachers
3. **Course Unenrollment** - Student removed from course → Notifications sent
4. **Teacher Assignment** - Teacher assigned to course → Notification sent

---

## 🔍 Troubleshooting

### Celery Not Processing Tasks

```powershell
# Restart Celery worker
celery -A Student_Management_System worker --loglevel=info

# Check Redis connection
redis-cli ping
# Should return: PONG
```

### Redis Connection Error

```powershell
# Check if Redis is running
redis-cli ping

# Start Redis (Windows)
redis-server
```

### Database Migration Issues

```powershell
# Reset migrations (development only)
python manage.py migrate admin zero

# Remake migrations
python manage.py makemigrations
python manage.py migrate
```

### PostgreSQL Connection Error

```powershell
# Verify credentials in .env file
# Check PostgreSQL is running
# Verify host and port (default: localhost:5432)
```

---

## 📝 Development Notes

- All models include timestamp fields for audit trails
- Custom User model with role-based differentiation
- Asynchronous email processing prevents API blocking
- Tests are placeholder files - implement comprehensive test coverage
- Project follows Django best practices

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes and test thoroughly
3. Ensure Celery tasks are working correctly
4. Submit pull request with documentation

---

## 📄 License

This project is proprietary. Please see LICENSE file for details.

---

## ✅ Checklist for Production Deployment

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Move `SECRET_KEY` to `.env` file
- [ ] Set up SSL/HTTPS
- [ ] Configure PostgreSQL with proper backups
- [ ] Set up Redis with persistence
- [ ] Configure Celery worker auto-restart
- [ ] Set up application monitoring and logging
- [ ] Run `python manage.py collectstatic`
- [ ] Configure email service credentials securely
- [ ] Set up regular database backups
- [ ] Configure CORS if frontend is separate domain

---

**Last Updated**: December 5, 2025
