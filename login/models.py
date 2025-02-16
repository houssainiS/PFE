from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Make email unique
    role = models.CharField(max_length=100, null=True, blank=True)  # role field is nullable

    class Meta:
        db_table = 'user'  # Set the table name to 'user'
