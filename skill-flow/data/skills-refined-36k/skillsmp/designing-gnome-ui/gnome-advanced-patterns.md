# GNOME Advanced UI Patterns

Advanced patterns for complex GNOME applications. Read this file when building apps with drag & drop, undo/redo, tabs, media display, or complex adaptive layouts.

## When to Use This File

| Building | Read This |
|----------|-----------|
| File manager, photo organizer | Drag & Drop, Grid Selection |
| Text/document editor | Undo/Redo, Tabs |
| Browser-style multi-document app | Tabs |
| Media player, image viewer | Media Display |
| Complex dashboard | Split Views, Popovers |
| First-run experience | Welcome/Onboarding |

## Drag and Drop

### Basic Drag Source

```python
# Make a widget draggable
drag_source = Gtk.DragSource()
drag_source.set_actions(Gdk.DragAction.MOVE)

def on_prepare(source, x, y):
    # Return the data to drag
    item = get_item_at_position(x, y)
    return Gdk.ContentProvider.new_for_value(item)

def on_drag_begin(source, drag):
    # Create drag icon
    icon = Gtk.DragIcon.get_for_drag(drag)
    icon.set_child(create_drag_preview(source.get_widget()))

drag_source.connect("prepare", on_prepare)
drag_source.connect("drag-begin", on_drag_begin)
widget.add_controller(drag_source)
```

### Drop Target

```python
# Accept drops on a widget
drop_target = Gtk.DropTarget.new(MyItem, Gdk.DragAction.MOVE)

def on_drop(target, value, x, y):
    # Handle the dropped item
    item = value
    insert_at_position(item, x, y)
    return True  # Drop accepted

def on_motion(target, x, y):
    # Show drop indicator
    show_drop_indicator_at(x, y)
    return Gdk.DragAction.MOVE

drop_target.connect("drop", on_drop)
drop_target.connect("motion", on_motion)
drop_target.connect("leave", lambda t: hide_drop_indicator())
container.add_controller(drop_target)
```

### Reorderable List

```python
class ReorderableListBox(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.dragged_row = None
        self.setup_dnd()

    def setup_dnd(self):
        # Each row needs drag source
        pass  # Set up in row creation

    def create_row(self, item):
        row = Adw.ActionRow(title=item.title)

        # Drag handle
        handle = Gtk.Image(icon_name="list-drag-handle-symbolic")
        handle.add_css_class("drag-handle")
        row.add_prefix(handle)

        # Drag source on handle only
        drag_source = Gtk.DragSource()
        drag_source.set_actions(Gdk.DragAction.MOVE)

        def on_prepare(source, x, y):
            self.dragged_row = row
            return Gdk.ContentProvider.new_for_value(item)

        def on_end(source, drag, delete):
            self.dragged_row = None

        drag_source.connect("prepare", on_prepare)
        drag_source.connect("drag-end", on_end)
        handle.add_controller(drag_source)

        # Drop target on row
        drop_target = Gtk.DropTarget.new(type(item), Gdk.DragAction.MOVE)

        def on_drop(target, value, x, y):
            if self.dragged_row == row:
                return False
            # Reorder items
            self.reorder_item(value, item)
            return True

        drop_target.connect("drop", on_drop)
        row.add_controller(drop_target)

        return row

    def reorder_item(self, dragged_item, target_item):
        # Update model order
        pass
```

### File Drop from External Apps

```python
# Accept file drops from file manager
drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)

def on_drop(target, value, x, y):
    files = value.get_files()
    for file in files:
        path = file.get_path()
        import_file(path)
    return True

drop_target.connect("drop", on_drop)
window.add_controller(drop_target)
```

## Undo/Redo

### Command Pattern

```python
from abc import ABC, abstractmethod
from collections import deque

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @property
    def description(self):
        return "Action"


class UndoManager:
    def __init__(self, max_history=100):
        self.undo_stack = deque(maxlen=max_history)
        self.redo_stack = deque(maxlen=max_history)
        self.on_changed = None  # Callback for UI updates

    def execute(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self._notify()

    def undo(self):
        if not self.can_undo():
            return
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        self._notify()

    def redo(self):
        if not self.can_redo():
            return
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        self._notify()

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0

    def _notify(self):
        if self.on_changed:
            self.on_changed()
```

