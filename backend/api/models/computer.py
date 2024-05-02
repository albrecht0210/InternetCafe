import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

class Computer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Computer name'), max_length=100, unique=True)

    STATUS_CHOICES = (
        (1, 'Available'),
        (2, 'Pending'),
        (3, 'In Use'),
        (4, 'Maintenance')
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    