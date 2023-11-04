from rest_framework import permissions
from .models import Course

# class SuperUserOrGetPermission(permissions.BasePermission):
#     def has_permission(self, request, view) -> bool:
#         return request.user.is_authenticated and (
#             request.user.is_superuser or request.method == "GET"
#         )

#     def has_object_permissions(self, request, view, object) -> bool:
#         return request.user.is_superuser or request.user in object.students.all()


class SuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.is_superuser

class SuperUserOrGetPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True
        return request.method in permissions.SAFE_METHODS
    def has_object_permissions(self, request, view, object: Course) -> bool:
         return request.user.is_superuser or request.user in object.students.all()

