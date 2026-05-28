---
name: audio-sync
description: Synchronizing narration/audio with video animations
metadata:
  tags: audio, sync, timing, narration, tts
priority: high
---

# Audio-Visual Synchronization

Proper sync between narration and visuals is critical. Out-of-sync audio destroys the learning experience.

> **Recommended:** Use `StrictSyncScene` base class from `strict-sync.md` for automatic timing enforcement.

## The Sync Problem

```
❌ PROBLEM: Narration says one thing while video shows another

Video: [Shows graph building]
Audio: "And now we see the final result"  ← MISMATCH!
```

## Sync Strategy: Scene-Based Timing

### Method 1: Timed Sections with Markers

```python
class SyncedScene(Scene):
    """Scene with precise timing markers for audio sync."""

    def construct(self):
        # Define timeline
        self.timeline = {
            "hook": (0, 5),           # 0-5 seconds
            "setup": (5, 15),         # 5-15 seconds
            "explanation": (15, 40),  # 15-40 seconds
            "conclusion": (40, 50),   # 40-50 seconds
        }

        self.run_section("hook", self.section_hook)
        self.run_section("setup", self.section_setup)
        self.run_section("explanation", self.section_explanation)
        self.run_section("conclusion", self.section_conclusion)

    def run_section(self, name, section_func):
        """Run a section with timing enforcement."""
        start_time, end_time = self.timeline[name]
        target_duration = end_time - start_time

        # Mark start
        section_start = self.renderer.time

        # Run the section
        section_func()

        # Calculate actual duration
        actual_duration = self.renderer.time - section_start

        # Pad if section was too short
        if actual_duration < target_duration:
            self.wait(target_duration - actual_duration)

        print(f"Section '{name}': target={target_duration}s, actual={actual_duration:.1f}s")
```

### Method 2: Script-Driven Animation

```python
# Define script with precise timestamps
NARRATION_SCRIPT = [
    {
        "time": 0,
        "duration": 3,
        "text": "How do we find the shortest path?",
        "animation": "show_title"
    },
    {
        "time": 3,
        "duration": 2,
        "text": "Dijkstra's Algorithm.",
        "animation": "show_algorithm_name"
    },
    {
        "time": 5,
        "duration": 5,
        "text": "Let's build a simple graph.",
        "animation": "build_graph"
    },
    # ... etc
]

class ScriptDrivenScene(Scene):
    def construct(self):
        for segment in NARRATION_SCRIPT:
            # Get the animation method
            anim_method = getattr(self, segment["animation"])

            # Run animation within time budget
            self.run_timed(anim_method, segment["duration"])

    def run_timed(self, method, target_duration):
        """Run method and ensure it takes exactly target_duration."""
        start = self.renderer.time
        method()
        elapsed = self.renderer.time - start

        if elapsed < target_duration:
            self.wait(target_duration - elapsed)
        elif elapsed > target_duration:
            print(f"⚠️ Animation exceeded budget: {elapsed:.1f}s > {target_duration}s")
```

## Timing Estimation

### Words to Seconds

```python
def estimate_speech_duration(text, wpm=150):
    """Estimate how long text takes to speak.

    Args:
        text: The narration text
        wpm: Words per minute (default 150 for clear speech)

    Returns:
        Duration in seconds
    """
    words = len(text.split())
    return (words / wpm) * 60

# Examples:
# "How do we find the shortest path?" (7 words) ≈ 2.8 seconds
# "Let's build a simple graph with nodes and edges." (9 words) ≈ 3.6 seconds
```

### Animation to Seconds

```python
# Typical animation durations
ANIMATION_TIMING = {
    "Write": 1.0,           # Writing text
    "Create": 1.0,          # Drawing shapes
    "FadeIn": 0.5,          # Fade in
    "FadeOut": 0.5,         # Fade out
    "Transform": 1.0,       # Morphing
    "GrowFromCenter": 0.8,  # Growing
    "Indicate": 0.8,        # Highlighting
    "wait": 1.0,            # Default pause
}

def estimate_scene_duration(animations):
    """Estimate total scene duration."""
    total = 0
    for anim_type, custom_time in animations:
        if custom_time:
            total += custom_time
        else:
            total += ANIMATION_TIMING.get(anim_type, 1.0)
    return total
```

## Pre-Production Sync Planning

### Step 1: Write Script First

```
SCRIPT:
[0-3s]  "How do we find the shortest path?"
[3-5s]  "Dijkstra's Algorithm."
[5-10s] "Let's build a graph. Each circle is a location."
[10-15s] "Numbers show distances between locations."
[15-20s] "We start from A and want shortest paths to all nodes."
[20-25s] "Key insight: always pick the closest unvisited node."
[25-35s] "Starting from A, C is closest with distance 2."
[35-45s] "From C, we update distances and continue..."
[45-50s] "Done! We found all shortest distances."
[50-55s] "The greedy choice gives optimal results."
```

