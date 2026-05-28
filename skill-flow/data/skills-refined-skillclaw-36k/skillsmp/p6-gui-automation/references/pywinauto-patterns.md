# pywinauto Patterns for P6 Professional

This reference documents pywinauto patterns specifically for Oracle Primavera P6 Professional automation.

## Window Detection

### Finding P6 Main Window

P6 window titles follow these patterns:

```python
import pywinauto
from pywinauto import Application

# Pattern 1: Connect by window title regex
app = Application(backend="uia").connect(title_re=".*Primavera P6.*")

# Pattern 2: Connect by process name
app = Application(backend="uia").connect(path="PM.exe")

# Pattern 3: Connect by exact title (less reliable, title changes)
app = Application(backend="uia").connect(title="Primavera P6 Professional - MYPROJECT")
```

### Window Title Patterns

| P6 Version | Title Pattern | Example |
|------------|---------------|---------|
| P6 Professional | `Primavera P6 Professional - {PROJECT}` | `Primavera P6 Professional - GEMCO L1` |
| P6 EPPM | `Oracle Primavera P6 - {PROJECT}` | `Oracle Primavera P6 - GEMCO L1` |
| Login Dialog | `Log In` | `Log In` |
| Open Project | `Open Project` | `Open Project` |

### Backend Selection

Always use "uia" backend for P6 (Win32 backend has issues with P6's custom controls):

```python
# CORRECT
app = Application(backend="uia")

# WRONG - P6 controls won't be detected properly
app = Application(backend="win32")
```

## Dialog Handling

### Common P6 Dialogs

```python
# Find dialog by title
def find_dialog(main_window, title, timeout=5):
    try:
        dialog = main_window.child_window(title=title, control_type="Window")
        dialog.wait("visible", timeout=timeout)
        return dialog
    except Exception:
        return None

# Common dialogs
open_project = find_dialog(main_window, "Open Project")
schedule_dialog = find_dialog(main_window, "Schedule")
find_dialog = find_dialog(main_window, "Find")
confirm_dialog = find_dialog(main_window, "Confirm")
```

### Closing Dialogs Safely

```python
def close_any_dialogs(main_window):
    """Close any open dialogs by pressing ESC."""
    for _ in range(3):  # Try up to 3 times
        main_window.type_keys("{ESC}")
        time.sleep(0.2)
```

### Dialog Button Patterns

```python
# Find and click OK button
dialog.child_window(title="OK", control_type="Button").click()

# Find and click Cancel button
dialog.child_window(title="Cancel", control_type="Button").click()

# Find button by automation ID
dialog.child_window(auto_id="btnOK").click()
```

## Grid Navigation

### Activity Grid Structure

P6's activity grid is a custom control. Standard tree/grid controls don't always work.

```python
# Focus the grid area
def focus_activity_grid(main_window):
    # Click in the grid area or use Tab to navigate
    main_window.type_keys("{TAB}" * 5)  # Adjust count based on layout
    time.sleep(0.1)
```

### Keyboard Navigation (Preferred)

Keyboard navigation is MORE RELIABLE than mouse clicks for P6:

```python
# Navigate to first row
main_window.type_keys("^{HOME}")  # Ctrl+HOME

# Navigate to last row
main_window.type_keys("^{END}")   # Ctrl+END

# Move up/down
main_window.type_keys("{UP}")
main_window.type_keys("{DOWN}")

# Move left/right in cells
main_window.type_keys("{TAB}")        # Next column
main_window.type_keys("+{TAB}")       # Previous column (Shift+TAB)

# Select all
main_window.type_keys("^a")           # Ctrl+A
```

### Column Navigation Pattern

To navigate to a specific column:

```python
def navigate_to_column(main_window, target_column, visible_columns):
    """Navigate to a specific column using TAB."""
    if target_column not in visible_columns:
        raise ValueError(f"Column '{target_column}' not visible")
    
    target_index = visible_columns.index(target_column)
    
    # Reset to first column
    main_window.type_keys("{HOME}")
    time.sleep(0.1)
    
    # TAB to target column
    for _ in range(target_index):
        main_window.type_keys("{TAB}")
        time.sleep(0.05)  # Small delay between tabs
```

### Reading Column Headers

```python
def get_visible_columns(main_window):
    """Attempt to read column headers from the grid."""
    # This is P6-version specific and may require adjustment
    # One approach: read header row via UIA
    grid = main_window.child_window(control_type="DataGrid")
    headers = grid.child_window(control_type="Header")
    columns = []
    for item in headers.children():
        columns.append(item.window_text())
    return columns
```

## Find Dialog (Ctrl+F)

The most reliable way to select activities:

```python
def select_activity_by_id(main_window, activity_id):
    """Select activity using Ctrl+F find dialog."""
    # Open Find dialog
    main_window.type_keys("^f")
    time.sleep(0.3)
    
    # Find the dialog
    find_dlg = main_window.child_window(title="Find")
    find_dlg.wait("visible", timeout=3)
    
    # Type activity ID
    find_dlg.type_keys(activity_id, with_spaces=True)
    
    # Press Find Next
    find_dlg.type_keys("{ENTER}")
    time.sleep(0.2)
    
    # Close dialog
    find_dlg.type_keys("{ESC}")
    
    return True
```

## Edit Mode

### Entering Edit Mode

```python
def enter_edit_mode(main_window):
    """Enter edit mode for current cell."""
    main_window.type_keys("{F2}")
    time.sleep(0.1)

def exit_edit_mode(main_window, save=True):
    """Exit edit mode."""
    if save:
        main_window.type_keys("{ENTER}")
    else:
        main_window.type_keys("{ESC}")
    time.sleep(0.1)
```

### Editing Cell Value

```python
def edit_cell(main_window, value):
    """Edit current cell value."""
    # Enter edit mode
    main_window.type_keys("{F2}")
    time.sleep(0.1)
    
    # Select all existing text
    main_window.type_keys("^a")
    time.sleep(0.05)
    
    # Type new value
    main_window.type_keys(str(value), with_spaces=True)
    
    # Confirm
    main_window.type_keys("{ENTER}")
    time.sleep(0.1)
```

## Menu Access

### Using Menu Bar

```python
def select_menu(main_window, menu_path):
    """Select menu item by path like 'File->Print Preview'."""
    parts = menu_path.split("->")
    
    # Use Alt to access menu
    main_window.type_keys(f"%{parts[0][0].lower()}")  # Alt+First letter
    time.sleep(0.2)
    
    # Navigate to submenu items
    for item in parts[1:]:
        main_window.type_keys(item[0].lower())
        time.sleep(0.1)
```

### Common Menu Shortcuts

```python
# File menu
main_window.type_keys("%f")  # Alt+F

# Edit menu
main_window.type_keys("%e")  # Alt+E

# View menu
main_window.type_keys("%v")  # Alt+V

# Project menu
main_window.type_keys("%p")  # Alt+P

# Tools menu
main_window.type_keys("%t")  # Alt+T
```

## Error Recovery

### Retry Pattern

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=0.5):
    """Retry decorator for flaky UI operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    time.sleep(delay * (attempt + 1))
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=3)
def select_activity(main_window, activity_id):
    # ... potentially flaky operation
    pass
```

### Screenshot on Error

```python
import pyautogui
from datetime import datetime

def capture_error_screenshot(prefix="error"):
    """Capture screenshot for debugging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/{prefix}_{timestamp}.png"
    pyautogui.screenshot(filename)
    return filename
