from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapi.urls')),
    path('accounts/', include('allauth.urls')),  # This will handle the LinkedIn OAuth flow
    
]