### Example Commands

```python
class InsertTextCommand(Command):
    def __init__(self, buffer, position, text):
        self.buffer = buffer
        self.position = position
        self.text = text

    def execute(self):
        iter = self.buffer.get_iter_at_offset(self.position)
        self.buffer.insert(iter, self.text)

    def undo(self):
        start = self.buffer.get_iter_at_offset(self.position)
        end = self.buffer.get_iter_at_offset(self.position + len(self.text))
        self.buffer.delete(start, end)

    @property
    def description(self):
        return "Insert text"


class DeleteItemCommand(Command):
    def __init__(self, list_store, item, index):
        self.list_store = list_store
        self.item = item
        self.index = index

    def execute(self):
        self.list_store.remove(self.index)

    def undo(self):
        self.list_store.insert(self.index, self.item)

    @property
    def description(self):
        return f"Delete {self.item.title}"
```

### Connecting to UI

```python
class App(Adw.Application):
    def __init__(self):
        super().__init__()
        self.undo_manager = UndoManager()
        self.undo_manager.on_changed = self.update_undo_actions

    def setup_actions(self):
        undo_action = Gio.SimpleAction.new("undo", None)
        undo_action.connect("activate", lambda a, p: self.undo_manager.undo())
        self.add_action(undo_action)

        redo_action = Gio.SimpleAction.new("redo", None)
        redo_action.connect("activate", lambda a, p: self.undo_manager.redo())
        self.add_action(redo_action)

        # Keyboard shortcuts
        self.set_accels_for_action("app.undo", ["<Control>z"])
        self.set_accels_for_action("app.redo", ["<Control><Shift>z"])

    def update_undo_actions(self):
        self.lookup_action("undo").set_enabled(self.undo_manager.can_undo())
        self.lookup_action("redo").set_enabled(self.undo_manager.can_redo())
```

## Tabs (AdwTabView)

### Basic Tab Setup

```python
# Tab view for multi-document interface
tab_view = Adw.TabView()

# Tab bar in header
tab_bar = Adw.TabBar()
tab_bar.set_view(tab_view)
header.set_title_widget(tab_bar)

# Tab overview (grid view of all tabs)
tab_overview = Adw.TabOverview()
tab_overview.set_view(tab_view)
tab_overview.set_child(toolbar_view)  # Wrap main content

# Overview button
overview_btn = Adw.TabButton()
overview_btn.set_view(tab_view)
header.pack_end(overview_btn)
```

### Creating Tabs

```python
def new_tab(title="New Tab", content=None):
    if content is None:
        content = create_default_content()

    page = tab_view.append(content)
    page.set_title(title)
    page.set_icon(Gio.ThemedIcon.new("text-x-generic-symbolic"))

    # Make closable
    tab_view.set_page_pinned(page, False)

    # Select the new tab
    tab_view.set_selected_page(page)
    return page

def close_tab(page):
    tab_view.close_page(page)
```

### Tab Signals

```python
# Handle tab close request (confirm if unsaved)
def on_close_page(view, page):
    if page_has_unsaved_changes(page):
        show_save_dialog(page)
        return Gdk.EVENT_STOP  # Prevent close
    return Gdk.EVENT_PROPAGATE  # Allow close

tab_view.connect("close-page", on_close_page)

# Handle tab selection change
def on_selected_changed(view, param):
    page = view.get_selected_page()
    if page:
        update_window_title(page.get_title())

tab_view.connect("notify::selected-page", on_selected_changed)

# Handle tab reorder
tab_view.connect("page-reordered", lambda v, p, pos: save_tab_order())
```

### Tab Context Menu

