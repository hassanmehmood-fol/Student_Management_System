from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from admin.views import AdminCreateUserView , UserListView  , CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('user-list/', UserListView.as_view(), name='admin-user-list'),
    
    
     path('', include(router.urls))
]
