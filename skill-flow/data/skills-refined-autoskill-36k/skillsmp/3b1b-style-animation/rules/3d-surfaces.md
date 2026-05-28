---
name: 3d-surfaces
description: 3D mathematical surface visualization
metadata:
  tags: 3d, surface, visualization, three-dimensional
---

# 3D Surface Visualization

## Basic 3D Surface

```python
from manim import *
import numpy as np

class Basic3DSurface(ThreeDScene):
    def construct(self):
        # 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )

        # Surface z = sin(x) * cos(y)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # Set camera angle
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        # Rotate camera for full view
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # Axis labels
        x_label = MathTex("x").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis, UP)
        z_label = MathTex("z").next_to(axes.z_axis, OUT)

        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
```

## Paraboloid (Loss Landscape style)

```python
class ParaboloidSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[0, 4, 1],
            x_length=5,
            y_length=5,
            z_length=4
        )

        # z = x^2 + y^2 (paraboloid)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),
            u_range=[-1.8, 1.8],
            v_range=[-1.8, 1.8],
            resolution=(40, 40),
            fill_opacity=0.8,
            checkerboard_colors=[PURPLE_D, PURPLE_E]
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        # Mark minimum point
        min_point = Dot3D(axes.c2p(0, 0, 0), color=GREEN, radius=0.15)
        min_label = MathTex(r"(0, 0)", color=GREEN)

        self.play(GrowFromCenter(min_point))
        self.add_fixed_in_frame_mobjects(min_label)
        min_label.to_corner(UR)
        self.play(Write(min_label))

        self.wait()
```

## Saddle Surface

```python
class SaddleSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-4, 4, 2],
            x_length=5,
            y_length=5,
            z_length=5
        )

        # z = x^2 - y^2 (saddle/hyperbolic paraboloid)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 - v**2),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[ORANGE, RED_E]
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        # Mark saddle point
        saddle_point = Dot3D(axes.c2p(0, 0, 0), color=YELLOW, radius=0.15)
        self.play(GrowFromCenter(saddle_point))

        # Label
        title = Text("Saddle Point", font_size=28, color=YELLOW)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # Rotate to show saddle shape
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(6)
        self.stop_ambient_camera_rotation()
```

## Contour Lines on Surface

```python
class SurfaceWithContours(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 4, 1]
        )

        def func(x, y):
            return x**2 + y**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-1.8, 1.8],
            v_range=[-1.8, 1.8],
            resolution=(30, 30),
            fill_opacity=0.5,
            fill_color=BLUE
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes), Create(surface))

        # Add contour lines at different z levels
        contour_levels = [0.5, 1, 2, 3]
        contours = VGroup()

        for level in contour_levels:
            radius = np.sqrt(level)
            contour = ParametricFunction(
                lambda t, r=radius: axes.c2p(r * np.cos(t), r * np.sin(t), level),
                t_range=[0, 2 * PI],
                color=YELLOW,
                stroke_width=2
            )
            contours.add(contour)

        self.play(Create(contours), run_time=2)
        self.wait()
```

## Gradient Vector Field on Surface

```python
class GradientOnSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 5, 1]
        )

        def func(x, y):
            return x**2 + y**2

        def gradient(x, y):
            return np.array([2*x, 2*y])  # ∇f = (2x, 2y)

        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(20, 20),
            fill_opacity=0.6,
            fill_color=BLUE
        )

        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes), Create(surface))

        # Add gradient arrows on xy-plane
        arrows = VGroup()
        for x in np.linspace(-1.2, 1.2, 5):
            for y in np.linspace(-1.2, 1.2, 5):
                if abs(x) > 0.2 or abs(y) > 0.2:  # Skip near origin
                    grad = gradient(x, y)
                    norm = np.linalg.norm(grad)
                    if norm > 0.1:
                        # Scale arrow for visibility
                        scale = 0.3 / norm

                        arrow = Arrow3D(
                            start=axes.c2p(x, y, 0),
                            end=axes.c2p(x + grad[0] * scale, y + grad[1] * scale, 0),
                            color=RED,
                            resolution=8
                        )
                        arrows.add(arrow)

        self.play(Create(arrows), run_time=2)

        # Label
        label = MathTex(r"\nabla f = (2x, 2y)", color=RED, font_size=24)
        label.to_corner(UL)
        self.add_fixed_in_frame_mobjects(label)
        self.play(Write(label))

        self.wait()
```

## Gaussian Surface (3D Bell Curve)

```python
class GaussianSurface3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 0.5, 0.1]
        )

        def bivariate_gaussian(x, y, mu_x=0, mu_y=0, sigma=1):
            return (1 / (2 * np.pi * sigma**2)) * np.exp(
                -((x - mu_x)**2 + (y - mu_y)**2) / (2 * sigma**2)
            )

        surface = Surface(
            lambda u, v: axes.c2p(u, v, bivariate_gaussian(u, v)),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(40, 40),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=3)

        # Formula
        formula = MathTex(
            r"f(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}",
            font_size=24
        )
        formula.to_corner(UL)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))

        # Rotate
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

## Animated Surface Deformation

```python
class SurfaceDeformation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1]
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes))

        # Amplitude parameter
        amp = ValueTracker(0)

        # Surface that deforms
        surface = always_redraw(
            lambda: Surface(
                lambda u, v: axes.c2p(
                    u, v,
                    amp.get_value() * np.sin(u * 2) * np.cos(v * 2)
                ),
                u_range=[-1.8, 1.8],
                v_range=[-1.8, 1.8],
                resolution=(30, 30),
                fill_opacity=0.7,
                fill_color=BLUE
            )
        )

        self.add(surface)

        # Animate amplitude change
        self.play(amp.animate.set_value(1), run_time=2)
        self.wait(0.5)
        self.play(amp.animate.set_value(-0.5), run_time=1.5)
        self.play(amp.animate.set_value(0.8), run_time=1.5)
        self.wait()
```

## Guidelines

- Use checkerboard colors for depth perception
- Always rotate camera to show 3D structure
- Mark critical points (minima, maxima, saddles)
- Use appropriate resolution (not too high = slow, not too low = jagged)
- Add contour lines for height reference

## Forbidden

- Do NOT use flat colors (hard to see 3D shape)
- Do NOT skip camera rotation
- Do NOT make surfaces too opaque (lose depth cues)
- Do NOT forget axis labels
- Do NOT rotate camera too fast
