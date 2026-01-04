"""
Custom authentication pipeline for social-auth (Auth0)
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def check_patient_profile(strategy, backend, user, response, *args, **kwargs):
    """
    Check if a PATIENT user has a patient profile.
    If not, prevent login and show an error message.
    Also clean up the user session to allow the next user to log in.
    """
    if user and hasattr(user, 'role'):
        # Only check for PATIENT role users
        if user.role == 'PATIENT':
            # Check if patient profile exists
            try:
                user.patient_profile
                # Profile exists, allow login
                return None
            except Exception:
                # Patient profile doesn't exist
                # Delete the user account if it was just created (no social auth yet)
                # This prevents orphaned accounts from accumulating
                if not user.social_auth.exists():
                    user.delete()
                
                # Store error message in session
                request = strategy.request
                messages.error(
                    request,
                    'Your patient profile does not exist. Please contact a receptionist to create your profile.'
                )
                
                # Return redirect to login page to stop the pipeline
                # This will clean up the session and show the error
                return redirect('hospital:login')
    
    # For all other roles, allow login
    return None

