from rest_framework import generics , status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import TeacherOwnProfileSerializer ,TeacherAssignedCourseSerializer , TeacherCourseWithStudentsSerializer , TeacherEnrollStudentSerializer , StudentDetailSerializer
from .permissions import IsTeacherAndOwner
from core.models import Course , User , Enrollment
from teacher.permissions import IsTeacherAndOwner
from rest_framework.response import Response
from drf_yasg import openapi
from admin.task import send_unenrollment_email , send_enrollment_email


class TeacherProfileView(generics.RetrieveUpdateAPIView):
    """
    View/Edit own profile (Teacher only).
    Email is non-editable.
    """
    serializer_class = TeacherOwnProfileSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    def get_object(self):
      
        return self.request.user

    @swagger_auto_schema(tags=["Get Teacher Profile (self)"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Update Teacher Profile(self)"])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Partial Update Teacher Profile(self)"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TeacherAssignedCoursesView(generics.ListAPIView):
    serializer_class = TeacherAssignedCourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    @swagger_auto_schema(tags=["Get Details of Assigned Courses (self)"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.filter(teachers=self.request.user)
    
    
class TeacherAssignedCourseDetailView(generics.RetrieveAPIView):
    serializer_class = TeacherAssignedCourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]
    lookup_url_kwarg = 'course_id'
    
    def get_queryset(self):
        return Course.objects.filter(teachers=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific course assigned to the authenticated teacher.",
        tags=["Retrieve details of a specific course assigned to the authenticated teacher."],
        responses={200: TeacherAssignedCourseSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)         

class TeacherCoursesWithStudentsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]
    
    def get_serializer_class(self):
        student_id = self.request.query_params.get('student_id')
        if student_id:
            return StudentDetailSerializer
        return TeacherCourseWithStudentsSerializer

    @swagger_auto_schema(
        manual_parameters=[              
            openapi.Parameter(
                'student_id',
                openapi.IN_QUERY,
                description="ID of the student to get detailed profile (optional)",
                type=openapi.TYPE_INTEGER
            )
        ],
        tags=["Get Courses with Enrolled Students or Specific Student Profile (self)"]
    )
    def get(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')

        if student_id:  
            try:
                student = User.objects.get(id=student_id, role='student')
            except User.DoesNotExist:
                return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    
            courses = Course.objects.filter(teachers=request.user, students=student)
            if not courses.exists():
                return Response({"detail": "Not authorized to view this student."}, status=status.HTTP_403_FORBIDDEN)

            serializer = StudentDetailSerializer(student, context={'request': request})
            return Response(serializer.data)

        else:  
            courses = Course.objects.filter(teachers=request.user)
            serializer = TeacherCourseWithStudentsSerializer(courses, many=True, context={'request': request})
            return Response(serializer.data)

    
class TeacherEnrollStudentView(generics.CreateAPIView):
    serializer_class = TeacherEnrollStudentSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    @swagger_auto_schema(tags=["Add Student to Course (self)"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        enrollment = serializer.save()
    
        send_enrollment_email.delay(enrollment.student.id, enrollment.course.id)



# class TeacherRemoveStudentView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated, IsTeacherAndOwner]

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the student to remove'),
#                 'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the course')
#             },
#             required=['student_id', 'course_id']
#         ),
#         tags=["Delete Student from Course (self)"]
#     )
#     def delete(self, request, *args, **kwargs):
#         student_id = request.data.get('student_id')
#         course_id = request.data.get('course_id')

#         try:
#             enrollment = Enrollment.objects.get(student_id=student_id, course_id=course_id)
#         except Enrollment.DoesNotExist:
#             return Response({"detail": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Ensure teacher is assigned to this course
#         if not enrollment.course.teachers.filter(id=request.user.id).exists():
#             return Response({"detail": "Not authorized to remove this student."}, status=status.HTTP_403_FORBIDDEN)

#         enrollment.delete()
#         return Response({"message": "Student removed from course successfully."}, status=status.HTTP_200_OK)
    
          

class TeacherRemoveStudentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsTeacherAndOwner]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the student to remove'),
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the course')
            },
            required=['student_id', 'course_id']
        ),
        tags=["Delete Student from Course (self)"]
    )
    def delete(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')

        try:
            enrollment = Enrollment.objects.get(student_id=student_id, course_id=course_id)
        except Enrollment.DoesNotExist:
            return Response({"detail": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure teacher is assigned to this course
        if not enrollment.course.teachers.filter(id=request.user.id).exists():
            return Response({"detail": "Not authorized to remove this student."}, status=status.HTTP_403_FORBIDDEN)

        # Delete enrollment
        enrollment.delete()

        # Trigger Celery email for unenrollment
        send_unenrollment_email.delay(student_id, course_id)

        return Response(
            {"message": "Student removed from course successfully. Emails are queued to be sent."},
            status=status.HTTP_200_OK
        )                          