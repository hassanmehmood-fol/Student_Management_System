from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from core.models import User, Course, Notification

def create_notification(user, title, message, notif_type='general', related_course=None):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type,
        related_course=related_course,
        email_sent=True
    )

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

    user = User.objects.get(email=email)
    create_notification(user, subject, message, notif_type='credentials')

@shared_task
def send_enrollment_email(student_id, course_id):
    student = User.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    
    subject_student = f"Enrolled in {course.title}"
    message_student = f"Hello {student.username},\n\nYou have been successfully enrolled in the course: {course.title}."
    send_mail(subject_student, message_student, 'noreply@example.com', [student.email])
    
    try:
        create_notification(student, subject_student, message_student, notif_type='enrollment', related_course=course)
    except Exception as e:
        print(f"Failed to create notification for student {student.id}: {e}")
    
    for teacher in course.teachers.all():
        subject_teacher = f"New Student Enrolled in {course.title}"
        message_teacher = f"Hello {teacher.username},\n\nStudent {student.username} has enrolled in your course: {course.title}."
        send_mail(subject_teacher, message_teacher, 'noreply@example.com', [teacher.email])
        
        try:
            create_notification(teacher, subject_teacher, message_teacher, notif_type='enrollment', related_course=course)
        except Exception as e:
            print(f"Failed to create notification for teacher {teacher.id}: {e}")
      
@shared_task
def send_unenrollment_email(student_id, course_id):
    student = User.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    
    subject_student = f"Removed from {course.title}"
    message_student = f"Hello {student.username},\n\nYou have been removed from the course: {course.title}."
    send_mail(subject_student, message_student, 'noreply@example.com', [student.email])
    create_notification(student, subject_student, message_student, notif_type='unenrollment', related_course=course)
    
    for teacher in course.teachers.all():
        subject_teacher = f"Student Removed from {course.title}"
        message_teacher = f"Hello {teacher.username},\n\nStudent {student.username} has been removed from your course: {course.title}."
        send_mail(subject_teacher, message_teacher, 'noreply@example.com', [teacher.email])
        create_notification(teacher, subject_teacher, message_teacher, notif_type='unenrollment', related_course=course)

@shared_task
def send_teacher_assignment_email(teacher_id, course_id):
    teacher = User.objects.get(id=teacher_id)
    course = Course.objects.get(id=course_id)
    
    subject = f"You have been assigned to {course.title}"
    message = f"""
Hello {teacher.username},

You have been assigned to teach the course: {course.title}.
"""
    send_mail(subject, message, 'noreply@example.com', [teacher.email], fail_silently=False)
    create_notification(teacher, subject, message, notif_type='course', related_course=course)
