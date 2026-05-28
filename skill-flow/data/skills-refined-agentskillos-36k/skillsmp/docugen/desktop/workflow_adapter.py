"""Adapter converting StepDetector output to markdown generator input format.

Bridges the capture pipeline (StepDetector → StepRecord objects) with the
documentation pipeline (generate_markdown.py's JSON format).
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from .step_detector import StepDetector, StepRecord, DetectorConfig
from .platform_utils import get_platform

logger = logging.getLogger(__name__)


def steps_to_workflow_data(
    steps: list[StepRecord],
    title: str = "Desktop Workflow",
    description: str = "",
    app_name: str = "",
    image_dir: Optional[Path] = None,
) -> dict:
    """Convert StepRecord objects to generate_markdown.py's expected format.

    Args:
        steps: List of StepRecord objects from StepDetector.
        title: Workflow title.
        description: Workflow description.
        app_name: Application name being documented.
        image_dir: Directory where step screenshots are saved.
            If None, uses relative paths like "./images/step-NN-after.png".

    Returns:
        Dictionary matching generate_markdown.py's input schema.
    """
    platform = get_platform()

    workflow = {
        "title": title,
        "description": description,
        "mode": "desktop",
        "app_name": app_name,
        "platform": {
            "os": platform.os_type,
            "dpi_scale": platform.dpi_scale,
        },
        "prerequisites": [],
        "steps": [],
        "troubleshooting": [],
    }

    for step in steps:
        image_path = _resolve_image_path(step, image_dir)

        step_data = {
            "number": step.step_number,
            "title": step.description or f"Step {step.step_number}",
            "description": step.description,
            "screenshot": str(image_path),
            "expected_result": "",
            "mode": "desktop",
            "app_name": app_name,
            "ssim_score": step.ssim_score,
            "timestamp": datetime.fromtimestamp(step.timestamp).isoformat(),
        }

        if step.element_metadata:
            step_data["element"] = step.element_metadata

        workflow["steps"].append(step_data)

    return workflow


def detector_to_workflow_data(
    detector: StepDetector,
    title: str = "Desktop Workflow",
    description: str = "",
    app_name: str = "",
) -> dict:
    """Convert a StepDetector's recorded steps to workflow data.

    Convenience wrapper around steps_to_workflow_data that extracts
    steps and output_dir from the detector.

    Args:
        detector: StepDetector with recorded steps.
        title: Workflow title.
        description: Workflow description.
        app_name: Application name.

    Returns:
        Dictionary matching generate_markdown.py's input schema.
    """
    return steps_to_workflow_data(
        steps=detector.steps,
        title=title,
        description=description,
        app_name=app_name,
        image_dir=detector.config.output_dir,
    )


def save_workflow_json(
    workflow_data: dict,
    output_path: Path,
) -> Path:
    """Save workflow data as JSON for generate_markdown.py consumption.

    Args:
        workflow_data: Workflow dictionary from steps_to_workflow_data.
        output_path: Path to write the JSON file.

    Returns:
        The output path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(workflow_data, indent=2))
    logger.info("Saved workflow data: %s", output_path)
    return output_path


def _resolve_image_path(step: StepRecord, image_dir: Optional[Path]) -> str:
    """Resolve the image path for a step's screenshot."""
    if image_dir:
        return str(image_dir / f"step-{step.step_number:02d}-after.png")
    return f"./images/step-{step.step_number:02d}-after.png"
