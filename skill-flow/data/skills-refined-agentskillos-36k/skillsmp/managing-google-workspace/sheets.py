"""Google Sheets tools for reading, writing, and managing spreadsheets."""

import asyncio
import logging

from src.humcp.decorator import tool
from src.tools.google.auth import SCOPES, get_google_service

logger = logging.getLogger("humcp.tools.google.sheets")

SHEETS_READONLY_SCOPES = [SCOPES["sheets_readonly"], SCOPES["drive_readonly"]]
SHEETS_FULL_SCOPES = [SCOPES["sheets"], SCOPES["drive"]]


@tool()
async def google_sheets_list_spreadsheets(max_results: int = 25) -> dict:
    """List Google Spreadsheets accessible to the user.

    Returns recent spreadsheets ordered by modification time.

    Args:
        max_results: Maximum number of spreadsheets to return (default: 25).

    Returns:
        List of spreadsheets with id, name, modified date, and web_link.
    """
    try:

        def _list():
            service = get_google_service("drive", "v3", SHEETS_READONLY_SCOPES)
            query = (
                "mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
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
                "spreadsheets": [
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

        logger.info("sheets_list_spreadsheets")
        result = await asyncio.to_thread(_list)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_list_spreadsheets failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_get_info(spreadsheet_id: str) -> dict:
    """Get metadata about a spreadsheet.

    Returns information about all sheets in the spreadsheet including dimensions.

    Args:
        spreadsheet_id: ID of the spreadsheet.

    Returns:
        Spreadsheet info with id, title, locale, sheets list, and web_link.
    """
    try:

        def _get():
            service = get_google_service("sheets", "v4", SHEETS_READONLY_SCOPES)
            spreadsheet = (
                service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            )
            sheets = spreadsheet.get("sheets", [])
            return {
                "id": spreadsheet["spreadsheetId"],
                "title": spreadsheet.get("properties", {}).get("title", ""),
                "locale": spreadsheet.get("properties", {}).get("locale", ""),
                "sheets": [
                    {
                        "id": s["properties"]["sheetId"],
                        "title": s["properties"]["title"],
                        "index": s["properties"]["index"],
                        "row_count": s["properties"]
                        .get("gridProperties", {})
                        .get("rowCount", 0),
                        "column_count": s["properties"]
                        .get("gridProperties", {})
                        .get("columnCount", 0),
                    }
                    for s in sheets
                ],
                "web_link": spreadsheet.get("spreadsheetUrl", ""),
            }

        logger.info("sheets_get_info id=%s", spreadsheet_id)
        result = await asyncio.to_thread(_get)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_get_info failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_read_values(
    spreadsheet_id: str, range_notation: str = "Sheet1"
) -> dict:
    """Read values from a spreadsheet range.

    Reads cell values from the specified range using A1 notation.

    Args:
        spreadsheet_id: ID of the spreadsheet.
        range_notation: Range in A1 notation (default: "Sheet1", e.g., "Sheet1!A1:D10").

    Returns:
        Values with range, rows (2D array), row_count, and column_count.
    """
    try:

        def _read():
            service = get_google_service("sheets", "v4", SHEETS_READONLY_SCOPES)
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_notation)
                .execute()
            )
            values = result.get("values", [])
            return {
                "range": result.get("range", ""),
                "rows": values,
                "row_count": len(values),
                "column_count": max(len(row) for row in values) if values else 0,
            }

        logger.info("sheets_read_values id=%s range=%s", spreadsheet_id, range_notation)
        result = await asyncio.to_thread(_read)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_read_values failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_write_values(
    spreadsheet_id: str,
    range_notation: str,
    values: list,
    input_option: str = "USER_ENTERED",
) -> dict:
    """Write values to a spreadsheet range.

    Updates cells in the specified range with the provided values.

    Args:
        spreadsheet_id: ID of the spreadsheet.
        range_notation: Range in A1 notation (e.g., "Sheet1!A1:D10").
        values: 2D array of values to write.
        input_option: How to interpret input ("USER_ENTERED" or "RAW").

    Returns:
        Update result with updated_range, updated_rows, updated_columns, updated_cells.
    """
    try:

        def _write():
            service = get_google_service("sheets", "v4", SHEETS_FULL_SCOPES)
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range_notation,
                    valueInputOption=input_option,
                    body=body,
                )
                .execute()
            )
            return {
                "updated_range": result.get("updatedRange", ""),
                "updated_rows": result.get("updatedRows", 0),
                "updated_columns": result.get("updatedColumns", 0),
                "updated_cells": result.get("updatedCells", 0),
            }

        logger.info(
            "sheets_write_values id=%s range=%s", spreadsheet_id, range_notation
        )
        result = await asyncio.to_thread(_write)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_write_values failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_append_values(
    spreadsheet_id: str,
    range_notation: str,
    values: list,
    input_option: str = "USER_ENTERED",
) -> dict:
    """Append values to a spreadsheet (adds rows after existing data).

    Appends rows to the end of the data in the specified range.

    Args:
        spreadsheet_id: ID of the spreadsheet.
        range_notation: Range to append to (e.g., "Sheet1!A:D").
        values: 2D array of values to append.
        input_option: How to interpret input ("USER_ENTERED" or "RAW").

    Returns:
        Append result with updated_range, updated_rows, updated_cells.
    """
    try:

        def _append():
            service = get_google_service("sheets", "v4", SHEETS_FULL_SCOPES)
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_notation,
                    valueInputOption=input_option,
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )
            updates = result.get("updates", {})
            return {
                "updated_range": updates.get("updatedRange", ""),
                "updated_rows": updates.get("updatedRows", 0),
                "updated_cells": updates.get("updatedCells", 0),
            }

        logger.info(
            "sheets_append_values id=%s range=%s", spreadsheet_id, range_notation
        )
        result = await asyncio.to_thread(_append)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_append_values failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_create_spreadsheet(
    title: str, sheet_names: list[str] | None = None
) -> dict:
    """Create a new Google Spreadsheet.

    Creates a spreadsheet with optional named sheets.

    Args:
        title: Title for the new spreadsheet.
        sheet_names: Optional list of sheet names to create.

    Returns:
        Created spreadsheet with id, title, sheets list, and web_link.
    """
    try:

        def _create():
            service = get_google_service("sheets", "v4", SHEETS_FULL_SCOPES)

            body = {"properties": {"title": title}}

            if sheet_names:
                body["sheets"] = [
                    {"properties": {"title": name}} for name in sheet_names
                ]

            spreadsheet = service.spreadsheets().create(body=body).execute()

            return {
                "id": spreadsheet["spreadsheetId"],
                "title": spreadsheet.get("properties", {}).get("title", ""),
                "sheets": [
                    s["properties"]["title"] for s in spreadsheet.get("sheets", [])
                ],
                "web_link": spreadsheet.get("spreadsheetUrl", ""),
            }

        logger.info("sheets_create_spreadsheet title=%s", title)
        result = await asyncio.to_thread(_create)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_create_spreadsheet failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_add_sheet(spreadsheet_id: str, sheet_title: str) -> dict:
    """Add a new sheet to an existing spreadsheet.

    Creates a new tab/sheet within the spreadsheet.

    Args:
        spreadsheet_id: ID of the spreadsheet.
        sheet_title: Title for the new sheet.

    Returns:
        New sheet details with sheet_id, title, and spreadsheet_id.
    """
    try:

        def _add():
            service = get_google_service("sheets", "v4", SHEETS_FULL_SCOPES)
            request = {"addSheet": {"properties": {"title": sheet_title}}}
            result = (
                service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": [request]})
                .execute()
            )
            new_sheet = result.get("replies", [{}])[0].get("addSheet", {})
            return {
                "sheet_id": new_sheet.get("properties", {}).get("sheetId"),
                "title": new_sheet.get("properties", {}).get("title"),
                "spreadsheet_id": spreadsheet_id,
            }

        logger.info("sheets_add_sheet id=%s title=%s", spreadsheet_id, sheet_title)
        result = await asyncio.to_thread(_add)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_add_sheet failed")
        return {"success": False, "error": str(e)}


@tool()
async def google_sheets_clear_values(spreadsheet_id: str, range_notation: str) -> dict:
    """Clear values from a spreadsheet range.

    Removes all values from cells in the specified range without deleting the cells.

    Args:
        spreadsheet_id: ID of the spreadsheet.
        range_notation: Range to clear in A1 notation.

    Returns:
        Clear result with cleared_range and spreadsheet_id.
    """
    try:

        def _clear():
            service = get_google_service("sheets", "v4", SHEETS_FULL_SCOPES)
            result = (
                service.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheet_id, range=range_notation, body={})
                .execute()
            )
            return {
                "cleared_range": result.get("clearedRange", ""),
                "spreadsheet_id": spreadsheet_id,
            }

        logger.info(
            "sheets_clear_values id=%s range=%s", spreadsheet_id, range_notation
        )
        result = await asyncio.to_thread(_clear)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("sheets_clear_values failed")
        return {"success": False, "error": str(e)}
