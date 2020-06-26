from django.contrib import admin
from .models import School, Classes, Course, Teacher, Student
from .forms import CreateCourseForm

admin.site.register(School)
admin.site.register(Classes)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
