from django.contrib import admin

# Register your models here.
from .models import Space, Message, School

admin.site.register(Space)
admin.site.register(Message)
admin.site.register(School)

