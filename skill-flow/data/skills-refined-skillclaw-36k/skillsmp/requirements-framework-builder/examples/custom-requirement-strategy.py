"""
Example: Custom Requirement Strategy

This example shows how to create a custom requirement strategy
for the Requirements Framework.

To add this strategy:
1. Place this file in ~/.claude/hooks/lib/
2. Register in strategy_registry.py
3. Configure in requirements.yaml
"""

from typing import Any, Dict, Optional
from base_strategy import BaseStrategy


class CustomTimeLimitStrategy(BaseStrategy):
    """
    Example strategy: Time-limited requirement.

    This requirement must be satisfied within a time window
    (e.g., work hours only, or within X hours of starting).

    Configuration example:
    ```yaml
    requirements:
      work_hours_only:
        enabled: true
        type: time_limit
        start_hour: 9
        end_hour: 17
        timezone: "America/New_York"
        message: "This project is only accessible during work hours"
    ```
    """

    def is_satisfied(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str
    ) -> bool:
        """
        Check if current time is within allowed hours.

        Args:
            requirement: The requirement configuration
            state: Current state for this branch
            session_id: Current session ID

        Returns:
            True if within allowed hours, False otherwise
        """
        import datetime

        # Get configuration
        start_hour = requirement.get('start_hour', 0)
        end_hour = requirement.get('end_hour', 24)

        # Get current hour
        now = datetime.datetime.now()
        current_hour = now.hour

        # Check if within allowed hours
        return start_hour <= current_hour < end_hour

    def satisfy(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str,
        **kwargs
    ) -> None:
        """
        Time-based requirements can't be manually satisfied.
        This is a no-op for this strategy.
        """
        # Time-based requirements are auto-evaluated
        # Manual satisfaction doesn't apply
        pass

    def get_message(
        self,
        requirement: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """
        Get the blocking message for this requirement.

        Args:
            requirement: The requirement configuration
            context: Additional context (session, branch, etc.)

        Returns:
            Formatted message string
        """
        start_hour = requirement.get('start_hour', 0)
        end_hour = requirement.get('end_hour', 24)

        custom_message = requirement.get('message', '')
        if custom_message:
            return custom_message

        return f"""🕐 **Time Restriction Active**

This project is only accessible between {start_hour}:00 and {end_hour}:00.

Current time is outside the allowed window.
"""

    def clear(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str
    ) -> None:
        """
        Clear satisfaction for this requirement.
        No-op for time-based requirements.
        """
        pass


class CustomEnvironmentStrategy(BaseStrategy):
    """
    Example strategy: Environment-based requirement.

    Requires specific environment variables or conditions.

    Configuration example:
    ```yaml
    requirements:
      production_check:
        enabled: true
        type: environment
        required_vars:
          - AWS_PROFILE
          - DATABASE_URL
        forbidden_vars:
          - DEBUG
        message: "Production environment not configured"
    ```
    """

    def is_satisfied(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str
    ) -> bool:
        """Check if environment meets requirements."""
        import os

        required_vars = requirement.get('required_vars', [])
        forbidden_vars = requirement.get('forbidden_vars', [])

        # Check required vars exist
        for var in required_vars:
            if not os.environ.get(var):
                return False

        # Check forbidden vars don't exist
        for var in forbidden_vars:
            if os.environ.get(var):
                return False

        return True

    def satisfy(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str,
        **kwargs
    ) -> None:
        """Environment requirements are auto-evaluated."""
        pass

    def get_message(
        self,
        requirement: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Get blocking message."""
        import os

        required_vars = requirement.get('required_vars', [])
        forbidden_vars = requirement.get('forbidden_vars', [])

        missing = [v for v in required_vars if not os.environ.get(v)]
        present = [v for v in forbidden_vars if os.environ.get(v)]

        custom_message = requirement.get('message', '')
        if custom_message:
            return custom_message

        parts = ["🌍 **Environment Check Failed**\n"]

        if missing:
            parts.append(f"Missing required variables: {', '.join(missing)}")

        if present:
            parts.append(f"Forbidden variables present: {', '.join(present)}")

        return "\n".join(parts)

    def clear(
        self,
        requirement: Dict[str, Any],
        state: Dict[str, Any],
        session_id: str
    ) -> None:
        """Environment requirements can't be cleared."""
        pass


# To register these strategies, add to strategy_registry.py:
#
# from time_limit_strategy import CustomTimeLimitStrategy
# from environment_strategy import CustomEnvironmentStrategy
#
# STRATEGIES = {
#     'blocking': BlockingStrategy,
#     'dynamic': DynamicStrategy,
#     'guard': GuardStrategy,
#     'time_limit': CustomTimeLimitStrategy,
#     'environment': CustomEnvironmentStrategy,
# }
