"""Desktop workflow orchestration for DocuGen.

Ties together capture, step detection, element metadata, and markdown
generation into a cohesive workflow runner for desktop applications.

Usage:
    from docugen.desktop.desktop_workflow import DesktopWorkflow

    workflow = DesktopWorkflow(title="Configure Display Settings")
    workflow.start(app_name="System Settings")

    # User performs action, then calls:
    workflow.capture_step(description="Click Displays")

    # When done:
    result = workflow.finish()
    # result contains workflow_data dict ready for generate_markdown

Pipeline:
    1. Initialize capture (mss) + optional accessibility backend
    2. For each user action:
       a. Capture before screenshot
       b. Wait for user action
       c. Capture after screenshot
       d. SSIM comparison for step boundary detection
       e. Query accessibility/vision for element metadata
    3. Generate workflow JSON via workflow_adapter
    4. Produce markdown via generate_markdown
"""

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .capture import ScreenCapture
from .mode_detection import detect_mode
from .platform_router import get_accessibility_backend, get_element_metadata
from .step_detector import DetectorConfig, StepDetector, StepRecord
from .workflow_adapter import detector_to_workflow_data, save_workflow_json

logger = logging.getLogger(__name__)


@dataclass
class WorkflowConfig:
    """Configuration for a desktop workflow capture session.

    Attributes:
        ssim_threshold: SSIM threshold for step detection (lower = more sensitive).
        debounce_ms: Minimum milliseconds between captures.
        output_dir: Directory for screenshots and output.
        capture_window: If set, capture only this window title (else fullscreen).
        include_frontmatter: Whether to include YAML frontmatter in markdown.
    """

    ssim_threshold: float = 0.87
    debounce_ms: int = 300
    output_dir: str = "./docugen_output"
    capture_window: Optional[str] = None
    include_frontmatter: bool = True


@dataclass
class WorkflowStep:
    """Result of a single step capture.

    Attributes:
        step_number: Sequential step number.
        description: User-provided action description.
        before_path: Path to screenshot before action.
        after_path: Path to screenshot after action.
        ssim_score: Visual similarity between before/after.
        element: Element metadata dict (from accessibility or vision).
        timestamp: Capture timestamp.
        is_significant: Whether SSIM detected meaningful change.
    """

    step_number: int
    description: str
    before_path: str
    after_path: str
    ssim_score: float
    element: Optional[dict] = None
    timestamp: float = 0.0
    is_significant: bool = True


