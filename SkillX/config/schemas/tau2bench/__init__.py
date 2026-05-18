"""Tau2-Bench domain tool schemas.

Complete tool schemas for airline, retail, and telecom domains.
"""

from .airline import AIRLINE_TOOL_SCHEMAS
from .retail import RETAIL_TOOL_SCHEMAS
from .telecom import TELECOM_TOOL_SCHEMAS

__all__ = [
    "AIRLINE_TOOL_SCHEMAS",
    "RETAIL_TOOL_SCHEMAS",
    "TELECOM_TOOL_SCHEMAS",
]
