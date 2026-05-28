# GNOME HIG Reference

Complete pattern catalog with code snippets for GTK 4/libadwaita (Python) and Qt/PySide6 equivalents.

## Design Principles (GNOME HIG Foundation)

1. **Design for People** - Inclusive across abilities, cultures, devices
2. **Make it Simple** - One thing done well, layered disclosure, frequent features prominent
3. **Reduce User Effort** - Automate, minimize steps, reduce cognitive load
4. **Be Considerate** - Prevent errors, enable undo, respect attention

## Container Patterns

### Application Window

**When:** Main app window, primary functionality

**Structure:**
- `AdwApplicationWindow` as root
- `AdwHeaderBar` at top
- Content area below (often `AdwToolbarView` for bottom bars)

**GTK 4/libadwaita (Python):**
```python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="My App")
        self.set_default_size(800, 600)

        # Header bar
        header = Adw.HeaderBar()

        # Primary action button (end of header)
        add_btn = Gtk.Button(icon_name="list-add-symbolic")
        add_btn.set_tooltip_text("Add Item")
        header.pack_end(add_btn)

        # Menu button
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic")
        menu_btn.set_tooltip_text("Main Menu")
        header.pack_end(menu_btn)

        # Main content
        content = Adw.Clamp(maximum_size=600)  # Constrain width
        # ... add content widgets

        # Assemble with toolbar view
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(content)

        self.set_content(toolbar_view)
```

**Qt/PySide6 equivalent:**
```python
from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(800, 600)

        # Toolbar mimics header bar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Use Adwaita-qt theme or custom QSS for styling
```

### Preferences Window

**When:** App settings, configuration options

**Structure:**
- `AdwPreferencesWindow` with pages
- `AdwPreferencesPage` for major sections
- `AdwPreferencesGroup` for related settings (boxed lists)
- Row widgets for individual settings

**GTK 4/libadwaita (Python):**
```python
class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, parent):
        super().__init__(transient_for=parent, modal=True)
        self.set_title("Preferences")

        # General page
        general_page = Adw.PreferencesPage(
            title="General",
            icon_name="emblem-system-symbolic"
        )

        # Appearance group
        appearance_group = Adw.PreferencesGroup(title="Appearance")

        # Dark mode switch
        dark_row = Adw.SwitchRow(
            title="Dark Mode",
            subtitle="Use dark color scheme"
        )
        appearance_group.add(dark_row)

        # Font size combo
        font_row = Adw.ComboRow(title="Font Size")
        font_row.set_model(Gtk.StringList.new(["Small", "Medium", "Large"]))
        font_row.set_selected(1)  # Default to Medium
        appearance_group.add(font_row)

        general_page.add(appearance_group)
        self.add(general_page)
```

### Dialog (Alert/Action)

**When:** Needs user decision, blocking errors, confirmations for irreversible actions

**Structure:**
- Heading describes action (not "Warning" or "Confirm")
- Body explains consequences
- Cancel button first, action button last
- Specific verb labels

**GTK 4/libadwaita (Python):**
```python
def show_delete_dialog(parent, item_name):
    dialog = Adw.AlertDialog(
        heading=f"Delete {item_name}?",
        body="This item will be permanently deleted. This cannot be undone."
    )

    dialog.add_response("cancel", "Cancel")
    dialog.add_response("delete", "Delete")

    dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.set_default_response("cancel")
    dialog.set_close_response("cancel")

    dialog.connect("response", on_delete_response)
    dialog.present(parent)
```

### Boxed Lists (Preferences Groups)

**When:** Displaying lists of settings, actions, or selectable items

**Row types:**
- `AdwActionRow` - clickable row, optional suffix widget
- `AdwSwitchRow` - row with toggle switch
- `AdwComboRow` - row with dropdown
- `AdwEntryRow` - row with text entry
- `AdwSpinRow` - row with numeric spinner
- `AdwExpanderRow` - collapsible row with children

