from django.db import models
from members.models import Member
from programs.models import Program


class Order(models.Model):
    STATUS_CHOICES = (
        ('Initiated', 'Initiated'),
        ('Disputed', 'Disputed'),
        ('Claimed', 'Claimed'),
        ('Completed', 'Completed'),
    )

    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='member_orders')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name='program_orders')
    claim_amount = models.DecimalField(max_digits=9, decimal_places=2)
    charge_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Initiated')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)
