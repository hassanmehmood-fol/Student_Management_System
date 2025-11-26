from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from user.serializer import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user.permissions import IsCustomAdmin


class RegisterView(APIView):
    permission_classes = [IsCustomAdmin]  
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=RegisterSerializer, tags=['User Register'])
    def post(self, request):
        # Ensure role is valid
        role = request.data.get('role')
        if role not in ['teacher', 'student']:
            return Response({"error": "Role must be teacher or student"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]  
    authentication_classes = [] 

    @swagger_auto_schema(request_body=LoginSerializer , tags=['User Login'])  
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Login successful",
                "user": serializer.validated_data['user'],
                "access": serializer.validated_data['access'],
                "refresh": serializer.validated_data['refresh']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
