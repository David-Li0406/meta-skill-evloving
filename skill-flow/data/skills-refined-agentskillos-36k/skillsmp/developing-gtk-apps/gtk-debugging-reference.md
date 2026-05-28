# GTK Debugging Reference

Environment variables, GTK Inspector, and debugging tools for GTK 4/libadwaita apps.

## Environment Variables

```bash
# Debug GTK warnings
GTK_DEBUG=interactive myapp  # Opens inspector

# Debug GLib
G_MESSAGES_DEBUG=all myapp  # All debug messages
G_MESSAGES_DEBUG=Gtk myapp  # Only GTK messages

# Debug GSettings
GSETTINGS_BACKEND=memory myapp  # Don't persist settings

# Debug threading issues
G_DEBUG=fatal-criticals myapp  # Abort on critical warnings

# Force specific display backend
GDK_BACKEND=wayland myapp
GDK_BACKEND=x11 myapp
```

## GTK Inspector

```python
# Enable inspector in code
Gtk.Window.set_interactive_debugging(True)

# Or press Ctrl+Shift+D in app (if enabled)
```

### Inspector Features

- **Objects:** Browse widget tree, inspect properties
- **CSS:** Live CSS editing, see applied styles
- **Recorder:** Record and replay rendering
- **Statistics:** Frame timing, memory usage
- **Actions:** View and trigger actions
- **Logs:** GLib log messages

## Adaptive Preview (libadwaita 1.7+)

```bash
# Preview app on different device sizes
# Press Ctrl+Shift+M in inspector to open adaptive preview
# Features: device bezels, scaling, screenshots
```

## Debugging Common Issues

### UI Not Updating

```python
# Check if on main thread
import threading
print(f"Current thread: {threading.current_thread().name}")

# Force UI update
from gi.repository import GLib
while GLib.MainContext.default().pending():
    GLib.MainContext.default().iteration(False)
```

### Signal Not Firing

```python
# Check signal exists
from gi.repository import GObject
signal_id = GObject.signal_lookup("clicked", Gtk.Button)
print(f"Signal exists: {signal_id != 0}")

# Trace all signals
def trace_handler(*args):
    print(f"Signal received: {args}")
widget.connect("notify", trace_handler)
```

### Memory Leaks

```python
import gc
import weakref

# Track object destruction
def check_cleanup():
    weak_ref = weakref.ref(widget)
    widget.destroy()
    gc.collect()
    print(f"Widget destroyed: {weak_ref() is None}")
```

### CSS Not Applying

```python
# Check CSS load errors
css_provider = Gtk.CssProvider()
try:
    css_provider.load_from_string("invalid {")
except GLib.Error as e:
    print(f"CSS error: {e.message}")

# Debug CSS classes
for css_class in widget.get_css_classes():
    print(f"CSS class: {css_class}")
```

## Logging

```python
from gi.repository import GLib

# Set log handler
def log_handler(domain, level, message, user_data):
    print(f"[{domain}] {level}: {message}")

GLib.log_set_handler(None, GLib.LogLevelFlags.LEVEL_WARNING, log_handler, None)

# Log from your code
GLib.log("myapp", GLib.LogLevelFlags.LEVEL_DEBUG, "Debug message")
GLib.log("myapp", GLib.LogLevelFlags.LEVEL_WARNING, "Warning message")
```

## Profiling

```bash
# GTK frame timing
GTK_DEBUG=snapshot myapp

# Sysprof integration
sysprof-cli -c myapp

# Python profiling
python -m cProfile -o profile.out myapp
```

## Inspecting at Runtime

```python
# In a running app, access inspector:
Gtk.Window.set_interactive_debugging(True)

# Inspect widget hierarchy
def print_tree(widget, indent=0):
    print("  " * indent + type(widget).__name__)
    if hasattr(widget, 'get_first_child'):
        child = widget.get_first_child()
        while child:
            print_tree(child, indent + 1)
            child = child.get_next_sibling()

print_tree(window)
```

## GDB Integration

```bash
# Run with debugger
gdb --args python myapp.py

# Useful GDB commands for GTK
# (gdb) break g_log
# (gdb) break gtk_widget_realize
# (gdb) call gtk_window_set_interactive_debugging(1)
```

## Testing Without Display

```bash
# Virtual framebuffer for CI
xvfb-run pytest tests/

# Broadway backend (web-based)
GDK_BACKEND=broadway broadwayd :5 &
GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 myapp
# Access at http://localhost:8080
```
