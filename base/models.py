from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Space(models.Model):
    LOCATION_CHOICES = [
        ('on-campus', 'On-Campus'),
        ('off-campus', 'Off-Campus'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey (School, on_delete=models.SET_NULL, null=True)
    hostel = models.CharField(max_length=200)
    room_number = models.CharField(max_length=5)
    price = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True) 
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, null=True)
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


class ContactFormSubmission(models.Model):
    subject = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        blank=True,  
        null=True,   
    )
    message = models.TextField()

    def __str__(self):
        return self.email


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class UserRating(models.Model):
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given', null=True)
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received', null=True)
    rating = models.PositiveIntegerField()  # You can define the rating scale as per your requirements

    class Meta:
        unique_together = ('rated_by', 'rated_user')  # Ensure each user can rate another user only once

    def __str__(self):
        return f"{self.rated_by.username} -> {self.rated_user.username} ({self.rating})"
