from rest_framework import serializers
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_active', 'verify_counter', 'is_admin', 'is_email_verified', 'is_phone_verified', 'roles')
