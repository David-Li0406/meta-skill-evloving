"""Unified tool schema registry for all benchmarks and domains.

Tool schemas follow the OpenAPI-style function calling format:
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "Tool description",
        "parameters": {
            "properties": {...},
            "required": [...],
            "type": "object"
        }
    }
}

Supported benchmarks and domains:
- tau2bench: airline, retail, telecom
- bfcl: gorilla_file_system, math_api, memory_kv, memory_rec_sum,
        memory_vector, message_api, posting_api, ticket_api,
        trading_bot, travel_booking, vehicle_control, web_search
- appworld: 457 APIs across 11 apps
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Type alias for tool schema
ToolSchema = Dict[str, Any]


class ToolSchemaRegistry:
    """
    Centralized registry for tool schemas across all domains.

    Supports:
    - Domain-specific schemas (airline, retail, telecom)
    - Benchmark-specific schemas (appworld, bfcl, tau2bench)

    Usage:
        # Register schemas
        ToolSchemaRegistry.register("airline", AIRLINE_SCHEMAS)

        # Get specific tool schema
        schema = ToolSchemaRegistry.get("airline", "get_user_details")

        # Get all schemas for a domain
        all_schemas = ToolSchemaRegistry.get_all("airline")
    """

    _schemas: Dict[str, Dict[str, ToolSchema]] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, domain: str, schemas: List[ToolSchema]) -> None:
        """
        Register tool schemas for a domain.

        Args:
            domain: Domain name (airline, retail, telecom, appworld, etc.)
            schemas: List of tool schemas in OpenAPI function format
        """
        if domain not in cls._schemas:
            cls._schemas[domain] = {}

        for schema in schemas:
            if "function" in schema:
                name = schema["function"]["name"]
                cls._schemas[domain][name] = schema
            else:
                logger.warning(f"Invalid schema format (missing 'function' key): {schema}")

        logger.info(f"Registered {len(schemas)} tool schemas for domain '{domain}'")

    @classmethod
    def get(cls, domain: str, tool_name: str) -> Optional[ToolSchema]:
        """
        Get schema for a specific tool in a domain.

        Args:
            domain: Domain name
            tool_name: Tool name

        Returns:
            Tool schema if found, None otherwise
        """
        cls._ensure_initialized()
        return cls._schemas.get(domain, {}).get(tool_name)

    @classmethod
    def get_all(cls, domain: str) -> Dict[str, ToolSchema]:
        """
        Get all schemas for a domain.

        Args:
            domain: Domain name

        Returns:
            Dictionary mapping tool names to their schemas
        """
        cls._ensure_initialized()
        return cls._schemas.get(domain, {})

    @classmethod
    def get_tool_names(cls, domain: str) -> List[str]:
        """
        Get all tool names for a domain.

        Args:
            domain: Domain name

        Returns:
            List of tool names
        """
        cls._ensure_initialized()
        return list(cls._schemas.get(domain, {}).keys())

    @classmethod
    def list_domains(cls) -> List[str]:
        """List all registered domains."""
        cls._ensure_initialized()
        return list(cls._schemas.keys())

    @classmethod
    def has_domain(cls, domain: str) -> bool:
        """Check if a domain has registered schemas."""
        cls._ensure_initialized()
        return domain in cls._schemas

    @classmethod
    def clear(cls) -> None:
        """Clear all registered schemas."""
        cls._schemas = {}
        cls._initialized = False

    @classmethod
    def _ensure_initialized(cls) -> None:
        """Ensure all built-in schemas are loaded."""
        if cls._initialized:
            return

        try:
            # Load Tau2-Bench schemas
            from .schemas.tau2bench import (
                AIRLINE_TOOL_SCHEMAS,
                RETAIL_TOOL_SCHEMAS,
                TELECOM_TOOL_SCHEMAS,
            )

            if AIRLINE_TOOL_SCHEMAS:
                cls.register("airline", AIRLINE_TOOL_SCHEMAS)
            if RETAIL_TOOL_SCHEMAS:
                cls.register("retail", RETAIL_TOOL_SCHEMAS)
            if TELECOM_TOOL_SCHEMAS:
                cls.register("telecom", TELECOM_TOOL_SCHEMAS)

        except ImportError as e:
            logger.warning(f"Could not load tau2bench schemas: {e}")

        try:
            # Load BFCL schemas
            from .schemas.bfcl import BFCL_ALL_SCHEMAS

            for domain, schemas in BFCL_ALL_SCHEMAS.items():
                if schemas:
                    cls.register(f"bfcl_{domain}", schemas)

        except ImportError as e:
            logger.warning(f"Could not load bfcl schemas: {e}")

        try:
            # Load AppWorld schemas
            from .schemas.appworld import APPWORLD_TOOL_SCHEMAS

            if APPWORLD_TOOL_SCHEMAS:
                cls.register("appworld", APPWORLD_TOOL_SCHEMAS)

        except ImportError as e:
            logger.warning(f"Could not load appworld schemas: {e}")

        cls._initialized = True


def load_schemas_from_file(filepath: str, domain: str) -> None:
    """
    Load tool schemas from a JSON file and register them.

    Args:
        filepath: Path to JSON file containing tool schemas
        domain: Domain name to register under
    """
    import json

    with open(filepath, "r", encoding="utf-8") as f:
        schemas = json.load(f)

    if isinstance(schemas, list):
        ToolSchemaRegistry.register(domain, schemas)
    elif isinstance(schemas, dict) and "tools" in schemas:
        ToolSchemaRegistry.register(domain, schemas["tools"])
    elif isinstance(schemas, dict):
        # Dict format with tool names as keys
        ToolSchemaRegistry.register(domain, list(schemas.values()))
    else:
        raise ValueError(f"Invalid schema file format: {filepath}")