class DesktopWorkflow:
    """Orchestrates desktop workflow documentation capture.

    Manages the lifecycle of a desktop recording session: initialization,
    step capture with SSIM detection, element metadata extraction, and
    final markdown generation.
    """

    def __init__(self, title: str, config: Optional[WorkflowConfig] = None):
        """Initialize a desktop workflow session.

        Args:
            title: Workflow title for the generated documentation.
            config: Optional configuration overrides.
        """
        self.title = title
        self.config = config or WorkflowConfig()
        self._capture = ScreenCapture()
        self._detector = StepDetector(
            config=DetectorConfig(desktop_threshold=self.config.ssim_threshold)
        )
        self._accessibility = get_accessibility_backend()
        self._output_dir = Path(self.config.output_dir)
        self._images_dir = self._output_dir / "images"
        self._started = False
        self._app_name: Optional[str] = None
        self._description: Optional[str] = None
        self._last_capture_time: float = 0.0
        self._captures: list[WorkflowStep] = []

    def start(
        self,
        app_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """Start the workflow recording session.

        Creates output directories and initializes capture state.

        Args:
            app_name: Name of the application being documented.
            description: Brief description of the workflow.
        """
        self._app_name = app_name
        self._description = description
        self._images_dir.mkdir(parents=True, exist_ok=True)
        self._started = True
        logger.info(
            "Desktop workflow started: %s (app: %s)", self.title, app_name or "any"
        )

    def capture_step(
        self,
        description: str,
        click_coords: Optional[tuple[int, int]] = None,
        force: bool = False,
    ) -> Optional[WorkflowStep]:
        """Capture a single workflow step.

        Takes before/after screenshots via StepDetector, runs SSIM comparison,
        and extracts element metadata from accessibility APIs or visual analysis.

        Args:
            description: Description of the action being performed.
            click_coords: Optional (x, y) of where the user clicked.
            force: If True, record step even if SSIM shows no change.

        Returns:
            WorkflowStep if step was recorded, None if debounced or
            no significant change detected (and force=False).
        """
        if not self._started:
            raise RuntimeError("Call start() before capturing steps")

        # Debounce check
        now = time.time()
        elapsed_ms = (now - self._last_capture_time) * 1000
        if elapsed_ms < self.config.debounce_ms and not force:
            logger.debug("Debounced capture (%.0fms < %dms)", elapsed_ms, self.config.debounce_ms)
            return None

        step_num = len(self._captures) + 1

        # Use StepDetector's capture API
        self._detector.capture_before()

        if force:
            record = self._detector.record_manual_step(description=description)
        else:
            record = self._detector.capture_after(description=description)

        if record is None and not force:
            logger.debug("Step %d skipped: no significant change detected", step_num)
            return None

        ssim_score = record.ssim_score if record else 0.0
        before_path = record.before_capture.path if record else ""
        after_path = record.after_capture.path if record else ""

        # Get element metadata
        element = None
        if click_coords:
            x, y = click_coords
            element = get_element_metadata(x, y, screenshot_path=after_path)

        self._last_capture_time = time.time()

        result = WorkflowStep(
            step_number=step_num,
            description=description,
            before_path=before_path,
            after_path=after_path,
            ssim_score=ssim_score,
            element=element,
            timestamp=now,
            is_significant=True,
        )
        self._captures.append(result)

        logger.info(
            "Captured step %d: %s (SSIM=%.3f, element=%s)",
            step_num, description, ssim_score,
            element.get("title", "none") if element else "none",
        )
        return result

    def add_manual_step(
        self,
        description: str,
        screenshot_path: Optional[str] = None,
        element: Optional[dict] = None,
    ) -> WorkflowStep:
        """Add a manually triggered step without SSIM detection.

        Useful for actions that don't produce visible screen changes
        (e.g., keyboard shortcuts, hover states).

        Args:
            description: Description of the action.
            screenshot_path: Optional path to an existing screenshot.
            element: Optional pre-extracted element metadata.

        Returns:
            WorkflowStep for the manual step.
        """
        if not self._started:
            raise RuntimeError("Call start() before adding steps")

        step_num = len(self._captures) + 1

        # Capture current screen if no screenshot provided
        if not screenshot_path:
            screenshot_path = str(self._images_dir / f"step-{step_num:02d}-manual.png")
            self._capture.capture_fullscreen(output_path=screenshot_path)

        result = WorkflowStep(
            step_number=step_num,
            description=description,
            before_path=screenshot_path,
            after_path=screenshot_path,
            ssim_score=0.0,
            element=element,
            timestamp=time.time(),
            is_significant=True,
        )
        self._captures.append(result)
        logger.info("Added manual step %d: %s", step_num, description)
        return result

    def get_steps(self) -> list[WorkflowStep]:
        """Get all captured steps.

        Returns:
            List of WorkflowStep instances.
        """
        return list(self._captures)

    def finish(self) -> dict:
        """Finish the workflow and generate output data.

        Produces the workflow_data dict suitable for generate_markdown.

        Returns:
            Workflow data dict with title, steps, platform info, etc.
        """
        if not self._started:
            raise RuntimeError("Call start() before finishing")

        workflow_data = detector_to_workflow_data(
            detector=self._detector,
            title=self.title,
            description=self._description or "",
            app_name=self._app_name or "",
        )

        # Enrich with desktop-specific metadata
        workflow_data["mode"] = "desktop"
        workflow_data["config"] = {
            "ssim_threshold": self.config.ssim_threshold,
            "debounce_ms": self.config.debounce_ms,
        }

        self._started = False
        logger.info(
            "Workflow finished: %s (%d steps)", self.title, len(self._captures)
        )
        return workflow_data

    def save(self, output_path: Optional[str] = None) -> Path:
        """Finish workflow and save JSON to disk.

        Args:
            output_path: Optional path for the JSON file.
                Defaults to output_dir/workflow.json.

        Returns:
            Path to the saved JSON file.
        """
        workflow_data = self.finish()
        path = output_path or str(self._output_dir / "workflow.json")
        return save_workflow_json(workflow_data, path)
