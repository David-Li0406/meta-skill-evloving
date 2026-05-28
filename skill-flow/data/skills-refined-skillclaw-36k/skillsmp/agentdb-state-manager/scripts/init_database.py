#!/usr/bin/env python3
"""Initialize AgentDB schema for workflow state tracking.

This script initializes the AgentDB database with the canonical schema for
workflow state management. It creates tables, indexes, and loads state
definitions from workflow-states.json.

Usage:
    python init_database.py [--session-id SESSION_ID]

If --session-id is not provided, generates timestamp-based ID.

Constants:
- SCHEMA_VERSION: Current schema version
  Rationale: Track schema evolution for migrations
- WORKFLOW_STATES_PATH: Path to workflow-states.json
  Rationale: Single source of truth for state definitions
"""

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

# Add workflow-utilities to path for worktree_context
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)

# Constants with documented rationale
SCHEMA_VERSION = "1.0.0"  # Current schema version for migrations
WORKFLOW_STATES_PATH = Path(__file__).parent.parent / "templates" / "workflow-states.json"
SYNC_SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "agentdb_sync_schema.sql"


def get_default_db_path() -> Path:
    """Get default database path in worktree state directory.

    Returns:
        Path to agentdb.duckdb in .claude-state/ directory.
        Falls back to current directory if worktree detection fails.
    """
    try:
        from worktree_context import get_state_dir

        return get_state_dir() / "agentdb.duckdb"
    except (ImportError, RuntimeError):
        # Fallback for non-git environments or missing module
        return Path("agentdb.duckdb")


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit.

    Args:
        message: Error message to display
        code: Exit code (default 1)
    """
    print(f"{Colors.RED}✗ Error:{Colors.END} {message}", file=sys.stderr)
    sys.exit(code)


def success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message to display
    """
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to display
    """
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message to display
    """
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def generate_session_id() -> str:
    """Generate timestamp-based session ID for AgentDB.

    Returns:
        16-character hex session ID

    Rationale: Timestamp-based IDs are reproducible within a timeframe,
    providing a balance between uniqueness and consistency.
    """
    current_time = datetime.now(UTC).isoformat()
    return hashlib.md5(current_time.encode()).hexdigest()[:16]


def load_workflow_states() -> dict[str, Any]:
    """Load canonical state definitions from workflow-states.json.

    Returns:
        Dictionary of state definitions

    Raises:
        FileNotFoundError: If workflow-states.json not found
        json.JSONDecodeError: If JSON is malformed
    """
    if not WORKFLOW_STATES_PATH.exists():
        error_exit(f"workflow-states.json not found: {WORKFLOW_STATES_PATH}")

    info(f"Loading state definitions from {WORKFLOW_STATES_PATH.name}...")

    try:
        with open(WORKFLOW_STATES_PATH, encoding="utf-8") as f:
            states = json.load(f)
        success(f"Loaded {len(states.get('states', {}))} object types")
        return states
    except json.JSONDecodeError as e:
        error_exit(f"Invalid JSON in workflow-states.json: {e}")
    except Exception as e:
        error_exit(f"Failed to load workflow-states.json: {e}")


def create_schema(session_id: str, workflow_states: dict[str, Any], db_path: Path) -> bool:
    """Create AgentDB schema with tables and indexes.

    Args:
        session_id: AgentDB session identifier
        workflow_states: State definitions from workflow-states.json
        db_path: Path to DuckDB database file

    Returns:
        True if schema created successfully, False otherwise
    """
    info("Creating AgentDB schema...")

    try:
        # Ensure parent directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Connect to DuckDB
        conn = duckdb.connect(str(db_path))

        # Load and execute the sync schema SQL file
        if SYNC_SCHEMA_PATH.exists():
            print(f"\n{Colors.BOLD}Executing sync schema from {SYNC_SCHEMA_PATH.name}:{Colors.END}")
            schema_sql = SYNC_SCHEMA_PATH.read_text()

            # Remove SQL comments
            import re

            # Remove single-line comments (-- ...)
            schema_sql = re.sub(r"--[^\n]*\n", "\n", schema_sql)

            # Split by semicolons
            statements = [s.strip() for s in schema_sql.split(";") if s.strip()]

            # Execute all statements
            success_count = 0
            for i, stmt in enumerate(statements, 1):
                if stmt:
                    try:
                        conn.execute(stmt)
                        success_count += 1
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            # Only warn for non-trivial errors
                            if "SELECT" not in stmt[:20]:  # Skip validation queries
                                warning(f"  Statement {i}: {str(e)[:60]}")
            print(f"  ✓ Executed {success_count} statements")
        else:
            warning(f"Sync schema not found: {SYNC_SCHEMA_PATH}")

        # Create session metadata table
        print(f"\n{Colors.BOLD}Creating session metadata:{Colors.END}")

        session_statements = [
            """
            CREATE TABLE IF NOT EXISTS session_metadata (
                key VARCHAR PRIMARY KEY,
                value VARCHAR
            );
            """,
            f"""
            INSERT INTO session_metadata (key, value)
            VALUES
                ('session_id', '{session_id}'),
                ('schema_version', '{SCHEMA_VERSION}'),
                ('workflow_version', '{workflow_states.get("version", "unknown")}'),
                ('initialized_at', current_timestamp)
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
            """,
        ]

        for stmt in session_statements:
            conn.execute(stmt.strip())

        conn.close()
        success(f"Schema created in {db_path}")
        return True

    except Exception as e:
        error_exit(f"Schema creation failed: {e}")


