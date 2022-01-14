from .models import *
from rest_framework import serializers
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password','user_type']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FileSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField('get_file_url')
    def get_file_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.file)


    class Meta:
        model = FileUpload
        fields='__all__'
        extra_fields = ('file_path')
    
    
