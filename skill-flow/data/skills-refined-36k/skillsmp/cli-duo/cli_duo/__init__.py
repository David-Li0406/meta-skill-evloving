"""CLI Duo - coordinate two AI CLIs on the same repository."""
from .orchestrator import (
    create_session,
    end_session,
    get_session,
    list_registered_clis,
    list_sessions,
    register_cli,
    remove_cli,
    render_session_summary,
    swap_roles,
)

__version__ = "0.1.0"

__all__ = [
    "create_session",
    "end_session",
    "get_session",
    "list_registered_clis",
    "list_sessions",
    "register_cli",
    "remove_cli",
    "render_session_summary",
    "swap_roles",
]
