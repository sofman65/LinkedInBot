from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapi.urls')),  # Your API routes
    path('accounts/', include('allauth.urls')),  # For django-allauth authentication
    ]