# utils.py

import requests
from django.utils import timezone
from datetime import timedelta
def refresh_access_token(user_profile):
    """
    Function to refresh the LinkedIn access token using the refresh token.
    """
    refresh_token = user_profile.linkedin_refresh_token

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': '771867qn4hv7ov',
        'client_secret': 'WPL_AP1.NvZe8venmmJCugpQ.IYHICg==',
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        user_profile.linkedin_access_token = token_data['access_token']
        user_profile.token_expires_at = timezone.now() + timedelta(seconds=token_data['expires_in'])
        user_profile.save()
    else:
        # Handle token refresh error here
        raise Exception("Failed to refresh LinkedIn access token.")
