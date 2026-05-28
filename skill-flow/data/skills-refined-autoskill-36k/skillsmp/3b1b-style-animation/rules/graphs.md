---
name: graphs
description: Function plotting and graph visualization
metadata:
  tags: graphs, plotting, functions, visualization
---

# Function Graphing

## Basic Function Plot

```python
from manim import *
import numpy as np

class BasicFunctionPlot(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
            }
        )

        # Axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Plot function
        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = MathTex(r"f(x) = x^2", color=BLUE)
        graph_label.to_corner(UR)

        self.play(Create(graph), Write(graph_label))
        self.wait()
```

## Multiple Functions Comparison

```python
class MultipleFunctions(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5
        )
        self.play(Create(axes))

        functions = [
            (lambda x: x**2, r"x^2", BLUE),
            (lambda x: x**3, r"x^3", GREEN),
            (lambda x: np.abs(x), r"|x|", RED),
        ]

        legend = VGroup()

        for func, label_tex, color in functions:
            graph = axes.plot(func, color=color, x_range=[-2, 2])
            self.play(Create(graph), run_time=0.8)

            # Legend entry
            legend_line = Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3)
            legend_label = MathTex(label_tex, font_size=24)
            legend_item = VGroup(legend_line, legend_label).arrange(RIGHT, buff=0.2)
            legend.add(legend_item)

        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR)
        self.play(Create(legend))
        self.wait()
```

## Animated Function Drawing

```python
class AnimatedDrawing(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4
        )

        # Custom x-axis labels for pi
        x_labels = VGroup(
            MathTex(r"-\pi").move_to(axes.c2p(-PI, 0) + DOWN * 0.4),
            MathTex(r"-\frac{\pi}{2}").move_to(axes.c2p(-PI/2, 0) + DOWN * 0.4),
            MathTex(r"0").move_to(axes.c2p(0, 0) + DOWN * 0.4),
            MathTex(r"\frac{\pi}{2}").move_to(axes.c2p(PI/2, 0) + DOWN * 0.4),
            MathTex(r"\pi").move_to(axes.c2p(PI, 0) + DOWN * 0.4),
        )
        x_labels.scale(0.7)

        self.play(Create(axes), Write(x_labels))

        # Trace point along curve
        graph = axes.plot(np.sin, color=BLUE, x_range=[-PI, PI])

        # Dot that traces the curve
        dot = Dot(color=YELLOW, radius=0.08)
        dot.move_to(axes.c2p(-PI, np.sin(-PI)))

        trace = VMobject()
        trace.set_stroke(BLUE, width=3)
        trace.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_trace(mob):
            mob.add_line_to(dot.get_center())

        trace.add_updater(update_trace)

        self.add(trace, dot)
        self.play(
            MoveAlongPath(dot, graph),
            run_time=4,
            rate_func=linear
        )
        trace.remove_updater(update_trace)

        # Label
        label = MathTex(r"y = \sin(x)", color=BLUE)
        label.to_corner(UR)
        self.play(Write(label))
        self.wait()
```

## Derivative Visualization

```python
class DerivativeVisualization(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5
        )
        self.play(Create(axes))

        # Function f(x) = x^2
        func = lambda x: x**2
        deriv = lambda x: 2*x

        graph = axes.plot(func, color=BLUE, x_range=[-1.5, 2.2])
        self.play(Create(graph))

        # Point of tangency
        x_val = ValueTracker(1)

        # Tangent line that updates
        tangent = always_redraw(
            lambda: axes.plot(
                lambda x: deriv(x_val.get_value()) * (x - x_val.get_value()) + func(x_val.get_value()),
                color=YELLOW,
                x_range=[x_val.get_value() - 1, x_val.get_value() + 1]
            )
        )

        # Point on curve
        point = always_redraw(
            lambda: Dot(
                axes.c2p(x_val.get_value(), func(x_val.get_value())),
                color=RED
            )
        )

        # Slope indicator
        slope_text = always_redraw(
            lambda: MathTex(
                f"\\text{{slope}} = {deriv(x_val.get_value()):.2f}",
                font_size=24
            ).to_corner(UR)
        )

        self.add(tangent, point, slope_text)

        # Animate x moving
        self.play(x_val.animate.set_value(-1), run_time=2)
        self.play(x_val.animate.set_value(2), run_time=3)
        self.wait()
```

## Area Under Curve (Integral)

```python
class AreaUnderCurve(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=5
        )
        self.play(Create(axes))

        # Function
        func = lambda x: 0.2 * x**2 + 0.5
        graph = axes.plot(func, color=BLUE, x_range=[0, 4.5])
        self.play(Create(graph))

        # Animated area from a to b
        a, b = 1, 4

        # Riemann sum rectangles (increasing n)
        for n in [4, 8, 16, 32]:
            dx = (b - a) / n
            rectangles = VGroup()

            for i in range(n):
                x_left = a + i * dx
                height = func(x_left)

                rect = Rectangle(
                    width=dx * axes.x_length / 5,
                    height=height * axes.y_length / 5,
                    fill_color=BLUE,
                    fill_opacity=0.5,
                    stroke_width=1
                )
                rect.move_to(axes.c2p(x_left + dx/2, height/2))
                rect.align_to(axes.c2p(x_left, 0), LEFT + DOWN)
                rectangles.add(rect)

            if n == 4:
                self.play(Create(rectangles), run_time=1)
                current_rects = rectangles
            else:
                self.play(Transform(current_rects, rectangles), run_time=0.8)

        # Replace with smooth area
        area = axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.5)
        self.play(Transform(current_rects, area))

        # Integral notation
        integral = MathTex(
            r"\int_1^4 f(x)\,dx",
            font_size=28
        ).to_corner(UR)
        self.play(Write(integral))
        self.wait()
```

## Parametric Curves

```python
class ParametricCurve(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6
        )
        self.play(Create(axes))

        # Lissajous curve
        curve = ParametricFunction(
            lambda t: axes.c2p(
                2 * np.sin(3 * t),
                2 * np.sin(2 * t)
            ),
            t_range=[0, 2 * PI],
            color=BLUE
        )

        self.play(Create(curve), run_time=4)

        # Equations
        equations = MathTex(
            r"x(t) = 2\sin(3t)",
            r"\\",
            r"y(t) = 2\sin(2t)",
            font_size=24
        ).to_corner(UL)

        self.play(Write(equations))
        self.wait()
```

## Guidelines

- Always include axis labels and numbers
- Use consistent colors for related graphs
- Animate curve drawing for emphasis
- Show relationship between function and derivative/integral
- Use ValueTracker for interactive demonstrations

## Forbidden

- Do NOT forget axis labels
- Do NOT use same color for different functions
- Do NOT skip the coordinate system
- Do NOT make curves too thin to see
- Do NOT animate too fast for complex curves
