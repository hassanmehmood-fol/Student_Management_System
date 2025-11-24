# Student Management System

## Description
A comprehensive Django-based Student Management System with REST APIs for managing users (Admin, Teachers, Students), courses, enrollments, schedules, and notifications. Built with Django REST Framework and PostgreSQL.

## Features
- **User Management**: Multi-role system (Admin, Teacher, Student)
- **Course Management**: Create and manage courses with descriptions and duration
- **Enrollment System**: Students can enroll in courses with status tracking (Active, Completed, Dropped)
- **Course Scheduling**: Manage course schedules with day, time, and location
- **Teacher Assignment**: Assign teachers to courses
- **Notifications**: System for sending notifications to users (General, Course, Enrollment, Account related)
- **JWT Authentication**: Secure authentication using JWT tokens
- **API Documentation**: Swagger/OpenAPI documentation with drf-yasg

## Tech Stack
- **Framework**: Django 5.2.8
- **Database**: PostgreSQL
- **API**: Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Documentation**: drf-yasg (Swagger)

## Installed Libraries / Packages
- Django
- djangorestframework
- djangorestframework-simplejwt
- drf-yasg
- psycopg2-binary
- python-dotenv
- PyJWT
- pytz
- sqlparse
- tzdata
- inflection
- packaging
- PyYAML
- uritemplate
- asgiref

## Project Structure
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

## Database Models

### User
- Multi-role authentication system
- Roles: Admin, Teacher, Student
- Fields: username, email, first_name, last_name, role, joined_date, is_active, is_staff

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

## Installation & Setup

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

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration
Create a `.env` file in the project root with PostgreSQL credentials:
```
DBNAME=your_database_name
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432
```

### Step 4: Run Migrations
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

## Admin Panel
- Access Django admin at: `http://localhost:8000/admin/`
- Manage Users, Courses, Teachers, Enrollments, Schedules, and Notifications

## API Endpoints (Available)
- **Admin**: `/admin/` - Django admin panel
- **Swagger Documentation**: `/swagger/` - Interactive API documentation (when running)

## Authentication
- Uses JWT token-based authentication
- Include token in Authorization header: `Authorization: Bearer <your_token>`

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

## Future Enhancements
- Complete REST API endpoints implementation
- Grades and assessment system
- Real-time notifications
- Email notification service
- Student performance analytics
- Course prerequisites
- Payment integration for paid courses

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