**GTK 4/libadwaita (Python):**
```python
# Action row with navigation arrow
row = Adw.ActionRow(
    title="Account Settings",
    subtitle="Manage your account"
)
row.add_suffix(Gtk.Image(icon_name="go-next-symbolic"))
row.set_activatable(True)
row.connect("activated", lambda r: open_account_settings())

# Entry row for text input
name_row = Adw.EntryRow(title="Display Name")
name_row.connect("changed", on_name_changed)

# Spin row for numbers
port_row = Adw.SpinRow.new_with_range(1, 65535, 1)
port_row.set_title("Port")
port_row.set_value(8080)
```

## Navigation Patterns

### View Switcher (2-4 views)

**GTK 4/libadwaita:**
```python
# In header bar for desktop, bottom bar for mobile
view_switcher = Adw.ViewSwitcher()
view_switcher.set_stack(view_stack)
view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
header.set_title_widget(view_switcher)

# View stack with pages
view_stack = Adw.ViewStack()
view_stack.add_titled_with_icon(page1, "page1", "Overview", "view-grid-symbolic")
view_stack.add_titled_with_icon(page2, "page2", "Details", "view-list-symbolic")
```

### Sidebar Navigation (Many views)

**GTK 4/libadwaita:**
```python
split_view = Adw.NavigationSplitView()

# Sidebar
sidebar = Adw.NavigationPage(title="Projects")
sidebar_content = Gtk.ListBox()
sidebar_content.set_selection_mode(Gtk.SelectionMode.SINGLE)
# ... populate list
sidebar.set_child(sidebar_content)

# Content area
content = Adw.NavigationPage(title="Project Details")
# ... set content

split_view.set_sidebar(sidebar)
split_view.set_content(content)
```

## Feedback Patterns

### Toast

**When:** Action completed, recoverable errors, undo opportunities

**GTK 4/libadwaita:**
```python
# Simple toast
toast = Adw.Toast(title="Document saved")
toast_overlay.add_toast(toast)

# Toast with undo
toast = Adw.Toast(title="Item deleted")
toast.set_button_label("Undo")
toast.connect("button-clicked", on_undo_delete)
toast_overlay.add_toast(toast)
```

**Setup toast overlay:**
```python
# Wrap main content in toast overlay
toast_overlay = Adw.ToastOverlay()
toast_overlay.set_child(main_content)
self.set_content(toast_overlay)
```

### Progress Indicators

**GTK 4/libadwaita:**
```python
# Spinner for short/unknown duration
spinner = Gtk.Spinner()
spinner.start()

# Progress bar for long operations
progress = Gtk.ProgressBar()
progress.set_fraction(0.42)  # 42%
progress.set_text("Processing 13 of 31 items")
progress.set_show_text(True)

# Thin progress bar in header (for background tasks)
progress = Gtk.ProgressBar()
progress.add_css_class("osd")  # Overlay style
header.pack_end(progress)
```

### Banner (Persistent state)

**When:** Ongoing state that affects app functionality (offline, degraded mode, auth required)

**GTK 4/libadwaita:**
```python
banner = Adw.Banner(title="You are offline")
banner.set_button_label("Retry")
banner.set_revealed(True)
banner.connect("button-clicked", on_retry)

# Place at top of content area (inside AdwToolbarView or prepend to box)
toolbar_view.add_top_bar(banner)
```

**Error escalation pattern:**
```python
class SyncManager:
    def __init__(self, toast_overlay, banner):
        self.toast_overlay = toast_overlay
        self.banner = banner
        self.retry_count = 0

    def on_sync_error(self, error):
        self.retry_count += 1

        if self.retry_count <= 3:
            # Transient: Toast + auto-retry
            toast = Adw.Toast(title="Sync paused, retrying...")
            toast.set_timeout(2)
            self.toast_overlay.add_toast(toast)
            GLib.timeout_add_seconds(5, self.retry_sync)

        elif self.retry_count <= 10:
            # Persistent: Banner
            self.banner.set_title("Offline - changes saved locally")
            self.banner.set_button_label("Retry Now")
            self.banner.set_revealed(True)

        else:
            # Blocking: Dialog
            dialog = Adw.AlertDialog(
                heading="Unable to Sync",
                body="Check your internet connection and try again."
            )
            dialog.add_response("ok", "OK")
            dialog.present(self.window)
```

### Context Menus

**When:** Right-click/long-press actions on items (remove, rename, properties)

