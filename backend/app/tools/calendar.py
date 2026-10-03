from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain.tools import tool


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

TOKEN_FILE = BASE_DIR / "google_token.json"


def get_calendar_service():
    """Create and return an authenticated Google Calendar API service."""

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

    return build("calendar", "v3", credentials=creds)


@tool
def create_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    timezone: str = "Asia/Kolkata",
) -> str:
    """Create a Google Calendar event."""

    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": timezone,
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    return (
        f"Event created successfully.\n"
        f"Title: {created_event.get('summary', summary)}\n"
        f"Event ID: {created_event['id']}"
    )


@tool
def update_event(
    event_id: str,
    summary: str,
    start_datetime: str,
    end_datetime: str,
    timezone: str = "Asia/Kolkata",
) -> str:
    """Update an existing Google Calendar event."""

    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": timezone,
        },
    }

    updated_event = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event,
    ).execute()

    return (
        f"Event updated successfully.\n"
        f"Title: {updated_event.get('summary', summary)}\n"
        f"Event ID: {updated_event['id']}"
    )


@tool
def delete_event(event_id: str) -> str:
    """Delete a Google Calendar event."""

    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    return "Event deleted successfully."


@tool
def list_events(max_results: int = 10) -> str:
    """List upcoming Google Calendar events."""

    service = get_calendar_service()

    events_result = service.events().list(
        calendarId="primary",
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
        timeMin=datetime.now(timezone.utc).isoformat(),
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return "No upcoming events found."

    results = []

    for event in events:
        start = event.get("start", {}).get("dateTime")
        if not start:
            start = event.get("start", {}).get("date")

        results.append(
            f"Event ID: {event['id']}\n"
            f"Title: {event.get('summary', 'Untitled')}\n"
            f"Start: {start}"
        )

    return "\n\n".join(results)