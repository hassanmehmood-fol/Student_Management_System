from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from admin.serializers import AdminCreateUserSerializer
from drf_yasg.utils import swagger_auto_schema
from user.permissions import IsCustomAdmin

class AdminCreateUserView(APIView):
    permission_classes = [IsCustomAdmin]
 
    
    @swagger_auto_schema(request_body=AdminCreateUserSerializer , tags=['Admin Create User'])  
    def post(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