**GTK 4/libadwaita:**
```python
# Create menu model
menu = Gio.Menu()
menu.append("Rename", "item.rename")
menu.append("Remove", "item.remove")
menu.append("Properties", "item.properties")

# Create popover menu
popover = Gtk.PopoverMenu.new_from_model(menu)
popover.set_parent(widget)
popover.set_has_arrow(False)

# Show on right-click
gesture = Gtk.GestureClick(button=3)  # Right button
gesture.connect("pressed", lambda g, n, x, y: show_context_menu(popover, x, y))
widget.add_controller(gesture)

def show_context_menu(popover, x, y):
    rect = Gdk.Rectangle()
    rect.x, rect.y = int(x), int(y)
    rect.width = rect.height = 1
    popover.set_pointing_to(rect)
    popover.popup()
```

**For list rows:**
```python
# Add secondary click to each row
row = Adw.ActionRow(title="Item Name")
gesture = Gtk.GestureClick(button=3)
gesture.connect("pressed", lambda g, n, x, y: show_item_menu(row))
row.add_controller(gesture)
```

## Sidebar Patterns

### Sidebar Structure

**When:** Many/dynamic navigation destinations (file manager, email, chat)

**GTK 4/libadwaita:**
```python
split_view = Adw.NavigationSplitView()

# Sidebar with sections
sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
sidebar_box.set_margin_top(12)
sidebar_box.set_margin_bottom(12)

# Section: Favorites
favorites_label = Gtk.Label(label="Favorites", xalign=0)
favorites_label.add_css_class("heading")
favorites_label.set_margin_start(12)
sidebar_box.append(favorites_label)

favorites_list = Gtk.ListBox()
favorites_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
favorites_list.add_css_class("navigation-sidebar")
# Add rows...
sidebar_box.append(favorites_list)

# Section: Locations
locations_label = Gtk.Label(label="Locations", xalign=0)
locations_label.add_css_class("heading")
locations_label.set_margin_start(12)
sidebar_box.append(locations_label)

locations_list = Gtk.ListBox()
locations_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
locations_list.add_css_class("navigation-sidebar")
sidebar_box.append(locations_list)

# Wrap in scroll
scrolled = Gtk.ScrolledWindow()
scrolled.set_child(sidebar_box)

sidebar_page = Adw.NavigationPage(title="Files")
sidebar_page.set_child(scrolled)
split_view.set_sidebar(sidebar_page)
```

### Sidebar Row with Icon

```python
def create_sidebar_row(title, icon_name, subtitle=None):
    row = Adw.ActionRow(title=title)
    row.add_prefix(Gtk.Image(icon_name=icon_name))
    if subtitle:
        row.set_subtitle(subtitle)
    row.set_activatable(True)
    return row

# Example rows
home_row = create_sidebar_row("Home", "user-home-symbolic")
docs_row = create_sidebar_row("Documents", "folder-documents-symbolic")
trash_row = create_sidebar_row("Trash", "user-trash-symbolic")
```

## Search Patterns

### Search Bar Integration

**When:** Content filtering by text, type-to-search activation

**GTK 4/libadwaita:**
```python
# Search bar slides down from header bar
search_bar = Gtk.SearchBar()
search_entry = Gtk.SearchEntry()
search_entry.set_hexpand(True)
search_bar.set_child(search_entry)
search_bar.connect_entry(search_entry)

# Toggle button in header bar
search_button = Gtk.ToggleButton(icon_name="system-search-symbolic")
search_button.set_tooltip_text("Search")
header.pack_end(search_button)

# Bind toggle to search bar
search_bar.bind_property(
    "search-mode-enabled",
    search_button, "active",
    GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE
)

# Place search bar below header
toolbar_view.add_top_bar(search_bar)

# Enable Ctrl+F and type-to-search
search_bar.set_key_capture_widget(window)
```

**Search activation methods:**
- Ctrl+F keyboard shortcut (standard)
- Toggle button in header bar
- Type-to-search (typing activates search automatically)

### Live Search Results

```python
def on_search_changed(entry):
    query = entry.get_text().lower()
    if not query:
        # Show all items
        filter_model.set_filter(None)
        return

    def match_func(item):
        return query in item.title.lower()

    custom_filter = Gtk.CustomFilter.new(match_func)
    filter_model.set_filter(custom_filter)

search_entry.connect("search-changed", on_search_changed)
```

