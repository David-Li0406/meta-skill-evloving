---
name: Glow Component Factory
description: Step-by-step guide for creating Industrial Amber UI components following the GlowFactory pattern.
---

# Glow Component Factory Workflow

This skill guides the creation of new Industrial Amber design system components for Gosling2.

## The Glow Component Philosophy

**Core Principles**:
1. **NO Inline Styles**: All styling via `theme.qss` and `objectName`
2. **Consistent Factory**: Always extend GlowWidget base classes
3. **Amber Aesthetic**: Dark background, amber accents, tactical readability
4. **Signal-Based**: Components communicate via signals, not direct references

## Component Creation Workflow

### Phase 1: Design & Planning

#### Step 1.1: Define Component Purpose
Ask yourself:
*   What is the component's primary function?
*   Is it an input (button, line edit) or display (label, LED)?
*   Does it need state (active/inactive, selected/unselected)?
*   What signals does it need to emit?

#### Step 1.2: Check for Existing Components
Before creating new component, check:
```
src/presentation/widgets/glow/
    __init__.py
    base.py          # GlowWidget base class
    button.py        # GlowButton
    line_edit.py     # GlowLineEdit
    combo_box.py     # GlowComboBox
    led.py           # GlowLED
    toggle.py        # GlowToggle
    tooltip.py       # GlowTooltip
```

Can you extend or compose existing components instead?

#### Step 1.3: Choose Base Class
*   **Interactive Elements**: Extend GlowWidget
*   **Buttons**: Extend GlowButton
*   **Input Fields**: Extend QLineEdit or QTextEdit
*   **Display Elements**: Extend QLabel or QFrame

### Phase 2: Implementation

#### Step 2.1: Create Component File
Location: `src/presentation/widgets/glow/{component_name}.py`

**Template**:
```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from .base import GlowWidget  # If extending GlowWidget


class Glow{ComponentName}(QWidget):  # Or extend GlowWidget
    """
    Brief description of component's purpose.

    Signals:
        signal_name: When signal is emitted
    """

    # Define signals
    value_changed = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_properties()
        self._init_ui()
        self._connect_signals()

    def _init_properties(self):
        """Initialize internal state"""
        self._value = None
        self._is_active = False

    def _init_ui(self):
        """Create and layout child widgets"""
        # Create widgets
        # Set object names
        # Create layouts
        # Apply layouts

    def _connect_signals(self):
        """Connect internal signals/slots"""
        pass

    # Public API
    def set_value(self, value):
        """Set component value"""
        self._value = value
        self._update_ui()
        self.value_changed.emit(value)

    def get_value(self):
        """Get current value"""
        return self._value

    # Private helpers
    def _update_ui(self):
        """Update visual state based on internal state"""
        pass
```

#### Step 2.2: Set Object Names (for QSS styling)
```python
def _init_ui(self):
    # Main widget
    self.setObjectName("GlowMyComponent")

    # Child widgets
    self.label = QLabel("Label")
    self.label.setObjectName("GlowLabel")

    self.input = QLineEdit()
    self.input.setObjectName("GlowInput")
```

#### Step 2.3: Implement Glow Effects (if interactive)
For hover/active states:
```python
def enterEvent(self, event):
    """Mouse enter - trigger glow"""
    self.setProperty("glow", "active")
    self.style().polish(self)  # Reapply stylesheet
    super().enterEvent(event)

def leaveEvent(self, event):
    """Mouse leave - remove glow"""
    self.setProperty("glow", "inactive")
    self.style().polish(self)
    super().leaveEvent(event)
```

### Phase 3: Styling (theme.qss)

#### Step 3.1: Add QSS Rules
Location: `src/resources/theme.qss`

**Template**:
```css
/* Glow{ComponentName} - Brief description */
QWidget#GlowMyComponent {
    background-color: #000000;
    border: 1px solid #FFC66D;
    border-radius: 4px;
    padding: 8px;
}

QWidget#GlowMyComponent[glow="active"] {
    border: 2px solid #FFC66D;
    box-shadow: 0 0 12px rgba(255, 198, 109, 0.6);
}

QLabel#GlowLabel {
    color: #FFC66D;
    font-family: "Bahnschrift Condensed", sans-serif;
    font-size: 11pt;
    text-transform: uppercase;
}
```

#### Step 3.2: Color Palette Usage
Use Industrial Amber colors:
```css
/* Amber - Primary accent */
color: #FFC66D;
border-color: #FFC66D;

/* Muted Amber - Secondary */
color: #FF8C00;

/* Magenta - Critical actions */
background-color: #FF00FF;

/* Cyan - Unprocessed data */
color: #00E5FF;

/* Red - Errors */
color: #FF4444;

/* Void - Backgrounds */
background-color: #000000;
```

#### Step 3.3: Typography
```css
font-family: "Bahnschrift Condensed", "Segoe UI", sans-serif;
font-size: 11pt;  /* Body text */
font-size: 14pt;  /* Headers */
text-transform: uppercase;  /* For buttons and labels */
letter-spacing: 1px;  /* Tactical spacing */
```

### Phase 4: Integration

#### Step 4.1: Export from Glow Module
Update `src/presentation/widgets/glow/__init__.py`:
```python
from .button import GlowButton
from .line_edit import GlowLineEdit
from .my_component import GlowMyComponent  # Add new component

__all__ = [
    'GlowButton',
    'GlowLineEdit',
    'GlowMyComponent',  # Export
]
```

