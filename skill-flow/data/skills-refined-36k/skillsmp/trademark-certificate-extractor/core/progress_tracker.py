#!/usr/bin/env python3
"""
Progress Tracker Module

Provides real-time progress tracking for batch processing operations.
"""

import sys
import time
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
from pathlib import Path
import threading


class ProgressTracker:
    """
    Tracks and displays progress for batch operations with ETA calculation
    """

    def __init__(self, total: int, description: str = "Processing",
                 show_eta: bool = True, show_rate: bool = True):
        """
        Initialize progress tracker

        Args:
            total: Total number of items to process
            description: Description of the operation
            show_eta: Whether to show estimated time remaining
            show_rate: Whether to show processing rate
        """
        self.total = total
        self.description = description
        self.show_eta = show_eta
        self.show_rate = show_rate

        self.current = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.completed_items = []
        self.failed_items = []
        self.skipped_items = []

        self._lock = threading.Lock()
        self._is_finished = False

    def update(self, increment: int = 1, status: str = "success",
               item_name: Optional[str] = None, details: Optional[Dict] = None):
        """
        Update progress

        Args:
            increment: Number of items to increment
            status: Status of the item ("success", "failed", "skipped")
            item_name: Name of the processed item
            details: Additional details about the item
        """
        with self._lock:
            self.current += increment

            # Track items by status
            item_info = {
                'name': item_name,
                'details': details or {},
                'timestamp': datetime.now()
            }

            if status == "success":
                self.completed_items.append(item_info)
            elif status == "failed":
                self.failed_items.append(item_info)
            elif status == "skipped":
                self.skipped_items.append(item_info)

            self._display_progress()

    def _display_progress(self):
        """Display progress bar and statistics"""
        if self._is_finished:
            return

        # Calculate percentage
        percentage = (self.current / self.total * 100) if self.total > 0 else 0

        # Calculate elapsed time
        elapsed = time.time() - self.start_time

        # Calculate ETA
        if self.current > 0 and self.show_eta:
            rate = self.current / elapsed
            remaining = (self.total - self.current) / rate if rate > 0 else 0
            eta_str = self._format_time(remaining)
        else:
            eta_str = "N/A"

        # Calculate rate
        if self.show_rate and elapsed > 0:
            rate = self.current / elapsed
            rate_str = f"{rate:.2f} items/s"
        else:
            rate_str = ""

        # Build progress bar
        bar_length = 40
        filled_length = int(bar_length * self.current / self.total) if self.total > 0 else 0
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        # Build status line
        status_parts = []
        if len(self.completed_items) > 0:
            status_parts.append(f"✓ {len(self.completed_items)}")
        if len(self.failed_items) > 0:
            status_parts.append(f"✗ {len(self.failed_items)}")
        if len(self.skipped_items) > 0:
            status_parts.append(f"⊘ {len(self.skipped_items)}")

        status_str = " | ".join(status_parts) if status_parts else ""

        # Display progress line
        line = f"\r{self.description}: |{bar}| {self.current}/{self.total} ({percentage:.1f}%)"

        if self.show_eta:
            line += f" | ETA: {eta_str}"

        if self.show_rate and rate_str:
            line += f" | {rate_str}"

        if status_str:
            line += f" | {status_str}"

        # Print with carriage return to overwrite previous line
        sys.stdout.write(line)
        sys.stdout.flush()

    def _format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time string"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def finish(self, message: Optional[str] = None):
        """
        Mark progress as finished and display final summary

        Args:
            message: Optional completion message
        """
        with self._lock:
            if self._is_finished:
                return

            self._is_finished = True

            # Final update
            self._display_progress()
            sys.stdout.write("\n")

            # Display summary
            elapsed = time.time() - self.start_time
            elapsed_str = self._format_time(elapsed)

            print("\n" + "=" * 60)
            if message:
                print(message)
            else:
                print("✓ Processing completed")

            print("-" * 60)
            print(f"Total items: {self.total}")
            print(f"Completed: {len(self.completed_items)}")
            print(f"Failed: {len(self.failed_items)}")
            print(f"Skipped: {len(self.skipped_items)}")
            print(f"Total time: {elapsed_str}")

            if elapsed > 0:
                rate = self.total / elapsed
                print(f"Average rate: {rate:.2f} items/s")

            print("=" * 60)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get progress summary

        Returns:
            Dictionary with progress statistics
        """
        with self._lock:
            elapsed = time.time() - self.start_time

            return {
                'total': self.total,
                'current': self.current,
                'completed': len(self.completed_items),
                'failed': len(self.failed_items),
                'skipped': len(self.skipped_items),
                'percentage': (self.current / self.total * 100) if self.total > 0 else 0,
                'elapsed_seconds': elapsed,
                'rate': (self.current / elapsed) if elapsed > 0 else 0,
                'is_finished': self._is_finished,
            }

    def get_failed_items(self) -> list:
        """Get list of failed items"""
        with self._lock:
            return self.failed_items.copy()

    def get_completed_items(self) -> list:
        """Get list of completed items"""
        with self._lock:
            return self.completed_items.copy()


class MultiStageProgressTracker:
    """
    Tracks progress across multiple stages of processing
    """

    def __init__(self, stages: Dict[str, int]):
        """
        Initialize multi-stage progress tracker

        Args:
            stages: Dictionary mapping stage names to total items in each stage
        """
        self.stages = stages
        self.current_stage = None
        self.stage_trackers = {}
        self.start_time = time.time()

    def start_stage(self, stage_name: str):
        """
        Start a new processing stage

        Args:
            stage_name: Name of the stage to start
        """
        if stage_name not in self.stages:
            raise ValueError(f"Unknown stage: {stage_name}")

        self.current_stage = stage_name
        total = self.stages[stage_name]

        print(f"\n{'='*60}")
        print(f"Stage: {stage_name}")
        print(f"{'='*60}")

        self.stage_trackers[stage_name] = ProgressTracker(
            total=total,
            description=stage_name
        )

    def update(self, increment: int = 1, status: str = "success",
               item_name: Optional[str] = None):
        """Update current stage progress"""
        if self.current_stage and self.current_stage in self.stage_trackers:
            self.stage_trackers[self.current_stage].update(
                increment=increment,
                status=status,
                item_name=item_name
            )

    def finish_stage(self):
        """Finish current stage"""
        if self.current_stage and self.current_stage in self.stage_trackers:
            self.stage_trackers[self.current_stage].finish()

    def finish_all(self):
        """Finish all stages and display overall summary"""
        if self.current_stage:
            self.finish_stage()

        elapsed = time.time() - self.start_time

        print("\n" + "=" * 60)
        print("ALL STAGES COMPLETED")
        print("=" * 60)

        total_items = 0
        total_completed = 0
        total_failed = 0

        for stage_name, tracker in self.stage_trackers.items():
            summary = tracker.get_summary()
            total_items += summary['total']
            total_completed += summary['completed']
            total_failed += summary['failed']

            print(f"{stage_name}:")
            print(f"  Completed: {summary['completed']}/{summary['total']}")
            print(f"  Failed: {summary['failed']}")

        print("-" * 60)
        print(f"Total items processed: {total_items}")
        print(f"Total completed: {total_completed}")
        print(f"Total failed: {total_failed}")
        print(f"Total time: {self._format_time(elapsed)}")
        print("=" * 60)

    def _format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time string"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"


if __name__ == "__main__":
    # Test progress tracker
    import random

    print("Testing Single Stage Progress Tracker")
    print("=" * 60)

    tracker = ProgressTracker(total=50, description="Processing certificates")

    for i in range(50):
        time.sleep(0.1)  # Simulate processing

        # Randomly assign status
        rand = random.random()
        if rand < 0.8:
            status = "success"
        elif rand < 0.95:
            status = "skipped"
        else:
            status = "failed"

        tracker.update(status=status, item_name=f"certificate_{i}.pdf")

    tracker.finish()

    # Test multi-stage tracker
    print("\n\nTesting Multi-Stage Progress Tracker")
    print("=" * 60)

    multi_tracker = MultiStageProgressTracker({
        'OCR Extraction': 20,
        'Logo Extraction': 20,
        'LLM Processing': 20,
        'Excel Generation': 1,
    })

    for stage in ['OCR Extraction', 'Logo Extraction', 'LLM Processing', 'Excel Generation']:
        multi_tracker.start_stage(stage)
        total = multi_tracker.stages[stage]

        for i in range(total):
            time.sleep(0.05)
            multi_tracker.update(status="success", item_name=f"item_{i}")

        multi_tracker.finish_stage()

    multi_tracker.finish_all()
