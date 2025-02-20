from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import User  # Import your custom User model
import openai
from django.http import JsonResponse
import environ
from django.core.exceptions import ImproperlyConfigured
# Initialize environ
env = environ.Env()
import os
# Specify the full path to the .env file
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
environ.Env.read_env(env_file)

#temprary
import os
from django.http import HttpResponse

# AI API settings

try:
    openai.api_key = env('OPENAI_API_KEY')
except KeyError:
    raise ImproperlyConfigured("Set the OPENAI_API_KEY environment variable")

def ask_openai(message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=50,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
    
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


@login_required(login_url='login')
def getResponse(request, user_id):
    user_message = request.GET.get('userMessage', '')

    if not user_message:
        return JsonResponse({"response": "Please enter a message."})

    try:
        # Get the response from OpenAI
        chat_response = ask_openai(user_message)
    except Exception as e:
        chat_response = f"Error: {str(e)}"

    return JsonResponse({"response": chat_response})