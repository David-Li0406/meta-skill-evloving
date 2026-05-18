"""BFCL-specific extraction configuration."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import json


@dataclass
class BFCLExtractionConfig:
    """Configuration for BFCL skill extraction."""

    # Benchmark identifier
    benchmark: str = "bfcl"

    # Skill type
    skill_type: str = "functional"

    # Filter settings
    filter_threshold: float = 0.999

    # Extraction settings
    batch_size: int = 10
    max_concurrent: int = 5
    max_retries: int = 5

    # Tool summary settings
    max_feedback_length: int = 1500

    # Plan format
    plan_step_prefix: str = "# step"

    # Tool schemas path (for tool-schema validation)
    tool_schemas_path: Optional[str] = None

    # Loaded tool schemas
    tool_schemas: Dict[str, Any] = field(default_factory=dict)

    def load_tool_schemas(self, path: str) -> None:
        """Load tool schemas from file."""
        with open(path, "r", encoding="utf-8") as f:
            self.tool_schemas = json.load(f)
        self.tool_schemas_path = path

    def get_tool_schema(self, tool_name: str) -> Optional[Dict]:
        """Get schema for a specific tool."""
        return self.tool_schemas.get(tool_name)

    def validate_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> tuple:
        """
        Validate a tool call against its schema.

        Returns:
            Tuple of (is_valid, error_message)
        """
        schema = self.get_tool_schema(tool_name)
        if not schema:
            return (True, None)  # No schema, assume valid

        # Check required parameters
        if "parameters" in schema:
            params_schema = schema["parameters"]
            required = params_schema.get("required", [])

            for param in required:
                if param not in arguments:
                    return (False, f"Missing required parameter: {param}")

        return (True, None)