```python
def on_setup_menu(view, page):
    if page is None:
        return

    menu = Gio.Menu()
    menu.append("Duplicate Tab", "tab.duplicate")
    menu.append("Pin Tab", "tab.pin")
    menu.append("Close Other Tabs", "tab.close-others")
    view.set_menu_model(menu)

tab_view.connect("setup-menu", on_setup_menu)
```

## System Notifications

### When to Use

| Feedback Type | Use Case |
|--------------|----------|
| Toast | In-app events, user is actively using app |
| Banner | Persistent in-app state |
| Notification | Events when app is backgrounded, important alerts |

### Basic Notification

```python
def send_notification(title, body, action_name=None):
    notification = Gio.Notification.new(title)
    notification.set_body(body)
    notification.set_priority(Gio.NotificationPriority.NORMAL)

    # Optional action when clicked
    if action_name:
        notification.set_default_action(f"app.{action_name}")

    # Send with unique ID (for updating/withdrawing)
    app.send_notification("download-complete", notification)

# Example: Download complete
send_notification(
    "Download Complete",
    "report.pdf has finished downloading",
    "show-downloads"
)
```

### Notification with Actions

```python
notification = Gio.Notification.new("New Message")
notification.set_body("Alice: Hey, are you free?")

# Action buttons
notification.add_button("Reply", "app.reply::alice")
notification.add_button("Mark Read", "app.mark-read::alice")

# Click action (opens conversation)
notification.set_default_action("app.open-conversation::alice")

app.send_notification("message-alice", notification)
```

### Withdrawing Notifications

```python
# Remove notification (e.g., when user views the content)
app.withdraw_notification("message-alice")
```

### Notification Priority

```python
# Low: Background info, can wait
notification.set_priority(Gio.NotificationPriority.LOW)

# Normal: Default
notification.set_priority(Gio.NotificationPriority.NORMAL)

# High: Time-sensitive (shows as banner)
notification.set_priority(Gio.NotificationPriority.HIGH)

# Urgent: Critical alerts (persistent until dismissed)
notification.set_priority(Gio.NotificationPriority.URGENT)
```

## Popovers (Non-Menu)

### Tool Palette

```python
def create_tool_popover():
    popover = Gtk.Popover()

    grid = Gtk.Grid(column_spacing=6, row_spacing=6)
    grid.set_margin_top(12)
    grid.set_margin_bottom(12)
    grid.set_margin_start(12)
    grid.set_margin_end(12)

    tools = [
        ("edit-select-symbolic", "Select"),
        ("edit-cut-symbolic", "Cut"),
        ("draw-brush-symbolic", "Brush"),
        ("draw-eraser-symbolic", "Eraser"),
    ]

    for i, (icon, tooltip) in enumerate(tools):
        btn = Gtk.ToggleButton()
        btn.set_icon_name(icon)
        btn.set_tooltip_text(tooltip)
        btn.add_css_class("flat")
        grid.attach(btn, i % 2, i // 2, 1, 1)

    popover.set_child(grid)
    return popover
```

### Color Picker Popover

```python
def create_color_popover():
    popover = Gtk.Popover()

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    box.set_margin_top(12)
    box.set_margin_bottom(12)
    box.set_margin_start(12)
    box.set_margin_end(12)

    # Color chooser
    color_chooser = Gtk.ColorChooserWidget()
    color_chooser.set_use_alpha(True)
    box.append(color_chooser)

    # Apply button
    apply_btn = Gtk.Button(label="Apply")
    apply_btn.add_css_class("suggested-action")
    box.append(apply_btn)

    popover.set_child(box)
    return popover
```

### Popover Best Practices

```python
# Size constraints - keep small
popover.set_size_request(200, -1)  # Max width, natural height

# No close button needed - click outside dismisses

# Position relative to button
button = Gtk.MenuButton(icon_name="color-select-symbolic")
button.set_popover(color_popover)

# Or manual positioning
popover.set_parent(widget)
popover.set_position(Gtk.PositionType.BOTTOM)
popover.popup()
```

## Media Display

### Image Viewer