```

### Window Recovery

```python
def recover_window_focus(app):
    """Attempt to recover P6 window focus."""
    try:
        # Try to find and focus the main window
        main_window = app.window(title_re=".*Primavera P6.*")
        main_window.set_focus()
        time.sleep(0.3)
        
        # Close any dialogs
        main_window.type_keys("{ESC}")
        time.sleep(0.1)
        
        return main_window
    except Exception as e:
        logger.error(f"Failed to recover window: {e}")
        return None
```

## Timing Constants

Recommended delays for P6 operations:

```python
# Standard action delay
ACTION_DELAY = 0.1

# Delay after dialog opens
DIALOG_DELAY = 0.3

# Delay between cell navigation
CELL_DELAY = 0.05

# Delay after menu access
MENU_DELAY = 0.2

# Timeout for dialog appearance
DIALOG_TIMEOUT = 5.0

# Timeout for P6 connection
CONNECTION_TIMEOUT = 10.0
```

## Testing Connection

```python
def test_p6_connection():
    """Test if P6 is running and accessible."""
    try:
        app = Application(backend="uia").connect(title_re=".*Primavera P6.*", timeout=5)
        main_window = app.window(title_re=".*Primavera P6.*")
        title = main_window.window_text()
        print(f"Connected to: {title}")
        return True
    except Exception as e:
        print(f"P6 not found: {e}")
        return False
```
