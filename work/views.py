from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import User  # Import your custom User model

# Ensure user is authenticated before accessing views
@login_required(login_url='login')  # Redirect to login if not authenticated
def home(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get user or return 404
    if user != request.user:  # Prevent access to other users' pages
        return redirect('home', user_id=request.user.id)  
    return render(request, 'work/home.html', {'user': user})

@login_required(login_url='login')
def simple_mode(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return redirect('home', user_id=request.user.id)  
    return render(request, 'work/simpleMode.html', {'user': user})

@login_required(login_url='login')
def advanced_mode(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return redirect('home', user_id=request.user.id)  
    return render(request, 'work/advancedMode.html', {'user': user})
