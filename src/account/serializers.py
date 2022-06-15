from rest_framework import serializers
from .models import CustomUser
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
# User Details

class UserDetailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]
 
class UserLoginSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'password',
            'last_login',
        ]
   
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise ValueError("Email is already taken, please enter a different email address.")
        return value
class UserUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
        ]