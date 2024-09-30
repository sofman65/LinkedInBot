# urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='myapi/login.html'), name='login'),
    path('accounts/', include('allauth.urls')),  # Includes allauth URLs
    path('dashboard/', views.dashboard, name='dashboard'),  # Add this line
    path('generate-linkedin-post/', views.generate_linkedin_post, name='generate_linkedin_post'),
    path('post-to-linkedin/', views.post_to_linkedin, name='post_to_linkedin'),
    path('approve-post/<int:post_id>/', views.approve_post, name='approve_post'),
    path('reject-post/<int:post_id>/', views.reject_post, name='reject_post'),
    path('pending-posts/', views.pending_posts, name='pending_posts'),
]
