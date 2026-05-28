import json
import logging
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger("humcp.google.auth")

TOKEN_PATH = Path.home() / ".humcp" / "google_token.json"
CLIENT_SECRET_PATH = Path.home() / ".humcp" / "client_secret.json"

SCOPES = {
    # Gmail
    "gmail_readonly": "https://www.googleapis.com/auth/gmail.readonly",
    "gmail_send": "https://www.googleapis.com/auth/gmail.send",
    "gmail_modify": "https://www.googleapis.com/auth/gmail.modify",
    # Calendar
    "calendar": "https://www.googleapis.com/auth/calendar",
    "calendar_readonly": "https://www.googleapis.com/auth/calendar.readonly",
    # Drive
    "drive": "https://www.googleapis.com/auth/drive",
    "drive_readonly": "https://www.googleapis.com/auth/drive.readonly",
    "drive_file": "https://www.googleapis.com/auth/drive.file",
    # Tasks
    "tasks": "https://www.googleapis.com/auth/tasks",
    "tasks_readonly": "https://www.googleapis.com/auth/tasks.readonly",
    # Docs
    "docs": "https://www.googleapis.com/auth/documents",
    "docs_readonly": "https://www.googleapis.com/auth/documents.readonly",
    # Sheets
    "sheets": "https://www.googleapis.com/auth/spreadsheets",
    "sheets_readonly": "https://www.googleapis.com/auth/spreadsheets.readonly",
    # Slides
    "slides": "https://www.googleapis.com/auth/presentations",
    "slides_readonly": "https://www.googleapis.com/auth/presentations.readonly",
    # Forms
    "forms": "https://www.googleapis.com/auth/forms.body",
    "forms_readonly": "https://www.googleapis.com/auth/forms.body.readonly",
    "forms_responses": "https://www.googleapis.com/auth/forms.responses.readonly",
    # Chat
    "chat_spaces": "https://www.googleapis.com/auth/chat.spaces.readonly",
    "chat_messages": "https://www.googleapis.com/auth/chat.messages",
    "chat_messages_readonly": "https://www.googleapis.com/auth/chat.messages.readonly",
}


def _ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_client_config() -> dict | None:
    """Load OAuth client configuration from environment or file."""
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

    if client_id and client_secret:
        logger.debug("Using OAuth credentials from environment variables")
        return {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        }

    if CLIENT_SECRET_PATH.exists():
        logger.debug("Using OAuth credentials from %s", CLIENT_SECRET_PATH)
        with open(CLIENT_SECRET_PATH) as f:
            return json.load(f)

    return None


def get_credentials(scopes: list[str]) -> Credentials | None:
    """Get valid credentials, refreshing or re-authenticating as needed."""
    _ensure_config_dir()
    creds = None

    # Load existing token if available
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)
            logger.debug("Loaded existing credentials from token file")
        except Exception as e:
            logger.warning("Failed to load existing token: %s", e)
            creds = None

    # Refresh or get new credentials
    if creds and creds.expired and creds.refresh_token:
        try:
            logger.info("Refreshing expired credentials")
            creds.refresh(Request())
            _save_credentials(creds)
        except Exception as e:
            logger.warning("Failed to refresh token: %s", e)
            creds = None

    if not creds or not creds.valid:
        creds = _run_auth_flow(scopes)

    return creds


def _run_auth_flow(scopes: list[str]) -> Credentials | None:
    """Run the OAuth authorization flow."""
    client_config = load_client_config()
    if not client_config:
        logger.error(
            "Google OAuth not configured. Set GOOGLE_OAUTH_CLIENT_ID and "
            "GOOGLE_OAUTH_CLIENT_SECRET environment variables, or create "
            "%s",
            CLIENT_SECRET_PATH,
        )
        return None

    try:
        # Allow http for localhost during development
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        flow = InstalledAppFlow.from_client_config(client_config, scopes)
        logger.info("Opening browser for Google authentication...")
        creds = flow.run_local_server(port=0)

        _save_credentials(creds)
        logger.info("Authentication successful")
        return creds

    except Exception as e:
        logger.error("OAuth flow failed: %s", e)
        return None


def _save_credentials(creds: Credentials) -> None:
    """Save credentials to token file."""
    _ensure_config_dir()
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
    logger.debug("Credentials saved to %s", TOKEN_PATH)


def get_google_service(service_name: str, version: str, scopes: list[str]):
    """Build an authenticated Google API service client."""
    creds = get_credentials(scopes)
    if not creds:
        raise ValueError(
            "Google authentication failed. Please configure OAuth credentials:\n"
            "1. Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET env vars\n"
            "2. Or create ~/.humcp/client_secret.json with OAuth credentials"
        )

    return build(service_name, version, credentials=creds)


def check_auth_status() -> dict:
    """Check current authentication status."""
    config = load_client_config()
    has_config = config is not None
    has_token = TOKEN_PATH.exists()

    status = {
        "configured": has_config,
        "authenticated": False,
        "token_path": str(TOKEN_PATH),
        "config_source": None,
    }

    if has_config:
        if os.getenv("GOOGLE_OAUTH_CLIENT_ID"):
            status["config_source"] = "environment"
        else:
            status["config_source"] = str(CLIENT_SECRET_PATH)

    if has_token:
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
            status["authenticated"] = creds.valid or creds.refresh_token is not None
            if creds.expired:
                status["token_status"] = "expired (will refresh)"
            elif creds.valid:
                status["token_status"] = "valid"
        except Exception:
            status["token_status"] = "invalid"

    return status
