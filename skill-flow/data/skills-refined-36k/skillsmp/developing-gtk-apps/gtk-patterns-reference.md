# GTK Patterns Reference

Common patterns for actions, GSettings, resources, Blueprint, and file operations in GTK 4/libadwaita apps.

## Signals and Properties

### Connecting Signals

```python
# Standard connection
button.connect("clicked", self.on_button_clicked)

# With user data
button.connect("clicked", self.on_button_clicked, extra_data)

# Connect after (runs after default handler)
widget.connect_after("signal-name", handler)
```

### Disconnecting - Prevent Memory Leaks

```python
class MyWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.handler_ids = []

        # Track handlers
        handler_id = some_object.connect("changed", self.on_changed)
        self.handler_ids.append((some_object, handler_id))

    def do_close_request(self):
        # Disconnect all handlers
        for obj, handler_id in self.handler_ids:
            obj.disconnect(handler_id)
        return False  # Allow close
```

### Property Bindings

```python
# One-way binding
source.bind_property(
    "active",              # source property
    target, "sensitive",   # target object, property
    GObject.BindingFlags.SYNC_CREATE
)

# Two-way binding
entry.bind_property(
    "text",
    model, "name",
    GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE
)

# With transform
def transform_to(binding, value):
    return value.upper()

source.bind_property_full(
    "text", target, "label",
    GObject.BindingFlags.SYNC_CREATE,
    transform_to, None
)
```

## Actions

### Application vs Window Actions

```python
class MyApp(Adw.Application):
    def do_startup(self):
        Adw.Application.do_startup(self)

        # App-level actions (app.action-name)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda a, p: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Control>q"])

class MyWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Window-level actions (win.action-name)
        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.on_save)
        self.add_action(save_action)
        self.get_application().set_accels_for_action("win.save", ["<Control>s"])
```

### Stateful Actions (Toggles, Radio)

```python
# Toggle action
dark_action = Gio.SimpleAction.new_stateful(
    "dark-mode",
    None,
    GLib.Variant.new_boolean(False)
)
dark_action.connect("change-state", self.on_dark_mode_changed)
self.add_action(dark_action)

def on_dark_mode_changed(self, action, value):
    action.set_state(value)
    is_dark = value.get_boolean()
    # Apply dark mode

# Radio action (string state)
view_action = Gio.SimpleAction.new_stateful(
    "view",
    GLib.VariantType.new("s"),
    GLib.Variant.new_string("grid")
)
view_action.connect("change-state", self.on_view_changed)
```

### Parameterized Actions

```python
# Action with parameter
open_action = Gio.SimpleAction.new(
    "open-item",
    GLib.VariantType.new("s")  # String parameter
)
open_action.connect("activate", self.on_open_item)
self.add_action(open_action)

def on_open_item(self, action, parameter):
    item_id = parameter.get_string()
    self.open_item(item_id)

# Trigger from code
self.activate_action("open-item", GLib.Variant.new_string("item-123"))
```

## GSettings

### Schema Definition (gschemas.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<schemalist>
  <schema id="com.example.MyApp" path="/com/example/MyApp/">
    <key name="window-width" type="i">
      <default>800</default>
      <summary>Window width</summary>
    </key>
    <key name="window-height" type="i">
      <default>600</default>
    </key>
    <key name="dark-mode" type="b">
      <default>false</default>
    </key>
    <key name="recent-files" type="as">
      <default>[]</default>
    </key>
  </schema>
</schemalist>
```

### Using GSettings

```python
class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")
        self.settings = Gio.Settings.new("com.example.MyApp")

    def do_activate(self):
        win = MyWindow(application=self, settings=self.settings)
        win.present()

class MyWindow(Adw.ApplicationWindow):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings

        # Bind settings to properties
        self.settings.bind(
            "window-width", self, "default-width",
            Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "window-height", self, "default-height",
            Gio.SettingsBindFlags.DEFAULT
        )

        # Read/write manually
        dark = self.settings.get_boolean("dark-mode")
        self.settings.set_boolean("dark-mode", True)

        # Listen for changes
        self.settings.connect("changed::dark-mode", self.on_dark_changed)
```

### Compile Schemas (Development)

```bash
# Compile for local testing
glib-compile-schemas /path/to/schemas/

