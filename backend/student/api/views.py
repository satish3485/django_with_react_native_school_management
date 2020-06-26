
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User
from rest_framework import serializers
from school.models import School, Classes, Course, Teacher, Student
from django.shortcuts import get_object_or_404
from .serializers import (LoginSerializer, UserSerializer,CourseSerializer,
                            AssigenmentSerializer,SudentSerializer,ClasSerializer,
                            ChangePasswordSerializer, NotificationSerializer)

from teacher.models import Assignments

from rest_framework.generics import ListAPIView, RetrieveAPIView,UpdateAPIView
#  create course Viewset

from notifications.models import Notification



class NotificationViewSet(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = NotificationSerializer

    def list(self, request):
        queryset = request.user.notifications.unread()
        return Response(NotificationSerializer(queryset, many=True).data)
 
class NotificationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class =  NotificationSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return self.request.user.notifications.unread()



class CourseListView(ListAPIView):
    permission_class = [
        permissions.IsAuthenticated
    ]
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.all().filter(clas=self.request.user.student.clas)



class AssignmentListView(ListAPIView):
    permission_class = [
        permissions.IsAuthenticated
    ]
    serializer_class = AssigenmentSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return Assignments.objects.all().filter(course=id)

class AllAssignmentView(ListAPIView):
    # queryset = Assignments.objects.all()
    permission_class = [
        permissions.IsAuthenticated
    ]
    serializer_class = AssigenmentSerializer
    def get_queryset(self):
        id = self.request.user.student.clas
        return Assignments.objects.all().filter(course__clas=id).order_by('-startDate')


#  create assignments
class AssignmentViewSet(generics.GenericAPIView):
    permission_class = [
        permissions.AllowAny
    ]
    serializer_class = AssigenmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment = serializer.save()
        return Response({
        "assignment": AssigenmentSerializer(assignment, context=self.get_serializer_context()).data
        })
        
        
    # def get_queryset(self):
    #     id = self.request.GET.get('pk')
    #     return Assignments.objects.all().filter(course=id)

# class CourseDetailView(RetrieveAPIView):
#     queryset = Course.objects.all()
#     permission_class = [
#         permissions.AllowAny
#     ]
#     serializer_class = CourseSerializer



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "token": token,
            "id":user.student.id
        })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# class StudentViewApi(viewsets.ModelViewSet):
#     queryset = Student.objects.all().filter()
#     serializer_class = SudentSerializer
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

class StudentViewApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SudentSerializer
    def get_object(self, pk=None):
        clas = self.request.user.student.clas
        return self.request.user.student


         


class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SudentSerializer
    def get_queryset(self):
        return Student.objects.all().filter(user= self.request.user)


class ClassViewApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ClasSerializer
    def get_object(self, pk=None):
        return self.request.user.student.clas


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = [
            permissions.IsAuthenticated
        ]

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=400)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=400)