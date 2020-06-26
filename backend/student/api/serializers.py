from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from school.models import School, Classes, Course, Teacher, Student
from teacher.models import Assignments
from notifications.models import Notification

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'



class AssigenmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        fields = '__all__'


# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        
        if isinstance(data, six.string_types):
            
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class SudentSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Student
        fields = '__all__'
        # fields = ('id','name','image', 'phone', 'email', 'about','dateofbirth','fatherName','motherName','gender','address')


class ClasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'
        # fields = ('id','name','image', 'phone', 'email', 'about','dateofbirth','fatherName','motherName','gender','address')

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, Student):
            serializer = StudentSerializer(value)
        if isinstance(value, Teacher):
            serializer = TeacherSerializer(value)

        return serializer.data

class NotificationSerializer(serializers.ModelSerializer):
    
    # recipient = UserSerializer(read_only=True)
    # unread = serializers.BooleanField(read_only=True)
    # deleted = serializers.BooleanField(read_only=True)
    # target = GenericNotificationRelatedField(read_only=True)
    # id = serializers.PrimaryKeyRelatedField( read_only=True)
    # verb = serializers.CharField()
    class Meta:
        model = Notification
        fields = '__all__'
