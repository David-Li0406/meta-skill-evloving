"""Tool schemas for all benchmarks and domains.

Organized by benchmark:
- tau2bench: airline, retail, telecom (customer service domains)
- bfcl: 12 API domains (gorilla_file_system, math_api, etc.)
- appworld: 457 APIs across 11 apps (spotify, amazon, venmo, etc.)
"""

# Tau2-Bench schemas
from .tau2bench import (
    AIRLINE_TOOL_SCHEMAS,
    RETAIL_TOOL_SCHEMAS,
    TELECOM_TOOL_SCHEMAS,
)

# BFCL schemas
from .bfcl import BFCL_ALL_SCHEMAS

# AppWorld schemas
from .appworld import APPWORLD_TOOL_SCHEMAS, get_schema as get_appworld_schema

__all__ = [
    # Tau2-Bench
    "AIRLINE_TOOL_SCHEMAS",
    "RETAIL_TOOL_SCHEMAS",
    "TELECOM_TOOL_SCHEMAS",
    # BFCL
    "BFCL_ALL_SCHEMAS",
    # AppWorld
    "APPWORLD_TOOL_SCHEMAS",
    "get_appworld_schema",
]
