from django.urls import path
from courses import views
from contents.views import ContentView, ContentDetailView


urlpatterns = [
    path("courses/", views.CourseView.as_view()),
    path("courses/<uuid:course_id>/", views.CourseDetailView.as_view()),
    path("courses/<uuid:course_id>/students/", views.StudentView.as_view()),
    path(
        "courses/<uuid:course_id>/students/<uuid:student_id>/",
        views.DestroyStudentView.as_view(),
    ),
    path("courses/<uuid:course_id>/contents/", ContentView.as_view()),
    path(
        "courses/<uuid:course_id>/contents/<uuid:content_id>/",
        ContentDetailView.as_view(),
    ),
]
