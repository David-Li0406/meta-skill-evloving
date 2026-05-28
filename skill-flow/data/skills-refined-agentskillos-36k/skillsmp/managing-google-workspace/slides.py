"""Google Slides tools for creating and managing presentations."""

import asyncio
import logging

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.slides")

SLIDES_READONLY_SCOPES = [SCOPES["slides_readonly"], SCOPES["drive_readonly"]]
SLIDES_FULL_SCOPES = [SCOPES["slides"], SCOPES["drive"]]


@tool()
async def google_slides_list_presentations(max_results: int = 25) -> dict:
    """List Google Slides presentations accessible to the user.

    Returns recent presentations ordered by modification time.

    Args:
        max_results: Maximum number of presentations to return (default: 25).

    Returns:
        List of presentations with id, name, modified date, and web_link.
    """
    try:

        def _list():
            service = get_google_service("drive", "v3", SLIDES_READONLY_SCOPES)
            query = (
                "mimeType='application/vnd.google-apps.presentation' and trashed=false"
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
                "presentations": [
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

        logger.info("slides_list_presentations")
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_list_presentations failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_slides_get_presentation(presentation_id: str) -> dict:
    """Get details about a presentation including slides content.

    Returns presentation metadata and text content from all slides.

    Args:
        presentation_id: ID of the presentation.

    Returns:
        Presentation info with id, title, slide_count, slides with text elements, dimensions.
    """
    try:

        def _get():
            service = get_google_service("slides", "v1", SLIDES_READONLY_SCOPES)
            presentation = (
                service.presentations().get(presentationId=presentation_id).execute()
            )

            slides = []
            for slide in presentation.get("slides", []):
                slide_info = {
                    "id": slide["objectId"],
                    "elements": [],
                }

                # Extract text content from shapes
                for element in slide.get("pageElements", []):
                    if "shape" in element and "text" in element.get("shape", {}):
                        text_content = []
                        for text_element in element["shape"]["text"].get(
                            "textElements", []
                        ):
                            if "textRun" in text_element:
                                text_content.append(
                                    text_element["textRun"].get("content", "")
                                )
                        if text_content:
                            slide_info["elements"].append(
                                {
                                    "type": "text",
                                    "content": "".join(text_content).strip(),
                                }
                            )

                slides.append(slide_info)

            return {
                "id": presentation["presentationId"],
                "title": presentation.get("title", ""),
                "slide_count": len(slides),
                "slides": slides,
                "width": presentation.get("pageSize", {})
                .get("width", {})
                .get("magnitude", 0),
                "height": presentation.get("pageSize", {})
                .get("height", {})
                .get("magnitude", 0),
            }

        logger.info("slides_get_presentation id=%s", presentation_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_get_presentation failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_slides_create_presentation(title: str) -> dict:
    """Create a new Google Slides presentation.

    Creates an empty presentation with one blank slide.

    Args:
        title: Title for the new presentation.

    Returns:
        Created presentation with id, title, slide_count, and web_link.
    """
    try:

        def _create():
            service = get_google_service("slides", "v1", SLIDES_FULL_SCOPES)
            presentation = (
                service.presentations().create(body={"title": title}).execute()
            )
            return {
                "id": presentation["presentationId"],
                "title": presentation.get("title", ""),
                "slide_count": len(presentation.get("slides", [])),
                "web_link": f"https://docs.google.com/presentation/d/{presentation['presentationId']}/edit",
            }

        logger.info("slides_create_presentation title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_create_presentation failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_slides_add_slide(
    presentation_id: str,
    layout: str = "BLANK",
    insert_at: int = -1,
) -> dict:
    """Add a new slide to a presentation.

    Creates a slide with the specified layout at the given position.

    Args:
        presentation_id: ID of the presentation.
        layout: Slide layout type (default: "BLANK"). Options include BLANK, TITLE, etc.
        insert_at: Position to insert slide (-1 for end).

    Returns:
        New slide info with slide_id, presentation_id, and layout.
    """
    try:

        def _add():
            service = get_google_service("slides", "v1", SLIDES_FULL_SCOPES)

            request = {
                "createSlide": {
                    "slideLayoutReference": {"predefinedLayout": layout},
                }
            }

            if insert_at >= 0:
                request["createSlide"]["insertionIndex"] = insert_at

            result = (
                service.presentations()
                .batchUpdate(
                    presentationId=presentation_id, body={"requests": [request]}
                )
                .execute()
            )

            new_slide_id = (
                result.get("replies", [{}])[0].get("createSlide", {}).get("objectId")
            )

            return {
                "slide_id": new_slide_id,
                "presentation_id": presentation_id,
                "layout": layout,
            }

        logger.info("slides_add_slide id=%s layout=%s", presentation_id, layout)
        result = await asyncio.to_thread(_add)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_add_slide failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_slides_add_text(
    presentation_id: str,
    slide_id: str,
    text: str,
    x: float = 100,
    y: float = 100,
    width: float = 400,
    height: float = 100,
) -> dict:
    """Add a text box to a slide.

    Creates a text box at the specified position with the given dimensions.

    Args:
        presentation_id: ID of the presentation.
        slide_id: ID of the slide to add text to.
        text: Text content for the text box.
        x: X position in points (default: 100).
        y: Y position in points (default: 100).
        width: Width in points (default: 400).
        height: Height in points (default: 100).

    Returns:
        Created text box info with shape_id, slide_id, and text.
    """
    try:

        def _add_text():
            service = get_google_service("slides", "v1", SLIDES_FULL_SCOPES)

            # Create text box shape
            shape_id = f"textbox_{slide_id}_{int(x)}_{int(y)}"

            requests = [
                {
                    "createShape": {
                        "objectId": shape_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {
                                "width": {"magnitude": width, "unit": "PT"},
                                "height": {"magnitude": height, "unit": "PT"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": x,
                                "translateY": y,
                                "unit": "PT",
                            },
                        },
                    }
                },
                {
                    "insertText": {
                        "objectId": shape_id,
                        "text": text,
                        "insertionIndex": 0,
                    }
                },
            ]

            service.presentations().batchUpdate(
                presentationId=presentation_id, body={"requests": requests}
            ).execute()

            return {
                "shape_id": shape_id,
                "slide_id": slide_id,
                "text": text,
            }

        logger.info("slides_add_text id=%s slide=%s", presentation_id, slide_id)
        result = await asyncio.to_thread(_add_text)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_add_text failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_slides_get_thumbnail(
    presentation_id: str,
    slide_id: str,
    size: str = "MEDIUM",
) -> dict:
    """Get a thumbnail image URL for a slide.

    Returns a URL to a thumbnail image of the specified slide.

    Args:
        presentation_id: ID of the presentation.
        slide_id: ID of the slide.
        size: Thumbnail size - "SMALL", "MEDIUM", or "LARGE" (default: "MEDIUM").

    Returns:
        Thumbnail info with slide_id, content_url, width, and height.
    """
    try:

        def _get_thumbnail():
            service = get_google_service("slides", "v1", SLIDES_READONLY_SCOPES)

            size_map = {
                "SMALL": "SMALL",
                "MEDIUM": "MEDIUM",
                "LARGE": "LARGE",
            }
            thumbnail_size = size_map.get(size.upper(), "MEDIUM")

            result = (
                service.presentations()
                .pages()
                .getThumbnail(
                    presentationId=presentation_id,
                    pageObjectId=slide_id,
                    thumbnailProperties_thumbnailSize=thumbnail_size,
                )
                .execute()
            )

            return {
                "slide_id": slide_id,
                "content_url": result.get("contentUrl", ""),
                "width": result.get("width", 0),
                "height": result.get("height", 0),
            }

        logger.info("slides_get_thumbnail id=%s slide=%s", presentation_id, slide_id)
        result = await asyncio.to_thread(_get_thumbnail)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("slides_get_thumbnail failed")
        return {"success": False, "error": str(e)}
