from rest_framework import serializers
from .models import Course
from accounts.models import Account
from students_courses.models import StudentCourse
from contents.serializers import ContentSerializer
from students_courses.serializers import StudentCourseSerializer


COURSE_STATUS = ("not started", "in progress", "finished")


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    students_courses = StudentCourseSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(choices=COURSE_STATUS, required=False)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "students_courses",
            "contents",
        ]


class CourseStudentsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    students_courses = StudentCourseSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"]

    def update(self, instance: Course, validated_data: dict) -> Course:
        email_list = []
        for student in validated_data["students_courses"]:
            email = student["student"]["email"]
            try:
                student = Account.objects.get(email=email)
                try:
                    StudentCourse.objects.get(course=instance, student=student)
                except:
                    instance.students.add(student)
                    instance.save()
            except Account.DoesNotExist:
                email_list.append(email)
            if len(email_list) > 0:
                email_string = ",".join(email_list)
                error = f"No active accounts was found: {email_string}."
                raise serializers.ValidationError({"detail": error})
        return instance