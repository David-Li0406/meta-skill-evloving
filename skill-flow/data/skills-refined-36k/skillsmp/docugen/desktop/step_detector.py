"""Desktop workflow step detection via SSIM-based visual change analysis.

Integrates the ScreenCapture infrastructure with SSIM comparison to
automatically detect meaningful steps during desktop workflow recording.
"""

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .capture import ScreenCapture, CaptureResult

logger = logging.getLogger(__name__)


@dataclass
class StepRecord:
    """A recorded workflow step with before/after captures."""

    step_number: int
    before_capture: CaptureResult
    after_capture: CaptureResult
    ssim_score: float
    timestamp: float
    description: str = ""
    element_metadata: Optional[dict] = None
    detection_method: str = "ssim"  # 'ssim' or 'manual'


@dataclass
class DetectorConfig:
    """Configuration for the step detector."""

    ssim_threshold: float = 0.90
    desktop_threshold: float = 0.87
    debounce_seconds: float = 0.3
    mode: str = "desktop"  # 'desktop' or 'web'
    output_dir: Optional[Path] = None

    @property
    def effective_threshold(self) -> float:
        """Return the threshold to use based on mode."""
        if self.mode == "desktop":
            return self.desktop_threshold
        return self.ssim_threshold


class StepDetector:
    """Detects workflow step boundaries using SSIM visual comparison.

    Captures before/after screenshots and uses Structural Similarity
    Index to determine if a meaningful UI change occurred.

    Usage:
        detector = StepDetector()
        detector.capture_before()
        # ... user performs action ...
        step = detector.capture_after()
        if step:
            print(f"Step {step.step_number} detected (SSIM: {step.ssim_score:.3f})")
    """

    def __init__(self, config: Optional[DetectorConfig] = None):
        self._config = config or DetectorConfig()
        self._capture = ScreenCapture()
        self._steps: list[StepRecord] = []
        self._before: Optional[CaptureResult] = None
        self._last_step_time: float = 0
        self._window_id: Optional[int] = None

    @property
    def config(self) -> DetectorConfig:
        return self._config

    @property
    def steps(self) -> list[StepRecord]:
        return list(self._steps)

    @property
    def step_count(self) -> int:
        return len(self._steps)

    def set_target_window(self, window_id: int) -> None:
        """Set a specific window to capture instead of fullscreen."""
        self._window_id = window_id

    def capture_before(self) -> CaptureResult:
        """Take the 'before' screenshot for comparison.

        Returns:
            The CaptureResult of the before screenshot.
        """
        self._before = self._take_screenshot()
        return self._before

    def capture_after(self, description: str = "") -> Optional[StepRecord]:
        """Take the 'after' screenshot and compare with 'before'.

        Applies debouncing and SSIM thresholding to determine if this
        represents a meaningful workflow step.

        Args:
            description: Human-readable description of the action taken.

        Returns:
            StepRecord if a significant change was detected, None otherwise.
        """
        if self._before is None:
            logger.warning("capture_after called without capture_before")
            self._before = self._take_screenshot()
            return None

        # Debounce check
        now = time.time()
        if now - self._last_step_time < self._config.debounce_seconds:
            logger.debug("Debounced: too soon since last step")
            return None

        after = self._take_screenshot()
        ssim_score = self._compare(self._before, after)

        threshold = self._config.effective_threshold
        is_step = ssim_score < threshold

        logger.debug(
            "SSIM %.4f (threshold %.2f) → %s",
            ssim_score, threshold, "STEP" if is_step else "skip"
        )

        if is_step:
            step = StepRecord(
                step_number=self.step_count + 1,
                before_capture=self._before,
                after_capture=after,
                ssim_score=ssim_score,
                timestamp=now,
                description=description,
            )
            self._steps.append(step)
            self._last_step_time = now

            # Save screenshots if output_dir configured
            if self._config.output_dir:
                self._save_step(step)

            # Advance: the 'after' becomes the next 'before'
            self._before = after
            return step

        # No significant change; keep current 'before'
        return None

    def record_manual_step(self, description: str = "") -> StepRecord:
        """Force-record a step regardless of SSIM score.

        Useful for manual triggers where the user explicitly marks a step.

        Args:
            description: Human-readable description of the action.

        Returns:
            The recorded StepRecord.
        """
        if self._before is None:
            self._before = self._take_screenshot()

        after = self._take_screenshot()
        ssim_score = self._compare(self._before, after)

        step = StepRecord(
            step_number=self.step_count + 1,
            before_capture=self._before,
            after_capture=after,
            ssim_score=ssim_score,
            timestamp=time.time(),
            description=description,
            detection_method="manual",
        )
        self._steps.append(step)
        self._last_step_time = time.time()

        if self._config.output_dir:
            self._save_step(step)

        self._before = after
        return step

    def delete_step(self, step_number: int) -> bool:
        """Delete a recorded step by its step number.

        Remaining steps are renumbered to maintain sequence.

        Args:
            step_number: The 1-based step number to delete.

        Returns:
            True if step was found and deleted, False otherwise.
        """
        idx = step_number - 1
        if idx < 0 or idx >= len(self._steps):
            logger.warning("delete_step: step %d not found", step_number)
            return False

        self._steps.pop(idx)
        # Renumber remaining steps
        for i, step in enumerate(self._steps):
            step.step_number = i + 1

        return True

    def merge_steps(self, step_num1: int, step_num2: int) -> Optional[StepRecord]:
        """Merge two consecutive steps into one.

        The merged step keeps the first step's before_capture and
        the second step's after_capture. SSIM is recalculated for
        the merged pair.

        Args:
            step_num1: First step number (1-based).
            step_num2: Second step number (1-based), must be step_num1 + 1.

        Returns:
            The merged StepRecord, or None if merge is invalid.
        """
        if step_num2 != step_num1 + 1:
            logger.warning("merge_steps: steps must be consecutive")
            return None

        idx1 = step_num1 - 1
        idx2 = step_num2 - 1
        if idx1 < 0 or idx2 >= len(self._steps):
            logger.warning("merge_steps: step numbers out of range")
            return None

        s1 = self._steps[idx1]
        s2 = self._steps[idx2]

        ssim_score = self._compare(s1.before_capture, s2.after_capture)

        merged = StepRecord(
            step_number=step_num1,
            before_capture=s1.before_capture,
            after_capture=s2.after_capture,
            ssim_score=ssim_score,
            timestamp=s2.timestamp,
            description=s1.description or s2.description,
            detection_method="merged",
        )

        # Replace the pair with the merged step
        self._steps[idx1] = merged
        self._steps.pop(idx2)

        # Renumber
        for i, step in enumerate(self._steps):
            step.step_number = i + 1

        return merged

    def redetect(self, threshold: Optional[float] = None) -> list[StepRecord]:
        """Re-evaluate stored steps against a new threshold.

        Filters the existing steps based on the new threshold without
        re-capturing screenshots. Steps whose SSIM score is above the
        new threshold are removed (considered insignificant).

        Args:
            threshold: New SSIM threshold. If None, uses current config.

        Returns:
            List of steps that were removed (no longer significant).
        """
        if threshold is not None:
            if self._config.mode == "desktop":
                self._config.desktop_threshold = threshold
            else:
                self._config.ssim_threshold = threshold

        effective = self._config.effective_threshold
        removed = []
        kept = []

        for step in self._steps:
            if step.detection_method == "manual":
                # Manual steps are always kept
                kept.append(step)
            elif step.ssim_score >= effective:
                removed.append(step)
            else:
                kept.append(step)

        self._steps = kept
        # Renumber
        for i, step in enumerate(self._steps):
            step.step_number = i + 1

        logger.info(
            "Redetect: kept %d steps, removed %d (threshold=%.3f)",
            len(kept), len(removed), effective
        )
        return removed

    def reset(self) -> None:
        """Reset the detector state, clearing all recorded steps."""
        self._steps.clear()
        self._before = None
        self._last_step_time = 0

    def _take_screenshot(self) -> CaptureResult:
        """Take a screenshot using the configured capture method."""
        if self._window_id is not None:
            return self._capture.window(self._window_id)
        return self._capture.fullscreen()

    def _compare(self, before: CaptureResult, after: CaptureResult) -> float:
        """Compute SSIM between two CaptureResults.

        Uses the existing detect_step module for SSIM calculation.
        Falls back to a simple byte comparison if scikit-image unavailable.
        """
        try:
            from skimage.metrics import structural_similarity as ssim
            from PIL import Image
            import numpy as np
            import io

            before_img = Image.open(io.BytesIO(before.image_bytes)).convert("L")
            after_img = Image.open(io.BytesIO(after.image_bytes)).convert("L")

            before_arr = np.array(before_img)
            after_arr = np.array(after_img)

            # Resize if dimensions differ
            if before_arr.shape != after_arr.shape:
                after_img = after_img.resize(
                    (before_arr.shape[1], before_arr.shape[0])
                )
                after_arr = np.array(after_img)

            score, _ = ssim(before_arr, after_arr, full=True)
            return float(score)

        except ImportError:
            logger.warning(
                "scikit-image not available; using byte-level comparison"
            )
            # Fallback: compare raw bytes (crude but functional)
            if before.image_bytes == after.image_bytes:
                return 1.0
            return 0.5  # Unknown similarity; treat as moderate change

    def _save_step(self, step: StepRecord) -> None:
        """Save step screenshots to the output directory."""
        output_dir = self._config.output_dir
        if output_dir is None:
            return

        output_dir.mkdir(parents=True, exist_ok=True)
        num = step.step_number

        before_path = output_dir / f"step-{num:02d}-before.png"
        after_path = output_dir / f"step-{num:02d}-after.png"

        step.before_capture.save(before_path)
        step.after_capture.save(after_path)

        logger.info("Saved step %d: %s, %s", num, before_path, after_path)
