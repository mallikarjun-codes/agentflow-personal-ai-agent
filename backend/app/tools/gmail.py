import base64
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain.tools import tool


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

TOKEN_FILE = BASE_DIR / "google_token.json"


def get_gmail_service():
    """Create and return an authenticated Gmail API service."""

    if not TOKEN_FILE.exists():
        raise RuntimeError(
            "Google authorization required. Visit /auth/google first."
        )

    creds = Credentials.from_authorized_user_file(
        str(TOKEN_FILE),
        SCOPES,
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        

    if not creds.valid:
        raise RuntimeError(
            "Google credentials are invalid. Visit /auth/google again."
        )

    return build("gmail", "v1", credentials=creds)


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email using the authenticated Gmail account."""

    service = get_gmail_service()

    message = EmailMessage()
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()

    return f"Email sent successfully. Message ID: {result['id']}"