### Search Empty State

```python
# "No results" placeholder
no_results = Adw.StatusPage(
    icon_name="system-search-symbolic",
    title="No Results Found",
    description="Try a different search term"
)

# Show/hide based on results count
stack.add_named(results_view, "results")
stack.add_named(no_results, "no-results")

def update_results_view():
    if filter_model.get_n_items() == 0 and search_entry.get_text():
        stack.set_visible_child_name("no-results")
    else:
        stack.set_visible_child_name("results")
```

## Form Validation Patterns

### Entry Row with Validation

**GTK 4/libadwaita:**
```python
# Entry row with error styling
name_row = Adw.EntryRow(title="Name")

def validate_name(row):
    text = row.get_text()
    if not text:
        row.add_css_class("error")
        row.set_tooltip_text("Name is required")
        return False
    elif len(text) < 3:
        row.add_css_class("error")
        row.set_tooltip_text("Name must be at least 3 characters")
        return False
    else:
        row.remove_css_class("error")
        row.set_tooltip_text("")
        return True

# Validate on change (real-time) or on focus-out
name_row.connect("changed", lambda r: validate_name(r))
```

### Form Submission with Validation

```python
def on_save_clicked(button):
    # Validate all fields
    errors = []
    if not validate_name(name_row):
        errors.append("name")
    if not validate_email(email_row):
        errors.append("email")

    if errors:
        # Focus first error field
        if "name" in errors:
            name_row.grab_focus()
        # Show error toast
        toast = Adw.Toast(title="Please fix the errors above")
        toast_overlay.add_toast(toast)
        return

    # Proceed with save
    do_save()
```

### Validation Timing

| Timing | Use When |
|--------|----------|
| On change (real-time) | Format validation (email, URL), character limits |
| On focus out | Expensive validation, API checks |
| On submit | Final validation, show all errors |

**Best practice:** Show positive feedback when valid rather than only errors. Use `success` CSS class for valid fields if helpful.

## Grid View Patterns

### Basic Grid View

**GTK 4:**
```python
# Create grid view with selection
grid_view = Gtk.GridView()
grid_view.set_model(selection_model)

# Factory for grid items
factory = Gtk.SignalListItemFactory()

def setup_item(factory, list_item):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    image = Gtk.Picture()
    image.set_size_request(150, 150)
    image.set_content_fit(Gtk.ContentFit.COVER)
    label = Gtk.Label()
    label.set_ellipsize(Pango.EllipsizeMode.END)
    box.append(image)
    box.append(label)
    list_item.set_child(box)

def bind_item(factory, list_item):
    box = list_item.get_child()
    image = box.get_first_child()
    label = box.get_last_child()
    item = list_item.get_item()
    image.set_filename(item.thumbnail_path)
    label.set_label(item.title)

factory.connect("setup", setup_item)
factory.connect("bind", bind_item)
grid_view.set_factory(factory)
```

### Selection Model

```python
# Single selection (default)
selection_model = Gtk.SingleSelection(model=list_store)

# Multi-selection
selection_model = Gtk.MultiSelection(model=list_store)

# Connect to selection changes
selection_model.connect("selection-changed", on_selection_changed)

def on_selection_changed(model, position, n_items):
    selected = get_selected_items(model)
    update_action_bar(selected)
```

### Selection Mode Toggle

```python
# Action bar for selection mode
action_bar = Gtk.ActionBar()
action_bar.set_revealed(False)

select_all_btn = Gtk.Button(label="Select All")
select_all_btn.connect("clicked", lambda b: selection_model.select_all())

delete_btn = Gtk.Button(label="Delete")
delete_btn.add_css_class("destructive-action")

cancel_btn = Gtk.Button(label="Cancel")
cancel_btn.connect("clicked", lambda b: exit_selection_mode())

action_bar.pack_start(select_all_btn)
action_bar.pack_end(delete_btn)
action_bar.pack_end(cancel_btn)

# Toggle button in header bar
select_btn = Gtk.ToggleButton(icon_name="selection-mode-symbolic")
select_btn.set_tooltip_text("Select Items")

def on_select_mode_toggled(button):
    if button.get_active():
        selection_model = Gtk.MultiSelection(model=list_store)
        grid_view.set_model(selection_model)
        action_bar.set_revealed(True)
    else:
        selection_model = Gtk.SingleSelection(model=list_store)
        grid_view.set_model(selection_model)
        action_bar.set_revealed(False)

select_btn.connect("toggled", on_select_mode_toggled)
```

