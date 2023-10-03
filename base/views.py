from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from .forms import UserForm, SpaceForm, NewsletterSubscriptionForm
from .models import Space, Message, School, NewsletterSubscription, SpaceRating

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
    
    context = {'spaces': spaces, 'space_count': space_count, 'schools': schools, 'space_messages': space_messages}
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
    context = {'user':user, 'spaces':spaces,'space_messages':space_messages, 'schools': schools}
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
def rate_space(request,pk):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review = request.POST.get('review')
        user = request.user

        # Check if the user has already rated the product
        existing_rating = SpaceRating.objects.filter(user=user, space_id=pk).first()

        if existing_rating:
            # Update the existing rating
            existing_rating.rating = rating
            existing_rating.review = review
            existing_rating.save()
        else:
            # Create a new rating
            SpaceRating.objects.create(user=user, space_id= pk, rating=rating, review=review)

        # Redirect back to the product detail page or wherever you want
        return redirect('product_detail', space_id=pk)