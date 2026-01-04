"""
Custom authentication pipeline for social-auth (Auth0)
"""
from django.shortcuts import redirect


def check_patient_profile(strategy, backend, user, response, *args, **kwargs):
    """
    Check if a PATIENT user has a patient profile.
    If not, try to link to an existing patient profile by email.
    If no profile exists, prevent login and show an error message.
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
                # Patient profile doesn't exist for this user
                # Try to find an existing Patient profile with the same email
                from hospital.models import Patient
                
                try:
                    # Look for a Patient with matching email
                    existing_patient = Patient.objects.get(user__email=user.email)
                    
                    # Found a patient with this email!
                    # Link it to the current Auth0 user
                    existing_patient.user = user
                    existing_patient.save()
                    
                    # Profile now linked, allow login
                    return None
                    
                except Patient.DoesNotExist:
                    # No patient profile found with this email
                    # Delete the user account if it was just created (no social auth yet)
                    if not user.social_auth.exists():
                        user.delete()
                    
                    # Store error in session for one-time display
                    request = strategy.request
                    request.session['auth_error'] = 'Your patient profile does not exist. Please contact a receptionist to create your profile.'
                    
                    # Return redirect to login page to stop the pipeline
                    return redirect('hospital:login')
    
    # For all other roles, allow login
    return None

