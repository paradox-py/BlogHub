from django.core.mail import send_mail
from django.conf import settings
from .models import Blog

def share_blog(subject, message, blog, recipient_email):
    if not isinstance(blog, Blog):
        raise ValueError("The 'blog' parameter must be an instance of Blog")
    
    # Construct the full URL manually
    site_url = settings.SITE_URL  # Make sure you set this in settings.py
    full_url = f'{site_url}{blog.get_absolute_url()}'
    
    # Construct the full message
    full_message = f'{message}\n\nRead more at: {full_url}'

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]  # Ensure this is a list

    send_mail(
        subject,
        full_message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
