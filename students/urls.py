from django.urls import path
from .views import StudentProfileView , StudentEnrolledCoursesView

urlpatterns = [
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
    path('enrolled-courses/', StudentEnrolledCoursesView.as_view(), name='student-enrolled-courses'),

]
