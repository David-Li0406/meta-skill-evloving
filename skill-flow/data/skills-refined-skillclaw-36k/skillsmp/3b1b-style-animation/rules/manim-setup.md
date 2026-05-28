---
name: manim-setup
description: Environment setup and project structure for Manim deep learning animations
metadata:
  tags: manim, setup, installation, project-structure
---

# Manim Setup for Deep Learning Animations

## Installation

Use ManimCE (Community Edition) for stability and active maintenance:

```bash
pip install manim
```

For GPU acceleration (recommended for complex neural network animations):

```bash
pip install manim[webgl_renderer]
```

## Project Structure

```
project/
├── scenes/
│   ├── neural_network.py
│   ├── backpropagation.py
│   └── transformer.py
├── components/
│   ├── neuron.py
│   ├── layer.py
│   └── attention.py
├── utils/
│   ├── colors.py
│   └── animations.py
├── assets/
│   └── images/
└── manim.cfg
```

## Configuration (manim.cfg)

```ini
[CLI]
quality = production_quality
preview = True

[output]
media_dir = ./media

[video]
pixel_height = 1080
pixel_width = 1920
frame_rate = 60
background_color = #1c1c1c
```

## Base Scene Template

```python
from manim import *

class DeepLearningScene(Scene):
    def construct(self):
        # 3b1b style dark background
        self.camera.background_color = "#1c1c1c"

        # Your animation code here
        pass
```

## Rendering Commands

```bash
# Preview quality (fast)
manim -pql scene.py SceneName

# Production quality
manim -pqh scene.py SceneName

# 4K quality
manim -pqk scene.py SceneName
```

## Forbidden

- Do NOT use `from manimlib import *` (old 3b1b version) - use `from manim import *` (ManimCE)
- Do NOT hardcode paths - use relative paths or config
- Do NOT skip virtual environment setup for reproducibility