# Or set search path
export GSETTINGS_SCHEMA_DIR=/path/to/schemas/
```

## Resources (GResource)

### Resource Definition (resources.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <gresource prefix="/com/example/MyApp">
    <file preprocess="xml-stripblanks">window.ui</file>
    <file>style.css</file>
    <file>icons/symbolic/my-icon-symbolic.svg</file>
  </gresource>
</gresources>
```

### Compile and Load

```bash
# Compile resources
glib-compile-resources --target=resources.gresource resources.xml
```

```python
# Load at startup
resource = Gio.Resource.load("resources.gresource")
Gio.resources_register(resource)

# Or compile inline (development)
resource = Gio.resource_load(
    os.path.join(os.path.dirname(__file__), "resources.gresource")
)
Gio.resources_register(resource)
```

### Using Resources

```python
# Load UI from resource
builder = Gtk.Builder.new_from_resource("/com/example/MyApp/window.ui")

# Load CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_resource("/com/example/MyApp/style.css")
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
```

## Blueprint (UI Definition)

Blueprint is a modern, declarative markup language for GTK 4 UIs. Cleaner than XML, with IDE support for completion and error checking.

**Note:** For which widgets to use in your Blueprint templates, see `designing-gnome-ui` skill.

### Blueprint vs XML

```
<!-- XML (verbose) -->
<object class="AdwHeaderBar">
  <child type="end">
    <object class="GtkMenuButton">
      <property name="icon-name">open-menu-symbolic</property>
    </object>
  </child>
</object>
```

```blueprint
// Blueprint (concise)
Adw.HeaderBar {
  [end]
  MenuButton {
    icon-name: "open-menu-symbolic";
  }
}
```

### Setup with Meson

```meson
# meson.build
gnome = import('gnome')

blueprints = files(
  'ui/window.blp',
  'ui/preferences.blp',
)

blueprint_targets = []
foreach blueprint : blueprints
  blueprint_targets += gnome.compile_resources(
    '@0@'.format(blueprint).replace('.blp', ''),
    configure_file(
      input: blueprint,
      output: '@PLAINNAME@.ui',
      command: [
        find_program('blueprint-compiler'),
        'compile',
        '--output', '@OUTPUT@',
        '@INPUT@',
      ],
    ),
  )
endforeach
```

### Port Existing XML

```bash
# Auto-convert .ui files to .blp
blueprint-compiler port window.ui
```

### Key Patterns

```blueprint
using Gtk 4.0;
using Adw 1;

template $MyWindow: Adw.ApplicationWindow {
  default-width: 800;
  default-height: 600;

  content: Adw.ToolbarView {
    [top]
    Adw.HeaderBar header_bar {}

    content: Adw.Clamp {
      maximum-size: 600;

      child: Gtk.Box {
        orientation: vertical;
        spacing: 12;

        Adw.PreferencesGroup {
          title: "Settings";

          Adw.SwitchRow dark_switch {
            title: "Dark Mode";
          }
        }
      };
    };
  };
}
```

**Property bindings:**
```blueprint
Gtk.Label {
  label: bind model.name;  // One-way binding
}

Gtk.Entry {
  text: bind model.value bidirectional;  // Two-way
}

Gtk.Button {
  sensitive: bind model.count > 0;  // Expression
}
```

### Complete Blueprint Window Template

```blueprint
// window.blp
using Gtk 4.0;
using Adw 1;

template $MyAppWindow: Adw.ApplicationWindow {
  default-width: 800;
  default-height: 600;
  title: "My App";

  content: Adw.ToastOverlay toast_overlay {
    child: Adw.ToolbarView {
      [top]
      Adw.HeaderBar {
        [start]
        Gtk.Button {
          icon-name: "list-add-symbolic";
          tooltip-text: "Add Item";
          action-name: "win.add";
        }

        [end]
        Gtk.MenuButton {
          icon-name: "open-menu-symbolic";
          tooltip-text: "Main Menu";
          menu-model: primary_menu;
        }
      }

      content: Adw.Clamp {
        maximum-size: 600;
        child: Gtk.Box {
          orientation: vertical;
          margin-top: 24;
          margin-bottom: 24;
          margin-start: 12;
          margin-end: 12;
          spacing: 24;

          Adw.PreferencesGroup {
            title: "Items";

            Adw.ActionRow {
              title: "Example Item";
              subtitle: "Click to view";
              activatable: true;

              [suffix]
              Gtk.Image {
                icon-name: "go-next-symbolic";
              }
            }
          }
        };
      };
    };
  };
}

menu primary_menu {
  section {
    item {
      label: "_Preferences";
      action: "app.preferences";
    }
    item {
      label: "_Keyboard Shortcuts";
      action: "win.show-help-overlay";
    }
    item {
      label: "_About";
      action: "app.about";
    }
  }
}
```

