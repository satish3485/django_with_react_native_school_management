from django.db import models
from school.models import School, Classes, Course, Teacher, Student
import datetime
import os
from django.conf import settings
# Create your models here.


def content_file_name_assignment(instance, filename):
    ext = filename.split('.')[-1]
    currentTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = "%s_%s.%s" % (filename.split('.')[0], currentTime, ext)
    name = os.path.join('assignments', filename)
    return name


class Assignments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30, null=False, default=None)
    description = models.CharField(max_length=2000, blank=True)
    startDate = models.DateField(default=datetime.datetime.now, blank=True)
    endDate = models.DateField(blank=True, null=True)
    image = models.FileField(
        upload_to=content_file_name_assignment, blank=True, null=True)
    maxPoints = models.PositiveIntegerField(default=100, null=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