```python
class ImageViewer(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # Scrollable picture
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_vexpand(True)

        self.picture = Gtk.Picture()
        self.picture.set_can_shrink(True)
        self.picture.set_content_fit(Gtk.ContentFit.CONTAIN)

        self.scrolled.set_child(self.picture)
        self.append(self.scrolled)

        # Zoom controls
        self.zoom_level = 1.0
        self.setup_zoom_gestures()

    def load_image(self, path):
        self.picture.set_filename(path)

    def setup_zoom_gestures(self):
        # Scroll to zoom
        scroll = Gtk.EventControllerScroll()
        scroll.set_flags(Gtk.EventControllerScrollFlags.VERTICAL)

        def on_scroll(controller, dx, dy):
            if controller.get_current_event_state() & Gdk.ModifierType.CONTROL_MASK:
                self.zoom(1.0 - dy * 0.1)
                return True
            return False

        scroll.connect("scroll", on_scroll)
        self.add_controller(scroll)

        # Pinch to zoom
        zoom_gesture = Gtk.GestureZoom()
        zoom_gesture.connect("scale-changed", lambda g, s: self.zoom(s))
        self.add_controller(zoom_gesture)

    def zoom(self, factor):
        self.zoom_level = max(0.1, min(10.0, self.zoom_level * factor))
        # Apply zoom via CSS transform or picture sizing
```

### Video Player Controls

```python
class VideoControls(Gtk.Box):
    def __init__(self, media_stream):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add_css_class("toolbar")

        self.stream = media_stream

        # Play/Pause
        self.play_btn = Gtk.Button(icon_name="media-playback-start-symbolic")
        self.play_btn.connect("clicked", self.toggle_play)
        self.append(self.play_btn)

        # Progress slider
        self.progress = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 0, 100, 1
        )
        self.progress.set_hexpand(True)
        self.progress.set_draw_value(False)
        self.progress.connect("value-changed", self.on_seek)
        self.append(self.progress)

        # Time label
        self.time_label = Gtk.Label(label="0:00 / 0:00")
        self.time_label.add_css_class("numeric")
        self.append(self.time_label)

        # Volume
        self.volume_btn = Gtk.VolumeButton()
        self.volume_btn.set_value(1.0)
        self.append(self.volume_btn)

        # Fullscreen
        self.fullscreen_btn = Gtk.Button(icon_name="view-fullscreen-symbolic")
        self.append(self.fullscreen_btn)

    def toggle_play(self, button):
        if self.stream.get_playing():
            self.stream.pause()
            self.play_btn.set_icon_name("media-playback-start-symbolic")
        else:
            self.stream.play()
            self.play_btn.set_icon_name("media-playback-pause-symbolic")
```

## Split/Paned Views

### Resizable Split View

```python
# Horizontal split (side by side)
paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)

# Left panel
left_panel = Gtk.Box()
paned.set_start_child(left_panel)
paned.set_shrink_start_child(False)  # Don't allow shrinking to 0
paned.set_resize_start_child(False)  # Fixed width left panel

# Right panel
right_panel = Gtk.Box()
paned.set_end_child(right_panel)
paned.set_shrink_end_child(False)
paned.set_resize_end_child(True)  # Right panel gets extra space

# Set initial position (pixels from start)
paned.set_position(250)

# Save/restore position
def on_position_changed(paned, param):
    settings.set_int("pane-position", paned.get_position())

paned.connect("notify::position", on_position_changed)
```

### Three-Pane Layout

```python
# Main horizontal split
outer_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)

# Sidebar
sidebar = create_sidebar()
outer_paned.set_start_child(sidebar)

# Inner vertical split (content + details)
inner_paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

content = create_content_view()
inner_paned.set_start_child(content)

details = create_details_panel()
inner_paned.set_end_child(details)

outer_paned.set_end_child(inner_paned)
```

## Welcome/Onboarding

### First-Run Welcome

