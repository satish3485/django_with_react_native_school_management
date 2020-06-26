"""
by satish kumar

"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from school import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home_view, name=''),
    path('', views.home_view, name='goBack'),

    path('schoollogin', views.school_login, name="schoollogin"),
    path('logout/', LogoutView.as_view(
        template_name='index.html'), name='logout'),
    path('schoolclick', views.school_login, name='schoolclick'),
    path('school_dashboard', views.school_dashboard, name='school_dashboard'),
    path('school/profile/<int:pk>', views.school_school_update,
         name='school_school_update'),
    path('school/change_password/<int:pk>', views.school_change_password,
         name='school_change_password'),
    path('teacher_registeration', views.teacher_registeration,
         name='teacher_registeration'),
    path('school/update_teacher/<int:pk>', views.school_teacher_update,
         name='school_teacher_update'),
    path('school_teacher_list', views.school_teacher_list,
         name='school_teacher_list'),
    path('school/delete_teacher/<int:pk>', views.school_teacher_delete,
         name='school_teacher_delete'),
    path('school/search_teacher', views.school_search_teacher,
         name='school_search_teacher'),
    path('school/teacher_pdf', views.school_teacher_pdf,
         name='school_teacher_pdf'),
    path('school/student_pdf', views.school_student_pdf,
         name='school_student_pdf'),



    path('school_student_list', views.school_student_list,
         name='school_student_list'),
    path('student_registeration', views.student_registeration,
         name='student_registeration'),
    path('school/delete_student/<int:pk>', views.school_student_delete,
         name='school_student_delete'),
    path('school/update_student/<int:pk>', views.school_student_update,
         name='school_student_update'),
    path('school/search_student', views.school_search_student,
         name='school_search_student'),

    path('school/create_class', views.school_create_class,
         name='school_create_class'),
    path('school/classes_list', views.school_class_list,
         name='school_class_list'),
    path('school/delete_class/<int:pk>', views.school_delete_class,
         name='school_delete_class'),
    path('school/update_class/<int:pk>', views.school_update_class,
         name='school_update_class'),
    path('school/delete_course/<int:pk>/<int:pk2>', views.school_delete_course_in_class,
         name='school_delete_course_in_class'),




    path('school/course_list', views.school_course_list,
         name='school_course_list'),
    path('school/create_course', views.school_create_course,
         name='school_create_course'),
    path('school/delete_course/<int:pk>', views.school_delete_course,
         name='school_delete_course'),
    path('school/update_course/<int:pk>', views.school_update_course,
         name='school_update_course'),
     path('school/assignment_delete/<int:pk>/<int:pk2>', views.school_delete_assignment,
          name='school_delete_assignment'),

     path('school/sendnotification', views.sendNotification,
         name='school_send_notification'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
