from django.contrib import admin

# Register your models here.
from .models import Space, Messages

admin.site.register(Space)
admin.site.register(Messages)

