# P6 Keyboard Shortcuts Reference

Complete reference of Oracle Primavera P6 Professional keyboard shortcuts for GUI automation.

## Navigation

### Activity Grid Navigation

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| First activity | Ctrl+HOME | `^{HOME}` | Goes to top-left cell |
| Last activity | Ctrl+END | `^{END}` | Goes to bottom-right cell |
| Move up | UP Arrow | `{UP}` | Move up one row |
| Move down | DOWN Arrow | `{DOWN}` | Move down one row |
| Move left | LEFT Arrow | `{LEFT}` | Move left in cell or collapse |
| Move right | RIGHT Arrow | `{RIGHT}` | Move right in cell or expand |
| Next cell | TAB | `{TAB}` | Move to next column |
| Previous cell | Shift+TAB | `+{TAB}` | Move to previous column |
| Page up | PAGE UP | `{PGUP}` | Scroll up one page |
| Page down | PAGE DOWN | `{PGDN}` | Scroll down one page |
| First column | HOME | `{HOME}` | Go to first column in row |
| Last column | END | `{END}` | Go to last column in row |

### WBS/Hierarchy Navigation

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Expand node | + (numpad) or RIGHT | `{ADD}` or `{RIGHT}` | Expand WBS/group |
| Collapse node | - (numpad) or LEFT | `{SUBTRACT}` or `{LEFT}` | Collapse WBS/group |
| Expand all | Ctrl+Shift++ | `^+{ADD}` | Expand all nodes |
| Collapse all | Ctrl+Shift+- | `^+{SUBTRACT}` | Collapse all nodes |

## Selection

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Select all | Ctrl+A | `^a` | Select all activities |
| Extend selection up | Shift+UP | `+{UP}` | Add row above to selection |
| Extend selection down | Shift+DOWN | `+{DOWN}` | Add row below to selection |
| Select to first | Ctrl+Shift+HOME | `^+{HOME}` | Select from current to first |
| Select to last | Ctrl+Shift+END | `^+{END}` | Select from current to last |

## Find and Filter

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Find | Ctrl+F | `^f` | Open Find dialog |
| Find next | F3 | `{F3}` | Find next match |
| Find previous | Shift+F3 | `+{F3}` | Find previous match |
| Filter | Ctrl+Shift+F | `^+f` | Open filter dialog |
| Clear filter | Ctrl+Shift+R | `^+r` | Remove all filters |

## Editing

### Cell Editing

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Edit cell | F2 | `{F2}` | Enter edit mode |
| Confirm edit | ENTER | `{ENTER}` | Save and move down |
| Cancel edit | ESC | `{ESC}` | Discard changes |
| Select all text | Ctrl+A | `^a` | When in edit mode |
| Copy | Ctrl+C | `^c` | Copy selection |
| Cut | Ctrl+X | `^x` | Cut selection |
| Paste | Ctrl+V | `^v` | Paste clipboard |
| Undo | Ctrl+Z | `^z` | Undo last change |
| Redo | Ctrl+Y | `^y` | Redo undone change |

### Activity Operations

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Add activity | INSERT | `{INSERT}` | Add new activity below |
| Delete activity | DELETE | `{DELETE}` | Delete selected activities |
| Duplicate | Ctrl+D | `^d` | Duplicate selected |
| Indent | Ctrl+RIGHT | `^{RIGHT}` | Indent in WBS |
| Outdent | Ctrl+LEFT | `^{LEFT}` | Outdent in WBS |

## Scheduling

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Schedule (F9) | F9 | `{F9}` | Run schedule calculation |
| Level resources | Shift+F9 | `+{F9}` | Level resources |
| Schedule check | Ctrl+F9 | `^{F9}` | Run schedule check |