```python
def show_welcome_if_first_run():
    if settings.get_boolean("first-run-complete"):
        return

    welcome = Adw.Window(title="Welcome")
    welcome.set_default_size(600, 500)
    welcome.set_modal(True)
    welcome.set_transient_for(main_window)

    carousel = Adw.Carousel()
    carousel.set_allow_long_swipes(True)

    # Page 1: Welcome
    page1 = Adw.StatusPage(
        icon_name="application-x-executable-symbolic",
        title="Welcome to App Name",
        description="A brief description of what your app does"
    )
    carousel.append(page1)

    # Page 2: Feature highlight
    page2 = Adw.StatusPage(
        icon_name="emblem-photos-symbolic",
        title="Organize Your Photos",
        description="Easily sort and find your memories"
    )
    carousel.append(page2)

    # Page 3: Get started
    page3 = Adw.StatusPage(
        icon_name="go-next-symbolic",
        title="Ready to Start",
        description="Click below to begin"
    )
    start_btn = Gtk.Button(label="Get Started")
    start_btn.add_css_class("pill")
    start_btn.add_css_class("suggested-action")
    start_btn.connect("clicked", lambda b: finish_onboarding(welcome))
    page3.set_child(start_btn)
    carousel.append(page3)

    # Dots indicator
    dots = Adw.CarouselIndicatorDots()
    dots.set_carousel(carousel)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box.append(carousel)
    box.append(dots)

    welcome.set_content(box)
    welcome.present()

def finish_onboarding(window):
    settings.set_boolean("first-run-complete", True)
    window.close()
```

### Feature Callouts

```python
# Highlight a new feature after update
def show_feature_callout(widget, title, description):
    popover = Gtk.Popover()
    popover.set_autohide(False)  # Require explicit dismiss

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    box.set_margin_top(12)
    box.set_margin_bottom(12)
    box.set_margin_start(12)
    box.set_margin_end(12)

    title_label = Gtk.Label(label=title)
    title_label.add_css_class("heading")
    box.append(title_label)

    desc_label = Gtk.Label(label=description)
    desc_label.set_wrap(True)
    desc_label.set_max_width_chars(30)
    box.append(desc_label)

    dismiss_btn = Gtk.Button(label="Got It")
    dismiss_btn.connect("clicked", lambda b: popover.popdown())
    box.append(dismiss_btn)

    popover.set_child(box)
    popover.set_parent(widget)
    popover.popup()
```

## Keyboard Shortcuts (Access Keys)

### Setting Up Mnemonics

```python
# Underlined letter activated with Alt+letter
label = Gtk.Label.new_with_mnemonic("_File")  # Alt+F
button = Gtk.Button.new_with_mnemonic("_Save")  # Alt+S

# For menu items (in .ui file)
<item>
  <attribute name="label" translatable="yes">_Preferences</attribute>
  <attribute name="action">app.preferences</attribute>
</item>
```

### Custom Shortcuts

```python
class App(Adw.Application):
    def setup_shortcuts(self):
        # Single shortcut
        self.set_accels_for_action("app.new", ["<Control>n"])

        # Multiple shortcuts for same action
        self.set_accels_for_action("app.save", ["<Control>s", "<Control><Shift>s"])

        # View-specific shortcuts
        self.set_accels_for_action("win.zoom-in", ["<Control>plus", "<Control>equal"])
        self.set_accels_for_action("win.zoom-out", ["<Control>minus"])
        self.set_accels_for_action("win.zoom-reset", ["<Control>0"])
```

### Shortcut Controller

```python
# Handle shortcuts in a specific widget
shortcut_controller = Gtk.ShortcutController()

# Escape to cancel
shortcut = Gtk.Shortcut.new(
    Gtk.ShortcutTrigger.parse_string("Escape"),
    Gtk.CallbackAction.new(lambda w, a: cancel_action())
)
shortcut_controller.add_shortcut(shortcut)

# Delete key
shortcut = Gtk.Shortcut.new(
    Gtk.ShortcutTrigger.parse_string("Delete"),
    Gtk.CallbackAction.new(lambda w, a: delete_selected())
)
shortcut_controller.add_shortcut(shortcut)

widget.add_controller(shortcut_controller)
```
