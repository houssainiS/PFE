from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Subscription


admin.site.register(Subscription)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role')  # Fields to display in the admin list view
    list_filter = ('role',)  # Allow filtering by role in the admin list view
    search_fields = ('username', 'email')  # Allow searching by username and email
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field to the admin form
    )

# Register your custom User model in the admin panel
admin.site.register(User, CustomUserAdmin)