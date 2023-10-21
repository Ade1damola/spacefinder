from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from .forms import UserForm, SpaceForm, NewsletterSubscriptionForm
from .models import Space, Message, School, NewsletterSubscription, UserRating
from .models import UserRating


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    spaces = Space.objects.filter(
        Q(school__name__icontains=q) |
        Q(hostel__icontains=q) |
        Q(price__icontains=q)
        )
    
    space_count = spaces.count()
    schools = School.objects.all()
    space_messages = Message.objects.filter(Q(space__school__name__icontains=q))
    
    context = {'spaces': spaces, 'space_count': space_count, 'schools': schools,
                'space_messages': space_messages}
    return render(request, 'base/home.html', context)


def space(request, pk):
    space = Space.objects.get(id=pk)
    space_messages = space.message.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            space = space,
            body = request.POST.get('body')
        )
        return redirect('space', pk=space.id)

    context = {'space': space, 'space_messages': space_messages}
    return render(request, 'base/space.html', context)


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
           user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occourred during registration!')

    return render(request, 'base/login_register.html', {'form': form})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    spaces = user.space_set.all()
    space_messages = user.message_set.all()
    schools = School.objects.all()
    ratings_received = UserRating.objects.filter(rated_user=user)
    
    # Calculate the average rating for the user (if ratings exist)
    average_rating = ratings_received.aggregate(Avg('rating'))['rating__avg']
    context = {'user':user, 'spaces':spaces,'space_messages':space_messages, 'schools': schools, 'rating': average_rating}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


@login_required(login_url='login')
def createSpace(request):
    form = SpaceForm()
    school = School.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        school, created = School.objects.get_or_create(name=topic_name)

        Space.objects.create(
            host=request.user,
            school=school,
            hostel=request.POST.get('hostel'),
            room_number=request.POST.get('room_number'),
            price=request.POST.get('price')
        )
        return redirect('home')
    
    context = {'form': form, 'school': school}
    return render(request, 'base/space-form.html', context)


@login_required(login_url='login')
def updateSpace(request, pk):
    space = get_object_or_404(Space, id=pk)
    
    if request.user != space.host:
        return HttpResponse("You're not allowed to do this!!!")

    if request.method == 'POST':
        form = SpaceForm(request.POST, instance=space)
        if form.is_valid():
            school_name = request.POST.get('school')
            school, created = School.objects.get_or_create(name=school_name)

            space.school = school
            space.hostel = request.POST.get('hostel')
            space.room_number = request.POST.get('room_number')
            space.price = request.POST.get('price')
            space.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during space update!')
    
    form = SpaceForm(instance=space)
    schools = School.objects.all()
    context = {'form': form, 'space': space, 'schools': schools}
    return render(request, 'base/space-form.html', context) 


@login_required(login_url='login')
def deleteSpace(request, pk):
    space = Space.objects.get(id=pk)

    if request.user != space.host:
        return HttpResponse("You're not allowed to do this!!!")

    if request.method == 'POST':
        space.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':space}) 


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You're not allowed to do this!!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message}) 


def subscribe_to_newsletter(request):
    form = NewsletterSubscriptionForm()
    if request.method == 'POST':

        NewsletterSubscription.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number')
        )
        if form.is_valid():
            form.save()
            # Optionally, you can send a confirmation email here.
            return redirect('about')  # Redirect back to the "About" section.

    # Handle form display here (GET request) or form validation errors.
    return render(request, 'base/contact.html', {'form': form})


@login_required(login_url='login')
def rate_user(request, rated_user_id):
    if request.method == 'POST':
        rater = request.user
        rated_user = User.objects.get(pk=rated_user_id)
        rating_value = int(request.POST.get('rating'))

        # Check if the rater has already rated the user
        existing_rating = UserRating.objects.filter(rated_by=rater, rated_user=rated_user).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            UserRating.objects.create(rated_by=rater, rated_user=rated_user, rating=rating_value)

    # Redirect back to the user's profile or another appropriate page
    return redirect('user_profile', user_id=rated_user_id)


def about(request):


    return render(request, 'base/about.html')


def contact(request):


    return render(request, 'base/contact.html')

def accomodation(request):


    return render(request, 'base/accomodation.html')

def confirm_pay(request):


    return render(request, 'base/confirm_pay.html')


def hostel(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    spaces = Space.objects.filter(
        Q(school__name__icontains=q) |
        Q(hostel__icontains=q) |
        Q(price__icontains=q) |
        Q(gender__icontains=q) |
        Q(location__icontains=q)
        )
    
    space_count = spaces.count()
    schools = School.objects.all()
    space_messages = Message.objects.filter(Q(space__school__name__icontains=q))
    
    context = {'spaces': spaces, 'space_count': space_count, 'schools': schools,
                'space_messages': space_messages}
    return render(request, 'base/hostel.html', context)