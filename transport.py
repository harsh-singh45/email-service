from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from config import settings

def send_email(to_emails: List[str], subject: str, html_body: str):
    """
    Sends a rich HTML email using the SendGrid API.
    """
    print(f"Attempting to send email via SendGrid. Subject: '{subject}', To: {', '.join(to_emails)}")

    # The from_email MUST be an email you have verified in your SendGrid account.
    from_email = settings.sendgrid_from_email
    api_key_to_use = settings.sendgrid_api_key

    # Create the SendGrid Mail object
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_body  # Directly use the generated HTML content
    )
    try:
        sg = SendGridAPIClient(api_key_to_use)
        response = sg.send(message)

        print(f"SendGrid response status code: {response.status_code}")
        print(f"Email successfully sent. Subject: '{subject}'")

    except Exception as e:
        print(f"An unexpected error occurred with SendGrid: {e}")
        # In a real application, you would want more robust error handling or logging.
        raise
