from django.urls import path
from .views import TeacherProfileView

urlpatterns = [
    path('profile/', TeacherProfileView.as_view(), name='teacher-profile'),
]
