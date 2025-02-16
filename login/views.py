from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'login/index.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user, `role` will be null by default
            login(request, user)  # Automatically log the user in after registration
            return redirect('work:home')  # Redirect to home or dashboard page
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('work:home')  # Redirect after successful login
        else:
            return render(request, 'login/login.html', {'error': 'Invalid credentials'})
    return render(request, 'login/login.html')

