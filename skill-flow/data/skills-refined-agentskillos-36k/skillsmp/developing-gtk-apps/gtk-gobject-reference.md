# GObject Reference for GTK 4/Libadwaita (Python)

Patterns for creating custom GObject classes, properties, signals, and template widgets.

## Custom GObject Classes

### Basic Subclass

```python
from gi.repository import GObject

class MyModel(GObject.Object):
    """Simple GObject subclass."""

    def __init__(self):
        super().__init__()
        self._name = ""

    @GObject.Property(type=str, default="")
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
```

### With Type Registration (Required for Templates)

```python
from gi.repository import GObject, Gtk, Adw

@Gtk.Template(resource="/com/example/MyApp/window.ui")
class MyWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MyWindow"  # Must match template name

    # Template children
    header_bar = Gtk.Template.Child()
    content_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_button_clicked(self, button):
        print("Button clicked!")
```

## Properties

### Basic Property Types

```python
from gi.repository import GObject

class MyObject(GObject.Object):
    # String property
    @GObject.Property(type=str, default="")
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Integer property with range
    @GObject.Property(type=int, minimum=0, maximum=100, default=50)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value

    # Boolean property
    @GObject.Property(type=bool, default=False)
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value

    # Float property
    @GObject.Property(type=float, default=1.0)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
```

### Read-Only Properties

```python
class MyObject(GObject.Object):
    @GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)
    def computed_value(self):
        return f"{self._name}-{self._id}"
```

### Object/Boxed Properties

```python
from gi.repository import GObject, Gio

class MyObject(GObject.Object):
    # Object property (another GObject)
    @GObject.Property(type=Gio.File)
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    # GObject.Object for generic objects
    @GObject.Property(type=GObject.Object)
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
```

### Notify on Change

```python
class MyObject(GObject.Object):
    def __init__(self):
        super().__init__()
        self._items = []

    @GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)
    def count(self):
        return len(self._items)

    def add_item(self, item):
        self._items.append(item)
        self.notify("count")  # Manually notify property changed
```

## Signals

### Defining Custom Signals

```python
from gi.repository import GObject

class MyObject(GObject.Object):
    __gsignals__ = {
        # Signal with no parameters
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),

        # Signal with parameters
        "item-added": (GObject.SignalFlags.RUN_LAST, None, (str,)),

        # Signal with multiple parameters
        "item-moved": (GObject.SignalFlags.RUN_LAST, None, (int, int)),

        # Signal with return value
        "validate": (GObject.SignalFlags.RUN_LAST, bool, (str,)),
    }

    def add_item(self, name):
        self._items.append(name)
        self.emit("item-added", name)
        self.emit("changed")

    def move_item(self, from_idx, to_idx):
        # Move logic...
        self.emit("item-moved", from_idx, to_idx)

    def set_value(self, value):
        if self.emit("validate", value):
            self._value = value
```

### Connecting to Signals

```python
def on_item_added(obj, name):
    print(f"Added: {name}")

def on_item_moved(obj, from_idx, to_idx):
    print(f"Moved from {from_idx} to {to_idx}")

my_object = MyObject()
my_object.connect("item-added", on_item_added)
my_object.connect("item-moved", on_item_moved)
```

### Signal with Accumulator

```python
class MyObject(GObject.Object):
    __gsignals__ = {
        # Stop emission on first True return
        "should-close": (
            GObject.SignalFlags.RUN_LAST,
            bool,
            (),
            GObject.signal_accumulator_true_handled
        ),
    }
```

## Template Classes

### With Blueprint UI

```blueprint
// window.blp
using Gtk 4.0;
using Adw 1;

template $MyWindow: Adw.ApplicationWindow {
  title: "My App";

  content: Adw.ToolbarView {
    [top]
    Adw.HeaderBar {}

    content: Gtk.Box main_box {
      orientation: vertical;
      spacing: 12;

      Gtk.Button save_button {
        label: "Save";
        clicked => $on_save_clicked();
      }
    };
  };
}
```

```python
# window.py
from gi.repository import Gtk, Adw

@Gtk.Template(resource="/com/example/MyApp/window.ui")
class MyWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MyWindow"

    main_box = Gtk.Template.Child()
    save_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_save_clicked(self, button):
        self.save()
```

