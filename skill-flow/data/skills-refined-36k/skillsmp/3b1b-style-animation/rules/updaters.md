---
name: updaters
description: add_updater patterns for real-time dynamic animations
metadata:
  tags: updater, dynamic, real-time, animation, continuous
priority: high
---

# Updaters for Dynamic Animations

Updaters allow mobjects to automatically update their state every frame.

## Core Requirement

**MUST** use updaters for elements that need to continuously track or respond to other elements.

**MUST** remove updaters with `clear_updaters()` when no longer needed.

**MUST NOT** leave orphan updaters that cause performance issues.

---

## Pattern 1: Basic Updater

Element follows another element.

```python
class FollowScene(Scene):
    def construct(self):
        # Leader moves
        leader = Dot(color=BLUE)

        # Follower tracks leader
        follower = Dot(color=RED)
        follower.add_updater(lambda m: m.move_to(leader.get_center() + RIGHT))

        self.add(leader, follower)
        self.play(leader.animate.shift(UP * 2 + RIGHT * 3), run_time=2)

        # MUST: Clear updater when done
        follower.clear_updaters()
```

## Pattern 2: Value Tracker

Animate based on a changing value.

```python
class ValueTrackerScene(Scene):
    def construct(self):
        # Create value tracker
        t = ValueTracker(0)

        # Circle radius depends on t
        circle = Circle(radius=1, color=BLUE)
        circle.add_updater(
            lambda m: m.become(
                Circle(radius=0.5 + t.get_value(), color=BLUE)
            )
        )

        self.add(circle)

        # Animate the value
        self.play(t.animate.set_value(2), run_time=2)
        self.play(t.animate.set_value(0.5), run_time=1)

        circle.clear_updaters()
```

## Pattern 3: Label Following Object

Text that stays attached to a moving object.

```python
class LabelFollowScene(Scene):
    def construct(self):
        # Moving dot
        dot = Dot(color=BLUE)

        # Label that follows
        label = Text("A", font_size=24)
        label.add_updater(
            lambda m: m.next_to(dot, UP, buff=0.2)
        )

        self.add(dot, label)
        self.play(dot.animate.shift(RIGHT * 3 + UP * 2), run_time=2)

        label.clear_updaters()
```

## Pattern 4: Dynamic Calculation Display

Show real-time calculated values.

```python
class DynamicLabelScene(Scene):
    def construct(self):
        x = ValueTracker(1)

        # Function value display
        label = always_redraw(
            lambda: MathTex(f"f(x) = {x.get_value():.2f}^2 = {x.get_value()**2:.2f}")
        )

        self.add(label)
        self.play(x.animate.set_value(3), run_time=3)
```

## Pattern 5: Line Between Moving Points

Connection that updates automatically.

```python
class DynamicLineScene(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2, color=BLUE)
        dot2 = Dot(RIGHT * 2, color=RED)

        # Line always connects the two dots
        line = always_redraw(
            lambda: Line(dot1.get_center(), dot2.get_center(), color=WHITE)
        )

        self.add(dot1, dot2, line)

        self.play(
            dot1.animate.shift(UP * 2),
            dot2.animate.shift(DOWN + RIGHT),
            run_time=2
        )
```

## Pattern 6: Graph Function Updater

Dynamic function plotting.

```python
class DynamicGraphScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 5])
        self.add(axes)

        # Parameter that changes
        a = ValueTracker(1)

        # Graph updates with parameter
        graph = always_redraw(
            lambda: axes.plot(
                lambda x: a.get_value() * x**2,
                color=BLUE
            )
        )

        label = always_redraw(
            lambda: MathTex(f"y = {a.get_value():.1f}x^2").to_corner(UR)
        )

        self.add(graph, label)
        self.play(a.animate.set_value(0.5), run_time=2)
        self.play(a.animate.set_value(2), run_time=2)
```

## Pattern 7: Conditional Updater

Update only under certain conditions.

```python
class ConditionalUpdaterScene(Scene):
    def construct(self):
        dot = Dot(color=BLUE)
        trail = VGroup()

        def update_trail(mob):
            # Only add to trail if dot is moving right
            if dot.get_center()[0] > mob.get_center()[0] if len(trail) > 0 else True:
                new_dot = Dot(dot.get_center(), radius=0.03, color=BLUE_E)
                trail.add(new_dot)
                self.add(new_dot)

        dot.add_updater(update_trail)

        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 4), run_time=2)
        dot.clear_updaters()
```

## Pattern 8: dt-based Animation

Smooth time-based animation.

```python
class TimeDependentScene(Scene):
    def construct(self):
        dot = Dot(color=BLUE)

        # Rotate around origin using dt
        def orbit(mob, dt):
            mob.rotate(dt * PI, about_point=ORIGIN)

        dot.shift(RIGHT * 2)
        dot.add_updater(orbit)

        self.add(dot)
        self.wait(4)  # Orbits for 4 seconds

        dot.clear_updaters()
```

---

## always_redraw vs add_updater

| Method | Use Case |
|--------|----------|
| `always_redraw(func)` | Recreate entire mobject each frame |
| `add_updater(func)` | Modify existing mobject properties |

```python
# always_redraw: for complex redraws
label = always_redraw(lambda: Text(f"Value: {tracker.get_value():.2f}"))

# add_updater: for simple property changes
dot.add_updater(lambda m: m.set_color(RED if tracker.get_value() > 5 else BLUE))
```

---

## Checklist

```
□ Using add_updater for tracking relationships
□ Using always_redraw for dynamic recreations
□ ValueTracker for parameterized animations
□ ALWAYS calling clear_updaters() when done
□ Removing updaters before removing mobjects
□ Using dt parameter for time-based animation
```

---

## Common Mistakes

```python
# ❌ BAD: Forgetting to clear updaters
follower.add_updater(lambda m: m.move_to(leader))
# ... animation ...
# Missing: follower.clear_updaters()

# ✅ GOOD: Always clear when done
follower.add_updater(lambda m: m.move_to(leader))
# ... animation ...
follower.clear_updaters()
```

```python
# ❌ BAD: Heavy computation in updater
def heavy_update(mob):
    # This runs 60 times per second!
    result = expensive_calculation()
    mob.set_value(result)

# ✅ GOOD: Precompute or use ValueTracker
tracker = ValueTracker(precomputed_value)
mob.add_updater(lambda m: m.set_value(tracker.get_value()))
```
