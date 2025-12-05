from django.urls import path, include
from rest_framework.routers import DefaultRouter
from admin.views import (
    AdminCreateUserView,
    UserListView,
    CourseViewSet,
    TeacherProfileViewSet,
    StudentProfileViewSet,
    CourseScheduleViewSet,
    EnrollStudentView,
    AdminUnenrollStudentView  
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'teachers', TeacherProfileViewSet, basename='teachers')
router.register(r'students', StudentProfileViewSet, basename='students')
router.register(r'course-schedules', CourseScheduleViewSet, basename='course-schedule')

urlpatterns = [
    path('create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('user-list/', UserListView.as_view(), name='admin-user-list'),
    path('enroll-student/', EnrollStudentView.as_view(), name='enroll-student'),
    path('unenroll-student/', AdminUnenrollStudentView.as_view(), name='unenroll-student'),  # <- new path
    path('', include(router.urls))
]
