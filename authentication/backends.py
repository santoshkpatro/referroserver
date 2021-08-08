from django.contrib.auth.backends import BaseBackend
from .models import User


class PhoneBackend(BaseBackend):
    def authenticate(self, request):
        pass

    def get_user(self, phone: str):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
