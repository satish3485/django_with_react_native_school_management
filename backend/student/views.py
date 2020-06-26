from django.shortcuts import render, redirect, reverse
from . import models
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
# Create your views here.
from school.models import School, Classes, Course, Teacher, Student

from school.forms import StudentRegisterationForm, UserRegisterForm
from teacher.models import Assignments


def is_student(user):
    try:
        return user.student.role == "STUDENT"

    except:
        pass
    return False


def student_login(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('student_dashboard')
        else:
            form = AuthenticationForm()
            form._errors = True
            return render(request, 'student/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'student/login.html', {'form': form})


@login_required(login_url='student_login')
@user_passes_test(is_student, login_url='student_logout')
def student_dashboard(request):

    course = Course.objects.all().filter(
        clas=request.user.student.clas)

    return render(request, 'student/student_course_list.html', {'data': course, 'school': request.user.student.school})


@login_required(login_url='student_login')
@user_passes_test(is_student, login_url='student_logout')
def student_view_assignments(request, pk):

    course = get_object_or_404(Course, pk=pk,
                               school=request.user.student.school)
    assignments = Assignments.objects.all().filter(
        course=pk)

    return render(request, 'student/student_assignment_list.html', {'data': assignments, 'course': course, 'school': request.user.student.school})


@login_required(login_url='student_login')
@user_passes_test(is_student, login_url='student_logout')
def student_view_assignments_detail(request, pk, pk2):

    course = get_object_or_404(Course, pk=pk,
                               school=request.user.student.school)
    assignments = get_object_or_404(Assignments,
                                    pk=pk2)

    return render(request, 'student/student_assignment_detail.html', {'data': assignments, 'course': course, 'school': request.user.student.school})


@login_required(login_url='student_login')
@user_passes_test(is_student, login_url='student_logout')
def student_student_update(request, pk):

    if request.user.id == pk:
        form1 = UserRegisterForm(request.POST or None, initial={'username': request.user.username,
                                                                'password1': request.user.password,
                                                                'password2': request.user.password})
        form = StudentRegisterationForm(
            request.POST or None, request.FILES or None, instance=request.user.student)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated")

        return render(request, 'student/student_update.html', {'form': form, 'form1': form1, 'school': request.user.student.school})
    return redirect('student_logout')


@login_required(login_url='teacher_login')
@user_passes_test(is_student, login_url='teacher_logout')
def student_change_password(request, pk):
    if request.method == 'POST' and pk == request.user.id:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('student_student_update', pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form, 'school': request.user
    })
