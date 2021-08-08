import random
import pyotp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.conf import settings


class Role(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    profile = models.URLField(blank=True, null=True)

    verify_counter = models.IntegerField(default=0, blank=True, null=True)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    roles = models.ManyToManyField(Role, blank=True)

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def generate_phone_otp(self):
        self.verify_counter = random.randint(10, 10000)
        self.save()
        hotp = pyotp.HOTP(settings.SECRET_OTP_TOKEN)
        return hotp.at(self.verify_counter)

    def verify_phone_otp(self, otp):
        hotp = pyotp.HOTP(settings.SECRET_OTP_TOKEN)
        return hotp.verify(otp, self.verify_counter)

    def reset_counter(self):
        self.verify_counter = random.randint(10, 10000)
        self.save()
