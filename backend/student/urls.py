"""
by satish kumar

"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from student import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path,include
from student import views


# router.register('api/courses', CourseViewSet, 'courses')

# urlpatterns = router.urls


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('studentclick', views.student_login, name='studentclick'),
    path('student/', views.student_login, name='student_login'),
    path('logout', LogoutView.as_view(
        next_page='student/'), name='student_logout'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_assignment/<int:pk>', views.student_view_assignments,
         name='student_view_assignments'),
    path('student_assignment/<int:pk>/<int:pk2>', views.student_view_assignments_detail,
         name='student_view_assignments_detail'),
    path('student/profile/<int:pk>', views.student_student_update,
         name='student_student_update'),

    path('student/change_password/<int:pk>', views.student_change_password,
         name='student_change_password'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
