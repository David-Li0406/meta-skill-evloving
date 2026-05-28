"""WebSocket-based visualizer for the web UI.

Implements VisualizerProtocol, broadcasting orchestration events to
connected WebSocket clients. Kept in the web/ layer because it depends
on FastAPI WebSocket.
"""

import asyncio
from datetime import datetime
from typing import Callable, Optional, Set

from fastapi import WebSocket
from loguru import logger

from orchestrator.visualizers import OrchestratorState


class WebVisualizer:
    """WebSocket-based visualizer implementing VisualizerProtocol."""

    _flush_interval = 0.05  # 50ms batch interval

    def __init__(
        self,
        state: OrchestratorState,
        clients: Set[WebSocket],
        on_phase_change: Optional[Callable[[str], None]] = None,
    ):
        self.state = state
        self.clients = clients
        self._on_phase_change = on_phase_change
        # Log buffering for batch sending
        self._log_buffer: list[dict] = []
        self._log_lock = asyncio.Lock()
        self._clients_lock = asyncio.Lock()  # Protects concurrent client set modifications
        self._flush_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        """Start the log flush background task."""
        if self._running:
            return
        self._running = True
        self._flush_task = asyncio.create_task(self._flush_loop())

    async def stop(self) -> None:
        """Stop the log flush task and flush remaining logs."""
        self._running = False
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
            self._flush_task = None
        # Final flush
        await self._flush_logs()

    async def _flush_loop(self) -> None:
        """Periodically flush buffered logs."""
        while self._running:
            await asyncio.sleep(self._flush_interval)
            await self._flush_logs()

    async def _flush_logs(self) -> None:
        """Send buffered logs as a batch."""
        async with self._log_lock:
            if not self._log_buffer:
                return
            batch = self._log_buffer[:]
            self._log_buffer.clear()
        # Broadcast batch
        if batch:
            await self._broadcast("log_batch", batch)

    async def _broadcast(self, msg_type: str, data) -> None:
        """Broadcast message to all connected clients (thread-safe)."""
        message = {"type": msg_type, "data": data}
        disconnected = set()

        # Get a snapshot of clients under lock
        async with self._clients_lock:
            clients_snapshot = list(self.clients)

        # Send to all clients (without holding lock during I/O)
        for client in clients_snapshot:
            try:
                await client.send_json(message)
            except Exception as e:
                logger.debug(f"Send to client failed: {e}")
                disconnected.add(client)

        # Remove disconnected clients under lock
        if disconnected:
            async with self._clients_lock:
                self.clients -= disconnected

    async def set_workflow_phase(self, phase: str) -> None:
        """Notify the frontend of a workflow phase transition.

        This allows the engine to drive phase changes (e.g. planning → executing)
        without the service layer having to guess when transitions happen.
        """
        if self._on_phase_change:
            self._on_phase_change(phase)
        await self._broadcast("phase", {"phase": phase})

    async def set_task(self, task: str) -> None:
        """Set the current task description."""
        self.state.task = task
        self.state.start_time = datetime.now()
        self.state.is_running = True
        await self._broadcast("task", task)

    async def set_nodes(self, nodes: list[dict], phases: list) -> None:
        """Initialize with node list and phases."""
        node_data = [
            {
                "id": n["id"],
                "name": n.get("name", n["id"]),
                "purpose": n.get("purpose", ""),
                "depends_on": n.get("depends_on", []),
                "status": "pending"
            }
            for n in nodes
        ]
        self.state.nodes = node_data
        await self._broadcast("nodes", {"nodes": node_data})

    async def update_status(self, node_id: str, status: str) -> None:
        """Update node status."""
        if status == "running" and node_id not in self.state.node_times:
            self.state.node_times[node_id] = datetime.now()

        time_str = ""
        if node_id in self.state.node_times:
            elapsed = (datetime.now() - self.state.node_times[node_id]).total_seconds()
            time_str = f"{elapsed:.1f}s"

        # Update state
        for node in self.state.nodes:
            if node["id"] == node_id:
                node["status"] = status
                if time_str:
                    node["time"] = time_str
                break

        await self._broadcast("status", {
            "node_id": node_id,
            "status": status,
            "time": time_str
        })

    async def set_phase(self, phase_num: int) -> None:
        """Set current phase number."""
        self.state.current_phase = phase_num
        await self._broadcast("phase", phase_num)

    async def add_log(self, message: str, level: str = "info", node_id: Optional[str] = None) -> None:
        """Add log entry with optional node context."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        elapsed = self.state.get_elapsed()

        icons = {
            "info": "💬", "tool": "🔧", "send": "📤", "recv": "📥",
            "ok": "✅", "error": "❌", "warn": "⚠️"
        }

        log_entry = {
            "message": message,
            "level": level,
            "timestamp": timestamp,
            "elapsed": elapsed,
            "icon": icons.get(level, "•"),
            "node_id": node_id,
        }
        self.state.logs.append(log_entry)
        # Buffer log for batch sending
        async with self._log_lock:
            self._log_buffer.append(log_entry)

    async def select_plan(self, plans: list) -> int:
        """Send plans to UI and wait for user selection."""
        self.state.plans = plans
        self.state.waiting_for_selection = True
        self.state.selected_plan_index = None
        await self._broadcast("plans", {"plans": plans})

        # Wait for user selection
        while self.state.selected_plan_index is None:
            await asyncio.sleep(0.1)

        self.state.waiting_for_selection = False
        return self.state.selected_plan_index
