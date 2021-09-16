from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


#Singup User
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


#Current User
@login_required
def current(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/current.html', {'todos': todos})

#Login User
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'forms': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo/login.html', {'forms': AuthenticationForm(), 'error': 'Username and Password didnt match'})
        else:
            login(request, user)
            return redirect('current')

#Logout User
@login_required
def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')

#Create TodoList
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'forms': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/createTodo.html', {'error': 'Bad data passed, Please try again!!! '})

#View Todos
@login_required
def viewtodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todos)
        return render(request, 'todo/todoDetails.html', {'todos': todos, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todos)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/todoDetails.html', {'error': 'Bad Information Passed'})


#Complete Todos
@login_required
def completetodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.datecompleted = timezone.now()
        todos.save()
        return redirect('current')

@login_required
def deletetodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('current')

#Completed Todos List
@login_required
def completedtodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

#HomePage
def home(request):
    return render(request, 'todo/home.html')