### With XML UI

```xml
<!-- window.ui -->
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <template class="MyWindow" parent="AdwApplicationWindow">
    <property name="title">My App</property>
    <child>
      <object class="AdwToolbarView">
        <child type="top">
          <object class="AdwHeaderBar"/>
        </child>
        <property name="content">
          <object class="GtkBox" id="main_box">
            <property name="orientation">vertical</property>
            <property name="spacing">12</property>
            <child>
              <object class="GtkButton" id="save_button">
                <property name="label">Save</property>
                <signal name="clicked" handler="on_save_clicked"/>
              </object>
            </child>
          </object>
        </property>
      </object>
    </child>
  </template>
</interface>
```

## List Models

### Implementing Gio.ListModel

```python
from gi.repository import GObject, Gio

class Item(GObject.Object):
    def __init__(self, title):
        super().__init__()
        self._title = title

    @GObject.Property(type=str)
    def title(self):
        return self._title


class ItemListModel(GObject.Object, Gio.ListModel):
    def __init__(self):
        super().__init__()
        self._items = []

    def do_get_item_type(self):
        return Item

    def do_get_n_items(self):
        return len(self._items)

    def do_get_item(self, position):
        if position < len(self._items):
            return self._items[position]
        return None

    def append(self, item):
        position = len(self._items)
        self._items.append(item)
        self.items_changed(position, 0, 1)

    def remove(self, position):
        if position < len(self._items):
            del self._items[position]
            self.items_changed(position, 1, 0)

    def clear(self):
        n = len(self._items)
        self._items.clear()
        self.items_changed(0, n, 0)
```

### Using with ListView/GridView

```python
# Create model
model = ItemListModel()
model.append(Item("First"))
model.append(Item("Second"))

# Selection model
selection = Gtk.SingleSelection(model=model)

# Factory for items
factory = Gtk.SignalListItemFactory()

def on_setup(factory, list_item):
    label = Gtk.Label()
    list_item.set_child(label)

def on_bind(factory, list_item):
    label = list_item.get_child()
    item = list_item.get_item()
    label.set_label(item.title)

factory.connect("setup", on_setup)
factory.connect("bind", on_bind)

# List view
list_view = Gtk.ListView(model=selection, factory=factory)
```

### Real-World Example: Todo List Model

Complete todo list with persistence, filtering, and property notifications:

