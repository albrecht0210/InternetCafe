import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)