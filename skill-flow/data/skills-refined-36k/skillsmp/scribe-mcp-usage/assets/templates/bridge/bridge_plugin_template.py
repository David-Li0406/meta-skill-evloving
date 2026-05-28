"""
Bridge Plugin Template

Copy this file and implement the required methods for your bridge.
"""

from typing import Dict, Any, Optional
import asyncio
import logging

from scribe_mcp.bridges import BridgePlugin, BridgeManifest, BridgeState
from scribe_mcp.bridges import get_tool_registry

logger = logging.getLogger(__name__)


class MyBridgePlugin(BridgePlugin):
    """
    Your bridge implementation.

    Replace 'MyBridgePlugin' with your bridge name (e.g., CouncilBridgePlugin).
    """

    def __init__(self, manifest: BridgeManifest):
        """
        Initialize your bridge.

        Args:
            manifest: Bridge manifest configuration
        """
        super().__init__(manifest)

        # Add your initialization here
        self._connected = False
        self._background_task: Optional[asyncio.Task] = None

    # =========================================================================
    # REQUIRED METHODS
    # =========================================================================

    async def on_activate(self) -> None:
        """
        Called when bridge transitions to ACTIVE state.

        Use this to:
        - Establish external connections
        - Initialize resources
        - Start background tasks
        - Register custom tools

        Raises:
            Exception: If activation fails, bridge will be set to ERROR state
        """
        logger.info(f"Activating bridge: {self.bridge_id}")

        # TODO: Add your activation logic
        # Example: Connect to external service
        self._connected = True

        # Example: Start background task
        # self._background_task = asyncio.create_task(self._background_loop())

        # Example: Register custom tools
        # registry = get_tool_registry()
        # registry.register_custom_tool(
        #     self.bridge_id,
        #     "my_tool",
        #     self._my_custom_tool,
        #     description="Description of my tool"
        # )

        logger.info(f"Bridge {self.bridge_id} activated successfully")

    async def on_deactivate(self) -> None:
        """
        Called when bridge transitions to INACTIVE state.

        Use this to:
        - Close external connections
        - Clean up resources
        - Stop background tasks
        - Unregister custom tools

        Must be idempotent - safe to call multiple times.
        """
        logger.info(f"Deactivating bridge: {self.bridge_id}")

        # TODO: Add your deactivation logic

        # Example: Stop background task
        if self._background_task:
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass
            self._background_task = None

        # Example: Disconnect
        self._connected = False

        # Example: Unregister tools
        # registry = get_tool_registry()
        # registry.unregister_bridge_tools(self.bridge_id)

        logger.info(f"Bridge {self.bridge_id} deactivated")

    async def health_check(self) -> Dict[str, Any]:
        """
        Return health status for monitoring.

        Must return dict with at least {"healthy": bool}.

        Recommended additional fields:
        - message: Human-readable status
        - latency_ms: Response time
        - last_error: Most recent error
        - uptime_seconds: Time since activation

        Returns:
            Dict with health status
        """
        # TODO: Implement your health check logic
        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "latency_ms": 5 if self._connected else None,
            # Add more health metrics as needed
        }

    # =========================================================================
    # OPTIONAL HOOK METHODS
    # =========================================================================

    async def pre_append(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called before entry is appended to log.

        Use this to:
        - Validate entry data
        - Enrich with metadata
        - Transform data
        - Reject invalid entries (raise exception)

        Args:
            entry_data: Entry data about to be logged

        Returns:
            Modified entry data (or original if no changes)

        Raises:
            ValueError: If entry should be rejected
        """
        # TODO: Add your pre-append logic (or remove this method)

        # Example: Add bridge metadata
        entry_data["meta"] = entry_data.get("meta", {})
        entry_data["meta"]["bridge_id"] = self.bridge_id
        entry_data["meta"]["bridge_version"] = self.manifest.version

        return entry_data

    async def post_append(self, entry_data: Dict[str, Any]) -> None:
        """
        Called after entry is successfully appended to log.

        Use this to:
        - Send notifications
        - Update external systems
        - Trigger workflows
        - Collect analytics

        Fire-and-forget - exceptions are logged but don't affect the append.

        Args:
            entry_data: Entry data that was logged
        """
        # TODO: Add your post-append logic (or remove this method)

        # Example: Log for debugging
        logger.debug(f"Entry logged: {entry_data.get('message', '')[:50]}")

    async def pre_rotate(self, log_type: str) -> None:
        """
        Called before log rotation begins.

        Use this to:
        - Archive data to external storage
        - Generate reports
        - Send summaries

        Args:
            log_type: Type of log being rotated
        """
        # TODO: Add your pre-rotate logic (or remove this method)
        logger.info(f"Pre-rotate hook for {log_type}")

    async def post_rotate(self, log_type: str, archive_path: str) -> None:
        """
        Called after log rotation completes.

        Args:
            log_type: Type of log that was rotated
            archive_path: Path to archived log file
        """
        # TODO: Add your post-rotate logic (or remove this method)
        logger.info(f"Post-rotate: {log_type} -> {archive_path}")

    async def pre_project_create(
        self,
        project_name: str,
        project_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Called before project is created.

        Use this to:
        - Validate project configuration
        - Add default metadata
        - Apply naming conventions

        Args:
            project_name: Name of project being created
            project_config: Project configuration

        Returns:
            Modified project config (or original if no changes)

        Raises:
            ValueError: If project creation should be rejected
        """
        # TODO: Add your pre-project-create logic (or remove this method)
        return project_config

    async def post_project_create(
        self,
        project_name: str,
        project_data: Dict[str, Any]
    ) -> None:
        """
        Called after project is created.

        Args:
            project_name: Name of project that was created
            project_data: Complete project data
        """
        # TODO: Add your post-project-create logic (or remove this method)
        logger.info(f"Project created: {project_name}")

    # =========================================================================
    # CUSTOM METHODS
    # =========================================================================

    # Add your custom methods here

    # async def _background_loop(self) -> None:
    #     """Example background task."""
    #     while True:
    #         try:
    #             await asyncio.sleep(60)
    #             logger.debug("Background task running...")
    #         except asyncio.CancelledError:
    #             break

    # async def _my_custom_tool(self, param1: str, param2: int = 10) -> Dict:
    #     """Example custom tool."""
    #     return {"param1": param1, "param2": param2, "result": "success"}


# =============================================================================
# REGISTRATION EXAMPLE
# =============================================================================

async def register_bridge():
    """
    Example: How to register this bridge with Scribe.
    """
    from pathlib import Path
    from scribe_mcp.bridges import BridgeRegistry
    from scribe_mcp.storage.sqlite import SQLiteStorage

    # Initialize storage
    storage = SQLiteStorage("path/to/db")
    await storage.setup()

    # Initialize registry
    registry = BridgeRegistry(storage)

    # Load manifest
    manifest = registry.load_manifest(
        Path(".scribe/config/bridges/my_bridge.yaml")
    )

    # Register with plugin class
    await registry.register_bridge(manifest, MyBridgePlugin)

    # Activate
    await registry.activate_bridge(manifest.bridge_id)

    print(f"Bridge {manifest.bridge_id} registered and activated!")


if __name__ == "__main__":
    # Run registration example
    asyncio.run(register_bridge())
