from django.contrib import admin
from .models import Account, Computer, Queue, Session
# Register your models here.

admin.site.register(Account)
admin.site.register(Computer)
admin.site.register(Queue)
admin.site.register(Session)
