from django.conf import settings
from django.db import models

class GeneratedWebsite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    prompt = models.TextField(blank=True)  # New field to store the user input (prompt)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "generated_website"  # Custom table name

    def __str__(self):  # Indentation fixed
        return f"{self.title} - {self.user.username}"


class Template(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    theme = models.CharField(max_length=100)
    code = models.TextField()  # Stores the generated HTML, CSS, and JS
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
