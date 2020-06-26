from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from . import models


class AssignmentsForm(forms.ModelForm):
    """docstring for TeacherRegisterationForm."""

    class Meta:
        model = models.Assignments
        fields = ['name', 'description', 'startDate',
                  'endDate', 'image', 'maxPoints']
