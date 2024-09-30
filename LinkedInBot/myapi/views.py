from django.shortcuts import render, redirect  # Updated import
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import LinkedInProfile
import requests
from django.http import JsonResponse

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

def login(request):
    return redirect('/social-auth/login/linkedin-oauth2/')

# views.py

def post_to_linkedin(request):
    """Simulate posting an update to LinkedIn without real authentication."""

    # Simulate a user object for testing purposes
    class SimulatedUser:
        id = 1
        username = "test_user"
        social_auth = {
            'linkedin-oauth2': {
                'uid': '12345',  # Mock LinkedIn UID for testing
            }
        }

        def get(self, provider):
            return self.social_auth.get(provider)

    # Replace request.user with a simulated user
    request.user = SimulatedUser()

    try:
        # Mock LinkedIn access token for testing (Replace with a real token once OAuth is working)
        access_token = 'mock_access_token'

        # LinkedIn API URL for posting content
        url = 'https://api.linkedin.com/v2/shares'

        # Set up the request headers with authorization
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # The data that will be posted on LinkedIn (you can adjust this based on the user input)
        data = {
            "owner": f"urn:li:person:{request.user.get('linkedin-oauth2')['uid']}",
            "text": {
                "text": "This is a sample post from my LinkedIn bot!"
            },
            "distribution": {
                "linkedInDistributionTarget": {}
            }
        }

        # Send the POST request to LinkedIn API
        response = requests.post(url, headers=headers, json=data)

        # Check the response status
        if response.status_code == 201:
            return JsonResponse({'status': 'Post successful!'}, status=201)
        else:
            return JsonResponse({'status': 'Post failed', 'error': response.json()}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'status': 'An error occurred', 'error': str(e)}, status=500)


def dashboard(request):
    """Display user profile info after LinkedIn login."""
    user_profile = LinkedInProfile.objects.filter(user=request.user).first()
    return render(request, 'dashboard.html', {'profile': user_profile})
