---
name: textual-tui-builder
description: Use this skill when creating Text User Interface (TUI) applications with the Textual Python framework, including prototyping interactive CLIs or card games.
---

# Textual TUI Builder

## Overview

This skill helps you build sophisticated Text User Interfaces (TUIs) using the Textual framework, a Python library for creating terminal and browser-based applications. It includes reference documentation, a card game template, and best practices for Textual development.

## When to Use

Invoke this skill when the user asks to:
- Build a terminal/TUI application in Python
- Create a CLI dashboard or interactive terminal interface
- Prototype card games or interactive CLIs
- Convert a CLI script to an interactive TUI

## Quick Start

### Basic Textual App

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
from textual.widgets import Header, Footer
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
        # Your content here
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        pass

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    MyApp().run()
```

## Common Workflows

### Creating a New TUI App

1. Start with basic app structure (see Quick Start)
2. Design layout (read `references/layout.md`)
3. Add widgets (read `references/widgets.md`)
4. Style with CSS (read `references/styling.md`)
5. Add interactivity (read `references/interactivity.md`)

### Adding Interactive Features

1. Define key bindings in `BINDINGS`
2. Implement action methods (`action_*`)
3. Handle widget messages (`on_button_pressed`, etc.)
4. Use reactive attributes for state management
5. Update UI in watchers

## Best Practices

- **Progressive Development**: Start simple, add complexity incrementally
- **Reactive State**: Use `reactive()` for state that affects UI
- **CSS Separation**: Keep styling in `.tcss` files, not inline
- **Widget Reuse**: Create custom widgets for repeated components
- **Message Bubbling**: Use `event.stop()` to control message propagation
- **Type Hints**: Use proper type hints for better IDE support
- **IDs and Classes**: Use semantic IDs/classes for querying and styling

## Dependencies

```bash
# Install textual
pip install textual

# With dev tools
pip install textual[dev]
```

## Resources

### references/
Comprehensive documentation loaded on-demand:
- `basics.md` - Core concepts and app structure
- `widgets.md` - Widget catalog and usage
- `layout.md` - Layout systems and positioning
- `styling.md` - CSS and theming
- `interactivity.md` - Events, bindings, and actions

### assets/
- `card-game-template/` - Complete starter template for card games with interactive cards, hands, and turn management

## Official Documentation

For topics not covered in this skill, consult:
- https://textual.textualize.io/ (official docs)
- https://github.com/Textualize/textual (GitHub repo)