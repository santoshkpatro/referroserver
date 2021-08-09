import uuid
from django.db import models
from programs.models import Program


class Member(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='members')
    username = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = uuid.uuid4().hex[:15].upper()
        super(Program, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username
