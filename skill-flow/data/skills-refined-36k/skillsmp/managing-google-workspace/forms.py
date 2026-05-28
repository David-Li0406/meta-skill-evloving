"""Google Forms tools for managing forms and responses."""

import asyncio
import logging

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.forms")

FORMS_READONLY_SCOPES = [SCOPES["forms_readonly"], SCOPES["drive_readonly"]]
FORMS_FULL_SCOPES = [SCOPES["forms"], SCOPES["drive"]]
FORMS_RESPONSES_SCOPES = [SCOPES["forms_responses"]]


@tool()
async def google_forms_list_forms(max_results: int = 25) -> dict:
    """List Google Forms accessible to the user.

    Returns recent forms ordered by modification time.

    Args:
        max_results: Maximum number of forms to return (default: 25).

    Returns:
        List of forms with id, name, modified date, and web_link.
    """
    try:

        def _list():
            service = get_google_service("drive", "v3", FORMS_READONLY_SCOPES)
            query = "mimeType='application/vnd.google-apps.form' and trashed=false"
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
                "forms": [
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

        logger.info("forms_list_forms")
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("forms_list_forms failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_forms_get_form(form_id: str) -> dict:
    """Get details about a form including questions.

    Returns form metadata and all questions with their types and options.

    Args:
        form_id: ID of the form.

    Returns:
        Form details with id, title, description, responder_uri, questions list.
    """
    try:

        def _get():
            service = get_google_service("forms", "v1", FORMS_READONLY_SCOPES)
            form = service.forms().get(formId=form_id).execute()

            questions = []
            for item in form.get("items", []):
                q_info = {
                    "id": item.get("itemId", ""),
                    "title": item.get("title", ""),
                }

                if "questionItem" in item:
                    question = item["questionItem"].get("question", {})
                    q_info["required"] = question.get("required", False)

                    # Determine question type
                    if "textQuestion" in question:
                        q_info["type"] = "text"
                        q_info["paragraph"] = question["textQuestion"].get(
                            "paragraph", False
                        )
                    elif "choiceQuestion" in question:
                        choice = question["choiceQuestion"]
                        q_info["type"] = choice.get("type", "RADIO").lower()
                        q_info["options"] = [
                            o.get("value", "") for o in choice.get("options", [])
                        ]
                    elif "scaleQuestion" in question:
                        q_info["type"] = "scale"
                        q_info["low"] = question["scaleQuestion"].get("low", 1)
                        q_info["high"] = question["scaleQuestion"].get("high", 5)
                    elif "dateQuestion" in question:
                        q_info["type"] = "date"
                    elif "timeQuestion" in question:
                        q_info["type"] = "time"
                    else:
                        q_info["type"] = "unknown"

                questions.append(q_info)

            return {
                "id": form["formId"],
                "title": form.get("info", {}).get("title", ""),
                "description": form.get("info", {}).get("description", ""),
                "document_title": form.get("info", {}).get("documentTitle", ""),
                "responder_uri": form.get("responderUri", ""),
                "questions": questions,
                "question_count": len(questions),
            }

        logger.info("forms_get_form id=%s", form_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("forms_get_form failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_forms_create_form(title: str, document_title: str = "") -> dict:
    """Create a new Google Form.

    Creates an empty form with the specified title.

    Args:
        title: Display title for the form.
        document_title: Document name in Drive (defaults to title).

    Returns:
        Created form with id, title, document_title, responder_uri, and edit_uri.
    """
    try:

        def _create():
            service = get_google_service("forms", "v1", FORMS_FULL_SCOPES)
            body = {
                "info": {
                    "title": title,
                    "documentTitle": document_title or title,
                }
            }
            form = service.forms().create(body=body).execute()

            return {
                "id": form["formId"],
                "title": form.get("info", {}).get("title", ""),
                "document_title": form.get("info", {}).get("documentTitle", ""),
                "responder_uri": form.get("responderUri", ""),
                "edit_uri": f"https://docs.google.com/forms/d/{form['formId']}/edit",
            }

        logger.info("forms_create_form title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("forms_create_form failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_forms_list_responses(form_id: str, max_results: int = 100) -> dict:
    """List responses submitted to a form.

    Returns summary information about form responses.

    Args:
        form_id: ID of the form.
        max_results: Maximum number of responses to return (default: 100).

    Returns:
        List of responses with id, created time, last_submitted, and answer_count.
    """
    try:

        def _list():
            service = get_google_service("forms", "v1", FORMS_RESPONSES_SCOPES)
            results = (
                service.forms()
                .responses()
                .list(formId=form_id, pageSize=max_results)
                .execute()
            )
            responses = results.get("responses", [])

            return {
                "responses": [
                    {
                        "id": r.get("responseId", ""),
                        "created": r.get("createTime", ""),
                        "last_submitted": r.get("lastSubmittedTime", ""),
                        "answer_count": len(r.get("answers", {})),
                    }
                    for r in responses
                ],
                "total": len(responses),
            }

        logger.info("forms_list_responses form_id=%s", form_id)
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("forms_list_responses failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_forms_get_response(form_id: str, response_id: str) -> dict:
    """Get a specific form response with all answers.

    Returns detailed answer data for a single form submission.

    Args:
        form_id: ID of the form.
        response_id: ID of the response.

    Returns:
        Response details with response_id, created, last_submitted, and answers list.
    """
    try:

        def _get():
            service = get_google_service("forms", "v1", FORMS_RESPONSES_SCOPES)
            response = (
                service.forms()
                .responses()
                .get(formId=form_id, responseId=response_id)
                .execute()
            )

            answers = []
            for question_id, answer_data in response.get("answers", {}).items():
                answer_info = {
                    "question_id": question_id,
                }

                if "textAnswers" in answer_data:
                    answer_info["type"] = "text"
                    answer_info["values"] = [
                        a.get("value", "")
                        for a in answer_data["textAnswers"].get("answers", [])
                    ]
                elif "fileUploadAnswers" in answer_data:
                    answer_info["type"] = "file"
                    answer_info["files"] = [
                        {"id": f.get("fileId"), "name": f.get("fileName")}
                        for f in answer_data["fileUploadAnswers"].get("answers", [])
                    ]

                answers.append(answer_info)

            return {
                "response_id": response.get("responseId", ""),
                "created": response.get("createTime", ""),
                "last_submitted": response.get("lastSubmittedTime", ""),
                "answers": answers,
            }

        logger.info(
            "forms_get_response form_id=%s response_id=%s", form_id, response_id
        )
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("forms_get_response failed")
        return {"success": False, "error": str(e)}
