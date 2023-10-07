from django.contrib import admin

# Register your models here.
from .models import Space, Message, School, NewsletterSubscription, UserRating

admin.site.register(Space)
admin.site.register(Message)
admin.site.register(School)
admin.site.register(NewsletterSubscription)
admin.site.register(UserRating)