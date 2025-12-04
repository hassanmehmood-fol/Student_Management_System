from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from core.models import User, Course

@shared_task
def send_user_credentials_email(email, username, password):
    subject = "Your Account Credentials"
    message = f"""
    Hello {username},

    Your account has been created successfully.
    Login credentials:

    Email: {email}
    Password: {password}

    Please login and change your password after first login.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@shared_task
def send_enrollment_email(student_id, course_id):
    student = User.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    

    subject_student = f"Enrolled in {course.title}"
    message_student = f"Hello {student.username},\n\nYou have been successfully enrolled in the course: {course.title}."
    send_mail(subject_student, message_student, 'noreply@example.com', [student.email])
    
    for teacher in course.teachers.all():
        subject_teacher = f"New Student Enrolled in {course.title}"
        message_teacher = f"Hello {teacher.username},\n\nStudent {student.username} has enrolled in your course: {course.title}."
        send_mail(subject_teacher, message_teacher, 'noreply@example.com', [teacher.email])