## Primary Menu Structure

### Standard Primary Menu

**Every GNOME app should include these items:**

```python
menu = Gio.Menu()

# App-specific items first (optional)
menu.append("Import...", "app.import")
menu.append("Export...", "app.export")

# Separator (implicit by creating new section)
section = Gio.Menu()
section.append("Preferences", "app.preferences")
section.append("Keyboard Shortcuts", "win.show-help-overlay")
section.append("Help", "app.help")
section.append("About App Name", "app.about")
menu.append_section(None, section)

# Menu button setup
menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic")
menu_button.set_tooltip_text("Main Menu")
menu_button.set_menu_model(menu)
header.pack_end(menu_button)
```

**Menu organization:**
- 3-12 items maximum in primary menu
- Group related items in sections
- Preferences, Shortcuts, Help, About at bottom
- Never include Quit (use Ctrl+Q shortcut)

### Shortcuts Window

```python
# In app class
def do_activate(self):
    # Set up shortcuts window
    builder = Gtk.Builder.new_from_resource("/com/example/app/shortcuts.ui")
    self.set_help_overlay(builder.get_object("shortcuts"))

# In shortcuts.ui
<object class="GtkShortcutsWindow" id="shortcuts">
  <child>
    <object class="GtkShortcutsSection">
      <property name="title">General</property>
      <child>
        <object class="GtkShortcutsGroup">
          <property name="title">Navigation</property>
          <child>
            <object class="GtkShortcutsShortcut">
              <property name="accelerator">&lt;Control&gt;f</property>
              <property name="title">Search</property>
            </object>
          </child>
        </object>
      </child>
    </object>
  </child>
</object>
```

### About Dialog

```python
def show_about(app):
    about = Adw.AboutDialog(
        application_name="App Name",
        application_icon="com.example.AppName",
        version="1.0.0",
        developer_name="Developer Name",
        copyright="© 2024 Developer Name",
        license_type=Gtk.License.GPL_3_0,
        website="https://example.com",
        issue_url="https://github.com/example/app/issues"
    )
    about.set_developers(["Developer Name"])
    about.set_designers(["Designer Name"])
    about.present(window)
```

## Additional Control Patterns

### Multiline Text Entry

```python
# Use GtkTextView for multiline, styled to match Adwaita
text_view = Gtk.TextView()
text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
text_view.set_top_margin(12)
text_view.set_bottom_margin(12)
text_view.set_left_margin(12)
text_view.set_right_margin(12)

# Wrap in scrolled window with frame
scrolled = Gtk.ScrolledWindow()
scrolled.set_child(text_view)
scrolled.set_min_content_height(100)
scrolled.add_css_class("card")  # Boxed appearance

# Add to preferences group with custom widget
group = Adw.PreferencesGroup(title="Description")
group.add(scrolled)
```

### Date Selection

```python
# Use GtkCalendar in a popover
calendar = Gtk.Calendar()
calendar.connect("day-selected", on_date_selected)

popover = Gtk.Popover()
popover.set_child(calendar)

# Date entry button
date_button = Gtk.MenuButton(label="Select Date")
date_button.set_popover(popover)

def on_date_selected(calendar):
    date = calendar.get_date()
    date_button.set_label(date.format("%Y-%m-%d"))
    popover.popdown()
```

### Cancellable Operations

