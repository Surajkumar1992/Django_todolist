from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout


# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'forms': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'forms': UserCreationForm(), 'error': 'The Username is already taken '})
        else:
            return render(request, 'todo/signup.html', {'forms': UserCreationForm(), 'error':'Password didn\'t match' })

def current(request):
    return render(request, 'todo/current.html')

def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todo/home.html')