"""
Manages the generation of email content from predefined templates.
"""
from typing import Dict
from jinja2 import Template

# --- Base Template ---
# A simple, clean base structure for all emails.
HTML_WRAPPER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .button { display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 3px; }
        .footer { margin-top: 20px; font-size: 0.8em; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        {{ body_content | safe }}
        <div class="footer">
            <p>The {{ company_name }} Team</p>
        </div>
    </div>
</body>
</html>
"""

def render_template(subject: str, body_html: str, data: Dict) -> str:
    """Renders the final HTML email by wrapping content in the base template."""
    wrapped_body = Template(body_html).render(data)
    final_html = Template(HTML_WRAPPER).render(subject=subject, body_content=wrapped_body, company_name=data.get("company_name", "Company"))
    return final_html

# --- Template Definitions ---

def get_subscription_end_notification(data: Dict) -> (str, str):
    """Generates the 'Subscription Ending' email content."""
    subject = "Your Subscription is About to End — Renew Today!"
    body = """
    <p>Hi {{ FirstName }},</p>
    <p>We noticed your subscription to <strong>{{ ProductServiceName }}</strong> is ending on <strong>{{ EndDate }}</strong>. We’d hate to see you miss out on all the benefits — exclusive updates, premium content, and priority support.</p>
    <p>Renew now to continue uninterrupted access:</p>
    <p><a href="#" class="button">👉 Renew My Subscription</a></p>
    <p>If you’ve already renewed, thank you! Please disregard this message.</p>
    <p>Best regards,</p>
    """
    html_content = render_template(subject, body, data)
    return subject, html_content

def get_opt_in_confirmation(data: Dict) -> (str, str):
    """Generates the 'Opt-In Confirmation' email content."""
    subject = "Please Confirm Your Subscription"
    body = """
    <p>Hi {{ FirstName }},</p>
    <p>Thanks for your interest in {{ company_name }}!</p>
    <p>To make sure we’ve got your permission, please confirm your subscription by clicking the button below:</p>
    <p><a href="#" class="button">✅ Confirm My Subscription</a></p>
    <p>Once confirmed, you’ll receive updates on our latest offers, news, and insights.</p>
    <p>If you didn’t request this, simply ignore this email.</p>
    <p>Warm regards,</p>
    """
    html_content = render_template(subject, body, data)
    return subject, html_content

def get_newsletter_template(data: Dict) -> (str, str):
    """Generates the 'Newsletter' email content."""
    subject = f"{data.get('Month', 'This Month')} Highlights – News, Tips & What’s Next!"
    body = """
    <p>Hello {{ FirstName }},</p>
    <p>Here’s what’s new this month at {{ company_name }}:</p>
    <h4>📰 In the Spotlight: {{ Headline1 }}</h4>
    <p><i>A brief description or introduction to the main headline can go here, expanding on the topic.</i></p>
    <h4>💡 Pro Tip: {{ TipOrInsight }}</h4>
    <p><i>Elaborate on the tip, providing actionable advice your readers can use.</i></p>
    <h4>📅 Upcoming Event: {{ EventName }} on {{ EventDate }}</h4>
    <p><i>Give some more details about the event and why people should be excited to attend or participate.</i></p>
    <h4>🎁 Exclusive Offer: {{ OfferDetails }}</h4>
    <p><i>Explain the offer in more detail and create a sense of urgency or exclusivity.</i></p>
    <p>Stay tuned for more updates and insights in next month’s edition!</p>
    <p>Cheers,</p>
    """
    html_content = render_template(subject, body, data)
    return subject, html_content

def get_product_launch_announcement(data: Dict) -> (str, str):
    """Generates the 'New Product Launch' email content."""
    subject = f"Introducing Our New {data.get('ProductName', 'Product')} – It’s Finally Here! 🚀"
    body = """
    <p>Hi {{ FirstName }},</p>
    <p>We’re thrilled to announce the launch of our latest innovation — <strong>{{ ProductName }}</strong>!</p>
    <p>Designed to {{ ProductBenefit }}, this is a game-changer you won’t want to miss.</p>
    <h4>✨ Key Features:</h4>
    <ul>
        <li>{{ Feature1 }}</li>
        <li>{{ Feature2 }}</li>
        <li>{{ Feature3 }}</li>
    </ul>
    <p><a href="#" class="button">Be among the first to experience it → Learn More / Buy Now</a></p>
    <p>Thank you for being part of our journey!</p>
    """
    html_content = render_template(subject, body, data)
    return subject, html_content
