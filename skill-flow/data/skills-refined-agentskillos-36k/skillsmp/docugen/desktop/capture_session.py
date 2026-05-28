"""Interactive desktop capture session with hotkey support.

Provides the user-facing layer for desktop workflow recording. Supports
two interaction modes:

1. **Conversational** (Claude Code skill): The skill prompts the user with
   AskUserQuestion, then calls record_step() when the user reports their action.

2. **Hotkey** (standalone/background): A global keyboard listener detects a
   configurable hotkey (default: Ctrl+Shift+D) and triggers a capture event.
   The caller consumes events via wait_for_event() or poll_events().

Usage (conversational):
    session = CaptureSession(title="Change Display Settings", app_name="System Settings")
    session.start()

    # Skill prompts user, gets description
    step = session.record_step("Click Displays in sidebar", coords=(85, 320))

    data = session.finish()

Usage (hotkey):
    session = CaptureSession(title="Configure Firewall")
    session.start(use_hotkeys=True)

    # User presses Ctrl+Shift+D after each action
    event = session.wait_for_event(timeout=60)
    if event and event.type == "capture":
        step = session.record_step("User action", coords=event.coords)

    data = session.finish()
"""

import logging
import queue
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .desktop_workflow import DesktopWorkflow, WorkflowConfig, WorkflowStep

logger = logging.getLogger(__name__)

# Try importing pynput for hotkey support
try:
    from pynput import keyboard as pynput_keyboard

    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    logger.debug("pynput not available; hotkey support disabled")


class SessionState(Enum):
    """Capture session states."""

    IDLE = "idle"
    RECORDING = "recording"
    PAUSED = "paused"
    FINISHED = "finished"


class EventType(Enum):
    """Types of session events."""

    CAPTURE = "capture"
    PAUSE = "pause"
    RESUME = "resume"
    FINISH = "finish"


@dataclass
class SessionEvent:
    """An event emitted by the capture session.

    Attributes:
        type: The event type.
        timestamp: When the event occurred.
        coords: Optional mouse coordinates (for capture events).
        description: Optional action description.
    """

    type: EventType
    timestamp: float = field(default_factory=time.time)
    coords: Optional[tuple[int, int]] = None
    description: Optional[str] = None


@dataclass
class HotkeyConfig:
    """Configuration for hotkey triggers.

    Attributes:
        capture_hotkey: Key combination to trigger a capture.
        finish_hotkey: Key combination to end the session.
        pause_hotkey: Key combination to pause/resume.
    """

    capture_hotkey: str = "<ctrl>+<shift>+d"
    finish_hotkey: str = "<ctrl>+<shift>+f"
    pause_hotkey: str = "<ctrl>+<shift>+p"


def _get_mouse_position() -> tuple[int, int]:
    """Get current mouse cursor position.

    Returns:
        (x, y) screen coordinates of the cursor.
    """
    try:
        from pynput import mouse

        controller = mouse.Controller()
        pos = controller.position
        return (int(pos[0]), int(pos[1]))
    except Exception:
        return (0, 0)


