---
name: strict-sync
description: Strict audio-video synchronization with automatic timing enforcement
metadata:
  tags: sync, timing, audio, animation, strict
priority: highest
---

# Strict Audio-Video Sync

**Problem:** Manual timing calculations lead to drift and sync errors.

**Solution:** Use a base class that automatically enforces timing for each segment.

## StrictSyncScene Base Class

```python
from manim import *

class StrictSyncScene(Scene):
    """Base class with strict audio-video synchronization."""

    # Override in subclass with your timing data
    TIMING = {}

    def construct(self):
        self.camera.background_color = "#1c1c1c"
        self._current_time = 0

        # Call all segment methods in order
        for seg_id in sorted(self.TIMING.keys()):
            method_name = f"seg_{seg_id}"
            if hasattr(self, method_name):
                self._run_segment(seg_id, getattr(self, method_name))

        # Final padding
        self.wait(2)

    def _run_segment(self, seg_id: str, method):
        """Run segment and enforce exact timing."""
        timing = self.TIMING[seg_id]
        target_start = timing["start"]
        target_end = timing["end"]
        target_duration = target_end - target_start

        # Sync to segment start (if we're behind)
        if self._current_time < target_start:
            self.wait(target_start - self._current_time)
            self._current_time = target_start

        # Record start
        segment_start = self.renderer.time

        # Run the segment
        method()

        # Calculate actual duration
        actual_duration = self.renderer.time - segment_start

        # Pad if segment was too short
        if actual_duration < target_duration:
            remaining = target_duration - actual_duration
            self.wait(remaining)

        # Update current time
        self._current_time = target_end

        # Debug output
        final_duration = self.renderer.time - segment_start
        status = "✓" if abs(final_duration - target_duration) < 0.1 else "⚠"
        print(f"{status} {seg_id}: target={target_duration:.1f}s actual={final_duration:.1f}s")
```

## Usage Pattern

```python
TIMING = {
    "01_hook": {"start": 0, "end": 5.65},
    "02_setup": {"start": 5.65, "end": 12.14},
    "03_main": {"start": 12.14, "end": 25.0},
    "04_result": {"start": 25.0, "end": 30.0},
}

class MyScene(StrictSyncScene):
    TIMING = TIMING

    def seg_01_hook(self):
        """Just write animations - timing is automatic."""
        text = Text("Hook question?", font_size=40)
        self.play(Write(text), run_time=1)
        # NO need for self.wait() - base class handles it!
        self.play(FadeOut(text), run_time=0.5)

    def seg_02_setup(self):
        graph = self.create_graph()
        self.play(FadeIn(graph), run_time=1)
        # Remaining time is auto-calculated and waited

    def seg_03_main(self):
        # Your main content
        pass

    def seg_04_result(self):
        result = Text("Result", font_size=32)
        self.play(Write(result), run_time=1)
        self.play(FadeOut(result), run_time=0.5)
```

## Key Benefits

| Before (Manual) | After (StrictSync) |
|-----------------|-------------------|
| Calculate duration manually | Auto-calculated |
| Easy to make timing errors | Enforced by base class |
| Drift accumulates | Each segment syncs to target |
| Debug timing issues | Built-in timing debug output |

## Advanced: Per-Animation Sync

For even tighter control, use animation markers:

```python
class TightSyncScene(StrictSyncScene):
    """Even tighter sync with per-animation timing."""

    def seg_with_markers(self):
        """Sync specific animations to specific times."""
        seg = self.TIMING["this_segment"]
        seg_start = seg["start"]

        # Animation 1: at segment start
        self.play_at(seg_start, Write(text1), run_time=1)

        # Animation 2: at segment start + 2s
        self.play_at(seg_start + 2, Transform(a, b), run_time=0.5)

        # Animation 3: at segment start + 4s
        self.play_at(seg_start + 4, FadeOut(all), run_time=0.5)

    def play_at(self, target_time: float, *animations, **kwargs):
        """Play animation at exact target time."""
        current = self.renderer.time
        if current < target_time:
            self.wait(target_time - current)
        self.play(*animations, **kwargs)
```

## Complete Example

```python
#!/usr/bin/env python3
from manim import *

TIMING = {
    "01": {"start": 0, "end": 3.5},
    "02": {"start": 3.5, "end": 8.0},
    "03": {"start": 8.0, "end": 15.0},
}

class StrictSyncScene(Scene):
    TIMING = {}

    def construct(self):
        self.camera.background_color = "#1c1c1c"
        self._current_time = 0

        for seg_id in sorted(self.TIMING.keys()):
            method_name = f"seg_{seg_id}"
            if hasattr(self, method_name):
                self._run_segment(seg_id, getattr(self, method_name))

        self.wait(2)  # End padding

    def _run_segment(self, seg_id, method):
        timing = self.TIMING[seg_id]
        target_duration = timing["end"] - timing["start"]

        if self._current_time < timing["start"]:
            self.wait(timing["start"] - self._current_time)
            self._current_time = timing["start"]

        start = self.renderer.time
        method()
        actual = self.renderer.time - start

        if actual < target_duration:
            self.wait(target_duration - actual)

        self._current_time = timing["end"]


class DemoScene(StrictSyncScene):
    TIMING = TIMING

    def seg_01(self):
        t = Text("Hello", font_size=48)
        self.play(Write(t), run_time=1)
        self.play(FadeOut(t), run_time=0.5)

    def seg_02(self):
        t = Text("World", font_size=48)
        self.play(Write(t), run_time=1)
        self.play(FadeOut(t), run_time=0.5)

    def seg_03(self):
        t = Text("Done!", font_size=48, color=YELLOW)
        self.play(Write(t), run_time=1)
        self.play(FadeOut(t), run_time=0.5)
```

## Checklist

When using StrictSync:

```
□ TIMING dict has all segment IDs in order
□ Each segment method is named seg_XX where XX matches TIMING key
□ Animations total time < segment duration (leave room for auto-wait)
□ No manual self.wait() calls for timing (only for artistic pauses)
□ End padding is handled by base class
```

## Debug Output

When rendered, you'll see:

```
✓ 01: target=3.5s actual=3.5s
✓ 02: target=4.5s actual=4.5s
⚠ 03: target=7.0s actual=7.2s  ← Warning: slightly over
```

Fix `⚠` warnings by reducing animation run_time in that segment.
