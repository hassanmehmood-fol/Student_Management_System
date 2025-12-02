from django.urls import path
from .views import TeacherProfileView , TeacherAssignedCoursesView

urlpatterns = [
    path('profile/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('assigned-courses/', TeacherAssignedCoursesView.as_view(),name='teacher-assigned-courses'),
]