class CaptureSession:
    """Interactive desktop capture session with optional hotkey triggers.

    Wraps DesktopWorkflow with event-driven interaction support. Can be
    used synchronously (record_step) or asynchronously (hotkey events).
    """

    def __init__(
        self,
        title: str,
        app_name: Optional[str] = None,
        description: Optional[str] = None,
        config: Optional[WorkflowConfig] = None,
        hotkey_config: Optional[HotkeyConfig] = None,
    ):
        """Initialize a capture session.

        Args:
            title: Workflow title for documentation.
            app_name: Target application name.
            description: Brief workflow description.
            config: Workflow configuration overrides.
            hotkey_config: Hotkey bindings configuration.
        """
        self._title = title
        self._app_name = app_name
        self._description = description
        self._workflow = DesktopWorkflow(title=title, config=config)
        self._hotkey_config = hotkey_config or HotkeyConfig()
        self._state = SessionState.IDLE
        self._events: queue.Queue[SessionEvent] = queue.Queue()
        self._hotkey_listener = None
        self._lock = threading.Lock()

    @property
    def state(self) -> SessionState:
        """Current session state."""
        return self._state

    @property
    def step_count(self) -> int:
        """Number of steps captured so far."""
        return len(self._workflow.get_steps())

    @property
    def steps(self) -> list[WorkflowStep]:
        """All captured steps."""
        return self._workflow.get_steps()

    def start(self, use_hotkeys: bool = False) -> dict:
        """Start the capture session.

        Args:
            use_hotkeys: Whether to enable global hotkey listener.

        Returns:
            Dict with session status and capabilities info.
        """
        if self._state != SessionState.IDLE:
            raise RuntimeError(f"Session already in state: {self._state.value}")

        self._workflow.start(
            app_name=self._app_name,
            description=self._description,
        )
        self._state = SessionState.RECORDING

        hotkeys_active = False
        if use_hotkeys:
            hotkeys_active = self._start_hotkey_listener()

        logger.info(
            "Capture session started: %s (hotkeys=%s)",
            self._title,
            hotkeys_active,
        )

        return {
            "status": "recording",
            "title": self._title,
            "app_name": self._app_name,
            "hotkeys_active": hotkeys_active,
            "hotkey_config": {
                "capture": self._hotkey_config.capture_hotkey,
                "finish": self._hotkey_config.finish_hotkey,
                "pause": self._hotkey_config.pause_hotkey,
            }
            if hotkeys_active
            else None,
        }

    def record_step(
        self,
        description: str,
        coords: Optional[tuple[int, int]] = None,
        force: bool = True,
    ) -> Optional[WorkflowStep]:
        """Record a step from a user action.

        This is the primary method for conversational mode. The Claude Code
        skill calls this after the user reports their action.

        Args:
            description: What the user did.
            coords: Optional click coordinates for element lookup.
            force: Whether to record even without SSIM change.

        Returns:
            WorkflowStep if recorded, None if session not recording.
        """
        if self._state != SessionState.RECORDING:
            logger.warning("Cannot record step in state: %s", self._state.value)
            return None

        return self._workflow.capture_step(
            description=description,
            click_coords=coords,
            force=force,
        )

    def add_keyboard_step(self, shortcut: str, description: Optional[str] = None) -> WorkflowStep:
        """Record a keyboard shortcut step.

        Keyboard shortcuts often don't produce visible screen changes,
        so this uses add_manual_step internally.

        Args:
            shortcut: The key combination (e.g., "Cmd+S").
            description: Optional override for the step description.

        Returns:
            WorkflowStep for the keyboard action.
        """
        if self._state != SessionState.RECORDING:
            raise RuntimeError(f"Session not recording (state={self._state.value})")

        desc = description or f"Press {shortcut}"
        return self._workflow.add_manual_step(
            description=desc,
            element={"name": shortcut, "type": "keyboard_shortcut", "source": "manual"},
        )

    def pause(self) -> None:
        """Pause the capture session."""
        if self._state != SessionState.RECORDING:
            return
        self._state = SessionState.PAUSED
        logger.info("Capture session paused")

    def resume(self) -> None:
        """Resume a paused capture session."""
        if self._state != SessionState.PAUSED:
            return
        self._state = SessionState.RECORDING
        logger.info("Capture session resumed")

    def undo_last_step(self) -> Optional[WorkflowStep]:
        """Remove and return the last captured step.

        Returns:
            The removed WorkflowStep, or None if no steps exist.
        """
        with self._lock:
            steps = self._workflow._captures
            if steps:
                removed = steps.pop()
                logger.info("Undid step %d: %s", removed.step_number, removed.description)
                return removed
            return None

    def wait_for_event(self, timeout: Optional[float] = None) -> Optional[SessionEvent]:
        """Block until a session event occurs.

        Used in hotkey mode to wait for user-triggered captures.

        Args:
            timeout: Maximum seconds to wait (None = wait forever).

        Returns:
            SessionEvent if one occurred, None on timeout.
        """
        try:
            return self._events.get(timeout=timeout)
        except queue.Empty:
            return None

    def poll_events(self) -> list[SessionEvent]:
        """Non-blocking check for pending events.

        Returns:
            List of all pending SessionEvents (may be empty).
        """
        events = []
        while not self._events.empty():
            try:
                events.append(self._events.get_nowait())
            except queue.Empty:
                break
        return events

    def finish(self) -> dict:
        """End the capture session and generate output.

        Stops hotkey listener, finalizes the workflow, and returns
        the workflow data dict ready for markdown generation.

        Returns:
            Workflow data dict with steps, metadata, and config.
        """
        self._stop_hotkey_listener()

        if self._state == SessionState.FINISHED:
            raise RuntimeError("Session already finished")

        if self._state == SessionState.IDLE:
            raise RuntimeError("Session was never started")

        result = self._workflow.finish()
        self._state = SessionState.FINISHED
        logger.info("Capture session finished: %d steps", self.step_count)
        return result

    def get_status(self) -> dict:
        """Get current session status for display.

        Returns:
            Dict with state, step count, and timing info.
        """
        return {
            "state": self._state.value,
            "title": self._title,
            "app_name": self._app_name,
            "steps_captured": self.step_count,
            "hotkeys_active": self._hotkey_listener is not None,
        }

    def get_action_prompt(self) -> dict:
        """Generate AskUserQuestion data for the next action prompt.

        Returns a dict matching the AskUserQuestion tool schema that
        the Claude Code skill can use directly.

        Returns:
            Dict with question, header, options for AskUserQuestion.
        """
        step_num = self.step_count + 1
        return {
            "questions": [
                {
                    "question": f"Step {step_num}: What action will you perform next on the desktop?",
                    "header": "Next action",
                    "multiSelect": False,
                    "options": [
                        {
                            "label": "Click an element",
                            "description": "I'll click a button, menu item, or other UI element",
                        },
                        {
                            "label": "Type text",
                            "description": "I'll type into a text field or search box",
                        },
                        {
                            "label": "Keyboard shortcut",
                            "description": "I'll use a keyboard shortcut (e.g., Cmd+S)",
                        },
                        {
                            "label": "Done recording",
                            "description": "I've completed all the steps in this workflow",
                        },
                    ],
                }
            ]
        }

    def get_element_prompt(self) -> dict:
        """Generate AskUserQuestion for element identification after action.

        Returns:
            Dict with question, header, options for AskUserQuestion.
        """
        return {
            "questions": [
                {
                    "question": "Where did you click? Describe the element or provide coordinates.",
                    "header": "Element",
                    "multiSelect": False,
                    "options": [
                        {
                            "label": "I'll describe it",
                            "description": "Let me tell you what I clicked on",
                        },
                        {
                            "label": "Auto-detect",
                            "description": "Use accessibility/vision to identify the element",
                        },
                    ],
                }
            ]
        }

    # --- Hotkey listener internals ---

    def _start_hotkey_listener(self) -> bool:
        """Start the global hotkey listener.

        Returns:
            True if listener started successfully, False if pynput unavailable.
        """
        if not HAS_PYNPUT:
            logger.warning("pynput not available; hotkey support disabled")
            return False

        try:
            hotkeys = {
                self._hotkey_config.capture_hotkey: self._on_capture_hotkey,
                self._hotkey_config.finish_hotkey: self._on_finish_hotkey,
                self._hotkey_config.pause_hotkey: self._on_pause_hotkey,
            }
            self._hotkey_listener = pynput_keyboard.GlobalHotKeys(hotkeys)
            self._hotkey_listener.start()
            logger.info(
                "Hotkey listener started (capture=%s, finish=%s, pause=%s)",
                self._hotkey_config.capture_hotkey,
                self._hotkey_config.finish_hotkey,
                self._hotkey_config.pause_hotkey,
            )
            return True
        except Exception as e:
            logger.error("Failed to start hotkey listener: %s", e)
            self._hotkey_listener = None
            return False

    def _stop_hotkey_listener(self) -> None:
        """Stop the global hotkey listener."""
        if self._hotkey_listener:
            try:
                self._hotkey_listener.stop()
            except Exception:
                pass
            self._hotkey_listener = None
            logger.debug("Hotkey listener stopped")

    def _on_capture_hotkey(self) -> None:
        """Handle capture hotkey press."""
        if self._state != SessionState.RECORDING:
            return

        coords = _get_mouse_position()
        event = SessionEvent(
            type=EventType.CAPTURE,
            coords=coords,
        )
        self._events.put(event)
        logger.debug("Capture hotkey pressed at coords=(%d, %d)", coords[0], coords[1])

    def _on_finish_hotkey(self) -> None:
        """Handle finish hotkey press."""
        event = SessionEvent(type=EventType.FINISH)
        self._events.put(event)
        logger.debug("Finish hotkey pressed")

    def _on_pause_hotkey(self) -> None:
        """Handle pause/resume hotkey press."""
        if self._state == SessionState.RECORDING:
            self.pause()
            self._events.put(SessionEvent(type=EventType.PAUSE))
        elif self._state == SessionState.PAUSED:
            self.resume()
            self._events.put(SessionEvent(type=EventType.RESUME))
