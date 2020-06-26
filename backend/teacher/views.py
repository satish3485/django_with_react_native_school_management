from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from school.models import School, Classes, Course, Teacher, Student

from school.forms import TeacherRegisterationForm, UserRegisterForm
# Create your views here.


def home_view(request):
    return render(request, 'index.html')


def is_school(user):
    try:
        return user.school.role == "SCHOOL"

    except models.School.DoesNotExist:
        pass
    return False


def is_teacher(user):
    try:
        return user.teacher.role == "TEACHER"
    except models.Teacher.DoesNotExist:
        pass
    return False


def is_student(user):
    try:
        return user.student.role == "STUDENT"

    except models.Student.DoesNotExist:
        pass
    return False


def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('teacher_dashboard')
        else:
            form = AuthenticationForm()
            form._errors = True
            return render(request, 'teacher/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'teacher/login.html', {'form': form})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_dashboard(request):

    classes = Classes.objects.all().filter(
        school=request.user.teacher.school)

    return render(request, 'teacher/teacher_classes_list.html', {'data': classes, 'school': request.user.teacher.school})

# ======================= classes ==================================


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_view_class(request, pk):
    classes = get_object_or_404(Classes, pk=pk,
                                school=request.user.teacher.school)
    data = Course.objects.all().filter(
        clas=pk, school=request.user.teacher.school.id)

    return render(request, 'teacher/teacher_course_list.html', {'data': data, 'class': classes, 'school': request.user.teacher.school})

# ===================== Assignments ============================


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_view_assignments(request, pk):
    course = get_object_or_404(Course, pk=pk,
                               school=request.user.teacher.school)
    data = models.Assignments.objects.all().filter(
        course=pk)

    return render(request, 'teacher/teacher_assignment_list.html', {'data': data, 'course': course, 'school': request.user.teacher.school})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_create_assignments(request, pk):
    course = get_object_or_404(Course, pk=pk,
                               school=request.user.teacher.school)
    form = forms.AssignmentsForm()
    if request.method == 'POST':
        form = forms.AssignmentsForm(request.POST, request.FILES)
        if form.is_valid():

            f2 = form.save(commit=False)
            f2.course = course
            f2.save()
            messages.success(request, "Assignment added successfully")
            return redirect('teacher_view_assignments', course.id)

    return render(request, 'teacher/teacher_create_assignment.html', {'form': form, 'course': course, 'school': request.user.teacher.school})


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_update_assignment(request, pk, pk2):
    assignment = get_object_or_404(models.Assignments, pk=pk2)
    course = get_object_or_404(Course, pk=pk,
                               school=request.user.teacher.school)
    if assignment != None:
        form = forms.AssignmentsForm(
            request.POST or None, request.FILES or None, instance=assignment)
        if request.method == 'POST':
            if form.is_valid():
                f2 = form.save(commit=False)
                f2.course = course
                f2.save()
                messages.success(request, "Assignment updated successfully")
                return redirect('teacher_view_assignments', course.id)
        return render(request, 'teacher/teacher_update_assignment.html', {'form': form, 'course': course, 'school': request.user.teacher.school})
    return redirect('teacher_view_assignments', course.id)


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_delete_assignment(request, pk, pk2):
    assignment = get_object_or_404(models.Assignments, pk=pk2)
    if assignment != None:
        assignment.delete()
        messages.success(request, "Assignment is deleted")
    return redirect('teacher_view_assignments', pk)


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_teacher_update(request, pk):

    if request.user.id == pk:
        form1 = UserRegisterForm(request.POST or None, initial={'username': request.user.username,
                                                                'password1': request.user.password,
                                                                'password2': request.user.password})
        form = TeacherRegisterationForm(
            request.POST or None, request.FILES or None, instance=request.user.teacher)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated")

        return render(request, 'teacher/teacher_update.html', {'form': form, 'form1': form1, 'school': request.user.teacher.school})
    return redirect('teacher_logout')


@login_required(login_url='teacher_login')
@user_passes_test(is_teacher, login_url='teacher_logout')
def teacher_change_password(request, pk):
    if request.method == 'POST' and pk == request.user.id:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('teacher_teacher_update', pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form, 'school': request.user
    })