#### Step 4.2: Use in Parent Widget
```python
from ..widgets.glow import GlowMyComponent

class MyFeatureWidget(QWidget):
    def _init_ui(self):
        # Create component
        self.my_component = GlowMyComponent()
        self.my_component.value_changed.connect(self._on_value_changed)

        # Add to layout
        layout.addWidget(self.my_component)
```

### Phase 5: Testing

#### Step 5.1: Visual Testing
1. Run application
2. Navigate to component
3. Verify:
    *   Colors match Industrial Amber palette
    *   Glow effects work on hover
    *   Text is readable
    *   Component responds to interaction

#### Step 5.2: Unit Testing
Create `tests/unit/presentation/widgets/glow/test_my_component.py`:
```python
import pytest
from PyQt6.QtCore import Qt
from src.presentation.widgets.glow import GlowMyComponent


def test_component_creation(qtbot):
    """Test component can be created"""
    component = GlowMyComponent()
    qtbot.addWidget(component)
    assert component is not None


def test_value_changed_signal(qtbot):
    """Test signal emission on value change"""
    component = GlowMyComponent()
    qtbot.addWidget(component)

    with qtbot.waitSignal(component.value_changed, timeout=1000):
        component.set_value("test")

    assert component.get_value() == "test"


def test_mouse_interaction(qtbot):
    """Test hover effects"""
    component = GlowMyComponent()
    qtbot.addWidget(component)

    # Simulate hover
    qtbot.mouseMove(component)
    # Verify property changed (if applicable)
```

#### Step 5.3: Integration Testing
Test in actual UI context:
```python
def test_component_in_parent_widget(qtbot):
    """Test component works within parent widget"""
    parent = MyFeatureWidget()
    qtbot.addWidget(parent)

    # Interact with component
    component = parent.my_component
    component.set_value("test")

    # Verify parent receives signal
    assert parent.current_value == "test"
```

## Common Component Patterns

### Pattern 1: Stateful Toggle
```python
class GlowToggle(GlowWidget):
    toggled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._is_on = False

    def mousePressEvent(self, event):
        self._is_on = not self._is_on
        self.toggled.emit(self._is_on)
        self._update_visual_state()
```

### Pattern 2: Value Display with Units
```python
class GlowValueDisplay(QWidget):
    def __init__(self, label: str, unit: str = ""):
        super().__init__()
        self._label = label
        self._unit = unit
        self._value = None

    def set_value(self, value: float):
        self._value = value
        self._update_display()

    def _update_display(self):
        text = f"{self._label}: {self._value} {self._unit}"
        self.label_widget.setText(text)
```

### Pattern 3: Multi-State Indicator
```python
class GlowStatusLED(GlowLED):
    class State(Enum):
        OFF = "#333333"
        ACTIVE = "#FFC66D"
        WARNING = "#FF8C00"
        ERROR = "#FF4444"

    def set_state(self, state: State):
        self.setGlowColor(state.value)
        self.setActive(state != State.OFF)
```

## Industrial Amber Design Guidelines

### Spacing
*   **Tight**: 4px (within components)
*   **Normal**: 8px (between related components)
*   **Wide**: 16px (between sections)

### Borders
*   **Standard**: 1px solid
*   **Active**: 2px solid with glow
*   **Separator**: 7px solid black bar

### Glow Effects
```css
/* Standard glow */
box-shadow: 0 0 8px rgba(255, 198, 109, 0.4);

/* Strong glow (active state) */
box-shadow: 0 0 16px rgba(255, 198, 109, 0.8);

/* Pulsing glow (critical state) */
animation: glow-pulse 1.5s ease-in-out infinite;

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 8px rgba(255, 198, 109, 0.4); }
    50% { box-shadow: 0 0 20px rgba(255, 198, 109, 1.0); }
}
```

### Text Treatment
*   **All Caps for Controls**: "SAVE", "CANCEL", "APPLY"
*   **Title Case for Data**: "Artist Name", "Song Title"
*   **Uppercase for Status**: "READY", "PROCESSING", "ERROR"

## Anti-Patterns to Avoid

### ❌ Inline Styles
```python
# BAD
button.setStyleSheet("background-color: red;")

# GOOD
button.setObjectName("ErrorButton")
# Define #ErrorButton in theme.qss
```

### ❌ Raw PyQt Widgets
```python
# BAD
button = QPushButton("Click Me")

# GOOD
from ..widgets.glow import GlowButton
button = GlowButton("CLICK ME")
```

### ❌ Hardcoded Colors
```python
# BAD
painter.setPen(QColor(255, 198, 109))

# GOOD
painter.setPen(QColor("#FFC66D"))  # Or define in constants
```

### ❌ Fixed Sizes
```python
# BAD
widget.setFixedSize(200, 100)

# GOOD
widget.setMinimumSize(200, 100)
widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
```

## Completion Checklist

Before considering component complete:
*   ✅ Extends appropriate GlowWidget base
*   ✅ Has clear, descriptive objectName
*   ✅ All styling in theme.qss (no inline styles)
*   ✅ Uses Industrial Amber color palette
*   ✅ Emits appropriate signals
*   ✅ Has docstring explaining purpose
*   ✅ Exported from glow/__init__.py
*   ✅ Has unit tests
*   ✅ Manually tested in UI
*   ✅ Follows naming conventions
