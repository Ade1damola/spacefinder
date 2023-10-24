from django.forms import ModelForm, CharField
from django.contrib.auth.models import User
from .models import Space, NewsletterSubscription, ContactFormSubmission

class UserForm(ModelForm):
    first_name = CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


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