```python
from gi.repository import GObject, Gio, GLib
import json
import os

class TodoItem(GObject.Object):
    """A single todo item with observable properties."""

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, title="", completed=False, item_id=None):
        super().__init__()
        self._id = item_id or str(GLib.uuid_string_random())
        self._title = title
        self._completed = completed
        self._created_at = GLib.DateTime.new_now_local().to_unix()

    @GObject.Property(type=str)
    def id(self):
        return self._id

    @GObject.Property(type=str, default="")
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if self._title != value:
            self._title = value
            self.emit("changed")

    @GObject.Property(type=bool, default=False)
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        if self._completed != value:
            self._completed = value
            self.emit("changed")

    @GObject.Property(type=int)
    def created_at(self):
        return self._created_at

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "completed": self._completed,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data):
        item = cls(
            title=data.get("title", ""),
            completed=data.get("completed", False),
            item_id=data.get("id"),
        )
        item._created_at = data.get("created_at", item._created_at)
        return item


class TodoListModel(GObject.Object, Gio.ListModel):
    """Observable list model for todo items with filtering and persistence."""

    __gsignals__ = {
        "items-changed-external": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, data_file=None):
        super().__init__()
        self._items = []
        self._item_handlers = {}  # Track signal handlers for cleanup
        self._data_file = data_file or os.path.join(
            GLib.get_user_data_dir(), "myapp", "todos.json"
        )

    # --- Gio.ListModel interface ---

    def do_get_item_type(self):
        return TodoItem

    def do_get_n_items(self):
        return len(self._items)

    def do_get_item(self, position):
        if 0 <= position < len(self._items):
            return self._items[position]
        return None

    # --- CRUD operations ---

    def add(self, title):
        """Add a new todo item."""
        item = TodoItem(title=title)
        self._connect_item(item)
        position = len(self._items)
        self._items.append(item)
        self.items_changed(position, 0, 1)
        self._auto_save()
        return item

    def remove(self, item):
        """Remove a todo item."""
        try:
            position = self._items.index(item)
            self._disconnect_item(item)
            del self._items[position]
            self.items_changed(position, 1, 0)
            self._auto_save()
            return True
        except ValueError:
            return False

    def remove_at(self, position):
        """Remove item at position."""
        if 0 <= position < len(self._items):
            item = self._items[position]
            self._disconnect_item(item)
            del self._items[position]
            self.items_changed(position, 1, 0)
            self._auto_save()
            return True
        return False

    def clear_completed(self):
        """Remove all completed items."""
        # Work backwards to avoid index shifting
        removed = 0
        for i in range(len(self._items) - 1, -1, -1):
            if self._items[i].completed:
                self._disconnect_item(self._items[i])
                del self._items[i]
                self.items_changed(i, 1, 0)
                removed += 1
        if removed > 0:
            self._auto_save()
        return removed

    def reorder(self, from_pos, to_pos):
        """Move item from one position to another."""
        if from_pos == to_pos:
            return
        if not (0 <= from_pos < len(self._items)):
            return
        if not (0 <= to_pos < len(self._items)):
            return

        item = self._items.pop(from_pos)
        self._items.insert(to_pos, item)

        # Notify of changes
        min_pos = min(from_pos, to_pos)
        max_pos = max(from_pos, to_pos)
        self.items_changed(min_pos, max_pos - min_pos + 1, max_pos - min_pos + 1)
        self._auto_save()

    # --- Item change tracking ---

    def _connect_item(self, item):
        handler_id = item.connect("changed", self._on_item_changed)
        self._item_handlers[item] = handler_id

    def _disconnect_item(self, item):
        if item in self._item_handlers:
            item.disconnect(self._item_handlers[item])
            del self._item_handlers[item]

    def _on_item_changed(self, item):
        """Called when any item's properties change."""
        try:
            position = self._items.index(item)
            # Notify that item at position changed (removed 1, added 1 = same item updated)
            self.items_changed(position, 1, 1)
            self._auto_save()
        except ValueError:
            pass

    # --- Computed properties ---

    @GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)
    def pending_count(self):
        return sum(1 for item in self._items if not item.completed)

    @GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)
    def completed_count(self):
        return sum(1 for item in self._items if item.completed)

    # --- Persistence ---

    def _auto_save(self):
        """Save after changes (debounce in production)."""
        self.save()

    def save(self):
        """Save todos to disk."""
        os.makedirs(os.path.dirname(self._data_file), exist_ok=True)
        data = [item.to_dict() for item in self._items]
        with open(self._data_file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load todos from disk."""
        if not os.path.exists(self._data_file):
            return

        try:
            with open(self._data_file, "r") as f:
                data = json.load(f)

            # Clear existing
            old_count = len(self._items)
            for item in self._items:
                self._disconnect_item(item)
            self._items.clear()

            # Load new
            for item_data in data:
                item = TodoItem.from_dict(item_data)
                self._connect_item(item)
                self._items.append(item)

            self.items_changed(0, old_count, len(self._items))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading todos: {e}")


# --- Filtered view for "active" or "completed" tabs ---

def create_filtered_model(model, show_completed=None):
    """Create a filtered view of the todo list.

    Args:
        model: TodoListModel instance
        show_completed: None=all, True=completed only, False=active only
    """
    if show_completed is None:
        return model

    def filter_func(item):
        return item.completed == show_completed

    custom_filter = Gtk.CustomFilter.new(filter_func)
    return Gtk.FilterListModel(model=model, filter=custom_filter)
```

**Usage in a window:**

```python
class TodoWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = TodoListModel()
        self.model.load()

        # Selection model for ListView
        self.selection = Gtk.NoSelection(model=self.model)

        # Factory for todo rows
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_setup)
        factory.connect("bind", self._on_bind)

        # ListView
        self.list_view = Gtk.ListView(model=self.selection, factory=factory)
        # ... rest of UI setup

    def _on_setup(self, factory, list_item):
        row = Adw.ActionRow()
        check = Gtk.CheckButton()
        row.add_prefix(check)
        row.check = check  # Store reference
        list_item.set_child(row)

    def _on_bind(self, factory, list_item):
        row = list_item.get_child()
        item = list_item.get_item()

        row.set_title(item.title)
        row.check.set_active(item.completed)

        # Bind checkbox to item's completed property
        row.check.connect("toggled", lambda c: setattr(item, "completed", c.get_active()))
```

