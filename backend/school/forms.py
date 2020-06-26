from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from . import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

# for admin


class SchoolRegisterationForm(forms.ModelForm):
    """docstring for TeacherRegisterationForm."""

    class Meta:
        model = models.School
        fields = ['principle', 'name', 'city', 'board', 'phone', 'email', 'website',
                  'image',  'address', 'about']


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TeacherRegisterationForm(forms.ModelForm):
    """docstring for TeacherRegisterationForm."""

    class Meta:
        model = models.Teacher
        fields = ['name', 'phone', 'email',
                  'image', 'degree', 'dateofbirth', 'gender', 'address', 'about']


class StudentRegisterationForm(forms.ModelForm):
    """docstring for StudentRegisterationForm."""

    class Meta:
        model = models.Student
        fields = ['name', 'phone', 'email',
                  'image', 'dateofbirth', 'fatherName', 'motherName', 'gender', 'address', 'about', 'clas']


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = models.Classes
        fields = ['name', 'section']


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['name', 'clas']
