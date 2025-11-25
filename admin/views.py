from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from user.serializer import AdminCreateUserSerializer

class AdminCreateUserView(APIView):
    permission_classes = [permissions.IsAdminUser]  

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
