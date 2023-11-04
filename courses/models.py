from django.db import models
import uuid
from accounts.models import Account


class CourseStatus(models.TextChoices):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"


class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=11, choices=CourseStatus.choices, default=CourseStatus.NOT_STARTED
    )
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name="courses",
        null=True,
    )
    students = models.ManyToManyField(
        Account,
        through="students_courses.StudentCourse",
        related_name="my_courses",
    )

    def is_superuser(self, user):
        return user.is_superuser or self.students.filter(id=user.id).exists()




