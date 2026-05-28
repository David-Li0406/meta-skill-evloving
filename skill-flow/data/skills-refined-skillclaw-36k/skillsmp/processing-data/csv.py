"""CSV file tools with DuckDB query support.

Security Note:
    The query_csv_file tool only allows SELECT queries for safety.
    All queries are validated before execution.
"""

import csv as csv_lib
import logging
import re
from pathlib import Path

from src.humcp.decorator import tool

logger = logging.getLogger("humcp.tools.csv")

# Allowed SQL operations (read-only)
_ALLOWED_SQL_PATTERN = re.compile(
    r"^\s*SELECT\s+.+\s+FROM\s+",
    re.IGNORECASE | re.DOTALL,
)

# Disallowed SQL keywords that could modify data or execute dangerous operations
_DISALLOWED_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|EXEC|EXECUTE|"
    r"ATTACH|DETACH|COPY|LOAD|INSTALL|PRAGMA)\b",
    re.IGNORECASE,
)

try:
    import duckdb

    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False


class CSVManager:
    def __init__(self, csv_files: list[str] | None = None):
        self.csv_files = []
        self.csv_map = {}
        if csv_files:
            for file_path in csv_files:
                path = Path(file_path)
                if path.exists() and path.suffix.lower() == ".csv":
                    self.csv_files.append(path)
                    self.csv_map[path.stem] = path

    def get_file_path(self, csv_name: str):
        return self.csv_map.get(csv_name)

    def list_files(self):
        return list(self.csv_map.keys())


_csv_manager = None


def get_csv_manager():
    global _csv_manager
    if _csv_manager is None:
        _csv_manager = CSVManager()
    return _csv_manager


def set_csv_files(csv_files: list):
    global _csv_manager
    _csv_manager = CSVManager(csv_files)


@tool()
async def list_csv_files() -> dict:
    """List all available CSV files."""
    try:
        manager = get_csv_manager()
        logger.info("Listing CSV files count=%d", len(manager.list_files()))
        return {
            "success": True,
            "data": manager.list_files(),
            "count": len(manager.list_files()),
        }
    except Exception as e:
        logger.exception("Failed to list CSV files")
        return {"success": False, "error": str(e)}


@tool()
async def read_csv_file(csv_name: str, row_limit: int | None = None) -> dict:
    """Read contents of a CSV file."""
    try:
        manager = get_csv_manager()
        file_path = manager.get_file_path(csv_name)
        if not file_path:
            return {"success": False, "error": f"CSV '{csv_name}' not found"}
        logger.info("Reading CSV file name=%s limit=%s", csv_name, row_limit)

        rows = []
        with open(file_path, encoding="utf-8") as f:
            reader = csv_lib.DictReader(f)
            for i, row in enumerate(reader):
                if row_limit and i >= row_limit:
                    break
                rows.append(row)

        return {"success": True, "data": rows, "row_count": len(rows)}
    except Exception as e:
        logger.exception("Failed to read CSV file name=%s", csv_name)
        return {"success": False, "error": str(e)}


@tool()
async def get_csv_columns(csv_name: str) -> dict:
    """Get column names from a CSV file."""
    try:
        manager = get_csv_manager()
        file_path = manager.get_file_path(csv_name)
        if not file_path:
            return {"success": False, "error": f"CSV '{csv_name}' not found"}
        logger.info("Getting CSV columns name=%s", csv_name)

        with open(file_path, encoding="utf-8") as f:
            reader = csv_lib.DictReader(f)
            columns = reader.fieldnames or []

        return {"success": True, "data": columns, "column_count": len(columns)}
    except Exception as e:
        logger.exception("Failed to get CSV columns name=%s", csv_name)
        return {"success": False, "error": str(e)}


