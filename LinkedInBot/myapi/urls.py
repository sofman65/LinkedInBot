# urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='yourapp/login.html'), name='login'),
    path('accounts/', include('allauth.urls')),  # Includes allauth URLs
]
