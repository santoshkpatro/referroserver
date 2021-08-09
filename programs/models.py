import uuid
from django.db import models
from authentication.models import User


class Program(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=100)
    incentive = models.DecimalField(max_digits=8, decimal_places=2)

    access_token = models.UUIDField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = uuid.uuid4().hex[:10].upper()
        super(Program, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def generate_access_token(self):
        self.access_token = uuid.uuid4()
        self.save()
        return str(self.access_token)
