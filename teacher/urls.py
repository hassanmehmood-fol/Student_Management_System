from django.urls import path
from .views import (
    TeacherProfileView,
    TeacherAssignedCoursesView,
    TeacherCoursesWithStudentsView,
    TeacherEnrollStudentView,
    TeacherRemoveStudentView
)

urlpatterns = [
    path('profile/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('assigned-courses/', TeacherAssignedCoursesView.as_view(), name='teacher-assigned-courses'),
    path('courses-with-students/', TeacherCoursesWithStudentsView.as_view(), name='teacher-courses-with-students'),

    path('enroll-student/', TeacherEnrollStudentView.as_view(), name='teacher-enroll-student'),
    path('remove-student/', TeacherRemoveStudentView.as_view(), name='teacher-remove-student'),
]
