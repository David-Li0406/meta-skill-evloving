---
name: text-transforms
description: TransformMatchingStrings and text animation patterns
metadata:
  tags: text, transform, matching, animation, tex
priority: high
---

# Text Transform Patterns

Smooth text transformations for mathematical explanations.

## Core Requirement

**MUST** use `TransformMatchingStrings` or `TransformMatchingTex` for text that shares common substrings.

**MUST** use `t2c` (text-to-color) parameter for highlighting specific parts of equations.

**MUST NOT** use basic Transform for text with matching parts (loses visual continuity).

---

## Pattern 1: TransformMatchingTex

Smoothly transform LaTeX with matching parts.

```python
class TexTransformScene(Scene):
    def construct(self):
        # Initial equation
        eq1 = MathTex("a^2 + b^2 = c^2")

        self.play(Write(eq1))
        self.wait()

        # Transform to modified version - matching parts morph smoothly
        eq2 = MathTex("a^2 + b^2 = ", "c^2")
        eq2[1].set_color(YELLOW)

        self.play(TransformMatchingTex(eq1, eq2))
```

## Pattern 2: TransformMatchingStrings

For regular Text objects with matching substrings.

```python
class TextTransformScene(Scene):
    def construct(self):
        text1 = Text("Binary Search: O(n)")
        self.play(Write(text1))

        text2 = Text("Binary Search: O(log n)")
        text2[-7:-1].set_color(GREEN)  # Highlight "log n"

        self.play(TransformMatchingStrings(text1, text2))
```

## Pattern 3: t2c (Text to Color)

Color specific parts of Tex.

```python
class ColoredTexScene(Scene):
    def construct(self):
        # Color specific substrings
        eq = MathTex(
            "E = mc^2",
            tex_to_color_map={
                "E": BLUE,
                "m": GREEN,
                "c": RED,
            }
        )

        self.play(Write(eq))
```

## Pattern 4: Substrings to Isolate

Isolate parts for individual animation.

```python
class IsolateScene(Scene):
    def construct(self):
        # Split into animatable parts
        eq = MathTex(
            "f(x)", "=", "x^2", "+", "2x", "+", "1",
            substrings_to_isolate=["x"]
        )

        self.play(Write(eq))

        # Animate specific part
        self.play(eq[2].animate.set_color(YELLOW))  # x^2
        self.play(eq[4].animate.set_color(YELLOW))  # 2x
```

## Pattern 5: Step-by-Step Equation Building

Progressive equation reveal.

```python
class EquationBuildScene(Scene):
    def construct(self):
        steps = [
            MathTex("x + 3 = 7"),
            MathTex("x + 3 - 3 = 7 - 3"),
            MathTex("x = 7 - 3"),
            MathTex("x = 4"),
        ]

        # Position all at same location
        for step in steps:
            step.move_to(ORIGIN)

        self.play(Write(steps[0]))

        for i in range(len(steps) - 1):
            self.wait(0.5)
            self.play(TransformMatchingTex(steps[i], steps[i + 1]))

        self.wait()
```

## Pattern 6: Equation with Highlights

Dynamic highlighting during explanation.

```python
class HighlightEquationScene(Scene):
    def construct(self):
        eq = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")

        self.play(Write(eq))

        # Highlight first term
        self.play(eq[0:2].animate.set_color(BLUE))
        self.wait(0.5)

        # Highlight second term
        self.play(
            eq[0:2].animate.set_color(WHITE),
            eq[3:5].animate.set_color(GREEN)
        )
        self.wait(0.5)

        # Highlight result
        self.play(
            eq[3:5].animate.set_color(WHITE),
            eq[6:8].animate.set_color(YELLOW)
        )
```

## Pattern 7: Text Replacement Animation

Replace part of text smoothly.

```python
class TextReplaceScene(Scene):
    def construct(self):
        title = Text("Complexity: O(n²)")
        self.play(Write(title))

        # Create new text with different part
        new_title = Text("Complexity: O(n log n)")
        new_title.move_to(title)

        self.play(TransformMatchingStrings(title, new_title))
```

## Pattern 8: Brace with Label

Annotate parts of equations.

```python
class BraceAnnotationScene(Scene):
    def construct(self):
        eq = MathTex("f(x) = ", "ax^2", "+", "bx", "+", "c")
        self.play(Write(eq))

        # Add brace under quadratic term
        brace = Brace(eq[1], DOWN)
        label = brace.get_text("quadratic term")

        self.play(
            GrowFromCenter(brace),
            Write(label)
        )
```

---

## Transform Comparison

| Method | Use Case |
|--------|----------|
| `Transform(a, b)` | Complete replacement |
| `TransformMatchingTex(a, b)` | LaTeX with matching parts |
| `TransformMatchingStrings(a, b)` | Text with matching substrings |
| `ReplacementTransform(a, b)` | a becomes b (a is removed) |

---

## Checklist

```
□ Using TransformMatchingTex for LaTeX equations
□ Using t2c for semantic coloring
□ Isolating substrings for individual animation
□ Positioning equations at same location before transform
□ Using Brace for annotations
□ Progressive reveal for step-by-step explanations
```

---

## Common Mistakes

```python
# ❌ BAD: Basic Transform loses matching structure
self.play(Transform(eq1, eq2))

# ✅ GOOD: TransformMatchingTex preserves structure
self.play(TransformMatchingTex(eq1, eq2))
```

```python
# ❌ BAD: Different positions cause jumping
eq1 = MathTex("x = 1").to_edge(LEFT)
eq2 = MathTex("x = 2").to_edge(RIGHT)
self.play(TransformMatchingTex(eq1, eq2))  # Jumps!

# ✅ GOOD: Same position for smooth morph
eq1 = MathTex("x = 1")
eq2 = MathTex("x = 2")
eq2.move_to(eq1)
self.play(TransformMatchingTex(eq1, eq2))
```
