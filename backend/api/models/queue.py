import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

class Queue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField('Account', on_delete=models.CASCADE, unique=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, blank=True, null=True)
    # account = models.ForeignKey('Account', on_delete=models.CASCADE, unique=True)
    number = models.CharField(_('Number'), null=True, blank=True, max_length=6)
    
    STATUS_CHOICES = (
        (1, 'Waiting'),
        (2, 'Now Serving'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('account', 'status')

    def __str__(self):
        return self.account