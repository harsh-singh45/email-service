import uvicorn
from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any

import transport
import templates
from config import settings

# --- Initialize the FastAPI app ---
app = FastAPI(
    title="Real-World Email Service",
    description="An API to send templated emails for common business scenarios.",
    version="1.0.0",
)

# --- Base Models ---
class EmailRecipient(BaseModel):
    to: List[EmailStr] = Field(..., example=["customer@example.com"])

class TemplatePayload(EmailRecipient):
    # Use a flexible dictionary for template variables
    data: Dict[str, Any]

# --- Specific Payload Models for validation and OpenAPI documentation ---
class SubscriptionEndPayload(TemplatePayload):
    data: Dict[str, Any] = Field(..., example={
        "FirstName": "Alex",
        "ProductServiceName": "Pro Plan",
        "EndDate": "October 31, 2025"
    })

class OptInPayload(TemplatePayload):
    data: Dict[str, Any] = Field(..., example={"FirstName": "Casey"})

class NewsletterPayload(TemplatePayload):
    data: Dict[str, Any] = Field(..., example={
        "FirstName": "Jordan",
        "Month": "October",
        "Headline1": "Our Biggest Update Yet!",
        "TipOrInsight": "You can now sync your data across devices seamlessly.",
        "EventName": "Annual Tech Summit",
        "EventDate": "November 15, 2025",
        "OfferDetails": "Get 20% off on all annual plans this month."
    })

class ProductLaunchPayload(TemplatePayload):
    data: Dict[str, Any] = Field(..., example={
        "FirstName": "Sam",
        "ProductName": "SyncMaster 5000",
        "ProductBenefit": "automate your workflow like never before",
        "Feature1": "AI-Powered Suggestions",
        "Feature2": "One-Click Cloud Backup",
        "Feature3": "Real-time Collaboration"
    })


# --- API Endpoints ---

@app.post("/send/subscription-ending", status_code=status.HTTP_202_ACCEPTED, tags=["Templates"])
async def send_subscription_ending(payload: SubscriptionEndPayload, background_tasks: BackgroundTasks):
    """Sends a notification that a user's subscription is about to end."""
    payload.data['company_name'] = settings.company_name
    subject, html_content = templates.get_subscription_end_notification(payload.data)
    background_tasks.add_task(
        transport.send_email,
        to_emails=payload.to,
        subject=subject,
        html_body=html_content
    )
    return {"message": "Subscription ending notification has been queued."}


@app.post("/send/opt-in-confirmation", status_code=status.HTTP_202_ACCEPTED, tags=["Templates"])
async def send_opt_in_confirmation(payload: OptInPayload, background_tasks: BackgroundTasks):
    """Sends an email to confirm a user's subscription to a newsletter or service."""
    payload.data['company_name'] = settings.company_name
    subject, html_content = templates.get_opt_in_confirmation(payload.data)
    background_tasks.add_task(
        transport.send_email,
        to_emails=payload.to,
        subject=subject,
        html_body=html_content
    )
    return {"message": "Opt-in confirmation email has been queued."}


@app.post("/send/newsletter", status_code=status.HTTP_202_ACCEPTED, tags=["Templates"])
async def send_newsletter(payload: NewsletterPayload, background_tasks: BackgroundTasks):
    """Sends a monthly newsletter to a list of subscribers."""
    payload.data['company_name'] = settings.company_name
    subject, html_content = templates.get_newsletter_template(payload.data)
    background_tasks.add_task(
        transport.send_email,
        to_emails=payload.to,
        subject=subject,
        html_body=html_content
    )
    return {"message": "Newsletter has been queued."}


@app.post("/send/product-launch", status_code=status.HTTP_202_ACCEPTED, tags=["Templates"])
async def send_product_launch(payload: ProductLaunchPayload, background_tasks: BackgroundTasks):
    """Sends a new product launch announcement."""
    payload.data['company_name'] = settings.company_name
    subject, html_content = templates.get_product_launch_announcement(payload.data)
    background_tasks.add_task(
        transport.send_email,
        to_emails=payload.to,
        subject=subject,
        html_body=html_content
    )
    return {"message": "Product launch announcement has been queued."}


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health Check"])
def read_root():
    """A simple check endpoint to confirm the service is running."""
    return {"status": "ok", "service": "Real-World Email Service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