```python
# window.py - Load Blueprint template
@Gtk.Template(resource="/com/example/MyApp/window.ui")
class MyAppWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MyAppWindow"

    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_actions()

    def _setup_actions(self):
        add_action = Gio.SimpleAction.new("add", None)
        add_action.connect("activate", self._on_add)
        self.add_action(add_action)

    def _on_add(self, action, param):
        self.toast_overlay.add_toast(Adw.Toast(title="Item added"))
```

## File Operations with Gio

### Async File Read

```python
def load_file_async(self, path, callback):
    file = Gio.File.new_for_path(path)
    file.load_contents_async(None, callback)

def on_file_loaded(self, file, result):
    try:
        success, contents, etag = file.load_contents_finish(result)
        text = contents.decode('utf-8')
        self.process_content(text)
    except GLib.Error as e:
        self.show_error(f"Could not load file: {e.message}")
```

### Async File Write

```python
def save_file_async(self, path, content, callback):
    file = Gio.File.new_for_path(path)
    file.replace_contents_async(
        content.encode('utf-8'),
        None,  # etag
        False,  # make_backup
        Gio.FileCreateFlags.REPLACE_DESTINATION,
        None,  # cancellable
        callback
    )

def on_file_saved(self, file, result):
    try:
        file.replace_contents_finish(result)
        self.show_toast("File saved")
    except GLib.Error as e:
        self.show_error(f"Could not save: {e.message}")
```

### XDG Directories

```python
from gi.repository import GLib

# User data (persistent)
data_dir = GLib.get_user_data_dir()  # ~/.local/share
app_data = os.path.join(data_dir, "myapp")

# User config
config_dir = GLib.get_user_config_dir()  # ~/.config
app_config = os.path.join(config_dir, "myapp")

# Cache (can be deleted)
cache_dir = GLib.get_user_cache_dir()  # ~/.cache
app_cache = os.path.join(cache_dir, "myapp")

# Create if needed
os.makedirs(app_data, exist_ok=True)
```

## Common Anti-Patterns

### Blocking the Main Loop

```python
# WRONG - freezes UI
def on_button_clicked(self, button):
    time.sleep(5)  # UI frozen
    result = requests.get(url)  # UI frozen
    self.update(result)

# RIGHT - async
def on_button_clicked(self, button):
    self.spinner.start()
    threading.Thread(target=self._fetch_data).start()

def _fetch_data(self):
    result = requests.get(url)
    GLib.idle_add(self._on_data_ready, result)

def _on_data_ready(self, result):
    self.spinner.stop()
    self.update(result)
```

### Signal Handler Memory Leaks

```python
# WRONG - handler keeps window alive
self.app.settings.connect("changed", self.on_settings_changed)
# Window never garbage collected

# RIGHT - disconnect on close
def __init__(self):
    self.handler_id = self.app.settings.connect("changed", self.on_changed)

def do_close_request(self):
    self.app.settings.disconnect(self.handler_id)
    return False
```

### Forgetting to Chain Up

```python
# WRONG - breaks parent behavior
class MyApp(Adw.Application):
    def do_startup(self):
        self.setup_actions()
        # Forgot to call parent - app broken

# RIGHT - chain up
class MyApp(Adw.Application):
    def do_startup(self):
        Adw.Application.do_startup(self)  # Chain up first
        self.setup_actions()
```

### Wrong Settings Bind Flags

```python
# WRONG - allows UI to write back (if read-only setting)
settings.bind("system-setting", widget, "prop", Gio.SettingsBindFlags.DEFAULT)

# RIGHT - read-only binding
settings.bind("system-setting", widget, "prop", Gio.SettingsBindFlags.GET)
```
