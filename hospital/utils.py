"""
Utility functions for the hospital application
"""
import logging
import threading
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_email_async(subject, html_content, to_email, from_email=None, plain_content=None):
    """
    Send email asynchronously in a background thread
    
    Args:
        subject (str): Email subject
        html_content (str): HTML content of the email
        to_email (list): List of recipient email addresses
        from_email (str): Sender email address (optional)
        plain_content (str): Plain text content (optional)
    """
    def _send_email():
        try:
            if not from_email:
                sender = settings.DEFAULT_FROM_EMAIL
            else:
                sender = from_email
            
            # Create email with HTML and plain text
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_content or f"Please view this email in an HTML-enabled email client.",
                from_email=sender,
                to=to_email if isinstance(to_email, list) else [to_email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)
            
            logger.info(f"Email sent successfully to {to_email}")
        except Exception as e:
            logger.warning(f"Failed to send email to {to_email}: {str(e)}")
    
    # Start email sending in background thread
    thread = threading.Thread(target=_send_email, daemon=True)
    thread.start()
    logger.info(f"Email queued for async sending to {to_email}")
