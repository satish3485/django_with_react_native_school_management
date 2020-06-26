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
from django.contrib.auth.models import User
from knox.models import AuthToken
from teacher.models import Assignments

from notifications.signals import notify
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError



# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, title, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    except:
        print("we have errors")
        pass

    # try:
    #     # We got a response back, but we don't know whether it's an error yet.
    #     # This call raises errors so we can handle them with normal exception
    #     # flows.
    #     response.validate_response()
    # except DeviceNotRegisteredError:
    #     # Mark the push token as inactive
    #     from notifications.models import PushToken
    #     PushToken.objects.filter(token=token).update(active=False)
    # except PushResponseError as exc:
    #     # Encountered some other per-notification error.
    #     rollbar.report_exc_info(
    #         extra_data={
    #             'token': token,
    #             'message': message,
    #             'extra': extra,
    #             'push_response': exc.push_response._asdict(),
    #         })
    #     raise self.retry(exc=exc)

def home_view(request):
    return render(request, 'index.html')


# for login and home page for school
# @login_required(login_url='index')


def school_login(request):
    if request.user.is_authenticated:
        return redirect('school_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('school_dashboard')

        else:
            form = AuthenticationForm()
            form._errors = True
            return render(request, 'school/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'school/login.html', {'form': form})


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

@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def sendNotification(request):
    # user = request.user

    # reciver = User.objects.all().filter(student__school = request.user.school)
    # allStudents = models.Student.objects.all().filter(school = request.user.school)
    # # for s in allStudents:
    # #     print(s.notificationToken)
    # #     if s.notificationToken:
    # #         send_push_message(s.notificationToken, "Tommorw is school", extra=None)

    # notify.send(user, recipient=reciver, verb='Today is no class')
    classes = models.Classes.objects.all().filter(school = request.user.school)
    students = models.Student.objects.all().filter(school = request.user.school)
    if request.method == 'POST':
        title = request.POST.get("notificationTitle")
        description = request.POST.get("notificationTextarea")
        x = request.POST.get("selectusertosends")
        if x == "all":
            user = User.objects.all().filter(student__school = request.user.school) | User.objects.all().filter(teacher__school = request.user.school)
            for s in models.Student.objects.all().filter(school = request.user.school):
                if s.notificationToken:
                    send_push_message(s.notificationToken, title, description, extra=None)
            for s in models.Teacher.objects.all().filter(school = request.user.school):
                if s.notificationToken:
                    send_push_message(s.notificationToken, title, description, extra=None)
        elif x == "allStudent":
            user =  User.objects.all().filter(student__school = request.user.school)
            for s in models.Student.objects.all().filter(school = request.user.school):
                if s.notificationToken:
                    send_push_message(s.notificationToken, title, description, extra=None)

        elif x == "specificClass":
            clas = request.POST.get("class")
            user =  User.objects.all().filter(student__clas = clas)
            for s in models.Student.objects.all().filter(clas = clas):
                if s.notificationToken:
                    send_push_message(s.notificationToken, title, description, extra=None)
        else:
            studentId = request.POST.get("student")
            user =  User.objects.all().filter(student = studentId)
            for s in models.Student.objects.all().filter(id = studentId):
                if s.notificationToken:
                    send_push_message(s.notificationToken, title, description, extra=None)
        notify.send(request.user, recipient=user, verb=title, description=description)
        
        messages.success(request, "Notification Sent")
        # return redirect('school_dashboard')
    return render(request, 'school/notification.html', {'school': request.user, 'classes':classes, 'students':students})

@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_change_password(request, pk):
    if request.method == 'POST' and pk == request.user.id:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('school_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form, 'school': request.user
    })


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_dashboard(request):
    total_teacher = models.Teacher.objects.all().filter(
        school=request.user.school.id).count()
    total_student = models.Student.objects.all().filter(
        school=request.user.school.id).count()
    total_course = models.Course.objects.all().filter(
        school=request.user.school.id).count()

    total_class = models.Classes.objects.all().filter(
        school=request.user.school.id).count()

    # aggregate function return dictionary so fetch data from dictionay
    mydict = {
        'total_teacher': total_teacher,
        'total_student': total_student,
        'total_course': total_course,
        'total_class': total_class,
        'school': request.user
    }

    return render(request, 'school/school_dashboard.html', context=mydict)


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_school_update(request, pk):
    if request.user.id == pk:
        form1 = forms.UserRegisterForm(request.POST or None, initial={'username': request.user.username,
                                                                      'password1': request.user.password,
                                                                      'password2': request.user.password})
        form = forms.SchoolRegisterationForm(
            request.POST or None, request.FILES or None, instance=request.user.school)
        if request.method == 'POST':
            if form.is_valid():
                form.save()

                messages.success(request, "Updated")
                # if 'image' in request.FILES:
                #     data = models.Teacher.objects.all().filter(
                #         school=request.user.school.id)
                #     return render(request, 'school/teacher-list.html', {'data': data,  'school': request.user, 'pictureUpdate': True})
                # else:
                return redirect('school_dashboard')
            else:
                messages.success(request, form1._errors)
                messages.error(request, "Please check fields are required")
                mydict = {'form': form, 'form1': form1, 'school': request.user}
                return render(request, 'school/school-update.html', context=mydict)
        else:
            mydict = {'form': form, 'form1': form1, 'school': request.user}
            return render(request, 'school/school-update.html', context=mydict)
    else:
        return redirect('logout')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_teacher_pdf(request):
    teachers = models.Teacher.objects.all().filter(
        school=request.user.school.id)
    # paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string(
        'school/teacher_pdf_template.html', {'teachers': teachers, "school": request.user.school.name})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/teachers.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('teachers.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="teachers.pdf"'
        return response

    return response


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_student_pdf(request):
    students = models.Student.objects.all().filter(
        school=request.user.school.id)
    # paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string(
        'school/student_pdf_template.html', {'students': students, "school": request.user.school.name})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/students.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('students.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="students.pdf"'
        return response

    return response

# =======================Teacher view functions ====================
@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def teacher_registeration(request):
    form1 = forms.UserRegisterForm()
    form = forms.TeacherRegisterationForm()
    if request.method == 'POST':
        form = forms.TeacherRegisterationForm(request.POST, request.FILES)
        form1 = forms.UserRegisterForm(request.POST)
        if form1.is_valid() and form.is_valid():
            user = form1.save()

            f2 = form.save(commit=False)
            f2.user = user
            f2.school = request.user.school
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            messages.success(request, f"New Teacher added: {f2.name}")
            return redirect('teacher_registeration')
        else:
            messages.error(request, "Please check your all are required")

    mydict = {'form': form, 'form1': form1, 'school': request.user}
    return render(request, 'school/teacher-registration.html', context=mydict)


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_teacher_list(request):
    data = models.Teacher.objects.all().filter(
        school=request.user.school.id)
    return render(request, 'school/teacher-list.html', {'data': data,  'school': request.user})


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_teacher_update(request, pk):
    teacher = get_object_or_404(
        models.Teacher, pk=pk, school=request.user.school)
    if teacher != None:
        form1 = forms.UserRegisterForm(request.POST or None, initial={'username': teacher.user.username,
                                                                      'password1': teacher.user.password,
                                                                      'password2': teacher.user.password})
        form = forms.TeacherRegisterationForm(
            request.POST or None, request.FILES or None, instance=teacher)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Updated")
                # if 'image' in request.FILES:
                #     data = models.Teacher.objects.all().filter(
                #         school=request.user.school.id)
                #     return render(request, 'school/teacher-list.html', {'data': data,  'school': request.user, 'pictureUpdate': True})
                # else:
                return redirect('school_teacher_list')
            else:
                messages.error(request, "Please check fields are required")
                mydict = {'form': form, 'form1': form1, 'school': request.user}
                return render(request, 'school/teacher-update.html', context=mydict)
        else:
            mydict = {'form': form, 'form1': form1, 'school': request.user}
            return render(request, 'school/teacher-update.html', context=mydict)
    else:
        return redirect('teacher_registeration')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_teacher_delete(request, pk):
    teacher = get_object_or_404(
        models.Teacher, pk=pk, school=request.user.school)
    if teacher != None:
        user = get_object_or_404(
        User, pk=teacher.user.pk)
        user.delete()
        # teacher.delete()
        messages.success(request, f"Teacher is deleted")
        return redirect('school_teacher_list')
    else:
        messages.success(request, f"You are not able to delete it")
        return redirect('school_teacher_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_search_teacher(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(name__icontains=query)
            results = models.Teacher.objects.filter(
                lookups, school=request.user.school).distinct()
            return render(request, 'school/teacher-list.html', {'data': results,  'school': request.user})
        else:
            return redirect('school_teacher_list')
    else:
        return redirect('school_teacher_list')

# ==================Students start here ===================


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_student_list(request):
    data = models.Student.objects.all().filter(
        school=request.user.school.id)
    return render(request, 'school/student-list.html', {'data': data,  'school': request.user})


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def student_registeration(request):
    form1 = forms.UserRegisterForm()
    form = forms.StudentRegisterationForm()
    classes = models.Classes.objects.all().filter(
        school=request.user.school.id)

    if request.method == 'POST':
        form = forms.StudentRegisterationForm(request.POST, request.FILES)
        form1 = forms.UserRegisterForm(request.POST)
        if form1.is_valid() and form.is_valid():
            user = form1.save()

            f2 = form.save(commit=False)
            f2.user = user
            f2.school = request.user.school
            f2.save()
            messages.success(request, f"New Student added: {f2.name}")
            # my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            # my_teacher_group[0].user_set.add(user)
            return redirect('student_registeration')

    mydict = {'form': form, 'form1': form1,
              'classes': classes, 'school': request.user}
    return render(request, 'school/student-registration.html', context=mydict)


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_student_delete(request, pk):
    student = get_object_or_404(
        models.Student, pk=pk, school=request.user.school)
    if student != None:
        user = get_object_or_404(
        User, pk=student.user.pk)
        user.delete()
        # student.delete()
        messages.success(request, f"Student is deleted")
        return redirect('school_student_list')
    else:
        messages.success(request, f"You are not able to delete it")
        return redirect('school_student_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_student_update(request, pk):
    student = get_object_or_404(
        models.Student, pk=pk, school=request.user.school)
    if student != None:
        form1 = forms.UserRegisterForm(request.POST or None, initial={'username': student.user.username,
                                                                      'password1': student.user.password,
                                                                      'password2': student.user.password})
        form = forms.StudentRegisterationForm(
            request.POST or None, request.FILES or None, instance=student)
        classes = models.Classes.objects.all().filter(
            school=request.user.school.id)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Updated")

                return redirect('school_student_list')
            else:
                messages.error(request, "Please check fields are required")
                mydict = {'form': form, 'form1': form1,
                          'classes': classes, 'school': request.user}
                return render(request, 'school/student-update.html', context=mydict)
        else:
            mydict = {'form': form, 'form1': form1,
                      'classes': classes, 'school': request.user}
            return render(request, 'school/student-update.html', context=mydict)
    else:
        return redirect('student_registeration')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_search_student(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(name__icontains=query)
            results = models.Student.objects.filter(
                lookups, school=request.user.school).distinct()
            return render(request, 'school/student-list.html', {'data': results,  'school': request.user})
        else:
            return redirect('school_student_list')
    else:
        return redirect('school_student_list')
# =============================Student END=========================


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_class_list(request):
    data = models.Classes.objects.all().filter(
        school=request.user.school.id)

    form = forms.CreateClassForm()
    return render(request, 'school/classes_list.html', {'data': data, "form": form,  'school': request.user})


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_create_class(request):

    if request.method == 'POST':
        form = forms.CreateClassForm(request.POST)
        if form.is_valid():
            f2 = form.save(commit=False)
            f2.school = request.user.school
            f2.save()
            messages.success(request, "Class added successfully")

    return redirect('school_class_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_delete_class(request, pk):
    classes = get_object_or_404(
        models.Classes, pk=pk, school=request.user.school)
    if classes != None:
        classes.delete()
        messages.success(request, f"Class is deleted")
        return redirect('school_class_list')
    else:
        messages.success(request, f"You are not able to delete it")
        return redirect('school_class_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_update_class(request, pk):

    classes = get_object_or_404(
        models.Classes, pk=pk, school=request.user.school)

    courses = models.Course.objects.all().filter(clas=classes)

    if classes != None:
        form = forms.CreateClassForm(
            request.POST or None, instance=classes)
        if request.method == 'POST':
            if form.is_valid():

                f2 = form.save(commit=False)
                f2.school = request.user.school
                f2.save()
                messages.success(request, "Class update successfully")
                return redirect('school_class_list')

        return render(request, 'school/classes_update.html', {"form": form, "courses": courses,  'school': request.user})
    return redirect('school_class_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_delete_course_in_class(request, pk, pk2):

    classes = get_object_or_404(
        models.Classes, pk=pk, school=request.user.school)

    courses = models.Course.objects.all().filter(clas=classes, pk=pk2)
    if courses != None:
        form = forms.CreateClassForm(
            request.POST or None, instance=classes)
        courses.delete()
        messages.success(request, f"Course is deleted")
    return redirect('school_update_class', pk=pk)


# ==================== Courses ==========================
@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_course_list(request):
    data = models.Course.objects.all().filter(
        school=request.user.school.id)

    classes = models.Classes.objects.all().filter(
        school=request.user.school.id)

    form = forms.CreateCourseForm()
    return render(request, 'school/course_list.html', {'data': data, "classes": classes, "form": form,  'school': request.user})


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_create_course(request):
    if request.method == 'POST':
        form = forms.CreateCourseForm(request.POST)
        if form.is_valid():

            f2 = form.save(commit=False)
            f2.school = request.user.school
            f2.save()
            messages.success(request, "Course added successfully")

    return redirect('school_course_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_delete_course(request, pk):
    course = get_object_or_404(
        models.Course, pk=pk, school=request.user.school)
    if course != None:
        course.delete()
        messages.success(request, f"Course is deleted")
        return redirect('school_course_list')
    else:
        messages.success(request, f"You are not able to delete it")
        return redirect('school_course_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_update_course(request, pk):

    course = get_object_or_404(
        models.Course, pk=pk)

    classes = models.Classes.objects.all().filter(
        school=request.user.school.id)

    data = Assignments.objects.all().filter(course = course)
    if course != None:
        form = forms.CreateCourseForm(
            request.POST or None, instance=course)
        if request.method == 'POST':
            if form.is_valid():

                f2 = form.save(commit=False)
                f2.save()
                messages.success(request, "Course update successfully")
                return redirect('school_course_list')

        return render(request, 'school/course_update.html', {"form": form, "classes": classes, "data":data,  'school': request.user})

    return redirect('school_course_list')


@login_required(login_url='schoollogin')
@user_passes_test(is_school, login_url='logout')
def school_delete_assignment(request, pk, pk2):
    assignment = get_object_or_404(Assignments, pk=pk2)
    if assignment != None:
        assignment.delete()
        messages.success(request, "Assignment is deleted")
    return redirect('school_update_course', pk)
