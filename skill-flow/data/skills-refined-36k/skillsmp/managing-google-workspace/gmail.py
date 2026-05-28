"""Google Gmail tools for searching, reading, and sending emails."""

import asyncio
import base64
import logging
from email.mime.text import MIMEText

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.gmail")

# Scopes required for Gmail operations
GMAIL_READONLY_SCOPES = [SCOPES["gmail_readonly"]]
GMAIL_SEND_SCOPES = [SCOPES["gmail_send"]]


@tool()
async def google_gmail_search(query: str = "", max_results: int = 10) -> dict:
    """Search Gmail messages.

    Searches for emails matching the query using Gmail's search syntax.
    Examples: "from:john@example.com", "subject:meeting", "is:unread".

    Args:
        query: Gmail search query (default: "" returns recent emails).
        max_results: Maximum number of messages to return (default: 10, max: 100).

    Returns:
        List of messages with id, thread_id, subject, from, to, date, and snippet.
    """
    try:
        max_results = min(max_results, 100)

        def _search():
            service = get_google_service("gmail", "v1", GMAIL_READONLY_SCOPES)
            results = (
                service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])
            if not messages:
                return {"messages": [], "total": 0}

            detailed = []
            for msg in messages:
                msg_data = (
                    service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="metadata")
                    .execute()
                )
                headers = {
                    h["name"].lower(): h["value"]
                    for h in msg_data.get("payload", {}).get("headers", [])
                }
                detailed.append(
                    {
                        "id": msg["id"],
                        "thread_id": msg_data.get("threadId"),
                        "subject": headers.get("subject", "(no subject)"),
                        "from": headers.get("from", ""),
                        "to": headers.get("to", ""),
                        "date": headers.get("date", ""),
                        "snippet": msg_data.get("snippet", ""),
                    }
                )

            return {"messages": detailed, "total": len(detailed)}

        logger.info("gmail_search query=%s max_results=%s", query, max_results)
        result = await asyncio.to_thread(_search)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("gmail_search failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_gmail_read(message_id: str) -> dict:
    """Read the full content of a Gmail message.

    Retrieves the complete email including headers, body text, and labels.

    Args:
        message_id: ID of the message to read.

    Returns:
        Full message with id, thread_id, subject, from, to, cc, date, body, and labels.
    """
    try:

        def _read():
            service = get_google_service("gmail", "v1", GMAIL_READONLY_SCOPES)
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )

            headers = {
                h["name"].lower(): h["value"]
                for h in msg.get("payload", {}).get("headers", [])
            }

            body = ""
            payload = msg.get("payload", {})

            if "body" in payload and payload["body"].get("data"):
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode()
            elif "parts" in payload:
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain":
                        if part.get("body", {}).get("data"):
                            body = base64.urlsafe_b64decode(
                                part["body"]["data"]
                            ).decode()
                            break
                    elif part.get("mimeType") == "text/html" and not body:
                        if part.get("body", {}).get("data"):
                            body = base64.urlsafe_b64decode(
                                part["body"]["data"]
                            ).decode()

            return {
                "id": msg["id"],
                "thread_id": msg.get("threadId"),
                "subject": headers.get("subject", "(no subject)"),
                "from": headers.get("from", ""),
                "to": headers.get("to", ""),
                "cc": headers.get("cc", ""),
                "date": headers.get("date", ""),
                "body": body,
                "labels": msg.get("labelIds", []),
            }

        logger.info("gmail_read message_id=%s", message_id)
        result = await asyncio.to_thread(_read)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("gmail_read failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_gmail_send(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
) -> dict:
    """Send an email via Gmail.

    Composes and sends an email to the specified recipients.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Plain text email body.
        cc: Optional CC recipients (comma-separated).
        bcc: Optional BCC recipients (comma-separated).

    Returns:
        Sent message details with message_id and thread_id.
    """
    try:

        def _send():
            service = get_google_service("gmail", "v1", GMAIL_SEND_SCOPES)

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            result = (
                service.users()
                .messages()
                .send(userId="me", body={"raw": raw})
                .execute()
            )

            return {
                "message_id": result.get("id"),
                "thread_id": result.get("threadId"),
            }

        logger.info("gmail_send to=%s subject=%s", to, subject)
        result = await asyncio.to_thread(_send)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("gmail_send failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_gmail_labels() -> dict:
    """List all Gmail labels.

    Returns all labels in the user's mailbox including system labels
    (INBOX, SENT, etc.) and user-created labels.

    Returns:
        List of labels with id and name.
    """
    try:

        def _list_labels():
            service = get_google_service("gmail", "v1", GMAIL_READONLY_SCOPES)
            results = service.users().labels().list(userId="me").execute()
            items = results.get("labels", [])
            return {
                "labels": [
                    {"id": label["id"], "name": label["name"]} for label in items
                ],
                "total": len(items),
            }

        logger.info("gmail_labels")
        result = await asyncio.to_thread(_list_labels)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("gmail_labels failed")
        return {"success": False, "error": str(e)}
