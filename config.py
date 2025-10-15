# config.py (Corrected and Final Version)

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# --- THIS IS THE CRUCIAL FIX ---
# Explicitly load the .env file at the top of this module.
# This ensures that os.environ has the variables before Pydantic initializes.
load_dotenv()
# -----------------------------

class Settings(BaseSettings):
    """
    Loads and validates application settings from environment variables.
    """
    model_config = SettingsConfigDict(
        # We no longer need env_file here since we are pre-loading it,
        # but it doesn't hurt to keep it for clarity.
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )

    # --- General Settings ---
    company_name: str = os.getenv("COMPANY_NAME", "Your Company")

    # --- SendGrid Settings (for production/real emails) ---
    # These will now be correctly loaded from your .env file
    sendgrid_api_key: str = os. getenv("SENGRID_API_KEY", "DEFAULT_KEY_IF_NOT_SET")
    sendgrid_from_email: str = os.getenv("SENDGRID_FROM_EMAIL")


# Create a single, importable instance of the settings
settings = Settings()

# --- Optional: Add a print statement for final verification ---
# This will run once when the server starts.
print("--- Config Loaded ---")
print(f"Company Name: {settings.company_name}")
print(f"SendGrid API Key Loaded: {'Yes' if 'SG.' in settings.sendgrid_api_key else 'No, using default!'}")
print(f"SendGrid From Email: {settings.sendgrid_from_email}")
print("---------------------")