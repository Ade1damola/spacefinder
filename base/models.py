from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Space(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    school = models.CharField(max_length=200)
    hostel = models.CharField(max_length=200)
    room_number = models.CharField(max_length=5)
    price = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return {
            'school': self.school,
            'hostel': self.hostel,
            'room_number': self.room_number,
            'price': self.price,
                }
    
class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]