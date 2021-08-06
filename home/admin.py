from django.contrib import admin

# Register your models here.
from .models import Device, Message, News


admin.site.register(Device)
admin.site.register(Message)
admin.site.register(News)