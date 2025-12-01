from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, role='admin', **extra_fields)
      
      

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    joined_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    department = models.CharField(max_length=100, null=True, blank=True)

    
    enrollment_year = models.PositiveIntegerField(null=True, blank=True)
    batch = models.CharField(max_length=50, null=True, blank=True)
    roll_number = models.CharField(max_length=50, null=True, blank=True) 

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teachers = models.ManyToManyField(
        User,
        through='CourseTeacher',
        through_fields=('course', 'teacher'),
        limit_choices_to={'role': 'teacher'},
        related_name='courses'
    )
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        through_fields=('course', 'student'),
        limit_choices_to={'role': 'student'},
        related_name='courses_enrolled'
    )

    def __str__(self):
        return self.title

class CourseTeacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'course') 

    def __str__(self):
        return f"{self.teacher.username} -> {self.course.title}"


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course') 

    def __str__(self):
            return f"{self.student.username} -> {self.course.title} ({self.status})"
    
    
class CourseSchedule(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)

    class Meta:
        unique_together = ('course', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.course.title} on {self.get_day_of_week_display()} from {self.start_time} to {self.end_time} at {self.location}"

class Notification(models.Model):
    NOTIF_TYPE = (
        ('general', 'General'),
        ('course', 'Course'),
        ('enrollment', 'Enrollment'),
        ('account', 'Account'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE, default='general')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    related_enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
