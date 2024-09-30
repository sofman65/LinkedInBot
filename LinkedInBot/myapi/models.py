# models.py

from django.contrib.auth.models import User
from django.db import models

class LinkedInProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin_access_token = models.CharField(max_length=255)
    linkedin_uid = models.CharField(max_length=255)
    profile_picture_url = models.URLField(max_length=512, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - LinkedIn Profile"
