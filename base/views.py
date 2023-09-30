from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from .forms import UserForm, SpaceForm
from .models import Space, Messages

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    spaces = Space.objects.filter(
        Q(school__icontains=q) | 
        Q(hostel__icontains=q) |
        Q(price__icontains=q)
        )
    spaces = Space.objects.all()
    space_count = spaces.count()
    
    context = {'spaces': spaces, 'space_count': space_count}
    return render(request, 'base/home.html', context)


def space(request, pk):
    space = Space.objects.get(id=pk)
    space_messages = space.messages.all()

    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user,
            space = space,
            body = request.POST.get('body')
        )
        return redirect('space', pk=space.id)

    context = {'space': space, 'space_messages': space_messages,}
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
    context = {'user':user}
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
    if request.method == 'POST':
        Space.objects.create(
            host=request.user,
            school=request.POST.get('school'),
            hostel=request.POST.get('hostel'),
            room_number=request.POST.get('room_number'),
            price=request.POST.get('price'),
        )
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/space-form.html', context)


@login_required(login_url='login')
def updateSpace(request, pk):
    space = Space.objects.get(id=pk)
    form = SpaceForm(instance=space)

    if request.user != space.host:
        return HttpResponse("You're not allowed to do this!!!")
    
    if request.method == 'POST':
        space.name = request.POST.get('name')
        return redirect('home')
    context = {'form': form, 'space': space}
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
    message = Messages.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You're not allowed to do this!!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message}) 