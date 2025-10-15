# Real-World Email Service with FastAPI and SendGrid

This project provides a robust, template-driven email API built with Python, FastAPI, and SendGrid. It is designed to handle common, real-world email scenarios such as subscription confirmations, newsletters, and product announcements. The service uses background tasks for non-blocking email sending and Pydantic for strong data validation.

---

## Key Features

- **Template-Driven:** Easily send beautifully formatted HTML emails for different business cases.
- **Asynchronous Sending:** Uses FastAPI's BackgroundTasks to queue emails, ensuring immediate API responses without waiting for the email to be sent.
- **Dynamic Content:** Leverages Jinja2 to populate templates with dynamic data for personalized emails.
- **Type-Safe & Validated:** Uses Pydantic models for clear, validated API request bodies, which also auto-generates interactive documentation.
- **Configuration Management:** Securely manages credentials and settings using Pydantic Settings and a `.env` file.
- **Production-Ready Transport:** Integrated with SendGrid for reliable and scalable email delivery.

---

## Project Structure

```
email-service/
├─ main.py                # FastAPI app with all API endpoints
├─ transport.py           # Handles sending emails via SendGrid
├─ templates.py           # Contains all email templates and rendering logic
├─ config.py              # Pydantic settings management
├─ requirements.txt       # Python dependencies
├─ .env                   # Local environment variables (ignored by git)
└─ .env.example           # Example environment file
```

---

## Prerequisites

- Python 3.9+
- A SendGrid account with a verified sender email and an API Key.

---

## Setup and Installation

### 1. Clone the Repository (Optional)

```bash
git clone <your-repository-url>
cd email-service
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root. You can copy the example file to get started:

```bash
cp .env.example .env
```

Now, open the `.env` file and fill in your actual details.

#### Example `.env` Structure

```ini
# ---------------------
# GENERAL SETTINGS
# ---------------------
COMPANY_NAME="My Awesome SaaS"

# ---------------------
# SENDGRID CREDENTIALS
# ---------------------
SENGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SENDGRID_FROM_EMAIL="notifications@myawesomesaas.com"
```

---

## Running the Service

Once your `.env` file is configured, you can start the API server using Uvicorn. The `--reload` flag is great for development and will automatically restart the server when you make code changes.

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Making it Production Ready

### 1. Authenticate Your Domain (Crucial)

- Log in to SendGrid: Navigate to **Settings > Sender Authentication**.
- Authenticate a Domain: Follow the on-screen instructions. SendGrid will provide several DNS records (usually 3-5 CNAME records).
- Add DNS Records: Add these records to your domain's DNS provider (e.g., GoDaddy, Cloudflare, Namecheap).
- Verify: Once the DNS records are added, click "Verify" in SendGrid. It may take a few minutes up to 48 hours to propagate.
- After authentication, update your `.env` file to use an email from that domain (e.g., `SENDGRID_FROM_EMAIL="support@your-authenticated-domain.com"`).

### 2. Secure API Key Management

- Your `.env` file should **never** be committed to version control (ensure it's in your `.gitignore`).
- In production, use your hosting provider's system for managing secrets:
  - **Heroku:** Config Vars
  - **AWS:** Secrets Manager or Parameter Store
  - **Google Cloud:** Secret Manager
  - **Docker/Kubernetes:** Environment variables or secrets management tools

### 3. Use a Production-Grade Server

While Uvicorn is a great server, for production, you should run it with a process manager like Gunicorn.

**Example Production Command:**

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

This command starts 4 worker processes, allowing your API to handle concurrent requests efficiently.

### 4. Implement Logging and Error Monitoring

- **Logging:** Use Python's built-in `logging` module to write errors to a file or a log aggregator service (like Datadog, Logstash, or Sentry).
- **Error Monitoring:** Services like Sentry or Rollbar can automatically capture and alert you about unhandled exceptions.

---

## API Usage and Endpoints

### Interactive API Docs (Swagger UI)

Open your browser and navigate to:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This interface allows you to test each endpoint directly from your browser with auto-generated examples.

---

### 1. Send Subscription Ending Notification

- **Endpoint:** `POST /send/subscription-ending`
- **Description:** Sends a notification that a user's subscription is about to expire.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/send/subscription-ending" \
-H "Content-Type: application/json" \
-d '{
  "to": ["customer@example.com"],
  "data": {
    "FirstName": "Alex",
    "ProductServiceName": "Pro Plan",
    "EndDate": "October 31, 2025"
  }
}'
```

---

### 2. Send Opt-In Confirmation

- **Endpoint:** `POST /send/opt-in-confirmation`
- **Description:** Sends an email to a new user to confirm their subscription.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/send/opt-in-confirmation" \
-H "Content-Type: application/json" \
-d '{
  "to": ["new.subscriber@example.com"],
  "data": {
    "FirstName": "Casey"
  }
}'
```

---

### 3. Send Newsletter

- **Endpoint:** `POST /send/newsletter`
- **Description:** Sends a templated newsletter to a list of recipients.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/send/newsletter" \
-H "Content-Type: application/json" \
-d '{
  "to": ["reader@example.com"],
  "data": {
    "FirstName": "Jordan",
    "Month": "October",
    "Headline1": "Our Biggest Update Yet!",
    "TipOrInsight": "You can now sync your data across devices seamlessly.",
    "EventName": "Annual Tech Summit",
    "EventDate": "November 15, 2025",
    "OfferDetails": "Get 20% off on all annual plans this month."
  }
}'
```

---

### 4. Send New Product Launch Announcement

- **Endpoint:** `POST /send/product-launch`
- **Description:** Announce a new product to your audience.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/send/product-launch" \
-H "Content-Type: application/json" \
-d '{
  "to": ["loyal.customer@example.com"],
  "data": {
    "FirstName": "Sam",
    "ProductName": "SyncMaster 5000",
    "ProductBenefit": "automate your workflow like never before",
    "Feature1": "AI-Powered Suggestions",
    "Feature2": "One-Click Cloud Backup",
    "Feature3": "Real-time Collaboration"
  }
}'
```