def _validate_sql_query(query: str) -> tuple[bool, str]:
    """Validate SQL query for safety.

    Args:
        query: SQL query to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    # Check for disallowed keywords
    if _DISALLOWED_KEYWORDS.search(query):
        return False, "Query contains disallowed SQL keywords (only SELECT allowed)"

    # Check if query starts with SELECT
    if not _ALLOWED_SQL_PATTERN.match(query):
        return False, "Only SELECT queries are allowed"

    return True, ""


@tool()
async def query_csv_file(csv_name: str, sql_query: str) -> dict:
    """Execute SQL query on CSV file using DuckDB.

    Security: Only SELECT queries are allowed. Queries with INSERT, UPDATE,
    DELETE, DROP, or other data-modifying statements will be rejected.
    """
    try:
        if not DUCKDB_AVAILABLE:
            return {"success": False, "error": "DuckDB required: pip install duckdb"}

        manager = get_csv_manager()
        file_path = manager.get_file_path(csv_name)
        if not file_path:
            return {"success": False, "error": f"CSV '{csv_name}' not found"}

        # Sanitize and validate query
        query = sql_query.strip().split(";")[0]  # Only first statement
        is_valid, error_msg = _validate_sql_query(query)
        if not is_valid:
            logger.warning("SQL query rejected name=%s reason=%s", csv_name, error_msg)
            return {"success": False, "error": error_msg}

        logger.info("Querying CSV file name=%s", csv_name)

        # Use parameterized table creation with sanitized table name
        safe_table_name = re.sub(r"[^a-zA-Z0-9_]", "_", csv_name)
        conn = duckdb.connect(":memory:")
        conn.execute(
            f"CREATE TABLE {safe_table_name} AS SELECT * FROM read_csv_auto(?)",
            [str(file_path)],
        )
        # Replace table name in query
        query = re.sub(
            rf"\b{re.escape(csv_name)}\b",
            safe_table_name,
            query,
            flags=re.IGNORECASE,
        )
        result = conn.execute(query).fetchall()
        columns = [desc[0] for desc in conn.description]
        rows = [dict(zip(columns, row, strict=False)) for row in result]
        conn.close()

        return {
            "success": True,
            "data": rows,
            "row_count": len(rows),
            "columns": columns,
        }
    except Exception as e:
        logger.exception("Failed to query CSV file name=%s", csv_name)
        return {"success": False, "error": str(e)}


@tool()
async def describe_csv_file(csv_name: str) -> dict:
    """Get detailed information about a CSV file."""
    try:
        manager = get_csv_manager()
        file_path = manager.get_file_path(csv_name)
        if not file_path:
            return {"success": False, "error": f"CSV '{csv_name}' not found"}
        logger.info("Describing CSV file name=%s", csv_name)

        file_size = file_path.stat().st_size
        rows = []

        with open(file_path, encoding="utf-8") as f:
            reader = csv_lib.DictReader(f)
            columns = reader.fieldnames or []
            for i, row in enumerate(reader):
                if i < 5:
                    rows.append(row)
                if i >= 1000:
                    break
            row_count = i + 1

        return {
            "success": True,
            "data": {
                "file_name": csv_name,
                "file_size_bytes": file_size,
                "columns": columns,
                "column_count": len(columns),
                "row_count": row_count,
                "sample_rows": rows[:5],
            },
        }
    except Exception as e:
        logger.exception("Failed to describe CSV file name=%s", csv_name)
        return {"success": False, "error": str(e)}


@tool()
async def add_csv_file(file_path: str) -> dict:
    """Add a CSV file to available files."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}
        if path.suffix.lower() != ".csv":
            return {"success": False, "error": f"Not a CSV: {file_path}"}

        manager = get_csv_manager()
        manager.csv_files.append(path)
        manager.csv_map[path.stem] = path

        logger.info("Added CSV file name=%s", path.stem)
        return {
            "success": True,
            "data": {"message": f"Added: {path.stem}", "file_name": path.stem},
        }
    except Exception as e:
        logger.exception("Failed to add CSV file path=%s", file_path)
        return {"success": False, "error": str(e)}


@tool()
async def remove_csv_file(csv_name: str) -> dict:
    """Remove a CSV file from available files."""
    try:
        manager = get_csv_manager()
        if csv_name not in manager.csv_map:
            return {"success": False, "error": f"CSV '{csv_name}' not found"}

        path = manager.csv_map[csv_name]
        manager.csv_files.remove(path)
        del manager.csv_map[csv_name]

        logger.info("Removed CSV file name=%s", csv_name)
        return {"success": True, "data": {"message": f"Removed: {csv_name}"}}
    except Exception as e:
        logger.exception("Failed to remove CSV file name=%s", csv_name)
        return {"success": False, "error": str(e)}
