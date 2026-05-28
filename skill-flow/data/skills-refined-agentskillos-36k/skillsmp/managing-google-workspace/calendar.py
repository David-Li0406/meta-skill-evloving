"""Google Calendar tools for listing, creating, and managing calendar events."""

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.calendar")

# Scopes required for Calendar operations
CALENDAR_READONLY_SCOPES = [SCOPES["calendar_readonly"]]
CALENDAR_FULL_SCOPES = [SCOPES["calendar"]]


@tool()
async def google_calendar_list() -> dict:
    """List all calendars accessible to the user.

    Returns a list of calendars with their IDs, names, descriptions,
    and access roles. Useful for finding the correct calendar ID
    before listing events or creating new ones.

    Returns:
        List of calendars with id, name, description, primary status, and access_role.
    """
    try:

        def _list():
            service = get_google_service("calendar", "v3", CALENDAR_READONLY_SCOPES)
            results = service.calendarList().list().execute()
            calendars = results.get("items", [])
            return {
                "calendars": [
                    {
                        "id": cal["id"],
                        "name": cal.get("summary", ""),
                        "description": cal.get("description", ""),
                        "primary": cal.get("primary", False),
                        "access_role": cal.get("accessRole", ""),
                    }
                    for cal in calendars
                ],
                "total": len(calendars),
            }

        logger.info("calendar_list")
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("calendar_list failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_calendar_events(
    calendar_id: str = "primary",
    days_ahead: int = 7,
    max_results: int = 50,
) -> dict:
    """List upcoming events from a calendar.

    Retrieves events starting from now up to the specified number of days ahead.
    Events are returned in chronological order by start time.

    Args:
        calendar_id: Calendar ID to list events from (default: "primary").
        days_ahead: Number of days to look ahead (default: 7).
        max_results: Maximum number of events to return (default: 50).

    Returns:
        List of events with id, title, description, start/end times, location, and status.
    """
    try:

        def _list_events():
            service = get_google_service("calendar", "v3", CALENDAR_READONLY_SCOPES)

            now = datetime.now(UTC)
            time_min = now.isoformat()
            time_max = (now + timedelta(days=days_ahead)).isoformat()

            results = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            items = results.get("items", [])
            return {
                "events": [
                    {
                        "id": event["id"],
                        "title": event.get("summary", "(no title)"),
                        "description": event.get("description", ""),
                        "start": event.get("start", {}).get(
                            "dateTime", event.get("start", {}).get("date", "")
                        ),
                        "end": event.get("end", {}).get(
                            "dateTime", event.get("end", {}).get("date", "")
                        ),
                        "location": event.get("location", ""),
                        "status": event.get("status", ""),
                        "html_link": event.get("htmlLink", ""),
                    }
                    for event in items
                ],
                "total": len(items),
            }

        logger.info(
            "calendar_events calendar_id=%s days_ahead=%s", calendar_id, days_ahead
        )
        result = await asyncio.to_thread(_list_events)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("calendar_events failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_calendar_create_event(
    title: str,
    start_time: str,
    end_time: str,
    calendar_id: str = "primary",
    description: str = "",
    location: str = "",
    attendees: str = "",
) -> dict:
    """Create a new calendar event.

    Creates an event with the specified details. Times should be in ISO 8601 format.

    Args:
        title: Event title/summary.
        start_time: Start time in ISO 8601 format (e.g., "2024-01-15T09:00:00Z").
        end_time: End time in ISO 8601 format.
        calendar_id: Calendar ID to create event in (default: "primary").
        description: Optional event description.
        location: Optional event location.
        attendees: Optional comma-separated list of attendee email addresses.

    Returns:
        Created event details including id, title, times, and html_link.
    """
    try:

        def _create():
            service = get_google_service("calendar", "v3", CALENDAR_FULL_SCOPES)

            event_body = {
                "summary": title,
                "description": description,
                "location": location,
                "start": {"dateTime": start_time, "timeZone": "UTC"},
                "end": {"dateTime": end_time, "timeZone": "UTC"},
            }

            if attendees:
                event_body["attendees"] = [
                    {"email": email.strip()} for email in attendees.split(",")
                ]

            event = (
                service.events()
                .insert(calendarId=calendar_id, body=event_body)
                .execute()
            )

            return {
                "id": event["id"],
                "title": event.get("summary"),
                "start": event.get("start", {}).get("dateTime"),
                "end": event.get("end", {}).get("dateTime"),
                "html_link": event.get("htmlLink"),
            }

        logger.info("calendar_create_event title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("calendar_create_event failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_calendar_delete_event(
    event_id: str,
    calendar_id: str = "primary",
) -> dict:
    """Delete a calendar event.

    Permanently removes an event from the specified calendar.

    Args:
        event_id: ID of the event to delete.
        calendar_id: Calendar ID containing the event (default: "primary").

    Returns:
        Confirmation with the deleted event ID.
    """
    try:

        def _delete():
            service = get_google_service("calendar", "v3", CALENDAR_FULL_SCOPES)
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            return {"deleted_event_id": event_id}

        logger.info("calendar_delete_event event_id=%s", event_id)
        result = await asyncio.to_thread(_delete)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("calendar_delete_event failed")
        return {"success": False, "error": str(e)}
