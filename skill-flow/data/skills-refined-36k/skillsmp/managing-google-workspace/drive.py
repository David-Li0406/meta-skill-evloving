"""Google Drive tools for listing, searching, and reading files."""

import asyncio
import io
import logging

from googleapiclient.http import MediaIoBaseDownload

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.drive")

# Scopes required for Drive operations
DRIVE_READONLY_SCOPES = [SCOPES["drive_readonly"]]


@tool()
async def google_drive_list(
    folder_id: str = "root",
    max_results: int = 50,
    file_type: str = "",
) -> dict:
    """List files in a Google Drive folder.

    Returns files in the specified folder, optionally filtered by type.

    Args:
        folder_id: Folder ID to list (default: "root" for root folder).
        max_results: Maximum number of files to return (default: 50).
        file_type: Optional MIME type filter (e.g., "image", "document").

    Returns:
        List of files with id, name, mime_type, size, modified date, and web_link.
    """
    try:

        def _list():
            service = get_google_service("drive", "v3", DRIVE_READONLY_SCOPES)

            query = f"'{folder_id}' in parents and trashed = false"
            if file_type:
                query += f" and mimeType contains '{file_type}'"

            results = (
                service.files()
                .list(
                    q=query,
                    pageSize=max_results,
                    fields="files(id, name, mimeType, size, modifiedTime, webViewLink)",
                    orderBy="modifiedTime desc",
                )
                .execute()
            )

            files = results.get("files", [])
            return {
                "files": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "mime_type": f.get("mimeType", ""),
                        "size": f.get("size", ""),
                        "modified": f.get("modifiedTime", ""),
                        "web_link": f.get("webViewLink", ""),
                    }
                    for f in files
                ],
                "total": len(files),
            }

        logger.info("drive_list folder_id=%s max_results=%s", folder_id, max_results)
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("drive_list failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_drive_search(query: str, max_results: int = 50) -> dict:
    """Search for files in Google Drive.

    Performs a full-text search across all accessible files.

    Args:
        query: Search query to match against file contents and names.
        max_results: Maximum number of files to return (default: 50).

    Returns:
        List of matching files with metadata including owner information.
    """
    try:

        def _search():
            service = get_google_service("drive", "v3", DRIVE_READONLY_SCOPES)

            drive_query = f"fullText contains '{query}' and trashed = false"

            results = (
                service.files()
                .list(
                    q=drive_query,
                    pageSize=max_results,
                    fields="files(id, name, mimeType, size, modifiedTime, webViewLink, owners)",
                    orderBy="modifiedTime desc",
                )
                .execute()
            )

            files = results.get("files", [])
            return {
                "files": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "mime_type": f.get("mimeType", ""),
                        "size": f.get("size", ""),
                        "modified": f.get("modifiedTime", ""),
                        "web_link": f.get("webViewLink", ""),
                        "owner": (
                            f.get("owners", [{}])[0].get("emailAddress", "")
                            if f.get("owners")
                            else ""
                        ),
                    }
                    for f in files
                ],
                "total": len(files),
                "query": query,
            }

        logger.info("drive_search query=%s", query)
        result = await asyncio.to_thread(_search)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("drive_search failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_drive_get_file(file_id: str) -> dict:
    """Get detailed metadata for a file.

    Retrieves comprehensive information about a specific file.

    Args:
        file_id: ID of the file to get metadata for.

    Returns:
        Detailed file metadata including owners, parents, and download link.
    """
    try:

        def _get():
            service = get_google_service("drive", "v3", DRIVE_READONLY_SCOPES)

            file = (
                service.files()
                .get(
                    fileId=file_id,
                    fields="id, name, mimeType, size, createdTime, modifiedTime, "
                    "webViewLink, webContentLink, owners, parents, description",
                )
                .execute()
            )

            return {
                "id": file["id"],
                "name": file["name"],
                "mime_type": file.get("mimeType", ""),
                "size": file.get("size", ""),
                "created": file.get("createdTime", ""),
                "modified": file.get("modifiedTime", ""),
                "description": file.get("description", ""),
                "web_link": file.get("webViewLink", ""),
                "download_link": file.get("webContentLink", ""),
                "owners": [
                    {"name": o.get("displayName"), "email": o.get("emailAddress")}
                    for o in file.get("owners", [])
                ],
                "parent_folders": file.get("parents", []),
            }

        logger.info("drive_get_file file_id=%s", file_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("drive_get_file failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_drive_read_text_file(file_id: str) -> dict:
    """Read the content of a text-based file from Google Drive.

    Supports Google Docs (exported as plain text), Google Sheets (exported as CSV),
    and regular text files.

    Args:
        file_id: ID of the file to read.

    Returns:
        File content with name, mime_type, content text, and length.
    """
    try:

        def _read():
            service = get_google_service("drive", "v3", DRIVE_READONLY_SCOPES)

            file = (
                service.files().get(fileId=file_id, fields="name, mimeType").execute()
            )

            mime_type = file.get("mimeType", "")
            content = ""

            # Handle Google Docs - export as plain text
            if mime_type == "application/vnd.google-apps.document":
                request = service.files().export_media(
                    fileId=file_id, mimeType="text/plain"
                )
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                content = fh.getvalue().decode("utf-8")

            # Handle Google Sheets - export as CSV
            elif mime_type == "application/vnd.google-apps.spreadsheet":
                request = service.files().export_media(
                    fileId=file_id, mimeType="text/csv"
                )
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                content = fh.getvalue().decode("utf-8")

            # Handle regular files
            else:
                request = service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                try:
                    content = fh.getvalue().decode("utf-8")
                except UnicodeDecodeError:
                    return {
                        "error": "File is not a text file",
                        "name": file["name"],
                        "mime_type": mime_type,
                    }

            return {
                "name": file["name"],
                "mime_type": mime_type,
                "content": content,
                "length": len(content),
            }

        logger.info("drive_read_text_file file_id=%s", file_id)
        result = await asyncio.to_thread(_read)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("drive_read_text_file failed")
        return {"success": False, "error": str(e)}
