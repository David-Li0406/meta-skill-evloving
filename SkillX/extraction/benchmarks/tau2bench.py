"""τ²-Bench specific extraction configuration."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import json


# Default tool schemas for τ²-Bench domains
AIRLINE_TOOLS = [
    "book_reservation", "calculate", "cancel_reservation",
    "get_reservation_details", "get_user_details", "list_all_airports",
    "search_direct_flight", "search_onestop_flight", "send_certificate",
    "transfer_to_human_agents", "update_reservation_baggages",
    "update_reservation_flights", "update_reservation_passengers",
    "get_flight_status"
]

RETAIL_TOOLS = [
    "calculate", "cancel_pending_order", "exchange_delivered_order_items",
    "find_user_id_by_name_zip", "find_user_id_by_email", "get_order_details",
    "get_product_details", "get_user_details", "list_all_product_types",
    "modify_pending_order_address", "modify_pending_order_items",
    "modify_pending_order_payment", "modify_user_address",
    "return_delivered_order_items", "transfer_to_human_agents"
]

TELECOM_TOOLS = [
    "get_customer_by_phone", "get_customer_by_id", "get_customer_by_name",
    "get_details_by_id", "suspend_line", "resume_line",
    "get_bills_for_customer", "send_payment_request", "get_data_usage",
    "enable_roaming", "disable_roaming", "transfer_to_human_agents",
    "refuel_data"
]


@dataclass
class Tau2BenchExtractionConfig:
    """Configuration for τ²-Bench skill extraction."""

    # Benchmark identifier
    benchmark: str = "tau2bench"

    # Skill type (atomic/tool-centric)
    skill_type: str = "atomic"

    # Domain (airline, retail, telecom)
    domain: str = "airline"

    # Filter settings
    filter_threshold: float = 0.999

    # Extraction settings
    batch_size: int = 5
    max_concurrent: int = 3
    max_retries: int = 30

    # Tool summary settings
    max_feedback_length: int = 1500

    # Tool schemas
    tool_schemas: Dict[str, List[Dict]] = field(default_factory=dict)

    # Existing skills per domain
    existing_skills: Dict[str, Dict[str, Dict]] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize domain-specific tool lists."""
        self._domain_tools = {
            "airline": AIRLINE_TOOLS,
            "retail": RETAIL_TOOLS,
            "telecom": TELECOM_TOOLS,
        }

    def get_domain_tools(self) -> List[str]:
        """Get list of tools for current domain."""
        return self._domain_tools.get(self.domain, [])

    def is_valid_tool(self, tool_name: str) -> bool:
        """Check if tool is valid for current domain."""
        return tool_name in self.get_domain_tools()

    def load_tool_schemas(self, schemas: Dict[str, List[Dict]]) -> None:
        """Load tool schemas for all domains."""
        self.tool_schemas = schemas

    def get_tool_schema(self, tool_name: str) -> Optional[Dict]:
        """Get schema for a specific tool in current domain."""
        domain_schemas = self.tool_schemas.get(self.domain, [])
        for schema in domain_schemas:
            if schema.get("function", {}).get("name") == tool_name:
                return schema
        return None

    def load_existing_skills(self, skills_data: List[Dict]) -> None:
        """Load existing skills for current domain."""
        for item in skills_data:
            skill = item.get("skill", {})
            name = skill.get("name")
            if name:
                if self.domain not in self.existing_skills:
                    self.existing_skills[self.domain] = {}
                self.existing_skills[self.domain][name] = skill

    def get_existing_skill(self, tool_name: str) -> Optional[Dict]:
        """Get existing skill for a tool."""
        return self.existing_skills.get(self.domain, {}).get(tool_name)

    def get_missing_tools(self, used_tools: set) -> set:
        """
        Identify tools that are missing from existing skills.

        This is the key function for omission-based extraction.
        """
        existing = set(self.existing_skills.get(self.domain, {}).keys())
        return used_tools - existing
