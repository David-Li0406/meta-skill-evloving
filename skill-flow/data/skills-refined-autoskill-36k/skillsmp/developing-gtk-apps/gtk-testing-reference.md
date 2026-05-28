# GTK Testing Reference

Testing GTK 4/libadwaita apps with pytest, including widget testing, async operations, and GSettings.

## Test Setup with pytest

```python
# conftest.py
import pytest
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

@pytest.fixture(scope="session", autouse=True)
def gtk_init():
    """Initialize GTK once for all tests."""
    # Initialize libadwaita (also initializes GTK)
    Adw.init()
    yield

@pytest.fixture
def main_context():
    """Provide a GLib main context for async operations."""
    context = GLib.MainContext.default()
    yield context

def process_pending_events():
    """Process all pending GTK events."""
    context = GLib.MainContext.default()
    while context.pending():
        context.iteration(False)
```

## Testing Widgets

```python
# test_widgets.py
import pytest
from gi.repository import Gtk, Adw, GLib
from myapp.widgets import TodoRow

def process_pending_events():
    context = GLib.MainContext.default()
    while context.pending():
        context.iteration(False)

class TestTodoRow:
    def test_row_displays_title(self):
        row = TodoRow(title="Buy groceries")
        process_pending_events()

        assert row.get_title() == "Buy groceries"

    def test_checkbox_toggles_completed(self):
        row = TodoRow(title="Test task")
        process_pending_events()

        assert not row.completed
        row.check_button.set_active(True)
        process_pending_events()

        assert row.completed

    def test_emits_changed_signal(self):
        row = TodoRow(title="Test task")
        changed_called = False

        def on_changed(widget):
            nonlocal changed_called
            changed_called = True

        row.connect("changed", on_changed)
        row.set_title("Updated title")
        process_pending_events()

        assert changed_called
```

## Testing Windows and Dialogs

```python
# test_windows.py
from gi.repository import Gtk, Adw, Gio
from myapp.window import MainWindow
from myapp.app import MyApp

class TestMainWindow:
    def test_window_creates(self):
        app = MyApp()
        window = MainWindow(application=app)

        assert window is not None
        assert isinstance(window, Adw.ApplicationWindow)

    def test_window_has_header_bar(self):
        app = MyApp()
        window = MainWindow(application=app)
        process_pending_events()

        # Find header bar in widget tree
        content = window.get_content()
        assert content is not None

    def test_add_action_creates_item(self):
        app = MyApp()
        window = MainWindow(application=app)
        initial_count = window.model.get_n_items()

        # Activate the add action
        window.activate_action("add", None)
        process_pending_events()

        assert window.model.get_n_items() == initial_count + 1
```

## Testing Async Operations

```python
# test_async.py
from gi.repository import GLib
import threading

def wait_for_condition(condition_func, timeout_ms=1000):
    """Wait for a condition to become true, processing events."""
    context = GLib.MainContext.default()
    start = GLib.get_monotonic_time()
    timeout_us = timeout_ms * 1000

    while not condition_func():
        if GLib.get_monotonic_time() - start > timeout_us:
            raise TimeoutError("Condition not met within timeout")
        context.iteration(False)

class TestAsyncOperations:
    def test_async_load_completes(self):
        loader = DataLoader()
        loaded = False
        result_data = None

        def on_complete(data):
            nonlocal loaded, result_data
            loaded = True
            result_data = data

        loader.load_async(on_complete)

        # Wait for async operation
        wait_for_condition(lambda: loaded, timeout_ms=5000)

        assert loaded
        assert result_data is not None

    def test_cancellation_works(self):
        loader = DataLoader()
        cancelled = False

        def on_complete(data):
            pass

        def on_cancelled():
            nonlocal cancelled
            cancelled = True

        loader.load_async(on_complete, on_cancelled=on_cancelled)
        loader.cancel()

        wait_for_condition(lambda: cancelled, timeout_ms=1000)
        assert cancelled
```

## Testing GSettings

```python
# test_settings.py
import os
import tempfile
from gi.repository import Gio, GLib

class TestSettings:
    @pytest.fixture
    def memory_settings(self):
        """Use in-memory backend for tests."""
        # Set memory backend before creating settings
        os.environ["GSETTINGS_BACKEND"] = "memory"
        yield Gio.Settings.new("com.example.MyApp")
        del os.environ["GSETTINGS_BACKEND"]

    def test_default_values(self, memory_settings):
        settings = memory_settings
        assert settings.get_int("window-width") == 800
        assert settings.get_int("window-height") == 600

    def test_settings_persist(self, memory_settings):
        settings = memory_settings
        settings.set_int("window-width", 1024)

        # Re-read
        assert settings.get_int("window-width") == 1024
```

## Testing List Models

```python
# test_models.py
from myapp.models import TodoListModel, TodoItem

class TestTodoListModel:
    def test_add_item(self):
        model = TodoListModel()
        model.add("Test item")

        assert model.get_n_items() == 1
        assert model.get_item(0).title == "Test item"

    def test_items_changed_signal(self):
        model = TodoListModel()
        changes = []

        def on_items_changed(model, position, removed, added):
            changes.append((position, removed, added))

        model.connect("items-changed", on_items_changed)
        model.add("Test item")

        assert len(changes) == 1
        assert changes[0] == (0, 0, 1)  # position=0, removed=0, added=1

    def test_remove_item(self):
        model = TodoListModel()
        item = model.add("Test item")
        model.remove(item)

        assert model.get_n_items() == 0

    def test_filter_model(self):
        model = TodoListModel()
        model.add("Active task")
        completed = model.add("Done task")
        completed.completed = True

        # Filter to active only
        filter_model = Gtk.FilterListModel(model=model)
        filter_model.set_filter(
            Gtk.CustomFilter.new(lambda item: not item.completed)
        )

        assert filter_model.get_n_items() == 1
        assert filter_model.get_item(0).title == "Active task"
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with GTK debugging
GTK_DEBUG=interactive pytest tests/

# Run specific test file
pytest tests/test_widgets.py

# Run with coverage
pytest --cov=myapp tests/

# Skip slow integration tests
pytest -m "not slow" tests/
```

## Test Markers

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: integration tests")

# test_integration.py
@pytest.mark.slow
@pytest.mark.integration
def test_full_app_lifecycle():
    # Slow integration test
    pass
```

## Testing Without Display

For CI environments without a display:

```bash
# Use virtual framebuffer
xvfb-run pytest tests/

# Or with environment variable
GDK_BACKEND=broadway pytest tests/
```

## Mocking GIO Operations

```python
from unittest.mock import Mock, patch

class TestFileOperations:
    def test_load_file_error(self):
        window = MainWindow()

        # Mock Gio.File to simulate error
        with patch('gi.repository.Gio.File.new_for_path') as mock_file:
            mock_file.return_value.load_contents_finish.side_effect = GLib.Error(
                "File not found"
            )

            window.load_file("/nonexistent")
            process_pending_events()

            # Verify error handling
            assert window.error_shown
```
