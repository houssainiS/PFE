from django.shortcuts import render
from login.models import User 
# Create your views here.

def home(request, user_id):
    user = User.objects.get(id=user_id)  # Get the user by ID using your custom model
    return render(request, 'work/home.html', {'user': user})