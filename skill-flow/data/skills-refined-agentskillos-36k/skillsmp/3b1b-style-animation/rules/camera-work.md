---
name: camera-work
description: Camera movements and zooming techniques for deep learning visualizations
metadata:
  tags: manim, camera, zoom, movement
---

# Camera Work for Deep Learning Animations

## Moving Camera Scene

For complex network visualizations, use MovingCameraScene:

```python
from manim import *

class NetworkZoom(MovingCameraScene):
    def construct(self):
        network = self.create_network()
        self.add(network)

        # Zoom into a specific neuron
        neuron = network[0][2]  # Third neuron in first layer
        self.play(
            self.camera.frame.animate.set_width(neuron.width * 4).move_to(neuron),
            run_time=2
        )
        self.wait()

        # Zoom back out
        self.play(
            self.camera.frame.animate.set_width(14).move_to(ORIGIN),
            run_time=1.5
        )
```

## Zooming Techniques

### Smooth Zoom In

```python
# Zoom to show detail
self.play(
    self.camera.frame.animate.scale(0.5).move_to(target),
    run_time=1.5,
    rate_func=smooth
)
```

### Zoom with Focus Shift

```python
# Zoom while moving to new area
self.play(
    self.camera.frame.animate
        .set_width(6)
        .move_to(attention_head),
    run_time=2
)
```

## 3D Camera (for loss landscapes)

```python
from manim import *

class LossLandscape(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        surface = Surface(
            lambda u, v: np.array([u, v, self.loss_function(u, v)]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30)
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, surface)

        # Rotate camera around the surface
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()

    def loss_function(self, x, y):
        return x**2 + y**2  # Simple convex loss
```

## Camera Frame Saving

Save and restore camera positions:

```python
# Save current camera state
original_width = self.camera.frame.width
original_center = self.camera.frame.get_center()

# Zoom in
self.play(self.camera.frame.animate.scale(0.3).move_to(detail))
self.wait()

# Restore
self.play(
    self.camera.frame.animate
        .set_width(original_width)
        .move_to(original_center)
)
```

## Guidelines

- Use `rate_func=smooth` for natural camera movements
- Zoom in when explaining details (single neuron, attention weight)
- Zoom out when showing overall architecture
- Camera movement duration: 1.5-2 seconds for comprehension
- Always pause (wait) after camera movement

## Forbidden

- Do NOT make jarring instant camera jumps - always animate
- Do NOT zoom in too far (objects become pixelated)
- Do NOT rotate 3D camera too fast (causes motion sickness)
- Do NOT combine zoom and rotation simultaneously