## Views and Layouts

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Refresh | F5 | `{F5}` | Refresh current view |
| Toggle Gantt | Ctrl+G | `^g` | Show/hide Gantt chart |
| Zoom in | Ctrl++ | `^{ADD}` | Zoom in timeline |
| Zoom out | Ctrl+- | `^{SUBTRACT}` | Zoom out timeline |
| Fit timeline | Ctrl+0 | `^0` | Fit project to view |

## Dialog Shortcuts

### Common Dialog Buttons

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| OK / Accept | ENTER | `{ENTER}` | Confirm dialog |
| Cancel / Close | ESC | `{ESC}` | Cancel dialog |
| Apply | Alt+A | `%a` | Apply without closing |
| Help | F1 | `{F1}` | Open help |

### Menu Access

| Menu | Shortcut | pywinauto Syntax | Notes |
|------|----------|------------------|-------|
| File | Alt+F | `%f` | File menu |
| Edit | Alt+E | `%e` | Edit menu |
| View | Alt+V | `%v` | View menu |
| Project | Alt+P | `%p` | Project menu |
| Enterprise | Alt+N | `%n` | Enterprise menu |
| Tools | Alt+T | `%t` | Tools menu |
| Help | Alt+H | `%h` | Help menu |

## File Operations

| Action | Shortcut | pywinauto Syntax | Notes |
|--------|----------|------------------|-------|
| Open project | Ctrl+O | `^o` | Open project dialog |
| Close project | Ctrl+W | `^w` | Close current project |
| Save | Ctrl+S | `^s` | Save changes |
| Print | Ctrl+P | `^p` | Print dialog |
| Print Preview | Ctrl+Shift+P | `^+p` | Print preview |
| Export | Ctrl+E | `^e` | Export dialog |

## Special Keys Syntax (pywinauto)

| Key | Syntax | Description |
|-----|--------|-------------|
| Ctrl | `^` | Control modifier |
| Alt | `%` | Alt modifier |
| Shift | `+` | Shift modifier |
| Enter | `{ENTER}` | Enter key |
| Escape | `{ESC}` | Escape key |
| Tab | `{TAB}` | Tab key |
| F1-F12 | `{F1}` to `{F12}` | Function keys |
| Arrow keys | `{UP}`, `{DOWN}`, `{LEFT}`, `{RIGHT}` | Arrow keys |
| Home/End | `{HOME}`, `{END}` | Home and End |
| Page Up/Down | `{PGUP}`, `{PGDN}` | Page navigation |
| Insert | `{INSERT}` | Insert key |
| Delete | `{DELETE}` | Delete key |
| Backspace | `{BACKSPACE}` | Backspace key |
| Space | `{SPACE}` or ` ` | Space bar |

## Usage Examples

### Select Activity and Edit Duration

```python
# Open Find dialog
main_window.type_keys("^f")
time.sleep(0.3)

# Type activity ID and find
main_window.type_keys("A1010{ENTER}")
time.sleep(0.2)

# Close Find dialog
main_window.type_keys("{ESC}")

# Navigate to Duration column (assuming 3rd column)
main_window.type_keys("{HOME}")  # First column
main_window.type_keys("{TAB}{TAB}{TAB}")  # To duration

# Edit
main_window.type_keys("{F2}")  # Enter edit mode
main_window.type_keys("15d")   # Type new value
main_window.type_keys("{ENTER}")  # Confirm
```

### Run Schedule Calculation

```python
# Press F9 to schedule
main_window.type_keys("{F9}")
time.sleep(0.5)

# Wait for schedule dialog
schedule_dlg = main_window.child_window(title="Schedule")
schedule_dlg.wait("visible", timeout=5)

# Click Schedule button (or press Enter if focused)
main_window.type_keys("{ENTER}")
```

### Navigate WBS Hierarchy

```python
# Go to first activity
main_window.type_keys("^{HOME}")

# Collapse all WBS nodes
main_window.type_keys("^+{SUBTRACT}")

# Expand current node
main_window.type_keys("{ADD}")

# Expand all
main_window.type_keys("^+{ADD}")
```
