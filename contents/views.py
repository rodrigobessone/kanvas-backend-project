from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ContentSerializer
from .models import Content
from django.shortcuts import get_object_or_404
from .permissions import IsCourseStudentPermission
from courses.permissions import SuperUserPermission
from courses.models import Course
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied



class ContentView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [SuperUserPermission]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def perform_create(self, serializer) -> Content:
        get_object_or_404(Course, id=self.kwargs["course_id"])
        return serializer.save(course_id=self.kwargs["course_id"])


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCourseStudentPermission]
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    lookup_url_kwarg = "course_id"
    http_method_names = ["get", "patch", "delete"]

    # def perform_update(self, serializer) -> Content:
    #     return serializer.save(id=self.kwargs["content_id"])
    
    def get_object(self) -> Content: # (2)
        content = Content.objects.filter(pk=self.kwargs["content_id"]).first() # (3)
        course = Course.objects.filter(pk=self.kwargs["course_id"]).exists() # (4)
        print(course)
        if not course:
            print('course')
            raise NotFound({"detail": "course not found."}) # (6)
        if not content:
             print('content')
             raise NotFound({"detail": "content not found."}) # (5)
        self.check_object_permissions(self.request, content)
        return content # (7)