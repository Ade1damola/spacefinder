from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Space(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey (School, on_delete=models.SET_NULL, null=True)
    hostel = models.CharField(max_length=200)
    room_number = models.CharField(max_length=5)
    price = models.PositiveIntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.hostel
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="message")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    

class NewsletterSubscription(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=15,
        blank=True,  
        null=True,   
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class SpaceRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()
