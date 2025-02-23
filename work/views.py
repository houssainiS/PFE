from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import User  # Import your custom User model
import openai
from django.http import JsonResponse
import environ
from django.core.exceptions import ImproperlyConfigured
import os
import re

# Initialize environ
env = environ.Env()
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
environ.Env.read_env(env_file)

# AI API settings
try:
    openai.api_key = env('OPENAI_API_KEY')
except KeyError:
    raise ImproperlyConfigured("Set the OPENAI_API_KEY environment variable")

def ask_openai(message):
    # Adjust the prompt to request specific code generation
    prompt = f"Please generate the complete HTML code for a website based on the following description: {message}. Only include the contents inside the `<body>`, `<script>`, and `<style>` tags. The `<style>` tag should include the necessary CSS for layout, colors, fonts, and spacing, or be left empty if no styles are needed. The `<script>` tag should contain any JavaScript functionality, or be left empty if no JavaScript is required. Do not include the overall HTML structure, such as `<html>`, `<head>`, or external file references (no `<link>` or `<script src=...>` tags). Only provide the contents inside the `<body>`, `<script>`, and `<style>` tags."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
 
#excrat the code needed in html 



def extract_code_parts(ai_response):
    """Extract only the CSS, JavaScript, and HTML body content from the AI response."""
    
    # Print the full AI response for debugging
    print("Full AI response:")
    print(ai_response)
    print("\n" + "="*50 + "\n")  # Separator for better readability

    # Remove Markdown code block delimiters (```), ensuring we handle it correctly
    ai_response = re.sub(r"```(html|css|javascript)?\s*([\s\S]*?)```", r"\2", ai_response)

    # Improved regex for extracting body, style, and script sections
    body_match = re.search(r"<body[\s\S]*?</body>", ai_response, re.DOTALL | re.IGNORECASE)  # Match the <body> content
    css_match = re.search(r"<style[\s\S]*?</style>", ai_response, re.DOTALL | re.IGNORECASE)  # Match the <style> content
    js_match = re.search(r"<script[\s\S]*?</script>", ai_response, re.DOTALL | re.IGNORECASE)  # Match the <script> content

    # Extract the content
    body_content = body_match.group(0) if body_match else "No body content found."
    css_content = css_match.group(0) if css_match else "No CSS content found."
    js_content = js_match.group(0) if js_match else "No JS content found."

    # Print the extracted content for debugging
    print("Body Content:")
    print(body_content)
    print("\nCSS Content:")
    print(css_content)
    print("\nJS Content:")
    print(js_content)

    return {
        "body": body_content,
        "css": css_content,
        "js": js_content
    }

# Ensure user is authenticated before accessing views
@login_required(login_url='login')  # Redirect to login if not authenticated
def home(request, user_id):
    user = get_object_or_404(User, id=user_id)
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

# def getResponse(request, user_id):
#     user_message = request.GET.get('userMessage', '')

#     if not user_message:
#         return JsonResponse({"response": "Please enter a message."})

#     try:
#         # Get the response from OpenAI (adjusted prompt to ask for actual code)
#         chat_response = ask_openai(user_message)
#     except Exception as e:
#         chat_response = f"Error: {str(e)}"

#     # Return the generated HTML/CSS/JS code from OpenAI
#     return JsonResponse({"response": chat_response})

#testing

def get_ai_response(request, user_id):
    user_message = request.GET.get("userMessage", "")
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    ai_response = ask_openai(user_message)
    extracted_code = extract_code_parts(ai_response)

    return JsonResponse(extracted_code)