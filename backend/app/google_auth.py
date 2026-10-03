import os
import secrets
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow

router = APIRouter()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.events",
]

BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = BASE_DIR / "web_credentials.json"
TOKEN_FILE = BASE_DIR / "google_token.json"

REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://localhost:8000/auth/google/callback",
)

# Store the original OAuth flow so the same PKCE verifier
# is available when Google redirects back to us.
pending_flows = {}


@router.get("/auth/google")
def google_auth():
    state = secrets.token_urlsafe(32)

    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        scopes=SCOPES,
        autogenerate_code_verifier=True,
    )

    flow.redirect_uri = REDIRECT_URI

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
        state=state,
    )

    pending_flows[state] = flow

    return RedirectResponse(authorization_url)


@router.get("/auth/google/callback")
def google_callback(code: str, state: str):
    flow = pending_flows.pop(state, None)

    if flow is None:
        raise HTTPException(
            status_code=400,
            detail="OAuth session expired or invalid state",
        )

    flow.fetch_token(code=code)

    credentials = flow.credentials

    TOKEN_FILE.write_text(credentials.to_json())

    return HTMLResponse(
        """
        <h2>Google authorization successful ✅</h2>
        <p>You can close this window.</p>
        """
    )