```python
class ImportOperation:
    def __init__(self, toast_overlay):
        self.cancelled = False
        self.toast_overlay = toast_overlay

    def start(self, files):
        # Show progress dialog
        self.dialog = Adw.AlertDialog(heading="Importing Photos")
        self.progress = Gtk.ProgressBar()
        self.progress.set_show_text(True)
        self.dialog.set_extra_child(self.progress)

        self.dialog.add_response("cancel", "Cancel")
        self.dialog.connect("response", self.on_cancel)
        self.dialog.present(window)

        # Start import in thread
        threading.Thread(target=self.do_import, args=(files,)).start()

    def on_cancel(self, dialog, response):
        if response == "cancel":
            self.cancelled = True

    def do_import(self, files):
        for i, f in enumerate(files):
            if self.cancelled:
                GLib.idle_add(self.on_cancelled, i, len(files))
                return
            # Import file...
            GLib.idle_add(self.update_progress, i + 1, len(files))

        GLib.idle_add(self.on_complete, len(files))

    def update_progress(self, current, total):
        self.progress.set_fraction(current / total)
        self.progress.set_text(f"Importing {current} of {total}")

    def on_complete(self, count):
        self.dialog.close()
        toast = Adw.Toast(title=f"Imported {count} photos")
        self.toast_overlay.add_toast(toast)

    def on_cancelled(self, completed, total):
        self.dialog.close()
        toast = Adw.Toast(title=f"Import cancelled ({completed} of {total} imported)")
        self.toast_overlay.add_toast(toast)
```

## File Chooser Dialogs

### Open File

```python
def on_open_clicked(button):
    dialog = Gtk.FileDialog(title="Open Document")

    # Filter for specific file types
    filters = Gio.ListStore.new(Gtk.FileFilter)

    text_filter = Gtk.FileFilter()
    text_filter.set_name("Text Files")
    text_filter.add_mime_type("text/plain")
    text_filter.add_pattern("*.txt")
    filters.append(text_filter)

    all_filter = Gtk.FileFilter()
    all_filter.set_name("All Files")
    all_filter.add_pattern("*")
    filters.append(all_filter)

    dialog.set_filters(filters)
    dialog.set_default_filter(text_filter)

    dialog.open(window, None, on_open_response)

def on_open_response(dialog, result):
    try:
        file = dialog.open_finish(result)
        path = file.get_path()
        # Load file...
    except GLib.Error as e:
        if e.code != Gtk.DialogError.DISMISSED:
            show_error_toast(f"Could not open file: {e.message}")
```

### Save File

```python
def on_save_clicked(button):
    dialog = Gtk.FileDialog(
        title="Save Document",
        initial_name="Untitled.txt"
    )
    dialog.save(window, None, on_save_response)

def on_save_response(dialog, result):
    try:
        file = dialog.save_finish(result)
        path = file.get_path()
        # Save to path...
        toast = Adw.Toast(title="Document saved")
        toast_overlay.add_toast(toast)
    except GLib.Error as e:
        if e.code != Gtk.DialogError.DISMISSED:
            show_error_toast(f"Could not save file: {e.message}")
```

### Select Folder

```python
def on_select_folder_clicked(button):
    dialog = Gtk.FileDialog(title="Select Folder")
    dialog.select_folder(window, None, on_folder_response)

def on_folder_response(dialog, result):
    try:
        folder = dialog.select_folder_finish(result)
        path = folder.get_path()
        # Use folder...
    except GLib.Error:
        pass  # User cancelled
```

## Dark/Light Mode

### Following System Preference (Default)

```python
# Apps automatically follow system preference - no code needed
# Libadwaita handles this automatically
```

### Per-App Style Switching

```python
# Get style manager
style_manager = Adw.StyleManager.get_default()

# Check current mode
is_dark = style_manager.get_dark()

# Force specific mode (use sparingly - respect user preference)
style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

# Return to system preference
style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
```

### Style Toggle in Preferences

```python
# In preferences window
appearance_group = Adw.PreferencesGroup(title="Appearance")

style_row = Adw.ComboRow(title="Style")
style_row.set_model(Gtk.StringList.new(["System", "Light", "Dark"]))

def on_style_changed(row, param):
    selected = row.get_selected()
    style_manager = Adw.StyleManager.get_default()
    schemes = [
        Adw.ColorScheme.DEFAULT,      # System
        Adw.ColorScheme.FORCE_LIGHT,  # Light
        Adw.ColorScheme.FORCE_DARK,   # Dark
    ]
    style_manager.set_color_scheme(schemes[selected])

style_row.connect("notify::selected", on_style_changed)
appearance_group.add(style_row)
```

### Reacting to Style Changes

