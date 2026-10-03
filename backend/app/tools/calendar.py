import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.tools import tool

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def get_calendar_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

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
        f"Event created successfully. "
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
        f"Event updated successfully. "
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