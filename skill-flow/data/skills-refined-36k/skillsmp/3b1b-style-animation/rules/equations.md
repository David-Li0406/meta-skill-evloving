---
name: equations
description: LaTeX equation rendering and animation
metadata:
  tags: latex, equations, math, typography
---

# LaTeX Equation Rendering

## Basic Equation Display

```python
from manim import *

class EquationBasics(Scene):
    def construct(self):
        # Simple equation
        eq1 = MathTex(r"E = mc^2")
        self.play(Write(eq1))
        self.wait()

        # Equation with multiple parts
        eq2 = MathTex(
            r"f(x)", r"=", r"ax^2", r"+", r"bx", r"+", r"c"
        )
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2))
        self.wait()

        # Color individual parts
        eq2[0].set_color(YELLOW)  # f(x)
        eq2[2].set_color(BLUE)    # ax^2
        eq2[4].set_color(GREEN)   # bx
        eq2[6].set_color(RED)     # c

        self.play(
            *[Indicate(eq2[i]) for i in [0, 2, 4, 6]],
            run_time=1
        )
        self.wait()
```

## Equation Transformation

```python
class EquationTransformation(Scene):
    def construct(self):
        # Original equation
        eq1 = MathTex(r"(a + b)^2")

        self.play(Write(eq1))
        self.wait()

        # Expanded form
        eq2 = MathTex(r"a^2 + 2ab + b^2")

        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()

        # Alternative: ReplacementTransform for smooth morph
        eq3 = MathTex(r"a^2", r"+", r"2ab", r"+", r"b^2")
        eq3.next_to(eq2, DOWN, buff=1)

        # Highlight the 2ab term
        self.play(
            TransformFromCopy(eq2, eq3),
            run_time=1.5
        )
        self.play(eq3[2].animate.set_color(YELLOW))
        self.wait()
```

## Step-by-Step Derivation

```python
class StepByStepDerivation(Scene):
    def construct(self):
        # Quadratic formula derivation
        steps = [
            r"ax^2 + bx + c = 0",
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            r"x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}",
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
        ]

        prev_eq = None
        for i, step in enumerate(steps):
            eq = MathTex(step, font_size=36)

            if prev_eq:
                eq.next_to(prev_eq, DOWN, buff=0.5)
            else:
                eq.to_edge(UP, buff=1)

            # Arrow indicating derivation step
            if prev_eq:
                arrow = MathTex(r"\Downarrow", font_size=28)
                arrow.next_to(eq, UP, buff=0.15)
                self.play(
                    Write(arrow),
                    Write(eq),
                    run_time=0.8
                )
            else:
                self.play(Write(eq), run_time=0.8)

            self.wait(0.5)
            prev_eq = eq

        # Highlight final result
        final_box = SurroundingRectangle(prev_eq, color=YELLOW, buff=0.1)
        self.play(Create(final_box))
        self.wait()
```

## Equation with Annotations

```python
class AnnotatedEquation(Scene):
    def construct(self):
        # Main equation
        equation = MathTex(
            r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V"
        )
        equation.scale(0.9)

        self.play(Write(equation))
        self.wait()

        # Create braces and labels for each component
        # Note: This requires knowing the submobject indices

        # Brace under Q
        q_brace = Brace(equation[0][10], DOWN, buff=0.1)
        q_label = Text("Query", font_size=16).next_to(q_brace, DOWN, buff=0.05)
        q_label.set_color(YELLOW)

        # Brace under K
        k_brace = Brace(equation[0][12], DOWN, buff=0.1)
        k_label = Text("Key", font_size=16).next_to(k_brace, DOWN, buff=0.05)
        k_label.set_color(TEAL)

        # Brace under V
        v_brace = Brace(equation[0][14], DOWN, buff=0.1)
        v_label = Text("Value", font_size=16).next_to(v_brace, DOWN, buff=0.05)
        v_label.set_color(RED)

        self.play(
            GrowFromCenter(q_brace), Write(q_label),
            run_time=0.5
        )
        self.play(
            GrowFromCenter(k_brace), Write(k_label),
            run_time=0.5
        )
        self.play(
            GrowFromCenter(v_brace), Write(v_label),
            run_time=0.5
        )
        self.wait()
```

## Aligned Equations

```python
class AlignedEquations(Scene):
    def construct(self):
        # Multiple aligned equations
        equations = MathTex(
            r"f(x) &= x^2 + 2x + 1 \\",
            r"&= (x + 1)^2 \\",
            r"&= (x + 1)(x + 1)",
            font_size=36
        )

        self.play(Write(equations[0]))
        self.wait(0.5)
        self.play(Write(equations[1]))
        self.wait(0.5)
        self.play(Write(equations[2]))
        self.wait()
```

## Equation Isolation/Zoom

```python
class EquationZoom(MovingCameraScene):
    def construct(self):
        # Complex equation
        equation = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}"
        )

        self.play(Write(equation))
        self.wait()

        # Zoom into the integral sign
        integral_part = equation[0][0:5]  # Adjust indices as needed

        self.play(
            self.camera.frame.animate.set(width=integral_part.width * 3).move_to(integral_part),
            run_time=2
        )
        self.wait()

        # Zoom back out
        self.play(
            self.camera.frame.animate.set(width=14).move_to(ORIGIN),
            run_time=1.5
        )
        self.wait()
```

## Common Mathematical Formulas

```python
# Collection of properly formatted formulas

FORMULAS = {
    # Calculus
    "derivative": r"\frac{d}{dx}f(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
    "integral": r"\int_a^b f(x)\,dx = F(b) - F(a)",
    "chain_rule": r"\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)",

    # Linear Algebra
    "matrix_mult": r"(AB)_{ij} = \sum_k A_{ik} B_{kj}",
    "eigenvalue": r"A\mathbf{v} = \lambda\mathbf{v}",
    "determinant": r"\det(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) \prod_{i=1}^n a_{i,\sigma(i)}",

    # Probability
    "bayes": r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}",
    "gaussian": r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",

    # Deep Learning
    "softmax": r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}",
    "cross_entropy": r"H(p, q) = -\sum_x p(x) \log q(x)",
    "attention": r"\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V",
}
```

## Guidelines

- Use MathTex for mathematical notation, Text for regular text
- Split equations into parts for individual animation/coloring
- Use TransformMatchingTex for equation morphing
- Include step indicators (arrows) for derivations
- Use braces and labels for annotation

## Forbidden

- Do NOT use incorrect LaTeX syntax
- Do NOT forget to verify mathematical correctness
- Do NOT animate entire complex equations at once
- Do NOT use small font sizes for important formulas
- Do NOT skip step-by-step in complex derivations