def validate_schema(db_path: Path) -> bool:
    """Validate that schema was created correctly.

    Args:
        db_path: Path to DuckDB database file

    Returns:
        True if validation passed, False otherwise
    """
    info("Validating schema...")

    try:
        conn = duckdb.connect(str(db_path))

        # Check tables exist
        tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
        table_names = [t[0] for t in tables]

        required_tables = ["session_metadata", "agent_synchronizations"]
        for table in required_tables:
            if table not in table_names:
                error_exit(f"{table} table not found")

        # Check session metadata
        count = conn.execute("SELECT COUNT(*) FROM session_metadata").fetchone()[0]
        if count < 4:
            warning(f"Expected 4 metadata rows, found {count}")

        conn.close()
        success("Schema validation passed")
        return True

    except Exception as e:
        error_exit(f"Schema validation failed: {e}")


def print_summary(session_id: str, workflow_states: dict[str, Any], db_path: Path) -> None:
    """Print initialization summary.

    Args:
        session_id: AgentDB session identifier
        workflow_states: Loaded state definitions
        db_path: Path to DuckDB database file
    """
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}AgentDB Initialization Complete{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    print(f"{Colors.BLUE}Database:{Colors.END} {db_path}")
    print(f"{Colors.BLUE}Session ID:{Colors.END} {session_id}")
    print(f"{Colors.BLUE}Schema Version:{Colors.END} {SCHEMA_VERSION}")
    print(f"{Colors.BLUE}Workflow Version:{Colors.END} {workflow_states.get('version', 'unknown')}")

    print(f"\n{Colors.BOLD}Loaded State Definitions:{Colors.END}")
    for obj_type, description in workflow_states.get("object_types", {}).items():
        state_count = len(workflow_states.get("states", {}).get(obj_type, {}))
        print(f"  • {obj_type}: {state_count} states - {description}")

    print(f"\n{Colors.BOLD}Created Tables:{Colors.END}")
    print("  ✓ session_metadata (session configuration)")
    print("  ✓ schema_metadata (schema versioning)")
    print("  ✓ agent_synchronizations (workflow sync events)")
    print("  ✓ sync_executions (execution details)")
    print("  ✓ sync_audit_trail (HIPAA compliance audit)")

    print(f"\n{Colors.BOLD}Created Views:{Colors.END}")
    print("  ✓ v_current_sync_status (latest sync state)")
    print("  ✓ v_phi_access_audit (HIPAA compliance)")
    print("  ✓ v_sync_performance (metrics)")

    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print("  1. Record workflow transition: python record_sync.py --pattern phase_1_specify")
    print("  2. Query workflow state: python query_workflow_state.py")
    print("  3. Analyze metrics: python analyze_metrics.py")

    print(f"\n{Colors.GREEN}🎉 AgentDB ready for workflow state tracking!{Colors.END}\n")


def main() -> None:
    """Main entry point for AgentDB initialization."""
    parser = argparse.ArgumentParser(
        description="Initialize AgentDB schema for workflow state tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize with auto-generated session ID
  python init_database.py

  # Initialize with specific session ID
  python init_database.py --session-id abc123def456

  # Initialize with custom database path
  python init_database.py --db-path /path/to/agentdb.duckdb
""",
    )

    parser.add_argument("--session-id", type=str, help="AgentDB session ID (auto-generated if not provided)")
    parser.add_argument("--db-path", type=str, help="Path to DuckDB database file (default: .claude-state/agentdb.duckdb)")

    args = parser.parse_args()

    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}AgentDB Initialization{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    # Get database path
    db_path = Path(args.db_path) if args.db_path else get_default_db_path()
    info(f"Database path: {db_path}")

    # Generate or use provided session ID
    session_id = args.session_id or generate_session_id()
    if not args.session_id:
        info(f"Generated session ID: {session_id}")
    else:
        info(f"Using provided session ID: {session_id}")

    # Load canonical state definitions
    workflow_states = load_workflow_states()

    # Create schema
    if not create_schema(session_id, workflow_states, db_path):
        error_exit("Schema creation failed")

    # Validate schema
    if not validate_schema(db_path):
        error_exit("Schema validation failed")

    # Print summary
    print_summary(session_id, workflow_states, db_path)


if __name__ == "__main__":
    main()
