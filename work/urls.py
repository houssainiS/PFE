from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'work' 

urlpatterns = [
    path('<int:user_id>/', views.home, name='home'),  # Accept user_id in the URL
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),  # Logout view
    
    
]