"""
by satish kumar

"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('teacherclick', views.teacher_login, name='teacherclick'),
    path('teacher/', views.teacher_login, name='teacher_login'),
    path('logout', LogoutView.as_view(
        next_page='teacher/'), name='teacher_logout'),

    path('teacher/change_password/<int:pk>', views.teacher_change_password,
         name='teacher_change_password'),
    path('teacher/profile/<int:pk>', views.teacher_teacher_update,
         name='teacher_teacher_update'),

    path('teacher_dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('class/<int:pk>', views.teacher_view_class, name='teacher_view_class'),
    path('assignment/<int:pk>', views.teacher_view_assignments,
         name='teacher_view_assignments'),
    path('assignment_create/<int:pk>', views.teacher_create_assignments,
         name='teacher_create_assignments'),
    path('assignment_update/<int:pk>/<int:pk2>', views.teacher_update_assignment,
         name='teacher_update_assignment'),
    path('assignment_delete/<int:pk>/<int:pk2>', views.teacher_delete_assignment,
         name='teacher_delete_assignment'),



    path('studentclick', views.teacher_login, name='studentclick'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
