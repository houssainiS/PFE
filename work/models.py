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