## Common Patterns

### Weak References for Callbacks

```python
import weakref
from gi.repository import GLib

class MyWindow(Adw.ApplicationWindow):
    def start_timer(self):
        # Use weak reference to avoid preventing garbage collection
        weak_self = weakref.ref(self)

        def on_timeout():
            self = weak_self()
            if self is None:
                return False  # Stop timer, window was destroyed
            self.update()
            return True  # Continue timer

        GLib.timeout_add_seconds(1, on_timeout)
```

### Property Change Batching

```python
class MyModel(GObject.Object):
    def update_all(self, name, value, active):
        # Freeze notifications during batch update
        self.freeze_notify()
        try:
            self.name = name
            self.value = value
            self.active = active
        finally:
            self.thaw_notify()
        # All notifications sent at once after thaw
```

### Dispose Pattern

```python
class MyObject(GObject.Object):
    def __init__(self):
        super().__init__()
        self._connections = []
        self._disposed = False

    def connect_to(self, obj, signal, handler):
        handler_id = obj.connect(signal, handler)
        self._connections.append((obj, handler_id))
        return handler_id

    def do_dispose(self):
        if self._disposed:
            return
        self._disposed = True

        # Disconnect all signal handlers
        for obj, handler_id in self._connections:
            if obj.handler_is_connected(handler_id):
                obj.disconnect(handler_id)
        self._connections.clear()

        # Chain up
        GObject.Object.do_dispose(self)
```

## GTK 4 Widget Subclassing

### Custom Widget with Properties

```python
from gi.repository import Gtk, GObject

class CustomButton(Gtk.Button):
    __gtype_name__ = "CustomButton"

    def __init__(self):
        super().__init__()
        self._count = 0
        self.connect("clicked", self._on_clicked)

    @GObject.Property(type=int, minimum=0, default=0)
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        self.set_label(f"Clicked {value} times")

    def _on_clicked(self, button):
        self.count += 1
```

### Composite Widget

```python
@Gtk.Template(string="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <template class="SearchEntry" parent="GtkBox">
    <child>
      <object class="GtkEntry" id="entry">
        <property name="hexpand">true</property>
      </object>
    </child>
    <child>
      <object class="GtkButton" id="clear_btn">
        <property name="icon-name">edit-clear-symbolic</property>
      </object>
    </child>
  </template>
</interface>
""")
class SearchEntry(Gtk.Box):
    __gtype_name__ = "SearchEntry"

    entry = Gtk.Template.Child()
    clear_btn = Gtk.Template.Child()

    __gsignals__ = {
        "search-changed": (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }

    def __init__(self):
        super().__init__()
        self.entry.connect("changed", self._on_entry_changed)
        self.clear_btn.connect("clicked", self._on_clear_clicked)

    def _on_entry_changed(self, entry):
        self.emit("search-changed", entry.get_text())

    def _on_clear_clicked(self, button):
        self.entry.set_text("")
```

## Type Registration Order

**Critical:** Types must be registered before they're used in templates.

```python
# main.py
from gi.repository import Gtk, Adw, Gio

# Register types BEFORE creating application
from .widgets.custom_button import CustomButton
from .widgets.search_entry import SearchEntry
from .window import MyWindow  # Template uses CustomButton

class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")

    def do_activate(self):
        win = MyWindow(application=self)
        win.present()
```

## Debugging GObject Issues

```python
# Check if property exists
print(obj.find_property("name"))

# List all properties
for prop in obj.list_properties():
    print(f"{prop.name}: {prop.value_type}")

# Check signal existence
print(GObject.signal_lookup("clicked", Gtk.Button))

# Trace signal emissions
def trace_handler(*args):
    print(f"Signal emitted with args: {args}")

obj.connect("changed", trace_handler)
```
