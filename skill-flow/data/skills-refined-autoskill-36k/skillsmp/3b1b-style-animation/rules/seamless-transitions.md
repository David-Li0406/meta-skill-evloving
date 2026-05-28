---
name: seamless-transitions
description: Natural, seamless transitions between animation segments
metadata:
  tags: transitions, flow, seamless, pacing
priority: highest
---

# Seamless Transitions

> Inspired by 3Blue1Brown's animation style: progressive complexity, visual layering, temporal sequencing.

**Problem:** Choppy videos with awkward pauses between segments.

**Root causes:**
1. Each segment starts fresh with FadeIn, ends with FadeOut
2. Audio pause (0.3-0.5s) creates dead time
3. Strict timing enforcement adds unnecessary waits
4. No visual continuity between segments

## Solution 1: Persistent Elements

Keep core visuals on screen across segments. Only animate changes.

```python
class SeamlessScene(Scene):
    def construct(self):
        # Create persistent elements ONCE
        self.array = self._create_array()
        self.play(FadeIn(self.array), run_time=1)

        # Segments modify existing elements, don't recreate
        self.seg_01()  # Highlight element
        self.seg_02()  # Move pointer
        self.seg_03()  # Update value
        # No FadeOut between segments!

        # Single cleanup at the end
        self.play(FadeOut(self.array), run_time=0.5)
```

## Solution 2: Overlap Transitions

Start next animation BEFORE current one fully ends.

```python
def seg_transition(self):
    """Overlap FadeOut with next FadeIn."""
    # Instead of:
    # self.play(FadeOut(old))
    # self.play(FadeIn(new))

    # Do this:
    self.play(
        FadeOut(old),
        FadeIn(new),
        run_time=0.5
    )
```

## Solution 3: Reduce Audio Pauses

Generate audio with minimal pauses.

```python
# In audio generation script
pause = 0.2  # Instead of 0.4-0.5

# Or use continuous audio without pauses
# and let natural speech rhythm create breaks
```

## Solution 4: Fill Dead Time with Motion

Never have a static frame. Add subtle animations during waits.

```python
def wait_with_motion(self, duration, element):
    """Subtle pulse instead of static wait."""
    if duration > 0.5:
        self.play(
            element.animate.scale(1.02),
            run_time=duration / 2,
            rate_func=there_and_back
        )
    else:
        self.wait(duration)
```

## SeamlessStrictSync Base Class

Enhanced base class that maintains flow:

```python
class SeamlessStrictSync(Scene):
    """Strict timing with seamless transitions."""

    TIMING = {}
    AUDIO_PAUSE = 0.2  # Minimal pause

    def construct(self):
        self.camera.background_color = "#1c1c1c"
        self._current_time = 0
        self._persistent_elements = VGroup()

        # Setup phase - create all persistent elements
        self._setup()
        self.play(FadeIn(self._persistent_elements), run_time=1)

        # Run segments without recreating elements
        for seg_id in sorted(self.TIMING.keys()):
            method_name = f"seg_{seg_id}"
            if hasattr(self, method_name):
                self._run_segment_seamless(seg_id, getattr(self, method_name))

        # Single cleanup
        self.play(FadeOut(self._persistent_elements), run_time=0.5)
        self.wait(1.5)

    def _setup(self):
        """Override to create persistent elements."""
        pass

    def _run_segment_seamless(self, seg_id, method):
        """Run segment with minimal dead time."""
        timing = self.TIMING[seg_id]
        target_duration = timing["end"] - timing["start"]

        start = self.renderer.time
        method()
        elapsed = self.renderer.time - start

        # Only wait if significantly short
        remaining = target_duration - elapsed
        if remaining > 0.3:
            # Fill with subtle motion instead of static wait
            self._fill_time(remaining)
        elif remaining > 0:
            self.wait(remaining)

        self._current_time = timing["end"]

    def _fill_time(self, duration):
        """Fill time with subtle motion."""
        if self._persistent_elements:
            # Subtle breathe effect
            self.play(
                self._persistent_elements.animate.shift(UP * 0.02),
                run_time=duration / 2,
                rate_func=there_and_back
            )
        else:
            self.wait(duration)
```

## Example: Seamless Binary Search

```python
class BinarySearchSeamless(SeamlessStrictSync):
    TIMING = {...}

    def _setup(self):
        """Create array once."""
        self.boxes = [Square(...) for _ in range(9)]
        self.labels = [Text(str(v)) for v in ARRAY]
        self.pointers = VGroup()  # L, R, M pointers

        self._persistent_elements = VGroup(
            *self.boxes, *self.labels, self.pointers
        )

    def seg_01(self):
        """Just show hook text, array stays."""
        hook = Text("Find 23", color=YELLOW).to_edge(UP)
        self.play(Write(hook), run_time=1)
        # Don't FadeOut - let it stay or transform in next segment

    def seg_02(self):
        """Update pointers - no recreate."""
        self.play(
            self.pointers["L"].animate.move_to(...),
            self.pointers["M"].animate.move_to(...),
            run_time=0.5
        )
        # Highlight mid element
        self.boxes[4].set_stroke(YELLOW, width=4)
```

## Quick Checklist

For seamless videos:

```
□ Persistent elements created once in _setup()
□ Segments only modify/animate existing elements
□ No FadeOut between segments (only at very end)
□ Transitions overlap: FadeOut + FadeIn together
□ Audio pause ≤ 0.2 seconds
□ Dead time filled with subtle motion
□ Single cleanup at video end
```

## Anti-Patterns to Avoid

```python
# ❌ BAD: Recreating elements each segment
def seg_01(self):
    array = self._create_array()
    self.play(FadeIn(array))
    self.play(FadeOut(array))

def seg_02(self):
    array = self._create_array()  # Creating again!
    self.play(FadeIn(array))

# ✅ GOOD: Persistent elements
def _setup(self):
    self.array = self._create_array()

def seg_01(self):
    self.play(Indicate(self.array[0]))

def seg_02(self):
    self.play(self.array[0].animate.set_fill(GREEN))
```

```python
# ❌ BAD: Long static waits
self.wait(3)

# ✅ GOOD: Fill with motion
self.play(
    element.animate.scale(1.01),
    run_time=3,
    rate_func=there_and_back
)
```

```python
# ❌ BAD: Sequential FadeOut/FadeIn
self.play(FadeOut(old), run_time=0.5)
self.play(FadeIn(new), run_time=0.5)

# ✅ GOOD: Overlapped transition
self.play(FadeOut(old), FadeIn(new), run_time=0.5)
```
