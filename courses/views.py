from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import SuperUserOrGetPermission, SuperUserPermission
from .models import Course
from .serializers import CourseSerializer, CourseStudentsSerializer
from django.shortcuts import get_object_or_404
from accounts.models import Account
from students_courses.models import StudentCourse
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

class CourseView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, SuperUserOrGetPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Course.objects.filter(students=self.request.user)
        return self.queryset.all()



class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [SuperUserOrGetPermission]
    serializer_class = CourseSerializer
    lookup_url_kwarg = "course_id"
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self) -> Course:
        if self.request.user.is_superuser:
            return Course.objects.all()

        return Course.objects.filter(students=self.request.user)


class StudentView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [SuperUserPermission]
    queryset = Course.objects.all()
    serializer_class = CourseStudentsSerializer
    lookup_url_kwarg = "course_id"
    http_method_names = ["get", "put"]


class DestroyStudentView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [SuperUserPermission]
    queryset = Course.objects.all()
    serializer_class = CourseStudentsSerializer
    lookup_url_kwarg = "course_id"

    def perform_destroy(self, serializer) -> None:
        try:
            student = get_object_or_404(Account, id=self.kwargs["student_id"])
            student_course = StudentCourse.objects.get(
                student=student,
                course_id=self.kwargs["course_id"],
            )
            student_course.delete()
        except StudentCourse.DoesNotExist:
            error = "this id is not associated with this course."
            raise NotFound(error)