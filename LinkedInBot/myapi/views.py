from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import LinkedInProfile, PendingPost
import requests
import openai
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Fetch all pending posts (to be approved/rejected)
@api_view(['GET'])
@login_required
def pending_posts(request):
    posts = PendingPost.objects.filter(approved=False, rejected=False)
    serialized_posts = [{'id': post.id, 'text': post.text} for post in posts]
    return Response(serialized_posts, status=200)


# Helper function to get access token from session
def get_access_token_from_session(request):
    # Assuming the access token is stored in the session
    return request.session.get('access_token')



# Approve a post and send it to LinkedIn
@api_view(['POST'])
@login_required
def approve_post(request, post_id):
    try:
        post = PendingPost.objects.get(id=post_id)
        if post.approved or post.rejected:
            return Response({'error': 'Post already processed'}, status=400)

        # Mark the post as approved
        post.approved = True
        post.save()

        # Get the LinkedIn access token from the user's session or model
        linkedin_profile = LinkedInProfile.objects.filter(user=request.user).first()
        if not linkedin_profile or not linkedin_profile.access_token:
            return Response({'error': 'No LinkedIn access token found for the user.'}, status=400)
        
        access_token = linkedin_profile.access_token

        # Call LinkedIn API to post the content
        post_content = post.text
        url = "https://api.linkedin.com/v2/shares"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
        }
        data = {
            "content": {
                "contentEntities": [],
                "title": "Generated Post"
            },
            "owner": f"urn:li:person:{linkedin_profile.linkedin_uid}",
            "subject": "Generated Post",
            "text": {
                "text": post_content
            }
        }

        # Make POST request to LinkedIn API
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            return Response({'status': 'Post approved and published!'}, status=200)
        else:
            return Response({'error': 'Failed to post to LinkedIn', 'details': response.json()}, status=500)
    
    except PendingPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)


# Reject a post
@api_view(['POST'])
@login_required
def reject_post(request, post_id):
    try:
        post = PendingPost.objects.get(id=post_id)
        if post.approved or post.rejected:
            return Response({'error': 'Post already processed'}, status=400)
        
        # Mark the post as rejected
        post.rejected = True
        post.save()

        return Response({'status': 'Post rejected'}, status=200)
    
    except PendingPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)


# Endpoint to generate LinkedIn posts using AI (OpenAI)
@api_view(['POST'])
def generate_linkedin_post(request):
    prompt = request.data.get('prompt', None)
    
    if not prompt:
        return Response({'error': 'No prompt provided'}, status=400)
    
    openai.api_key = settings.OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            stream=True
        )
        post_content = response.choices[0].text.strip()



        # Create a PendingPost and save it to the database
        user = request.user  # Assuming user is logged in
        pending_post = PendingPost.objects.create(text=post_content, user=user)

        return Response({'post_content': post_content, 'status': 'Pending approval'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# Endpoint to post the generated content to LinkedIn
@api_view(['POST'])
def post_to_linkedin(request):
    access_token = request.data.get('access_token', None)  # Get access token from React
    post_content = request.data.get('post_content', None)

    if not access_token or not post_content:
        return Response({'error': 'Missing access token or post content'}, status=400)

    # LinkedIn API logic to post the content
    url = "https://api.linkedin.com/v2/shares"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
    }
    data = {
        "content": {
            "contentEntities": [],
            "title": "Generated Post"
        },
        "owner": f"urn:li:person:xxxx",  # Replace with the correct LinkedIn user URN
        "subject": "Generated Post",
        "text": {
            "text": post_content
        }
    }

    # Make POST request to LinkedIn API
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return Response({'status': 'Post successful!'}, status=200)
    else:
        return Response({'error': 'Failed to post to LinkedIn', 'details': response.json()}, status=500)


# Dashboard view
@login_required
def dashboard(request):
    """Display user profile info after LinkedIn login."""
    user_profile = LinkedInProfile.objects.filter(user=request.user).first()
    return render(request, 'dashboard.html', {'profile': user_profile})
