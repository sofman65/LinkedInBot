# models.py (in your app 'myapi')

from django.db import models
from django.contrib.auth.models import User

class LinkedInProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin_uid = models.CharField(max_length=255, default='default_value')  # Add a default value here
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s LinkedIn Profile"

class PendingPost(models.Model):
    text = models.TextField()  # The generated post content
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Whether the post is approved
    rejected = models.BooleanField(default=False)  # Whether the post is rejected
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who generated the post
    
    def __str__(self):
        return f"Post by {self.user.username} - Approved: {self.approved}, Rejected: {self.rejected}"