```python
# Update custom elements when style changes
def on_dark_changed(style_manager, param):
    is_dark = style_manager.get_dark()
    # Update any custom-styled elements
    update_custom_colors(is_dark)

style_manager = Adw.StyleManager.get_default()
style_manager.connect("notify::dark", on_dark_changed)
```

## Responsive Layouts (Breakpoints)

### Basic Sidebar Collapse

```python
# Collapse sidebar on narrow windows
split_view = Adw.NavigationSplitView()

breakpoint = Adw.Breakpoint.new(
    Adw.BreakpointCondition.parse("max-width: 600sp")
)
breakpoint.add_setter(split_view, "collapsed", True)
window.add_breakpoint(breakpoint)
```

### Multiple Breakpoints

```python
# Different layouts at different sizes
class AdaptiveWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        # Phone: single column, bottom bar
        phone_bp = Adw.Breakpoint.new(
            Adw.BreakpointCondition.parse("max-width: 400sp")
        )
        phone_bp.add_setter(self.split_view, "collapsed", True)
        phone_bp.add_setter(self.view_switcher_bar, "reveal", True)
        phone_bp.add_setter(self.header_switcher, "visible", False)

        # Tablet: collapsed sidebar, header switcher
        tablet_bp = Adw.Breakpoint.new(
            Adw.BreakpointCondition.parse("max-width: 800sp")
        )
        tablet_bp.add_setter(self.split_view, "collapsed", True)

        self.add_breakpoint(phone_bp)
        self.add_breakpoint(tablet_bp)
```

### Adaptive View Switcher

```python
# Header bar switcher for wide, bottom bar for narrow
header = Adw.HeaderBar()
view_switcher = Adw.ViewSwitcher()
view_switcher.set_stack(stack)
view_switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
header.set_title_widget(view_switcher)

# Bottom bar for narrow windows
switcher_bar = Adw.ViewSwitcherBar()
switcher_bar.set_stack(stack)

# Breakpoint to toggle
breakpoint = Adw.Breakpoint.new(
    Adw.BreakpointCondition.parse("max-width: 550sp")
)
breakpoint.add_setter(view_switcher, "visible", False)
breakpoint.add_setter(switcher_bar, "reveal", True)
window.add_breakpoint(breakpoint)

# Layout
toolbar_view = Adw.ToolbarView()
toolbar_view.add_top_bar(header)
toolbar_view.add_bottom_bar(switcher_bar)
toolbar_view.set_content(stack)
```

### Content Width Constraints

```python
# Prevent content from becoming too wide on large screens
clamp = Adw.Clamp()
clamp.set_maximum_size(800)  # Max width in pixels
clamp.set_tightening_threshold(600)  # Start padding at this width
clamp.set_child(content)

# Use ClampScrollable for scrolled content
scrolled = Gtk.ScrolledWindow()
clamp = Adw.ClampScrollable()
clamp.set_maximum_size(800)
clamp.set_child(content_box)
scrolled.set_child(clamp)
```

## Typography

**Style classes (use instead of custom CSS):**

| Class | Use For |
|-------|---------|
| `title-1` to `title-4` | Display headings, welcome screens |
| `heading` | Section headings, group titles |
| `body` | Default text, descriptions |
| `caption` | Secondary info, timestamps |
| `monospace` | Code, technical values |
| `dim-label` | De-emphasized text |
| `numeric` | Tabular numbers |

**GTK 4:**
```python
label = Gtk.Label(label="Welcome")
label.add_css_class("title-1")

subtitle = Gtk.Label(label="Get started by creating a project")
subtitle.add_css_class("body")
subtitle.add_css_class("dim-label")
```

## Writing Style Quick Reference

| Context | Style | Example |
|---------|-------|---------|
| Button labels | Header caps, imperative verb | "Save Document", "Add Item" |
| Menu items | Header caps | "Find and Replace" |
| Checkbox/switch | Sentence caps | "Show notifications" |
| Descriptions | Sentence caps, no period | "Changes will take effect after restart" |
| Toast messages | Informal heading | "Document saved" |
| Dialog headings | Describe action | "Delete project?" not "Warning" |

**Header capitalization:** Capitalize words 4+ letters, all verbs, all nouns, first/last words

## Spacing & Layout

