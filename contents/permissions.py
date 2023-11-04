from rest_framework import permissions
from students_courses.models import StudentCourse


class IsCourseStudentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            try:
                StudentCourse.objects.get(
                    course_id=obj.course_id, student_id=request.user.id
                )
                return True
            except:
                return False