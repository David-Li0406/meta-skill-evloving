# GTK DBus Reference

DBus activation and background services for GTK 4/libadwaita apps.

## When to Use DBus Activation

- App needs to run tasks when not visible (sync, downloads)
- Other apps need to communicate with your app
- System services need to trigger your app (notifications, files)
- Startup performance optimization (delay full UI until needed)

## DBus Service File

```ini
# data/com.example.MyApp.service
[D-BUS Service]
Name=com.example.MyApp
Exec=/usr/bin/myapp --gapplication-service
```

**Install with meson:**
```meson
# data/meson.build
install_data(
    'com.example.MyApp.service',
    install_dir: get_option('datadir') / 'dbus-1' / 'services'
)
```

## Application with DBus Activation

```python
from gi.repository import Gio, GLib, Adw

class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.example.MyApp",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.add_main_option(
            "gapplication-service",
            0,
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Run as background service",
            None
        )

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("gapplication-service"):
            # Running as service - don't show UI
            self.hold()  # Keep alive until explicitly released
            return 0

        # Normal launch - show window
        self.activate()
        return 0

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()
```

## Exporting DBus Interface

```python
# Define interface in XML
DBUS_INTERFACE = """
<node>
  <interface name="com.example.MyApp">
    <method name="Sync">
      <arg type="b" name="result" direction="out"/>
    </method>
    <method name="AddItem">
      <arg type="s" name="title" direction="in"/>
      <arg type="s" name="item_id" direction="out"/>
    </method>
    <property name="ItemCount" type="u" access="read"/>
    <signal name="ItemAdded">
      <arg type="s" name="item_id"/>
    </signal>
  </interface>
</node>
"""

class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")
        self._dbus_id = 0

    def do_dbus_register(self, connection, object_path):
        # Called when app registers on session bus
        introspection = Gio.DBusNodeInfo.new_for_xml(DBUS_INTERFACE)

        self._dbus_id = connection.register_object(
            object_path,
            introspection.interfaces[0],
            self._handle_method_call,
            self._handle_get_property,
            None  # set_property handler
        )
        return Adw.Application.do_dbus_register(self, connection, object_path)

    def do_dbus_unregister(self, connection, object_path):
        if self._dbus_id:
            connection.unregister_object(self._dbus_id)
        Adw.Application.do_dbus_unregister(self, connection, object_path)

    def _handle_method_call(self, connection, sender, path, interface,
                            method, params, invocation):
        if method == "Sync":
            result = self.perform_sync()
            invocation.return_value(GLib.Variant("(b)", (result,)))
        elif method == "AddItem":
            title = params.unpack()[0]
            item_id = self.add_item(title)
            invocation.return_value(GLib.Variant("(s)", (item_id,)))
            # Emit signal
            connection.emit_signal(
                None, path, interface, "ItemAdded",
                GLib.Variant("(s)", (item_id,))
            )
        else:
            invocation.return_error_literal(
                Gio.dbus_error_quark(),
                Gio.DBusError.UNKNOWN_METHOD,
                f"Unknown method: {method}"
            )

    def _handle_get_property(self, connection, sender, path, interface, prop):
        if prop == "ItemCount":
            return GLib.Variant("u", self.get_item_count())
        return None
```

## Calling DBus Methods from Other Apps

```python
from gi.repository import Gio, GLib

def call_myapp_sync():
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

    result = bus.call_sync(
        "com.example.MyApp",           # Bus name
        "/com/example/MyApp",          # Object path
        "com.example.MyApp",           # Interface
        "Sync",                        # Method
        None,                          # Parameters
        GLib.VariantType("(b)"),       # Return type
        Gio.DBusCallFlags.NONE,
        -1,                            # Timeout (-1 = default)
        None                           # Cancellable
    )
    return result.unpack()[0]

# Async version
def call_myapp_sync_async(callback):
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

    bus.call(
        "com.example.MyApp",
        "/com/example/MyApp",
        "com.example.MyApp",
        "Sync",
        None,
        GLib.VariantType("(b)"),
        Gio.DBusCallFlags.NONE,
        -1,
        None,
        callback
    )
```

## Background Portal (Flatpak)

For Flatpak apps, use the Background portal to request background permission:

```python
from gi.repository import Gio, GLib

def request_background_permission(window):
    """Request permission to run in background."""
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

    # Get window handle for portal
    handle = ""  # Empty for non-portal-aware windows

    options = GLib.Variant("a{sv}", {
        "reason": GLib.Variant("s", "Sync data in background"),
        "autostart": GLib.Variant("b", False),
        "commandline": GLib.Variant("as", ["myapp", "--gapplication-service"]),
    })

    try:
        result = bus.call_sync(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Background",
            "RequestBackground",
            GLib.Variant("(sa{sv})", (handle, options)),
            GLib.VariantType("(o)"),
            Gio.DBusCallFlags.NONE,
            -1,
            None
        )
        # Result is a request object path for async response
        return True
    except GLib.Error as e:
        print(f"Background permission denied: {e.message}")
        return False
```

**Flatpak manifest permission:**
```json
{
    "finish-args": [
        "--talk-name=org.freedesktop.portal.Background"
    ]
}
```

## Service Lifecycle

```python
class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")
        self._hold_count = 0

    def start_background_task(self):
        """Keep app alive during background work."""
        self.hold()
        self._hold_count += 1
        # Start async work...

    def finish_background_task(self):
        """Release hold when work completes."""
        self._hold_count -= 1
        self.release()
        # If no windows and no holds, app will exit

    def do_shutdown(self):
        # Cleanup background tasks
        self.cancel_pending_operations()
        Adw.Application.do_shutdown(self)
```

## Autostart (Non-Flatpak)

```ini
# ~/.config/autostart/com.example.MyApp.desktop
[Desktop Entry]
Type=Application
Name=My App Background Service
Exec=myapp --gapplication-service
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
```

## Listening for Signals

```python
def listen_for_item_added():
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

    def on_signal(connection, sender, path, interface, signal, params):
        item_id = params.unpack()[0]
        print(f"Item added: {item_id}")

    bus.signal_subscribe(
        "com.example.MyApp",          # Sender
        "com.example.MyApp",          # Interface
        "ItemAdded",                  # Signal
        "/com/example/MyApp",         # Path
        None,                         # arg0
        Gio.DBusSignalFlags.NONE,
        on_signal
    )
```

## DBus Type Signatures

| Type | Signature | Python |
|------|-----------|--------|
| Boolean | `b` | `bool` |
| Int32 | `i` | `int` |
| UInt32 | `u` | `int` |
| Int64 | `x` | `int` |
| UInt64 | `t` | `int` |
| Double | `d` | `float` |
| String | `s` | `str` |
| Object Path | `o` | `str` |
| Array | `a` | `list` |
| Dict | `a{sv}` | `dict` |
| Tuple | `(...)` | `tuple` |

```python
# Examples
GLib.Variant("s", "hello")                    # String
GLib.Variant("i", 42)                         # Int32
GLib.Variant("as", ["a", "b", "c"])          # Array of strings
GLib.Variant("(si)", ("hello", 42))          # Tuple
GLib.Variant("a{sv}", {"key": GLib.Variant("s", "value")})  # Dict
```