**Use libadwaita defaults - avoid custom margins:**

- `AdwClamp` constrains content width (default max: 600px)
- `AdwPreferencesGroup` handles internal spacing
- Box spacing: 12px between major sections, 6px between related items

**Responsive breakpoints:**
```python
# Check width for adaptive layouts
breakpoint = Adw.Breakpoint.new(
    Adw.BreakpointCondition.parse("max-width: 500sp")
)
breakpoint.add_setter(split_view, "collapsed", True)
self.add_breakpoint(breakpoint)
```

## Common Mistakes

### 1. Overloaded Header Bar

**Wrong:**
```
[Back] [Title] [Search] [Filter] [Sort] [Add] [Menu]
```

**Right:**
```
[Back] [    Title    ] [Add] [Menu]
```
Put secondary actions in menu or use view-specific controls below header.

### 2. Wrong Dialog Type

**Wrong:** Confirmation dialog for "Delete" when undo is possible
**Right:** Toast with "Undo" button - less intrusive, equally safe

**Wrong:** Toast for "You have unsaved changes"
**Right:** Dialog - requires acknowledgment before data loss

### 3. Missing Empty States

**Wrong:** Blank area when list is empty
**Right:** Placeholder page with:
- Relevant symbolic icon (48px+)
- Clear message ("No projects yet")
- Primary action button ("Create Project")

```python
status_page = Adw.StatusPage(
    icon_name="folder-symbolic",
    title="No Projects",
    description="Create a project to get started"
)
button = Gtk.Button(label="Create Project")
button.add_css_class("pill")
button.add_css_class("suggested-action")
status_page.set_child(button)
```

### 4. Generic Button Labels

**Wrong:** "OK", "Yes", "No", "Submit", "Confirm"
**Right:** Specific verbs: "Save", "Delete", "Send", "Create Project"

### 5. Custom Controls for Native Patterns

**Wrong:** Custom toggle widget
**Right:** `AdwSwitchRow`

**Wrong:** Custom dropdown
**Right:** `AdwComboRow`

**Wrong:** Custom tabs
**Right:** `AdwViewSwitcher` or `AdwTabView`

### 6. Frozen UI During Operations

**Wrong:** No feedback during network requests
**Right:**
- Short operations (<5s): Spinner
- Long operations: Progress bar with status text
- Background operations: Thin progress in header bar

### 7. Poor Keyboard Navigation

**Wrong:** Click-only interactions, no focus indicators
**Right:**
- All controls Tab-focusable
- Enter/Space activate buttons
- Escape closes dialogs/popovers
- Visible focus rings (libadwaita provides automatically)

### 8. Accessibility Gaps

**Testing checklist:**
```bash
# High contrast
GTK_THEME=Adwaita:hc ./my-app

# Large text (set in GNOME Settings > Accessibility)

# Screen reader
orca &
./my-app

# Keyboard only - unplug mouse, navigate entire app
```

## Color Reference

**Never hardcode colors.** Use CSS variables for automatic light/dark/high-contrast support:

| Variable | Use |
|----------|-----|
| `@accent_color` | Interactive elements |
| `@accent_bg_color` | Accent backgrounds |
| `@destructive_color` | Destructive actions |
| `@success_color` | Success states |
| `@warning_color` | Warnings |
| `@error_color` | Errors |
| `@view_bg_color` | Content backgrounds |
| `@headerbar_bg_color` | Header bar |
| `@card_bg_color` | Card/boxed list backgrounds |

## Keyboard Shortcuts

**Standard shortcuts to implement:**

| Shortcut | Action |
|----------|--------|
| Ctrl+W | Close window |
| Ctrl+Q | Quit app |
| Ctrl+N | New item |
| Ctrl+S | Save |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |
| Ctrl+F | Search/Find |
| Escape | Close dialog/popover, cancel |
| F1 | Help |

## External Resources

- [GNOME HIG](https://developer.gnome.org/hig/)
- [Libadwaita docs](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)
- [GNOME Icon Library](https://apps.gnome.org/IconLibrary/)
- [GTK 4 docs](https://docs.gtk.org/gtk4/)
- [Adwaita-qt](https://github.com/nickalcock/adwaita-qt) for Qt/PySide6
