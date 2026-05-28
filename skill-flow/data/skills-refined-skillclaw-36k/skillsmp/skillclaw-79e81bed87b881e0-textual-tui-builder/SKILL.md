---
name: textual-tui-builder
description: Use this skill when you want to create terminal user interfaces (TUIs) in Python using the Textual framework, whether for applications, dashboards, or interactive experiences.
---

# Skill body

## Overview

This skill helps you build sophisticated Text User Interfaces (TUIs) using the Textual framework, a modern Python library for creating terminal applications. It provides guidance on architecture, styling, and event handling, ensuring production-grade applications.

## When to Use

Invoke this skill when you need to:
- Build a terminal/TUI application in Python.
- Create a CLI dashboard or interactive terminal interface.
- Develop a data viewer, form, file browser, or any TUI component.
- Convert a CLI script to an interactive TUI.
- Prototype card games or other interactive applications.

## Design Process

Before coding, understand the requirements:

1. **Purpose**: What does this TUI do? What problem does it solve?
2. **Users**: Who will use it? Developers? End users? Power users?
3. **Interactions**: What actions can users take? What data do they view/edit?
4. **Layout**: Single screen? Multiple screens? Modal dialogs?
5. **Data**: What data sources? Real-time updates? File I/O?

## Architecture Guidelines

### Project Structure

```
my_tui_app/
├── __init__.py
├── app.py              # Main App class
├── screens/            # Screen classes (if multi-screen)
│   ├── __init__.py
│   ├── main.py
│   └── settings.py
├── widgets/            # Custom widgets
│   ├── __init__.py
│   └── custom_widget.py
├── styles/             # TCSS stylesheets
│   └── app.tcss
└── __main__.py         # Entry point
```

For simple apps, a single file is acceptable.

### Core App Pattern

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label
from textual.binding import Binding

class MyApp(App):
    """A Textual application."""

    CSS_PATH = "styles/app.tcss"  # External stylesheet
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Dark mode"),
        Binding("?", "show_help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Label("Hello, Textual!")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        pass

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = "dark" if self.theme == "light" else "light"

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

## Quick Start

### Basic Textual App

To create a simple Textual application, use the following template:

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Hello, Textual!")
        yield Footer()

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

### Card Game Template

For card game prototyping, copy the template:

```bash
cp -r assets/card-game-template/* ./my-game/
cd my-game
python app.py
```

The template includes:
- Interactive Card widget with face-up/down states
- Hand containers for player cards
- Play area with turn management
- Key bindings for card selection and playing
- Customizable styling

See `assets/card-game-template/README.md` for customization guide.

## Reference Documentation

This skill includes comprehensive reference files. Load them based on your task:

### references/basics.md
**Read when:** Setting up app structure, using reactive attributes, handling mounting, querying widgets, or working with messages/events.

### references/widgets.md
**Read when:** Adding UI elements like buttons, inputs, labels, data tables, or creating custom widgets.

### references/layout.md
**Read when:** Designing layouts, positioning widgets, using grid systems, or handling responsive sizing.