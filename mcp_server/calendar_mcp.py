import datetime
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from scalekit_backend.db.user_service import ScalekitUserService
from mcp.server.fastmcp import FastMCP

load_dotenv()

user_service = ScalekitUserService()

GOOGLE_CALENDAR_SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_encrypted_google_refresh_token_from_db(scalekit_user_id):
    user_data = user_service.get(scalekit_user_id)
    if user_data:
        return user_data.refresh_token, GOOGLE_CALENDAR_SCOPES
    raise ValueError(f"User {scalekit_user_id} not found")

def get_google_calendar_service(scalekit_user_id):
    refresh_token, granted_scopes = get_encrypted_google_refresh_token_from_db(scalekit_user_id)

    if not refresh_token:
        print(f"Error: No Google refresh token found for user {scalekit_user_id}. User needs to authorize via Scalekit.")
        return None

    TOKEN_URI = 'https://oauth2.googleapis.com/token'

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=os.environ.get('GOOGLE_OAUTH_CLIENT_ID'), # Your *Google Cloud Console* Client ID
        client_secret=os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'), # Your *Google Cloud Console* Client Secret
        scopes=granted_scopes
    )

    try:
        creds.refresh(Request())

        service = build('calendar', 'v3', credentials=creds)
        return service

    except Exception as e:
        print(f"Failed to refresh Google access token for user {scalekit_user_id}: {e}")
        return None

def get_todays_events_for_user(scalekit_user_id):
    service = get_google_calendar_service(scalekit_user_id)
    if not service:
        return []

    now = datetime.datetime.now()

    today_start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=datetime.timezone.utc).isoformat()

    tomorrow_start = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)
    tomorrow_start_iso = tomorrow_start.isoformat()

    print(f'Getting today\'s events for user {scalekit_user_id}...')
    try:
        events_result = service.events().list(calendarId='primary',
                                              timeMin=today_start,
                                              timeMax=tomorrow_start_iso,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except Exception as e:
        print(f"Error fetching calendar events for user {scalekit_user_id}: {e}")
        return []


mcp = FastMCP(
    "Google Calendar MCP",
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8000))
)

@mcp.tool(
    name="get_todays_events_for_user",
    description="Get today's Google Calendar events for a user by user_id. Returns a list of event dicts.",
)
def get_todays_events_for_user_mcp(scalekit_user_id: str):
    return get_todays_events_for_user(scalekit_user_id)

if __name__ == "__main__":
    mcp.run(transport="streamable-http") # type: ignore