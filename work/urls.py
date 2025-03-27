from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'work' 

urlpatterns = [
    path('<int:user_id>/', views.home, name='home'),  # Accept user_id in the URL
    path('logout/', LogoutView.as_view(next_page='login:index'), name='logout'),  # Logout view
    path('<int:user_id>/advancedMode/', views.advanced_mode , name='advanced_mode'),
    path('<int:user_id>/advancedMode/getResponse/',views.get_ai_response, name='get_ai_response'),
    path('save/', views.save_generated_website, name='save_generated_website'),
    path('<int:user_id>/history/', views.history, name='history'),
    path('<int:user_id>/history/<int:website_id>/', views.view_saved_website, name='view_saved_website'),
    path('<int:user_id>/history/<int:website_id>/code', views.view_code, name='view_code'),
    path('<int:user_id>/history/<int:website_id>/demo', views.demo, name='demo'),
    path('<int:user_id>/history/<int:website_id>/edit', views.edit_website, name='edit'),
    path('delete-website/<int:website_id>/', views.delete_website, name='delete_website'),
    path('<int:user_id>/templates', views.templates, name='templates'),
]