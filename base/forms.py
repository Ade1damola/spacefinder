from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Space, NewsletterSubscription, ContactFormSubmission

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class SpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = '__all__'
        exclude = ['host']


class NewsletterSubscriptionForm(ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormSubmission
        fields = ['subject','fullname', 'email','phone_number', 'message']