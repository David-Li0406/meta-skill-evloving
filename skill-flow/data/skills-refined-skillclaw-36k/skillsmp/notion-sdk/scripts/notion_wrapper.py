# /// script
# requires-python = ">=3.11"
# dependencies = ["notion-client>=2.6.0"]
# ///
"""Notion API client wrapper with validation and retry logic.

This module provides:
- Client initialization with token
- Token validation against Notion API
- Retry wrapper with rate limit and error handling
"""

import time
from notion_client import Client, APIResponseError, APIErrorCode


def get_client(token: str) -> Client:
    """Initialize authenticated Notion client.

    Args:
        token: Notion integration token (starts with ntn_ or secret_)

    Returns:
        Authenticated Client instance
    """
    return Client(auth=token)


def validate_token(token: str) -> tuple[bool, str]:
    """Test token validity by calling /users/me endpoint.

    Args:
        token: Notion integration token to validate

    Returns:
        Tuple of (success: bool, message: str)
    """
    # Format validation
    if not token.startswith(("ntn_", "secret_")):
        return (False, "Token must start with 'ntn_' or 'secret_'")

    try:
        client = get_client(token)
        user = client.users.me()
        bot_name = user.get("name", "Unknown")
        return (True, f"Authenticated as: {bot_name}")
    except APIResponseError as e:
        if e.code == APIErrorCode.Unauthorized:
            return (False, "Token invalid or expired")
        return (False, f"API error: {e.message}")
    except Exception as e:
        return (False, f"Connection failed: {str(e)}")


def api_call_with_retry(func, *args, max_retries: int = 3, **kwargs):
    """Execute API call with rate limit handling and exponential backoff.

    Handles:
    - 429 Rate Limited: Waits per Retry-After header
    - 500 Server Error: Exponential backoff retry

    Args:
        func: API method to call (e.g., client.pages.create)
        *args: Positional arguments for func
        max_retries: Maximum retry attempts (default: 3)
        **kwargs: Keyword arguments for func

    Returns:
        API response from func

    Raises:
        APIResponseError: On non-retryable errors
        RuntimeError: When max retries exceeded
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except APIResponseError as e:
            if e.code == APIErrorCode.RateLimited:
                # Respect Retry-After header from Notion
                retry_after = 1
                if hasattr(e, "additional_data") and e.additional_data:
                    retry_after = int(e.additional_data.get("retry_after", 1))
                print(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
            elif e.code in [APIErrorCode.InternalServerError]:
                if attempt < max_retries - 1:
                    wait = 2**attempt  # Exponential backoff: 1, 2, 4 seconds
                    print(f"Server error. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
            else:
                # Non-retryable error (auth, validation, not found)
                raise
    raise RuntimeError(f"Max retries ({max_retries}) exceeded")


if __name__ == "__main__":
    import os
    import sys

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("Error: NOTION_TOKEN environment variable not set")
        sys.exit(1)

    success, message = validate_token(token)
    print(message)
    sys.exit(0 if success else 1)