### Step 2: Plan Animations to Match

```python
ANIMATION_PLAN = {
    (0, 3): ["show title question"],
    (3, 5): ["transform to algorithm name"],
    (5, 10): ["create nodes one by one"],
    (10, 15): ["create edges with weight labels"],
    (15, 20): ["highlight source node A"],
    (20, 25): ["show insight text box"],
    (25, 35): ["algorithm step 1: process A, visit C"],
    (35, 45): ["algorithm steps 2-4: process remaining"],
    (45, 50): ["show completion, highlight paths"],
    (50, 55): ["show takeaway text"],
}
```

### Step 3: Implement with Timing Guards

```python
class Dijkstra1MinSynced(Scene):
    def construct(self):
        self.ensure_duration(0, 3, self.show_hook)
        self.ensure_duration(3, 5, self.show_title)
        self.ensure_duration(5, 10, self.build_nodes)
        self.ensure_duration(10, 15, self.build_edges)
        # ... etc

    def ensure_duration(self, start, end, method):
        """Ensure method runs exactly from start to end time."""
        target = end - start

        # Run animation
        before = self.renderer.time
        method()
        after = self.renderer.time
        elapsed = after - before

        # Adjust timing
        if elapsed < target:
            self.wait(target - elapsed)
        elif elapsed > target * 1.1:  # 10% tolerance
            print(f"⚠️ {method.__name__} took {elapsed:.1f}s, target was {target}s")
```

## Post-Production Sync Check

### Manual Review Process

```
1. Render video without audio
2. Play video with narration audio side by side
3. Note any sync issues:
   - Audio ahead of video
   - Video ahead of audio
   - Mismatched content
4. Adjust timing and re-render
```

### Automated Sync Validation

```python
def validate_sync(video_markers, audio_markers, tolerance=0.5):
    """Check if video and audio markers align.

    Args:
        video_markers: List of (time, event) for video
        audio_markers: List of (time, event) for audio
        tolerance: Acceptable difference in seconds

    Returns:
        List of sync issues
    """
    issues = []

    for v_time, v_event in video_markers:
        # Find matching audio event
        matching_audio = [
            (a_time, a_event)
            for a_time, a_event in audio_markers
            if a_event == v_event
        ]

        if not matching_audio:
            issues.append(f"No audio for video event '{v_event}' at {v_time}s")
            continue

        a_time, a_event = matching_audio[0]
        diff = abs(v_time - a_time)

        if diff > tolerance:
            issues.append(
                f"Sync issue for '{v_event}': "
                f"video={v_time}s, audio={a_time}s, diff={diff:.1f}s"
            )

    return issues
```

## TTS-Specific Sync Techniques

### Generate Audio with Timing Info

```python
import edge_tts
import asyncio

async def generate_with_timing(script, voice="en-US-GuyNeural"):
    """Generate TTS and return duration for each segment."""

    results = []

    for segment in script:
        output_path = f"audio/{segment['id']}.mp3"

        communicate = edge_tts.Communicate(segment["text"], voice)
        await communicate.save(output_path)

        # Get actual audio duration
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(output_path)
        duration = len(audio) / 1000  # milliseconds to seconds

        results.append({
            "id": segment["id"],
            "text": segment["text"],
            "target_time": segment["time"],
            "actual_duration": duration
        })

        print(f"{segment['id']}: {duration:.1f}s")

    return results
```

### Adjust Animation to Match Audio Duration

```python
def sync_animation_to_audio(audio_duration, animation_duration, scene):
    """Adjust scene timing to match audio."""

    if audio_duration > animation_duration:
        # Audio is longer - add pauses
        padding = audio_duration - animation_duration
        scene.wait(padding)
    else:
        # Animation is longer - speed up or trim
        # (Usually indicates animation is too complex)
        print(f"⚠️ Animation ({animation_duration}s) > Audio ({audio_duration}s)")
        print("Consider simplifying animation or extending narration")
```

## Quick Sync Checklist

Before combining video + audio:

```
□ Total video duration matches total audio duration (±2 seconds)
□ Each section's animation completes before narration moves on
□ Visual changes happen BEFORE or WITH narration (never after)
□ Pauses in narration have corresponding visual pauses
□ No visual still while narration continues for >3 seconds
□ No rapid animation while narration is silent for >3 seconds
```

## Common Sync Problems & Fixes

| Problem | Symptom | Fix |
|---------|---------|-----|
| Audio ahead | Narration describes next scene | Add animation, reduce audio speed |
| Video ahead | Visuals change before mentioned | Add wait(), extend narration |
| Uneven pacing | Some parts rushed, others slow | Use timed sections |
| Ending mismatch | Video ends before/after audio | Use `-shortest` flag in ffmpeg |
| Content mismatch | Audio talks about different thing | Re-align script with animations |
