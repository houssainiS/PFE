from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import User
import openai
from django.http import JsonResponse
import environ
from django.core.exceptions import ImproperlyConfigured
import os
import re
from .models import GeneratedWebsite
# Initialize environ
env = environ.Env()
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
environ.Env.read_env(env_file)

# AI API settings
try:
    openai.api_key = env('OPENAI_API_KEY')
except KeyError:
    raise ImproperlyConfigured("Set the OPENAI_API_KEY environment variable")

# DALL·E 2 image generation function
from openai import OpenAI
client = OpenAI()

def ask_dalle_2(prompt):
    """Generates an image from DALL·E 2 based on the given prompt using the new API."""
    try:
        # Make the API call to generate the image
        response = client.images.generate(
            prompt=prompt,  # Use the prompt provided
            size="256x256",  # Use supported size (256x256)
            quality="standard",  # Quality setting
            n=1,
        )
        
        # Extract the URL of the generated image
        image_url = response.data[0].url
        
        print(f"Image generated for prompt: {prompt}")
        return image_url
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def ask_openai(message):
    """Generates the HTML, CSS, and JS from OpenAI based on user input."""
    prompt = f"Please generate the complete HTML code for a website based on the following description: {message}. Only include the contents inside the `<body>`, `<script>`, and `<style>` tags. The `<style>` tag should include the necessary CSS for layout, colors, fonts, and spacing, or be left empty if no styles are needed. The `<script>` tag should contain any JavaScript functionality, or be left empty if no JavaScript is required. Do not include the overall HTML structure, such as `<html>`, `<head>`, or external file references (no `<link>` or `<script src=...>` tags). Only provide the contents inside the `<body>`, `<script>`, and `<style>` tags."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

def extract_code_parts(ai_response, generate_images):
    """Extract only the CSS, JavaScript, and HTML body content from the AI response and generate images if needed."""
    
    print("Full AI response:")
    print(ai_response)
    print("\n" + "="*50 + "\n")  # Separator for better readability

    ai_response = re.sub(r"```(html|css|javascript)?\s*([\s\S]*?)```", r"\2", ai_response)

    body_match = re.search(r"<body[\s\S]*?</body>", ai_response, re.DOTALL | re.IGNORECASE)
    css_match = re.search(r"<style[\s\S]*?</style>", ai_response, re.DOTALL | re.IGNORECASE)
    js_match = re.search(r"<script[\s\S]*?</script>", ai_response, re.DOTALL | re.IGNORECASE)

    body_content = body_match.group(0) if body_match else "No body content found."
    css_content = css_match.group(0) if css_match else "No CSS content found."
    js_content = js_match.group(0) if js_match else "No JS content found."
    
    # Check if image generation is enabled and if there are image tags in the body content
    if generate_images:
        img_tags = re.findall(r'<img [^>]*src="([^"]+)', body_content)
        print(f"Found {len(img_tags)} image(s) in the body content.")

        # Replace image sources with generated URLs
        for img_tag in img_tags:
            generated_image_url = ask_dalle_2(img_tag)  # Generate the image based on the prompt
            if generated_image_url:
                body_content = body_content.replace(img_tag, generated_image_url)

        # Print the body content after replacements
        print("\nModified Body Content After Replacing Image URLs:")
        print(body_content)

    return {
        "body": body_content,
        "css": css_content,
        "js": js_content
    }

def get_ai_response(request, user_id):
    user_message = request.GET.get("userMessage", "")
    generate_images = request.GET.get("generateImages", "false").lower() == "true"  # Capture the image switch state
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    ai_response = ask_openai(user_message)
    extracted_code = extract_code_parts(ai_response, generate_images)  # Pass the generateImages flag

    return JsonResponse(extracted_code)


# Ensure user is authenticated before accessing views
@login_required(login_url='login')
def home(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return redirect('home', user_id=request.user.id)
    return render(request, 'work/home.html', {'user': user})


@login_required(login_url='login')
def advanced_mode(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return redirect('home', user_id=request.user.id)
    return render(request, 'work/advancedMode.html', {'user': user})


@login_required
def save_generated_website(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        prompt = request.POST.get('prompt')
        body = request.POST.get('body', '')  # Assuming body is passed via AJAX
        css = request.POST.get('css', '')  # Optional, if you're passing css as well
        js = request.POST.get('js', '')    # Optional, if you're passing js as well
        
        # Create a new GeneratedWebsite instance and save it
        website = GeneratedWebsite.objects.create(
            user=request.user,
            title=title,
            body=body,
            css=css,
            js=js,
            prompt=prompt,
        )

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Website saved successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)



###################history page
# History page function
@login_required
def history(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get the user by ID
    saved_websites = GeneratedWebsite.objects.filter(user=user).order_by('-created_at')  # Filter by the logged-in user
    return render(request, 'work/history.html', {'saved_websites': saved_websites})


@login_required
def view_saved_website(request, user_id, website_id):
    website = get_object_or_404(GeneratedWebsite, id=website_id)
    return render(request, 'work/view_saved_website.html', {'website': website})



#see code page
def view_code(request, user_id, website_id):
    website = get_object_or_404(GeneratedWebsite, id=website_id)

    # Construct the full code including CSS, Body, and JS
    full_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{website.title}</title>
    <style>{website.css}</style>  <!-- Ensure CSS is included -->
</head>
<body>
    {website.body}
    <script>{website.js}</script>  <!-- Ensure JS is included -->
</body>
</html>"""

    # Split full code into lines for proper display
    code_lines = full_code.splitlines()

    return render(request, 'work/code.html', {
        'website': website,
        'code_lines': code_lines
    })

#demo page

def demo(request, user_id, website_id):
    website = get_object_or_404(GeneratedWebsite, id=website_id)
    return render(request, 'work/demo.html', {'website': website})

#editing page

@login_required
def edit_website(request,user_id, website_id):
    website = get_object_or_404(GeneratedWebsite, id=website_id)

    if request.method == "POST":
        new_body = request.POST.get("body", "")  # Get the updated body content
        website.body = new_body  # Update only the body
        website.save()  # Save changes

        return JsonResponse({"success": True})  # Return success response

    return render(request, "work/edit.html", {"website": website})

#delete 1 history 

@login_required
def delete_website(request, website_id):
    website = get_object_or_404(GeneratedWebsite, id=website_id, user=request.user)
    website.delete()
    return JsonResponse({"success": True})