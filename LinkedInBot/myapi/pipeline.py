# myapp/pipeline.py

from .models import LinkedInProfile

def save_profile(backend, user, response, *args, **kwargs):
    """Store LinkedIn access token and profile information after successful authentication."""
    if backend.name == 'linkedin-oauth2':
        access_token = response.get('access_token')
        id_token = response.get('id_token')

        # Extract the user's profile details
        linkedin_uid = response.get('id')
        profile_picture = response.get('picture')

        # Save or update the user's LinkedIn profile in the database
        LinkedInProfile.objects.update_or_create(
            user=user,
            defaults={
                'linkedin_access_token': access_token,
                'linkedin_uid': linkedin_uid,
                'profile_picture_url': profile_picture,
            }
        )
