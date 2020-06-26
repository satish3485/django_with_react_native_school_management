"""
by satish kumar

"""
from django.contrib import admin
from django.urls import path, include
from school import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),
    path('api/', include('student.api.urls'))
]
