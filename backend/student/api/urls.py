from django.urls import path,include
from knox import views as knox_views
from .views import (LoginAPI, UserAPI, 
CourseListView, AssignmentListView, AssignmentViewSet, 
StudentViewApi, ProfileUpdateView, ClassViewApi, ChangePasswordView, AllAssignmentView, NotificationViewSet,
NotificationUpdateView)

import notifications.urls

urlpatterns = [

    path('auth', include('knox.urls')),
    path('login/', LoginAPI.as_view()),
    path('userInfo', UserAPI.as_view()),

    path('course/', CourseListView.as_view()),
    path('assignments/<pk>', AssignmentListView.as_view()),
    path('assignment/create', AssignmentViewSet.as_view()),
    path('student/profile', StudentViewApi.as_view()),
    path('student/class', ClassViewApi.as_view()),
    path('student/update/profile/<pk>', ProfileUpdateView.as_view()),
    path('student/changepassword/<pk>', ChangePasswordView.as_view()),
    path('student/allassugnments', AllAssignmentView.as_view()),

    path("inbox/notifications/", NotificationViewSet.as_view(), name='notifications'),
    path("inbox/notifications/update/<pk>", NotificationUpdateView.as_view(), name='notificationsUpdate'),
] 