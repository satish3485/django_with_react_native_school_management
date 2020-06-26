from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

classes = [('Pre-Nursery', 'Pre-Nursery'), ('Nursery', 'Nursery'), ('KG', 'KG'), ('LKG', 'LKG'), ('UKG', 'UKG'), ('one', 'one'), ('two', 'two'), ('three', 'three'),
           ('four', 'four'), ('five', 'five'), ('six', 'six'), ('seven', 'seven'), ('eight', 'eight'), ('nine', 'nine'), ('ten', 'ten'), ('eleven', 'eleven'), ('twelve', 'twelve')]


gender_choice = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

def content_file_name_teacher(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.user.username, ext)
    name = os.path.join('teacher', filename)
    fullname = os.path.join(settings.MEDIA_ROOT, name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return name


def content_file_name_student(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.user.username, ext)
    name = os.path.join('student', filename)
    fullname = os.path.join(settings.MEDIA_ROOT, name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return name


def content_file_name_school(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.user.username, ext)
    name = os.path.join('school', filename)
    fullname = os.path.join(settings.MEDIA_ROOT, name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return name


class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    principle = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100)
    # zip = models.PositiveIntegerField()
    city = models.CharField(max_length=20)
    board = models.CharField(max_length=100, default="")
    # rating = models.PositiveIntegerField(default=0)
    # classesAvailable = models.CharField(
    #     max_length=20, choices=classes, default='Pre-Nursery')
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(null=True, default="")
    website = models.URLField(
        max_length=200, null=True, default="www.hello.com")
    about = models.TextField(null=True, default="Description")
    image = models.ImageField(
        upload_to=content_file_name_school, null=True, default="school/school.png")
    createdDate = models.DateField(auto_now_add=True)
    # group = models.ForeignKey(
    #     Group, on_delete=models.CASCADE, default="SCHOOL")
    role = models.CharField(max_length=100, default="SCHOOL")

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Classes(models.Model):
    name = models.CharField(max_length=30, null=False)
    section = models.CharField(max_length=10, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # courses = models.ManyToManyField(Course, blank=True)
    # students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.name



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    phone = PhoneNumberField()
    email = models.EmailField(blank=True)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to=content_file_name_teacher,
                              null=True, default="teacher/teacher.png")
    degree = models.CharField(max_length=50, blank=True)
    dateofbirth = models.DateField(max_length=10)
    gender = models.CharField(choices=gender_choice, max_length=10)
    address = models.CharField(max_length=100, blank=True)
    # group = models.ForeignKey(
    #     Group, on_delete=models.CASCADE, default="TEACHER")
    role = models.CharField(max_length=100, default="TEACHER")
    notificationToken = models.CharField(max_length=100, default=None, null=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    clas = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30, null=False)
    phone = PhoneNumberField()
    email = models.EmailField(blank=True)
    about = models.TextField(blank=True, null=True, default=None)
    image = models.ImageField(
        upload_to=content_file_name_student, null=True, default="student/student.png")

    yearofenroll = models.DateField(auto_now_add=True)
    dateofbirth = models.DateField(blank=True, null=True)
    fatherName = models.CharField(max_length=30, null=True)
    motherName = models.CharField(max_length=30, null=True)
    gender = models.CharField(choices=gender_choice, max_length=10)
    # group = models.ForeignKey(
    #     Group, on_delete=models.CASCADE, default="STUDENT")
    address = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, default="STUDENT")
    notificationToken = models.CharField(max_length=100, default=None, null=True)
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.name



class Course(models.Model):
    name = models.CharField(max_length=30, null=False, default=None)

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    clas = models.ForeignKey(
        Classes, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

