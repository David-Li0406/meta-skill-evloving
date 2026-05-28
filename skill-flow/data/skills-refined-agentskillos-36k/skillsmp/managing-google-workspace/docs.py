"""Google Docs tools for searching, reading, creating, and editing documents."""

import asyncio
import logging

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.docs")

DOCS_READONLY_SCOPES = [SCOPES["docs_readonly"], SCOPES["drive_readonly"]]
DOCS_FULL_SCOPES = [SCOPES["docs"], SCOPES["drive"]]


@tool()
async def google_docs_search(query: str, max_results: int = 25) -> dict:
    """Search for Google Docs by name.

    Searches for documents whose names contain the query string.

    Args:
        query: Search string to match against document names.
        max_results: Maximum number of documents to return (default: 25).

    Returns:
        List of matching documents with id, name, modified date, and web_link.
    """
    try:

        def _search():
            service = get_google_service("drive", "v3", DOCS_READONLY_SCOPES)
            drive_query = (
                f"name contains '{query}' and "
                "mimeType='application/vnd.google-apps.document' and "
                "trashed=false"
            )
            results = (
                service.files()
                .list(
                    q=drive_query,
                    pageSize=max_results,
                    fields="files(id, name, modifiedTime, webViewLink)",
                )
                .execute()
            )
            files = results.get("files", [])
            return {
                "documents": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "modified": f.get("modifiedTime", ""),
                        "web_link": f.get("webViewLink", ""),
                    }
                    for f in files
                ],
                "total": len(files),
            }

        logger.info("docs_search query=%s", query)
        result = await asyncio.to_thread(_search)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_search failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_docs_get_content(document_id: str) -> dict:
    """Get the content of a Google Doc.

    Extracts all text content from a document.

    Args:
        document_id: ID of the document to read.

    Returns:
        Document content with id, title, full text content, and revision_id.
    """
    try:

        def _get():
            service = get_google_service("docs", "v1", DOCS_READONLY_SCOPES)
            doc = service.documents().get(documentId=document_id).execute()

            # Extract text content
            content = []
            for element in doc.get("body", {}).get("content", []):
                if "paragraph" in element:
                    for para_element in element["paragraph"].get("elements", []):
                        if "textRun" in para_element:
                            content.append(para_element["textRun"].get("content", ""))

            return {
                "id": doc["documentId"],
                "title": doc.get("title", ""),
                "content": "".join(content),
                "revision_id": doc.get("revisionId", ""),
            }

        logger.info("docs_get_content doc_id=%s", document_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_get_content failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_docs_create(title: str, content: str = "") -> dict:
    """Create a new Google Doc.

    Creates an empty document with the specified title, optionally with initial content.

    Args:
        title: Title for the new document.
        content: Optional initial text content.

    Returns:
        Created document details with id, title, and web_link.
    """
    try:

        def _create():
            service = get_google_service("docs", "v1", DOCS_FULL_SCOPES)

            # Create empty document
            doc = service.documents().create(body={"title": title}).execute()
            doc_id = doc["documentId"]

            # Add initial content if provided
            if content:
                requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
                service.documents().batchUpdate(
                    documentId=doc_id, body={"requests": requests}
                ).execute()

            return {
                "id": doc_id,
                "title": doc.get("title", ""),
                "web_link": f"https://docs.google.com/document/d/{doc_id}/edit",
            }

        logger.info("docs_create title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_create failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_docs_append_text(document_id: str, text: str) -> dict:
    """Append text to the end of a Google Doc.

    Adds text content at the end of the document.

    Args:
        document_id: ID of the document to append to.
        text: Text to append.

    Returns:
        Confirmation with updated status and document_id.
    """
    try:

        def _append():
            service = get_google_service("docs", "v1", DOCS_FULL_SCOPES)

            # Get current document to find end index
            doc = service.documents().get(documentId=document_id).execute()
            end_index = doc["body"]["content"][-1]["endIndex"] - 1

            requests = [
                {"insertText": {"location": {"index": end_index}, "text": text}}
            ]
            service.documents().batchUpdate(
                documentId=document_id, body={"requests": requests}
            ).execute()

            return {"updated": True, "document_id": document_id}

        logger.info("docs_append_text doc_id=%s", document_id)
        result = await asyncio.to_thread(_append)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_append_text failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_docs_find_replace(
    document_id: str, find_text: str, replace_text: str, match_case: bool = False
) -> dict:
    """Find and replace text in a Google Doc.

    Replaces all occurrences of the search text with the replacement text.

    Args:
        document_id: ID of the document to modify.
        find_text: Text to search for.
        replace_text: Text to replace with.
        match_case: Whether to match case exactly (default: False).

    Returns:
        Operation result with document_id, find/replace texts, and replacement count.
    """
    try:

        def _replace():
            service = get_google_service("docs", "v1", DOCS_FULL_SCOPES)
            requests = [
                {
                    "replaceAllText": {
                        "containsText": {"text": find_text, "matchCase": match_case},
                        "replaceText": replace_text,
                    }
                }
            ]
            result = (
                service.documents()
                .batchUpdate(documentId=document_id, body={"requests": requests})
                .execute()
            )

            replacements = 0
            for reply in result.get("replies", []):
                if "replaceAllText" in reply:
                    replacements = reply["replaceAllText"].get("occurrencesChanged", 0)

            return {
                "document_id": document_id,
                "find_text": find_text,
                "replace_text": replace_text,
                "replacements": replacements,
            }

        logger.info("docs_find_replace doc_id=%s find=%s", document_id, find_text)
        result = await asyncio.to_thread(_replace)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_find_replace failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_docs_list_in_folder(folder_id: str, max_results: int = 50) -> dict:
    """List all Google Docs in a specific folder.

    Returns all documents within the specified Drive folder.

    Args:
        folder_id: ID of the folder to list documents from.
        max_results: Maximum number of documents to return (default: 50).

    Returns:
        List of documents with id, name, modified date, and web_link.
    """
    try:

        def _list():
            service = get_google_service("drive", "v3", DOCS_READONLY_SCOPES)
            query = (
                f"'{folder_id}' in parents and "
                "mimeType='application/vnd.google-apps.document' and "
                "trashed=false"
            )
            results = (
                service.files()
                .list(
                    q=query,
                    pageSize=max_results,
                    fields="files(id, name, modifiedTime, webViewLink)",
                    orderBy="modifiedTime desc",
                )
                .execute()
            )
            files = results.get("files", [])
            return {
                "documents": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "modified": f.get("modifiedTime", ""),
                        "web_link": f.get("webViewLink", ""),
                    }
                    for f in files
                ],
                "total": len(files),
            }

        logger.info("docs_list_in_folder folder_id=%s", folder_id)
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("docs_list_in_folder failed")
        return {"success": False, "error": str(e)}
