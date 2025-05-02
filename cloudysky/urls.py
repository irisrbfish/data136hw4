from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app.views import custom_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Include app's URLs
    path('login/', custom_login, name='login'),  # Use our custom login view
    path('accounts/login/', custom_login, name='accounts_login'),  # Add this for redirects
] 