# Godot - Scripting

**Pages:** 66

---

## GDScript — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/index.html

**Contents:**
- GDScript

See GDScript grammar if you are interested in writing a third-party tool that interacts with GDScript, such as a linter or formatter.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Script Editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/script_editor.html

**Contents:**
- Script Editor
- Introduction
- Features
- Usage
  - Script Panel
  - Menus
  - Coding area
- User-contributed notes

Godot Engine's script editor is a powerful and fully-integrated text editor that not only streamlines the process of writing and debugging code written in GDScript but also allows for working with plain text files, providing developers with a seamless environment for scripting game logic and behaviors. It can highlight your code, automatically indent it, perform syntax checks, and much more. You can also create breakpoints to debug your project without switching to another window. The text editor also serves as an offline class reference viewer, which can be accessed in several ways as described in the Integrated class reference.

Some of the key features of the text editor are listed below:

Fully-integrated code editor for GDScript.

Syntax highlighting support for GDScript and JSON files.

Syntax checking for GDScript and JSON files.

Bookmark and breakpoint support.

Automatic indentation.

Multiple carets, which can be enabled using Alt + Left Click.

Auto-completion of variables, functions, constants, etc.

Inline refactoring of symbols by selecting them and using Ctrl + D.

Mass find and replace across project files.

If you are using GDScript in your project, the built-in text editor in Godot provides everything you need, serving as a one-stop location to fully utilize the Godot Engine. Nearly all parameters that can be adjusted via the user interface can also be modified directly through code.

If you would like to use an external text editor or prefer to use C# in your project, see Using an external text editor and Configuring an external editor.

Similar to many parts of the Godot's interface, the text editor can also be customized by changing its settings to your liking. You can access these settings by opening Editor > Editor Settings and going to the Text Editor group.

You can open the Script Editor using the Script button in the workspace selector, located at the top center of Godot's interface. Alternatively, you can use the Open Script button next to a node in the Scene Tree dock, or double-click on a .gd file or a recognized text file in the FileSystem dock to open it directly in the Script Editor.

Once it is open, you will see the text editor menus at the top, below the scene switcher. Next to the menus, you'll find buttons to open the online documentation or search within the built-in class reference. To the right of these buttons are two navigation arrows that allow you to navigate through your viewing history. Finally, you can use the float button to separate the text editor from Godot's window, which is useful if you are working with multiple monitors.

Underneath the menus on the left, you will see the script panel. In the center, adjacent to the script panel, is the coding area. Beneath the coding area is the status bar, which displays the error and warning count in the code. Clicking on the error or warning icons will show the list of errors with the line numbers. Clicking on one will jump to that line. You can also choose to ignore warnings by opening the list and clicking Ignore. The status bar also lets you change the zoom level of the code by clicking the percentage value. You can also use Ctrl + Mouse Wheel (Cmd + Mouse Wheel on Mac) to achieve the same effect. The status bar also shows the current position of the caret in terms of line and column, and whether the indentation is done using tabs, or spaces.

Many of the actions performed in the text editor can also be executed using shortcuts. The actions show their corresponding shortcuts next to them. For a complete shortcut list, see the text editor shortcuts.

In the next sections, we will go through different aspects of the text editor. You can also select a section below to jump to a specific topic:

Below the menus, on the left panel, you will see a list of opened files and documentation pages. Depending on the file type, this list will have an icon next to the file name. For example, the icon means that it is a GDScript. the means it is a C# script. The means that this is a built-in class reference. Finally, the means it is a currently running script (See tool annotation for more on this). Hovering a file will show a tooltip with its relative location in the project folder.

On the status bar, clicking the left arrow hides the script panel, clicking on the right arrow shows it.

If you did not change any settings, the file names may also have a different coloring. This helps you identify the recently edited files by highlighting them. This behavior can be changed in the Editor > Editor Settings by adjusting the Script Temperature properties in the Text Editor section.

The filter bar above the file names introduces a handy case-insensitive search to find a specific file. Even if you just type the letters of a file name into the bar, files containing these letters in order will also appear. Assume that there is a file named button.gd in the list. If you type btn into the filter bar, this file will appear in the results. To reset the filter, clear the filter bar.

An asterisk (*) next to a file name indicates that the file has unsaved changes.

If you just enter "*" in the filter bar, you can display all unsaved files.

You can drag a file to change the ordering. Middle-clicking on a file closes it. Right-clicking on a file provides several options to save or close files, or to copy the relative path of the file. On this menu:

You can also use Move Up and Move Down to change the order of the file, or use Sort to sort all files alphabetically. Toggle Scripts Panel hides the panel, which can be displayed again using the right arrow on the status bar. Close Docs closes all opened in-class reference documents leaving only script files open. Show in FileSystem finds and highlights the file in the FileSystem dock.

Below the file list, you'll see the name of the currently open file. The button next to this switches the ordering of the methods defined in this file between alphabetical and as they appear. Under this is the outline of the file. If this is a script file, it will contain the list of defined methods. If, however, a class reference page is open, this area will show the table of contents of this document. Clicking on an item in this list will jump to the respective function or section in the file. Similarly, the Filter Methods bar lets you search for a specific function or section within the selected document with the same behavior as filtering scripts.

The text editor's menus lie below the scene switcher and allow you to access a variety of tools and options, such as file management, search and replace, debugging controls, and code formatting features.

An asterisk (*) next to an action means that this operation is also available in the context menu, which can be opened by right-clicking in the code editor.

The File menu provides the following options:

New Script...: Opens the new script dialog to create and add the script to the project. If creation is successful, it will directly open it in the text editor. Depending on the version of Godot (with C# support or not), you can choose .gd or .cs as the extension.

New Text File...: Opens the file dialog to create a plain text file with one of the recognized formats. Godot can also highlight json files.

Open...: Opens the file dialog to let you browse inside your computer and choose any recognized text file to open it.

Reopen Closed Script: Reopens the last closed scripts. You can use this option multiple times to reopen other closed scripts if you closed more than one.

Open Recent: Provides a list of last opened scripts. You can also clear the list using the provided option at the bottom of the list.

Save: Saves the currently selected script.

Save As...: Opens the file dialog to save the currently open script with a different name.

Save All: Saves all unsaved open scripts in the text editor. Scripts with unsaved changes will have an asterisk (*) next to their names in the script list.

Soft Reload Tool Script: If the selected script is a tool, reloads the script to execute it again.

Copy Script Path: Copies the currently selected script's relative path in the project using the res:// prefix.

Show in FileSystem: Finds and highlights the selected file in the FileSystem dock.

History Previous: Changes the active script to the one that was previously opened. This is useful when you have multiple scripts open and want to quickly navigate back to the last script you were editing. If you also changed the caret position more than 10 lines, you will first move it to its previous location in the same file.

History Next: After using History Previous to go back to an earlier script, this feature allows you to move forward through the script history, switching to scripts that were previously accessed. Similar to above, if you also changed the caret position more than 10 lines, you will first move it to its next location in the same file.

Theme: Provides options to import an existing theme, save, or reload it. Changing theme settings is performed via Editor Settings.

Close: Closes the active script.

Close All: Closes all open scripts and prompts to save if there are unsaved changes.

Close Other Tabs: Closes all open scripts except the selected one.

Close Docs: Closes the class reference documentation pages, leaving only the scripts.

Run: If the script extends EditorScript and intended to be executed without running the project, this option runs the script. See Running one-off scripts using EditorScript for more.

Toggle Scripts Panel: Shows or hides the script panel located on the left side of the text editor, allowing you to expand the available coding area. More on the Scripts Panel is explained above.

The Edit menu provides several options for line operations:

Undo*: Allows you to reverse the most recent action or series of actions, restoring document or code to its previous state before the changes were made.

Redo*: Allows you to reapply an action that was previously undone, effectively redoing the last action that was reversed by the Undo function.

Cut*: Cuts the selection to the clipboard.

Copy*: Copies the selection to the clipboard.

Paste*: Pastes the content of the clipboard if it contains text.

Select All*: Selects the all code in the text editor.

Duplicate Selection: Copies the selection and appends it next to the selection.

Duplicate Lines: Duplicates the current line and adds it as a new line below the current line.

Evaluate Selection*: Computes the values of the selected text if it contains only a mathematical expression, such as 83 * 3 or pow(2,3).

Toggle Word Wrap: Disables the horizontal scrollbar by wrapping the long lines to the next line. Note that this is just a visual change and no new linebreaks are added.

Line: Provides a set of line operations. Depending on the opened file, the options might also be directly in the Edit menu, instead of a submenu.

Move Up: Moves the current line or the selected line(s) one line up.

Move Down: Moves the current line or the selected line(s) one line down.

Indent*: Indents the text from the caret or the selected line(s), following the indentation setting.

Unindent*: Unindents the text from the caret or the selected line(s), following the indentation setting.

Delete Line: Deletes the current line or the selected line(s).

Toggle Comment*: Comments and uncomments the current line or the selected line(s). You can perform the same action by selecting line(s) and choosing the same action after right-clicking on the selected text.

Folding: Provides a set of folding options for the selected text. Depending on the opened file, the options might also be directly in the Edit menu, instead of a submenu.

Fold/Unfold Line*: If the code in the current line has a code block or code region beneath it, it hides this block by collapsing the lines. You can then unfold it using this option again, using the ">" arrow next to the line number in the coding area, or clicking on the ellipsis "..." icon at the end of the folded line.

Fold All Lines: Folds all code blocks or code regions in the open document.

Unfold All Lines: Unfolds all code blocks and code regions in the open document.

Create Code Region*: Wraps the selected text in a foldable code region to improve the readability of larger scripts. See Built-in types for more.

Completion Query: Suggests from built-in or user created symbols to auto-complete the partially written code. Up and Down arrows navigate up and down, pressing Enter or Tab accepts and adds the highlighted symbol to the code. Tab will also replace existing text to the right of the caret.

Trim Trailing Whitespaces: Removes extra spacing at the end of each line in the file.

Trim Final Newlines: Removes the extra new lines at the end of the file.

Indentation: Provides options for the indentation of the open file. Depending on the opened file, the options might also be directly in the Edit menu, instead of a submenu.

Convert Indent to Spaces: Converts all indentation in the file to spaces.

Convert Indent to Tabs: Converts all indentation in the file to tabs.

Auto Indent: Converts the indentation of the selected lines (or the entire file) following the indentation setting.

Convert Case: Changes the case of the selected text to Upper Case*, Lower Case*, or capitalizes each initial letter of the words.

Syntax Highlighter: Allows you to choose the syntax highlighter.

Plain Text: Disables highlighting.

Standard: Default highlighting for C# scripts.

JSON: Syntax highlighting for JSON files.

GDScript: Syntax highlighting for GDScript files.

The Search menu provides the following options:

Find...: Opens the quick-find bar under the status bar to search for text in the open file. You can navigate to the next match and previous match using the up and down arrows, respectively. Checking Match Case makes the search case-sensitive. Checking Whole Words means that the text must not have any letters or numbers next to it, only symbols and whitespace.

Find Next: Similar to the down arrow, shows the next occurrence.

Find Previous: Similar to the up arrow, shows the previous occurrence.

Replace...: Opens the find and replace bar under the status bar to find text and replace it in the open file. You can choose to replace them one at a time or all at once. Additionally, you can limit the replacement to the selected text by checking the Selection Only checkbox in the find and replace bar. You can also use Ctrl + D to additionally select the next instance of the currently selected text, allowing you to perform an in-line replacement on multiple occurrences.

Find in Files...: Opens a window to search for text within the files in the project folder. Selecting "Find..." starts with the chosen folder, and includes the file extensions checked in the filters. The results are shown in the bottom panel with the number of matches and total number of files found, in the Search Results tab. Clicking on a result opens the file and jumps to the respective line.

Replace in Files...: Opens a window to search and replace text with different text within the found files in the project folder. After clicking Replace..., you can select in which files to replace using the Search Results tab in the bottom panel by (un)checking them and using Replace All button.

Note that "Replace in Files" operation cannot be undone!

Both the Find in Files and Replace in Files windows share the Search... and Replace... buttons. The only difference in the latter window is an additional text field that automatically fills in the search results panel when the Replace... button is clicked. The replacement operation is only executed if you click the Replace All button in this bottom panel, allowing you to also edit the word to replace later within this panel.

Contextual Help*: Opens the list of built-in class reference similar to pressing F1 on a symbol, or choosing Lookup Symbol from the context menu.

The Go To menu lets you navigate within the code at ease with these options:

Go to Function...: Opens the function list to jump to. You can achieve the same result by typing in the filter methods bar in the script panel.

Go to Line...: Jumps to the entered line number in the code editor.

Bookmarks: Contains actions for the bookmark functionality, which you can use to find your way through your code easier, such as an incomplete section. Bookmarked lines will have a blue bookmark symbol left of the line number.

Toggle Bookmark*: Adds or removes the bookmark on the line where the caret is. You can also right click on a line to achieve this.

Remove All Bookmarks: Removes all bookmarks in the open document.

Go to Next Bookmark: Jumps to the next bookmark in the open document.

Go to Previous Bookmark: Jumps to the previous bookmark in the open document.

Bookmarks menu will also contain the list of bookmarked lines, including their line number and displaying the partial content in that line.

Breakpoints: Breakpoints are helpful while debugging your code. Similar to Bookmarks menu, this menu lets you add or remove breakpoints, navigate between them and directly jump to a specific breakpoint. An easy way to add a breakpoint is hovering over the blank area left of a line number. It will show a faded red circle. Clicking it will add a breakpoint and the circle will stay there. Clicking on a circle removes the breakpoint.

Debug menu offers actions which can be used while debugging. See Script editor debug tools and options for more.

This section will only cover the basics of the coding area in terms of the user interface. To learn more about scripting in Godot, refer to the GDScript or Scripting documentation.

The coding area is where you will type your scripts if you are using the built-in text editor. It offers highlighting and auto-completion features to help you while you code.

The coding area shows line numbers on the left side. Below the navigation arrows on the right side, there is a clickable minimap that provides an overview of the entire script, allowing you to scroll through it.

If a line of code is long enough (more than 80 characters, by default), the text editor will display a vertical line that can be used as a soft guideline. For a hard guideline, this value is set to 100 characters, by default. Both values can be changed, or the display of the line can be toggled in the "Appearance" settings of the text editor.

In the script, to the left of function definitions, you might see additional icons. The icon indicates that this function is an override of an existing function. Clicking it opens the documentation of the original function. The icon means that it is a receiving method of a signal. Clicking it shows where the signal is coming from. A icon to the left of the line denotes a foldable block. You can click to collapse or expand it. Alternatively, the ellipsis (...) icon can also be clicked to expand a folded block.

The example below summarizes the paragraph above. Lines 52, 56, and 58 are foldable blocks, line 57 is a code region with the name "New Code Region," which you can also fold, and line 62 is a folded block. Line 53 is a bookmark, which can quickly be jumped to using the Go To > Bookmarks menu. Line 55 is a breakpoint that can be used in debugging.

Many of the colors of the text editor such as highlighting colors, or even breakpoint or bookmark icon colors can be customized. You can experiment them by opening the text editor settings navigating to Editor > Editor Settings > Text Editor section.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Upgrading from Godot 4.3 to Godot 4.4 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.4.html

**Contents:**
- Upgrading from Godot 4.3 to Godot 4.4
- Breaking changes
  - Core
  - GUI nodes
  - Physics
  - Rendering
  - Navigation
  - Editor plugins
- Behavior changes
  - Core

For most games and apps made with 4.3 it should be relatively safe to migrate to 4.4. This page intends to cover everything you need to pay attention to when migrating your project.

If you are migrating from 4.3 to 4.4, the breaking changes listed here might affect you. Changes are grouped by areas/systems.

This article indicates whether each breaking change affects GDScript and whether the C# breaking change is binary compatible or source compatible:

Binary compatible - Existing binaries will load and execute successfully without recompilation, and the run-time behavior won't change.

Source compatible - Source code will compile successfully without changes when upgrading Godot.

Method open_encrypted adds a new iv optional parameter

Method store_8 changes return type from void to bool

Method store_16 changes return type from void to bool

Method store_32 changes return type from void to bool

Method store_64 changes return type from void to bool

Method store_buffer changes return type from void to bool

Method store_csv_line changes return type from void to bool

Method store_double changes return type from void to bool

Method store_float changes return type from void to bool

Method store_half changes return type from void to bool

Method store_line changes return type from void to bool

Method store_pascal_string changes return type from void to bool

Method store_real changes return type from void to bool

Method store_string changes return type from void to bool

Method store_var changes return type from void to bool

Method execute_with_pipe adds a new blocking optional parameter

Method read_string_from_stdin adds a new buffer_size parameter [1]

Method compile adds a new show_error optional parameter

Method create_from_string adds a new show_error optional parameter

Method post adds a new count optional parameter

Method standardize_locale adds a new add_defaults optional parameter

The behavior of @export_file changed in Godot 4.4. When assigning a new value from the Inspector, the path is now stored and returned as a uid:// reference instead of the traditional res:// path(GH-97912). This is a breaking change and may cause issues if you're expecting res://-based paths in scripts or serialized files.

For example, exported arrays of files may now contain a mix of uid:// and res:// paths, especially if they were partially edited in the Inspector.

In 4.4, the only way to retain the res:// format is to manually edit the .tscn or .tres files in a text editor. Starting in Godot 4.5, a new annotation @export_file_path can be used to explicitly retain the old behavior and export raw res:// paths.

Default buffer size in 4.3 is 1024.

Method push_meta adds a new tooltip optional parameter

Method set_table_column_expand adds a new shrink optional parameter

Method connect_node adds a new keep_alive optional parameter

Signal frame_rect_changed changes new_rect parameter type from Vector2 to Rect2

Method set_point_pinned adds a new insert_at optional parameter

Method restart adds a new keep_seed optional parameter

Method restart adds a new keep_seed optional parameter

Method restart adds a new keep_seed optional parameter

Method restart adds a new keep_seed optional parameter

Method draw_list_begin adds a new breadcrumb optional parameter

Method draw_list_begin removes many parameters

Method index_buffer_create adds a new enable_device_address optional parameter

Method uniform_buffer_create adds a new enable_device_address optional parameter

Method vertex_buffer_create adds a new enable_device_address optional parameter

Method multimesh_allocate_data adds a new use_indirect optional parameter

Method get_default_texture_parameter changes return type from Texture2D to Texture

Method set_default_texture_parameter changes texture parameter type from Texture2D to Texture

VisualShaderNodeCubemap

Property cube_map changes type from Cubemap to TextureLayered

VisualShaderNodeTexture2DArray

Property texture_array changes type from Texture2DArray to TextureLayered

In C#, the enum RenderingDevice.StorageBufferUsage breaks compatibility because of the way the bindings generator detects the enum prefix. New members where added in GH-100062 to the enum that caused the enum members to be renamed.

Method query_path adds a new callback optional parameter

Method query_path adds a new callback optional parameter

Method open_scene_from_path adds a new set_inherited optional parameter

Method popup_node_selector adds a new current_value optional parameter

Method popup_property_selector adds a new current_value optional parameter

EditorSceneFormatImporter

Method _get_import_flags removed

EditorTranslationParserPlugin

Method _parse_file changes return type to Array and removes msgids and msgids_context_plural parameters

The method _get_import_flags was never used by the engine. It was removed despite the compatibility breakage as there's no way for users to rely on this affecting engine behavior.

The Curve resource now enforces its value range, so min_value and max_value need to be changed if any of the points fall outside of the default [0, 1] range.

The VisualShaderNodeVec4Constant shader node had its input type changed to Vector4. Users need to recreate the values in their constants.

The CSG implementation now uses Emmett Lalish's Manifold library (GH-94321). The new implementation is more consistent with manifold definitions and fixes a number of bugs and stability issues. As a result, non-manifold meshes are no longer supported. You can use MeshInstance3D for rendering non-manifold geometry, such as quads or planes.

Android sensor events are no longer enabled by default (GH-94799). Projects that use sensor events can enable them as needed in Project Settings under Input Devices > Sensors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Upgrading from Godot 4.2 to Godot 4.3 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.3.html

**Contents:**
- Upgrading from Godot 4.2 to Godot 4.3
- Breaking changes
  - GDExtension
  - Animation
  - GUI nodes
  - Physics
  - Rendering
  - Text
  - Audio
  - Navigation

For most games and apps made with 4.2 it should be relatively safe to migrate to 4.3. This page intends to cover everything you need to pay attention to when migrating your project.

If you are migrating from 4.2 to 4.3, the breaking changes listed here might affect you. Changes are grouped by areas/systems.

This article indicates whether each breaking change affects GDScript and whether the C# breaking change is binary compatible or source compatible:

Binary compatible - Existing binaries will load and execute successfully without recompilation, and the runtime behavior won't change.

Source compatible - Source code will compile successfully without changes when upgrading Godot.

Method close_library removed

Method initialize_library removed

Method open_library removed

Since it was basically impossible to use these methods in any useful way, these methods have been removed. Use GDExtensionManager::load_extension and GDExtensionManager::unload_extension instead to correctly load and unload a GDExtension.

Method position_track_interpolate adds a new backward optional parameter

Method rotation_track_interpolate adds a new backward optional parameter

Method scale_track_interpolate adds a new backward optional parameter

Method blend_shape_track_interpolate adds a new backward optional parameter

Method value_track_interpolate adds a new backward optional parameter

Method track_find_key adds a new limit optional parameter

Method track_find_key adds a new backward optional parameter

Method _post_process_key_value changes object parameter type from Object to uint64

Method add_bone changes return type from void to int32

Signal bone_pose_changed replaced by skeleton_updated

Method on_bone_pose_update replaced by on_skeleton_update

Method register_text_enter changes parameter line_edit type from Control to LineEdit

Method remove_button changes parameter button type from Control to Button

PhysicsShapeQueryParameters3D

Property motion changes type from Vector2 to Vector3

In C#, the enum PhysicsServer3D.G6DofJointAxisFlag breaks compatibility because of the way the bindings generator detects the enum prefix. New members were added in GH-89851 to the enum that caused the enum members to be renamed.

Enum field FinalAction.FINAL_ACTION_CONTINUE changes value from 2 to 0

Enum field InitialAction.INITIAL_ACTION_CLEAR changes value from 0 to 1

Enum field InitialAction.INITIAL_ACTION_CLEAR_REGION_CONTINUE changes value from 2 to 1

Enum field InitialAction.INITIAL_ACTION_CONTINUE changes value from 5 to 0

Enum field InitialAction.INITIAL_ACTION_DROP changes value from 4 to 2

Enum field InitialAction.INITIAL_ACTION_KEEP changes value from 3 to 0

Method buffer_clear removes post_barrier parameter

Method buffer_update removes post_barrier parameter

Method compute_list_begin removes allow_draw_overlap parameter

Method compute_list_end removes post_barrier parameter

Method draw_list_begin removes storage_textures parameter

Method draw_list_end removes post_barrier parameter

Method texture_clear removes post_barrier parameter

Method texture_copy removes post_barrier parameter

Method texture_resolve_multisample removes post_barrier parameter

Method texture_update removes post_barrier parameter

Method environment_set_fog adds a new fog_mode optional parameter

Method get_color_layer adds a new msaa optional parameter

Method get_depth_layer adds a new msaa optional parameter

Method get_velocity_layer adds a new msaa optional parameter

Method get_color_texture adds a new msaa optional parameter

Method get_depth_texture adds a new msaa optional parameter

Method get_velocity_texture adds a new msaa optional parameter

While the values of the enum fields in RenderingDevice.InitialAction and RenderingDevice.FinalAction changed, the only method that consumed them (draw_list_begin) added a compatibility method which supports the old values. So in practice it doesn't break compatibility.

In C#, the enum RenderingDevice.DriverResource breaks compatibility because of the way the bindings generator detects the enum prefix. New members were added in GH-83452 to the enum that caused the enum members to be renamed.

Method find_variation adds a new baseline_offset optional parameter

Method push_meta adds a new underline_mode optional parameter

Method shaped_text_get_word_breaks adds a new optional skip_grapheme_flags parameter

Method _shaped_text_get_word_breaks adds a new skip_grapheme_flags parameter

AudioStreamPlaybackPolyphonic

Method play_stream adds new playback_type, and bus optional parameters

Method get_id_path adds new allow_partial_path optional parameter

Method get_point_path adds new allow_partial_path optional parameter

Method get_id_path adds new allow_partial_path optional parameter

Method get_point_path adds new allow_partial_path optional parameter

Method get_id_path adds new allow_partial_path optional parameter

Method get_point_path adds new allow_partial_path optional parameter

Property avoidance_layers removed

Property constrain_avoidance removed

Method get_avoidance_layer_value removed

Method set_avoidance_layer_value removed

The constrain avoidance feature in NavigationRegion2D was experimental and has been discontinued with no replacement.

Method get_navigation_polygon adds new flip_h, flip_v, and transpose optional parameters

Method get_occluder adds new flip_h, flip_v, and transpose optional parameters

Method get_input_source_tracker changes return type from XRPositionalTracker to XRControllerTracker

Method get_tracker changes return type from XRPositionalTracker to XRTracker

EditorInspectorPlugin

Method add_property_editor adds a new label optional parameter

Method add_control_to_bottom_panel adds a new shortcut optional parameter

Method add_control_to_dock adds a new shortcut optional parameter

EditorSceneFormatImporterFBX

Type renamed to EditorSceneFormatImporterFBX2GLTF

In 4.3, some behavior changes have been introduced, which might require you to adjust your project.

Binary serialization was modified to fix some issues with the serialization of scripted Objects and typed Arrays (GH-78219). This breaks compat with script encoding/decoding.

PackedByteArray is now able to use a more compact base64 encoding for storage. But the trade-off is that it breaks compatibility, meaning that older versions of Godot may not be able to open resources saved by 4.3 (GH-89186).

To maximize compatibility, this new storage format will only be enabled for resources and scenes that contain large PackedByteArrays for now. Support for this new format will also be added in patch updates for older versions of Godot. Once all supported Godot versions are able to read the new format, we will gradually retire the compatibility measures and have all resources and scenes use the new storage format.

In C#, the Transform3D.InterpolateWith implementation was fixed to use the right order of operations, applying the rotation before the scale (GH-89843).

In C#, the Aabb.GetSupport implementation was fixed to properly return the support vector (GH-88919).

In C#, the Variant types' ToString implementation now defaults to using the InvariantCulture (GH-89547) which means Vector2(1.2, 3.4) is formatted using . as the decimal separator independently of the language of the operating system that the program is running on.

AnimationMixer replaced its Capture mode with a new Capture feature that works much better than the old one, this replaces the existing cache (GH-86715).

AnimationNode has a reworked process for retrieving the semantic time info. This ensures that time-related behavior works as expected, but changes the blending behavior. Implementors of the _process virtual method should also note that this method is now deprecated and will be replaced by a new one in the future (GH-87171).

More information about the changes to Animation can be found in the Migrating Animations from Godot 4.0 to 4.3 article.

The default font outline color was changed from white to black (GH-54641).

The auto_translate property is deprecated in favor of the auto_translate_mode property which is now in Node (GH-87530). The default value for auto_translate_mode is AUTO_TRANSLATE_INHERIT, which means nodes inherit the auto_translate_mode value from their parent. This means, existing nodes with the auto_translate property set to true may no longer be translated if they are children of a node with the auto_translate property set to false.

The SceneMultiplayer caching protocol was changed to send the received ID instead of the Node path when sending a node removal confirmation packet (GH-90027).

This is a breaking change for the high-level multiplayer protocol making it incompatible with previous Godot versions. Upgrade both your server and client versions to Godot 4.3 to handle this change gracefully.

Note that high-level multiplayer facilities are only ever meant to be compatible with server and client using the same Godot version. It is recommended to implement some kind of version checking.

Decals now convert the modulate color from an sRGB color to a linear color, like all other inputs, to ensure proper blending (GH-89849). Existing projects that were using the decal's modulate property will notice a change in their visuals.

The reverse Z depth buffer technique is now implemented. This may break compatibility for some shaders. Read the Introducing Reverse Z (AKA I'm sorry for breaking your shader) article for more information and guidance on how to fix common scenarios.

TileMap layers were moved to individual nodes (GH-87379 and GH-89179).

Android permissions are no longer requested automatically because it goes against the recommended best practices (GH-87080). Use the request_permission method in OS and the on_request_permissions_result signal on MainLoop to request permissions and wait for the user response.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Export — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/index.html

**Contents:**
- Export

This section is about exporting a build of your project. If you're trying to export properties from a script, see GDScript exported properties or C# exported properties.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Scripting — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/index.html

**Contents:**
- Scripting
- Programming languages
- Core features

This section covers programming languages and core features to code your games in Godot.

Here, you will find information that is not already covered in more specific sections. For instance, to learn about inputs, we recommend you to read Inputs.

The sections below each focus on a given programming language.

Some features are specific to the engine and are available in all supported languages. Whether you code in GDScript, C#, or another language, the pages below will help you make the most of Godot.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GDScript style guide — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html

**Contents:**
- GDScript style guide
- Formatting
  - Encoding and special characters
  - Indentation
  - Trailing comma
  - Blank lines
  - Line length
  - One statement per line
  - Format multiline statements for readability
  - Avoid unnecessary parentheses

This style guide lists conventions to write elegant GDScript. The goal is to encourage writing clean, readable code and promote consistency across projects, discussions, and tutorials. Hopefully, this will also support the development of auto-formatting tools.

Since GDScript is close to Python, this guide is inspired by Python's PEP 8 programming style guide.

Style guides aren't meant as hard rulebooks. At times, you may not be able to apply some of the guidelines below. When that happens, use your best judgment, and ask fellow developers for insights.

In general, keeping your code consistent in your projects and within your team is more important than following this guide to a tee.

Godot's built-in script editor uses a lot of these conventions by default. Let it help you.

Here is a complete class example based on these guidelines:

Use line feed (LF) characters to break lines, not CRLF or CR. (editor default)

Use one line feed character at the end of each file. (editor default)

Use UTF-8 encoding without a byte order mark. (editor default)

Use Tabs instead of spaces for indentation. (editor default)

Each indent level should be one greater than the block containing it.

Use 2 indent levels to distinguish continuation lines from regular code blocks.

Exceptions to this rule are arrays, dictionaries, and enums. Use a single indentation level to distinguish continuation lines:

Use a trailing comma on the last line in arrays, dictionaries, and enums. This results in easier refactoring and better diffs in version control as the last line doesn't need to be modified when adding new elements.

Trailing commas are unnecessary in single-line lists, so don't add them in this case.

Surround functions and class definitions with two blank lines:

Use one blank line inside functions to separate logical sections.

We use a single line between classes and function definitions in the class reference and in short code snippets in this documentation.

Keep individual lines of code under 100 characters.

If you can, try to keep lines under 80 characters. This helps to read the code on small displays and with two scripts opened side-by-side in an external text editor. For example, when looking at a differential revision.

Avoid combining multiple statements on a single line, including conditional statements, to adhere to the GDScript style guidelines for readability.

The only exception to that rule is the ternary operator:

When you have particularly long if statements or nested ternary expressions, wrapping them over multiple lines improves readability. Since continuation lines are still part of the same expression, 2 indent levels should be used instead of one.

GDScript allows wrapping statements using multiple lines using parentheses or backslashes. Parentheses are favored in this style guide since they make for easier refactoring. With backslashes, you have to ensure that the last line never contains a backslash at the end. With parentheses, you don't have to worry about the last line having a backslash at the end.

When wrapping a conditional expression over multiple lines, the and/or keywords should be placed at the beginning of the line continuation, not at the end of the previous line.

Avoid parentheses in expressions and conditional statements. Unless necessary for order of operations or wrapping over multiple lines, they only reduce readability.

Prefer the plain English versions of boolean operators, as they are the most accessible:

Use and instead of &&.

Use or instead of ||.

Use not instead of !.

You may also use parentheses around boolean operators to clear any ambiguity. This can make long expressions easier to read.

Regular comments (#) and documentation comments (##) should start with a space, but not code that you comment out. Additionally, code region comments (#region/#endregion) must follow that precise syntax, so they should not start with a space.

Using a space for regular and documentation comments helps differentiate text comments from disabled code.

In the script editor, to toggle commenting of the selected code, press Ctrl + K. This feature adds/removes a single # sign before any code on the selected lines.

Prefer writing comments on their own line as opposed to inline comments (comments written on the same line as code). Inline comments are best used for short comments, typically a few words at most:

Always use one space around operators and after commas. Also, avoid extra spaces in dictionary references and function calls. One exception to this is for single-line dictionary declarations, where a space should be added after the opening brace and before the closing brace. This makes the dictionary easier to visually distinguish from an array, as the [] characters look close to {} with most fonts.

Don't use spaces to align expressions vertically:

Use double quotes unless single quotes make it possible to escape fewer characters in a given string. See the examples below:

Don't omit the leading or trailing zero in floating-point numbers. Otherwise, this makes them less readable and harder to distinguish from integers at a glance.

Use lowercase for letters in hexadecimal numbers, as their lower height makes the number easier to read.

Take advantage of GDScript's underscores in literals to make large numbers more readable.

These naming conventions follow the Godot Engine style. Breaking these will make your code clash with the built-in naming conventions, leading to inconsistent code. As a summary table:

class_name YAMLParser

const MAX_SPEED = 200

{EARTH, WATER, AIR, FIRE}

Use snake_case for file names. For named classes, convert the PascalCase class name to snake_case:

This is consistent with how C++ files are named in Godot's source code. This also avoids case sensitivity issues that can crop up when exporting a project from Windows to other platforms.

Use PascalCase for class and node names:

Also use PascalCase when loading a class into a constant or a variable:

Use snake_case to name functions and variables:

Prepend a single underscore (_) to virtual methods functions the user must override, private functions, and private variables:

Use the past tense to name signals:

Write constants with CONSTANT_CASE, that is to say in all caps with an underscore (_) to separate words:

Use PascalCase for enum names and keep them singular, as they represent a type. Use CONSTANT_CASE for their members, as they are constants:

Write enums with each item on its own line. This allows adding documentation comments above each item more easily, and also makes for cleaner diffs in version control when items are added or removed.

This section focuses on code order. For formatting, see Formatting. For naming conventions, see Naming conventions.

We suggest to organize GDScript code this way:

And put the class methods and variables in the following order depending on their access modifiers:

We optimized the order to make it easy to read the code from top to bottom, to help developers reading the code for the first time understand how it works, and to avoid errors linked to the order of variable declarations.

This code order follows four rules of thumb:

Properties and signals come first, followed by methods.

Public comes before private.

Virtual callbacks come before the class's interface.

The object's construction and initialization functions, _init and _ready, come before functions that modify the object at runtime.

If the code is meant to run in the editor, place the @tool annotation on the first line of the script.

Follow with the optional @icon then the class_name if necessary. You can turn a GDScript file into a global type in your project using class_name. For more information, see Registering named classes. If the class is meant to be an abstract class, add @abstract before the class_name keyword.

Then, add the extends keyword if the class extends a built-in type.

Following that, you should have the class's optional documentation comments. You can use that to explain the role of your class to your teammates, how it works, and how other developers should use it, for example.

For inner classes, use single-line declarations:

Write signal declarations, followed by properties, that is to say, member variables, after the docstring.

Enums should come after signals, as you can use them as export hints for other properties.

Then, write constants, exported variables, public, private, and onready variables, in that order.

GDScript evaluates @onready variables right before the _ready callback. You can use that to cache node dependencies, that is to say, to get child nodes in the scene that your class relies on. This is what the example above shows.

Don't declare member variables if they are only used locally in a method, as it makes the code more difficult to follow. Instead, declare them as local variables in the method's body.

Declare local variables as close as possible to their first use. This makes it easier to follow the code, without having to scroll too much to find where the variable was declared.

After the class's properties come the methods.

Start with the _init() callback method, that the engine will call upon creating the object in memory. Follow with the _ready() callback, that Godot calls when it adds a node to the scene tree.

These functions should come first because they show how the object is initialized.

Other built-in virtual callbacks, like _unhandled_input() and _physics_process, should come next. These control the object's main loop and interactions with the game engine.

The rest of the class's interface, public and private methods, come after that, in that order.

GDScript supports optional static typing.

To declare a variable's type, use <variable>: <type>:

To declare the return type of a function, use -> <type>:

In most cases, you can let the compiler infer the type using :=. Prefer := when the type is written on the same line as the assignment, otherwise prefer writing the type explicitly.

Include the type hint when the type is ambiguous, and omit the type hint when it's redundant.

In some cases, the type must be stated explicitly, otherwise the behavior will not be as expected because the compiler will only be able to use the function's return type. For example, get_node() cannot infer a type unless the scene or file of the node is loaded in memory. In this case, you should set the type explicitly.

Alternatively, you can use the as keyword to cast the return type, and that type will be used to infer the type of the var.

This option is considered more type-safe than type hints, but also less null-safe as it silently casts the variable to null in case of a type mismatch at runtime, without an error/warning.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
class_name StateMachine
extends Node
## Hierarchical State machine for the player.
##
## Initializes states and delegates engine callbacks ([method Node._physics_process],
## [method Node._unhandled_input]) to the state.

signal state_changed(previous, new)

@export var initial_state: Node
var is_active = true:
    set = set_is_active

@onready var _state = initial_state:
    set = set_state
@onready var _state_name = _state.name


func _init():
    add_to_group("state_machine")


func _enter_tree():
    print("this happens before the ready method!")


func _ready():
    state_changed.connect(_on_state_changed)
    _state.enter()


func _unhandled_input(event):
    _state.unhandled_input(event)


func _physics_process(delta):
    _state.physics_process(delta)


func transition_to(target_state_path, msg={}):
    if not has_node(target_state_path):
        return

    var target_state = get_node(target_state_path)
    assert(target_state.is_composite == false)

    _state.exit()
    self._state = target_state
    _state.enter(msg)
    Events.player_state_changed.emit(_state.name)


func set_is_active(value):
    is_active = value
    set_physics_process(value)
    set_process_unhandled_input(value)
    set_block_signals(not value)


func set_state(value):
    _state = value
    _state_name = _state.name


func _on_state_changed(previous, new):
    print("state changed")
    state_changed.emit()


class State:
    var foo = 0

    func _init():
        print("Hello!")
```

Example 2 (python):
```python
for i in range(10):
    print("hello")
```

Example 3 (python):
```python
for i in range(10):
  print("hello")

for i in range(10):
        print("hello")
```

Example 4 (csharp):
```csharp
effect.interpolate_property(sprite, "transform/scale",
        sprite.get_scale(), Vector2(2.0, 2.0), 0.3,
        Tween.TRANS_QUAD, Tween.EASE_OUT)
```

---

## GDScript reference — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html

**Contents:**
- GDScript reference
- History
- Example of GDScript
- Identifiers
- Keywords
- Operators
- Literals
- Annotations
  - @onready annotation
- Comments

GDScript is a high-level, object-oriented, imperative, and gradually typed programming language built for Godot. It uses an indentation-based syntax similar to languages like Python. Its goal is to be optimized for and tightly integrated with Godot Engine, allowing great flexibility for content creation and integration.

GDScript is entirely independent from Python and is not based on it.

Documentation about GDScript's history has been moved to the Frequently Asked Questions.

Some people can learn better by taking a look at the syntax, so here's an example of how GDScript looks.

If you have previous experience with statically typed languages such as C, C++, or C# but never used a dynamically typed one before, it is advised you read this tutorial: GDScript: An introduction to dynamic languages.

Any string that restricts itself to alphabetic characters (a to z and A to Z), digits (0 to 9) and _ qualifies as an identifier. Additionally, identifiers must not begin with a digit. Identifiers are case-sensitive (foo is different from FOO).

Identifiers may also contain most Unicode characters part of UAX#31. This allows you to use identifier names written in languages other than English. Unicode characters that are considered "confusable" for ASCII characters and emoji are not allowed in identifiers.

The following is the list of keywords supported by the language. Since keywords are reserved words (tokens), they can't be used as identifiers. Operators (like in, not, and or or) and names of built-in types as listed in the following sections are also reserved.

Keywords are defined in the GDScript tokenizer in case you want to take a look under the hood.

Used by pattern guards in match statements.

Exits the execution of the current for or while loop.

Immediately skips to the next iteration of the for or while loop.

Used where a statement is required syntactically but execution of code is undesired, e.g. in empty functions.

Returns a value from a function.

Defines an inner class. See Inner classes.

Defines the script as a globally accessible class with the specified name. See Registering named classes.

Defines what class to extend with the current class.

Tests whether a variable extends a given class, or is of a given built-in type.

Tests whether a value is within a string, array, range, dictionary, or node. When used with for, it iterates through them instead of testing.

Cast the value to a given type if possible.

Refers to current class instance. See self.

Resolves the scope of the parent method. See Inheritance.

Defines a signal. See Signals.

Defines a function. See Functions.

Defines a static function or a static member variable.

Defines a constant. See Constants.

Defines an enum. See Enums.

Defines a variable. See Variables.

Editor helper for debugger breakpoints. Unlike breakpoints created by clicking in the gutter, breakpoint is stored in the script itself. This makes it persistent across different machines when using version control.

Preloads a class or variable. See Classes as resources.

Waits for a signal or a coroutine to finish. See Awaiting signals or coroutines.

Previously used for coroutines. Kept as keyword for transition.

Asserts a condition, logs error on failure. Ignored in non-debug builds. See Assert keyword.

Used to represent that a function does not return any value.

Infinity constant. Used for comparisons and as result of calculations.

NAN (not a number) constant. Used as impossible result from calculations.

The following is the list of supported operators and their precedence. All binary operators are left-associative, including the ** operator. This means that 2 ** 2 ** 3 is equal to (2 ** 2) ** 3. Use parentheses to explicitly specify precedence you need, for example 2 ** (2 ** 3). The ternary if/else operator is right-associative.

Grouping (highest priority)

Parentheses are not really an operator, but allow you to explicitly specify the precedence of an operation.

Awaiting signals or coroutines

See also is_instance_of() function.

Multiplies x by itself y times, similar to calling pow() function.

Multiplication / Division / Remainder

The % operator is additionally used for format strings.

Note: These operators have the same behavior as C++, which may be unexpected for users coming from Python, JavaScript, etc. See a detailed note after the table.

Addition (or Concatenation) / Subtraction

See a detailed note after the table.

in is also used with the for keyword as part of the syntax.

Boolean NOT and its unrecommended alias

Boolean AND and its unrecommended alias

Boolean OR and its unrecommended alias

true_expr if cond else false_expr

Assignment (lowest priority)

You cannot use an assignment operator inside an expression.

The behavior of some operators may differ from what you expect:

If both operands of the / operator are int, then integer division is performed instead of fractional. For example 5 / 2 == 2, not 2.5. If this is not desired, use at least one float literal (x / 2.0), cast (float(x) / y), or multiply by 1.0 (x * 1.0 / y).

The % operator is only available for ints, for floats use the fmod() function.

For negative values, the % operator and fmod() use truncation instead of rounding towards negative infinity. This means that the remainder has a sign. If you need the remainder in a mathematical sense, use the posmod() and fposmod() functions instead.

The == and != operators sometimes allow you to compare values of different types (for example, 1 == 1.0 is true), but in other cases it can cause a runtime error. If you're not sure about the types of the operands, you can safely use the is_same() function (but note that it is more strict about types and references). To compare floats, use the is_equal_approx() and is_zero_approx() functions instead.

Base 16 (hexadecimal) integer

Base 2 (binary) integer

Floating-point number (real)

"""Hello""", '''Hi'''

Triple-quoted regular strings

r"""Hello""", r'''Hi'''

Triple-quoted raw strings

There are also two constructs that look like literals, but actually are not:

Shorthand for get_node("NodePath")

Shorthand for get_node("%UniqueNode")

Integers and floats can have their numbers separated with _ to make them more readable. The following ways to write numbers are all valid:

Regular string literals can contain the following escape sequences:

Horizontal tab character

Vertical tab character

UTF-16 Unicode codepoint XXXX (hexadecimal, case-insensitive)

UTF-32 Unicode codepoint XXXXXX (hexadecimal, case-insensitive)

There are two ways to represent an escaped Unicode character above 0xFFFF:

as a UTF-16 surrogate pair \uXXXX\uXXXX.

as a single UTF-32 codepoint \UXXXXXX.

Also, using \ followed by a newline inside a string will allow you to continue it in the next line, without inserting a newline character in the string itself.

A string enclosed in quotes of one type (for example ") can contain quotes of another type (for example ') without escaping. Triple-quoted strings allow you to avoid escaping up to two consecutive quotes of the same type (unless they are adjacent to the string edges).

Raw string literals always encode the string as it appears in the source code. This is especially useful for regular expressions. A raw string literal doesn't process escape sequences, however it does recognize \\ and \" (\') and replaces them with themselves. Thus, a string can have a quote that matches the opening one, but only if it's preceded by a backslash.

Some strings cannot be represented using raw string literals: you cannot have an odd number of backslashes at the end of a string or have an unescaped opening quote inside the string. However, in practice this doesn't matter since you can use a different quote type or use concatenation with a regular string literal.

GDScript also supports format strings.

Annotations are special tokens in GDScript that act as modifiers to a script or its code and may affect how the script is treated by the Godot engine or editor.

Every annotation starts with the @ character and is specified by a name. A detailed description and example for each annotation can be found inside the GDScript class reference.

For instance, you can use it to export a value to the editor:

For more information about exporting properties, read the GDScript exports article.

Any constant expression compatible with the required argument type can be passed as an annotation argument value:

Annotations can be specified one per line or all in the same line. They affect the next statement that isn't an annotation. Annotations can have arguments sent between parentheses and separated by commas.

Both of these are the same:

When using nodes, it's common to desire to keep references to parts of the scene in a variable. As scenes are only warranted to be configured when entering the active scene tree, the sub-nodes can only be obtained when a call to Node._ready() is made.

This can get a little cumbersome, especially when nodes and external references pile up. For this, GDScript has the @onready annotation, that defers initialization of a member variable until _ready() is called. It can replace the above code with a single line:

Applying @onready and any @export annotation to the same variable doesn't work as you might expect. The @onready annotation will cause the default value to be set after the @export takes effect and will override it:

Therefore, the ONREADY_WITH_EXPORT warning is generated, which is treated as an error by default. We do not recommend disabling or ignoring it.

Anything from a # to the end of the line is ignored and is considered a comment.

In the Godot script editor, special keywords are highlighted within comments to bring the user's attention to specific comments:

Critical (appears in red): ALERT, ATTENTION, CAUTION, CRITICAL, DANGER, SECURITY

Warning (appears in yellow): BUG, DEPRECATED, FIXME, HACK, TASK, TBD, TODO, WARNING

Notice (appears in green): INFO, NOTE, NOTICE, TEST, TESTING

These keywords are case-sensitive, so they must be written in uppercase for them to be recognized:

The list of highlighted keywords and their colors can be changed in the Text Editor > Theme > Comment Markers section of the Editor Settings.

Use two hash symbols (##) instead of one (#) to add a documentation comment, which will appear in the script documentation and in the inspector description of an exported variable. Documentation comments must be placed directly above a documentable item (such as a member variable), or at the top of a file. Dedicated formatting options are also available. See GDScript documentation comments for details.

Code regions are special types of comments that the script editor understands as foldable regions. This means that after writing code region comments, you can collapse and expand the region by clicking the arrow that appears at the left of the comment. This arrow appears within a purple square to be distinguishable from standard code folding.

The syntax is as follows:

To create a code region quickly, select several lines in the script editor, right-click the selection then choose Create Code Region. The region description will be selected automatically for editing.

It is possible to nest code regions within other code regions.

Here's a concrete usage example of code regions:

This can be useful to organize large chunks of code into easier to understand sections. However, remember that external editors generally don't support this feature, so make sure your code is easy to follow even when not relying on folding code regions.

Individual functions and indented sections (such as if and for) can always be collapsed in the script editor. This means you should avoid using a code region to contain a single function or indented section, as it won't bring much of a benefit. Code regions work best when they're used to group multiple elements together.

A line of code in GDScript can be continued on the next line by using a backslash (\). Add one at the end of a line and the code on the next line will act like it's where the backslash is. Here is an example:

A line can be continued multiple times like this:

Built-in types are stack-allocated. They are passed as values. This means a copy is created on each assignment or when passing them as arguments to functions. The exceptions are Object, Array, Dictionary, and packed arrays (such as PackedByteArray), which are passed by reference so they are shared. All arrays, Dictionary, and some objects (Node, Resource) have a duplicate() method that allows you to make a copy.

A variable in GDScript can be assigned to several built-in types.

null is an empty data type that contains no information and can not be assigned any other value.

Only types that inherit from Object can have a null value (Object is therefore called a "nullable" type). Variant types must have a valid value at all times, and therefore cannot have a null value.

Short for "boolean", it can only contain true or false.

Short for "integer", it stores whole numbers (positive and negative). It is stored as a 64-bit value, equivalent to int64_t in C++.

Stores real numbers, including decimals, using floating-point values. It is stored as a 64-bit value, equivalent to double in C++. Note: Currently, data structures such as Vector2, Vector3, and PackedFloat32Array store 32-bit single-precision float values.

A sequence of characters in Unicode format.

An immutable string that allows only one instance of each name. They are slower to create and may result in waiting for locks when multithreading. In exchange, they're very fast to compare, which makes them good candidates for dictionary keys.

A pre-parsed path to a node or a node property. It can be easily assigned to, and from, a String. They are useful to interact with the tree to get a node, or affecting properties like with Tweens.

2D vector type containing x and y fields. Can also be accessed as an array.

Same as a Vector2 but the components are integers. Useful for representing items in a 2D grid.

2D Rectangle type containing two vectors fields: position and size. Also contains an end field which is position + size.

3D vector type containing x, y and z fields. This can also be accessed as an array.

Same as Vector3 but the components are integers. Can be use for indexing items in a 3D grid.

3×2 matrix used for 2D transforms.

3D Plane type in normalized form that contains a normal vector field and a d scalar distance.

Quaternion is a datatype used for representing a 3D rotation. It's useful for interpolating rotations.

Axis-aligned bounding box (or 3D box) contains 2 vectors fields: position and size. Also contains an end field which is position + size.

3x3 matrix used for 3D rotation and scale. It contains 3 vector fields (x, y and z) and can also be accessed as an array of 3D vectors.

3D Transform contains a Basis field basis and a Vector3 field origin.

Color data type contains r, g, b, and a fields. It can also be accessed as h, s, and v for hue/saturation/value.

Resource ID (RID). Servers use generic RIDs to reference opaque data.

Base class for anything that is not a built-in type.

Generic sequence of arbitrary object types, including other arrays or dictionaries (see below). The array can resize dynamically. Arrays are indexed starting from index 0. Negative indices count from the end.

Godot 4.0 added support for typed arrays. On write operations, Godot checks that element values match the specified type, so the array cannot contain invalid values. The GDScript static analyzer takes typed arrays into account, however array methods like front() and back() still have the Variant return type.

Typed arrays have the syntax Array[Type], where Type can be any Variant type, native or user class, or enum. Nested array types (like Array[Array[int]]) are not supported.

Array and Array[Variant] are the same thing.

Arrays are passed by reference, so the array element type is also an attribute of the in-memory structure referenced by a variable in runtime. The static type of a variable restricts the structures that it can reference to. Therefore, you cannot assign an array with a different element type, even if the type is a subtype of the required type.

If you want to convert a typed array, you can create a new array and use the Array.assign() method:

The only exception was made for the Array (Array[Variant]) type, for user convenience and compatibility with old code. However, operations on untyped arrays are considered unsafe.

PackedArrays are generally faster to iterate on and modify compared to a typed Array of the same type (e.g. PackedInt64Array versus Array[int]) and consume less memory. In the worst case, they are expected to be as fast as an untyped Array. Conversely, non-Packed Arrays (typed or not) have extra convenience methods such as Array.map that PackedArrays lack. Consult the class reference for details on the methods available. Typed Arrays are generally faster to iterate on and modify than untyped Arrays.

While all Arrays can cause memory fragmentation when they become large enough, if memory usage and performance (iteration and modification speed) is a concern and the type of data you're storing is compatible with one of the Packed Array types, then using those may yield improvements. However, if you do not have such concerns (e.g. the size of your array does not reach the tens of thousands of elements) it is likely more helpful to use regular or typed Arrays, as they provide convenience methods that can make your code easier to write and maintain (and potentially faster if your data requires such operations a lot). If the data you will store is of a known type (including your own defined classes), prefer to use a typed Array as it may yield better performance in iteration and modification compared to an untyped Array.

PackedByteArray: An array of bytes (integers from 0 to 255).

PackedInt32Array: An array of 32-bit integers.

PackedInt64Array: An array of 64-bit integers.

PackedFloat32Array: An array of 32-bit floats.

PackedFloat64Array: An array of 64-bit floats.

PackedStringArray: An array of strings.

PackedVector2Array: An array of Vector2 values.

PackedVector3Array: An array of Vector3 values.

PackedVector4Array: An array of Vector4 values.

PackedColorArray: An array of Color values.

Associative container which contains values referenced by unique keys.

Lua-style table syntax is also supported. Lua-style uses = instead of : and doesn't use quotes to mark string keys (making for slightly less to write). However, keys written in this form can't start with a digit (like any GDScript identifier), and must be string literals.

To add a key to an existing dictionary, access it like an existing key and assign to it:

The bracket syntax can be used to access properties of any Object, not just Dictionaries. Keep in mind it will cause a script error when attempting to index a non-existing property. To avoid this, use the Object.get() and Object.set() methods instead.

Godot 4.4 added support for typed dictionaries. On write operations, Godot checks that element keys and values match the specified type, so the dictionary cannot contain invalid keys or values. The GDScript static analyzer takes typed dictionaries into account. However, dictionary methods that return values still have the Variant return type.

Typed dictionaries have the syntax Dictionary[KeyType, ValueType], where KeyType and ValueType can be any Variant type, native or user class, or enum. Both the key and value type must be specified, but you can use Variant to make either of them untyped. Nested typed collections (like Dictionary[String, Dictionary[String, int]]) are not supported.

Dictionary and Dictionary[Variant, Variant] are the same thing.

A signal is a message that can be emitted by an object to those who want to listen to it. The Signal type can be used for passing the emitter around.

Signals are better used by getting them from actual objects, e.g. $Button.button_up.

Contains an object and a function, which is useful for passing functions as values (e.g. when connecting to signals).

Getting a method as a member returns a callable. var x = $Sprite2D.rotate will set the value of x to a callable with $Sprite2D as the object and rotate as the method.

You can call it using the call method: x.call(PI).

Variables can exist as class members or local to functions. They are created with the var keyword and may, optionally, be assigned a value upon initialization.

Variables can optionally have a type specification. When a type is specified, the variable will be forced to have always that same type, and trying to assign an incompatible value will raise an error.

Types are specified in the variable declaration using a : (colon) symbol after the variable name, followed by the type.

If the variable is initialized within the declaration, the type can be inferred, so it's possible to omit the type name:

Type inference is only possible if the assigned value has a defined type, otherwise it will raise an error.

Built-in types (Array, Vector2, int, String, etc.).

Engine classes (Node, Resource, RefCounted, etc.).

Constant names if they contain a script resource (MyScript if you declared const MyScript = preload("res://my_script.gd")).

Other classes in the same script, respecting scope (InnerClass.NestedClass if you declared class NestedClass inside the class InnerClass in the same scope).

Script classes declared with the class_name keyword.

Autoloads registered as singletons.

While Variant is a valid type specification, it's not an actual type. It only means there's no set type and is equivalent to not having a static type at all. Therefore, inference is not allowed by default for Variant, since it's likely a mistake.

You can turn off this check, or make it only a warning, by changing it in the project settings. See GDScript warning system for details.

Member variables are initialized in the following order:

Depending on the variable's static type, the variable is either null (untyped variables and objects) or has a default value of the type (0 for int, false for bool, etc.).

The specified values are assigned in the order of the variables in the script, from top to bottom.

(Only for Node-derived classes) If the @onready annotation is applied to a variable, its initialization is deferred to step 5.

If defined, the _init() method is called.

When instantiating scenes and resources, the exported values are assigned.

(Only for Node-derived classes) @onready variables are initialized.

(Only for Node-derived classes) If defined, the _ready() method is called.

You can specify a complex expression as a variable initializer, including function calls. Make sure the variables are initialized in the correct order, otherwise your values may be overwritten. For example:

To fix this, move the _data variable definition above the a definition or remove the empty dictionary assignment (= {}).

A class member variable can be declared static:

Static variables belong to the class, not instances. This means that static variables share values between multiple instances, unlike regular member variables.

From inside a class, you can access static variables from any function, both static and non-static. From outside the class, you can access static variables using the class or an instance (the second is not recommended as it is less readable).

The @export and @onready annotations cannot be applied to a static variable. Local variables cannot be static.

The following example defines a Person class with a static variable named max_id. We increment the max_id in the _init() function. This makes it easy to keep track of the number of Person instances in our game.

In this code, we create two instances of our Person class and check that the class and every instance have the same max_id value, because the variable is static and accessible to every instance.

Static variables can have type hints, setters and getters:

A base class static variable can also be accessed via a child class:

When referencing a static variable from a tool script, the other script containing the static variable must also be a tool script. See Running code in the editor for details.

Since GDScript classes are resources, having static variables in a script prevents it from being unloaded even if there are no more instances of that class and no other references left. This can be important if static variables store large amounts of data or hold references to other project resources, such as scenes. You should clean up this data manually, or use the @static_unload annotation if static variables don't store important data and can be reset.

Currently, due to a bug, scripts are never freed, even if @static_unload annotation is used.

Note that @static_unload applies to the entire script (including inner classes) and must be placed at the top of the script, before class_name and extends:

See also Static functions and Static constructor.

Values assigned to typed variables must have a compatible type. If it's needed to coerce a value to be of a certain type, in particular for object types, you can use the casting operator as.

Casting between object types results in the same object if the value is of the same type or a subtype of the cast type.

If the value is not a subtype, the casting operation will result in a null value.

For built-in types, they will be forcibly converted if possible, otherwise the engine will raise an error.

Casting is also useful to have better type-safe variables when interacting with the scene tree:

Constants are values you cannot change when the game is running. Their value must be known at compile-time. Using the const keyword allows you to give a constant value a name. Trying to assign a value to a constant after it's declared will give you an error.

We recommend using constants whenever a value is not meant to change.

Although the type of constants is inferred from the assigned value, it's also possible to add explicit type specification:

Assigning a value of an incompatible type will raise an error.

You can also create constants inside a function, which is useful to name local magic values.

Enums are basically a shorthand for constants, and are pretty useful if you want to assign consecutive integers to some constant.

If you pass a name to the enum, it will put all the keys inside a constant Dictionary of that name. This means all constant methods of a dictionary can also be used with a named enum.

Keys in a named enum are not registered as global constants. They should be accessed prefixed by the enum's name (Name.KEY).

If not assigning a value to a key of an enum it will be assigned the previous value plus one, or 0 if it is the first entry in the enum. Multiple keys with the same value are allowed.

Functions always belong to a class. The scope priority for variable look-up is: local → class member → global. The self variable is always available and is provided as an option for accessing class members (see self), but is not always required (and should not be sent as the function's first argument, unlike Python).

A function can return at any point. The default return value is null.

If a function contains only one line of code, it can be written on one line:

Functions can also have type specification for the arguments and for the return value. Types for arguments can be added in a similar way to variables:

If a function argument has a default value, it's possible to infer the type:

The return type of the function can be specified after the arguments list using the arrow token (->):

Functions that have a return type must return a proper value. Setting the type as void means the function doesn't return anything. Void functions can return early with the return keyword, but they can't return any value.

Non-void functions must always return a value, so if your code has branching statements (such as an if/else construct), all the possible paths must have a return. E.g., if you have a return inside an if block but not after it, the editor will raise an error because if the block is not executed, the function won't have a valid value to return.

Functions are first-class values in terms of the Callable object. Referencing a function by name without calling it will automatically generate the proper callable. This can be used to pass functions as arguments.

Callables must be called with the call() method. You cannot use the () operator directly. This behavior is implemented to avoid performance issues on direct function calls.

Lambda functions allow you to declare functions that do not belong to a class. Instead, a Callable object is created and assigned to a variable directly. This can be useful to create callables to pass around without polluting the class scope.

To call the created lambda you can use the call() method:

Lambda functions can be named for debugging purposes (the name is displayed in the Debugger):

You can specify type hints for lambda functions in the same way as for regular ones:

Note that if you want to return a value from a lambda function, an explicit return is required (you can't omit return):

Lambda functions capture the local environment:

Local variables are captured by value once, when the lambda is created. So they won't be updated in the lambda if reassigned in the outer function:

Also, a lambda cannot reassign an outer local variable. After exiting the lambda, the variable will be unchanged, because the lambda capture implicitly shadows it:

However, if you use pass-by-reference data types (arrays, dictionaries, and objects), then the content changes are shared until you reassign the variable:

A function can be declared static. When a function is static, it has no access to the instance member variables or self. A static function has access to static variables. Also static functions are useful to make libraries of helper functions:

Lambda functions cannot be declared static.

See also Static variables and Static constructor.

A variadic function is a function that can take a variable number of arguments. Since Godot 4.5, GDScript supports variadic functions. To declare a variadic function, you need to use the rest parameter, which collects all the excess arguments into an array.

A function can have at most one rest parameter, which must be the last one in the parameter list. The rest parameter cannot have a default value. Static and lambda functions can also be variadic.

Static typing works for variadic functions too. However, typed arrays are currently not supported as a static type of the rest parameter:

Although you can declare functions as variadic using the rest parameter, unpacking parameters when calling a function using spread syntax that exists in some languages ​​(JavaScript, PHP) is currently not supported in GDScript. However, you can use callv() to call a function with an array of arguments:

See Abstract classes and methods.

Statements are standard and can be assignments, function calls, control flow structures, etc (see below). ; as a statement separator is entirely optional.

Expressions are sequences of operators and their operands in orderly fashion. An expression by itself can be a statement too, though only calls are reasonable to use as statements since other expressions don't have side effects.

Expressions return values that can be assigned to valid targets. Operands to some operator can be another expression. An assignment is not an expression and thus does not return any value.

Here are some examples of expressions:

Identifiers, attributes, and subscripts are valid assignment targets. Other expressions cannot be on the left side of an assignment.

self can be used to refer to the current instance and is often equivalent to directly referring to symbols available in the current script. However, self also allows you to access properties, methods, and other names that are defined dynamically (i.e. are expected to exist in subtypes of the current class, or are provided using _set() and/or _get()).

Beware that accessing members of child classes in the base class is often considered a bad practice, because this blurs the area of responsibility of any given piece of code, making the overall relationship between parts of your game harder to reason about. Besides that, one can simply forget that the parent class had some expectations about it's descendants.

Simple conditions are created by using the if/else/elif syntax. Parenthesis around conditions are allowed, but not required. Given the nature of the tab-based indentation, elif can be used instead of else/if to maintain a level of indentation.

Short statements can be written on the same line as the condition:

Sometimes, you might want to assign a different initial value based on a boolean expression. In this case, ternary-if expressions come in handy:

Ternary-if expressions can be nested to handle more than 2 cases. When nesting ternary-if expressions, it is recommended to wrap the complete expression over multiple lines to preserve readability:

You may also wish to check if a value is contained within something. You can use an if statement combined with the in operator to accomplish this:

Simple loops are created by using while syntax. Loops can be broken using break or continued using continue (which skips to the next iteration of the loop without executing any further code in the current iteration):

To iterate through a range, such as an array or table, a for loop is used. When iterating over an array, the current array element is stored in the loop variable. When iterating over a dictionary, the key is stored in the loop variable.

If you want to assign values on an array as it is being iterated through, it is best to use for i in array.size().

The loop variable is local to the for-loop and assigning to it will not change the value on the array. Objects passed by reference (such as nodes) can still be manipulated by calling methods on the loop variable.

A match statement is used to branch execution of a program. It's the equivalent of the switch statement found in many other languages, but offers some additional features.

match is more type strict than the == operator. For example 1 will not match 1.0. The only exception is String vs StringName matching: for example, the String "hello" is considered equal to the StringName &"hello".

Replace switch with match.

Change default to a single underscore.

The patterns are matched from top to bottom. If a pattern matches, the first corresponding block will be executed. After that, the execution continues below the match statement.

The special continue behavior in match supported in 3.x was removed in Godot 4.0.

The following pattern types are available:

Matches a constant expression, an identifier, or an attribute access (A.B):

This pattern matches everything. It's written as a single underscore.

It can be used as the equivalent of the default in a switch statement in other languages:

A binding pattern introduces a new variable. Like the wildcard pattern, it matches everything - and also gives that value a name. It's especially useful in array and dictionary patterns:

Matches an array. Every single element of the array pattern is a pattern itself, so you can nest them.

The length of the array is tested first, it has to be the same size as the pattern, otherwise the pattern doesn't match.

Open-ended array: An array can be bigger than the pattern by making the last subpattern ...

Every subpattern has to be comma-separated.

Works in the same way as the array pattern. Every key has to be a constant pattern.

The size of the dictionary is tested first, it has to be the same size as the pattern, otherwise the pattern doesn't match.

Open-ended dictionary: A dictionary can be bigger than the pattern by making the last subpattern ...

Every subpattern has to be comma separated.

If you don't specify a value, then only the existence of the key is checked.

A value pattern is separated from the key pattern with a :.

You can also specify multiple patterns separated by a comma. These patterns aren't allowed to have any bindings in them.

A pattern guard is an optional condition that follows the pattern list and allows you to make additional checks before choosing a match branch. Unlike a pattern, a pattern guard can be an arbitrary expression.

Only one branch can be executed per match. Once a branch is chosen, the rest are not checked. If you want to use the same pattern for multiple branches or to prevent choosing a branch with too general pattern, you can specify a pattern guard after the list of patterns with the when keyword:

If there is no matching pattern for the current branch, the pattern guard is not evaluated and the patterns of the next branch are checked.

If a matching pattern is found, the pattern guard is evaluated.

If it's true, then the body of the branch is executed and match ends.

If it's false, then the patterns of the next branch are checked.

By default, all script files are unnamed classes. In this case, you can only reference them using the file's path, using either a relative or an absolute path. For example, if you name a script file character.gd:

You can give your class a name to register it as a new type in Godot's editor. For that, you use the class_name keyword. You can optionally use the @icon annotation with a path to an image, to use it as an icon. Your class will then appear with its new icon in the editor:

SVG images that are used as custom node icons should have the Editor > Scale With Editor Scale and Editor > Convert Icons With Editor Theme import options enabled. This allows icons to follow the editor's scale and theming settings if the icons are designed with the same color palette as Godot's own icons.

Here's a class file example:

If you want to use extends too, you can keep both on the same line:

Named classes are globally registered, which means they become available to use in other scripts without the need to load or preload them:

Godot initializes non-static variables every time you create an instance, and this includes arrays and dictionaries. This is in the spirit of thread safety, since scripts can be initialized in separate threads without the user knowing.

The Godot editor will hide these custom classes with names that begin with the prefix "Editor" in the 'Create New Node' or 'Create New Scene' dialog windows. The classes are available for instantiation at runtime via their class names, but are automatically hidden by the editor windows along with the built-in editor nodes used by the Godot editor.

Since Godot 4.5, you can define abstract classes and methods using the @abstract annotation.

An abstract class is a class that cannot be instantiated directly. Instead, it is meant to be inherited by other classes. Attempting to instantiate an abstract class will result in an error.

An abstract method is a method that has no implementation. Therefore, a newline or a semicolon is expected after the function header. This defines a contract that inheriting classes must conform to, because the method signature must be compatible when overriding.

Inheriting classes must either provide implementations for all abstract methods, or the inheriting class must be marked as abstract. If a class has at least one abstract method (either its own or an unimplemented inherited one), then it must also be marked as abstract. However, the reverse is not true: an abstract class is allowed to have no abstract methods.

If you want to declare a method as optional to be overridden, you should use a non-abstract method and provide a default implementation.

For example, you could have an abstract class called Shape that defines an abstract method called draw(). You can then create subclasses like Circle and Square that implement the draw() method in their own way. This allows you to define a common interface for all shapes without having to implement all the details in the abstract class itself:

Both inner classes and classes created using class_name can be abstract. This example creates two abstract classes, one of which is a subclass of another abstract class:

Since an abstract class cannot be instantiated, it is not possible to attach an abstract class to a node. If you attempt to do so, the engine will print an error when running the scene:

Unnamed classes can also be defined as abstract, the @abstract annotation must precede extends:

A class (stored as a file) can inherit from:

An inner class inside another class file.

Multiple inheritance is not allowed.

Inheritance uses the extends keyword:

If inheritance is not explicitly defined, the class will default to inheriting RefCounted.

To check if a given instance inherits from a given class, the is keyword can be used:

To call a function in a super class (i.e. one extend-ed in your current class), use the super keyword:

This is especially useful because functions in extending classes replace functions with the same name in their super classes. If you still want to call them, you can use super:

If you need to call a different function from the super class, you can specify the function name with the attribute operator:

One of the common misconceptions is trying to override non-virtual engine methods such as get_class(), queue_free(), etc. This is not supported for technical reasons.

In Godot 3, you can shadow engine methods in GDScript, and it will work if you call this method in GDScript. However, the engine will not execute your code if the method is called inside the engine on some event.

In Godot 4, even shadowing may not always work, as GDScript optimizes native method calls. Therefore, we added the NATIVE_METHOD_OVERRIDE warning, which is treated as an error by default. We strongly advise against disabling or ignoring the warning.

Note that this does not apply to virtual methods such as _ready(), _process() and others (marked with the virtual qualifier in the documentation and the names start with an underscore). These methods are specifically for customizing engine behavior and can be overridden in GDScript. Signals and notifications can also be useful for these purposes.

The class constructor, called on class instantiation, is named _init. If you want to call the base class constructor, you can also use the super syntax. Note that every class has an implicit constructor that is always called (defining the default values of class variables). super is used to call the explicit constructor:

This is better explained through examples. Consider this scenario:

There are a few things to keep in mind here:

If the inherited class (state.gd) defines an _init constructor that takes arguments (e in this case), then the inheriting class (idle.gd) must define _init as well and pass appropriate parameters to _init from state.gd.

idle.gd can have a different number of arguments than the base class state.gd.

In the example above, e passed to the state.gd constructor is the same e passed in to idle.gd.

If idle.gd's _init constructor takes 0 arguments, it still needs to pass some value to the state.gd base class, even if it does nothing. This brings us to the fact that you can pass expressions to the base constructor as well, not just variables, e.g.:

A static constructor is a static function _static_init that is called automatically when the class is loaded, after the static variables have been initialized:

A static constructor cannot take arguments and must not return any value.

A class file can contain inner classes. Inner classes are defined using the class keyword. They are instanced using the ClassName.new() function.

Classes stored as files are treated as GDScripts. They must be loaded from disk to access them in other classes. This is done using either the load or preload functions (see below). Instancing of a loaded class resource is done by calling the new function on the class object:

Documentation about exports has been moved to GDScript exported properties.

Sometimes, you want a class' member variable to do more than just hold data and actually perform some validation or computation whenever its value changes. It may also be desired to encapsulate its access in some way.

For this, GDScript provides a special syntax to define properties using the set and get keywords after a variable declaration. Then you can define a code block that will be executed when the variable is accessed or assigned.

Unlike setget in previous Godot versions, set and get methods are always called (except as noted below), even when accessed inside the same class (with or without prefixing with self.). This makes the behavior consistent. If you need direct access to the value, use another variable for direct access and make the property code use that name.

Also there is another notation to use existing class functions if you want to split the code from the variable declaration or you need to reuse the code across multiple properties (but you can't distinguish which property the setter/getter is being called for):

This can also be done in the same line:

The setter and getter must use the same notation, mixing styles for the same variable is not allowed.

You cannot specify type hints for inline setters and getters. This is done on purpose to reduce the boilerplate. If the variable is typed, then the setter's argument is automatically of the same type, and the getter's return value must match it. Separated setter/getter functions can have type hints, and the type must match the variable's type or be a wider type.

When a variable is initialized, the value of the initializer will be written directly to the variable. Including if the @onready annotation is applied to the variable.

Using the variable's name to set it inside its own setter or to get it inside its own getter will directly access the underlying member, so it won't generate infinite recursion and saves you from explicitly declaring another variable:

This also applies to the alternative syntax:

The exception does not propagate to other functions called in the setter/getter. For example, the following code will cause an infinite recursion:

By default, scripts don't run inside the editor and only the exported properties can be changed. In some cases, it is desired that they do run inside the editor (as long as they don't execute game code or manually avoid doing so). For this, the @tool annotation exists and must be placed at the top of the file:

See Running code in the editor for more information.

Be cautious when freeing nodes with queue_free() or free() in a tool script (especially the script's owner itself). As tool scripts run their code in the editor, misusing them may lead to crashing the editor.

Godot implements reference counting to free certain instances that are no longer used, instead of a garbage collector, or requiring purely manual management. Any instance of the RefCounted class (or any class that inherits it, such as Resource) will be freed automatically when no longer in use. For an instance of any class that is not a RefCounted (such as Node or the base Object type), it will remain in memory until it is deleted with free() (or queue_free() for Nodes).

If a Node is deleted via free() or queue_free(), all of its children will also recursively be deleted.

To avoid reference cycles that can't be freed, a WeakRef function is provided for creating weak references, which allow access to the object without preventing a RefCounted from freeing. Here is an example:

Alternatively, when not using references, the is_instance_valid(instance) can be used to check if an object has been freed.

Signals are a tool to emit messages from an object that other objects can react to. To create custom signals for a class, use the signal keyword.

Signals are a Callback mechanism. They also fill the role of Observers, a common programming pattern. For more information, read the Observer tutorial in the Game Programming Patterns ebook.

You can connect these signals to methods the same way you connect built-in signals of nodes like Button or RigidBody3D.

In the example below, we connect the health_depleted signal from a Character node to a Game node. When the Character node emits the signal, the game node's _on_character_health_depleted is called:

You can emit as many arguments as you want along with a signal.

Here is an example where this is useful. Let's say we want a life bar on screen to react to health changes with an animation, but we want to keep the user interface separate from the player in our scene tree.

In our character.gd script, we define a health_changed signal and emit it with Signal.emit(), and from a Game node higher up our scene tree, we connect it to the Lifebar using the Signal.connect() method:

In the Game node, we get both the Character and Lifebar nodes, then connect the character, that emits the signal, to the receiver, the Lifebar node in this case.

This allows the Lifebar to react to health changes without coupling it to the Character node.

You can write optional argument names in parentheses after the signal's definition:

These arguments show up in the editor's node dock, and Godot can use them to generate callback functions for you. However, you can still emit any number of arguments when you emit signals; it's up to you to emit the correct values.

You can also create copies of GDScript Callable objects which accept additional arguments using Callable.bind(). This allows you to add extra information to the connection if the emitted signal itself doesn't give you access to all the data that you need.

When the signal is emitted, the callback method receives the bound values, in addition to those provided by the signal.

Building on the example above, let's say we want to display a log of the damage taken by each character on the screen, like Player1 took 22 damage.. The health_changed signal doesn't give us the name of the character that took damage. So when we connect the signal to the in-game console, we can add the character's name using the bind method:

Our BattleLog node receives each bound element as an extra argument:

The await keyword can be used to create coroutines which wait until a signal is emitted before continuing execution. Using the await keyword with a signal or a call to a function that is also a coroutine will immediately return the control to the caller. When the signal is emitted (or the called coroutine finishes), it will resume execution from the point on where it stopped.

For example, to stop execution until the user presses a button, you can do something like this:

In this case, the wait_confirmation becomes a coroutine, which means that the caller also needs to await it:

Note that requesting a coroutine's return value without await will trigger an error:

However, if you don't depend on the result, you can just call it asynchronously, which won't stop execution and won't make the current function a coroutine:

If you use await with an expression that isn't a signal nor a coroutine, the value will be returned immediately and the function won't give the control back to the caller:

This also means that returning a signal from a function that isn't a coroutine will make the caller await that signal:

Unlike yield in previous Godot versions, you cannot obtain the function state object. This is done to ensure type safety. With this type safety in place, a function cannot say that it returns an int while it actually returns a function state object during runtime.

The assert keyword can be used to check conditions in debug builds. These assertions are ignored in non-debug builds. This means that the expression passed as argument won't be evaluated in a project exported in release mode. Due to this, assertions must not contain expressions that have side effects. Otherwise, the behavior of the script would vary depending on whether the project is run in a debug build.

When running a project from the editor, the project will be paused if an assertion error occurs.

You can optionally pass a custom error message to be shown if the assertion fails:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# Everything after "#" is a comment.
# A file is a class!

# (optional) icon to show in the editor dialogs:
@icon("res://path/to/optional/icon.svg")

# (optional) class definition:
class_name MyClass

# Inheritance:
extends BaseClass


# Member variables.
var a = 5
var s = "Hello"
var arr = [1, 2, 3]
var dict = {"key": "value", 2: 3}
var other_dict = {key = "value", other_key = 2}
var typed_var: int
var inferred_type := "String"

# Constants.
const ANSWER = 42
const THE_NAME = "Charly"

# Enums.
enum {UNIT_NEUTRAL, UNIT_ENEMY, UNIT_ALLY}
enum Named {THING_1, THING_2, ANOTHER_THING = -1}

# Built-in vector types.
var v2 = Vector2(1, 2)
var v3 = Vector3(1, 2, 3)


# Functions.
func some_function(param1, param2, param3):
    const local_const = 5

    if param1 < local_const:
        print(param1)
    elif param2 > 5:
        print(param2)
    else:
        print("Fail!")

    for i in range(20):
        print(i)

    while param2 != 0:
        param2 -= 1

    match param3:
        3:
            print("param3 is 3!")
        _:
            print("param3 is not 3!")

    var local_var = param1 + 3
    return local_var


# Functions override functions with the same name on the base/super class.
# If you still want to call them, use "super":
func something(p1, p2):
    super(p1, p2)


# It's also possible to call another function in the super class:
func other_something(p1, p2):
    super.something(p1, p2)


# Inner class
class Something:
    var a = 10


# Constructor
func _init():
    print("Constructed!")
    var lv = Something.new()
    print(lv.a)
```

Example 2 (unknown):
```unknown
12_345_678  # Equal to 12345678.
3.141_592_7  # Equal to 3.1415927.
0x8080_0000_ffff  # Equal to 0x80800000ffff.
0b11_00_11_00  # Equal to 0b11001100.
```

Example 3 (swift):
```swift
print("\tchar=\"\\t\"")  # Prints `    char="\t"`.
print(r"\tchar=\"\\t\"") # Prints `\tchar=\"\\t\"`.
```

Example 4 (typescript):
```typescript
@export_range(1, 100, 1, "or_greater")
var ranged_var: int = 50
```

---

## GDScript format strings — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_format_string.html

**Contents:**
- GDScript format strings
- Format strings
- Multiple placeholders
- Format specifiers
  - Placeholder types
  - Placeholder modifiers
- Padding
  - Dynamic padding
- Escape sequence
- String format method

Godot offers multiple ways to dynamically change the contents of strings:

Format strings: var string = "I have %s cats." % "3"

The String.format() method: var string = "I have {0} cats.".format([3])

String concatenation: var string = "I have " + str(3) + " cats."

This page explains how to use format strings, and briefly explains the format() method and string concatenation.

Format strings are a way to reuse text templates to succinctly create different but similar strings.

Format strings are just like normal strings, except they contain certain placeholder character sequences such as %s. These placeholders can then be replaced by parameters handed to the format string.

Examine this concrete GDScript example:

Placeholders always start with a %, but the next character or characters, the format specifier, determines how the given value is converted to a string.

The %s seen in the example above is the simplest placeholder and works for most use cases: it converts the value by the same method by which an implicit String conversion or str() would convert it. Strings remain unchanged, booleans turn into either "True" or "False", an int or float becomes a decimal, and other types usually return their data in a human-readable string.

There are other format specifiers.

Format strings may contain multiple placeholders. In such a case, the values are handed in the form of an array, one value per placeholder (unless using a format specifier with *, see dynamic padding):

Note the values are inserted in order. Remember all placeholders must be replaced at once, so there must be an appropriate number of values.

There are format specifiers other than s that can be used in placeholders. They consist of one or more characters. Some of them work by themselves like s, some appear before other characters, some only work with certain values or characters.

One and only one of these must always appear as the last character in a format specifier. Apart from s, these require certain types of parameters.

Simple conversion to String by the same method as implicit String conversion.

A single Unicode character. Accepts a Unicode code point (integer) or a single-character string. Supports values beyond 255.

A decimal integer. Expects an integer or a real number (will be floored).

An octal integer. Expects an integer or a real number (will be floored).

A hexadecimal integer with lower-case letters. Expects an integer or a real number (will be floored).

A hexadecimal integer with upper-case letters. Expects an integer or a real number (will be floored).

A decimal real number. Expects an integer or a real number.

A vector. Expects any float or int-based vector object ( Vector2, Vector3, Vector4, Vector2i, Vector3i or Vector4i). Will display the vector coordinates in parentheses, formatting each coordinate as if it was an %f, and using the same modifiers.

These characters appear before the above. Some of them work only under certain conditions.

In number specifiers, show + sign if positive.

Set padding. Padded with spaces or with zeroes if integer starts with 0 in an integer or real number placeholder. The leading 0 is ignored if - is present. When used after ., see ..

Before f or v, set precision to 0 decimal places. Can be followed up with numbers to change. Padded with zeroes.

Pad to the right rather than the left.

Dynamic padding, expects additional integer parameter to set padding or precision after ., see dynamic padding.

The . (dot), * (asterisk), - (minus sign) and digit (0-9) characters are used for padding. This allows printing several values aligned vertically as if in a column, provided a fixed-width font is used.

To pad a string to a minimum length, add an integer to the specifier:

If the integer starts with 0, integer values are padded with zeroes instead of white space:

Precision can be specified for real numbers by adding a . (dot) with an integer following it. With no integer after ., a precision of 0 is used, rounding to integer values. The integer to use for padding must appear before the dot.

The - character will cause padding to the right rather than the left, useful for right text alignment:

By using the * (asterisk) character, the padding or precision can be set without modifying the format string. It is used in place of an integer in the format specifier. The values for padding and precision are then passed when formatting:

It is still possible to pad with zeroes in integer placeholders by adding 0 before *:

To insert a literal % character into a format string, it must be escaped to avoid reading it as a placeholder. This is done by doubling the character:

There is also another way to format text in GDScript, namely the String.format() method. It replaces all occurrences of a key in the string with the corresponding value. The method can handle arrays or dictionaries for the key/value pairs.

Arrays can be used as key, index, or mixed style (see below examples). Order only matters when the index or mixed style of Array is used.

A quick example in GDScript:

The following are some examples of how to use the various invocations of the String.format() method.

"Hi, {name} v{version}!".format({"name":"Godette", "version":"3.0"})

"Hi, {0} v{1}!".format({"0":"Godette", "1":"3.0"})

"Hi, {0} v{version}!".format({"0":"Godette", "version":"3.0"})

"Hi, {name} v{version}!".format([["version","3.0"], ["name","Godette"]])

"Hi, {0} v{1}!".format(["Godette","3.0"])

"Hi, {name} v{0}!".format(["3.0", ["name","Godette"]])

"Hi, {} v{}!".format(["Godette", "3.0"], "{}")

Placeholders can also be customized when using String.format, here's some examples of that functionality.

"Hi, {0} v{1}".format(["Godette", "3.0"], "{_}")

"Hi, 0% v1%".format(["Godette", "3.0"], "_%")

"Hi, %0 v%1".format(["Godette", "3.0"], "%_")

Combining both the String.format method and the % operator could be useful, as String.format does not have a way to manipulate the representation of numbers.

"Hi, {0} v{version}".format({0:"Godette", "version":"%0.2f" % 3.114})

You can also combine strings by concatenating them together, using the + operator.

When using string concatenation, values that are not strings must be converted using the str() function. There is no way to specify the string format of converted values.

Because of these limitations, format strings or the format() method are often a better choice. In many cases, string concatenation is also less readable.

In Godot's C++ code, GDScript format strings can be accessed using the vformat() helper function in the Variant header.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (julia):
```julia
# Define a format string with placeholder '%s'
var format_string = "We're waiting for %s."

# Using the '%' operator, the placeholder is replaced with the desired value
var actual_string = format_string % "Godot"

print(actual_string)
# Output: "We're waiting for Godot."
```

Example 2 (gdscript):
```gdscript
var format_string = "%s was reluctant to learn %s, but now he enjoys it."
var actual_string = format_string % ["Estragon", "GDScript"]

print(actual_string)
# Output: "Estragon was reluctant to learn GDScript, but now he enjoys it."
```

Example 3 (markdown):
```markdown
print("%10d" % 12345)
# output: "     12345"
# 5 leading spaces for a total length of 10
```

Example 4 (markdown):
```markdown
print("%010d" % 12345)
# output: "0000012345"
```

---

## GD0001: Missing partial modifier on declaration of type that derives from GodotObject — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0001.html

**Contents:**
- GD0001: Missing partial modifier on declaration of type that derives from GodotObject
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A type that derives from GodotObject is not declared partial.

Godot source generators add generated code to user-defined types to implement the integration with the engine. Source generators can't add generated code to types that aren't declared partial.

To fix a violation of this rule, add the partial keyword to the type declaration.

Do not suppress a warning from this rule. Types that derive from GodotObject but aren't partial can't be enhanced by the source generators, resulting in unexpected runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
// The source generators can't enhance this type to work with Godot.
public class InvalidNode : Node { }

// The source generators can enhance this type to work with Godot.
public partial class ValidNode { }
```

---

## GD0002: Missing partial modifier on declaration of type which contains nested classes that derive from GodotObject — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0002.html

**Contents:**
- GD0002: Missing partial modifier on declaration of type which contains nested classes that derive from GodotObject
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A type that derives from GodotObject is contained in a non-partial type declaration.

Godot source generators add generated code to user-defined types to implement the integration with the engine. Source generators can't add generated code to types that aren't declared partial.

To fix a violation of this rule, add the partial keyword to the type declaration.

Do not suppress a warning from this rule. Types that derive from GodotObject but aren't partial can't be enhanced by the source generators, resulting in unexpected runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
public class InvalidParentType
{
    // MyNode is contained in a non-partial type so the source generators
    // can't enhance this type to work with Godot.
    public partial class MyNode : Node { }
}

public partial class ValidParentType
{
    // MyNode is contained in a partial type so the source generators
    // can enhance this type to work with Godot.
    public partial class MyNode : Node { }
}
```

---

## GD0104: The exported property is write-only — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0104.html

**Contents:**
- GD0104: The exported property is write-only
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A write-only property is annotated with the [Export] attribute. Write-only properties can't be exported.

Godot doesn't allow exporting write-only properties.

To fix a violation of this rule, make sure the property declares both a getter and a setter, or remove the [Export] attribute.

Do not suppress a warning from this rule. Write-only members can't be exported so they will be ignored by Godot, resulting in runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
private int _backingField;

// Write-only properties can't be exported.
[Export]
public int InvalidProperty { set => _backingField = value; }

// This property can be exported because it has both a getter and a setter.
[Export]
public int ValidProperty { get; set; }
```

---

## GD0111: The exported tool button must be an expression-bodied property — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0111.html

**Contents:**
- GD0111: The exported tool button must be an expression-bodied property
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A property is annotated with the [ExportToolButton] attribute but it's not an expression-bodied property.

When reloading the .NET assembly, Godot will attempt to serialize exported members to preserve their values. A field or a property with a backing field that stores a Callable may prevent the unloading of the assembly.

An expression-bodied property doesn't have a backing field and won't store the Callable, so Godot won't attempt to serialize it, which should result in the successful reloading of the .NET assembly.

To fix a violation of this rule, replace the property implementation with an expression-bodied property.

Do not suppress a warning from this rule. Callable instances may prevent the .NET assembly from unloading.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
[ExportToolButton("Click me!")]
public Callable ValidClickMeButton => Callable.From(ClickMe);

// Invalid because the Callable will be stored in the property's backing field.
[ExportToolButton("Click me!")]
public Callable InvalidClickMeButton { get; } = Callable.From(ClickMe);
```

---

## GD0110: The exported tool button is not a Callable — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0110.html

**Contents:**
- GD0110: The exported tool button is not a Callable
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

Breaking - If the property's type is changed to Callable

Non-breaking - If the [ExportToolButton] is replaced with [Export]

A property of a type different from Callable is annotated with the [ExportToolButton] attribute.

The [ExportToolButton] attribute is used to create clickable buttons in the inspector so, the property must be a Callable that will be executed when clicking the button.

To fix a violation of this rule, change the type of the property to Callable. Alternatively, if you intended to export a normal property, replace the [ExportToolButton] attribute with [Export].

Do not suppress a warning from this rule. The exported property must be a Callable so it can executed in the editor when clicking the button in the inspector.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GD0108: The exported tool button is not in a tool class — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0108.html

**Contents:**
- GD0108: The exported tool button is not in a tool class
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A property is annotated with the [ExportToolButton] attribute in a class that is not annotated with the [Tool] attribute.

The [ExportToolButton] is used to create clickable buttons in the inspector so, like every other script that runs in the editor, it needs to be annotated with the [Tool] attribute.

To fix a violation of this rule, add the [Tool] attribute to the class that contains the member annotated with the [ExportToolButton] attribute.

Do not suppress a warning from this rule. The clickable buttons in the inspector won't be functional if their script is not annotated with the [Tool] attribute.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
[Tool]
public partial class MyNode : Node
{
    [ExportToolButton("Click me!")]
    public Callable ClickMeButton => Callable.From(ClickMe);

    private static void ClickMe()
    {
        GD.Print("Hello world!");
    }
}
```

---

## GD0107: Types not derived from Node should not export Node members — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0107.html

**Contents:**
- GD0107: Types not derived from Node should not export Node members
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A type that doesn't derive from Node contains an exported field or property of a type that derives from Node.

Exported nodes are serialized as NodePath. Only types derived from Node are able to get the node instance from the NodePath.

To fix a violation of this rule, avoid exporting Node members on a type that doesn't derive from Node, or consider exporting a NodePath.

Do not suppress a warning from this rule. Types that don't derive from Node will be unable to retrieve the right node instance for exported Node members, resulting in unexpected runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GD0201: The name of the delegate must end with 'EventHandler' — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0201.html

**Contents:**
- GD0201: The name of the delegate must end with 'EventHandler'
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A delegate annotated with the [Signal] attribute has a name that doesn't end with 'EventHandler'.

Godot source generators will generate C# events using the name of the delegate with the 'EventHandler' suffix removed. Adding the 'EventHandler' suffix to the name of delegates used in events is a .NET naming convention.

Using a suffix for the delegate allows the generated event to use the name without the suffix avoiding a naming conflict.

Take a look at the C# signals documentation for more information about how to declare and use signals.

To fix a violation of this rule, add 'EventHandler' to the end of the delegate name.

Do not suppress a warning from this rule. Signal delegates without the suffix will be ignored by the source generator, so the signal won't be registered.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
// This delegate is invalid since the name doesn't end with 'EventHandler'.
[Signal]
public void InvalidSignal();

// This delegate is valid since the name ends with 'EventHandler'.
[Signal]
public void ValidSignalEventHandler();
```

---

## GD0106: The exported property is an explicit interface implementation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0106.html

**Contents:**
- GD0106: The exported property is an explicit interface implementation
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

An explicit interface property implementation is annotated with the [Export] attribute. Properties that implement an interface explicitly can't be exported.

Godot doesn't allow exporting explicit interface property implementations. When an interface member is implemented explicitly, the member is hidden and consumers can't access them unless the type is converted to the interface first. Explicitly implemented members can also share the same name of other members in the type, so it could create naming conflicts with other exported members.

To fix a violation of this rule, implement the interface implicitly or remove the [Export] attribute.

Do not suppress a warning from this rule. Explicit interface property implementations can't be exported so they will be ignored by Godot, resulting in runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
public interface MyInterface
{
    public int MyProperty { get; set; }
}

public class MyNode1 : Node, MyInterface
{
    // The property can be exported because it implements the interface implicitly.
    [Export]
    public int MyProperty { get; set; }
}

public class MyNode2 : Node, MyInterface
{
    // The property can't be exported because it implements the interface explicitly.
    [Export]
    int MyInterface.MyProperty { get; set; }
}
```

---

## GD0109: The '[ExportToolButton]' attribute cannot be used with another '[Export]' attribute — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0109.html

**Contents:**
- GD0109: The '[ExportToolButton]' attribute cannot be used with another '[Export]' attribute
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A property is annotated with both the [ExportToolButton] and the [Export] attributes.

The [ExportToolButton] attribute already implies exporting the member, so the [Export] is unnecessary.

To fix a violation of this rule, remove the [Export] attribute.

Do not suppress a warning from this rule. Multiple export attributes may lead to duplicated members, resulting in unexpected runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GD0202: The parameter of the delegate signature of the signal is not supported — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0202.html

**Contents:**
- GD0202: The parameter of the delegate signature of the signal is not supported
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

Breaking - If the parameter type is changed

Non-breaking - If the [Signal] attribute is removed

An unsupported type is specified for a parameter of a delegate annotated with the [Signal] attribute when a Variant-compatible type is expected.

Every signal parameter must be Variant-compatible so it can be marshalled when emitting the signal and invoking the callbacks.

Take a look at the C# signals documentation for more information about how to declare and use signals.

To fix a violation of this rule, change the parameter type to be Variant-compatible or remove the [Signal] attribute from the delegate. Note that removing the attribute will mean the signal is not registered.

If the signal doesn't need to interact with Godot, consider using C# events directly. Pure C# events allow you to use any C# type for its parameters.

Do not suppress a warning from this rule. Signal delegates with parameters that can't be marshalled will result in runtime errors when emitting the signal or invoking the callbacks.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (php):
```php
class SomeType { }

// SomeType is not a valid parameter type because it doesn't derive from GodotObject,
// so it's not compatible with Variant.
public void InvalidSignalEventHandler(SomeType someType);

// System.Int32 is a valid type because it's compatible with Variant.
public void ValidSignalEventHandler(int someInt);
```

---

## GD0303: The parent symbol of a type argument that must be Variant compatible was not handled — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0303.html

**Contents:**
- GD0303: The parent symbol of a type argument that must be Variant compatible was not handled
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

This is a bug in the engine and must be reported.

The MustBeVariantAnalyzer has found an unhandled case in the user source code. Please, open an issue and attach a minimal reproduction project so it can be fixed.

Violations of this rule can't be fixed.

Suppressing a warning from this rule may result in unexpected errors, since the case found by the analyzer may need to be handled by the user to prevent types that are not Variant-compatible from reaching the engine. Attempting to marshal incompatible types will result in runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GD0402: The class must not be generic — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0402.html

**Contents:**
- GD0402: The class must not be generic
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A generic type is annotated with the [GlobalClass] attribute.

The Godot editor assumes every global class is instantiable, but generic types can't be instantiated because the type parameters are unbound.

To fix a violation of this rule, change the type to remove the generic type parameters or remove the [GlobalClass] attribute.

Do not suppress a warning from this rule. Adding the [GlobalClass] to a generic type is an easy mistake to make and this warning helps users realize that it may result in unexpected errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
// This type is a valid global class because it's not generic.
[GlobalClass]
class SomeType : Node { }

// This type is not a valid global class because it's generic.
[GlobalClass]
class SomeGenericType<T> { }
```

---

## GD0302: The generic type parameter must be annotated with the '[MustBeVariant]' attribute — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0302.html

**Contents:**
- GD0302: The generic type parameter must be annotated with the '[MustBeVariant]' attribute
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

A generic type is specified for a generic type argument when a Variant-compatible type is expected, but the specified generic type is not annotated with the [MustBeVariant] attribute.

When a generic type parameter is annotated with the [MustBeVariant] attribute, the generic type is required to be a Variant-compatible type. When the type used is also a generic type, this generic type must be annotated with the [MustBeVariant] attribute as well. For example, the generic Godot.Collections.Array<T> type only supports items of a type that can be converted to Variant, a generic type can be specified if it's properly annotated.

To fix a violation of this rule, add the [MustBeVariant] attribute to the generic type that is used as a generic type argument that must be Variant-compatible.

Do not suppress a warning from this rule. API that contains generic type arguments annotated with the [MustBeVariant] attribute usually has this requirement because the values will be passed to the engine, if the type can't be marshalled it will result in runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
public void Method1<T>()
{
    // T is not valid here because it may not a Variant-compatible type.
    var invalidArray = new Godot.Collections.Array<T>();
}

public void Method2<[MustBeVariant] T>()
{
    // T is guaranteed to be a Variant-compatible type because it's annotated
    // with the [MustBeVariant] attribute, so it can be used here.
    var validArray = new Godot.Collections.Array<T>();
}
```

---

## GD0301: The generic type argument must be a Variant compatible type — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0301.html

**Contents:**
- GD0301: The generic type argument must be a Variant compatible type
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

An unsupported type is specified for a generic type argument when a Variant-compatible type is expected.

When a generic type parameter is annotated with the [MustBeVariant] attribute, the generic type is required to be a Variant-compatible type. For example, the generic Godot.Collections.Array<T> type only supports items of a type that can be converted to Variant.

To fix a violation of this rule, change the generic type argument to be a Variant-compatible type or use a different API that doesn't require the generic type argument to be a Variant-compatible type.

Do not suppress a warning from this rule. API that contains generic type arguments annotated with the [MustBeVariant] attribute usually has this requirement because the values will be passed to the engine, if the type can't be marshalled it will result in runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (php):
```php
class SomeType { }

// SomeType is not a valid type because it doesn't derive from GodotObject,
// so it's not compatible with Variant.
var invalidArray = new Godot.Collections.Array<SomeType>();

// System.Int32 is a valid type because it's compatible with Variant.
var validArray = new Godot.Collections.Array<int>();
```

---

## GD0203: The delegate signature of the signal must return void — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0203.html

**Contents:**
- GD0203: The delegate signature of the signal must return void
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

Breaking - If the return type is changed

Non-breaking - If the [Signal] attribute is removed

A delegate annotated with the [Signal] attribute has a return type when void was expected.

Every signal must return void. There can be multiple callbacks registered for each signal, if signal callbacks could return something it wouldn't be possible to determine which of the returned values to use.

Take a look at the C# signals documentation for more information about how to declare and use signals.

To fix a violation of this rule, change the delegate to return void or remove the [Signal] attribute from the delegate. Note that removing the attribute will mean the signal is not registered.

If the signal doesn't need to interact with Godot, consider using C# events directly. Pure C# events allow you to use any C# type for its parameters.

Do not suppress a warning from this rule. Signal delegates that return something will result in unexpected runtime errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (java):
```java
// This signal delegate is invalid because it doesn't return void.
public int InvalidSignalEventHandler();

// This signal delegate is valid because it returns void.
public void ValidSignalEventHandler();
```

---

## GD0401: The class must derive from Godot.GodotObject or a derived class — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/diagnostics/GD0401.html

**Contents:**
- GD0401: The class must derive from Godot.GodotObject or a derived class
- Cause
- Rule description
- How to fix violations
- When to suppress warnings
- User-contributed notes

Fix is breaking or non-breaking

Breaking - If changing the inheritance chain

Non-breaking - If removing the [GlobalClass] attribute

A type annotated with the [GlobalClass] attribute does not derive from GodotObject.

The [GlobalClass] has no effect for types that don't derive from GodotObject. Every global class must ultimately derive from GodotObject so it can be marshalled.

To fix a violation of this rule, change the type to derive from GodotObject or remove the [GlobalClass] attribute.

Do not suppress a warning from this rule. Adding the [GlobalClass] to a type that doesn't derive from GodotObject is an easy mistake to make and this warning helps users realize that it may result in unexpected errors.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
// This type is not registered as a global class because it doesn't derive from GodotObject.
[GlobalClass]
class SomeType { }

// This type is a global class because it derives from Godot.Node
// which ultimately derives from GodotObject.
[GlobalClass]
class MyNode : Node { }

// This type is a global class because it derives from Godot.Resource
// which ultimately derives from GodotObject.
[GlobalClass]
class MyResource : Resource { }
```

---

## C# API differences to GDScript — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html

**Contents:**
- C# API differences to GDScript
- General differences
- Global scope
  - Constants
  - Math functions
  - Random functions
  - Other functions
  - Tips
  - Full list of equivalences
- @export annotation

This is an (incomplete) list of API differences between C# and GDScript.

As explained in General differences between C# and GDScript, PascalCase is used to access Godot APIs in C# instead of the snake_case used by GDScript and C++. Where possible, fields and getters/setters have been converted to properties. In general, the C# Godot API strives to be as idiomatic as is reasonably possible. See the C# style guide, which we encourage you to also use for your own C# code.

In GDScript, the setters/getters of a property can be called directly, although this is not encouraged. In C#, only the property is defined. For example, to translate the GDScript code x.set_name("Friend") to C#, write x.Name = "Friend";.

A C# IDE will provide intellisense, which is extremely useful when figuring out renamed C# APIs. The built-in Godot script editor has no support for C# intellisense, and it also doesn't provide many other C# development tools that are considered essential. See Configuring an external editor.

Global functions and some constants had to be moved to classes, since C# does not allow declaring them in namespaces. Most global constants were moved to their own enums.

In C#, only primitive types can be constant. For example, the TAU constant is replaced by the Mathf.Tau constant, but the Vector2.RIGHT constant is replaced by the Vector2.Right read-only property. This behaves similarly to a constant, but can't be used in some contexts like switch statements.

Global enum constants were moved to their own enums. For example, ERR_* constants were moved to the Error enum.

Variant.Operator enum

Math global functions, like abs, acos, asin, atan and atan2, are located under Mathf as Abs, Acos, Asin, Atan and Atan2. The PI constant can be found as Mathf.Pi.

C# also provides static System.Math and System.MathF classes that may contain other useful mathematical operations.

Random global functions, like rand_range and rand_seed, are located under GD. Example: GD.RandRange and GD.RandSeed.

Consider using System.Random or, if you need cryptographically strong randomness, System.Security.Cryptography.RandomNumberGenerator.

Many other global functions like print and var_to_str are located under GD. Example: GD.Print and GD.VarToStr.

GodotObject.WeakRef(obj)

GodotObject.InstanceFromId(id)

is_instance_id_valid(id)

GodotObject.IsInstanceIdValid(id)

is_instance_valid(obj)

GodotObject.IsInstanceValid(obj)

Sometimes it can be useful to use the using static directive. This directive allows to access the members and nested types of a class without specifying the class name.

List of Godot's global scope functions and their equivalent in C#:

Mathf.AngleDifference

Mathf.BezierDerivative

Mathf.BezierInterpolate

bytes_to_var_with_objects

GD.BytesToVarWithObjects

Mathf.CubicInterpolate

cubic_interpolate_angle

Mathf.CubicInterpolateAngle

cubic_interpolate_angle_in_time

Mathf.CubicInterpolateInTime

cubic_interpolate_in_time

Mathf.CubicInterpolateAngleInTime

GodotObject.InstanceFromId

Mathf.IsFinite or float.IsFinite or double.IsFinite

Mathf.IsInf or float.IsInfinity or double.IsInfinity

GodotObject.IsInstanceIdValid

GodotObject.IsInstanceValid

Mathf.IsNaN or float.IsNaN or double.IsNaN

operator == or object.ReferenceEquals

Use OS.IsStdoutVerbose and GD.Print

Use $ string interpolation

Variant.As<T> or GD.Convert

Variant.Type.ToString

var_to_bytes_with_objects

GD.VarToBytesWithObjects

List of GDScript utility functions and their equivalent in C#:

System.Diagnostics.Debug.Assert

Use explicit conversion: (char)65

System.Environment.StackTrace

GD.Print(System.Environment.StackTrace)

GD.Range or System.Linq.Enumerable.Range

ClassDB.ClassExists(type)

preload, as it works in GDScript, is not available in C#. Use GD.Load or ResourceLoader.Load instead.

Use the [Export] attribute instead of the GDScript @export annotation. This attribute can also be provided with optional PropertyHint and hintString parameters. Default values can be set by assigning a value.

See also: C# exported properties.

Use the [Signal] attribute to declare a signal instead of the GDScript signal keyword. This attribute should be used on a delegate, whose name signature will be used to define the signal. The delegate must have the EventHandler suffix, an event will be generated in the class with the same name but without the suffix, use that event's name with EmitSignal.

See also: C# signals.

GDScript has the ability to defer the initialization of a member variable until the ready function is called with @onready (cf. @onready annotation). For example:

However C# does not have this ability. To achieve the same effect you need to do this.

Singletons are available as static classes rather than using the singleton pattern. This is to make code less verbose than it would be with an Instance property.

However, in some very rare cases this is not enough. For example, you may want to access a member from the base class GodotObject, like Connect. For such use cases we provide a static property named Singleton that returns the singleton instance. The type of this instance is GodotObject.

If you are developing main screen plugins, it is essential to note that EditorInterface is not a static class in C#, unlike in GDScript. Therefore, you must use the singleton pattern to obtain an instance of the EditorInterface:

EditorInterface.Singleton

Use System.String (string). Most of Godot's String methods have an equivalent in System.String or are provided by the StringExtensions class as extension methods.

Note that C# strings use UTF-16 encoding, while Godot Strings use UTF-32 encoding.

Strings are immutable in .NET, so all methods that manipulate a string don't modify the original string and return a newly created string with the modifications applied. To avoid creating multiple string allocations consider using a StringBuilder.

List of Godot's String methods and their equivalent in C#:

StringExtensions.Bigrams

StringExtensions.BinToInt

StringExtensions.CEscape

StringExtensions.CUnescape

StringExtensions.Capitalize

StringExtensions.CasecmpTo or StringExtensions.CompareTo (Consider using string.Equals or string.Compare)

StringExtensions.Count (Consider using RegEx)

StringExtensions.CountN (Consider using RegEx)

StringExtensions.Dedent

string.Remove (Consider using StringBuilder to manipulate strings)

StringExtensions.Find (Consider using string.IndexOf or string.IndexOfAny)

StringExtensions.FindN (Consider using string.IndexOf or string.IndexOfAny)

Use $ string interpolation

StringExtensions.GetBaseDir

StringExtensions.GetBaseName

StringExtensions.GetExtension

StringExtensions.GetFile

StringExtensions.Hash (Consider using object.GetHashCode unless you need to guarantee the same behavior as in GDScript)

StringExtensions.HexDecode (Consider using System.Convert.FromHexString)

StringExtensions.HexToInt (Consider using int.Parse or long.Parse with System.Globalization.NumberStyles.HexNumber)

StringExtensions.Indent

string.Insert (Consider using StringBuilder to manipulate strings)

StringExtensions.IsAbsolutePath

string.IsNullOrEmpty or string.IsNullOrWhiteSpace

StringExtensions.IsRelativePath

StringExtensions.IsSubsequenceOf

StringExtensions.IsSubsequenceOfN

StringExtensions.IsValidFileName

StringExtensions.IsValidFloat (Consider using float.TryParse or double.TryParse)

StringExtensions.IsValidHexNumber

StringExtensions.IsValidHtmlColor

StringExtensions.IsValidIdentifier

StringExtensions.IsValidInt (Consider using int.TryParse or long.TryParse)

StringExtensions.IsValidIPAddress

StringExtensions.JSONEscape

StringExtensions.Left (Consider using string.Substring or string.AsSpan)

StringExtensions.Match (Consider using RegEx)

StringExtensions.MatchN (Consider using RegEx)

StringExtensions.Md5Buffer (Consider using System.Security.Cryptography.MD5.HashData)

StringExtensions.Md5Text (Consider using System.Security.Cryptography.MD5.HashData with StringExtensions.HexEncode)

N/A (Consider using string.Equals or string.Compare)

StringExtensions.NocasecmpTo or StringExtensions.CompareTo (Consider using string.Equals or string.Compare)

float.ToString or double.ToString

int.ToString or long.ToString

float.ToString or double.ToString

uint.ToString or ulong.ToString

StringExtensions.PadDecimals

StringExtensions.PadZeros

StringExtensions.PathJoin

Use string constructor or a StringBuilder

string.Replace or RegEx

StringExtensions.ReplaceN (Consider using string.Replace or RegEx)

StringExtensions.RFind (Consider using string.LastIndexOf or string.LastIndexOfAny)

StringExtensions.RFindN (Consider using string.LastIndexOf or string.LastIndexOfAny)

StringExtensions.Right (Consider using string.Substring or string.AsSpan)

StringExtensions.Sha1Buffer (Consider using System.Security.Cryptography.SHA1.HashData)

StringExtensions.Sha1Text (Consider using System.Security.Cryptography.SHA1.HashData with StringExtensions.HexEncode)

StringExtensions.Sha256Buffer (Consider using System.Security.Cryptography.SHA256.HashData)

StringExtensions.Sha256Text (Consider using System.Security.Cryptography.SHA256.HashData with StringExtensions.HexEncode)

StringExtensions.Similarity

StringExtensions.SimplifyPath

StringExtensions.Split (Consider using string.Split)

StringExtensions.SplitFloat

StringExtensions.StripEdges (Consider using string.Trim, string.TrimStart or string.TrimEnd)

StringExtensions.StripEscapes

StringExtensions.Substr (Consider using string.Substring or string.AsSpan)

StringExtensions.ToAsciiBuffer (Consider using System.Text.Encoding.ASCII.GetBytes)

StringExtensions.ToCamelCase

StringExtensions.ToFloat (Consider using float.TryParse or double.TryParse)

StringExtensions.ToInt (Consider using int.TryParse or long.TryParse)

StringExtensions.ToPascalCase

StringExtensions.ToSnakeCase

StringExtensions.ToUtf16Buffer (Consider using System.Text.Encoding.UTF16.GetBytes)

StringExtensions.ToUtf32Buffer (Consider using System.Text.Encoding.UTF32.GetBytes)

StringExtensions.ToUtf8Buffer (Consider using System.Text.Encoding.UTF8.GetBytes)

StringExtensions.ToUtf16Buffer in Windows and StringExtensions.ToUtf32Buffer in other platforms

StringExtensions.TrimPrefix

StringExtensions.TrimSuffix

StringExtensions.URIDecode (Consider using System.Uri.UnescapeDataString)

StringExtensions.URIEncode (Consider using System.Uri.EscapeDataString)

StringExtensions.ValidateNodeName

StringExtensions.XMLEscape

StringExtensions.XMLUnescape

List of Godot's PackedByteArray methods that create a String and their C# equivalent:

get_string_from_ascii

StringExtensions.GetStringFromAscii (Consider using System.Text.Encoding.ASCII.GetString)

get_string_from_utf16

StringExtensions.GetStringFromUtf16 (Consider using System.Text.Encoding.UTF16.GetString)

get_string_from_utf32

StringExtensions.GetStringFromUtf32 (Consider using System.Text.Encoding.UTF32.GetString)

StringExtensions.GetStringFromUtf8 (Consider using System.Text.Encoding.UTF8.GetString)

StringExtensions.HexEncode (Consider using System.Convert.ToHexString)

.NET provides path utility methods under the System.IO.Path class. They can only be used with native OS paths, not Godot paths (paths that start with res:// or user://). See File paths in Godot projects.

The following method was converted to a property with a different name:

The following methods were converted to properties with their respective names changed:

The Signal type implements the awaitable pattern which means it can be used with the await keyword. See await keyword.

Instead of using the Signal type, the recommended way to use Godot signals in C# is to use the generated C# events. See C# signals.

The following methods were converted to properties with their respective names changed:

Currently C# supports Callable if one of the following holds:

Callable was created using the C# Callable type.

Callable is a basic version of the engine's Callable. Custom Callables are unsupported. A Callable is custom when any of the following holds:

Callable has bound information (Callables created with bind/unbind are unsupported).

Callable was created from other languages through the GDExtension API.

Some methods such as bind and unbind are not implemented, use lambdas instead:

The lambda captures the name variable so it can be bound to the SayHello method.

This type is named Rid in C# to follow the .NET naming convention.

The following methods were converted to properties with their respective names changed:

Structs cannot have parameterless constructors in C#. Therefore, new Basis() initializes all primitive members to their default value. Use Basis.Identity for the equivalent of Basis() in GDScript and C++.

The following method was converted to a property with a different name:

Structs cannot have parameterless constructors in C#. Therefore, new Transform2D() initializes all primitive members to their default value. Please use Transform2D.Identity for the equivalent of Transform2D() in GDScript and C++.

The following methods were converted to properties with their respective names changed:

Structs cannot have parameterless constructors in C#. Therefore, new Transform3D() initializes all primitive members to their default value. Please use Transform3D.Identity for the equivalent of Transform3D() in GDScript and C++.

The following methods were converted to properties with their respective names changed:

The following field was converted to a property with a slightly different name:

The following method was converted to a property with a different name:

This type is named Rect2I in C# to follow the .NET naming convention.

The following field was converted to a property with a slightly different name:

The following method was converted to a property with a different name:

This type is named Aabb in C# to follow the .NET naming convention.

The following method was converted to a property with a different name:

Structs cannot have parameterless constructors in C#. Therefore, new Quaternion() initializes all primitive members to their default value. Please use Quaternion.Identity for the equivalent of Quaternion() in GDScript and C++.

Structs cannot have parameterless constructors in C#. Therefore, new Projection() initializes all primitive members to their default value. Please use Projection.Identity for the equivalent of Projection() in GDScript and C++.

Structs cannot have parameterless constructors in C#. Therefore, new Color() initializes all primitive members to their default value (which represents the transparent black color). Please use Colors.Black for the equivalent of Color() in GDScript and C++.

The global Color8 method to construct a Color from bytes is available as a static method in the Color type.

The Color constants are available in the Colors static class as readonly properties.

The following method was converted to a property with a different name:

The following method was converted to a method with a different name:

FromHtml(ReadOnlySpan<char>)

The following methods are available as constructors:

The equivalent of packed arrays are System.Array.

See also PackedArray in C#.

Use Godot.Collections.Array for an untyped Variant array. Godot.Collections.Array<T> is a type-safe wrapper around Godot.Collections.Array.

See also Array in C#.

Use Godot.Collections.Dictionary for an untyped Variant dictionary. Godot.Collections.Dictionary<TKey, TValue> is a type-safe wrapper around Godot.Collections.Dictionary.

See also Dictionary in C#.

Godot.Variant is used to represent Godot's native Variant type. Any Variant-compatible type can be converted from/to it.

See also: C# Variant.

This is explained extensively in Cross-language scripting.

Something similar to GDScript's await keyword can be achieved with C#'s await keyword.

The await keyword in C# can be used with any awaitable expression. It's commonly used with operands of the types Task, Task<TResult>, ValueTask, or ValueTask<TResult>.

An expression t is awaitable if one of the following holds:

t is of compile-time type dynamic.

t has an accessible instance or extension method called GetAwaiter with no parameters and no type parameters, and a return type A for which all of the following hold:

A implements the interface System.Runtime.CompilerServices.INotifyCompletion.

A has an accessible, readable instance property IsCompleted of type bool.

A has an accessible instance method GetResult with no parameters and no type parameters.

An equivalent of awaiting a signal in GDScript can be achieved with the await keyword and GodotObject.ToSignal.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
using static Godot.GD;

public class Test
{
    static Test()
    {
        Print("Hello"); // Instead of GD.Print("Hello");
    }
}
```

Example 2 (json):
```json
using Godot;

public partial class MyNode : Node
{
    [Export]
    private NodePath _nodePath;

    [Export]
    private string _name = "default";

    [Export(PropertyHint.Range, "0,100000,1000,or_greater")]
    private int _income;

    [Export(PropertyHint.File, "*.png,*.jpg")]
    private string _icon;
}
```

Example 3 (json):
```json
[Signal]
delegate void MySignalEventHandler(string willSendAString);
```

Example 4 (swift):
```swift
@onready var my_label = get_node("MyLabel")
```

---

## C# collections — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_collections.html

**Contents:**
- C# collections
- Choose a collection
- Godot collections
  - PackedArray
  - Array
  - Dictionary
- User-contributed notes

The .NET base class library contains multiple collection types that can be used to store and manipulate data. Godot also provide some collection types that are tightly integrated with the rest of the engine.

The main difference between the .NET collections and the Godot collections is that the .NET collections are implemented in C# while the Godot collections are implemented in C++ and the Godot C# API is a wrapper over it, this is an important distinction since it means every operation on a Godot collection requires marshaling which can be expensive especially inside a loop.

Due to the performance implications, using Godot collections is only recommended when absolutely necessary (such as interacting with the Godot API). Godot only understands its own collection types, so it's required to use them when talking to the engine.

If you have a collection of elements that don't need to be passed to a Godot API, using a .NET collection would be more performant.

It's also possible to convert between .NET collections and Godot collections. The Godot collections contain constructors from generic .NET collection interfaces that copy their elements, and the Godot collections can be used with the LINQ ToList, ToArray and ToDictionary methods. But keep in mind this conversion requires marshaling every element in the collection and copies it to a new collection so it can be expensive.

Despite this, the Godot collections are optimized to try and avoid unnecessary marshaling, so methods like Sort or Reverse are implemented with a single interop call and don't need to marshal every element. Keep an eye out for generic APIs that take collection interfaces like LINQ because every method requires iterating the collection and, therefore, marshaling every element. Prefer using the instance methods of the Godot collections when possible.

To choose which collection type to use for each situation, consider the following questions:

Does your collection need to interact with the Godot engine? (e.g.: the type of an exported property, calling a Godot method).

If yes, since Godot only supports Variant-compatible types, use a Godot collection.

If not, consider choosing an appropriate .NET collection.

Do you need a Godot collection that represents a list or sequential set of data?

Godot arrays are similar to the C# collection List<T>.

Godot packed arrays are more memory-efficient arrays, in C# use one of the supported System.Array types.

Do you need a Godot collection that maps a set of keys to a set of values?

Godot dictionaries store pairs of keys and values and allow easy access to the values by their associated key.

Godot packed arrays are implemented as an array of a specific type, allowing it to be more tightly packed as each element has the size of the specific type, not Variant.

In C#, packed arrays are replaced by System.Array:

Other C# arrays are not supported by the Godot C# API since a packed array equivalent does not exist. See the list of Variant-compatible types.

Godot arrays are implemented as an array of Variant and can contain several elements of any type. In C#, the equivalent type is Godot.Collections.Array.

The generic Godot.Collections.Array<T> type allows restricting the element type to a Variant-compatible type.

An untyped Godot.Collections.Array can be converted to a typed array using the Godot.Collections.Array<T>(Godot.Collections.Array) constructor.

Despite the name, Godot arrays are more similar to the C# collection List<T> than System.Array. Their size is not fixed and can grow or shrink as elements are added/removed from the collection.

List of Godot's Array methods and their equivalent in C#:

System.Linq.Enumerable.All

System.Linq.Enumerable.Any

Array[^1] or System.Linq.Enumerable.Last or System.Linq.Enumerable.LastOrDefault

System.Linq.Enumerable.Count

Use System.Linq.Enumerable.Where

Array[0] or System.Linq.Enumerable.First or System.Linq.Enumerable.FirstOrDefault

System.Linq.Enumerable.Select

PickRandom (Consider using System.Random)

Array[i] with RemoveAt(i)

Array[^1] with RemoveAt(Count - 1)

Array[0] with RemoveAt(0)

System.Linq.Enumerable.Aggregate

System.Linq.Enumerable.OrderBy

Godot dictionaries are implemented as a dictionary with Variant keys and values. In C#, the equivalent type is Godot.Collections.Dictionary.

The generic Godot.Collections.Dictionary<TKey, TValue> type allows restricting the key and value types to a Variant-compatible type.

An untyped Godot.Collections.Dictionary can be converted to a typed dictionary using the Godot.Collections.Dictionary<TKey, TValue>(Godot.Collections.Dictionary) constructor.

If you need a dictionary where the key is typed but not the value, use Variant as the TValue generic parameter of the typed dictionary.

List of Godot's Dictionary methods and their equivalent in C#:

Dictionary[Variant] indexer or TryGetValue

Dictionary[Variant] indexer, Add or TryGetValue

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
// The keys must be string, but the values can be any Variant-compatible type.
var dictionary = new Godot.Collections.Dictionary<string, Variant>();
```

---

## C# exported properties — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_exports.html

**Contents:**
- C# exported properties
- Basic use
- Grouping exports
- Strings as paths
- Limiting editor input ranges
- Floats with easing hint
- Export with suffix hint
- Colors
- Nodes
- Resources

In Godot, class members can be exported. This means their value gets saved along with the resource (such as the scene) they're attached to. They will also be available for editing in the property editor. Exporting is done by using the [Export] attribute.

In that example the value 5 will be saved, and after building the current project it will be visible in the property editor.

One of the fundamental benefits of exporting member variables is to have them visible and editable in the editor. This way, artists and game designers can modify values that later influence how the program runs. For this, a special export syntax is provided.

Exporting can only be done with Variant-compatible types.

Exporting properties can also be done in GDScript, for information on that see GDScript exported properties.

Exporting works with fields and properties. They can have any access modifier.

Exported members can specify a default value; otherwise, the default value of the type is used instead.

An int like Number defaults to 0. Text defaults to null because string is a reference type.

Default values can be specified for fields and properties.

Properties with a backing field use the default value of the backing field.

A property's get is not actually executed to determine the default value. Instead, Godot analyzes the C# source code. This works fine for most cases, such as the examples on this page. However, some properties are too complex for the analyzer to understand.

For example, the following property attempts to use math to display the default value as 5 in the property editor, but it doesn't work:

The analyzer doesn't understand this code and falls back to the default value for int, 0. However, when running the scene or inspecting a node with an attached tool script, _number will be 2, and NumberWithBackingField will return 5. This difference may cause confusing behavior. To avoid this, don't use complex properties. Alternatively, if the default value can be explicitly specified, it can be overridden with the _PropertyCanRevert() and _PropertyGetRevert() methods.

Any type of Resource or Node can be exported. The property editor shows a user-friendly assignment dialog for these types. This can be used instead of GD.Load and GetNode. See Nodes and Resources.

It is possible to group your exported properties inside the Inspector with the [ExportGroup] attribute. Every exported property after this attribute will be added to the group. Start a new group or use [ExportGroup("")] to break out.

The second argument of the attribute can be used to only group properties with the specified prefix.

Groups cannot be nested, use [ExportSubgroup] to create subgroups within a group.

You can also change the name of your main category, or create additional categories in the property list with the [ExportCategory] attribute.

The list of properties is organized based on the class inheritance, and new categories break that expectation. Use them carefully, especially when creating projects for public use.

Property hints can be used to export strings as paths

String as a path to a file.

String as a path to a directory.

String as a path to a file, custom filter provided as hint.

Using paths in the global filesystem is also possible, but only in scripts in tool mode.

String as a path to a PNG file in the global filesystem.

String as a path to a directory in the global filesystem.

The multiline annotation tells the editor to show a large input field for editing over multiple lines.

Using the range property hint allows you to limit what can be input as a value using the editor.

Allow integer values from 0 to 20.

Allow integer values from -10 to 20.

Allow floats from -10 to 20 and snap the value to multiples of 0.2.

If you add the hints "or_greater" and/or "or_less" you can go above or below the limits when adjusting the value by typing it instead of using the slider.

Display a visual representation of the ease function when editing.

Display a unit hint suffix for exported variables. Works with numeric types, such as floats or vectors:

In the above example, \u00b2 is used to write the "squared" character (²).

Regular color given as red-green-blue-alpha value.

Color given as red-green-blue value (alpha will always be 1).

Since Godot 4.0, nodes can be directly exported without having to use NodePaths.

A specific type of node can also be directly exported. The list of nodes shown after pressing "Assign" in the inspector is filtered to the specified type, and only a correct node can be assigned.

Custom node classes can also be exported directly. The filtering behavior depends on whether the custom class is a global class.

Exporting NodePaths like in Godot 3.x is still possible, in case you need it:

In the Inspector, you can then drag and drop a resource file from the FileSystem dock into the variable slot.

Opening the inspector dropdown may result in an extremely long list of possible classes to create, however. Therefore, if you specify a type derived from Resource such as:

The drop-down menu will be limited to AnimationNode and all its derived classes. Custom resource classes can also be used, see C# global classes.

It must be noted that even if the script is not being run while in the editor, the exported properties are still editable. This can be used in conjunction with a script in "tool" mode.

Members whose type is an enum with the [Flags] attribute can be exported and their values are limited to the members of the enum type. The editor will create a widget in the Inspector, allowing to select none, one, or multiple of the enum members. The value will be stored as an integer.

A flags enum uses powers of 2 for the values of the enum members. Members that combine multiple flags using logical OR (|) are also possible.

Integers used as bit flags can store multiple true/false (boolean) values in one property. By using the Flags property hint, any of the given flags can be set from the editor.

You must provide a string description for each flag. In this example, Fire has value 1, Water has value 2, Earth has value 4 and Wind corresponds to value 8. Usually, constants should be defined accordingly (e.g. private const int ElementWind = 8 and so on).

You can add explicit values using a colon:

Only power of 2 values are valid as bit flags options. The lowest allowed value is 1, as 0 means that nothing is selected. You can also add options that are a combination of other flags:

Export annotations are also provided for the physics and render layers defined in the project settings.

Using bit flags requires some understanding of bitwise operations. If in doubt, use boolean variables instead.

Members whose type is an enum can be exported and their values are limited to the members of the enum type. The editor will create a widget in the Inspector, enumerating the following as "Thing 1", "Thing 2", "Another Thing". The value will be stored as an integer.

Integer and string members can also be limited to a specific list of values using the [Export] annotation with the PropertyHint.Enum hint. The editor will create a widget in the Inspector, enumerating the following as Warrior, Magician, Thief. The value will be stored as an integer, corresponding to the index of the selected option (i.e. 0, 1, or 2).

You can add explicit values using a colon:

If the type is string, the value will be stored as a string.

If you want to set an initial value, you must specify it explicitly:

If you want to create a clickable button in the inspector, you can use the [ExportToolButton] attribute. This exports a Callable property or field as a clickable button. Since this runs in the editor, usage of the [Tool] attribute is required. When the button is pressed, the callable is called:

You can also set an icon for the button with a second argument. If specified, an icon will be fetched via GetThemeIcon(), from the "EditorIcons" theme type.

As explained in the C# Variant documentation, only certain C# arrays and the collection types defined in the Godot.Collections namespace are Variant-compatible, therefore, only those types can be exported.

Using the generic Godot.Collections.Array<T> allows specifying the type of the array elements, which will be used as a hint for the editor. The Inspector will restrict the elements to the specified type.

The default value of Godot arrays is null. A different default can be specified:

Arrays with specified types which inherit from resource can be set by drag-and-dropping multiple files from the FileSystem dock.

Using the generic Godot.Collections.Dictionary<TKey, TValue> allows specifying the types of the key and value elements of the dictionary.

The default value of Godot dictionaries is null. A different default can be specified:

C# arrays can exported as long as the element type is a Variant-compatible type.

The default value of C# arrays is null. A different default can be specified:

When changing an exported variable's value from a script in Tool mode, the value in the inspector won't be updated automatically. To update it, call NotifyPropertyListChanged() after setting the exported variable's value.

Not every type of export can be provided on the level of the language itself to avoid unnecessary design complexity. The following describes some more or less common exporting features which can be implemented with a low-level API.

Before reading further, you should get familiar with the way properties are handled and how they can be customized with _Set(), _Get(), and _GetPropertyList() methods as described in Accessing data or logic from an object.

For binding properties using the above methods in C++, see Binding properties using _set/_get/_get_property_list.

The script must operate in the tool mode so the above methods can work from within the editor.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
using Godot;

public partial class ExportExample : Node3D
{
    [Export]
    public int Number { get; set; } = 5;
}
```

Example 2 (csharp):
```csharp
[Export]
private int _number;

[Export]
public int Number { get; set; }
```

Example 3 (csharp):
```csharp
[Export]
public int Number { get; set; }

[Export]
public string Text { get; set; }
```

Example 4 (csharp):
```csharp
[Export]
private string _greeting = "Hello World";

[Export]
public string Greeting { get; set; } = "Hello World";
```

---

## About godot-cpp — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/about_godot_cpp.html

**Contents:**
- About godot-cpp
- Differences between godot-cpp and C++ modules
  - Advantages of godot-cpp
  - Advantages of C++ modules
- Version compatibility
- User-contributed notes

godot-cpp are the official C++ GDExtension bindings, maintained as part of the Godot project.

godot-cpp is built with the GDExtension system, which allows access to Godot in almost the same way as modules: A lot of engine code can be used in your godot-cpp project almost exactly as it is.

In particular, godot-cpp has access to all functions that GDScript and C# have, and additional access to a few more for fast low-level access of data, or deeper integration with Godot.

You can use both godot-cpp and C++ modules to run C or C++ code in a Godot project.

They also both allow you to integrate third-party libraries into Godot. The one you should choose depends on your needs.

Unlike modules, godot-cpp (and GDExtensions, in general) don't require compiling the engine's source code, making it easier to distribute your work. It gives you access to most of the API available to GDScript and C#, allowing you to code game logic with full control regarding performance. It's ideal if you need high-performance code you'd like to distribute as an add-on in the asset library.

You can use the same compiled godot-cpp library in the editor and exported project. With C++ modules, you have to recompile all the export templates you plan to use if you require its functionality at runtime.

godot-cpp only requires you to compile your library, not the whole engine. That's unlike C++ modules, which are statically compiled into the engine. Every time you change a module, you need to recompile the engine. Even with incremental builds, this process is slower than using godot-cpp.

We recommend C++ modules in cases where godot-cpp (or another GDExtension system) isn't enough:

C++ modules provide deeper integration into the engine. GDExtension's access is not as deep as static modules.

You can use C++ modules to provide additional features in a project without carrying native library files around. This extends to exported projects.

If you notice that specific systems are not accessible via godot-cpp but are via custom modules, feel free to open an issue on the godot-cpp repository to discuss implementation options for exposing the missing functionality.

GDExtensions targeting an earlier version of Godot should work in later minor versions, but not vice-versa. For example, a GDExtension targeting Godot 4.2 should work just fine in Godot 4.3, but one targeting Godot 4.3 won't work in Godot 4.2.

For this reason, when creating GDExtensions, you may want to target the lowest version of Godot that has the features you need, not the most recent version of Godot. This can save you from needing to create multiple builds for different versions of Godot.

There is one exception to this: extensions targeting Godot 4.0 will not work with Godot 4.1 and later (see Updating your GDExtension for 4.1).

GDExtensions are also only compatible with engine builds that use the same level of floating-point precision the extension was compiled for. This means that if you use an engine build with double-precision floats, the extension must also be compiled for double-precision floats and use an extension_api.json file generated by your custom engine build. See Large world coordinates for details.

Generally speaking, if you build a custom version of Godot, you should generate an extension_api.json from it for your GDExtensions, because it may have some differences from official Godot builds.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Adding documentation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/gdextension_docs_system.html

**Contents:**
- Adding documentation
- Documentation styling
- Publishing documentation online
- User-contributed notes

Adding documentation for GDExtensions is only possible for Godot 4.3 and later. The support can be integrated into your project regardless because the snippet will check if you use the appropriate godot-cpp version. If you set the compatibility_minimum to 4.2 and you load a project with the extension through a 4.2 editor, the documentation page for that class will be empty. The extension itself will still work.

The GDExtension documentation system works in a similar manner to the built-in engine documentation. It uses a series of XML files (one per class) to document the exposed constructors, properties, methods, constants, signals, and theme items of each class.

We are assuming you are using the project files explained in the example project with the following structure:

Inside the Godot demo project directory of your GDExtension directory, run the following terminal command:

This command calls upon the Godot editor binary to generate documentation via the --doctool and --gdextension-docs commands. The ../ addition is to let Godot know where the GDExtension SConstruct file is located. By calling this command, Godot generates a doc_classes directory inside the project directory in which it generates XML files for the GDExtension classes. Those files can then be edited to add information about member variables, methods, signals, and more.

To add the now edited documentation to the GDExtension and let the editor load it, you need to add the following lines to your SConstruct file:

The if-statement checks if we are compiling the GDExtension library with the editor and template_debug flags. SCons then tries to load all the XML files inside the doc_classes directory and appends them to the sources variable which already includes all the source files of your extension. If it fails it means we are currently trying to compile the library when the godot_cpp is set to a version before 4.3.

After loading the extension in a 4.3 Godot editor or later and open the documentation of your extension class either by Ctrl + Click in the script editor or the Editor help dialog you will see something like this:

To style specific parts of text you can use BBCode tags similarly to how they can be used in RichTextLabels. You can set text as bold, italic, underlined, colored, codeblocks etc. by embedding them in tags like this:

Currently, the supported tags for the GDExtension documentation system are:

[center]{text}[/center]

[color={code/name}]{text}[/color]

You may want to publish an online reference for your GDExtension, similar to this website. The most important step is to build reStructuredText (.rst) files from your XML class reference:

Your .rst files will now be available in docs/classes/. From here, you can use any documentation builder that supports reStructuredText syntax to create a website from them.

godot-docs uses Sphinx. You can use the repository as a basis to build your own documentation system. The following guide describes the basic steps, but they are not exhaustive: You will need a bit of personal insight to make it work.

Add godot-docs as a submodule to your docs/ folder.

Copy over its conf.py, index.rst, .readthedocs.yaml files into /docs/. You may later decide to copy over and edit more of godot-docs' files, like _templates/layout.html.

Modify these files according to your project. This mostly involves adjusting paths to point to the godot-docs subfolder, as well as strings to reflect it's your project rather than Godot you're building the docs for.

Create an account on readthedocs.org. Import your project, and modify its base .readthedocs.yaml file path to /docs/.readthedocs.yaml.

Once you have completed all these steps, your documentation should be available at <repo-name>.readthedocs.io.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
gdextension_cpp_example/  # GDExtension directory
|
+--demo/                  # game example/demo to test the extension
|   |
|   +--main.tscn
|   |
|   +--bin/
|       |
|       +--gdexample.gdextension
|
+--godot-cpp/             # C++ bindings
|
+--src/                   # source code of the extension we are building
|   |
|   +--register_types.cpp
|   +--register_types.h
|   +--gdexample.cpp
|   +--gdexample.h
```

Example 2 (markdown):
```markdown
# Replace "godot" with the full path to a Godot editor binary
# if Godot is not installed in your `PATH`.
godot --doctool ../ --gdextension-docs
```

Example 3 (typescript):
```typescript
if env["target"] in ["editor", "template_debug"]:
    try:
        doc_data = env.GodotCPPDocData("src/gen/doc_data.gen.cpp", source=Glob("doc_classes/*.xml"))
        sources.append(doc_data)
    except AttributeError:
        print("Not including class reference as we're targeting a pre-4.3 baseline.")
```

Example 4 (json):
```json
[b]this text will be shown as bold[/b]
```

---

## C# Variant — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_variant.html

**Contents:**
- C# Variant
- Variant-compatible types
- Using Variant in a generic context
- User-contributed notes

For a detailed explanation of Variant in general, see the Variant documentation page.

Godot.Variant is used to represent Godot's native Variant type. Any Variant-compatible type can be converted from/to it. We recommend avoiding Godot.Variant unless it is necessary to interact with untyped engine APIs. Take advantage of C#'s type safety when possible.

Converting from a Variant-compatible C# type to Godot.Variant can be done using implicit conversions. There are also CreateFrom method overloads and the generic Variant.From<T> methods. Only the syntax is different: the behavior is the same.

Implicit conversions to Godot.Variant make passing variants as method arguments very convenient. For example, the third argument of tween_property specifying the final color of the tween is a Godot.Variant.

Converting from Godot.Variant to a C# type can be done using explicit conversions. There are also Variant.As{TYPE} methods and the generic Variant.As<T> method. All of these behave the same.

The Variant.As{TYPE} methods are typically named after C# types (Int32), not C# keywords (int).

If the Variant type doesn't match the conversion target type, the consequences vary depending on the source and target values.

The conversion may examine the value and return a similar but potentially unexpected value of the target type. For example, the string "42a" may be converted to the integer 42.

The default value of the target type may be returned.

An empty array may be returned.

An exception may be thrown.

Converting to the correct type avoids complicated behavior and should be preferred.

The Variant.Obj property returns a C# object with the correct value for any variant. This may be useful when the type of Variant is completely unknown. However, when possible, prefer more specific conversions. Variant.Obj evaluates a switch on Variant.VariantType and it may not be necessary. Also, if the result is a value type, it is boxed.

For example, if the potential for Variant.As<MyNode>() to throw an invalid cast exception isn't acceptable, consider using a Variant.As<GodotObject>() is MyNode n type pattern instead.

Since the Variant type in C# is a struct, it can't be null. To create a "null" Variant, use the default keyword or the Godot.Variant parameterless constructor.

A Variant-compatible type can be converted to and from a Godot.Variant. These C# types are Variant-compatible:

All the built-in value types, except decimal, nint and nuint.

Classes derived from GodotObject.

Collections types defined in the Godot.Collections namespace.

Full list of Variant types and their equivalent C# type:

long (Godot stores 64-bit integers in Variant)

double (Godot stores 64-bit floats in Variant)

Godot.GodotObject or any derived type.

Godot.Collections.Dictionary

Godot.Collections.Array

Godot uses 64-bit integers and floats in Variant. Smaller integer and float types such as int, short and float are supported since they can fit in the bigger type. Be aware that when a conversion is performed, using the wrong type will result in potential precision loss.

Enums are supported by Godot.Variant since their underlying type is an integer type which are all compatible. However, implicit conversions don't exist, enums must be manually converted to their underlying integer type before they can converted to/from Godot.Variant or use the generic Variant.As<T> and Variant.From<T> methods to convert them.

When using generics, you may be interested in restricting the generic T type to be only one of the Variant-compatible types. This can be achieved using the [MustBeVariant] attribute.

Combined with the generic Variant.From<T> allows you to obtain an instance of Godot.Variant from an instance of a generic T type. Then it can be used in any API that only supports the Godot.Variant struct.

In order to invoke a method with a generic parameter annotated with the [MustBeVariant] attribute, the value must be a Variant-compatible type or a generic T type annotated with the [MustBeVariant] attribute as well.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
int x = 42;
Variant numberVariant = x;
Variant helloVariant = "Hello, World!";

Variant numberVariant2 = Variant.CreateFrom(x);
Variant numberVariant3 = Variant.From(x);
```

Example 2 (unknown):
```unknown
Tween tween = CreateTween();
tween.TweenProperty(GetNode("Sprite"), "modulate", Colors.Red, 1.0f);
```

Example 3 (csharp):
```csharp
int number = (int)numberVariant;
string hello = (string)helloVariant;

int number2 = numberVariant.As<int>();
int number3 = numberVariant.AsInt32();
```

Example 4 (typescript):
```typescript
enum MyEnum { A, B, C }

Variant variant1 = (int)MyEnum.A;
MyEnum enum1 = (MyEnum)(int)variant1;

Variant variant2 = Variant.From(MyEnum.A);
MyEnum enum2 = variant2.As<MyEnum>();
```

---

## C# global classes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_global_classes.html

**Contents:**
- C# global classes
- User-contributed notes

Global classes (also known as named scripts) are types registered in Godot's editor so they can be used more conveniently. In GDScript, this is achieved using the class_name keyword at the top of a script. This page describes how to achieve the same effect in C#.

Global classes show up in the Add Node and Create Resource dialogs.

If an exported property is a global class, the inspector restricts assignment, allowing only instances of that global class or any derived classes.

Global classes are registered with the [GlobalClass] attribute.

The file name must match the class name in case-sensitive fashion. For example, a global class named "MyNode" must have a file name of MyNode.cs, not myNode.cs.

The MyNode type will be registered as a global class with the same name as the type's name.

The Select a Node window for the MyNode exported property filters the list of nodes in the scene to match the assignment restriction.

If a custom type isn't registered as a global class, the assignment is restricted to the Godot type the custom type is based on. For example, inspector assignments to an export of the type MySimpleSprite2D are restricted to Sprite2D and derived types.

When combined with the [GlobalClass] attribute, the [Icon] attribute allows providing a path to an icon to show when the class is displayed in the editor.

The Stats class is a custom resource registered as a global class. Exporting properties of the type Stats will only allow instances of this resource type to be assigned, and the inspector will let you create and load instances of this type easily.

The Godot editor will hide these custom classes with names that begin with the prefix "Editor" in the "Create New Node" or "Create New Scene" dialog windows. The classes are available for instantiation at runtime via their class names, but are automatically hidden by the editor windows along with the built-in editor nodes used by the Godot editor.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
using Godot;

[GlobalClass]
public partial class MyNode : Node
{
}
```

Example 2 (json):
```json
public partial class Main : Node
{
    [Export]
    public MyNode MyNode { get; set; }
}
```

Example 3 (swift):
```swift
public partial class MySimpleSprite2D : Sprite2D
{
}
```

Example 4 (json):
```json
using Godot;

[GlobalClass, Icon("res://Stats/StatsIcon.svg")]
public partial class Stats : Resource
{
    [Export]
    public int Strength { get; set; }

    [Export]
    public int Defense { get; set; }

    [Export]
    public int Speed { get; set; }
}
```

---

## C++ (godot-cpp) — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/index.html

**Contents:**
- C++ (godot-cpp)

This section documents godot-cpp, the official C++ GDExtension bindings maintained as part of the Godot project.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## C# signals — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_signals.html

**Contents:**
- C# signals
- Signals as C# events
- Custom signals as C# events
- Signal emission
- Bound values
- Signal creation at runtime
- Using Connect and Disconnect
- Disconnecting automatically when the receiver is freed
  - No automatic disconnection: a lambda expression that captures a variable
  - No automatic disconnection: a custom signal

For a detailed explanation of signals in general, see the Using signals section in the step by step tutorial.

Signals are implemented using C# events, the idiomatic way to represent the observer pattern in C#. This is the recommended way to use signals in C# and the focus of this page.

In some cases it's necessary to use the older Connect() and Disconnect() APIs. See Using Connect and Disconnect for more details.

If you encounter a System.ObjectDisposedException while handling a signal, you might be missing a signal disconnection. See Disconnecting automatically when the receiver is freed for more details.

To provide more type-safety, Godot signals are also all available through events. You can handle these events, as any other event, with the += and -= operators.

In addition, you can always access signal names associated with a node type through its nested SignalName class. This is useful when, for example, you want to await on a signal (see await keyword).

To declare a custom event in your C# script, use the [Signal] attribute on a public delegate type. Note that the name of this delegate needs to end with EventHandler.

Once this is done, Godot will create the appropriate events automatically behind the scenes. You can then use said events as you'd do for any other Godot signal. Note that events are named using your delegate's name minus the final EventHandler part.

If you want to connect to these signals in the editor, you will need to (re)build the project to see them appear.

You can click the Build button in the upper-right corner of the editor to do so.

To emit signals, use the EmitSignal method. Note that, as for signals defined by the engine, your custom signal names are listed under the nested SignalName class.

In contrast with other C# events, you cannot use Invoke to raise events tied to Godot signals.

Signals support arguments of any Variant-compatible type.

Consequently, any Node or RefCounted will be compatible automatically, but custom data objects will need to inherit from GodotObject or one of its subclasses.

Sometimes you'll want to bind values to a signal when the connection is established, rather than (or in addition to) when the signal is emitted. To do so, you can use an anonymous function like in the following example.

Here, the Button.Pressed signal does not take any argument. But we want to use the same ModifyValue for both the "plus" and "minus" buttons. So we bind the modifier value at the time we're connecting the signals.

Finally, you can create custom signals directly while your game is running. Use the AddUserSignal method for that. Be aware that it should be executed before any use of said signals (either connecting to them or emitting them). Also, note that signals created this way won't be visible through the SignalName nested class.

In general, it isn't recommended to use Connect() and Disconnect(). These APIs don't provide as much type safety as the events. However, they're necessary for connecting to signals defined by GDScript and passing ConnectFlags.

In the following example, pressing the button for the first time prints Greetings!. OneShot disconnects the signal, so pressing the button again does nothing.

Normally, when any GodotObject is freed (such as any Node), Godot automatically disconnects all connections associated with that object. This happens for both signal emitters and signal receivers.

For example, a node with this code will print "Hello!" when the button is pressed, then free itself. Freeing the node disconnects the signal, so pressing the button again doesn't do anything:

When a signal receiver is freed while the signal emitter is still alive, in some cases automatic disconnection won't happen:

The signal is connected to a lambda expression that captures a variable.

The signal is a custom signal.

The following sections explain these cases in more detail and include suggestions for how to disconnect manually.

Automatic disconnection is totally reliable if a signal emitter is freed before any of its receivers are freed. With a project style that prefers this pattern, the above limits may not be a concern.

If you connect to a lambda expression that captures variables, Godot can't tell that the lambda is associated with the instance that created it. This causes this example to have potentially unexpected behavior:

On tick 4, the lambda expression tries to access the Name property of the node, but the node has already been freed. This causes the exception.

To disconnect, keep a reference to the delegate created by the lambda expression and pass that to -=. For example, this node connects and disconnects using the _EnterTree and _ExitTree lifecycle methods:

In this example, Free causes the node to leave the tree, which calls _ExitTree. _ExitTree disconnects the signal, so _tick is never called again.

The lifecycle methods to use depend on what the node does. Another option is to connect to signals in _Ready and disconnect in Dispose.

Godot uses Delegate.Target to determine what instance a delegate is associated with. When a lambda expression doesn't capture a variable, the generated delegate's Target is the instance that created the delegate. When a variable is captured, the Target instead points at a generated type that stores the captured variable. This is what breaks the association. If you want to see if a delegate will be automatically cleaned up, try checking its Target.

Callable.From doesn't affect the Delegate.Target, so connecting a lambda that captures variables using Connect doesn't work any better than +=.

Connecting to a custom signal using += doesn't disconnect automatically when the receiving node is freed.

To disconnect, use -= at an appropriate time. For example:

Another solution is to use Connect, which does disconnect automatically with custom signals:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
Timer myTimer = GetNode<Timer>("Timer");
myTimer.Timeout += () => GD.Print("Timeout!");
```

Example 2 (swift):
```swift
await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
```

Example 3 (json):
```json
[Signal]
public delegate void MySignalEventHandler();

[Signal]
public delegate void MySignalWithArgumentEventHandler(string myString);
```

Example 4 (gdscript):
```gdscript
public override void _Ready()
{
    MySignal += () => GD.Print("Hello!");
    MySignalWithArgument += SayHelloTo;
}

private void SayHelloTo(string name)
{
    GD.Print($"Hello {name}!");
}
```

---

## Getting started — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/gdextension_cpp_example.html

**Contents:**
- Getting started
- Workflow overview
- Example project
- Setting up the project
- Building the C++ bindings
- Creating a simple plugin
- Compiling the plugin
- Using the GDExtension module
- Adding properties
- Signals

As a GDExtension, godot-cpp is more complicated to use than GDScript and C#. If you decide to work with it, here's what to expect your workflow to look like:

Create a new godot-cpp project (from the template, or from scratch, as explained below).

Develop your code with your favorite IDE locally.

Build and test your code with the earliest compatible Godot version.

Create builds for all platforms you want to support (e.g. using GitHub Actions).

Optional: Publish on the Godot Asset Library.

For your first godot-cpp project, we recommend starting with this guide to understand the technology involved with godot-cpp. After you're done, you can use the godot-cpp template, which has better coverage of features, such as a GitHub action pipeline and useful SConstruct boilerplate code. However, the template does not explain itself to a high level of detail, which is why we recommend going through this guide first.

There are a few prerequisites you'll need:

A Godot 4 executable.

SCons as a build tool.

A copy of the godot-cpp repository.

See also Configuring an IDE and Compiling as the build tools are identical to the ones you need to compile Godot from source.

You can download the godot-cpp repository from GitHub or let Git do the work for you. Note that this repository has different branches for different versions of Godot. GDExtensions will not work in older versions of Godot (only Godot 4 and up) and vice versa, so make sure you download the correct branch.

To use GDExtension you need to use the godot-cpp branch that matches the version of Godot that you are targeting. For example, if you're targeting Godot 4.1, use the 4.1 branch. Throughout this tutorial we use 4.x, which will need to be replaced with the version of Godot you are targeting.

The master branch is the development branch which is updated regularly to work with Godot's master branch.

GDExtensions targeting an earlier version of Godot should work in later minor versions, but not vice-versa. For example, a GDExtension targeting Godot 4.2 should work just fine in Godot 4.3, but one targeting Godot 4.3 won't work in Godot 4.2.

There is one exception to this: extensions targeting Godot 4.0 will not work with Godot 4.1 and later (see Updating your GDExtension for 4.1).

If you are versioning your project using Git, it is recommended to add it as a Git submodule:

Alternatively, you can also clone it to the project folder:

If you decide to download the repository or clone it into your folder, make sure to keep the folder layout the same as we've setup here. Much of the code we'll be showcasing here assumes the project has this layout.

If you cloned the example from the link specified in the introduction, the submodules are not automatically initialized. You will need to execute the following commands:

This will initialize the repository in your project folder.

Now that we've downloaded our prerequisites, it is time to build the C++ bindings.

The repository contains a copy of the metadata for the current Godot release, but if you need to build these bindings for a newer version of Godot, call the Godot executable:

The resulting extension_api.json file will be created in the executable's directory. Copy it to the project folder and add custom_api_file=<PATH_TO_FILE> to the scons command below.

To generate and compile the bindings, use this command (replacing <platform> with windows, linux or macos depending on your OS):

The build process automatically detects the number of CPU threads to use for parallel builds. To specify a number of CPU threads to use, add -jN at the end of the SCons command line where N is the number of CPU threads to use.

This step will take a while. When it is completed, you should have static libraries that can be compiled into your project stored in godot-cpp/bin/.

You may need to add bits=64 to the command on Windows or Linux.

Now it's time to build an actual plugin. We'll start by creating an empty Godot project in which we'll place a few files.

Open Godot and create a new project. For this example, we will place it in a folder called demo inside our GDExtension's folder structure.

In our demo project, we'll create a scene containing a Node called "Main" and we'll save it as main.tscn. We'll come back to that later.

Back in the top-level GDExtension module folder, we're also going to create a subfolder called src in which we'll place our source files.

You should now have demo, godot-cpp, and src directories in your GDExtension module.

Your folder structure should now look like this:

In the src folder, we'll start with creating our header file for the GDExtension node we'll be creating. We will name it gdexample.h:

There are a few things of note to the above. We include sprite2d.hpp which contains bindings to the Sprite2D class. We'll be extending this class in our module.

We're using the namespace godot, since everything in GDExtension is defined within this namespace.

Then we have our class definition, which inherits from our Sprite2D through a container class. We'll see a few side effects of this later on. The GDCLASS macro sets up a few internal things for us.

After that, we declare a single member variable called time_passed.

In the next block we're defining our methods, we have our constructor and destructor defined, but there are two other functions that will likely look familiar to some, and one new method.

The first is _bind_methods, which is a static function that Godot will call to find out which methods can be called and which properties it exposes. The second is our _process function, which will work exactly the same as the _process function you're used to in GDScript.

Let's implement our functions by creating our gdexample.cpp file:

This one should be straightforward. We're implementing each method of our class that we defined in our header file.

Note our _process function, which keeps track of how much time has passed and calculates a new position for our sprite using a sine and cosine function.

There is one more C++ file we need; we'll name it register_types.cpp. Our GDExtension plugin can contain multiple classes, each with their own header and source file like we've implemented GDExample up above. What we need now is a small bit of code that tells Godot about all the classes in our GDExtension plugin.

The initialize_example_module and uninitialize_example_module functions get called respectively when Godot loads our plugin and when it unloads it. All we're doing here is parse through the functions in our bindings module to initialize them, but you might have to set up more things depending on your needs. We call the GDREGISTER_RUNTIME_CLASS macro for each of our classes in our library. This will make them run only in game, like the default for GDScript.

The important function is the third function called example_library_init. We first call a function in our bindings library that creates an initialization object. This object registers the initialization and termination functions of the GDExtension. Furthermore, it sets the level of initialization (core, servers, scene, editor, level).

At last, we need the header file for the register_types.cpp named register_types.h.

To compile the project we need to define how SCons using should compile it using an SConstruct file which references the one in godot-cpp. Writing it from scratch is outside the scope of this tutorial, but you can the SConstruct file we prepared. We'll cover a more customizable, detailed example on how to use these build files in a subsequent tutorial.

This SConstruct file was written to be used with the latest godot-cpp master, you may need to make small changes using it with older versions or refer to the SConstruct file in the Godot 4.x documentation.

Once you've downloaded the SConstruct file, place it in your GDExtension folder structure alongside godot-cpp, src and demo, then run:

You should now be able to find the module in demo/bin/<platform>.

When building for iOS, package the module as a static .xcframework, you can use following commands to do so:

Here, we've compiled both godot-cpp and our gdexample library as debug builds. For optimized builds, you should compile them using the target=template_release switch.

Before we jump back into Godot, we need to create one more file in demo/bin/.

This file lets Godot know what dynamic libraries should be loaded for each platform and the entry function for the module. It is called gdexample.gdextension.

This file contains a configuration section that controls the entry function of the module. You should also set the minimum compatible Godot version with compatibility_minimum, which prevents older version of Godot from trying to load your extension. The reloadable flag enables automatic reloading of your extension by the editor every time you recompile it, without needing to restart the editor. This only works if you compile your extension in debug mode (default).

The libraries section is the important bit: it tells Godot the location of the dynamic library in the project's filesystem for each supported platform. It will also result in just that file being exported when you export the project, which means the data pack won't contain libraries that are incompatible with the target platform.

Finally, the dependencies section allows you to name additional dynamic libraries that should be included as well. This is important when your GDExtension plugin implements someone else's library and requires you to supply a third-party dynamic library with your project.

Here is another overview to check the correct file structure:

Time to jump back into Godot. We load up the main scene we created way back in the beginning and now add a newly available GDExample node to the scene:

We're going to assign the Godot logo to this node as our texture, disable the centered property:

We're finally ready to run the project:

GDScript allows you to add properties to your script using the export keyword. In GDExtension you have to register the properties with a getter and setter function or directly implement the _get_property_list, _get and _set methods of an object (but that goes far beyond the scope of this tutorial).

Lets add a property that allows us to control the amplitude of our wave.

In our gdexample.h file we need to add a member variable and getter and setter functions:

In our gdexample.cpp file we need to make a number of changes, we will only show the methods we end up changing, don't remove the lines we're omitting:

Once you compile the module with these changes in place, you will see that a property has been added to our interface. You can now change this property and when you run your project, you will see that our Godot icon travels along a larger figure.

Let's do the same but for the speed of our animation and use a setter and getter function. Our gdexample.h header file again only needs a few more lines of code:

This requires a few more changes to our gdexample.cpp file, again we're only showing the methods that have changed so don't remove anything we're omitting:

Now when the project is compiled, we'll see another property called speed. Changing its value will make the animation go faster or slower. Furthermore, we added a property range which describes in which range the value can be. The first two arguments are the minimum and maximum value and the third is the step size.

For simplicity, we've only used the hint_range of the property method. There are a lot more options to choose from. These can be used to further configure how properties are displayed and set on the Godot side.

Last but not least, signals fully work in GDExtension as well. Having your extension react to a signal given out by another object requires you to call connect on that object. We can't think of a good example for our wobbling Godot icon, we would need to showcase a far more complete example.

This is the required syntax:

To connect our signal the_signal from some other node with our method my_method, we need to provide the connect method with the name of the signal and a Callable. The Callable holds information about an object on which a method can be called. In our case, it associates our current object instance this with the method my_method of the object. Then the connect method will add this to the observers of the_signal. Whenever the_signal is now emitted, Godot knows which method of which object it needs to call.

Note that you can only call my_method if you've previously registered it in your _bind_methods method. Otherwise Godot will not know about the existence of my_method.

To learn more about Callable, check out the class reference here: Callable.

Having your object sending out signals is more common. For our wobbling Godot icon, we'll do something silly just to show how it works. We're going to emit a signal every time a second has passed and pass the new location along.

In our gdexample.h header file, we need to define a new member time_emit:

This time, the changes in gdexample.cpp are more elaborate. First, you'll need to set time_emit = 0.0; in either our _init method or in our constructor. We'll look at the other 2 needed changes one by one.

In our _bind_methods method, we need to declare our signal. This is done as follows:

Here, our ADD_SIGNAL macro can be a single call with a MethodInfo argument. MethodInfo's first parameter will be the signal's name, and its remaining parameters are PropertyInfo types which describe the essentials of each of the method's parameters. PropertyInfo parameters are defined with the data type of the parameter, and then the name that the parameter will have by default.

So here, we add a signal, with a MethodInfo which names the signal "position_changed". The PropertyInfo parameters describe two essential arguments, one of type Object, the other of type Vector2, respectively named "node" and "new_pos".

Next, we'll need to change our _process method:

After a second has passed, we emit our signal and reset our counter. We can add our parameter values directly to emit_signal.

Once the GDExtension library is compiled, we can go into Godot and select our sprite node. In the Node dock, we can find our new signal and link it up by pressing the Connect button or double-clicking the signal. We've added a script on our main node and implemented our signal like this:

Every second, we output our position to the console.

We hope the above example showed you the basics. You can build upon this example to create full-fledged scripts to control nodes in Godot using C++!

Instead of basing your project off the above example setup, we recommend to restart now by cloning the godot-cpp template, and base your project off of that. It has better coverage of features, such as a GitHub build action and additional useful SConstruct boilerplate.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
mkdir gdextension_cpp_example
cd gdextension_cpp_example
git init
git submodule add -b 4.x https://github.com/godotengine/godot-cpp
cd godot-cpp
git submodule update --init
```

Example 2 (unknown):
```unknown
mkdir gdextension_cpp_example
cd gdextension_cpp_example
git clone -b 4.x https://github.com/godotengine/godot-cpp
```

Example 3 (sql):
```sql
cd gdextension_cpp_example
git submodule update --init
```

Example 4 (unknown):
```unknown
godot --dump-extension-api
```

---

## The GDExtension system — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/index.html

**Contents:**
- The GDExtension system

GDExtension is a Godot-specific technology that lets the engine interact with native shared libraries at runtime. You can use it to run native code without compiling it with the engine.

GDExtension is not a scripting language and has no relation to GDScript.

This section describes how GDExtension works, and is generally aimed at people wanting to make a GDExtension from scratch, for example to create language bindings. If you want to use existing language bindings, please refer to other articles instead, such as the articles about C++ (godot-cpp) or one of the community-made ones.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## What is GDExtension? — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/what_is_gdextension.html

**Contents:**
- What is GDExtension?
- Version compatibility
- User-contributed notes

GDExtension is a Godot-specific technology that lets the engine interact with native shared libraries at runtime. You can use it to run native code without compiling it with the engine.

There are three primary methods with which this is achieved:

gdextension_interface.h: A set of C functions that Godot and a GDExtension can use to communicate.

extension_api.json: A list of C functions that are exposed from Godot APIs (Core Features).

*.gdextension: A file format read by Godot to load a GDExtension.

Most people create GDExtensions with some existing language binding, such as godot-cpp (for C++), or one of the community-made ones.

See godot-cpp Version Compatibility, which applies to all GDExtensions.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## The .gdextension file — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/gdextension_file.html

**Contents:**
- The .gdextension file
- Introduction
- Configuration section
- Libraries section
  - Running system
  - Build
  - Architecture
- Icons section
- Dependencies section
- User-contributed notes

The .gdextension file in your project contains the instructions for how to load the GDExtension. The instructions are separated into specific sections. This page should give you a quick overview of the different options available to you. For an introduction how to get started with C++ (godot-cpp), take a look at the GDExtension C++ Example.

Name of the entry function for initializing the GDExtension. This function should be defined in the register_types.cpp file when using godot-cpp. Adding this is necessary for the extension to work.

compatibility_minimum

Minimum compatible version. This prevents older versions of Godot from loading extensions that depend on features from newer versions of Godot. Only supported in Godot 4.1 or later

compatibility_maximum

Maximum compatible version. This prevents newer versions of Godot from loading the extension. Only supported in Godot 4.3 or later

Reloads the extension upon recompilation. Reloading is supported for the godot-cpp binding in Godot 4.2 or later. Other language bindings may or may not support it as well. This flag should be mainly used for developing or debugging an extension.

The GDExtension is part of a v2 Android plugin. During export this flag will indicate to the editor that the GDExtension native shared libraries are exported by the Android plugin AAR binaries.

In this section you can set the paths to the compiled binaries of your GDExtension libraries. By specifying feature flags you can filter which version should be loaded and exported with your game depending on which feature flags are active. Every feature flag must match to Godot's feature flags or your custom export flags to be loaded in an exported game. For instance macos.debug means that it will be loaded if Godot has both the macos and debug flag active. Each line of the section is evaluated from top to bottom.

Here is an example of what that can look like:

Entries are matched in order, so if two sets of feature tags could match the same system, be sure to put the more specific ones first:

Here are lists of some of the available built-in options (for more look at the feature tags):

Windows operating system

Linux operating system

Linux or BSD operating system

Android operating system

Build with debug symbols

Optimized build without debug symbols

double-precision build

single-precision build

RISC-V build (any bitness)

32-bit WebAssembly build

By default, Godot uses the Node icon in the scene dock for GDExtension nodes. A custom icon can be set by reference to its name and resource path of an SVG file.

The path should point to a 16 by 16 pixel SVG image. Read the guide for creating icons for more information.

In this section you set the paths of the GDExtension dependencies. This is used internally to export the dependencies when exporting your game executable. You are able to set which dependency is loaded depending on the feature flags of the exported executable. In addition, you are able to set an optional subdirectory to move your dependencies into. If no path is supplied Godot will move the libraries into the same directory as your game executable.

In MacOS it is necessary to have shared libraries inside a folder called Frameworks with a directory structure like this: Game.app/Contents/Frameworks.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
[libraries]

macos.debug = "res://bin/libgdexample.macos.template_debug.framework"
macos.release = "res://bin/libgdexample.macos.template_release.framework"
windows.debug.x86_32 = "res://bin/libgdexample.windows.template_debug.x86_32.dll"
windows.release.x86_32 = "res://bin/libgdexample.windows.template_release.x86_32.dll"
windows.debug.x86_64 = "res://bin/libgdexample.windows.template_debug.x86_64.dll"
windows.release.x86_64 = "res://bin/libgdexample.windows.template_release.x86_64.dll"
linux.debug.x86_64 = "res://bin/libgdexample.linux.template_debug.x86_64.so"
linux.release.x86_64 = "res://bin/libgdexample.linux.template_release.x86_64.so"
linux.debug.arm64 = "res://bin/libgdexample.linux.template_debug.arm64.so"
linux.release.arm64 = "res://bin/libgdexample.linux.template_release.arm64.so"
linux.debug.rv64 = "res://bin/libgdexample.linux.template_debug.rv64.so"
linux.release.rv64 = "res://bin/libgdexample.linux.template_release.rv64.so"
```

Example 2 (json):
```json
[libraries]

linux.release.editor.x86_64 = "res://bin/libgdexample.linux.template_release.x86_64.so"
linux.release.x86_64 = "res://bin/libgdexample.linux.noeditor.template_release.x86_64.so"
```

Example 3 (json):
```json
[icons]

GDExample = "res://icons/gd_example.svg"
```

Example 4 (json):
```json
[dependencies]

macos.debug = {
    "res://bin/libdependency.macos.template_debug.framework" : "Contents/Frameworks"
}
macos.release = {
    "res://bin/libdependency.macos.template_release.framework" : "Contents/Frameworks"
}
windows.debug = {
    "res://bin/libdependency.windows.template_debug.x86_64.dll" : "",
    "res://bin/libdependency.windows.template_debug.x86_32.dll" : ""
}
windows.release = {
    "res://bin/libdependency.windows.template_release.x86_64.dll" : "",
    "res://bin/libdependency.windows.template_release.x86_32.dll" : ""
}
linux.debug = {
    "res://bin/libdependency.linux.template_debug.x86_64.so" : "",
    "res://bin/libdependency.linux.template_debug.arm64.so" : "",
    "res://bin/libdependency.linux.template_debug.rv64.so" : ""
}
linux.release = {
    "res://bin/libdependency.linux.template_release.x86_64.so" : "",
    "res://bin/libdependency.linux.template_release.arm64.so" : "",
    "res://bin/libdependency.linux.template_release.rv64.so" : ""
}
```

---

## How to read the Godot API — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/how_to_read_the_godot_api.html

**Contents:**
- How to read the Godot API
- Inheritance
- Brief Description
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Constants

On this page, you'll learn how to read the class reference for the Godot API.

The API, or Application Programming Interface, is an index of what Godot offers users. It provides a brief summary of which classes exist, how they are related to each other, what features they have, and how to use them.

At the top of each file, you will see the name of the class.

The "Inherits" section lists each class the current one inherits. Here CanvasItem inherits Node and Node inherits Object.

The "Inherited By" section lists each class which directly inherits the current class. Here Control and Node2D both inherit CanvasItem.

Next a brief description of the class. This text appears in Godot Editor popups for creating Nodes, Resources, and other types.

Next a more detailed description the class, its features, and its use case(s).

Things you may find here:

Specifics of how the class works.

Code samples of common use cases.

Usage details which are shared between each of the class's methods.

Warnings about required dependencies or configuration.

Links to other related parts of the Godot API.

The page then provides links to parts of the manual which mention or make use of the current class.

The Properties table lists the variables which belong to each instance of the class, also known as the "properties."

The left column contains the data type of the property. The text is also a link to that data type's Godot API page.

The center column contains the name of the property. The text is also a link to that property's full description on the page. Use this name to get the property's data or set a new value to it.

The right column contains the default value of the property. To initialize it with a different value, you must set a different value via script or the Inspector.

The Methods table lists the functions which belong to each instance of the class, also known as the "methods."

The left column contains the data type of the method's return value.

The right column contains the name, parameters, and qualifiers of the method. The name is the text before the opening parenthesis. It is also a link to the method's full description on the page. Use this name to call the method.

For each parameter, the page details its data type, name, and default value, if any.

Possible qualifiers include...

const: the method does not change any data in the class instance.

virtual: the method does nothing but wait for a script to override it.

vararg: the method can accept an arbitrary number of arguments.

The Signals list details the names and parameters of events which "signal" a change in game state to other class instances.

Like the Methods table, any parameters will include their data type and name.

Each signal also has a detailed explanation of when the signal is emitted.

The Enumerations list details the enumerable data types associated with the current class.

For each enumeration, the page states its name and then lists its possible values.

For each enumeration value, the page states its name, its integer value, and an explanation of its use case(s) and/or affects.

The Constants list details named integer constants in the current class.

For each constant, the page states its name, its integer value, and an explanation of its use case(s) and/or affects.

NOTIFICATION_* constants' descriptions will state which engine event triggers the notification.

The Property Descriptions list details everything about each property.

It restates the data type and name of the property.

Every property in the Godot API is bound to a pair of setter and getter functions. Using either is equivalent. They are listed here.

Below that is a detailed summary of what the property's data represents, its use case(s) and/or the affects of changing it. It may include code samples and/or links to relevant parts of the Godot API.

Knowing the setter and getter names is useful when one must bind a method name or Callable to something.

The Method Descriptions list details everything about each method.

It restates the method's return data type, parameter names/types/defaults, and qualifiers.

Below that is a detailed summary of what the method does and its use case(s). It may include code samples and/or links to relevant parts of the Godot API.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Other languages — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/other_languages.html

**Contents:**
- Other languages
- User-contributed notes

The Godot developers officially support the following languages for Godot:

GDScript (all versions)

C++ (via GDExtension)

There are no plans to support additional languages officially. That said, the community offers several bindings for other languages (see below).

The bindings below are developed and maintained by the community:

Not all bindings mentioned here may be production-ready. Make sure to research options thoroughly before starting a project with one of those. Also, double-check whether the binding is compatible with the Godot version you're using.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Overview of debugging tools — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html

**Contents:**
- Overview of debugging tools
- Output Panel
- Debugger Panel
- Debug menu options
  - Deploy with Remote Debug
  - Small Deploy with Network Filesystem
  - Visible Collision Shapes
  - Visible Paths
  - Visible Navigation
  - Visible Avoidance

This guide will give you an overview of the available debugging tools in the engine.

Godot comes with a powerful debugger and profilers to track down bugs, inspect your game at runtime, monitor essential metrics, and measure performances. It also offers options to visualize collision boxes and navigation polygons in the running game.

Finally, you have options to debug the game running on a remote device and to reload changes to your scenes or your code while the game is running.

The output panel allows you to see text printed by the project, but also by the editor (e.g. from @tool scripts). You can find information about in Output panel.

Many of Godot's debugging tools are part of the Debugger panel, which you can find information about in Debugger panel.

There are a few common debug options you can toggle on or off when running your game in the editor, which can help you in debugging your game.

You can find these options in the Debug editor menu.

Here are the descriptions of the options:

When this option is enabled, using one-click deploy will make the executable attempt to connect to this computer's IP so the running project can be debugged. This option is intended to be used for remote debugging (typically with a mobile device). You don't need to enable it to use the GDScript debugger locally.

This option speeds up testing for games with a large footprint on remote devices.

When Small Deploy with Network Filesystem is on, instead of exporting the full game, deploying the game builds a minimal executable. The editor then provides files from the project over the network.

Also, on Android, the game is deployed using the USB cable to speed up deployment.

When this option is enabled, collision shapes and raycast nodes (for 2D and 3D) will be visible in the running project.

When this option is enabled, curve resources used by path nodes will be visible in the running project.

When this option is enabled, navigation meshes, and polygons will be visible in the running project.

When this option is enabled, avoidance object shapes, radiuses, and velocities will be visible in the running project.

When this option is enabled, redraw requests of 2D objects will become visible (as a short flash) in the running project. This is useful to troubleshoot low processor mode.

When this option is enabled, any changes made to the scene in the editor will be replicated in the running project. When used remotely on a device, this is more efficient when the network filesystem option is enabled.

When this option is enabled, any changes made to the script in the editor will be reloaded in the running project. When used remotely on a device, this is more efficient with the network filesystem.

When this option is enabled, the editor debug server will stay open and listen for new sessions started outside of the editor itself.

This opens a dialog allowing you to tell Godot to run multiple instances of the game at once, and to specify the command line arguments for each instance. This is especially useful when building and debugging multiplayer games.

When this option is enabled, the editor will run multiple instances of the project at once when you Run Project.

Below this checkbox is a selector to pick how many instances to run.

Checking the box and setting this to only 1 is the same as not checking this box at all.

These are the arguments that will be passed to every instance of the project when you Run Project, unless you select "Enabled" under "Override Main Run Args" for a specific instance.

Note that these arguments are space-separated.

These arguments can be accessed in your script by using get_cmdline_args.

Even if you uncheck "Enable Multiple Instances" these arguments will be passed when you Run Project.

These are the feature tags that will be passed to every instance of the project when you Run Project, unless you select "Enabled" under "Override Main Tags" for a specific instance.

When this is enabled, the arguments in the "Main Run Args" field will not be passed to this specific instance of the project when you Run Project.

These are the arguments that will be passed to this specific instance of the project when you Run Project. They will be combined with the "Main Run Args" unless you select "Enabled" under "Override Main Run Args".

When this is enabled, the tags in the "Main Feature Tags" field will not be passed to this specific instance of the project when you Run Project.

These are the feature tags that will be passed to this specific instance of the project when you Run Project. They will be combined with the "Main Feature Tags" unless you select "Enabled" under "Override Main Tags".

If you want to pass "User" arguments, that can be accessed with get_cmdline_user_args then you must prefix them with two dashes and a space like -- one two three.

Be aware that these dashes will apply to arguments added later in the "Launch Arguments" on a per instance basis, which can cause some confusion when combining the Main Run Args and Launch Arguments.

If you place -- one two three in the "Main Run Args" and -- four five six in the "Launch Arguments" then the final command line arguments will be one two three -- four five six. This is because the -- is repeated in the "Launch Arguments".

The script editor has its own set of debug tools for use with breakpoints and two options. The breakpoint tools can also be found in the Debugger tab of the debugger.

You can create a breakpoint by clicking the gutter in the left of the script editor (on the left of the line numbers). When hovering this gutter, you will see a transparent red dot appearing, which turns into an opaque red dot after the breakpoint is placed by clicking. Click the red dot again to remove the breakpoint. Breakpoints created this way persist across editor restarts, even if the script wasn't saved when exiting the editor.

You can also use the breakpoint keyword in GDScript to create a breakpoint that is stored in the script itself. Unlike breakpoints created by clicking in the gutter, this keyword-based breakpoint is persistent across different machines when using version control.

The Break button causes a break in the script like a breakpoint would. Continue makes the game continue after pausing at a breakpoint. Step Over goes to the next line of code, and Step Into goes into a function if possible. Otherwise, it does the same thing as Step Over.

The Debug with External Editor option lets you debug your game with an external editor. You can set a shortcut for it in Editor Settings > Shortcuts > Debugger.

When the debugger breaks on a breakpoint, a green triangle arrow is visible in the script editor's gutter. This arrow indicates the line of code the debugger broke on.

In the project settings, there is a Debug category with subcategories which control different things. Enable Advanced Settings to change these settings.

These are some general settings such as printing the current FPS to the Output panel, the maximum amount of functions when profiling and others.

These settings allow you to log console output and error messages to files.

These settings allow you to toggle specific GDScript warnings, such as for unused variables. You can also turn off warnings completely. See GDScript warning system for more information.

These settings allow you to toggle specific shader warnings, such as for unused variables. You can also turn off warnings completely.

These settings are for canvas item redraw debugging.

Shapes are where you can adjust the color of shapes that only appear for debugging purposes, such as collision and navigation shapes.

When running a game in the editor two options appear at the top of the Scene dock, Remote and Local. While using Remote you can inspect or change the nodes' parameters in the running project.

Some editor settings related to debugging can be found inside the Editor Settings, under the Network > Debug and Debugger sections.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## GDExtension C example — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/gdextension_c_example.html

**Contents:**
- GDExtension C example
- Introduction
- Setting up the project
- File structure
- Buildsystem
- Initializing the extension
- A basic class
- A wrapper API
- A demo project
- Custom methods

This is a simple example on how to work with GDExtension directly with C code. Note that the API is not meant to be used directly, so this will definitely be quite verbose and require a lot of steps even for a small example. However, it serves as a reference for creating bindings for a different language. It is still possible to use the API directly if you prefer, which might be convenient when only binding a third-party library.

In this example we will create a custom node that moves a sprite on the screen based on the user's parameters. While very simple, it serves to show how to do some of the things with GDExtension, like registering custom classes with methods, properties, and signals. It gives an insight on the GDExtension API.

There are a few prerequisites you'll need:

a Godot 4.2 (or later) executable,

SCons as a build tool.

Since this is using the API directly, there's no need to use the godot-cpp repository.

To organize our files, we're gonna split into mainly two folders:

We also need a copy of the gdextension_interface.h header from the Godot source code, which can be obtained directly from the Godot executable by running the following command:

This creates the header in the current folder, so you can just copy it to the src folder in the example project.

Lastly, there's another source of information we need to refer to, which is the JSON file with the Godot API reference. This file won't be used by the code directly, we will only use it to extract some information manually.

To get this JSON file, just call the Godot executable:

The resulting extension_api.json file will be created in the current folder. You can copy this file to the example folder to have it handy.

This extension is targeting Godot 4.2, but it should work on later versions as well. If you want to target a different minimal version, make sure to get the header and the JSON from the version Godot version you are targeting.

Using a buildsystem makes our life a lot easier when dealing with C code. For the sake of convenience, we'll use SCons since it's the same as what Godot itself uses.

The following SConstruct file is a simple one that will build your extension to the current platform that you are using, be it Linux, macOS, or Windows. This will be a non-optimized build for debugging purposes. It also assumes a 64-bit build, which is relevant for some parts of the example code. Making other build types and cross-compilation is out of the scope of this tutorial. Save this file to the root folder.

This will include all C files in the src folder, so we don't need to change this file when adding new source files.

The first bit of code will be responsible for initializing the extension. This is what makes Godot aware of what our GDExtension provides, such as classes and plugins.

Create the file init.h in the src folder, with the following contents:

The functions declared here have the signatures expected by the GDExtension API.

Note the inclusion of the defs.h file. This is one of our helpers to simplify writing the extension code. For now it will only contain the definition of GDE_EXPORT, a macro that makes the function public in the shared library so Godot can properly call it. This macro helps abstracting what each compiler expects.

Create the defs.h file in the src folder with the following contents:

We also include some standard headers to make things easier. Now we only have to include defs.h and those will come as a bonus.

Now, let's implement the functions we just declared. Create a file called init.c in the src folder and add this code:

What this does is set up the initialization data that Godot expects. The functions to initialize and deinitialize are set so Godot will call then when needed. It also sets the initialization level which varies per extension. Since we plan to add a custom node, the SCENE level is enough.

We will fill the initialize_gdexample_module() function later to register our custom class.

In order to make an actual node, first we'll create a C struct to hold data and functions that will act as methods. The plan is to make this a custom node that inherits from Sprite2D.

Create a file called gdexample.h in the src folder with the following contents:

Noteworthy here is the object field, which holds a pointer to the Godot object, and the gdexample_class_bind_methods() function, which will register the metadata of our custom class (properties, methods, and signals). The latter is not entirely necessary, as we can do it when registering the class, but it makes clearer to separate the concerns and let our class register its own metadata.

The object field is necessary because our class will inherit a Godot class. Since we can't inherit it directly, as we are not interacting with the source code (and C doesn't even have classes), we instead tell Godot to create an object of a type it knows and attach our extension to it. We will need the reference to such objects when calling methods on the parent class, for instance.

Let's create the source counterpart of this header. Create the file gdexample.c in the src folder and add the following code to it:

As we don't have anything to do with those functions yet, they'll stay empty for a while.

The next step is registering our class. However, in order to do so we need to create a StringName and for that we have to get a function from the GDExtension API. Since we'll need this a few times and we'll also need other things, let's create a wrapper API to facilitate this kind of chore.

We'll start by creating an api.h file in the src folder:

This file will include many other helpers as we fill our extension with something useful. For now it only has a pointer to a function that creates a StringName from a C string (in Latin-1 encoding) and another to destruct a StringName, which we'll need to use to avoid leaking memory, as well as the function to register a class, which is our initial goal.

We also keep a reference to the class_library here. This is something that Godot provides to us when initializing the extension and we'll need to use it when registering the things we create so Godot can tell which extension is making the call.

There's also a function to load those function pointers from the GDExtension API.

Let's work on the source counterpart of this header. Create the api.c file in the src folder, adding the following code:

The first important thing here is p_get_proc_address. This a function from the GDExtension API that is passed during initialization. You can use this function to request specific functions from the API by their name. Here we are caching the results so we don't have to keep a reference for p_get_proc_address everywhere and use our wrapper instead.

At the start we request the variant_get_ptr_destructor() function. This is not going to be used outside of this function, so we don't add to our wrapper and only cache it locally. The cast is necessary to silence compiler warnings.

Then we get the function that creates a StringName from a C string, exactly what we mentioned before as a needed function. We store that in our constructors struct.

Next, we use the variant_get_ptr_destructor() function we just got to query for the destructor for StringName, using the enum value from gdextension_interface.h API as a parameter. We could get destructors for other types in a similar manner, but we'll limit ourselves to what is needed for the example.

Lastly, we get the classdb_register_extension_class2() function, which we'll need in order to register our custom class.

You may wonder why the 2 is there in the function name. This means it's the second version of this function. The old version is kept to ensure backwards compatibility with older extensions, but since we have the second version available, it's best to use the new one, because we don't intend to support older Godot versions in this example.

The gdextension_interface.h header documents in which Godot version each function was introduced.

We also define the class_library variable here, which will be set during initialization.

Speaking of initialization, now we have to change the init.c file in order to fill the things we just added:

Here we set the class_library as needed and call our new load_api() function. Don't forget to also include the new headers at the top of this file:

Since we are here, we can register our new custom class. Let's fill the initialize_gdexample_module() function:

The struct with the class information is the biggest thing here. None of its fields are required with the exception of create_instance_func and free_instance_func. We haven't made those functions yet, so we'll have to work on them soon. Note that we skip the initialization if it isn't at the SCENE level. This function may be called multiple times, once for each level, but we only want to register our class once.

The other undefined thing here is StringName. This will be an opaque struct meant to hold the data of a Godot StringName in our extension. We'll define it in the appropriately named defs.h file:

As mentioned in the comment, the sizes can be found in the extension_api.json file that we generated earlier, under the builtin_class_sizes property. The BUILD_32 is never defined, as we assume we are working with a 64-bits build of Godot here, but if you need it you can add env.Append(CPPDEFINES=["BUILD_32"]) to your SConstruct file.

The // Types. comment foreshadows that we'll be adding more types to this file. Let's leave that for later.

The StringName struct here is just to hold Godot data, so we don't really care what is inside of it. Though, in this case, it is just a pointer to the data in the heap. We'll use this struct when we need to allocate data for a StringName ourselves, like we are doing when registering our class.

Back to registering, we need to work on our create and free functions. Let's include them in gdexample.h since they're specific to the custom class:

Before we can implement those function, we'll need a few more things in our API. We need a way to allocate and free memory. While we could do this with good ol' malloc(), we can instead make use of Godot's memory management functions. We'll also need a way to create a Godot object and set it with our custom instance.

So let's change the api.h to include these new functions:

Then we change the load_api() function in api.c to grab these new functions:

Now we can go back to gdexample.c and define the new functions, without forgetting to include the api.h header:

When instantiating an object, first we create a new Sprite2D object, since that's the parent of our class. Then we allocate memory for our custom struct and call its constructor. We save the pointer to the Godot object in the struct as well like we mentioned earlier.

Then we set our custom struct as the instance data. This will make Godot know that the object is an instance of our custom class and properly call our custom methods for instance, as well as passing this data back.

Note that we return the Godot object we created, not our custom struct.

For the gdextension_free_instance() function, we only call the destructor and free the memory we allocated for the custom data. It is not necessary to destruct the Godot object since that will be taken care of by the engine itself.

Now that we can create and free our custom object, we should be able to try it out in an actual project. For this, you need to open Godot and create a new project on the demo folder. The project manager may warn you the folder isn't empty if you have compiled the extension before, you can safely ignore this warning this time.

If you didn't compile the extension yet, it is the time to do it now. To do that, open a terminal or command prompt, navigate to the root folder of the extension and run scons. It should compile quickly since the extension is very simple.

Then, create a file called gdexample.gdextension inside the demo folder. This is a Godot resource that describes the extension, allowing the engine to properly load it. Put the following content in this file:

As you can see, gdexample_library_init() is the same name of the function we defined in our init.c file. It is important that the names match because it is how Godot calls the entry point of the extension.

We also set the compatibility minimum to 4.2, since we are targeting this version. It should still work on later versions. If you are using a later Godot version and rely on the new features, you need to increase this value to a version number that has everything you use. See Version compatibility for more information.

In the [libraries] section we set up the paths to the shared library on different platforms. Here there's only the debug versions since that's what we are working on for the example. Using feature tags you can fine tune this to also provide release versions, add more target operating systems, as well as providing 32-bit and 64-bit binaries.

You can also add library dependencies and custom icons for your classes in this file, but this is out of the scope for this tutorial.

After saving the file, go back to the editor. Godot should automatically load the extension. Nothing will be seen because our extension only registers a new class. To use this class add a Node2D as a root of the scene. Move it to the middle of viewport for better visibility. Then add a new child node to the root and in the Create New Node dialog search for "GDExample", the name of our class, as it should be listed there. If it isn't, it means that Godot didn't load the extension properly, so try restarting the editor and retrace the steps to see if anything went missing.

Our custom class is derived from Sprite2D, so it has a Texture property in the Inspector. Set this to the icon.svg file that Godot handily created for us when making the project. Save this scene as main.tscn and run it. You may want to set it as the main scene for convenience.

Voilà! We have a custom node running in Godot. However, it does not do anything and has nothing different than a regular Sprite2D node. We will fix that next by adding custom methods and properties.

A common thing in extensions is creating methods for the custom classes and exposing those to the Godot API. We are going to create a couple of getters and setters which are need for binding the properties afterwards.

First, let's add the new fields in our struct to hold the values for amplitude and speed, which we will use later on when creating the behavior for the node. Add them to the gdexample.h file, changing the GDExample struct:

In the same file, add the declaration for the getters and setters, right after the destructor.

In the gdexample.c file, we will initialize these values in the constructor and add the implementations for those new functions, which are quite trivial:

To make those simple functions work when called by Godot, we will need some wrappers to help us properly convert the data to and from the engine.

First, we will create wrappers for ptrcall. This is what Godot uses when the types of the values are known to be exact, which avoids using Variant. We're gonna need two of those: one for the functions that take no arguments and return a double (for the getters) and another for the functions that take a single double argument and return nothing (for the setters).

Add the declarations to the api.h file:

Those two functions follow the GDExtensionClassMethodPtrCall type, as defined in the gdextension_interface.h. We use float as a name here because in Godot the float type has double precision, so we keep this convention.

Then we implement those functions in the api.c file:

The method_userdata argument is a custom value that we give to Godot, in this case we will set as the function pointer for the one we want to call. So first we convert it to the function type, then we just call it by passing the arguments when needed, or setting the return value.

The p_instance argument contains the custom instance of our class, which we gave with object_set_instance() when creating the object.

p_args is an array of arguments. Note this contains pointers to the values. That's why we dereference it when passing to our functions. The number of arguments will be declared when binding the function (which we will do soon) and it will always include default ones if those exist.

Finally, the r_ret is a pointer to the variable where the return value needs to be set. Like the arguments, it will be the correct type as declared. For the function that does not return, we have to avoid setting it.

Note how the type and argument counts are exact, so if we needed different types, for example, we would have to create more wrappers. This could be automated using some code generation, but this is out of the scope for this tutorial.

While the ptrcall functions are used when types are exact, sometimes Godot cannot know if that's the case (when the call comes from a dynamically typed language, such as GDScript). In those situations it uses regular call functions, so we need to provide those as well when binding.

Let's create two new wrappers in the api.h file:

These follow the GDExtensionClassMethodCall type, which is a bit different. First, you receive pointers to Variants instead of exact types. There's also the amount of arguments and an error struct that you can set if something goes wrong.

In order to check the type and also extract interact with Variant, we will need a few more functions from the GDExtension API. So let's expand our wrapper structs:

The names say all about what those do. We have a couple of constructors to create and extract a floating point value to and from a Variant. We also have a couple of helpers to actually get those constructors, as well as a function to find out the type of a Variant.

Let's get those from the API, like we did before, by changing the load_api() function in the api.c file:

Now that we have these set, we can implement our call wrappers in the same file:

These functions are a bit longer but easy to follow. First they check if the argument count is as expected and if not they set the error struct and return. For the one that has one parameter, it also checks if the argument type is correct. This is important because mismatched types when extracting from Variant can cause crashes.

Then it proceeds to extract the argument using the constructor we setup before. The one with no arguments instead sets the return value after calling the function. Note how they use a pointer to a double variable, since this is what those constructors expect.

Before we can actually bind our methods, we need a way to create GDExtensionPropertyInfo instances. While we could do them inside the binding functions that we'll implement afterwards, it's easier to have a helper for it since we'll need it multiple times, including for when we bind properties.

Let's create these two functions in the api.h file:

The first one is a simplified version of the second since we usually don't need all the arguments for the property and are okay with the defaults. Then we also have a function to destruct the PropertyInfo since we need to create Strings and StringNames that need to be properly disposed of.

Speaking of which, we also need a way to create and destruct Strings, so we'll make an addition to existing structs in this same file. We'll also get a new API function for actually binding our custom method.

Before implementing those, let's do a quick stop in the defs.h file and include the size of the String type and a couple of enums:

While it's the same size as StringName, it is more clear to use a different name for it.

The enums here are just helpers to give names to the numbers they represent. The information about them is present in the extension_api.json file. Here we just set up the ones we need for the tutorial, to keep it more concise.

Going now to the api.c, we need to load the pointers to the new functions we added to the API.

Then we can also implement the functions to create the PropertyInfo struct.

The simple version of make_property() just calls the more complete one with a some default arguments. What those values mean exactly is out of the scope of this tutorial, check the page about the Object class for more details about binding methods and properties.

The complete version is more involved. First, it creates String's and StringName's for the needed fields, by allocating memory and calling their constructors. Then it creates a GDExtensionPropertyInfo struct and sets all the fields with the arguments provided. Finally it returns this created struct.

The destruct_property() function is straightforward, it simply calls the destructors for the created objects and frees their allocated memory.

Let's go back again to the header api.h to create the functions that will actually bind the methods:

Then switch back to the api.c file to implement these:

Both functions are very similar. First, they create a StringName with the method name. This is created in the stack since we don't need to keep it after the function ends. Then they create local variables to hold the call_func and ptrcall_func, pointing to the helper functions we defined earlier.

In the next step they diverge a bit. The first one creates a property for the return value, which has an empty name since it's not needed. The other creates an array of properties for the arguments, which in this case has a single element. This one also has an array of metadata, which can be used if there's something special about the argument (e.g. if an int value is 32 bits long instead of the default of 64 bits).

Afterwards, they create the GDExtensionClassMethodInfo with the required fields for each case. Then they make a StringName for the class name, in order to associate the method with the class. Next, they call the API function to actually bind this method to the class. Finally, we destruct the objects we created since they aren't needed anymore.

The bind helpers here use the call helpers we created earlier, so do note that those call helpers only accept the Godot FLOAT type (which is equivalent to double in C). If you intend to use this for other types, you would need to check the type of the arguments and return type and select an appropriate function callback. This is avoided here only to keep the example from becoming even longer.

Now that we have the means to bind methods, we can actually do so in our custom class. Go to the gdexample.c file and fill up the gdexample_class_bind_methods() function:

Since this function is already being called by the initialization process, we can stop here. This function is much more straightforward after we created all the infrastructure to make this work. You can see that implementing the binding functions inline here would take some space and also be quite repetitive. This also makes it easier to add another method in the future.

If you compile the code and reopen the demo project, nothing will be different at first, since we only added two new methods. To ensure those are registered properly, you can search for GDExample in the editor help and verify they are present in the documentation page.

Since we now have the getter and setter for our properties already bound, we can move forward to create actual properties that will be displayed in the Godot editor inspector.

Given our extensive setup in the previous section, there are only a few things needed to enable us to bind properties. First, let's get a new API function in the api.h file:

Let's also declare a function here to bind properties:

In the api.c file, we can load the new API function:

Then we can implement our new helper function in this same file:

This function is similar to the one for binding methods. The main difference is that we don't need an extra struct since we can simply use the GDExtensionPropertyInfo that is created by our helper function, so it's more straightforward. It only creates the StringName values from the C strings, creates a property info struct using our helper, calls the API function to register the property in the class and then destructs all the objects we created.

With this done, we can extend the gdexample_class_bind_methods() function in the gdexample.c file:

If you build the extension with scons, you'll see in the Godot editor the new property shown not only on the documentation page for the custom class but also in the Inspector dock when the GDExample node is selected.

Our custom node now has properties to influence how it operates, but it still doesn't do anything. In this section, we will bind the virtual method _process() and make our custom sprite move a little bit.

In the gdexample.h file, let's add a function that represents the custom _process() method:

We'll also add a "private" field to keep track of the time passed in our custom struct. This is "private" only in the sense that it won't be bound to the Godot API, even though it is public in the C side, given the language lacks access modifiers.

On the counterpart source file gdexample.c we need to initialize the new field in the constructor:

Then we can create the simplest implementation for the _process method:

For now it will do nothing but update the private field we created. We'll come back to this after the method is properly bound.

Virtual methods are a bit different from the regular bindings. Instead of explicitly registering the method itself, we'll register a special function that Godot will call to ask if a particular virtual method is implemented in our extension. The engine will pass a StringName as an argument so, following the spirit of this tutorial, we'll create a helper function to check if it is equal to a C string.

Let's add the declaration to the api.h file:

We'll also add a new struct to this file, to hold function pointers for custom operators:

Then in the api.c file we'll load the function pointer from the API:

As you can see we need a new local helper here in order to grab the function pointer for the operator.

With this handy, we can easily create our comparison function in the same file:

This function creates a StringName from the argument, compares with the other one using the operator function pointer, and returns the result. Note that the return value for the operator is passed as an out reference, this is a common thing in the API.

Let's go back to the gdexample.h file and add a couple of functions that will be used as the callbacks for the Godot API:

There are actually two ways of registering virtual methods. Only one has the get part, in which you give Godot a properly crafted function pointer which will be called. For this we would need to create another helper for each virtual method, something that is not very convenient. Instead, we use the second method which allows us to return any data, and then Godot will call a second callback and give us back this data along with the call information. We can simply give our own function pointer as custom data and then have a single callback for all virtual methods. Although in this example we will only use it for one method, this way is simpler to expand.

So let's implement those two functions in the gdexample.c file:

Those functions are also quite straightforward after making all the helpers previously.

For the first one, we simply check if the function name requested is _process and if it is we return a function pointer to our implementation of it. Otherwise we return NULL, signaling that the method is not being overridden. We don't use the p_class_userdata here since this function is meant only for one class and we don't have any data associated with it.

The second one is similar. If it is the _process() method, it uses the given function pointer to call the ptrcall helper, passing the call arguments forward. Otherwise it simply does nothing, since we don't have any other virtual methods being implemented.

The only thing missing is using those callbacks when the class is registered. Go to the init.c file and change the class_info initialization to include those, replacing the NULL value used previously:

This is enough to bind the virtual method. If you build the extension and run the demo project again, the _process() function will be called. You just won't be able to tell since the function itself does nothing visible. We will solve this now by making the custom node move following a pattern.

In order to make our node do stuff, we'll need to call Godot methods. Not only the GDExtension API functions as we've being doing so far, but actual engine methods, as we would do with scripting. This naturally requires some extra setup.

First, let's add Vector2 to our defs.h file, so we can use it in our method:

The REAL_T_IS_DOUBLE define is only needed if your Godot version was built with double precision support, which is not the default.

Now, in the api.h file, we'll add few things to the API structs, including a new one for holding engine methods to call.

Then in the api.c file we can grab the function pointers from Godot:

The only noteworthy part here is the Vector2 constructor, for which we request the index 3. Since there are multiple constructors with different kinds of arguments, we need to specify which one we want. In this case we're getting the one that takes two float numbers as the x and y coordinates, hence the name. This index can be retrieved from the extension_api.json file. Note we also need a new local helper to get it.

Be aware that we don't get anything for the methods struct here. This is because this function is called too early in the initialization process, so classes won't be properly registered yet.

Instead, we're gonna use the initialization level callback to grab those when we are registering our custom class. Add this to the init.c file:

Here we create StringName's for the class and method we want to get, then use the GDExtension API to retrieve their MethodBind, which is an object that represents the bound method. We get the set_position method from Node2D since this is where it was registered, even though we're going to use it in a Sprite2D, a derived class.

The seemingly random number for getting the bind is actually a hash of the method signature. This allows Godot to match the method you're requesting even if in a future Godot version this signature changes, by providing a compatibility method that matches what you're asking for. This is one of the systems that allow the engine to load extensions made for previous versions. You can get the value of this hash from the extension_api.json file.

With all that, we can finally implement our custom _process() method in the gdexample.c file:

After updating the time passed scaled by the speed property, it creates x and y values based on that, also modulated by the amplitude property. This is what will give the pattern effect. The math.h header is needed for the sin() and cos() functions used here.

Then it sets up an array of arguments to construct a Vector2, followed by calling the constructor. It sets up another array of arguments and use it to call the set_position() method via the bind we acquired previously.

Since nothing here allocates any memory, there's not a need to cleanup.

Now we can build the extension again and reopen Godot. Even in the editor you'll see the custom sprite moving.

Try changing the Speed and Amplitude properties and see how the sprite react.

To complete this tutorial, let's see how you can register a custom signal and emit it when appropriate. As you might have guessed, we'll need a few more function pointers from the API and more helper functions.

In the api.h file we're adding two things. One is an API function to register a signal, the other is a helper function to wrap the signal binding.

In this case we only have a version for one argument, since it's what we're going to use.

Moving to the api.c file, we can load this new function pointer and implement the helper:

This one is very similar to the function to bind methods. The main difference is that we don't need to fill another struct, we just pass the needed names and the array of arguments. The 1 at the end means the amount of arguments the signal provides.

With this we can bind the signal in gdexample.c:

In order to emit a signal, we need to call the emit_signal() method on our custom node. Since this is a vararg function (meaning it takes any amount of arguments), we cannot use ptrcall. To do a regular call, we have to create Variants, which require a few more steps of plumbing to get done.

First, in the defs.h file we create a definition for Variant:

We first set the size of Variant together with the size of Vector2 that we added before. Then we use it to create an opaque struct that is enough to hold the Variant data. Again, we set the size for double precision builds as a fallback, since by the official Godot builds use single precision.

The emit_signal() function will be called with two arguments. The first is the name of the signal to be emitted and the second is the argument we're passing to the signal connections, which is a Vector2 as we declared when binding it. So we're gonna create a helper function that can call a MethodBind with these types. Even though it does return something (an error code), we don't need to deal with it, so for now we're just going to ignore it.

In the api.h, we're adding a few things to the existing structs, plus a new helper function for the call:

Now let's switch to the api.c file to load these new function pointers and implement the helper function.

This helper function has some boilerplate code but is quite straightforward. It sets up the two arguments inside stack allocated Variants, then creates an array with pointers to those. It also sets up another Variant to keep the return value, which we don't need to construct since the call expects it to be uninitialized.

Then it actually calls the MethodBind using the instance we provided and the arguments. The NULL at the end would be a pointer to a GDExtensionCallError struct. This can be used to treat potential errors when calling the functions (such as wrong arguments). For the sake of simplicity we're not gonna handle that here.

At the end we need to destruct the Variants we created. While technically the Vector2 one does not require destructing, it is clearer to cleanup everything.

We also need to load the MethodBind, which we'll do in the init.c file, right after loading the one for the set_position method we did before:

Note that we reuse the native_class_name and method_name variables here, so we don't need to declare new ones.

Now go to the gdexample.h file where we're going to add a couple of fields:

The first one will store the time passed since the last signal was emitted, since we'll be doing so at regular intervals. The other is just to cache the signal name so we don't need to create a new StringName every time.

In the source gdexample.c file we can change the constructor and destructor to deal with the new fields:

It is important to destruct the StringName to avoid memory leaks.

Now we can add to the gdexample_class_process() function to actually emit the signal:

This updates the time passed for the signal emission and, if it is over one second it calls the emit_signal() function on the current instance, passing the name of the signal and the new position as arguments.

Now we're done with our C GDExtension. Build it once more and reopen the demo project in the editor.

In the documentation page for GDExample you can see the new signal we bound:

To check it's working, let's add a small script to the root node, parent of our custom one, that prints the position to the output every time it receives the signal:

Run the project and you can observe the values being printed in the Output dock in the editor:

This tutorial shows a basic extension with custom methods, properties, and signals. While it does require a good amount of boilerplate, it can scale well by creating helper functions to handle the tedious tasks.

This should serve as a good basis to understand the GDExtension API and as a starting point to create custom binding generators. In fact, it would be possible to create bindings for C using such type of generator, making the actual coding look more like the gdexample.c file in this example, which is quite straightforward and not very verbose.

If you want to create actual extensions, it is preferred to use the C++ bindings instead, as it takes away all of the boilerplate from your code. Check the godot-cpp documentation to see how you can do this.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
gdextension_c_example/
|
+--demo/                  # game example/demo to test the extension
|
+--src/                   # source code of the extension we are building
```

Example 2 (unknown):
```unknown
godot --dump-gdextension-interface
```

Example 3 (unknown):
```unknown
godot --dump-extension-api
```

Example 4 (python):
```python
#!/bin/env python
from SCons.Script import Environment
from os import path
import sys

env = Environment()

# Set the target path and name.
target_path = "demo/bin/"
target_name = "libgdexample"

# Set the compiler and flags.
env.Append(CPPPATH=["src"])  # Add the src folder to the include path.
env.Append(CFLAGS=["-O0", "-g"])  # Make it a debug build.

# Use Clang on macOS.
if sys.platform == "darwin":
    env["CC"] = "clang"

# Add all C files in "src" folder as sources.
sources = env.Glob("src/*.c")

# Create a shared library.
library = env.SharedLibrary(
    target=path.join(target_path, target_name),
    source=sources,
)

# Set the library as the default target.
env.Default(library)
```

---

## Debug — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/index.html

**Contents:**
- Debug

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Debugger panel — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html

**Contents:**
- Debugger panel
- Stack Trace
- Errors
- Evaluator
- Profiler
- Visual Profiler
- Network Profiler
- Monitors
- Video RAM
- Misc

Many of Godot's debugging tools, including the debugger, can be found in the debugger panel at the bottom of the screen. Click on Debugger to open it.

The debugger panel is split into several tabs, each focusing on a specific task.

The Stack Trace tab opens automatically when the GDScript compiler reaches a breakpoint in your code.

It gives you a stack trace, information about the state of the object, and buttons to control the program's execution. When the debugger breaks on a breakpoint, a green triangle arrow is visible in the script editor's gutter. This arrow indicates the line of code the debugger broke on.

You can create a breakpoint by clicking the gutter in the left of the script editor (on the left of the line numbers). When hovering this gutter, you will see a transparent red dot appearing, which turns into an opaque red dot after the breakpoint is placed by clicking. Click the red dot again to remove the breakpoint. Breakpoints created this way persist across editor restarts, even if the script wasn't saved when exiting the editor.

You can also use the breakpoint keyword in GDScript to create a breakpoint that is stored in the script itself. Unlike breakpoints created by clicking in the gutter, this keyword-based breakpoint is persistent across different machines when using version control.

You can use the buttons in the top-right corner to:

Skip all breakpoints. That way, you can save breakpoints for future debugging sessions.

Copy the current error message.

Step Into the code. This button takes you to the next line of code, and if it's a function, it steps line-by-line through the function.

Step Over the code. This button goes to the next line of code, but it doesn't step line-by-line through functions.

Break. This button pauses the game's execution.

Continue. This button resumes the game after a breakpoint or pause.

Using the debugger and breakpoints on tool scripts is not currently supported. Breakpoints placed in the script editor or using the breakpoint keyword are ignored. You can use print statements to display the contents of variables instead.

This is where error and warning messages are printed while running the game.

You can disable specific warnings in Project Settings > Debug > GDScript.

This tab contains an expression evaluator, also known as a REPL. This is a more powerful complement to the Stack Variables tree available in the Stack Trace tab.

When the project is interrupted in the debugger (due to a breakpoint or script error), you can enter an expression in the text field at the top. If the project is running, the expression field won't be editable, so you will need to set a breakpoint first. Expressions can be persisted across runs by unchecking Clear on Run, although they will be lost when the editor quits.

Expressions are evaluated using Godot's expression language, which allows you to perform arithmetic and call some functions within the expression. Expressions can refer to member variables, or local variables within the same scope as the line the breakpoint is on. You can also enter constant values, which makes it usable as a built-in calculator.

Consider the following script:

If the debugger breaks on the first line containing breakpoint, the following expressions return non-null values:

Constant expression: 2 * PI + 5

Member variable: counter, counter ** 2, sqrt(counter)

Local variable or function parameter: delta, text, text.to_upper()

If the debugger breaks on the second line containing breakpoint, the following expressions return non-null values:

Constant expression: 2 * PI + 5

Member variable: counter, counter ** 2, sqrt(counter)

Local variable or function parameter: delta, other_text, other_text.to_upper()

The profiler is used to see what code is running while your project is in use, and how that effects performance.

A detailed explanation of how to use the profiler can be found in the dedicated The Profiler page.

The Visual Profiler can be used to monitor what is taking the most time when rendering a frame on the CPU and GPU respectively. This allows tracking sources of potential CPU and GPU bottlenecks caused by rendering.

The Visual Profiler only measures CPU time taken for rendering tasks, such as performing draw calls. The Visual Profiler does not include CPU time taken for other tasks such as scripting and physics. Use the standard Profiler tab to track non-rendering-related CPU tasks.

To use the visual profiler, run the project, switch to the Visual Profiler tab within the Debugger bottom panel, then click Start:

Visual Profiler tab after clicking Start, waiting for a few seconds, then clicking Stop

You can also check Autostart, which will make the visual profiler automatically start when the project is run the next time. Note that the Autostart checkbox's state is not preserved across editor sessions.

You will see categories and results appearing as the profiler is running. Graph lines also appear, with the left side being a CPU framegraph and the right side being a GPU framegraph.

Click Stop to finish profiling, which will keep the results visible but frozen in place. Results remain visible after stopping the running project, but not after exiting the editor.

Click on result categories on the left to highlight them in the CPU and GPU graphs on the right. You can also click on the graph to move the cursor to a specific frame number and highlight the selected data type in the result categories on the left.

You can switch the result display between a time value (in milliseconds per frame) or a percentage of the target frametime (which is currently hardcoded to 16.67 milliseconds, or 60 FPS).

If framerate spikes occur during profiling, this can cause the graph to be poorly scaled. Disable Fit to Frame so that the graph will zoom onto the 60 FPS+ portion.

Remember that Visual Profiler results can vary heavily based on viewport resolution, which is determined by the window size if using the disabled or canvas_items stretch modes.

When comparing results across different runs, make sure to use the same viewport size for all runs.

Visual Profiler is supported when using any rendering method (Forward+, Mobile or Compatibility), but the reported categories will vary depending on the current rendering method as well as the enabled graphics features. For example, when using Forward+, a simple 2D scene with shadow-casting lights will result in the following categories appearing:

Example results from a 2D scene in the Visual Profiler

To give another example with Forward+, a 3D scene with shadow-casting lights and various effects enabled will result in the following categories enabled:

Example results from a 3D scene in the Visual Profiler

Notice how in the 3D example, several of the categories have (Parallel) appended to their name. This hints that multiple tasks are being performed in parallel on the GPU. This generally means that disabling only one of the features involved won't improve performance as much as anticipated, as the other task still needs to be performed sequentially.

The Visual Profiler is not supported when using the Compatibility renderer on macOS, due to platform limitations.

The Network Profiler contains a list of all the nodes that communicate over the multiplayer API and, for each one, some counters on the amount of incoming and outgoing network interactions. It also features a bandwidth meter that displays the total bandwidth usage at any given moment.

The bandwidth meter does not take the High-level multiplayer API's own compression system into account. This means that changing the compression algorithm used will not change the metrics reported by the bandwidth meter.

The monitors are graphs of several aspects of the game while it's running such as FPS, memory usage, how many nodes are in a scene and more. All monitors keep track of stats automatically, so even if one monitor isn't open while the game is running, you can open it later and see how the values changed.

In addition to the default performance monitors, you can also create custom performance monitors to track arbitrary values in your project.

The Video RAM tab shows the video RAM usage of the game while it is running. It provides a list of every resource using video RAM by resource path, the type of resource it is, what format it is in, and how much Video RAM that resource is using. There is also a total video RAM usage number at the top right of the panel.

The Misc tab contains tools to identify the control nodes you are clicking at runtime:

Clicked Control tells you where the clicked node is in the scene tree.

Clicked Control Type tells you the type of the node you clicked is.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var counter = 0

func _process(delta):
    counter += 1
    if counter == 5:
        var text = "Some text"
        breakpoint
    elif counter >= 6:
        var other_text = "Some other text"
        breakpoint
```

---

## Nodes and scene instances — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/nodes_and_scene_instances.html

**Contents:**
- Nodes and scene instances
- Getting nodes
- Node paths
  - Syntactic sugar
- Creating nodes
- Instancing scenes
- User-contributed notes

This guide explains how to get nodes, create nodes, add them as a child, and instantiate scenes from code.

Check the Creating instances tutorial to learn about Godot's approach to scene instancing.

You can get a reference to a node by calling the Node.get_node() method. For this to work, the child node must be present in the scene tree. Getting it in the parent node's _ready() function guarantees that.

If, for example, you have a scene tree like this, and you want to get a reference to the Sprite2D and Camera2D nodes to access them in your script.

To do so, you can use the following code.

Note that you get nodes using their name, not their type. Above, "Sprite2D" and "Camera2D" are the nodes' names in the scene.

If you rename the Sprite2D node as Skin in the Scene dock, you have to change the line that gets the node to get_node("Skin") in the script.

When getting a reference to a node, you're not limited to getting a direct child. The get_node() function supports paths, a bit like when working with a file browser. Add a slash to separate nodes.

Take the following example scene, with the script attached to the UserInterface node.

To get the AnimationPlayer node, you would use the following code.

As with file paths, you can use ".." to get a parent node. The best practice is to avoid doing that though not to break encapsulation. You can also start the path with a forward slash to make it absolute, in which case your topmost node would be "/root", the application's predefined root viewport.

You can use two shorthands to shorten your code in GDScript. Firstly, putting the @onready annotation before a member variable makes it initialize right before the _ready() callback.

There is also a short notation for get_node(): the dollar sign, "$". You place it before the name or path of the node you want to get.

To create a node from code, call its new() method like for any other class-based datatype.

You can store the newly created node's reference in a variable and call add_child() to add it as a child of the node to which you attached the script.

To delete a node and free it from memory, you can call its queue_free() method. Doing so queues the node for deletion at the end of the current frame after it has finished processing. At that point, the engine removes the node from the scene and frees the object in memory.

Before calling sprite2d.queue_free(), the remote scene tree looks like this.

After the engine freed the node, the remote scene tree doesn't display the sprite anymore.

You can alternatively call free() to immediately destroy the node. You should do this with care as any reference to it will instantly become null. We recommend using queue_free() unless you know what you're doing.

When you free a node, it also frees all its children. Thanks to this, to delete an entire branch of the scene tree, you only have to free the topmost parent node.

Scenes are templates from which you can create as many reproductions as you'd like. This operation is called instancing, and doing it from code happens in two steps:

Loading the scene from the local drive.

Creating an instance of the loaded PackedScene resource.

Preloading the scene can improve the user's experience as the load operation happens when the compiler reads the script and not at runtime. This feature is only available with GDScript.

At that point, scene is a packed scene resource, not a node. To create the actual node, you need to call PackedScene.instantiate(). It returns a tree of nodes that you can use as a child of your current node.

The advantage of this two-step process is you can keep a packed scene loaded and create new instances on the fly. For example, to quickly instance several enemies or bullets.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var sprite2d
var camera2d

func _ready():
    sprite2d = get_node("Sprite2D")
    camera2d = get_node("Camera2D")
```

Example 2 (gdscript):
```gdscript
private Sprite2D _sprite2D;
private Camera2D _camera2D;

public override void _Ready()
{
    base._Ready();

    _sprite2D = GetNode<Sprite2D>("Sprite2D");
    _camera2D = GetNode<Camera2D>("Camera2D");
}
```

Example 3 (gdscript):
```gdscript
var animation_player

func _ready():
    animation_player = get_node("ShieldBar/AnimationPlayer")
```

Example 4 (gdscript):
```gdscript
private AnimationPlayer _animationPlayer;

public override void _Ready()
{
    base._Ready();

    _animationPlayer = GetNode<AnimationPlayer>("ShieldBar/AnimationPlayer");
}
```

---

## Overridable functions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/overridable_functions.html

**Contents:**
- Overridable functions
- User-contributed notes

Godot's Node class provides virtual functions you can override to update nodes every frame or on specific events, like when they enter the scene tree.

This document presents the ones you'll use most often.

Under the hood, these functions rely on Godot's low-level notifications system. To learn more about it, see Godot notifications.

Two functions allow you to initialize and get nodes besides the class's constructor: _enter_tree() and _ready().

When the node enters the Scene Tree, it becomes active and the engine calls its _enter_tree() method. That node's children may not be part of the active scene yet. As you can remove and re-add nodes to the scene tree, this function may be called multiple times throughout a node's lifetime.

Most of the time, you'll use _ready() instead. This function is called only once in a node's lifetime, after _enter_tree(). _ready() ensures that all children have entered the scene tree first, so you can safely call get_node() on them.

To learn more about getting node references, read Nodes and scene instances.

Another related callback is _exit_tree(), which the engine calls every time a node is about to exit the scene tree. This can be when you call Node.remove_child() or when you free a node.

The two virtual methods _process() and _physics_process() allow you to update the node, every frame and every physics frame respectively. For more information, read the dedicated documentation: Idle and Physics Processing.

Two more essential built-in node callback functions are Node._unhandled_input() and Node._input(), which you use to both receive and process individual input events. The _unhandled_input() method receives every key press, mouse click, etc. that have not been handled already in an _input() callback or in a user interface component. You want to use it for gameplay input in general. The _input() callback allows you to intercept and process input events before _unhandled_input() gets them.

To learn more about inputs in Godot, see the Input section.

There are some more overridable functions like Node._get_configuration_warnings(). Specialized node types provide more callbacks like CanvasItem._draw() to draw programmatically or Control._gui_input() to handle clicks and input on UI elements.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# Called every time the node enters the scene tree.
func _enter_tree():
    pass

# Called when both the node and its children have entered the scene tree.
func _ready():
    pass

# Called when the node is about to leave the scene tree, after all its
# children received the _exit_tree() callback.
func _exit_tree():
    pass
```

Example 2 (gdscript):
```gdscript
// Called every time the node enters the scene tree.
public override void _EnterTree()
{
    base._EnterTree();
}

// Called when both the node and its children have entered the scene tree.
public override void _Ready()
{
    base._Ready();
}

// Called when the node is about to leave the scene tree, after all its
// children.
public override void _ExitTree()
{
    base._ExitTree();
}
```

Example 3 (gdscript):
```gdscript
# Called every frame.
func _process(delta):
    pass

# Called every physics frame.
func _physics_process(delta):
    pass
```

Example 4 (gdscript):
```gdscript
public override void _Process(double delta)
{
    // Called every frame.
    base._Process(delta);
}

public override void _PhysicsProcess(double delta)
{
    // Called every physics frame.
    base._PhysicsProcess(delta);
}
```

---

## Custom performance monitors — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/custom_performance_monitors.html

**Contents:**
- Custom performance monitors
- Introduction
- Creating a custom performance monitor
- Querying a performance monitor in a project
- User-contributed notes

As explained in the Debugger panel documentation, Godot features a Debugger > Monitors bottom panel that allows tracking various values with graphs showing their evolution over time. The data for those graphs is sourced from the engine's Performance singleton.

Since Godot 4.0, you can declare custom values to be displayed in the Monitors tab. Example use cases for custom performance monitors include:

Displaying performance metrics that are specific to your project. For instance, in a voxel game, you could create a performance monitor to track the number of chunks that are loaded every second.

Displaying in-game metrics that are not strictly related to performance, but are still useful to graph for debugging purposes. For instance, you could track the number of enemies present in the game to make sure your spawning mechanic works as intended.

In this example, we'll create a custom performance monitor to track how many enemies are present in the currently running project.

The main scene features a Timer node with the following script attached:

The second parameter of Performance.add_custom_monitor is a Callable.

enemy.tscn is a scene with a Node2D root node and Timer child node. The Node2D has the following script attached:

In this example, since we spawn 20 enemies per second, and each enemy despawns 2.5 seconds after they spawn, we expect the number of enemies present in the scene to stabilize to 50. We can make sure about this by looking at the graph.

To visualize the graph created from this custom performance monitor, run the project, switch to the editor while the project is running and open Debugger > Monitors at the bottom of the editor window. Scroll down to the newly available Game section and check Enemies. You should see a graph appearing as follows:

Example editor graph from a custom performance monitor

The performance monitor handling code doesn't have to live in the same script as the nodes themselves. You may choose to move the performance monitor registration and getter function to an autoload instead.

If you wish to display the value of the performance monitor in the running project's window (rather than the editor), use Performance.get_custom_monitor("category/name") to fetch the value of the custom monitor. You can display the value using a Label, RichTextLabel, Custom drawing in 2D, 3D text, etc.

This method can be used in exported projects as well (debug and release mode), which allows you to create visualizations outside the editor.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Timer


func _ready():
    # The slash delimiter is used to determine the category of the monitor.
    # If there is no slash in the monitor name, a generic "Custom" category
    # will be used instead.
    Performance.add_custom_monitor("game/enemies", get_enemy_count)
    timeout.connect(_on_timeout)
    # Spawn 20 enemies per second.
    wait_time = 0.05
    start()


func _on_timeout():
    var enemy = preload("res://enemy.tscn").instantiate()
    get_parent().add_child(enemy)


# This function is called every time the performance monitor is queried
# (this occurs once per second in the editor, more if called manually).
# The function must return a number greater than or equal to 0 (int or float).
func get_enemy_count():
    return get_tree().get_nodes_in_group("enemies").size()
```

Example 2 (gdscript):
```gdscript
extends Node2D


func _ready():
    add_to_group("enemies")
    $Timer.timeout.connect(_on_timer_timeout)
    # Despawn enemies 2.5 seconds after they spawn.
    $Timer.wait_time = 2.5
    $Timer.start()


func _on_timer_timeout():
    queue_free()
```

---

## Output panel — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/output_panel.html

**Contents:**
- Output panel
- Message categories
- Filtering messages
- Clearing messages
- Printing messages
  - Printing rich text
- User-contributed notes

The output panel is found at the bottom of the screen. Click on Output to open it.

The output panel provides several features to make viewing text printed by the project (and editor) easier.

The output panel automatically opens when running a project by default. You can control this behavior by changing the Run > Bottom Panel > Action on Play editor setting.

Four message categories are available:

Log: Standard messages printed by the project. Displayed in white or black (depending on the editor theme).

Error: Messages printed by the project or editor that indicate a failure of some kind. Displayed in red.

Warning: Messages printed by the project or editor that report important information, but do not indicate a failure. Displayed in yellow.

Editor: Messages printed by the editor, typically intended to be traces of undo/redo actions. Displayed in gray.

By clicking on the buttons on the right, you can hide certain message categories. This can make it easier to find specific messages you're looking for.

You can also filter messages by their text content using the Filter Messages box at the bottom of the Output panel.

When running the project, existing messages are automatically cleared by default. This is controlled by the Run > Output > Always Clear Output on Play editor setting. Additionally, you can manually clear messages by clicking the "cleaning brush" icon in the top-right corner of the Output panel.

Several methods are available to print messages:

print(): Prints a message. This method accepts multiple arguments which are concatenated together upon printing. This method has variants that separate arguments with tabs and spaces respectively: printt() and prints().

print_rich(): Same as print(), but BBCode can be used to format the text that is printed (see below).

push_error(): Prints an error message. When an error is printed in a running project, it's displayed in the Debugger > Errors tab instead.

push_warning(): Prints a warning message. When a warning is printed in a running project, it's displayed in the Debugger > Errors tab instead.

For more complex use cases, these can be used:

print_verbose(): Same as print(), but only prints when verbose mode is enabled in the Project Settings or the project is run with the --verbose command line argument.

printerr(): Same as print(), but prints to the standard error stream instead of the standard output string. push_error() should be preferred in most cases.

printraw(): Same as print(), but prints without a blank line at the end. This is the only method that does not print to the editor Output panel. It prints to the standard output stream only, which means it's still included in file logging.

print_stack(): Print a stack trace from the current location. Only supported when running from the editor, or when the project is exported in debug mode.

print_tree(): Prints the scene tree relative to the current node. Useful for debugging node structures created at runtime.

print_tree_pretty(): Same as print_tree(), but with Unicode characters for a more tree-like appearance. This relies on box-drawing characters, so it may not render correctly with all fonts.

To get more advanced formatting capabilities, consider using GDScript format strings along with the above printing functions.

The engine's logging facilities are covered in the logging documentation.

Using print_rich(), you can print rich text to the editor Output panel and standard output (visible when the user runs the project from a terminal). This works by converting the BBCode to ANSI escape codes that the terminal understands.

In the editor output, all BBCode tags are recognized as usual. In the terminal output, only a subset of BBCode tags will work, as documented in the linked print_rich() method description above. In the terminal, the colors will look different depending on the user's theme, while colors in the editor will use the same colors as they would in the project.

ANSI escape code support varies across terminal emulators. The exact colors displayed in terminal output also depend on the terminal theme chosen by the user.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Idle and Physics Processing — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html

**Contents:**
- Idle and Physics Processing
- User-contributed notes

Games run in a loop. Each frame, you need to update the state of your game world before drawing it on screen. Godot provides two virtual methods in the Node class to do so: Node._process() and Node._physics_process(). If you define either or both in a script, the engine will call them automatically.

There are two types of processing available to you:

Idle processing allows you to run code that updates a node every frame, as often as possible.

Physics processing happens at a fixed rate, 60 times per second by default. This is independent of your game's actual framerate, and keeps physics running smoothly. You should use it for anything that involves the physics engine, like moving a body that collides with the environment.

You can activate idle processing by defining the _process() method in a script. You can turn it off and back on by calling Node.set_process().

The engine calls this method every time it draws a frame:

Keep in mind that the frequency at which the engine calls _process() depends on your application's framerate, which varies over time and across devices.

The function's delta parameter is the time elapsed in seconds since the previous call to _process(). Use this parameter to make calculations independent of the framerate. For example, you should always multiply a speed value by delta to animate a moving object.

Physics processing works with a similar virtual function: _physics_process(). Use it for calculations that must happen before each physics step, like moving a character that collides with the game world. As mentioned above, _physics_process() runs at fixed time intervals as much as possible to keep the physics interactions stable. You can change the interval between physics steps in the Project Settings, under Physics -> Common -> Physics Fps. By default, it's set to run 60 times per second.

The engine calls this method before every physics step:

The function _process() is not synchronized with physics. Its rate depends on hardware and game optimization. It also runs after the physics step in single-threaded games.

You can see the _process() function at work by creating a scene with a single Label node, with the following script attached to it:

When you run the scene, you should see a counter increasing each frame.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _process(delta):
    # Do something...
    pass
```

Example 2 (gdscript):
```gdscript
public override void _Process(double delta)
{
    // Do something...
}
```

Example 3 (go):
```go
func _physics_process(delta):
    # Do something...
    pass
```

Example 4 (json):
```json
public override void _PhysicsProcess(double delta)
{
    // Do something...
}
```

---

## The Profiler — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html

**Contents:**
- The Profiler
- An overview of the profiler
- The measured data
- Scope of measurement and measurement windows
- Debugging slow code with the profiler
- Measuring manually in microseconds
- User-contributed notes

You run your game from Godot and play around. It's fun, it's becoming feature complete, and you feel it's getting close to release.

But then, you open the skill tree, and it grinds to a halt as something snags in your code. Watching the skill tree scroll by like it's a slide show is unacceptable. What went wrong? Is it positioning the skill tree elements, the UI, or rendering?

You could try to optimize everything and run the game repeatedly, but you can be smarter about this and narrow down the possibilities. Enter Godot's profiler.

You can open the profiler by opening the Debugger panel and clicking on the Profiler tab.

Godot's profiler does not automatically run because profiling is performance-intensive. It has to continually measure everything happening in the game and report back to the debugger, so it's off by default.

To begin profiling, run your game then focus back on the editor. Click on the Start button in the top-left corner of the Profiler tab. You can also check Autostart, which will make the profiler automatically start when the project is run the next time. Note that the Autostart checkbox's state is not preserved across editor sessions.

The profiler does not currently support C# scripts. C# scripts can be profiled using JetBrains Rider and JetBrains dotTrace with the Godot support plugin.

You can clear the data by clicking the Clear button anytime. Use the Measure drop-down menu to change the type of data you measure. The measurements panel and the graph will update accordingly.

The profiler's interface is split into two. There is a list of functions on the left and the performance graph on the right.

The main measurements are frame time, physics frame, idle time, and physics time.

The frame time is the time it takes Godot to execute all the logic for an entire image, from physics to rendering.

Physics frame is the time Godot has allocated between physics updates. In an ideal scenario, the frame time is whatever you chose: 16.66 milliseconds by default, which corresponds to 60FPS. It's a frame of reference you can use for everything else around it.

Idle time is the time Godot took to update logic other than physics, such as code that lives in _process or timers and cameras set to update on Idle.

Physics time is the time Godot took to update physics tasks, like _physics_process and built-in nodes set to Physics update.

Frame Time includes rendering time. Say you find a mysterious spike of lag in your game, but your physics and scripts are all running fast. The delay could be due to the appearance of particles or visual effects!

By default, Godot ticks on Frame Time and Physics Time. This gives you an overview of how long each frame takes relative to the allocated desired physics FPS. You can toggle functions on and off by clicking the checkboxes on the left. Other facilities make appearances as you go down the list, like Physics 2D, Physics, and Audio, before reaching Script functions, where your code appears.

If you click on the graph, you change which frame's information appears on the left. In the top right, there is also a frame counter where you can manually adjust the frame you are looking at more granularly.

You can change what measurement you are looking at using the Measure drop-down menu. By default, it starts with Frame Time and lists the time it takes to go through the frame in milliseconds. The average time is the average time any given function took when called more than once. For example, a function that took 0.05 milliseconds to run five times should give you an average of 0.01 milliseconds.

If accurate milliseconds count is not important, and you want to see proportions of time relative to the rest of the frame, use percentage measurements. Frame % is relative to Frame Time, and Physics % is relative to Physics Time.

The last option is the scope of the time. Inclusive measures the time a function took with any nested function calls. For example:

get_neighbors, find_nearest_neighbor and move_subject all took a lot of time. You could be fooled into thinking that this is because all three of them are slow.

But when changed to Self, Godot measures the time spent in the function body without considering function calls it made itself.

You can see that get_neighbors and move_subject have lost a lot of their importance. In effect, that means that get_neighbors and move_subject have spent more time waiting for some other function call to finish than not, and find_nearest_neighbor is actually slow.

Finding slow code with the profiler boils down to running your game and watching the performance graph as it draws. When an unacceptable spike occurs in the frame time, you can click on the graph to pause your game and narrow the _Frame #_ to the spike's start. You may need to jump back and forth between frames and functions to find the root cause.

Under the Script functions, turn on the checkboxes for some functions to find which take time. These are the functions you need to review and optimize.

If your function is complex, it could be challenging to figure out which part needs optimization. Is it your math or the way you access other pieces of data to do the math with? Is it the for loop? The if statements?

You can narrow down the measurement by manually counting ticks as the code runs with some temporary functions. The two functions are part of the Time class object. They are get_ticks_msec and get_ticks_usec. The first measures in milliseconds (1,000 per second), and the second measures in microseconds (1,000,000 per second).

Either one returns the amount of time since the game engine started in their respective time frame.

If you wrap a piece of code with a start and end count of microseconds, the difference between the two is the amount of time it took to run that piece of code.

As you become a more experienced programmer, this technique becomes less necessary. You begin to learn what parts of a running program are slow. Knowing that loops and branches can be slow comes from experience, and you gain experience by measuring and doing research.

But between the profiler and the ticks functions, you should have enough to get started finding which parts of your code need optimization.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
# Measuring the time it takes for worker_function() to run
var start = Time.get_ticks_usec()
worker_function()
var end = Time.get_ticks_usec()
var worker_time = (end-start)/1000000.0

# Measuring the time spent running a calculation over each element of an array
start = Time.get_ticks_usec()
for calc in calculations:
    result = pow(2, calc.power) * calc.product
end = Time.get_ticks_usec()
var loop_time = (end-start)/1000000.0

print("Worker time: %s\nLoop time: %s" % [worker_time, loop_time])
```

---

## Groups — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html

**Contents:**
- Groups
- Managing groups
  - Using the Node dock
  - Using code
- User-contributed notes

Groups in Godot work like tags in other software. You can add a node to as many groups as you want. Then, in code, you can use the SceneTree to:

Get a list of nodes in a group.

Call a method on all nodes in a group.

Send a notification to all nodes in a group.

This is a useful feature to organize large scenes and decouple code.

Groups are created by adding a node to a new group name, and likewise they are removed by removing all nodes from a given group.

There are two ways to add/remove nodes to groups:

During design, by using the Node dock in the editor, or the Global Groups in project settings.

During execution, by calling Node.add_to_group() or Node.remove_from_group().

You can create new groups using the Groups tab in the Node dock.

Select a node in the Scene dock then click the add button with the + symbol.

You should now see the Create New Group modal appear. Write the group name in the field.

You can optionally mark the option "Global", which will make the group visible project-wide, and able to be reused in any project scene. This will also allow you to give it a description.

When done, press Ok to create it.

You should see the new groups appear in the Groups tab under Scene Groups if the Global option was unmarked, or under Global Groups if that option was marked.

A selected Node from the Scene dock can be added into groups by marking the checkbox on the left side of the groups in the Groups dock. The node you had selected when creating a new group will be automatically checked.

All groups present in the project that were marked as Global, created from any scene, will be visible under Global Groups.

Any other group derived from nodes in the current scene will appear under Scene Groups.

The same underlying logic is used for both Global and Scene groups. Groups with the same name are considered one and the same. This feature is purely organizational.

You can manage Global Groups in the Global Groups dock, inside Project Settings. There, you will be able to add new global groups, or change existing groups' names and descriptions.

You can also manage groups from scripts. The following code adds the node to which you attach the script to the guards group as soon as it enters the scene tree.

Imagine you're creating an infiltration game. When an enemy spots the player, you want all guards and robots to be on alert.

In the fictional example below, we use SceneTree.call_group() to alert all enemies that the player was spotted.

The above code calls the function enter_alert_mode on every member of the group guards.

To get the full list of nodes in the guards group as an array, you can call SceneTree.get_nodes_in_group():

The SceneTree class provides many more useful methods to interact with scenes, their node hierarchy, and groups. It allows you to switch scenes easily or reload them, quit the game or pause and unpause it. It also provides useful signals.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _ready():
    add_to_group("guards")
```

Example 2 (gdscript):
```gdscript
public override void _Ready()
{
    base._Ready();

    AddToGroup("guards");
}
```

Example 3 (go):
```go
func _on_player_spotted():
    get_tree().call_group("guards", "enter_alert_mode")
```

Example 4 (json):
```json
public void _OnPlayerDiscovered()
{
    GetTree().CallGroup("guards", "enter_alert_mode");
}
```

---

## Cross-language scripting — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/cross_language_scripting.html

**Contents:**
- Cross-language scripting
- Instantiating nodes
  - Instantiating C# nodes from GDScript
  - Instantiating GDScript nodes from C#
- Accessing fields
  - Accessing C# fields from GDScript
  - Accessing GDScript fields from C#
- Calling methods
  - Calling C# methods from GDScript
  - Calling GDScript methods from C#

Godot allows you to mix and match scripting languages to suit your needs. This means a single project can define nodes in both C# and GDScript. This page will go through the possible interactions between two nodes written in different languages.

The following two scripts will be used as references throughout this page.

If you're not using nodes from the scene tree, you'll probably want to instantiate nodes directly from the code.

Using C# from GDScript doesn't need much work. Once loaded (see Classes as resources), the script can be instantiated with new().

When creating .cs scripts, you should always keep in mind that the class Godot will use is the one named like the .cs file itself. If that class does not exist in the file, you'll see the following error: Invalid call. Nonexistent function `new` in base.

For example, MyCoolNode.cs should contain a class named MyCoolNode.

The C# class needs to derive a Godot class, for example GodotObject. Otherwise, the same error will occur.

You also need to check your .cs file is referenced in the project's .csproj file. Otherwise, the same error will occur.

From the C# side, everything work the same way. Once loaded, the GDScript can be instantiated with GDScript.New().

Here we are using an Object, but you can use type conversion like explained in Type conversion and casting.

Accessing C# fields from GDScript is straightforward, you shouldn't have anything to worry about.

As C# is statically typed, accessing GDScript from C# is a bit more convoluted. You will have to use GodotObject.Get() and GodotObject.Set(). The first argument is the name of the field you want to access.

Keep in mind that when setting a field value you should only use types the GDScript side knows about. Essentially, you want to work with built-in types as described in Built-in types or classes extending Object.

Again, calling C# methods from GDScript should be straightforward. The marshalling process will do its best to cast the arguments to match function signatures. If that's impossible, you'll see the following error: Invalid call. Nonexistent function `FunctionName`.

To call GDScript methods from C# you'll need to use GodotObject.Call(). The first argument is the name of the method you want to call. The following arguments will be passed to said method.

Connecting to a C# signal from GDScript is the same as connecting to a signal defined in GDScript:

Connecting to a GDScript signal from C# only works with the Connect method because no C# static types exist for signals defined by GDScript:

A GDScript file may not inherit from a C# script. Likewise, a C# script may not inherit from a GDScript file. Due to how complex this would be to implement, this limitation is unlikely to be lifted in the future. See this GitHub issue for more information.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends Node

var my_property: String = "my gdscript value":
    get:
        return my_property
    set(value):
        my_property = value

signal my_signal
signal my_signal_with_params(msg: String, n: int)

func print_node_name(node: Node) -> void:
    print(node.get_name())

func print_array(arr: Array) -> void:
    for element in arr:
        print(element)

func print_n_times(msg: String, n: int) -> void:
    for i in range(n):
        print(msg)

func my_signal_handler():
    print("The signal handler was called!")

func my_signal_with_params_handler(msg: String, n: int):
    print_n_times(msg, n)
```

Example 2 (swift):
```swift
using Godot;

public partial class MyCSharpNode : Node
{
    public string MyProperty { get; set; } = "my c# value";

    [Signal] public delegate void MySignalEventHandler();
    [Signal] public delegate void MySignalWithParamsEventHandler(string msg, int n);

    public void PrintNodeName(Node node)
    {
        GD.Print(node.Name);
    }

    public void PrintArray(string[] arr)
    {
        foreach (string element in arr)
        {
            GD.Print(element);
        }
    }

    public void PrintNTimes(string msg, int n)
    {
        for (int i = 0; i < n; ++i)
        {
            GD.Print(msg);
        }
    }

    public void MySignalHandler()
    {
        GD.Print("The signal handler was called!");
    }

    public void MySignalWithParamsHandler(string msg, int n)
    {
        PrintNTimes(msg, n);
    }
}
```

Example 3 (gdscript):
```gdscript
var MyCSharpScript = load("res://Path/To/MyCSharpNode.cs")
var my_csharp_node = MyCSharpScript.new()
```

Example 4 (gdscript):
```gdscript
var myGDScript = GD.Load<GDScript>("res://path/to/my_gd_script.gd");
var myGDScriptNode = (GodotObject)myGDScript.New(); // This is a GodotObject.
```

---

## Instancing with signals — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/instancing_with_signals.html

**Contents:**
- Instancing with signals
- Shooting example
- User-contributed notes

Signals provide a way to decouple game objects, allowing you to avoid forcing a fixed arrangement of nodes. One sign that a signal might be called for is when you find yourself using get_parent(). Referring directly to a node's parent means that you can't easily move that node to another location in the scene tree. This can be especially problematic when you are instancing objects at runtime and may want to place them in an arbitrary location in the running scene tree.

Below we'll consider an example of such a situation: firing bullets.

Consider a player character that can rotate and shoot towards the mouse. Every time the mouse button is clicked, we create an instance of the bullet at the player's location. See Creating instances for details.

We'll use an Area2D for the bullet, which moves in a straight line at a given velocity:

However, if the bullets are added as children of the player, then they will remain "attached" to the player as it rotates:

Instead, we need the bullets to be independent of the player's movement - once fired, they should continue traveling in a straight line and the player can no longer affect them. Instead of being added to the scene tree as a child of the player, it makes more sense to add the bullet as a child of the "main" game scene, which may be the player's parent or even further up the tree.

You could do this by adding the bullet to the main scene directly:

However, this will lead to a different problem. Now if you try to test your "Player" scene independently, it will crash on shooting, because there is no parent node to access. This makes it a lot harder to test your player code independently and also means that if you decide to change your main scene's node structure, the player's parent may no longer be the appropriate node to receive the bullets.

The solution to this is to use a signal to "emit" the bullets from the player. The player then has no need to "know" what happens to the bullets after that - whatever node is connected to the signal can "receive" the bullets and take the appropriate action to spawn them.

Here is the code for the player using signals to emit the bullet:

In the main scene, we then connect the player's signal (it will appear in the "Node" tab of the Inspector)

Now the bullets will maintain their own movement independent of the player's rotation:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Area2D

var velocity = Vector2.RIGHT

func _physics_process(delta):
    position += velocity * delta
```

Example 2 (csharp):
```csharp
using Godot;

public partial class Bullet : Area2D
{
    public Vector2 Velocity { get; set; } = Vector2.Right;

    public override void _PhysicsProcess(double delta)
    {
        Position += Velocity * (float)delta;
    }
}
```

Example 3 (gdscript):
```gdscript
var bullet_instance = Bullet.instantiate()
get_parent().add_child(bullet_instance)
```

Example 4 (unknown):
```unknown
Node bulletInstance = Bullet.Instantiate();
GetParent().AddChild(bulletInstance);
```

---

## Pausing games and process mode — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html

**Contents:**
- Pausing games and process mode
- Introduction
- How pausing works
- Process Modes
- Pause menu example
- User-contributed notes

In most games it is desirable to, at some point, interrupt the game to do something else, such as taking a break or changing options. Implementing a fine-grained control for what can be paused (and what cannot) is a lot of work, so a simple framework for pausing is provided in Godot.

To pause the game the pause state must be set. This is done by assigning true to the SceneTree.paused property:

Doing this will cause two things. First, 2D and 3D physics will be stopped for all nodes. Second, the behavior of certain nodes will stop or start depending on their process mode.

The physics servers can be made active while the game is paused by using their set_active methods.

Each node in Godot has a "Process Mode" that defines when it processes. It can be found and changed under a node's Node properties in the inspector.

You can also alter the property with code:

This is what each mode tells a node to do:

Inherit: Process depending on the state of the parent, grandparent, etc. The first parent that has a non-Inherit state.

Pausable: Process the node (and its children in Inherit mode) only when the game is not paused.

WhenPaused: Process the node (and its children in Inherit mode) only when the game is paused.

Always: Process the node (and its children in Inherit mode) no matter what. Paused or not, this node will process.

Disabled: The node (and its children in Inherit mode) will not process at all.

By default, all nodes have this property in the "Inherit" state. If the parent is set to "Inherit", then the grandparent will be checked and so on. If a state can't be found in any of the grandparents, the pause state in SceneTree is used. This means that, by default, when the game is paused every node will be paused. Several things happen when a node stops processing.

The _process, _physics_process, _input, and _input_event functions will not be called. However signals still work and cause their connected function to run, even if that function's script is attached to a node that is not currently being processed.

Animation nodes will pause their current animation, audio nodes will pause their current audio stream, and particles will pause. These resume automatically when the game is no longer paused.

It is important to note that even if a node is processing while the game is paused physics will NOT work for it by default. As stated earlier this is because the physics servers are turned off. The physics servers can be made active while the game is paused by using their set_active methods.

Start by creating a button that will be used to pause the game.

Create a menu containing a close button, set the Process Mode of the menu's root node to When Paused, then hide the menu. Since the process mode is set to When Paused on the root node, all its children and grandchildren will inherit that process mode. This way, all the nodes in the menu will start processing when the game is paused.

Attach a script to the menu's root node, connect the pause button created earlier to a new method in the script, and inside that method pause the game and show the pause menu.

Finally, connect the menu's close button to a new method in the script. Inside that method, unpause the game and hide the pause menu.

You should now have a working pause menu.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
get_tree().paused = true
```

Example 2 (unknown):
```unknown
GetTree().Paused = true;
```

Example 3 (gdscript):
```gdscript
func _ready():
    process_mode = Node.PROCESS_MODE_PAUSABLE
```

Example 4 (gdscript):
```gdscript
public override void _Ready()
{
    ProcessMode = Node.ProcessModeEnum.Pausable;
}
```

---

## Evaluating expressions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/evaluating_expressions.html

**Contents:**
- Evaluating expressions
- Basic usage
- Passing variables to an expression
- Setting a base instance for the expression
- Example script
- Built-in functions
- User-contributed notes

Godot provides an Expression class you can use to evaluate expressions.

An expression can be:

A mathematical expression such as (2 + 4) * 16/4.0.

A boolean expression such as true && false.

A built-in method call like deg_to_rad(90).

A method call on a user-provided script like update_health(), if base_instance is set to a value other than null when calling Expression.execute().

The Expression class is independent from GDScript. It's available even if you compile Godot with the GDScript module disabled.

To evaluate a mathematical expression, use:

The following operators are available:

Can also be used to concatenate strings and arrays: - "hello" + " world" = hello world - [1, 2] + [3, 4] = [1, 2, 3, 4]

Performs and integer division if both operands are integers. If at least one of them is a floating-point number, returns a floating-point value.

Returns the remainder of an integer division (modulo). The result will always have the sign of the dividend.

Returns the result of a boolean AND.

Returns the result of a boolean OR.

Returns the result of a boolean NOT.

Spaces around operators are optional. Also, keep in mind the usual order of operations applies. Use parentheses to override the order of operations if needed.

All the Variant types supported in Godot can be used: integers, floating-point numbers, strings, arrays, dictionaries, colors, vectors, …

Arrays and dictionaries can be indexed like in GDScript:

You can pass variables to an expression. These variables will then become available in the expression's "context" and will be substituted when used in the expression:

Both the variable names and variable values must be specified as an array, even if you only define one variable. Also, variable names are case-sensitive.

By default, an expression has a base instance of null. This means the expression has no base instance associated to it.

When calling Expression.execute(), you can set the value of the base_instance parameter to a specific object instance such as self, another script instance or even a singleton:

Associating a base instance allows doing the following:

Reference the instance's constants (const) in the expression.

Reference the instance's member variables (var) in the expression.

Call methods defined in the instance and use their return values in the expression.

Setting a base instance to a value other than null allows referencing constants, member variables, and calling all methods defined in the script attached to the instance. Allowing users to enter expressions may allow cheating in your game, or may even introduce security vulnerabilities if you allow arbitrary clients to run expressions on other players' devices.

The script below demonstrates what the Expression class is capable of:

The output from the script will be:

All methods in the Global Scope are available in the Expression class, even if no base instance is bound to the expression. The same parameters and return types are available.

However, unlike GDScript, parameters are always required even if they're specified as being optional in the class reference. In contrast, this restriction on arguments doesn't apply to user-made functions when you bind a base instance to the expression.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var expression = Expression.new()
expression.parse("20 + 10*2 - 5/2.0")
var result = expression.execute()
print(result)  # 37.5
```

Example 2 (json):
```json
# Returns 1.
[1, 2][0]

# Returns 3. Negative indices can be used to count from the end of the array.
[1, 3][-1]

# Returns "green".
{"favorite_color": "green"}["favorite_color"]

# All 3 lines below return 7.0 (Vector3 is floating-point).
Vector3(5, 6, 7)[2]
Vector3(5, 6, 7)["z"]
Vector3(5, 6, 7).z
```

Example 3 (gdscript):
```gdscript
var expression = Expression.new()
# Define the variable names first in the second parameter of `parse()`.
# In this example, we use `x` for the variable name.
expression.parse("20 + 2 * x", ["x"])
# Then define the variable values in the first parameter of `execute()`.
# Here, `x` is assigned the integer value 5.
var result = expression.execute([5])
print(result)  # 30
```

Example 4 (gdscript):
```gdscript
func double(number):
    return number * 2


func _ready():
    var expression = Expression.new()
    expression.parse("double(10)")

    # This won't work since we're not passing the current script as the base instance.
    var result = expression.execute([], null)
    print(result)  # null

    # This will work since we're passing the current script (i.e. self)
    # as the base instance.
    result = expression.execute([], self)
    print(result)  # 20
```

---

## Change scenes manually — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/change_scenes_manually.html

**Contents:**
- Change scenes manually
- User-contributed notes

Sometimes it helps to have more control over how you swap scenes around. A Viewport's child nodes will render to the image it generates. This holds true even for nodes outside of the "current" scene. Autoloads fall into this category, and also scenes which you instantiate and add to the tree at runtime:

To complete the cycle and swap out the new scene with the old one, you have a choice to make. Many strategies exist for removing a scene from view of the Viewport. The tradeoffs involve balancing operation speed and memory consumption, as well as balancing data access and integrity.

Delete the existing scene. SceneTree.change_scene_to_file() and SceneTree.change_scene_to_packed() will delete the current scene immediately. You can also delete the main scene. Assuming the root node's name is "Main", you could do get_node("/root/Main").free() to delete the whole scene.

Pro: RAM is no longer dragging the dead weight.

Con: Returning to that scene is now more expensive since it must be loaded back into memory again (takes time AND memory). Not a problem if returning soon is unnecessary.

Con: No longer have access to that scene's data. Not a problem if using that data soon is unnecessary.

Note: It can be useful to preserve the data in a soon-to-be-deleted scene by re-attaching one or more of its nodes to a different scene, or even directly to the SceneTree.

Pro: No nodes means no processing, physics processing, or input handling. The CPU is available to work on the new scene's contents.

Con: Those nodes' processing and input handling no longer operate. Not a problem if using the updated data is unnecessary.

Hide the existing scene. By changing the visibility or collision detection of the nodes, you can hide the entire node sub-tree from the player's perspective.

Pro: You can still access the data if needed.

Pro: There's no need to move any more nodes around to save data.

Con: More data is being kept in memory, which will be become a problem on memory-sensitive platforms like web or mobile.

Processing continues.

Pro: Data continues to receive processing updates, so the scene will keep any data within it that relies on delta time or frame data updated.

Pro: Nodes are still members of groups (since groups belong to the SceneTree).

Con: The CPU's attention is now divided between both scenes. Too much load could result in low frame rates. You should be sure to test performance as you go to ensure the target platform can support the load from this approach.

Remove the existing scene from the tree. Assign a variable to the existing scene's root node. Then use Node.remove_child(Node) to detach the entire scene from the tree.

Memory still exists (similar pros/cons as hiding it from view).

Processing stops (similar pros/cons as deleting it completely).

Pro: This variation of "hiding" it is much easier to show/hide. Rather than potentially keeping track of multiple changes to the scene, you only need to call the add/remove_child methods. This is similar to disabling game objects in other engines.

Con: Unlike with hiding it from view only, the data contained within the scene will become stale if it relies on delta time, input, groups, or other data that is derived from SceneTree access.

There are also cases where you may wish to have many scenes present at the same time, such as adding your own singleton at runtime, or preserving a scene's data between scene changes (adding the scene to the root node).

Another case may be displaying multiple scenes at the same time using SubViewportContainers. This is optimal for rendering different content in different parts of the screen (e.g. minimaps, split-screen multiplayer).

Each option will have cases where it is best appropriate, so you must examine the effects of each approach, and determine what path best fits your unique situation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var simultaneous_scene = preload("res://levels/level2.tscn").instantiate()

func _add_a_scene_manually():
    # This is like autoloading the scene, only
    # it happens after already loading the main scene.
    get_tree().root.add_child(simultaneous_scene)
```

Example 2 (json):
```json
public Node simultaneousScene;

public MyClass()
{
    simultaneousScene = ResourceLoader.Load<PackedScene>("res://levels/level2.tscn").Instantiate();
}

public void _AddASceneManually()
{
    // This is like autoloading the scene, only
    // it happens after already loading the main scene.
    GetTree().Root.AddChild(simultaneousScene);
}
```

Example 3 (unknown):
```unknown
get_tree().root.add_child(scene)
```

Example 4 (unknown):
```unknown
GetTree().Root.AddChild(scene);
```

---

## Creating script templates — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/creating_script_templates.html

**Contents:**
- Creating script templates
- Locating the templates
  - Editor-defined templates
  - Project-defined templates
  - Template organization and naming
- Default behavior and overriding it
- Default template
- List of template placeholders
  - Base placeholders
  - Type placeholders

Godot provides a way to use script templates as seen in the Script Create Dialog while creating a new script:

A set of built-in script templates are provided with the editor, but it is also possible to create new ones and set them by default, both per project and at editor scope.

Templates are linked to a specific node type, so when you create a script you will only see the templates corresponding to that particular node, or one of its parent types. For example, if you are creating a script for a CharacterBody3D, you will only see templates defined for CharacterBody3Ds, Node3Ds or Nodes.

There are two places where templates can be managed.

These are available globally throughout any project. The location of these templates are determined per each OS:

Windows: %APPDATA%\Godot\script_templates\

Linux: $HOME/.config/godot/script_templates/

macOS: $HOME/Library/Application Support/Godot/script_templates/

If you're getting Godot from somewhere other than the official website, such as Steam, the folder might be in a different location. You can find it using the Godot editor. Go to Editor > Open Editor Data/Settings Folder and it will open a folder in your file browser, inside that folder is the script_templates folder.

The default path to search for templates is the res://script_templates/ directory. The path can be changed by configuring the project setting Editor > Script > Templates Search Path, both via code and the editor.

If no script_templates directory is found within a project, it is simply ignored.

Both editor and project defined templates are organized in the following way:

template_path is one of the 2 locations discussed in the previous two sections.

node_type is the node it will apply to (for example, Node, or CharacterBody3D), This is case-sensitive. If a script isn't in the proper node_type folder, it won't be detected.

file is the custom name you can chose for the template (for example, platformer_movement or smooth_camera).

extension indicates which language the template will apply to (it should be gd for GDScript or cs for C#).

script_templates/Node/smooth_camera.gd

script_templates/CharacterBody3D/platformer_movement.gd

the template's name is the same as the file name (minus the extension, prettyfied)

the description is empty

the space indent is set to 4

the template will not be set as the default for the given node

It is possible to customize this behavior by adding meta headers at the start of your file, like this:

In this case, the name will be set to "Platformer movement", with the given custom description, and it will be set as the default template for the node in which directory it has been saved.

This is an example of utilizing custom templates at editor and project level:

The script templates have the same extension as the regular script files. This may lead to an issue of a script parser treating those templates as actual scripts within a project. To avoid this, make sure to ignore the directory containing them by creating an empty .gdignore file. The directory won't be visible throughout the project's filesystem anymore, yet the templates can be modified by an external text editor anytime.

By default, every C# file inside the project directory is included in the compilation. Script templates must be manually excluded from the C# project to avoid build errors. See Exclude files from the build in the Microsoft documentation.

It is possible to create editor-level templates that have the same level as a project-specific templates, and also that have the same name as a built-in one, all will be shown on the new script dialog.

To override the default template, create a custom template at editor or project level inside a Node directory (or a more specific type, if only a subtype wants to be overridden) and start the file with the meta-default: true header.

Only one template can be set as default at the same time for the same node type.

The Default templates for basic Nodes, for both GDScript and C#, are shown here so you can use these as the base for creating other templates:

The Godot editor provides a set of useful built-in node-specific templates, such as basic_movement for both CharacterBody2D and CharacterBody3D and plugin for EditorPlugin.

The following describes the complete list of built-in template placeholders which are currently implemented.

The name of the Godot namespace (used in C# only).

The name of the new class.

The name of the new class as snake_case (used in GDScript only).

The base type a new script inherits from.

Indentation placeholder. The exact type and number of whitespace characters used for indentation is determined by the text_editor/indent/type and text_editor/indent/size settings in the EditorSettings respectively. Can be overridden by the meta-space-indent header on the template.

There used to be, in Godot 3.x, placeholders for GDScript type hints that would get replaced whenever a template was used to create a new script, such as: %INT_TYPE%, %STRING_TYPE%, %FLOAT_TYPE% or %VOID_RETURN%.

The placeholders no longer work for Godot 4.x, but if the setting text_editor/completion/add_type_hints from EditorSettings is disabled, type hints for parameters and return types will be automatically removed for a few base types:

:= will be transformed into =

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
template_path/node_type/file.extension
```

Example 2 (markdown):
```markdown
# meta-name: Platformer movement
# meta-description: Predefined movement for classical platformers
# meta-default: true
# meta-space-indent: 4
```

Example 3 (json):
```json
// meta-name: Platformer movement
// meta-description: Predefined movement for classical platformers
// meta-default: true
// meta-space-indent: 4
```

Example 4 (gdscript):
```gdscript
# meta-description: Base template for Node with default Godot cycle methods

extends _BASE_


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
    pass
```

---

## File system — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/filesystem.html

**Contents:**
- File system
- Introduction
- Implementation
- project.godot
- Path delimiter
- Resource path
- User path
- Host file system
- Drawbacks
- User-contributed notes

A file system manages how assets are stored and how they are accessed. A well-designed file system also allows multiple developers to edit the same source files and assets while collaborating. Godot stores all assets as files in its file system.

The file system stores resources on disk. Anything, from a script, to a scene or a PNG image is a resource to the engine. If a resource contains properties that reference other resources on disk, the paths to those resources are also included. If a resource has sub-resources that are built-in, the resource is saved in a single file together with all the bundled sub-resources. For example, a font resource is often bundled together with the font textures.

The Godot file system avoids using metadata files. Existing asset managers and VCSs are better than anything we can implement, so Godot tries its best to play along with Subversion, Git, Mercurial, etc.

Example of file system contents:

The project.godot file is the project description file, and it is always found at the root of the project. In fact, its location defines where the root is. This is the first file that Godot looks for when opening a project.

This file contains the project configuration in plain text, using the win.ini format. Even an empty project.godot can function as a basic definition of a blank project.

Godot only supports / as a path delimiter. This is done for portability reasons. All operating systems support this, even Windows, so a path such as C:\project\project.godot needs to be typed as C:/project/project.godot.

When accessing resources, using the host OS file system layout can be cumbersome and non-portable. To solve this problem, the special path res:// was created.

The path res:// will always point at the project root (where project.godot is located, so res://project.godot is always valid).

This file system is read-write only when running the project locally from the editor. When exported or when running on different devices (such as phones or consoles, or running from DVD), the file system will become read-only and writing will no longer be permitted.

Writing to disk is still needed for tasks such as saving game state or downloading content packs. To this end, the engine ensures that there is a special path user:// that is always writable. This path resolves differently depending on the OS the project is running on. Local path resolution is further explained in File paths in Godot projects.

Alternatively host file system paths can also be used, but this is not recommended for a released product as these paths are not guaranteed to work on all platforms. However, using host file system paths can be useful when writing development tools in Godot.

There are some drawbacks to this file system design. The first issue is that moving assets around (renaming them or moving them from one path to another inside the project) will break existing references to these assets. These references will have to be re-defined to point at the new asset location.

To avoid this, do all your move, delete and rename operations from within Godot, on the FileSystem dock. Never move assets from outside Godot, or dependencies will have to be fixed manually (Godot detects this and helps you fix them anyway, but why go the hard route?).

The second is that, under Windows and macOS, file and path names are case insensitive. If a developer working in a case insensitive host file system saves an asset as myfile.PNG, but then references it as myfile.png, it will work fine on their platform, but not on other platforms, such as Linux, Android, etc. This may also apply to exported binaries, which use a compressed package to store all files.

It is recommended that your team clearly define a naming convention for files when working with Godot. One fool-proof convention is to only allow lowercase file and path names.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
/project.godot
/enemy/enemy.tscn
/enemy/enemy.gd
/enemy/enemysprite.png
/player/player.gd
```

---

## Resources — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html

**Contents:**
- Resources
- Nodes and resources
- External vs built-in
- Loading resources from code
- Loading scenes
- Freeing resources
- Creating your own resources
- User-contributed notes

Up to this tutorial, we focused on the Node class in Godot as that's the one you use to code behavior and most of the engine's features rely on it. There is another datatype that is just as important: Resource.

Nodes give you functionality: they draw sprites, 3D models, simulate physics, arrange user interfaces, etc. Resources are data containers. They don't do anything on their own: instead, nodes use the data contained in resources.

Anything Godot saves or loads from disk is a resource. Be it a scene (a .tscn or a .scn file), an image, a script... Here are some Resource examples:

When the engine loads a resource from disk, it only loads it once. If a copy of that resource is already in memory, trying to load the resource again will return the same copy every time. As resources only contain data, there is no need to duplicate them.

Every object, be it a Node or a Resource, can export properties. There are many types of Properties, like String, integer, Vector2, etc., and any of these types can become a resource. This means that both nodes and resources can contain resources as properties:

There are two ways to save resources. They can be:

External to a scene, saved on the disk as individual files.

Built-in, saved inside the .tscn or the .scn file they're attached to.

To be more specific, here's a Texture2D in a Sprite2D node:

Clicking the resource preview allows us to view the resource's properties.

The path property tells us where the resource comes from. In this case, it comes from a PNG image called robi.png. When the resource comes from a file like this, it is an external resource. If you erase the path or this path is empty, it becomes a built-in resource.

The switch between built-in and external resources happens when you save the scene. In the example above, if you erase the path "res://robi.png" and save, Godot will save the image inside the .tscn scene file.

Even if you save a built-in resource, when you instance a scene multiple times, the engine will only load one copy of it.

There are two ways to load resources from code. First, you can use the load() function anytime:

You can also preload resources. Unlike load, this function will read the file from disk and load it at compile-time. As a result, you cannot call preload with a variable path: you need to use a constant string.

Scenes are also resources, but there is a catch. Scenes saved to disk are resources of type PackedScene. The scene is packed inside a Resource.

To get an instance of the scene, you have to use the PackedScene.instantiate() method.

This method creates the nodes in the scene's hierarchy, configures them, and returns the root node of the scene. You can then add it as a child of any other node.

The approach has several advantages. As the PackedScene.instantiate() function is fast, you can create new enemies, bullets, effects, etc. without having to load them again from disk each time. Remember that, as always, images, meshes, etc. are all shared between the scene instances.

When a Resource is no longer in use, it will automatically free itself. Since, in most cases, Resources are contained in Nodes, when you free a node, the engine frees all the resources it owns as well if no other node uses them.

Like any Object in Godot, users can also script Resources. Resource scripts inherit the ability to freely translate between object properties and serialized text or binary data (*.tres, *.res). They also inherit the reference-counting memory management from the RefCounted type.

This comes with many distinct advantages over alternative data structures, such as JSON, CSV, or custom TXT files. Users can only import these assets as a Dictionary (JSON) or as a FileAccess to parse. What sets Resources apart is their inheritance of Object, RefCounted, and Resource features:

They can define constants, so constants from other data fields or objects are not needed.

They can define methods, including setter/getter methods for properties. This allows for abstraction and encapsulation of the underlying data. If the Resource script's structure needs to change, the game using the Resource need not also change.

They can define signals, so Resources can trigger responses to changes in the data they manage.

They have defined properties, so users know 100% that their data will exist.

Resource auto-serialization and deserialization is a built-in Godot Engine feature. Users do not need to implement custom logic to import/export a resource file's data.

Resources can even serialize sub-Resources recursively, meaning users can design even more sophisticated data structures.

Users can save Resources as version-control-friendly text files (*.tres). Upon exporting a game, Godot serializes resource files as binary files (*.res) for increased speed and compression.

Godot Engine's Inspector renders and edits Resource files out-of-the-box. As such, users often do not need to implement custom logic to visualize or edit their data. To do so, double-click the resource file in the FileSystem dock or click the folder icon in the Inspector and open the file in the dialog.

They can extend other resource types besides just the base Resource.

Godot makes it easy to create custom Resources in the Inspector.

Create a new Resource object in the Inspector. This can even be a type that derives Resource, so long as your script is extending that type.

Set the script property in the Inspector to be your script.

The Inspector will now display your Resource script's custom properties. If one edits those values and saves the resource, the Inspector serializes the custom properties too! To save a resource from the Inspector, click the save icon at the top of the Inspector, and select "Save" or "Save As...".

If the script's language supports script classes, then it streamlines the process. Defining a name for your script alone will add it to the Inspector's creation dialog. This will auto-add your script to the Resource object you create.

Let's see some examples. Create a Resource and name it bot_stats. It should appear in your file tab with the full name bot_stats.tres. Without a script, it's useless, so let's add some data and logic! Attach a script to it named bot_stats.gd (or just create a new script, and then drag it to it).

To make the new resource class appear in the Create Resource GUI you need to provide a class name for GDScript, or use the [GlobalClass] attribute in C#.

Now, create a CharacterBody3D, name it Bot, and add the following script to it:

Now, select the CharacterBody3D node which we named bot, and drag&drop the bot_stats.tres resource onto the Inspector. It should print 10! Obviously, this setup can be used for more advanced features than this, but as long you really understand how it all worked, you should figure out everything else related to Resources.

Resource scripts are similar to Unity's ScriptableObjects. The Inspector provides built-in support for custom resources. If desired though, users can even design their own Control-based tool scripts and combine them with an EditorPlugin to create custom visualizations and editors for their data.

Unreal Engine's DataTables and CurveTables are also easy to recreate with Resource scripts. DataTables are a String mapped to a custom struct, similar to a Dictionary mapping a String to a secondary custom Resource script.

Instead of inlining the Dictionary values, one could also, alternatively:

Import a table of values from a spreadsheet and generate these key-value pairs.

Design a visualization within the editor and create a plugin that adds it to the Inspector when you open these types of Resources.

CurveTables are the same thing, except mapped to an Array of float values or a Curve/Curve2D resource object.

Beware that resource files (*.tres/*.res) will store the path of the script they use in the file. When loaded, they will fetch and load this script as an extension of their type. This means that trying to assign an inner class of a script (i.e. using the class keyword in GDScript) won't work. Godot will not serialize the custom properties on the script inner class properly.

In the example below, Godot would load the Node script, see that it doesn't extend Resource, and then determine that the script failed to load for the Resource object since the types are incompatible.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _ready():
    # Godot loads the Resource when it reads this very line.
    var imported_resource = load("res://robi.png")
    $sprite.texture = imported_resource
```

Example 2 (gdscript):
```gdscript
public override void _Ready()
{
    // Godot loads the Resource when it executes this line.
    var texture = GD.Load<Texture>("res://Robi.png");
    var sprite = GetNode<Sprite2D>("sprite");
    sprite.Texture = texture;
}
```

Example 3 (gdscript):
```gdscript
func _ready():
    # Godot loads the resource at compile-time
    var imported_resource = preload("res://robi.png")
    get_node("sprite").texture = imported_resource
```

Example 4 (unknown):
```unknown
// 'preload()' is unavailable in C Sharp.
```

---

## Using SceneTree — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html

**Contents:**
- Using SceneTree
- Introduction
- MainLoop
- SceneTree
- Root viewport
- Scene tree
- Tree order
- "Becoming active" by entering the Scene Tree
- Changing current scene
- User-contributed notes

In previous tutorials, everything revolved around the concept of nodes. Scenes are collections of nodes. They become active once they enter the scene tree.

The way Godot works internally is as follows. There is the OS class, which is the only instance that runs at the beginning. Afterwards, all drivers, servers, scripting languages, scene system, etc are loaded.

When initialization is complete, OS needs to be supplied a MainLoop to run. Up to this point, all this is internals working (you can check main/main.cpp file in the source code if you are ever interested to see how this works internally).

The user program, or game, starts in the MainLoop. This class has a few methods, for initialization, idle (frame-synchronized callback), fixed (physics-synchronized callback), and input. Again, this is low level and when making games in Godot, writing your own MainLoop seldom makes sense.

One of the ways to explain how Godot works is that it's a high-level game engine over a low-level middleware.

The scene system is the game engine, while the OS and servers are the low-level API.

The scene system provides its own main loop to OS, SceneTree. This is automatically instanced and set when running a scene, no need to do any extra work.

It's important to know that this class exists because it has a few important uses:

It contains the root Viewport, to which a scene is added as a child when it's first opened to become part of the Scene Tree (more on that next).

It contains information about the groups and has the means to call all nodes in a group or get a list of them.

It contains some global state functionality, such as setting pause mode or quitting the process.

When a node is part of the Scene Tree, the SceneTree singleton can be obtained by calling Node.get_tree().

The root Viewport is always at the top of the scene. From a node, it can be obtained in two different ways:

This node contains the main viewport. Anything that is a child of a Viewport is drawn inside of it by default, so it makes sense that the top of all nodes is always a node of this type otherwise nothing would be seen.

While other viewports can be created in the scene (for split-screen effects and such), this one is the only one that is never created by the user. It's created automatically inside SceneTree.

When a node is connected, directly or indirectly, to the root viewport, it becomes part of the scene tree.

This means that as explained in previous tutorials, it will get the _enter_tree() and _ready() callbacks (as well as _exit_tree()).

When nodes enter the Scene Tree, they become active. They get access to everything they need to process, get input, display 2D and 3D visuals, receive and send notifications, play sounds, etc. When they are removed from the scene tree, they lose these abilities.

Most node operations in Godot, such as drawing 2D, processing, or getting notifications are done in tree order, or top to bottom as seen in the editor (also known as pre-order traversal):

For example, the top node in a scene has its _process() function called first, then the node below it has its _process() function called, then the node below that and so on.

An important exception is the _ready() function: each parent node has its _ready() function called only after all its child nodes have their _ready() functions called, so that the parent knows its children are completely ready to be accessed. This is also known as post-order traversal. In the above image, NameLabel would be notified first (but only after its children, if it had any!), followed by Name, etc., and Panel would be notified last.

The order of operations can also be overridden using the process_priority node property. Nodes with a lower number are called first. For example, nodes with the priorities "0, 1, 2, 3" would be called in that order from left to right.

A scene is loaded from disk or created by scripting.

The root node of that scene (only one root, remember?) is added as either a child of the "root" Viewport (from SceneTree), or to any of its descendants.

Every node of the newly added scene will receive the "enter_tree" notification ( _enter_tree() callback in GDScript) in top-to-bottom order (pre-order traversal).

Every node will receive the "ready" notification ( _ready() callback in GDScript) for convenience, once all its children have received the "ready" notification (post-order traversal).

When a scene (or part of it) is removed, they receive the "exit scene" notification ( _exit_tree() callback in GDScript) in bottom-to-top order (the exact reverse of top-to-bottom order).

After a scene is loaded, you may want to change this scene for another one. One way to do this is to use the SceneTree.change_scene_to_file() function:

Rather than using file paths, one can also use ready-made PackedScene resources using the equivalent function SceneTree.change_scene_to_packed(PackedScene scene):

These are quick and useful ways to switch scenes but have the drawback that the game will stall until the new scene is loaded and running. At some point in the development of your game, it may be preferable to create proper loading screens with progress bar, animated indicators or threaded (background) loading. This must be done manually using Singletons (Autoload) and Background loading.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
get_tree().root # Access via scene main loop.
get_node("/root") # Access via absolute path.
```

Example 2 (unknown):
```unknown
GetTree().Root // Access via scene main loop.
GetNode("/root"); // Access via absolute path.
```

Example 3 (go):
```go
func _my_level_was_completed():
    get_tree().change_scene_to_file("res://levels/level2.tscn")
```

Example 4 (json):
```json
public void _MyLevelWasCompleted()
{
    GetTree().ChangeSceneToFile("res://levels/level2.tscn");
}
```

---

## Logging — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/logging.html

**Contents:**
- Logging
- Printing messages
- Project settings
- Built-in file logging
- Script backtraces
- Crash backtraces
- Creating custom loggers
- User-contributed notes

Godot comes with several ways to organize and collect log messages.

See Printing messages for instructions on printing messages. The printed output is generally identical to the logged output.

When running a project from the editor, the editor will display logged text in the Output panel.

There are several project settings to control logging behavior in Godot:

Application > Run > Disable stdout: Disables logging to standard output entirely. This also affects what custom loggers receive. This can be controlled at runtime by setting Engine.print_to_stdout.

Application > Run > Disable stderr: Disables logging to standard error entirely. This also affects what custom loggers receive. This can be controlled at runtime by setting Engine.print_error_messages.

Debug > Settings > stdout > Verbose stdout: Enables verbose logging to standard output. Prints from print_verbose() are only visible if verbose mode is enabled.

Debug > Settings > stdout > Print FPS: Prints the frames per second every second, as well as the V-Sync status on startup (as it can effectively cap the maximum framerate).

Debug > Settings > stdout > Print GPU Profile: Prints a report of GPU utilization every second, using the same data source as the Visual Profiler.

Some of these project settings can also be overridden using command line arguments such as --quiet, --verbose, and --print-fps.

The engine's own file logging is also configurable, as described in the section below.

By default, Godot writes log files in user://logs/godot.log on desktop platforms. You can change this location by modifying the debug/file_logging/log_path project setting. Logs are rotated to keep older files available for inspection. Each session creates a new log file, with the old file renamed to contain the date at which it was rotated. Up to 5 log files are kept by default, which can be adjusted using the debug/file_logging/max_log_files project setting.

File logging can also be disabled completely using the debug/file_logging/enable_file_logging project setting.

When the project crashes, crash logs are written to the same file as the log file. The crash log will only contain a usable backtrace if the binary that was run contains debugging symbols, or if it can find a debug symbols file that matches the binary. Official binaries don't provide debugging symbols, so this requires a custom build to work. See Debugging symbols for guidance on compiling binaries with debugging symbols enabled.

Log files for print() statements are updated when standard output is flushed by the engine. Standard output is flushed on every print in debug builds only. In projects that are exported in release mode, standard output is only flushed when the project exits or crashes to improve performance, especially if the project is often printing text to standard output.

On the other hand, the standard error stream (used by printerr(), push_error(), and push_warning()) is always flushed on every print, even in projects exported in release mode.

For some use cases like dedicated servers, it can be preferred to have release builds always flush stdout on print, so that logging services like journald can collect logs while the process is running. This can be done by enabling application/run/flush_stdout_on_print in the Project Settings.

Since Godot 4.5, when GDScript code encounters an error, it will log a backtrace that points to the origin of the error, while also containing the call stack leading to it. This behavior is always enabled when running in the editor, or when the project is exported in debug mode.

In projects exported in release mode, backtraces are disabled by default for performance reasons. You can enable them by checking Debug > Settings > GDScript > Always Track Call Stacks in the Project Settings. If you use a custom logging system that reports exceptions to a remote service, it's recommended to enable this to make reported errors more actionable.

Crash backtraces are only useful if they were recorded in a build that contains debugging symbols. Official Godot binaries do not contain debugging symbols, so you must compile a custom editor or export template binary to get useful crash backtraces.

When the project crashes, a crash backtrace is printed to the standard error stream. This is what it can look like in a build with debug symbols:

On the other hand, without debug symbols, it will look like this instead:

This backtrace is also logged to the file for the current session, but it is not visible in the editor Output panel. Since the engine's scripting system is not running anymore when the engine is crashing, it is not possible to access it from scripting in the same session. However, you can still read the crash backtrace on the next session by loading log files and searching for the crash backtrace string (Program crashed with signal) using FileAccess. This allows you to access the backtrace information even after a crash, as long as the user restarts the project and file logging is enabled:

You can customize the message that appears at the top of the backtrace using the Debug > Settings > Crash Handler > Message project setting. This can be used to point to a URL or email address that users can report issues to.

Since Godot 4.5, it is possible to create custom loggers. This custom logging can be used for many purposes:

Show an in-game console with the same messages as printed by the engine, without requiring other scripts to be modified.

Report printed errors from the player's machine to a remote server. This can make it easier for developers to fix bugs when the game is already released, or during playtesting.

Integrate a dedicated server export with monitoring platforms.

A custom logger can be registered by creating a class that inherits from Logger, then passing an instance of this class to OS.add_logger, in a script's _init() method. A good place to do this is an autoload.

The class must define two methods: _log_message() and _log_error().

Here is a minimal working example of a custom logger, with the script added as an autoload:

Note that to avoid infinite recursion, you cannot effectively use print() and its related methods in _log_message(). You also can't effectively use push_error() or push_warning() in _log_error(). Attempting to do so will print a message to the same stream as the original message. This message is not available in the custom logger, which is what prevents infinite recursion from occurring:

You can find an example of an in-game console built with a custom logger in the Custom Logging demo project.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
================================================================
handle_crash: Program crashed with signal 4
Engine version: Godot Engine v4.5.beta.custom_build (6c9aa4c7d3b9b91cd50714c40eeb234874df7075)
Dumping the backtrace. Please include this when reporting the bug to the project developer.
[1] /lib64/libc.so.6(+0x1a070) [0x7f6e5e277070] (??:0)
[2] godot() [0x4da3358] (/path/to/godot/core/core_bind.cpp:336 (discriminator 2))
[3] godot() [0xdf5f2f] (/path/to/godot/modules/gdscript/gdscript.h:591)
[4] godot() [0xbffd46] (/path/to/godot/modules/gdscript/gdscript.cpp:2065 (discriminator 1))
[5] godot() [0x30f2ea4] (/path/to/godot/core/variant/variant.h:870)
[6] godot() [0x550d4e1] (/path/to/godot/core/object/object.cpp:933)
[7] godot() [0x30d996a] (/path/to/godot/scene/main/node.cpp:318 (discriminator 1))
[8] godot() [0x3131a7f] (/path/to/godot/core/templates/hash_map.h:465)
[9] godot() [0x424589] (/path/to/godot/platform/linuxbsd/os_linuxbsd.cpp:970)
[10] /lib64/libc.so.6(+0x3575) [0x7f6e5e260575] (??:0)
[11] /lib64/libc.so.6(__libc_start_main+0x88) [0x7f6e5e260628] (??:0)
[12] godot() [0x464df5] (??:?)
-- END OF C++ BACKTRACE --
================================================================
GDScript backtrace (most recent call first):
    [0] _ready (res://test.gd:5)
-- END OF GDSCRIPT BACKTRACE --
================================================================
```

Example 2 (swift):
```swift
================================================================
handle_crash: Program crashed with signal 4
Engine version: Godot Engine v4.5.beta.custom_build (6c9aa4c7d3b9b91cd50714c40eeb234874df7075)
Dumping the backtrace. Please include this when reporting the bug to the project developer.
[1] /lib64/libc.so.6(+0x1a070) [0x7fdfaf666070] (??:0)
[2] godot() [0x4da3358] (??:0)
[3] godot() [0xdf5f2f] (??:0)
[4] godot() [0xbffd46] (??:0)
[5] godot() [0x30f2ea4] (??:0)
[6] godot() [0x550d4e1] (??:0)
[7] godot() [0x30d996a] (??:0)
[8] godot() [0x3131a7f] (??:0)
[9] godot() [0x424589] (??:0)
[10] /lib64/libc.so.6(+0x3575) [0x7fdfaf64f575] (??:0)
[11] /lib64/libc.so.6(__libc_start_main+0x88) [0x7fdfaf64f628] (??:0)
[12] godot() [0x464df5] (??:0)
-- END OF C++ BACKTRACE --
================================================================
GDScript backtrace (most recent call first):
    [0] _ready (res://test.gd:5)
-- END OF GDSCRIPT BACKTRACE --
================================================================
```

Example 3 (gdscript):
```gdscript
# This script can be made an autoload, so that it runs when the project starts.
extends Node

func _ready() -> void:
  var log_dir: String = String(ProjectSettings.get_setting("debug/file_logging/log_path")).get_base_dir()
  # Get the last log file by alphabetical order.
  # Since the timestamp is featured in the file name, it should always be the most recent
  # log file that was rotated. The non-timestamped log file is for the current session,
  # so we don't want to read that one.
  var last_log_file: String = log_dir.path_join(DirAccess.get_files_at(log_dir)[-1])
  var last_long_contents: String = FileAccess.get_file_as_string(last_log_file)

  var crash_begin_idx: int = last_long_contents.find("Program crashed with signal")
  if crash_begin_idx != -1:
      print("The previous session has crashed with the following backtrace:\n")
      print(last_long_contents.substr(crash_begin_idx))
```

Example 4 (gdscript):
```gdscript
extends Node

class CustomLogger extends Logger:
    # Note that this method is not called for messages that use
    # `push_error()` and `push_warning()`, even though these are printed to stderr.
    func _log_message(message: String, error: bool) -> void:
        # Do something with `message`.
        # `error` is `true` for messages printed to the standard error stream (stderr) with `print_error()`.
        # Note that this method will be called from threads other than the main thread, possibly at the same
        # time, so you will need to have some kind of thread-safety as part of it, like a Mutex.
        pass

    func _log_error(
            function: String,
            file: String,
            line: int,
            code: String,
            rationale: String,
            editor_notify: bool,
            error_type: int,
            script_backtraces: Array[ScriptBacktrace]
    ) -> void:
        # Do something with the error. The error text is in `rationale`.
        # See the Logger class reference for details on other parameters.
        # Note that this method will be called from threads other than the main thread, possibly at the same
        # time, so you will need to have some kind of thread-safety as part of it, like a Mutex.
        pass

# Use `_init()` to initialize the logger as early as possible, which ensures that messages
# printed early are taken into account. However, even when using `_init()`, the engine's own
# initialization messages are not accessible.
func _init() -> void:
    OS.add_logger(CustomLogger.new())
```

---

## Scene Unique Nodes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/scene_unique_nodes.html

**Contents:**
- Scene Unique Nodes
- Introduction
- Creation and usage
- Same-scene limitation
- Alternatives
- User-contributed notes

Using get_node() to reference nodes from a script can sometimes be fragile. If you move a button in a UI scene from one panel to another, the button's node path changes, and if a script uses get_node() with a hard-coded node path, the script will not be able to find the button anymore.

In situations like this, the node can be turned into a scene unique node to avoid having to update the script every time the node's path is changed.

There are two ways to create a scene unique node.

In the Scene tree dock, right-click on a node and select Access as Unique Name in the context menu.

After selecting the option, the node will now have a percent symbol (%) next to its name in the scene tree:

You can also do this while renaming the node by adding "%" to the beginning of the name. Once you confirm, the percent symbol will appear next to its name.

You can now use the node in your script. For example, you can reference it with a get_node() method call by typing the % symbol, followed by the node's name:

A scene unique node can only be retrieved by a node inside the same scene. To demonstrate this limitation, consider this example Player scene that instances a Sword scene:

Here are the results of get_node() calls inside the Player script:

get_node("%Eyes") returns the Eyes node.

get_node("%Hilt") returns null.

These are the results of get_node() calls inside the Sword script:

get_node("%Eyes") returns null.

get_node("%Hilt") returns the Hilt node.

If a script has access to a node in another scene, it can call get_node() on that node to get scene unique nodes from that node's scene. This also works in a node path, which avoids multiple get_node() calls. Here are two ways to get the Hilt node from the Player script using scene unique nodes:

get_node("Hand/Sword").get_node("%Hilt") returns the Hilt node.

get_node("Hand/Sword/%Hilt") also returns the Hilt node.

Scene unique names don't only work at the end of a node path. They can be used in the middle to navigate from one node to another. For example, the Sword node is marked as a scene unique node in the Player scene, so this is possible:

get_node("%Sword/%Hilt") returns the Hilt node.

Scene unique nodes are a useful tool to navigate a scene. However, there are some situations where other techniques may be better.

A Group allows locating a node (or a group of many nodes) from any other node, no matter what scene the two nodes are located in.

A Singleton (Autoload) is an always loaded node that can be accessed directly by any node regardless of the scene. These are useful when some data or functionality is shared globally.

Node.find_child() finds a node by name without knowing its full path. This seems similar to a scene unique node, but this method is able to find nodes in nested scenes, and doesn't require marking the node in the scene editor in any way. However, this method is slow. Scene unique nodes are cached by Godot and are fast to retrieve, but each time the method is called, find_child() needs to check every descendant (every child, grandchild, and so on).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
get_node("%RedButton").text = "Hello"
%RedButton.text = "Hello" # Shorter syntax
```

Example 2 (typescript):
```typescript
GetNode<Button>("%RedButton").Text = "Hello";
```

---

## Singletons (Autoload) — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html

**Contents:**
- Singletons (Autoload)
- Introduction
- Autoload
- Custom scene switcher
  - Creating the script
- User-contributed notes

Godot's scene system, while powerful and flexible, has a drawback: there is no method for storing information (e.g. a player's score or inventory) that is needed by more than one scene.

It's possible to address this with some workarounds, but they come with their own limitations:

You can use a "master" scene that loads and unloads other scenes as its children. However, this means you can no longer run those scenes individually and expect them to work correctly.

Information can be stored to disk in user:// and then loaded by scenes that require it, but frequently saving and loading data is cumbersome and may be slow.

The Singleton pattern is a useful tool for solving the common use case where you need to store persistent information between scenes. In our case, it's possible to reuse the same scene or class for multiple singletons as long as they have different names.

Using this concept, you can create objects that:

Are always loaded, no matter which scene is currently running.

Can store global variables such as player information.

Can handle switching scenes and between-scene transitions.

Act like a singleton, since GDScript does not support global variables by design.

Autoloading nodes and scripts can give us these characteristics.

Godot won't make an Autoload a "true" singleton as per the singleton design pattern. It may still be instanced more than once by the user if desired.

If you're creating an autoload as part of an editor plugin, consider registering it automatically in the Project Settings when the plugin is enabled.

You can create an Autoload to load a scene or a script that inherits from Node.

When autoloading a script, a Node will be created and the script will be attached to it. This node will be added to the root viewport before any other scenes are loaded.

To autoload a scene or script, start from the menu and navigate to Project > Project Settings > Globals > Autoload.

Here you can add any number of scenes or scripts. Each entry in the list requires a name, which is assigned as the node's name property. The order of the entries as they are added to the global scene tree can be manipulated using the up/down arrow keys. Like regular scenes, the engine will read these nodes in top-to-bottom order.

If the Enable column is checked (which is the default), then the singleton can be accessed directly in GDScript:

The Enable column has no effect in C# code. However, if the singleton is a C# script, a similar effect can be achieved by including a static property called Instance and assigning it in _Ready():

This allows the singleton to be accessed from C# code without GetNode() and without a typecast:

Note that autoload objects (scripts and/or scenes) are accessed just like any other node in the scene tree. In fact, if you look at the running scene tree, you'll see the autoloaded nodes appear:

Autoloads must not be removed using free() or queue_free() at runtime, or the engine will crash.

This tutorial will demonstrate building a scene switcher using autoloads. For basic scene switching, you can use the SceneTree.change_scene_to_file() method (see Using SceneTree for details). However, if you need more complex behavior when changing scenes, this method provides more functionality.

To begin, download the template from here: singleton_autoload_starter.zip and open it in Godot.

A window notifying you that the project was last opened in an older Godot version may appear, that's not an issue. Click Ok to open the project.

The project contains two scenes: scene_1.tscn and scene_2.tscn. Each scene contains a label displaying the scene name and a button with its pressed() signal connected. When you run the project, it starts in scene_1.tscn. However, pressing the button does nothing.

Open the Script window and create a new script called global.gd. Make sure it inherits from Node:

The next step is to add this script to the autoLoad list. Starting from the menu, open Project > Project Settings > Globals > Autoload and select the script by clicking the browse button or typing its path: res://global.gd. Press Add to add it to the autoload list and name it "Global", which is required for scripts to access it by the name "Global":

Now whenever we run any scene in the project, this script will always be loaded.

Returning to the script, it needs to fetch the current scene in the _ready() function. Both the current scene (the one with the button) and global.gd are children of root, but autoloaded nodes are always first. This means that the last child of root is always the loaded scene.

Now we need a function for changing the scene. This function needs to free the current scene and replace it with the requested one.

Using Object.call_deferred(), the second function will only run once all code from the current scene has completed. Thus, the current scene will not be removed while it is still being used (i.e. its code is still running).

Finally, we need to fill the empty callback functions in the two scenes:

Run the project and test that you can switch between scenes by pressing the button.

When scenes are small, the transition is instantaneous. However, if your scenes are more complex, they may take a noticeable amount of time to appear. To learn how to handle this, see the next tutorial: Background loading.

Alternatively, if the loading time is relatively short (less than 3 seconds or so), you can display a "loading plaque" by showing some kind of 2D element just before changing the scene. You can then hide it just after the scene is changed. This can be used to indicate to the player that a scene is being loaded.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
PlayerVariables.health -= 10
```

Example 2 (csharp):
```csharp
public partial class PlayerVariables : Node
{
    public static PlayerVariables Instance { get; private set; }

    public int Health { get; set; }

    public override void _Ready()
    {
        Instance = this;
    }
}
```

Example 3 (unknown):
```unknown
PlayerVariables.Instance.Health -= 10;
```

Example 4 (gdscript):
```gdscript
extends Node

var current_scene = null

func _ready():
    var root = get_tree().root
    # Using a negative index counts from the end, so this gets the last child node of `root`.
    current_scene = root.get_child(-1)
```

---

## @GDScript — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_%40gdscript.html

**Contents:**
- @GDScript
- Description
- Tutorials
- Methods
- Constants
- Annotations
- Method Descriptions
- User-contributed notes

Built-in GDScript constants, functions, and annotations.

A list of utility functions and annotations accessible from any script written in GDScript.

For the list of global functions and constants that can be accessed in any scripting language, see @GlobalScope.

Color8(r8: int, g8: int, b8: int, a8: int = 255)

assert(condition: bool, message: String = "")

convert(what: Variant, type: Variant.Type)

dict_to_inst(dictionary: Dictionary)

inst_to_dict(instance: Object)

is_instance_of(value: Variant, type: Variant)

preload(path: String)

print_debug(...) vararg

type_exists(type: StringName)

PI = 3.14159265358979 🔗

Constant that represents how many times the diameter of a circle fits around its perimeter. This is equivalent to TAU / 2, or 180 degrees in rotations.

TAU = 6.28318530717959 🔗

The circle constant, the circumference of the unit circle in radians. This is equivalent to PI * 2, or 360 degrees in rotations.

Positive floating-point infinity. This is the result of floating-point division when the divisor is 0.0. For negative infinity, use -INF. Dividing by -0.0 will result in negative infinity if the numerator is positive, so dividing by 0.0 is not the same as dividing by -0.0 (despite 0.0 == -0.0 returning true).

Warning: Numeric infinity is only a concept with floating-point numbers, and has no equivalent for integers. Dividing an integer number by 0 will not result in INF and will result in a run-time error instead.

"Not a Number", an invalid floating-point value. It is returned by some invalid operations, such as dividing floating-point 0.0 by 0.0.

NAN has special properties, including that != always returns true, while other comparison operators always return false. This is true even when comparing with itself (NAN == NAN returns false and NAN != NAN returns true). Due to this, you must use @GlobalScope.is_nan() to check whether a number is equal to NAN.

Warning: "Not a Number" is only a concept with floating-point numbers, and has no equivalent for integers. Dividing an integer 0 by 0 will not result in NAN and will result in a run-time error instead.

Marks a class or a method as abstract.

An abstract class is a class that cannot be instantiated directly. Instead, it is meant to be inherited by other classes. Attempting to instantiate an abstract class will result in an error.

An abstract method is a method that has no implementation. Therefore, a newline or a semicolon is expected after the function header. This defines a contract that inheriting classes must conform to, because the method signature must be compatible when overriding.

Inheriting classes must either provide implementations for all abstract methods, or the inheriting class must be marked as abstract. If a class has at least one abstract method (either its own or an unimplemented inherited one), then it must also be marked as abstract. However, the reverse is not true: an abstract class is allowed to have no abstract methods.

Mark the following property as exported (editable in the Inspector dock and saved to disk). To control the type of the exported property, use the type hint notation.

Note: Custom resources and nodes should be registered as global classes using class_name, since the Inspector currently only supports global classes. Otherwise, a less specific type will be exported instead.

Note: Node export is only supported in Node-derived classes and has a number of other limitations.

@export_category(name: String) 🔗

Define a new category for the following exported properties. This helps to organize properties in the Inspector dock.

See also @GlobalScope.PROPERTY_USAGE_CATEGORY.

Note: Categories in the Inspector dock's list usually divide properties coming from different classes (Node, Node2D, Sprite, etc.). For better clarity, it's recommended to use @export_group and @export_subgroup, instead.

@export_color_no_alpha() 🔗

Export a Color, Array[Color], or PackedColorArray property without allowing its transparency (Color.a) to be edited.

See also @GlobalScope.PROPERTY_HINT_COLOR_NO_ALPHA.

@export_custom(hint: PropertyHint, hint_string: String, usage: BitField[PropertyUsageFlags] = 6) 🔗

Allows you to set a custom hint, hint string, and usage flags for the exported property. Note that there's no validation done in GDScript, it will just pass the parameters to the editor.

Note: Regardless of the usage value, the @GlobalScope.PROPERTY_USAGE_SCRIPT_VARIABLE flag is always added, as with any explicitly declared script variable.

Export a String, Array[String], or PackedStringArray property as a path to a directory. The path will be limited to the project folder and its subfolders. See @export_global_dir to allow picking from the entire filesystem.

See also @GlobalScope.PROPERTY_HINT_DIR.

@export_enum(names: String, ...) vararg 🔗

Export an int, String, Array[int], Array[String], PackedByteArray, PackedInt32Array, PackedInt64Array, or PackedStringArray property as an enumerated list of options (or an array of options). If the property is an int, then the index of the value is stored, in the same order the values are provided. You can add explicit values using a colon. If the property is a String, then the value is stored.

See also @GlobalScope.PROPERTY_HINT_ENUM.

If you want to set an initial value, you must specify it explicitly:

If you want to use named GDScript enums, then use @export instead:

@export_exp_easing(hints: String = "", ...) vararg 🔗

Export a floating-point property with an easing editor widget. Additional hints can be provided to adjust the behavior of the widget. "attenuation" flips the curve, which makes it more intuitive for editing attenuation properties. "positive_only" limits values to only be greater than or equal to zero.

See also @GlobalScope.PROPERTY_HINT_EXP_EASING.

@export_file(filter: String = "", ...) vararg 🔗

Export a String, Array[String], or PackedStringArray property as a path to a file. The path will be limited to the project folder and its subfolders. See @export_global_file to allow picking from the entire filesystem.

If filter is provided, only matching files will be available for picking.

See also @GlobalScope.PROPERTY_HINT_FILE.

Note: The file will be stored and referenced as UID, if available. This ensures that the reference is valid even when the file is moved. You can use ResourceUID methods to convert it to path.

@export_file_path(filter: String = "", ...) vararg 🔗

Same as @export_file, except the file will be stored as a raw path. This means that it may become invalid when the file is moved. If you are exporting a Resource path, consider using @export_file instead.

@export_flags(names: String, ...) vararg 🔗

Export an integer property as a bit flag field. This allows to store several "checked" or true values with one property, and comfortably select them from the Inspector dock.

See also @GlobalScope.PROPERTY_HINT_FLAGS.

You can add explicit values using a colon:

You can also combine several flags:

Note: A flag value must be at least 1 and at most 2 ** 32 - 1.

Note: Unlike @export_enum, the previous explicit value is not taken into account. In the following example, A is 16, B is 2, C is 4.

You can also use the annotation on Array[int], PackedByteArray, PackedInt32Array, and PackedInt64Array

@export_flags_2d_navigation() 🔗

Export an integer property as a bit flag field for 2D navigation layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/2d_navigation/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_2D_NAVIGATION.

@export_flags_2d_physics() 🔗

Export an integer property as a bit flag field for 2D physics layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/2d_physics/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_2D_PHYSICS.

@export_flags_2d_render() 🔗

Export an integer property as a bit flag field for 2D render layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/2d_render/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_2D_RENDER.

@export_flags_3d_navigation() 🔗

Export an integer property as a bit flag field for 3D navigation layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/3d_navigation/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_3D_NAVIGATION.

@export_flags_3d_physics() 🔗

Export an integer property as a bit flag field for 3D physics layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/3d_physics/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_3D_PHYSICS.

@export_flags_3d_render() 🔗

Export an integer property as a bit flag field for 3D render layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/3d_render/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_3D_RENDER.

@export_flags_avoidance() 🔗

Export an integer property as a bit flag field for navigation avoidance layers. The widget in the Inspector dock will use the layer names defined in ProjectSettings.layer_names/avoidance/layer_1.

See also @GlobalScope.PROPERTY_HINT_LAYERS_AVOIDANCE.

@export_global_dir() 🔗

Export a String, Array[String], or PackedStringArray property as an absolute path to a directory. The path can be picked from the entire filesystem. See @export_dir to limit it to the project folder and its subfolders.

See also @GlobalScope.PROPERTY_HINT_GLOBAL_DIR.

@export_global_file(filter: String = "", ...) vararg 🔗

Export a String, Array[String], or PackedStringArray property as an absolute path to a file. The path can be picked from the entire filesystem. See @export_file to limit it to the project folder and its subfolders.

If filter is provided, only matching files will be available for picking.

See also @GlobalScope.PROPERTY_HINT_GLOBAL_FILE.

@export_group(name: String, prefix: String = "") 🔗

Define a new group for the following exported properties. This helps to organize properties in the Inspector dock. Groups can be added with an optional prefix, which would make group to only consider properties that have this prefix. The grouping will break on the first property that doesn't have a prefix. The prefix is also removed from the property's name in the Inspector dock.

If no prefix is provided, then every following property will be added to the group. The group ends when then next group or category is defined. You can also force end a group by using this annotation with empty strings for parameters, @export_group("", "").

Groups cannot be nested, use @export_subgroup to add subgroups within groups.

See also @GlobalScope.PROPERTY_USAGE_GROUP.

@export_multiline() 🔗

Export a String, Array[String], PackedStringArray, Dictionary or Array[Dictionary] property with a large TextEdit widget instead of a LineEdit. This adds support for multiline content and makes it easier to edit large amount of text stored in the property.

See also @GlobalScope.PROPERTY_HINT_MULTILINE_TEXT.

@export_node_path(type: String = "", ...) vararg 🔗

Export a NodePath or Array[NodePath] property with a filter for allowed node types.

See also @GlobalScope.PROPERTY_HINT_NODE_PATH_VALID_TYPES.

Note: The type must be a native class or a globally registered script (using the class_name keyword) that inherits Node.

@export_placeholder(placeholder: String) 🔗

Export a String, Array[String], or PackedStringArray property with a placeholder text displayed in the editor widget when no value is present.

See also @GlobalScope.PROPERTY_HINT_PLACEHOLDER_TEXT.

@export_range(min: float, max: float, step: float = 1.0, extra_hints: String = "", ...) vararg 🔗

Export an int, float, Array[int], Array[float], PackedByteArray, PackedInt32Array, PackedInt64Array, PackedFloat32Array, or PackedFloat64Array property as a range value. The range must be defined by min and max, as well as an optional step and a variety of extra hints. The step defaults to 1 for integer properties. For floating-point numbers this value depends on your EditorSettings.interface/inspector/default_float_step setting.

If hints "or_greater" and "or_less" are provided, the editor widget will not cap the value at range boundaries. The "exp" hint will make the edited values on range to change exponentially. The "hide_slider" hint will hide the slider element of the editor widget.

Hints also allow to indicate the units for the edited value. Using "radians_as_degrees" you can specify that the actual value is in radians, but should be displayed in degrees in the Inspector dock (the range values are also in degrees). "degrees" allows to add a degree sign as a unit suffix (the value is unchanged). Finally, a custom suffix can be provided using "suffix:unit", where "unit" can be any string.

See also @GlobalScope.PROPERTY_HINT_RANGE.

Export a property with @GlobalScope.PROPERTY_USAGE_STORAGE flag. The property is not displayed in the editor, but it is serialized and stored in the scene or resource file. This can be useful for @tool scripts. Also the property value is copied when Resource.duplicate() or Node.duplicate() is called, unlike non-exported variables.

@export_subgroup(name: String, prefix: String = "") 🔗

Define a new subgroup for the following exported properties. This helps to organize properties in the Inspector dock. Subgroups work exactly like groups, except they need a parent group to exist. See @export_group.

See also @GlobalScope.PROPERTY_USAGE_SUBGROUP.

Note: Subgroups cannot be nested, but you can use the slash separator (/) to achieve the desired effect:

@export_tool_button(text: String, icon: String = "") 🔗

Export a Callable property as a clickable button with the label text. When the button is pressed, the callable is called.

If icon is specified, it is used to fetch an icon for the button via Control.get_theme_icon(), from the "EditorIcons" theme type. If icon is omitted, the default "Callable" icon is used instead.

Consider using the EditorUndoRedoManager to allow the action to be reverted safely.

See also @GlobalScope.PROPERTY_HINT_TOOL_BUTTON.

Note: The property is exported without the @GlobalScope.PROPERTY_USAGE_STORAGE flag because a Callable cannot be properly serialized and stored in a file.

Note: In an exported project neither EditorInterface nor EditorUndoRedoManager exist, which may cause some scripts to break. To prevent this, you can use Engine.get_singleton() and omit the static type from the variable declaration:

Note: Avoid storing lambda callables in member variables of RefCounted-based classes (e.g. resources), as this can lead to memory leaks. Use only method callables and optionally Callable.bind() or Callable.unbind().

@icon(icon_path: String) 🔗

Add a custom icon to the current script. The icon specified at icon_path is displayed in the Scene dock for every node of that class, as well as in various editor dialogs.

Note: Only the script can have a custom icon. Inner classes are not supported.

Note: As annotations describe their subject, the @icon annotation must be placed before the class definition and inheritance.

Note: Unlike most other annotations, the argument of the @icon annotation must be a string literal (constant expressions are not supported).

Mark the following property as assigned when the Node is ready. Values for these properties are not assigned immediately when the node is initialized (Object._init()), and instead are computed and stored right before Node._ready().

@rpc(mode: String = "authority", sync: String = "call_remote", transfer_mode: String = "unreliable", transfer_channel: int = 0) 🔗

Mark the following method for remote procedure calls. See High-level multiplayer.

If mode is set as "any_peer", allows any peer to call this RPC function. Otherwise, only the authority peer is allowed to call it and mode should be kept as "authority". When configuring functions as RPCs with Node.rpc_config(), each of these modes respectively corresponds to the MultiplayerAPI.RPC_MODE_AUTHORITY and MultiplayerAPI.RPC_MODE_ANY_PEER RPC modes. See RPCMode. If a peer that is not the authority tries to call a function that is only allowed for the authority, the function will not be executed. If the error can be detected locally (when the RPC configuration is consistent between the local and the remote peer), an error message will be displayed on the sender peer. Otherwise, the remote peer will detect the error and print an error there.

If sync is set as "call_remote", the function will only be executed on the remote peer, but not locally. To run this function locally too, set sync to "call_local". When configuring functions as RPCs with Node.rpc_config(), this is equivalent to setting call_local to true.

The transfer_mode accepted values are "unreliable", "unreliable_ordered", or "reliable". It sets the transfer mode of the underlying MultiplayerPeer. See MultiplayerPeer.transfer_mode.

The transfer_channel defines the channel of the underlying MultiplayerPeer. See MultiplayerPeer.transfer_channel.

The order of mode, sync and transfer_mode does not matter, but values related to the same argument must not be used more than once. transfer_channel always has to be the 4th argument (you must specify 3 preceding arguments).

Note: Methods annotated with @rpc cannot receive objects which define required parameters in Object._init(). See Object._init() for more details.

Make a script with static variables to not persist after all references are lost. If the script is loaded again the static variables will revert to their default values.

Note: As annotations describe their subject, the @static_unload annotation must be placed before the class definition and inheritance.

Warning: Currently, due to a bug, scripts are never freed, even if @static_unload annotation is used.

Mark the current script as a tool script, allowing it to be loaded and executed by the editor. See Running code in the editor.

Note: As annotations describe their subject, the @tool annotation must be placed before the class definition and inheritance.

@warning_ignore(warning: String, ...) vararg 🔗

Mark the following statement to ignore the specified warning. See GDScript warning system.

See also @warning_ignore_start and @warning_ignore_restore.

@warning_ignore_restore(warning: String, ...) vararg 🔗

Stops ignoring the listed warning types after @warning_ignore_start. Ignoring the specified warning types will be reset to Project Settings. This annotation can be omitted to ignore the warning types until the end of the file.

Note: Unlike most other annotations, arguments of the @warning_ignore_restore annotation must be string literals (constant expressions are not supported).

@warning_ignore_start(warning: String, ...) vararg 🔗

Starts ignoring the listed warning types until the end of the file or the @warning_ignore_restore annotation with the given warning type.

Note: To suppress a single warning, use @warning_ignore instead.

Note: Unlike most other annotations, arguments of the @warning_ignore_start annotation must be string literals (constant expressions are not supported).

Color Color8(r8: int, g8: int, b8: int, a8: int = 255) 🔗

Deprecated: Use Color.from_rgba8() instead.

Returns a Color constructed from red (r8), green (g8), blue (b8), and optionally alpha (a8) integer channels, each divided by 255.0 for their final value. Using Color8() instead of the standard Color constructor is useful when you need to match exact color values in an Image.

Note: Due to the lower precision of Color8() compared to the standard Color constructor, a color created with Color8() will generally not be equal to the same color created with the standard Color constructor. Use Color.is_equal_approx() for comparisons to avoid issues with floating-point precision error.

void assert(condition: bool, message: String = "") 🔗

Asserts that the condition is true. If the condition is false, an error is generated. When running from the editor, the running project will also be paused until you resume it. This can be used as a stronger form of @GlobalScope.push_error() for reporting errors to project developers or add-on users.

An optional message can be shown in addition to the generic "Assertion failed" message. You can use this to provide additional details about why the assertion failed.

Warning: For performance reasons, the code inside assert() is only executed in debug builds or when running the project from the editor. Don't include code that has side effects in an assert() call. Otherwise, the project will behave differently when exported in release mode.

Note: assert() is a keyword, not a function. So you cannot access it as a Callable or use it inside expressions.

String char(code: int) 🔗

Returns a single character (as a String of length 1) of the given Unicode code point code.

This is the inverse of ord(). See also String.chr() and String.unicode_at().

Variant convert(what: Variant, type: Variant.Type) 🔗

Deprecated: Use @GlobalScope.type_convert() instead.

Converts what to type in the best way possible. The type uses the Variant.Type values.

Object dict_to_inst(dictionary: Dictionary) 🔗

Deprecated: Consider using JSON.to_native() or Object.get_property_list() instead.

Converts a dictionary (created with inst_to_dict()) back to an Object instance. Can be useful for deserializing.

Returns an array of dictionaries representing the current call stack.

Starting from _ready(), bar() would print:

See also print_debug(), print_stack(), and Engine.capture_script_backtraces().

Note: By default, backtraces are only available in editor builds and debug builds. To enable them for release builds as well, you need to enable ProjectSettings.debug/settings/gdscript/always_track_call_stacks.

Dictionary inst_to_dict(instance: Object) 🔗

Deprecated: Consider using JSON.from_native() or Object.get_property_list() instead.

Returns the passed instance converted to a Dictionary. Can be useful for serializing.

Note: This function can only be used to serialize objects with an attached GDScript stored in a separate file. Objects without an attached script, with a script written in another language, or with a built-in script are not supported.

Note: This function is not recursive, which means that nested objects will not be represented as dictionaries. Also, properties passed by reference (Object, Dictionary, Array, and packed arrays) are copied by reference, not duplicated.

bool is_instance_of(value: Variant, type: Variant) 🔗

Returns true if value is an instance of type. The type value must be one of the following:

A constant from the Variant.Type enumeration, for example @GlobalScope.TYPE_INT.

An Object-derived class which exists in ClassDB, for example Node.

A Script (you can use any class, including inner one).

Unlike the right operand of the is operator, type can be a non-constant value. The is operator supports more features (such as typed arrays). Use the operator instead of this method if you do not need to check the type dynamically.

Note: If value and/or type are freed objects (see @GlobalScope.is_instance_valid()), or type is not one of the above options, this method will raise a runtime error.

See also @GlobalScope.typeof(), type_exists(), Array.is_same_typed() (and other Array methods).

int len(var: Variant) 🔗

Returns the length of the given Variant var. The length can be the character count of a String or StringName, the element count of any array type, or the size of a Dictionary. For every other Variant type, a run-time error is generated and execution is stopped.

Resource load(path: String) 🔗

Returns a Resource from the filesystem located at the absolute path. Unless it's already referenced elsewhere (such as in another script or in the scene), the resource is loaded from disk on function call, which might cause a slight delay, especially when loading large scenes. To avoid unnecessary delays when loading something multiple times, either store the resource in a variable or use preload(). This method is equivalent of using ResourceLoader.load() with ResourceLoader.CACHE_MODE_REUSE.

Note: Resource paths can be obtained by right-clicking on a resource in the FileSystem dock and choosing "Copy Path", or by dragging the file from the FileSystem dock into the current script.

Important: Relative paths are not relative to the script calling this method, instead it is prefixed with "res://". Loading from relative paths might not work as expected.

This function is a simplified version of ResourceLoader.load(), which can be used for more advanced scenarios.

Note: Files have to be imported into the engine first to load them using this function. If you want to load Images at run-time, you may use Image.load(). If you want to import audio files, you can use the snippet described in AudioStreamMP3.data.

Note: If ProjectSettings.editor/export/convert_text_resources_to_binary is true, load() will not be able to read converted files in an exported project. If you rely on run-time loading of files present within the PCK, set ProjectSettings.editor/export/convert_text_resources_to_binary to false.

int ord(char: String) 🔗

Returns an integer representing the Unicode code point of the given character char, which should be a string of length 1.

This is the inverse of char(). See also String.chr() and String.unicode_at().

Resource preload(path: String) 🔗

Returns a Resource from the filesystem located at path. During run-time, the resource is loaded when the script is being parsed. This function effectively acts as a reference to that resource. Note that this function requires path to be a constant String. If you want to load a resource from a dynamic/variable path, use load().

Note: Resource paths can be obtained by right-clicking on a resource in the Assets Panel and choosing "Copy Path", or by dragging the file from the FileSystem dock into the current script.

Note: preload() is a keyword, not a function. So you cannot access it as a Callable.

void print_debug(...) vararg 🔗

Like @GlobalScope.print(), but includes the current stack frame when running with the debugger turned on.

The output in the console may look like the following:

See also print_stack(), get_stack(), and Engine.capture_script_backtraces().

Note: By default, backtraces are only available in editor builds and debug builds. To enable them for release builds as well, you need to enable ProjectSettings.debug/settings/gdscript/always_track_call_stacks.

Prints a stack trace at the current code location.

The output in the console may look like the following:

See also print_debug(), get_stack(), and Engine.capture_script_backtraces().

Note: By default, backtraces are only available in editor builds and debug builds. To enable them for release builds as well, you need to enable ProjectSettings.debug/settings/gdscript/always_track_call_stacks.

Array range(...) vararg 🔗

Returns an array with the given range. range() can be called in three ways:

range(n: int): Starts from 0, increases by steps of 1, and stops before n. The argument n is exclusive.

range(b: int, n: int): Starts from b, increases by steps of 1, and stops before n. The arguments b and n are inclusive and exclusive, respectively.

range(b: int, n: int, s: int): Starts from b, increases/decreases by steps of s, and stops before n. The arguments b and n are inclusive and exclusive, respectively. The argument s can be negative, but not 0. If s is 0, an error message is printed.

range() converts all arguments to int before processing.

Note: Returns an empty array if no value meets the value constraint (e.g. range(2, 5, -1) or range(5, 5, 1)).

To iterate over an Array backwards, use:

To iterate over float, convert them in the loop.

bool type_exists(type: StringName) 🔗

Returns true if the given Object-derived class exists in ClassDB. Note that Variant data types are not registered in ClassDB.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (python):
```python
@abstract class Shape:
    @abstract func draw()

class Circle extends Shape:
    func draw():
        print("Drawing a circle.")

class Square extends Shape:
    func draw():
        print("Drawing a square.")
```

Example 2 (swift):
```swift
extends Node

enum Direction {LEFT, RIGHT, UP, DOWN}

# Built-in types.
@export var string = ""
@export var int_number = 5
@export var float_number: float = 5

# Enums.
@export var type: Variant.Type
@export var format: Image.Format
@export var direction: Direction

# Resources.
@export var image: Image
@export var custom_resource: CustomResource

# Nodes.
@export var node: Node
@export var custom_node: CustomNode

# Typed arrays.
@export var int_array: Array[int]
@export var direction_array: Array[Direction]
@export var image_array: Array[Image]
@export var node_array: Array[Node]
```

Example 3 (swift):
```swift
@export_category("Statistics")
@export var hp = 30
@export var speed = 1.25
```

Example 4 (swift):
```swift
@export_color_no_alpha var dye_color: Color
@export_color_no_alpha var dye_colors: Array[Color]
```

---

## @GlobalScope — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html

**Contents:**
- @GlobalScope
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Global scope constants and functions.

A list of global scope enumerated constants and built-in functions. This is all that resides in the globals, constants regarding error codes, keycodes, property hints, etc.

Singletons are also documented here, since they can be accessed from anywhere.

For the entries that can only be accessed from scripts written in GDScript, see @GDScript.

There are notable differences when using this API with C#. See C# API differences to GDScript for more information.

Random number generation

NavigationMeshGenerator

NavigationMeshGenerator

PhysicsServer2DManager

PhysicsServer2DManager

PhysicsServer3DManager

PhysicsServer3DManager

angle_difference(from: float, to: float)

atan2(y: float, x: float)

bezier_derivative(start: float, control_1: float, control_2: float, end: float, t: float)

bezier_interpolate(start: float, control_1: float, control_2: float, end: float, t: float)

bytes_to_var(bytes: PackedByteArray)

bytes_to_var_with_objects(bytes: PackedByteArray)

clamp(value: Variant, min: Variant, max: Variant)

clampf(value: float, min: float, max: float)

clampi(value: int, min: int, max: int)

cos(angle_rad: float)

cubic_interpolate(from: float, to: float, pre: float, post: float, weight: float)

cubic_interpolate_angle(from: float, to: float, pre: float, post: float, weight: float)

cubic_interpolate_angle_in_time(from: float, to: float, pre: float, post: float, weight: float, to_t: float, pre_t: float, post_t: float)

cubic_interpolate_in_time(from: float, to: float, pre: float, post: float, weight: float, to_t: float, pre_t: float, post_t: float)

db_to_linear(db: float)

deg_to_rad(deg: float)

ease(x: float, curve: float)

error_string(error: int)

fmod(x: float, y: float)

fposmod(x: float, y: float)

hash(variable: Variant)

instance_from_id(instance_id: int)

inverse_lerp(from: float, to: float, weight: float)

is_equal_approx(a: float, b: float)

is_instance_id_valid(id: int)

is_instance_valid(instance: Variant)

is_same(a: Variant, b: Variant)

is_zero_approx(x: float)

lerp(from: Variant, to: Variant, weight: Variant)

lerp_angle(from: float, to: float, weight: float)

lerpf(from: float, to: float, weight: float)

linear_to_db(lin: float)

maxf(a: float, b: float)

minf(a: float, b: float)

move_toward(from: float, to: float, delta: float)

nearest_po2(value: int)

pingpong(value: float, length: float)

posmod(x: int, y: int)

pow(base: float, exp: float)

print_rich(...) vararg

print_verbose(...) vararg

push_error(...) vararg

push_warning(...) vararg

rad_to_deg(rad: float)

rand_from_seed(seed: int)

randf_range(from: float, to: float)

randfn(mean: float, deviation: float)

randi_range(from: int, to: int)

remap(value: float, istart: float, istop: float, ostart: float, ostop: float)

rid_from_int64(base: int)

rotate_toward(from: float, to: float, delta: float)

sin(angle_rad: float)

smoothstep(from: float, to: float, x: float)

snapped(x: Variant, step: Variant)

snappedf(x: float, step: float)

snappedi(x: float, step: int)

step_decimals(x: float)

str_to_var(string: String)

tan(angle_rad: float)

type_convert(variant: Variant, type: int)

type_string(type: int)

typeof(variable: Variant)

var_to_bytes(variable: Variant)

var_to_bytes_with_objects(variable: Variant)

var_to_str(variable: Variant)

weakref(obj: Variant)

wrap(value: Variant, min: Variant, max: Variant)

wrapf(value: float, min: float, max: float)

wrapi(value: int, min: int, max: int)

Left side, usually used for Control or StyleBox-derived classes.

Top side, usually used for Control or StyleBox-derived classes.

Right side, usually used for Control or StyleBox-derived classes.

Bottom side, usually used for Control or StyleBox-derived classes.

Corner CORNER_TOP_LEFT = 0

Corner CORNER_TOP_RIGHT = 1

Corner CORNER_BOTTOM_RIGHT = 2

Corner CORNER_BOTTOM_LEFT = 3

Orientation VERTICAL = 1

General vertical alignment, usually used for Separator, ScrollBar, Slider, etc.

Orientation HORIZONTAL = 0

General horizontal alignment, usually used for Separator, ScrollBar, Slider, etc.

enum ClockDirection: 🔗

ClockDirection CLOCKWISE = 0

Clockwise rotation. Used by some methods (e.g. Image.rotate_90()).

ClockDirection COUNTERCLOCKWISE = 1

Counter-clockwise rotation. Used by some methods (e.g. Image.rotate_90()).

enum HorizontalAlignment: 🔗

HorizontalAlignment HORIZONTAL_ALIGNMENT_LEFT = 0

Horizontal left alignment, usually for text-derived classes.

HorizontalAlignment HORIZONTAL_ALIGNMENT_CENTER = 1

Horizontal center alignment, usually for text-derived classes.

HorizontalAlignment HORIZONTAL_ALIGNMENT_RIGHT = 2

Horizontal right alignment, usually for text-derived classes.

HorizontalAlignment HORIZONTAL_ALIGNMENT_FILL = 3

Expand row to fit width, usually for text-derived classes.

enum VerticalAlignment: 🔗

VerticalAlignment VERTICAL_ALIGNMENT_TOP = 0

Vertical top alignment, usually for text-derived classes.

VerticalAlignment VERTICAL_ALIGNMENT_CENTER = 1

Vertical center alignment, usually for text-derived classes.

VerticalAlignment VERTICAL_ALIGNMENT_BOTTOM = 2

Vertical bottom alignment, usually for text-derived classes.

VerticalAlignment VERTICAL_ALIGNMENT_FILL = 3

Expand rows to fit height, usually for text-derived classes.

enum InlineAlignment: 🔗

InlineAlignment INLINE_ALIGNMENT_TOP_TO = 0

Aligns the top of the inline object (e.g. image, table) to the position of the text specified by INLINE_ALIGNMENT_TO_* constant.

InlineAlignment INLINE_ALIGNMENT_CENTER_TO = 1

Aligns the center of the inline object (e.g. image, table) to the position of the text specified by INLINE_ALIGNMENT_TO_* constant.

InlineAlignment INLINE_ALIGNMENT_BASELINE_TO = 3

Aligns the baseline (user defined) of the inline object (e.g. image, table) to the position of the text specified by INLINE_ALIGNMENT_TO_* constant.

InlineAlignment INLINE_ALIGNMENT_BOTTOM_TO = 2

Aligns the bottom of the inline object (e.g. image, table) to the position of the text specified by INLINE_ALIGNMENT_TO_* constant.

InlineAlignment INLINE_ALIGNMENT_TO_TOP = 0

Aligns the position of the inline object (e.g. image, table) specified by INLINE_ALIGNMENT_*_TO constant to the top of the text.

InlineAlignment INLINE_ALIGNMENT_TO_CENTER = 4

Aligns the position of the inline object (e.g. image, table) specified by INLINE_ALIGNMENT_*_TO constant to the center of the text.

InlineAlignment INLINE_ALIGNMENT_TO_BASELINE = 8

Aligns the position of the inline object (e.g. image, table) specified by INLINE_ALIGNMENT_*_TO constant to the baseline of the text.

InlineAlignment INLINE_ALIGNMENT_TO_BOTTOM = 12

Aligns inline object (e.g. image, table) to the bottom of the text.

InlineAlignment INLINE_ALIGNMENT_TOP = 0

Aligns top of the inline object (e.g. image, table) to the top of the text. Equivalent to INLINE_ALIGNMENT_TOP_TO | INLINE_ALIGNMENT_TO_TOP.

InlineAlignment INLINE_ALIGNMENT_CENTER = 5

Aligns center of the inline object (e.g. image, table) to the center of the text. Equivalent to INLINE_ALIGNMENT_CENTER_TO | INLINE_ALIGNMENT_TO_CENTER.

InlineAlignment INLINE_ALIGNMENT_BOTTOM = 14

Aligns bottom of the inline object (e.g. image, table) to the bottom of the text. Equivalent to INLINE_ALIGNMENT_BOTTOM_TO | INLINE_ALIGNMENT_TO_BOTTOM.

InlineAlignment INLINE_ALIGNMENT_IMAGE_MASK = 3

A bit mask for INLINE_ALIGNMENT_*_TO alignment constants.

InlineAlignment INLINE_ALIGNMENT_TEXT_MASK = 12

A bit mask for INLINE_ALIGNMENT_TO_* alignment constants.

EulerOrder EULER_ORDER_XYZ = 0

Specifies that Euler angles should be in XYZ order. When composing, the order is X, Y, Z. When decomposing, the order is reversed, first Z, then Y, and X last.

EulerOrder EULER_ORDER_XZY = 1

Specifies that Euler angles should be in XZY order. When composing, the order is X, Z, Y. When decomposing, the order is reversed, first Y, then Z, and X last.

EulerOrder EULER_ORDER_YXZ = 2

Specifies that Euler angles should be in YXZ order. When composing, the order is Y, X, Z. When decomposing, the order is reversed, first Z, then X, and Y last.

EulerOrder EULER_ORDER_YZX = 3

Specifies that Euler angles should be in YZX order. When composing, the order is Y, Z, X. When decomposing, the order is reversed, first X, then Z, and Y last.

EulerOrder EULER_ORDER_ZXY = 4

Specifies that Euler angles should be in ZXY order. When composing, the order is Z, X, Y. When decomposing, the order is reversed, first Y, then X, and Z last.

EulerOrder EULER_ORDER_ZYX = 5

Specifies that Euler angles should be in ZYX order. When composing, the order is Z, Y, X. When decomposing, the order is reversed, first X, then Y, and Z last.

Enum value which doesn't correspond to any key. This is used to initialize Key properties with a generic state.

Key KEY_SPECIAL = 4194304

Keycodes with this bit applied are non-printable.

Key KEY_ESCAPE = 4194305

Key KEY_TAB = 4194306

Key KEY_BACKTAB = 4194307

Key KEY_BACKSPACE = 4194308

Key KEY_ENTER = 4194309

Return key (on the main keyboard).

Key KEY_KP_ENTER = 4194310

Enter key on the numeric keypad.

Key KEY_INSERT = 4194311

Key KEY_DELETE = 4194312

Key KEY_PAUSE = 4194313

Key KEY_PRINT = 4194314

Key KEY_SYSREQ = 4194315

Key KEY_CLEAR = 4194316

Key KEY_HOME = 4194317

Key KEY_END = 4194318

Key KEY_LEFT = 4194319

Key KEY_RIGHT = 4194321

Key KEY_DOWN = 4194322

Key KEY_PAGEUP = 4194323

Key KEY_PAGEDOWN = 4194324

Key KEY_SHIFT = 4194325

Key KEY_CTRL = 4194326

Key KEY_META = 4194327

Key KEY_ALT = 4194328

Key KEY_CAPSLOCK = 4194329

Key KEY_NUMLOCK = 4194330

Key KEY_SCROLLLOCK = 4194331

Key KEY_F10 = 4194341

Key KEY_F11 = 4194342

Key KEY_F12 = 4194343

Key KEY_F13 = 4194344

Key KEY_F14 = 4194345

Key KEY_F15 = 4194346

Key KEY_F16 = 4194347

Key KEY_F17 = 4194348

Key KEY_F18 = 4194349

Key KEY_F19 = 4194350

Key KEY_F20 = 4194351

Key KEY_F21 = 4194352

Key KEY_F22 = 4194353

Key KEY_F23 = 4194354

Key KEY_F24 = 4194355

Key KEY_F25 = 4194356

F25 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F26 = 4194357

F26 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F27 = 4194358

F27 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F28 = 4194359

F28 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F29 = 4194360

F29 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F30 = 4194361

F30 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F31 = 4194362

F31 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F32 = 4194363

F32 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F33 = 4194364

F33 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F34 = 4194365

F34 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_F35 = 4194366

F35 key. Only supported on macOS and Linux due to a Windows limitation.

Key KEY_KP_MULTIPLY = 4194433

Multiply (*) key on the numeric keypad.

Key KEY_KP_DIVIDE = 4194434

Divide (/) key on the numeric keypad.

Key KEY_KP_SUBTRACT = 4194435

Subtract (-) key on the numeric keypad.

Key KEY_KP_PERIOD = 4194436

Period (.) key on the numeric keypad.

Key KEY_KP_ADD = 4194437

Add (+) key on the numeric keypad.

Key KEY_KP_0 = 4194438

Number 0 on the numeric keypad.

Key KEY_KP_1 = 4194439

Number 1 on the numeric keypad.

Key KEY_KP_2 = 4194440

Number 2 on the numeric keypad.

Key KEY_KP_3 = 4194441

Number 3 on the numeric keypad.

Key KEY_KP_4 = 4194442

Number 4 on the numeric keypad.

Key KEY_KP_5 = 4194443

Number 5 on the numeric keypad.

Key KEY_KP_6 = 4194444

Number 6 on the numeric keypad.

Key KEY_KP_7 = 4194445

Number 7 on the numeric keypad.

Key KEY_KP_8 = 4194446

Number 8 on the numeric keypad.

Key KEY_KP_9 = 4194447

Number 9 on the numeric keypad.

Key KEY_MENU = 4194370

Key KEY_HYPER = 4194371

Hyper key. (On Linux/X11 only).

Key KEY_HELP = 4194373

Key KEY_BACK = 4194376

Key KEY_FORWARD = 4194377

Key KEY_STOP = 4194378

Key KEY_REFRESH = 4194379

Key KEY_VOLUMEDOWN = 4194380

Key KEY_VOLUMEMUTE = 4194381

Key KEY_VOLUMEUP = 4194382

Key KEY_MEDIAPLAY = 4194388

Key KEY_MEDIASTOP = 4194389

Key KEY_MEDIAPREVIOUS = 4194390

Key KEY_MEDIANEXT = 4194391

Key KEY_MEDIARECORD = 4194392

Key KEY_HOMEPAGE = 4194393

Key KEY_FAVORITES = 4194394

Key KEY_SEARCH = 4194395

Key KEY_STANDBY = 4194396

Key KEY_OPENURL = 4194397

Open URL / Launch Browser key.

Key KEY_LAUNCHMAIL = 4194398

Key KEY_LAUNCHMEDIA = 4194399

Key KEY_LAUNCH0 = 4194400

Launch Shortcut 0 key.

Key KEY_LAUNCH1 = 4194401

Launch Shortcut 1 key.

Key KEY_LAUNCH2 = 4194402

Launch Shortcut 2 key.

Key KEY_LAUNCH3 = 4194403

Launch Shortcut 3 key.

Key KEY_LAUNCH4 = 4194404

Launch Shortcut 4 key.

Key KEY_LAUNCH5 = 4194405

Launch Shortcut 5 key.

Key KEY_LAUNCH6 = 4194406

Launch Shortcut 6 key.

Key KEY_LAUNCH7 = 4194407

Launch Shortcut 7 key.

Key KEY_LAUNCH8 = 4194408

Launch Shortcut 8 key.

Key KEY_LAUNCH9 = 4194409

Launch Shortcut 9 key.

Key KEY_LAUNCHA = 4194410

Launch Shortcut A key.

Key KEY_LAUNCHB = 4194411

Launch Shortcut B key.

Key KEY_LAUNCHC = 4194412

Launch Shortcut C key.

Key KEY_LAUNCHD = 4194413

Launch Shortcut D key.

Key KEY_LAUNCHE = 4194414

Launch Shortcut E key.

Key KEY_LAUNCHF = 4194415

Launch Shortcut F key.

Key KEY_GLOBE = 4194416

"Globe" key on Mac / iPad keyboard.

Key KEY_KEYBOARD = 4194417

"On-screen keyboard" key on iPad keyboard.

Key KEY_JIS_EISU = 4194418

英数 key on Mac keyboard.

Key KEY_JIS_KANA = 4194419

かな key on Mac keyboard.

Key KEY_UNKNOWN = 8388607

Exclamation mark (!) key.

Key KEY_QUOTEDBL = 34

Double quotation mark (") key.

Key KEY_NUMBERSIGN = 35

Number sign or hash (#) key.

Percent sign (%) key.

Key KEY_AMPERSAND = 38

Key KEY_APOSTROPHE = 39

Key KEY_PARENLEFT = 40

Left parenthesis (() key.

Key KEY_PARENRIGHT = 41

Right parenthesis (``)``) key.

Key KEY_ASTERISK = 42

Key KEY_SEMICOLON = 59

Less-than sign (<) key.

Greater-than sign (>) key.

Key KEY_QUESTION = 63

Question mark (?) key.

Key KEY_BRACKETLEFT = 91

Left bracket ([lb]) key.

Key KEY_BACKSLASH = 92

Key KEY_BRACKETRIGHT = 93

Right bracket ([rb]) key.

Key KEY_ASCIICIRCUM = 94

Key KEY_UNDERSCORE = 95

Key KEY_QUOTELEFT = 96

Key KEY_BRACELEFT = 123

Vertical bar or pipe (|) key.

Key KEY_BRACERIGHT = 125

Key KEY_ASCIITILDE = 126

Key KEY_SECTION = 167

Section sign (§) key.

flags KeyModifierMask: 🔗

KeyModifierMask KEY_CODE_MASK = 8388607

KeyModifierMask KEY_MODIFIER_MASK = 2130706432

KeyModifierMask KEY_MASK_CMD_OR_CTRL = 16777216

Automatically remapped to KEY_META on macOS and KEY_CTRL on other platforms, this mask is never set in the actual events, and should be used for key mapping only.

KeyModifierMask KEY_MASK_SHIFT = 33554432

KeyModifierMask KEY_MASK_ALT = 67108864

Alt or Option (on macOS) key mask.

KeyModifierMask KEY_MASK_META = 134217728

Command (on macOS) or Meta/Windows key mask.

KeyModifierMask KEY_MASK_CTRL = 268435456

KeyModifierMask KEY_MASK_KPAD = 536870912

KeyModifierMask KEY_MASK_GROUP_SWITCH = 1073741824

Group Switch key mask.

KeyLocation KEY_LOCATION_UNSPECIFIED = 0

Used for keys which only appear once, or when a comparison doesn't need to differentiate the LEFT and RIGHT versions.

For example, when using InputEvent.is_match(), an event which has KEY_LOCATION_UNSPECIFIED will match any KeyLocation on the passed event.

KeyLocation KEY_LOCATION_LEFT = 1

A key which is to the left of its twin.

KeyLocation KEY_LOCATION_RIGHT = 2

A key which is to the right of its twin.

MouseButton MOUSE_BUTTON_NONE = 0

Enum value which doesn't correspond to any mouse button. This is used to initialize MouseButton properties with a generic state.

MouseButton MOUSE_BUTTON_LEFT = 1

Primary mouse button, usually assigned to the left button.

MouseButton MOUSE_BUTTON_RIGHT = 2

Secondary mouse button, usually assigned to the right button.

MouseButton MOUSE_BUTTON_MIDDLE = 3

MouseButton MOUSE_BUTTON_WHEEL_UP = 4

Mouse wheel scrolling up.

MouseButton MOUSE_BUTTON_WHEEL_DOWN = 5

Mouse wheel scrolling down.

MouseButton MOUSE_BUTTON_WHEEL_LEFT = 6

Mouse wheel left button (only present on some mice).

MouseButton MOUSE_BUTTON_WHEEL_RIGHT = 7

Mouse wheel right button (only present on some mice).

MouseButton MOUSE_BUTTON_XBUTTON1 = 8

Extra mouse button 1. This is sometimes present, usually to the sides of the mouse.

MouseButton MOUSE_BUTTON_XBUTTON2 = 9

Extra mouse button 2. This is sometimes present, usually to the sides of the mouse.

flags MouseButtonMask: 🔗

MouseButtonMask MOUSE_BUTTON_MASK_LEFT = 1

Primary mouse button mask, usually for the left button.

MouseButtonMask MOUSE_BUTTON_MASK_RIGHT = 2

Secondary mouse button mask, usually for the right button.

MouseButtonMask MOUSE_BUTTON_MASK_MIDDLE = 4

Middle mouse button mask.

MouseButtonMask MOUSE_BUTTON_MASK_MB_XBUTTON1 = 128

Extra mouse button 1 mask.

MouseButtonMask MOUSE_BUTTON_MASK_MB_XBUTTON2 = 256

Extra mouse button 2 mask.

JoyButton JOY_BUTTON_INVALID = -1

An invalid game controller button.

JoyButton JOY_BUTTON_A = 0

Game controller SDL button A. Corresponds to the bottom action button: Sony Cross, Xbox A, Nintendo B.

JoyButton JOY_BUTTON_B = 1

Game controller SDL button B. Corresponds to the right action button: Sony Circle, Xbox B, Nintendo A.

JoyButton JOY_BUTTON_X = 2

Game controller SDL button X. Corresponds to the left action button: Sony Square, Xbox X, Nintendo Y.

JoyButton JOY_BUTTON_Y = 3

Game controller SDL button Y. Corresponds to the top action button: Sony Triangle, Xbox Y, Nintendo X.

JoyButton JOY_BUTTON_BACK = 4

Game controller SDL back button. Corresponds to the Sony Select, Xbox Back, Nintendo - button.

JoyButton JOY_BUTTON_GUIDE = 5

Game controller SDL guide button. Corresponds to the Sony PS, Xbox Home button.

JoyButton JOY_BUTTON_START = 6

Game controller SDL start button. Corresponds to the Sony Options, Xbox Menu, Nintendo + button.

JoyButton JOY_BUTTON_LEFT_STICK = 7

Game controller SDL left stick button. Corresponds to the Sony L3, Xbox L/LS button.

JoyButton JOY_BUTTON_RIGHT_STICK = 8

Game controller SDL right stick button. Corresponds to the Sony R3, Xbox R/RS button.

JoyButton JOY_BUTTON_LEFT_SHOULDER = 9

Game controller SDL left shoulder button. Corresponds to the Sony L1, Xbox LB button.

JoyButton JOY_BUTTON_RIGHT_SHOULDER = 10

Game controller SDL right shoulder button. Corresponds to the Sony R1, Xbox RB button.

JoyButton JOY_BUTTON_DPAD_UP = 11

Game controller D-pad up button.

JoyButton JOY_BUTTON_DPAD_DOWN = 12

Game controller D-pad down button.

JoyButton JOY_BUTTON_DPAD_LEFT = 13

Game controller D-pad left button.

JoyButton JOY_BUTTON_DPAD_RIGHT = 14

Game controller D-pad right button.

JoyButton JOY_BUTTON_MISC1 = 15

Game controller SDL miscellaneous button. Corresponds to Xbox share button, PS5 microphone button, Nintendo Switch capture button.

JoyButton JOY_BUTTON_PADDLE1 = 16

Game controller SDL paddle 1 button.

JoyButton JOY_BUTTON_PADDLE2 = 17

Game controller SDL paddle 2 button.

JoyButton JOY_BUTTON_PADDLE3 = 18

Game controller SDL paddle 3 button.

JoyButton JOY_BUTTON_PADDLE4 = 19

Game controller SDL paddle 4 button.

JoyButton JOY_BUTTON_TOUCHPAD = 20

Game controller SDL touchpad button.

JoyButton JOY_BUTTON_SDL_MAX = 21

The number of SDL game controller buttons.

JoyButton JOY_BUTTON_MAX = 128

The maximum number of game controller buttons supported by the engine. The actual limit may be lower on specific platforms:

Android: Up to 36 buttons.

Linux: Up to 80 buttons.

Windows and macOS: Up to 128 buttons.

JoyAxis JOY_AXIS_INVALID = -1

An invalid game controller axis.

JoyAxis JOY_AXIS_LEFT_X = 0

Game controller left joystick x-axis.

JoyAxis JOY_AXIS_LEFT_Y = 1

Game controller left joystick y-axis.

JoyAxis JOY_AXIS_RIGHT_X = 2

Game controller right joystick x-axis.

JoyAxis JOY_AXIS_RIGHT_Y = 3

Game controller right joystick y-axis.

JoyAxis JOY_AXIS_TRIGGER_LEFT = 4

Game controller left trigger axis.

JoyAxis JOY_AXIS_TRIGGER_RIGHT = 5

Game controller right trigger axis.

JoyAxis JOY_AXIS_SDL_MAX = 6

The number of SDL game controller axes.

JoyAxis JOY_AXIS_MAX = 10

The maximum number of game controller axes: OpenVR supports up to 5 Joysticks making a total of 10 axes.

MIDIMessage MIDI_MESSAGE_NONE = 0

Does not correspond to any MIDI message. This is the default value of InputEventMIDI.message.

MIDIMessage MIDI_MESSAGE_NOTE_OFF = 8

MIDI message sent when a note is released.

Note: Not all MIDI devices send this message; some may send MIDI_MESSAGE_NOTE_ON with InputEventMIDI.velocity set to 0.

MIDIMessage MIDI_MESSAGE_NOTE_ON = 9

MIDI message sent when a note is pressed.

MIDIMessage MIDI_MESSAGE_AFTERTOUCH = 10

MIDI message sent to indicate a change in pressure while a note is being pressed down, also called aftertouch.

MIDIMessage MIDI_MESSAGE_CONTROL_CHANGE = 11

MIDI message sent when a controller value changes. In a MIDI device, a controller is any input that doesn't play notes. These may include sliders for volume, balance, and panning, as well as switches and pedals. See the General MIDI specification for a small list.

MIDIMessage MIDI_MESSAGE_PROGRAM_CHANGE = 12

MIDI message sent when the MIDI device changes its current instrument (also called program or preset).

MIDIMessage MIDI_MESSAGE_CHANNEL_PRESSURE = 13

MIDI message sent to indicate a change in pressure for the whole channel. Some MIDI devices may send this instead of MIDI_MESSAGE_AFTERTOUCH.

MIDIMessage MIDI_MESSAGE_PITCH_BEND = 14

MIDI message sent when the value of the pitch bender changes, usually a wheel on the MIDI device.

MIDIMessage MIDI_MESSAGE_SYSTEM_EXCLUSIVE = 240

MIDI system exclusive (SysEx) message. This type of message is not standardized and it's highly dependent on the MIDI device sending it.

Note: Getting this message's data from InputEventMIDI is not implemented.

MIDIMessage MIDI_MESSAGE_QUARTER_FRAME = 241

MIDI message sent every quarter frame to keep connected MIDI devices synchronized. Related to MIDI_MESSAGE_TIMING_CLOCK.

Note: Getting this message's data from InputEventMIDI is not implemented.

MIDIMessage MIDI_MESSAGE_SONG_POSITION_POINTER = 242

MIDI message sent to jump onto a new position in the current sequence or song.

Note: Getting this message's data from InputEventMIDI is not implemented.

MIDIMessage MIDI_MESSAGE_SONG_SELECT = 243

MIDI message sent to select a sequence or song to play.

Note: Getting this message's data from InputEventMIDI is not implemented.

MIDIMessage MIDI_MESSAGE_TUNE_REQUEST = 246

MIDI message sent to request a tuning calibration. Used on analog synthesizers. Most modern MIDI devices do not need this message.

MIDIMessage MIDI_MESSAGE_TIMING_CLOCK = 248

MIDI message sent 24 times after MIDI_MESSAGE_QUARTER_FRAME, to keep connected MIDI devices synchronized.

MIDIMessage MIDI_MESSAGE_START = 250

MIDI message sent to start the current sequence or song from the beginning.

MIDIMessage MIDI_MESSAGE_CONTINUE = 251

MIDI message sent to resume from the point the current sequence or song was paused.

MIDIMessage MIDI_MESSAGE_STOP = 252

MIDI message sent to pause the current sequence or song.

MIDIMessage MIDI_MESSAGE_ACTIVE_SENSING = 254

MIDI message sent repeatedly while the MIDI device is idle, to tell the receiver that the connection is alive. Most MIDI devices do not send this message.

MIDIMessage MIDI_MESSAGE_SYSTEM_RESET = 255

MIDI message sent to reset a MIDI device to its default state, as if it was just turned on. It should not be sent when the MIDI device is being turned on.

Methods that return Error return OK when no error occurred.

Since OK has value 0, and all other error constants are positive integers, it can also be used in boolean checks.

Note: Many functions do not return an error code, but will print error messages to standard output.

Error ERR_UNAVAILABLE = 2

Error ERR_UNCONFIGURED = 3

Error ERR_UNAUTHORIZED = 4

Error ERR_PARAMETER_RANGE_ERROR = 5

Parameter range error.

Error ERR_OUT_OF_MEMORY = 6

Out of memory (OOM) error.

Error ERR_FILE_NOT_FOUND = 7

File: Not found error.

Error ERR_FILE_BAD_DRIVE = 8

File: Bad drive error.

Error ERR_FILE_BAD_PATH = 9

File: Bad path error.

Error ERR_FILE_NO_PERMISSION = 10

File: No permission error.

Error ERR_FILE_ALREADY_IN_USE = 11

File: Already in use error.

Error ERR_FILE_CANT_OPEN = 12

File: Can't open error.

Error ERR_FILE_CANT_WRITE = 13

File: Can't write error.

Error ERR_FILE_CANT_READ = 14

File: Can't read error.

Error ERR_FILE_UNRECOGNIZED = 15

File: Unrecognized error.

Error ERR_FILE_CORRUPT = 16

Error ERR_FILE_MISSING_DEPENDENCIES = 17

File: Missing dependencies error.

Error ERR_FILE_EOF = 18

File: End of file (EOF) error.

Error ERR_CANT_OPEN = 19

Error ERR_CANT_CREATE = 20

Error ERR_QUERY_FAILED = 21

Error ERR_ALREADY_IN_USE = 22

Already in use error.

Error ERR_LOCKED = 23

Error ERR_TIMEOUT = 24

Error ERR_CANT_CONNECT = 25

Error ERR_CANT_RESOLVE = 26

Error ERR_CONNECTION_ERROR = 27

Error ERR_CANT_ACQUIRE_RESOURCE = 28

Can't acquire resource error.

Error ERR_CANT_FORK = 29

Can't fork process error.

Error ERR_INVALID_DATA = 30

Error ERR_INVALID_PARAMETER = 31

Invalid parameter error.

Error ERR_ALREADY_EXISTS = 32

Already exists error.

Error ERR_DOES_NOT_EXIST = 33

Does not exist error.

Error ERR_DATABASE_CANT_READ = 34

Database: Read error.

Error ERR_DATABASE_CANT_WRITE = 35

Database: Write error.

Error ERR_COMPILATION_FAILED = 36

Compilation failed error.

Error ERR_METHOD_NOT_FOUND = 37

Method not found error.

Error ERR_LINK_FAILED = 38

Linking failed error.

Error ERR_SCRIPT_FAILED = 39

Error ERR_CYCLIC_LINK = 40

Cycling link (import cycle) error.

Error ERR_INVALID_DECLARATION = 41

Invalid declaration error.

Error ERR_DUPLICATE_SYMBOL = 42

Duplicate symbol error.

Error ERR_PARSE_ERROR = 43

Help error. Used internally when passing --version or --help as executable options.

Bug error, caused by an implementation issue in the method.

Note: If a built-in method returns this code, please open an issue on the GitHub Issue Tracker.

Error ERR_PRINTER_ON_FIRE = 48

Printer on fire error (This is an easter egg, no built-in methods return this error code).

PropertyHint PROPERTY_HINT_NONE = 0

The property has no hint for the editor.

PropertyHint PROPERTY_HINT_RANGE = 1

Hints that an int or float property should be within a range specified via the hint string "min,max" or "min,max,step". The hint string can optionally include "or_greater" and/or "or_less" to allow manual input going respectively above the max or below the min values.

Example: "-360,360,1,or_greater,or_less".

Additionally, other keywords can be included: "exp" for exponential range editing, "radians_as_degrees" for editing radian angles in degrees (the range values are also in degrees), "degrees" to hint at an angle and "hide_slider" to hide the slider.

PropertyHint PROPERTY_HINT_ENUM = 2

Hints that an int or String property is an enumerated value to pick in a list specified via a hint string.

The hint string is a comma separated list of names such as "Hello,Something,Else". Whitespaces are not removed from either end of a name. For integer properties, the first name in the list has value 0, the next 1, and so on. Explicit values can also be specified by appending :integer to the name, e.g. "Zero,One,Three:3,Four,Six:6".

PropertyHint PROPERTY_HINT_ENUM_SUGGESTION = 3

Hints that a String property can be an enumerated value to pick in a list specified via a hint string such as "Hello,Something,Else".

Unlike PROPERTY_HINT_ENUM, a property with this hint still accepts arbitrary values and can be empty. The list of values serves to suggest possible values.

PropertyHint PROPERTY_HINT_EXP_EASING = 4

Hints that a float property should be edited via an exponential easing function. The hint string can include "attenuation" to flip the curve horizontally and/or "positive_only" to exclude in/out easing and limit values to be greater than or equal to zero.

PropertyHint PROPERTY_HINT_LINK = 5

Hints that a vector property should allow its components to be linked. For example, this allows Vector2.x and Vector2.y to be edited together.

PropertyHint PROPERTY_HINT_FLAGS = 6

Hints that an int property is a bitmask with named bit flags.

The hint string is a comma separated list of names such as "Bit0,Bit1,Bit2,Bit3". Whitespaces are not removed from either end of a name. The first name in the list has value 1, the next 2, then 4, 8, 16 and so on. Explicit values can also be specified by appending :integer to the name, e.g. "A:4,B:8,C:16". You can also combine several flags ("A:4,B:8,AB:12,C:16").

Note: A flag value must be at least 1 and at most 2 ** 32 - 1.

Note: Unlike PROPERTY_HINT_ENUM, the previous explicit value is not taken into account. For the hint "A:16,B,C", A is 16, B is 2, C is 4.

PropertyHint PROPERTY_HINT_LAYERS_2D_RENDER = 7

Hints that an int property is a bitmask using the optionally named 2D render layers.

PropertyHint PROPERTY_HINT_LAYERS_2D_PHYSICS = 8

Hints that an int property is a bitmask using the optionally named 2D physics layers.

PropertyHint PROPERTY_HINT_LAYERS_2D_NAVIGATION = 9

Hints that an int property is a bitmask using the optionally named 2D navigation layers.

PropertyHint PROPERTY_HINT_LAYERS_3D_RENDER = 10

Hints that an int property is a bitmask using the optionally named 3D render layers.

PropertyHint PROPERTY_HINT_LAYERS_3D_PHYSICS = 11

Hints that an int property is a bitmask using the optionally named 3D physics layers.

PropertyHint PROPERTY_HINT_LAYERS_3D_NAVIGATION = 12

Hints that an int property is a bitmask using the optionally named 3D navigation layers.

PropertyHint PROPERTY_HINT_LAYERS_AVOIDANCE = 37

Hints that an integer property is a bitmask using the optionally named avoidance layers.

PropertyHint PROPERTY_HINT_FILE = 13

Hints that a String property is a path to a file. Editing it will show a file dialog for picking the path. The hint string can be a set of filters with wildcards like "*.png,*.jpg". By default the file will be stored as UID whenever available. You can use ResourceUID methods to convert it back to path. For storing a raw path, use PROPERTY_HINT_FILE_PATH.

PropertyHint PROPERTY_HINT_DIR = 14

Hints that a String property is a path to a directory. Editing it will show a file dialog for picking the path.

PropertyHint PROPERTY_HINT_GLOBAL_FILE = 15

Hints that a String property is an absolute path to a file outside the project folder. Editing it will show a file dialog for picking the path. The hint string can be a set of filters with wildcards, like "*.png,*.jpg".

PropertyHint PROPERTY_HINT_GLOBAL_DIR = 16

Hints that a String property is an absolute path to a directory outside the project folder. Editing it will show a file dialog for picking the path.

PropertyHint PROPERTY_HINT_RESOURCE_TYPE = 17

Hints that a property is an instance of a Resource-derived type, optionally specified via the hint string (e.g. "Texture2D"). Editing it will show a popup menu of valid resource types to instantiate.

PropertyHint PROPERTY_HINT_MULTILINE_TEXT = 18

Hints that a String property is text with line breaks. Editing it will show a text input field where line breaks can be typed.

PropertyHint PROPERTY_HINT_EXPRESSION = 19

Hints that a String property is an Expression.

PropertyHint PROPERTY_HINT_PLACEHOLDER_TEXT = 20

Hints that a String property should show a placeholder text on its input field, if empty. The hint string is the placeholder text to use.

PropertyHint PROPERTY_HINT_COLOR_NO_ALPHA = 21

Hints that a Color property should be edited without affecting its transparency (Color.a is not editable).

PropertyHint PROPERTY_HINT_OBJECT_ID = 22

Hints that the property's value is an object encoded as object ID, with its type specified in the hint string. Used by the debugger.

PropertyHint PROPERTY_HINT_TYPE_STRING = 23

If a property is String, hints that the property represents a particular type (class). This allows to select a type from the create dialog. The property will store the selected type as a string.

If a property is Array, hints the editor how to show elements. The hint_string must encode nested types using ":" and "/".

If a property is Dictionary, hints the editor how to show elements. The hint_string is the same as Array, with a ";" separating the key and value.

Note: The trailing colon is required for properly detecting built-in types.

PropertyHint PROPERTY_HINT_NODE_PATH_TO_EDITED_NODE = 24

Deprecated: This hint is not used by the engine.

PropertyHint PROPERTY_HINT_OBJECT_TOO_BIG = 25

Hints that an object is too big to be sent via the debugger.

PropertyHint PROPERTY_HINT_NODE_PATH_VALID_TYPES = 26

Hints that the hint string specifies valid node types for property of type NodePath.

PropertyHint PROPERTY_HINT_SAVE_FILE = 27

Hints that a String property is a path to a file. Editing it will show a file dialog for picking the path for the file to be saved at. The dialog has access to the project's directory. The hint string can be a set of filters with wildcards like "*.png,*.jpg". See also FileDialog.filters.

PropertyHint PROPERTY_HINT_GLOBAL_SAVE_FILE = 28

Hints that a String property is a path to a file. Editing it will show a file dialog for picking the path for the file to be saved at. The dialog has access to the entire filesystem. The hint string can be a set of filters with wildcards like "*.png,*.jpg". See also FileDialog.filters.

PropertyHint PROPERTY_HINT_INT_IS_OBJECTID = 29

Deprecated: This hint is not used by the engine.

PropertyHint PROPERTY_HINT_INT_IS_POINTER = 30

Hints that an int property is a pointer. Used by GDExtension.

PropertyHint PROPERTY_HINT_ARRAY_TYPE = 31

Hints that a property is an Array with the stored type specified in the hint string. The hint string contains the type of the array (e.g. "String").

Use the hint string format from PROPERTY_HINT_TYPE_STRING for more control over the stored type.

PropertyHint PROPERTY_HINT_DICTIONARY_TYPE = 38

Hints that a property is a Dictionary with the stored types specified in the hint string. The hint string contains the key and value types separated by a semicolon (e.g. "int;String").

Use the hint string format from PROPERTY_HINT_TYPE_STRING for more control over the stored types.

PropertyHint PROPERTY_HINT_LOCALE_ID = 32

Hints that a string property is a locale code. Editing it will show a locale dialog for picking language and country.

PropertyHint PROPERTY_HINT_LOCALIZABLE_STRING = 33

Hints that a dictionary property is string translation map. Dictionary keys are locale codes and, values are translated strings.

PropertyHint PROPERTY_HINT_NODE_TYPE = 34

Hints that a property is an instance of a Node-derived type, optionally specified via the hint string (e.g. "Node2D"). Editing it will show a dialog for picking a node from the scene.

PropertyHint PROPERTY_HINT_HIDE_QUATERNION_EDIT = 35

Hints that a quaternion property should disable the temporary euler editor.

PropertyHint PROPERTY_HINT_PASSWORD = 36

Hints that a string property is a password, and every character is replaced with the secret character.

PropertyHint PROPERTY_HINT_TOOL_BUTTON = 39

Hints that a Callable property should be displayed as a clickable button. When the button is pressed, the callable is called. The hint string specifies the button text and optionally an icon from the "EditorIcons" theme type.

Note: A Callable cannot be properly serialized and stored in a file, so it is recommended to use PROPERTY_USAGE_EDITOR instead of PROPERTY_USAGE_DEFAULT.

PropertyHint PROPERTY_HINT_ONESHOT = 40

Hints that a property will be changed on its own after setting, such as AudioStreamPlayer.playing or GPUParticles3D.emitting.

PropertyHint PROPERTY_HINT_GROUP_ENABLE = 42

Hints that a boolean property will enable the feature associated with the group that it occurs in. The property will be displayed as a checkbox on the group header. Only works within a group or subgroup.

By default, disabling the property hides all properties in the group. Use the optional hint string "checkbox_only" to disable this behavior.

PropertyHint PROPERTY_HINT_INPUT_NAME = 43

Hints that a String or StringName property is the name of an input action. This allows the selection of any action name from the Input Map in the Project Settings. The hint string may contain two options separated by commas:

If it contains "show_builtin", built-in input actions are included in the selection.

If it contains "loose_mode", loose mode is enabled. This allows inserting any action name even if it's not present in the input map.

PropertyHint PROPERTY_HINT_FILE_PATH = 44

Like PROPERTY_HINT_FILE, but the property is stored as a raw path, not UID. That means the reference will be broken if you move the file. Consider using PROPERTY_HINT_FILE when possible.

PropertyHint PROPERTY_HINT_MAX = 45

Represents the size of the PropertyHint enum.

flags PropertyUsageFlags: 🔗

PropertyUsageFlags PROPERTY_USAGE_NONE = 0

The property is not stored, and does not display in the editor. This is the default for non-exported properties.

PropertyUsageFlags PROPERTY_USAGE_STORAGE = 2

The property is serialized and saved in the scene file (default for exported properties).

PropertyUsageFlags PROPERTY_USAGE_EDITOR = 4

The property is shown in the EditorInspector (default for exported properties).

PropertyUsageFlags PROPERTY_USAGE_INTERNAL = 8

The property is excluded from the class reference.

PropertyUsageFlags PROPERTY_USAGE_CHECKABLE = 16

The property can be checked in the EditorInspector.

PropertyUsageFlags PROPERTY_USAGE_CHECKED = 32

The property is checked in the EditorInspector.

PropertyUsageFlags PROPERTY_USAGE_GROUP = 64

Used to group properties together in the editor. See EditorInspector.

PropertyUsageFlags PROPERTY_USAGE_CATEGORY = 128

Used to categorize properties together in the editor.

PropertyUsageFlags PROPERTY_USAGE_SUBGROUP = 256

Used to group properties together in the editor in a subgroup (under a group). See EditorInspector.

PropertyUsageFlags PROPERTY_USAGE_CLASS_IS_BITFIELD = 512

The property is a bitfield, i.e. it contains multiple flags represented as bits.

PropertyUsageFlags PROPERTY_USAGE_NO_INSTANCE_STATE = 1024

The property does not save its state in PackedScene.

PropertyUsageFlags PROPERTY_USAGE_RESTART_IF_CHANGED = 2048

Editing the property prompts the user for restarting the editor.

PropertyUsageFlags PROPERTY_USAGE_SCRIPT_VARIABLE = 4096

The property is a script variable. PROPERTY_USAGE_SCRIPT_VARIABLE can be used to distinguish between exported script variables from built-in variables (which don't have this usage flag). By default, PROPERTY_USAGE_SCRIPT_VARIABLE is not applied to variables that are created by overriding Object._get_property_list() in a script.

PropertyUsageFlags PROPERTY_USAGE_STORE_IF_NULL = 8192

The property value of type Object will be stored even if its value is null.

PropertyUsageFlags PROPERTY_USAGE_UPDATE_ALL_IF_MODIFIED = 16384

If this property is modified, all inspector fields will be refreshed.

PropertyUsageFlags PROPERTY_USAGE_SCRIPT_DEFAULT_VALUE = 32768

Deprecated: This flag is not used by the engine.

PropertyUsageFlags PROPERTY_USAGE_CLASS_IS_ENUM = 65536

The property is a variable of enum type, i.e. it only takes named integer constants from its associated enumeration.

PropertyUsageFlags PROPERTY_USAGE_NIL_IS_VARIANT = 131072

If property has nil as default value, its type will be Variant.

PropertyUsageFlags PROPERTY_USAGE_ARRAY = 262144

The property is an array.

PropertyUsageFlags PROPERTY_USAGE_ALWAYS_DUPLICATE = 524288

When duplicating a resource with Resource.duplicate(), and this flag is set on a property of that resource, the property should always be duplicated, regardless of the subresources bool parameter.

PropertyUsageFlags PROPERTY_USAGE_NEVER_DUPLICATE = 1048576

When duplicating a resource with Resource.duplicate(), and this flag is set on a property of that resource, the property should never be duplicated, regardless of the subresources bool parameter.

PropertyUsageFlags PROPERTY_USAGE_HIGH_END_GFX = 2097152

The property is only shown in the editor if modern renderers are supported (the Compatibility rendering method is excluded).

PropertyUsageFlags PROPERTY_USAGE_NODE_PATH_FROM_SCENE_ROOT = 4194304

The NodePath property will always be relative to the scene's root. Mostly useful for local resources.

PropertyUsageFlags PROPERTY_USAGE_RESOURCE_NOT_PERSISTENT = 8388608

Use when a resource is created on the fly, i.e. the getter will always return a different instance. ResourceSaver needs this information to properly save such resources.

PropertyUsageFlags PROPERTY_USAGE_KEYING_INCREMENTS = 16777216

Inserting an animation key frame of this property will automatically increment the value, allowing to easily keyframe multiple values in a row.

PropertyUsageFlags PROPERTY_USAGE_DEFERRED_SET_RESOURCE = 33554432

Deprecated: This flag is not used by the engine.

PropertyUsageFlags PROPERTY_USAGE_EDITOR_INSTANTIATE_OBJECT = 67108864

When this property is a Resource and base object is a Node, a resource instance will be automatically created whenever the node is created in the editor.

PropertyUsageFlags PROPERTY_USAGE_EDITOR_BASIC_SETTING = 134217728

The property is considered a basic setting and will appear even when advanced mode is disabled. Used for project settings.

PropertyUsageFlags PROPERTY_USAGE_READ_ONLY = 268435456

The property is read-only in the EditorInspector.

PropertyUsageFlags PROPERTY_USAGE_SECRET = 536870912

An export preset property with this flag contains confidential information and is stored separately from the rest of the export preset configuration.

PropertyUsageFlags PROPERTY_USAGE_DEFAULT = 6

Default usage (storage and editor).

PropertyUsageFlags PROPERTY_USAGE_NO_EDITOR = 2

Default usage but without showing the property in the editor (storage).

MethodFlags METHOD_FLAG_NORMAL = 1

Flag for a normal method.

MethodFlags METHOD_FLAG_EDITOR = 2

Flag for an editor method.

MethodFlags METHOD_FLAG_CONST = 4

Flag for a constant method.

MethodFlags METHOD_FLAG_VIRTUAL = 8

Flag for a virtual method.

MethodFlags METHOD_FLAG_VARARG = 16

Flag for a method with a variable number of arguments.

MethodFlags METHOD_FLAG_STATIC = 32

Flag for a static method.

MethodFlags METHOD_FLAG_OBJECT_CORE = 64

Used internally. Allows to not dump core virtual methods (such as Object._notification()) to the JSON API.

MethodFlags METHOD_FLAG_VIRTUAL_REQUIRED = 128

Flag for a virtual method that is required. In GDScript, this flag is set for abstract functions.

MethodFlags METHOD_FLAGS_DEFAULT = 1

Default method flags (normal).

Variant.Type TYPE_NIL = 0

Variant.Type TYPE_BOOL = 1

Variable is of type bool.

Variant.Type TYPE_INT = 2

Variable is of type int.

Variant.Type TYPE_FLOAT = 3

Variable is of type float.

Variant.Type TYPE_STRING = 4

Variable is of type String.

Variant.Type TYPE_VECTOR2 = 5

Variable is of type Vector2.

Variant.Type TYPE_VECTOR2I = 6

Variable is of type Vector2i.

Variant.Type TYPE_RECT2 = 7

Variable is of type Rect2.

Variant.Type TYPE_RECT2I = 8

Variable is of type Rect2i.

Variant.Type TYPE_VECTOR3 = 9

Variable is of type Vector3.

Variant.Type TYPE_VECTOR3I = 10

Variable is of type Vector3i.

Variant.Type TYPE_TRANSFORM2D = 11

Variable is of type Transform2D.

Variant.Type TYPE_VECTOR4 = 12

Variable is of type Vector4.

Variant.Type TYPE_VECTOR4I = 13

Variable is of type Vector4i.

Variant.Type TYPE_PLANE = 14

Variable is of type Plane.

Variant.Type TYPE_QUATERNION = 15

Variable is of type Quaternion.

Variant.Type TYPE_AABB = 16

Variable is of type AABB.

Variant.Type TYPE_BASIS = 17

Variable is of type Basis.

Variant.Type TYPE_TRANSFORM3D = 18

Variable is of type Transform3D.

Variant.Type TYPE_PROJECTION = 19

Variable is of type Projection.

Variant.Type TYPE_COLOR = 20

Variable is of type Color.

Variant.Type TYPE_STRING_NAME = 21

Variable is of type StringName.

Variant.Type TYPE_NODE_PATH = 22

Variable is of type NodePath.

Variant.Type TYPE_RID = 23

Variable is of type RID.

Variant.Type TYPE_OBJECT = 24

Variable is of type Object.

Variant.Type TYPE_CALLABLE = 25

Variable is of type Callable.

Variant.Type TYPE_SIGNAL = 26

Variable is of type Signal.

Variant.Type TYPE_DICTIONARY = 27

Variable is of type Dictionary.

Variant.Type TYPE_ARRAY = 28

Variable is of type Array.

Variant.Type TYPE_PACKED_BYTE_ARRAY = 29

Variable is of type PackedByteArray.

Variant.Type TYPE_PACKED_INT32_ARRAY = 30

Variable is of type PackedInt32Array.

Variant.Type TYPE_PACKED_INT64_ARRAY = 31

Variable is of type PackedInt64Array.

Variant.Type TYPE_PACKED_FLOAT32_ARRAY = 32

Variable is of type PackedFloat32Array.

Variant.Type TYPE_PACKED_FLOAT64_ARRAY = 33

Variable is of type PackedFloat64Array.

Variant.Type TYPE_PACKED_STRING_ARRAY = 34

Variable is of type PackedStringArray.

Variant.Type TYPE_PACKED_VECTOR2_ARRAY = 35

Variable is of type PackedVector2Array.

Variant.Type TYPE_PACKED_VECTOR3_ARRAY = 36

Variable is of type PackedVector3Array.

Variant.Type TYPE_PACKED_COLOR_ARRAY = 37

Variable is of type PackedColorArray.

Variant.Type TYPE_PACKED_VECTOR4_ARRAY = 38

Variable is of type PackedVector4Array.

Variant.Type TYPE_MAX = 39

Represents the size of the Variant.Type enum.

enum Variant.Operator: 🔗

Variant.Operator OP_EQUAL = 0

Equality operator (==).

Variant.Operator OP_NOT_EQUAL = 1

Inequality operator (!=).

Variant.Operator OP_LESS = 2

Less than operator (<).

Variant.Operator OP_LESS_EQUAL = 3

Less than or equal operator (<=).

Variant.Operator OP_GREATER = 4

Greater than operator (>).

Variant.Operator OP_GREATER_EQUAL = 5

Greater than or equal operator (>=).

Variant.Operator OP_ADD = 6

Addition operator (+).

Variant.Operator OP_SUBTRACT = 7

Subtraction operator (-).

Variant.Operator OP_MULTIPLY = 8

Multiplication operator (*).

Variant.Operator OP_DIVIDE = 9

Division operator (/).

Variant.Operator OP_NEGATE = 10

Unary negation operator (-).

Variant.Operator OP_POSITIVE = 11

Unary plus operator (+).

Variant.Operator OP_MODULE = 12

Remainder/modulo operator (%).

Variant.Operator OP_POWER = 13

Variant.Operator OP_SHIFT_LEFT = 14

Left shift operator (<<).

Variant.Operator OP_SHIFT_RIGHT = 15

Right shift operator (>>).

Variant.Operator OP_BIT_AND = 16

Bitwise AND operator (&).

Variant.Operator OP_BIT_OR = 17

Bitwise OR operator (|).

Variant.Operator OP_BIT_XOR = 18

Bitwise XOR operator (^).

Variant.Operator OP_BIT_NEGATE = 19

Bitwise NOT operator (~).

Variant.Operator OP_AND = 20

Logical AND operator (and or &&).

Variant.Operator OP_OR = 21

Logical OR operator (or or ||).

Variant.Operator OP_XOR = 22

Logical XOR operator (not implemented in GDScript).

Variant.Operator OP_NOT = 23

Logical NOT operator (not or !).

Variant.Operator OP_IN = 24

Logical IN operator (in).

Variant.Operator OP_MAX = 25

Represents the size of the Variant.Operator enum.

AudioServer AudioServer 🔗

The AudioServer singleton.

CameraServer CameraServer 🔗

The CameraServer singleton.

The ClassDB singleton.

DisplayServer DisplayServer 🔗

The DisplayServer singleton.

EditorInterface EditorInterface 🔗

The EditorInterface singleton.

Note: Only available in editor builds.

The Engine singleton.

EngineDebugger EngineDebugger 🔗

The EngineDebugger singleton.

GDExtensionManager GDExtensionManager 🔗

The GDExtensionManager singleton.

Geometry2D Geometry2D 🔗

The Geometry2D singleton.

Geometry3D Geometry3D 🔗

The Geometry3D singleton.

The InputMap singleton.

JavaClassWrapper JavaClassWrapper 🔗

The JavaClassWrapper singleton.

Note: Only implemented on Android.

JavaScriptBridge JavaScriptBridge 🔗

The JavaScriptBridge singleton.

Note: Only implemented on the Web platform.

Marshalls Marshalls 🔗

The Marshalls singleton.

NativeMenu NativeMenu 🔗

The NativeMenu singleton.

Note: Only implemented on macOS.

NavigationMeshGenerator NavigationMeshGenerator 🔗

The NavigationMeshGenerator singleton.

NavigationServer2D NavigationServer2D 🔗

The NavigationServer2D singleton.

NavigationServer3D NavigationServer3D 🔗

The NavigationServer3D singleton.

Performance Performance 🔗

The Performance singleton.

PhysicsServer2D PhysicsServer2D 🔗

The PhysicsServer2D singleton.

PhysicsServer2DManager PhysicsServer2DManager 🔗

The PhysicsServer2DManager singleton.

PhysicsServer3D PhysicsServer3D 🔗

The PhysicsServer3D singleton.

PhysicsServer3DManager PhysicsServer3DManager 🔗

The PhysicsServer3DManager singleton.

ProjectSettings ProjectSettings 🔗

The ProjectSettings singleton.

RenderingServer RenderingServer 🔗

The RenderingServer singleton.

ResourceLoader ResourceLoader 🔗

The ResourceLoader singleton.

ResourceSaver ResourceSaver 🔗

The ResourceSaver singleton.

ResourceUID ResourceUID 🔗

The ResourceUID singleton.

TextServerManager TextServerManager 🔗

The TextServerManager singleton.

The ThemeDB singleton.

TranslationServer TranslationServer 🔗

The TranslationServer singleton.

WorkerThreadPool WorkerThreadPool 🔗

The WorkerThreadPool singleton.

The XRServer singleton.

Variant abs(x: Variant) 🔗

Returns the absolute value of a Variant parameter x (i.e. non-negative value). Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

Note: For better type safety, use absf(), absi(), Vector2.abs(), Vector2i.abs(), Vector3.abs(), Vector3i.abs(), Vector4.abs(), or Vector4i.abs().

float absf(x: float) 🔗

Returns the absolute value of float parameter x (i.e. positive value).

Returns the absolute value of int parameter x (i.e. positive value).

float acos(x: float) 🔗

Returns the arc cosine of x in radians. Use to get the angle of cosine x. x will be clamped between -1.0 and 1.0 (inclusive), in order to prevent acos() from returning @GDScript.NAN.

float acosh(x: float) 🔗

Returns the hyperbolic arc (also called inverse) cosine of x, returning a value in radians. Use it to get the angle from an angle's cosine in hyperbolic space if x is larger or equal to 1. For values of x lower than 1, it will return 0, in order to prevent acosh() from returning @GDScript.NAN.

float angle_difference(from: float, to: float) 🔗

Returns the difference between the two angles (in radians), in the range of [-PI, +PI]. When from and to are opposite, returns -PI if from is smaller than to, or PI otherwise.

float asin(x: float) 🔗

Returns the arc sine of x in radians. Use to get the angle of sine x. x will be clamped between -1.0 and 1.0 (inclusive), in order to prevent asin() from returning @GDScript.NAN.

float asinh(x: float) 🔗

Returns the hyperbolic arc (also called inverse) sine of x, returning a value in radians. Use it to get the angle from an angle's sine in hyperbolic space.

float atan(x: float) 🔗

Returns the arc tangent of x in radians. Use it to get the angle from an angle's tangent in trigonometry.

The method cannot know in which quadrant the angle should fall. See atan2() if you have both y and x.

If x is between -PI / 2 and PI / 2 (inclusive), atan(tan(x)) is equal to x.

float atan2(y: float, x: float) 🔗

Returns the arc tangent of y/x in radians. Use to get the angle of tangent y/x. To compute the value, the method takes into account the sign of both arguments in order to determine the quadrant.

Important note: The Y coordinate comes first, by convention.

float atanh(x: float) 🔗

Returns the hyperbolic arc (also called inverse) tangent of x, returning a value in radians. Use it to get the angle from an angle's tangent in hyperbolic space if x is between -1 and 1 (non-inclusive).

In mathematics, the inverse hyperbolic tangent is only defined for -1 < x < 1 in the real set, so values equal or lower to -1 for x return negative @GDScript.INF and values equal or higher than 1 return positive @GDScript.INF in order to prevent atanh() from returning @GDScript.NAN.

float bezier_derivative(start: float, control_1: float, control_2: float, end: float, t: float) 🔗

Returns the derivative at the given t on a one-dimensional Bézier curve defined by the given control_1, control_2, and end points.

float bezier_interpolate(start: float, control_1: float, control_2: float, end: float, t: float) 🔗

Returns the point at the given t on a one-dimensional Bézier curve defined by the given control_1, control_2, and end points.

Variant bytes_to_var(bytes: PackedByteArray) 🔗

Decodes a byte array back to a Variant value, without decoding objects.

Note: If you need object deserialization, see bytes_to_var_with_objects().

Variant bytes_to_var_with_objects(bytes: PackedByteArray) 🔗

Decodes a byte array back to a Variant value. Decoding objects is allowed.

Warning: Deserialized object can contain code which gets executed. Do not use this option if the serialized object comes from untrusted sources to avoid potential security threats (remote code execution).

Variant ceil(x: Variant) 🔗

Rounds x upward (towards positive infinity), returning the smallest whole number that is not less than x. Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

See also floor(), round(), and snapped().

Note: For better type safety, use ceilf(), ceili(), Vector2.ceil(), Vector3.ceil(), or Vector4.ceil().

float ceilf(x: float) 🔗

Rounds x upward (towards positive infinity), returning the smallest whole number that is not less than x.

A type-safe version of ceil(), returning a float.

int ceili(x: float) 🔗

Rounds x upward (towards positive infinity), returning the smallest whole number that is not less than x.

A type-safe version of ceil(), returning an int.

Variant clamp(value: Variant, min: Variant, max: Variant) 🔗

Clamps the value, returning a Variant not less than min and not more than max. Any values that can be compared with the less than and greater than operators will work.

Note: For better type safety, use clampf(), clampi(), Vector2.clamp(), Vector2i.clamp(), Vector3.clamp(), Vector3i.clamp(), Vector4.clamp(), Vector4i.clamp(), or Color.clamp() (not currently supported by this method).

Note: When using this on vectors it will not perform component-wise clamping, and will pick min if value < min or max if value > max. To perform component-wise clamping use the methods listed above.

float clampf(value: float, min: float, max: float) 🔗

Clamps the value, returning a float not less than min and not more than max.

int clampi(value: int, min: int, max: int) 🔗

Clamps the value, returning an int not less than min and not more than max.

float cos(angle_rad: float) 🔗

Returns the cosine of angle angle_rad in radians.

float cosh(x: float) 🔗

Returns the hyperbolic cosine of x in radians.

float cubic_interpolate(from: float, to: float, pre: float, post: float, weight: float) 🔗

Cubic interpolates between two values by the factor defined in weight with pre and post values.

float cubic_interpolate_angle(from: float, to: float, pre: float, post: float, weight: float) 🔗

Cubic interpolates between two rotation values with shortest path by the factor defined in weight with pre and post values. See also lerp_angle().

float cubic_interpolate_angle_in_time(from: float, to: float, pre: float, post: float, weight: float, to_t: float, pre_t: float, post_t: float) 🔗

Cubic interpolates between two rotation values with shortest path by the factor defined in weight with pre and post values. See also lerp_angle().

It can perform smoother interpolation than cubic_interpolate() by the time values.

float cubic_interpolate_in_time(from: float, to: float, pre: float, post: float, weight: float, to_t: float, pre_t: float, post_t: float) 🔗

Cubic interpolates between two values by the factor defined in weight with pre and post values.

It can perform smoother interpolation than cubic_interpolate() by the time values.

float db_to_linear(db: float) 🔗

Converts from decibels to linear energy (audio).

float deg_to_rad(deg: float) 🔗

Converts an angle expressed in degrees to radians.

float ease(x: float, curve: float) 🔗

Returns an "eased" value of x based on an easing function defined with curve. This easing function is based on an exponent. The curve can be any floating-point number, with specific values leading to the following behaviors:

ease() curve values cheatsheet

See also smoothstep(). If you need to perform more advanced transitions, use Tween.interpolate_value().

String error_string(error: int) 🔗

Returns a human-readable name for the given Error code.

float exp(x: float) 🔗

The natural exponential function. It raises the mathematical constant e to the power of x and returns it.

e has an approximate value of 2.71828, and can be obtained with exp(1).

For exponents to other bases use the method pow().

Variant floor(x: Variant) 🔗

Rounds x downward (towards negative infinity), returning the largest whole number that is not more than x. Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

See also ceil(), round(), and snapped().

Note: For better type safety, use floorf(), floori(), Vector2.floor(), Vector3.floor(), or Vector4.floor().

float floorf(x: float) 🔗

Rounds x downward (towards negative infinity), returning the largest whole number that is not more than x.

A type-safe version of floor(), returning a float.

int floori(x: float) 🔗

Rounds x downward (towards negative infinity), returning the largest whole number that is not more than x.

A type-safe version of floor(), returning an int.

Note: This function is not the same as int(x), which rounds towards 0.

float fmod(x: float, y: float) 🔗

Returns the floating-point remainder of x divided by y, keeping the sign of x.

For the integer remainder operation, use the % operator.

float fposmod(x: float, y: float) 🔗

Returns the floating-point modulus of x divided by y, wrapping equally in positive and negative.

int hash(variable: Variant) 🔗

Returns the integer hash of the passed variable.

Object instance_from_id(instance_id: int) 🔗

Returns the Object that corresponds to instance_id. All Objects have a unique instance ID. See also Object.get_instance_id().

float inverse_lerp(from: float, to: float, weight: float) 🔗

Returns an interpolation or extrapolation factor considering the range specified in from and to, and the interpolated value specified in weight. The returned value will be between 0.0 and 1.0 if weight is between from and to (inclusive). If weight is located outside this range, then an extrapolation factor will be returned (return value lower than 0.0 or greater than 1.0). Use clamp() on the result of inverse_lerp() if this is not desired.

See also lerp(), which performs the reverse of this operation, and remap() to map a continuous series of values to another.

bool is_equal_approx(a: float, b: float) 🔗

Returns true if a and b are approximately equal to each other.

Here, "approximately equal" means that a and b are within a small internal epsilon of each other, which scales with the magnitude of the numbers.

Infinity values of the same sign are considered equal.

bool is_finite(x: float) 🔗

Returns whether x is a finite value, i.e. it is not @GDScript.NAN, positive infinity, or negative infinity. See also is_inf() and is_nan().

bool is_inf(x: float) 🔗

Returns true if x is either positive infinity or negative infinity. See also is_finite() and is_nan().

bool is_instance_id_valid(id: int) 🔗

Returns true if the Object that corresponds to id is a valid object (e.g. has not been deleted from memory). All Objects have a unique instance ID.

bool is_instance_valid(instance: Variant) 🔗

Returns true if instance is a valid Object (e.g. has not been deleted from memory).

bool is_nan(x: float) 🔗

Returns true if x is a NaN ("Not a Number" or invalid) value. This method is needed as @GDScript.NAN is not equal to itself, which means x == NAN can't be used to check whether a value is a NaN.

bool is_same(a: Variant, b: Variant) 🔗

Returns true, for value types, if a and b share the same value. Returns true, for reference types, if the references of a and b are the same.

These are Variant value types: null, bool, int, float, String, StringName, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i, Rect2, Rect2i, Transform2D, Transform3D, Plane, Quaternion, AABB, Basis, Projection, Color, NodePath, RID, Callable and Signal.

These are Variant reference types: Object, Dictionary, Array, PackedByteArray, PackedInt32Array, PackedInt64Array, PackedFloat32Array, PackedFloat64Array, PackedStringArray, PackedVector2Array, PackedVector3Array, PackedVector4Array, and PackedColorArray.

bool is_zero_approx(x: float) 🔗

Returns true if x is zero or almost zero. The comparison is done using a tolerance calculation with a small internal epsilon.

This function is faster than using is_equal_approx() with one value as zero.

Variant lerp(from: Variant, to: Variant, weight: Variant) 🔗

Linearly interpolates between two values by the factor defined in weight. To perform interpolation, weight should be between 0.0 and 1.0 (inclusive). However, values outside this range are allowed and can be used to perform extrapolation. If this is not desired, use clampf() to limit weight.

Both from and to must be the same type. Supported types: int, float, Vector2, Vector3, Vector4, Color, Quaternion, Basis, Transform2D, Transform3D.

See also inverse_lerp() which performs the reverse of this operation. To perform eased interpolation with lerp(), combine it with ease() or smoothstep(). See also remap() to map a continuous series of values to another.

Note: For better type safety, use lerpf(), Vector2.lerp(), Vector3.lerp(), Vector4.lerp(), Color.lerp(), Quaternion.slerp(), Basis.slerp(), Transform2D.interpolate_with(), or Transform3D.interpolate_with().

float lerp_angle(from: float, to: float, weight: float) 🔗

Linearly interpolates between two angles (in radians) by a weight value between 0.0 and 1.0.

Similar to lerp(), but interpolates correctly when the angles wrap around @GDScript.TAU. To perform eased interpolation with lerp_angle(), combine it with ease() or smoothstep().

Note: This function lerps through the shortest path between from and to. However, when these two angles are approximately PI + k * TAU apart for any integer k, it's not obvious which way they lerp due to floating-point precision errors. For example, lerp_angle(0, PI, weight) lerps counter-clockwise, while lerp_angle(0, PI + 5 * TAU, weight) lerps clockwise.

float lerpf(from: float, to: float, weight: float) 🔗

Linearly interpolates between two values by the factor defined in weight. To perform interpolation, weight should be between 0.0 and 1.0 (inclusive). However, values outside this range are allowed and can be used to perform extrapolation. If this is not desired, use clampf() on the result of this function.

See also inverse_lerp() which performs the reverse of this operation. To perform eased interpolation with lerp(), combine it with ease() or smoothstep().

float linear_to_db(lin: float) 🔗

Converts from linear energy to decibels (audio). Since volume is not normally linear, this can be used to implement volume sliders that behave as expected.

Example: Change the Master bus's volume through a Slider node, which ranges from 0.0 to 1.0:

float log(x: float) 🔗

Returns the natural logarithm of x (base [i]e[/i], with e being approximately 2.71828). This is the amount of time needed to reach a certain level of continuous growth.

Note: This is not the same as the "log" function on most calculators, which uses a base 10 logarithm. To use base 10 logarithm, use log(x) / log(10).

Note: The logarithm of 0 returns -inf, while negative values return -nan.

Variant max(...) vararg 🔗

Returns the maximum of the given numeric values. This function can take any number of arguments.

Note: When using this on vectors it will not perform component-wise maximum, and will pick the largest value when compared using x < y. To perform component-wise maximum, use Vector2.max(), Vector2i.max(), Vector3.max(), Vector3i.max(), Vector4.max(), and Vector4i.max().

float maxf(a: float, b: float) 🔗

Returns the maximum of two float values.

int maxi(a: int, b: int) 🔗

Returns the maximum of two int values.

Variant min(...) vararg 🔗

Returns the minimum of the given numeric values. This function can take any number of arguments.

Note: When using this on vectors it will not perform component-wise minimum, and will pick the smallest value when compared using x < y. To perform component-wise minimum, use Vector2.min(), Vector2i.min(), Vector3.min(), Vector3i.min(), Vector4.min(), and Vector4i.min().

float minf(a: float, b: float) 🔗

Returns the minimum of two float values.

int mini(a: int, b: int) 🔗

Returns the minimum of two int values.

float move_toward(from: float, to: float, delta: float) 🔗

Moves from toward to by the delta amount. Will not go past to.

Use a negative delta value to move away.

int nearest_po2(value: int) 🔗

Returns the smallest integer power of 2 that is greater than or equal to value.

Warning: Due to its implementation, this method returns 0 rather than 1 for values less than or equal to 0, with an exception for value being the smallest negative 64-bit integer (-9223372036854775808) in which case the value is returned unchanged.

float pingpong(value: float, length: float) 🔗

Wraps value between 0 and the length. If the limit is reached, the next value the function returns is decreased to the 0 side or increased to the length side (like a triangle wave). If length is less than zero, it becomes positive.

int posmod(x: int, y: int) 🔗

Returns the integer modulus of x divided by y that wraps equally in positive and negative.

float pow(base: float, exp: float) 🔗

Returns the result of base raised to the power of exp.

In GDScript, this is the equivalent of the ** operator.

void print(...) vararg 🔗

Converts one or more arguments of any type to string in the best way possible and prints them to the console.

Note: Consider using push_error() and push_warning() to print error and warning messages instead of print() or print_rich(). This distinguishes them from print messages used for debugging purposes, while also displaying a stack trace when an error or warning is printed. See also Engine.print_to_stdout and ProjectSettings.application/run/disable_stdout.

void print_rich(...) vararg 🔗

Converts one or more arguments of any type to string in the best way possible and prints them to the console.

The following BBCode tags are supported: b, i, u, s, indent, code, url, center, right, color, bgcolor, fgcolor.

URL tags only support URLs wrapped by a URL tag, not URLs with a different title.

When printing to standard output, the supported subset of BBCode is converted to ANSI escape codes for the terminal emulator to display. Support for ANSI escape codes varies across terminal emulators, especially for italic and strikethrough. In standard output, code is represented with faint text but without any font change. Unsupported tags are left as-is in standard output.

Note: Consider using push_error() and push_warning() to print error and warning messages instead of print() or print_rich(). This distinguishes them from print messages used for debugging purposes, while also displaying a stack trace when an error or warning is printed.

Note: Output displayed in the editor supports clickable [url=address]text[/url] tags. The [url] tag's address value is handled by OS.shell_open() when clicked.

void print_verbose(...) vararg 🔗

If verbose mode is enabled (OS.is_stdout_verbose() returning true), converts one or more arguments of any type to string in the best way possible and prints them to the console.

void printerr(...) vararg 🔗

Prints one or more arguments to strings in the best way possible to standard error line.

void printraw(...) vararg 🔗

Prints one or more arguments to strings in the best way possible to the OS terminal. Unlike print(), no newline is automatically added at the end.

Note: The OS terminal is not the same as the editor's Output dock. The output sent to the OS terminal can be seen when running Godot from a terminal. On Windows, this requires using the console.exe executable.

void prints(...) vararg 🔗

Prints one or more arguments to the console with a space between each argument.

void printt(...) vararg 🔗

Prints one or more arguments to the console with a tab between each argument.

void push_error(...) vararg 🔗

Pushes an error message to Godot's built-in debugger and to the OS terminal.

Note: This function does not pause project execution. To print an error message and pause project execution in debug builds, use assert(false, "test error") instead.

void push_warning(...) vararg 🔗

Pushes a warning message to Godot's built-in debugger and to the OS terminal.

float rad_to_deg(rad: float) 🔗

Converts an angle expressed in radians to degrees.

PackedInt64Array rand_from_seed(seed: int) 🔗

Given a seed, returns a PackedInt64Array of size 2, where its first element is the randomized int value, and the second element is the same as seed. Passing the same seed consistently returns the same array.

Note: "Seed" here refers to the internal state of the pseudo random number generator, currently implemented as a 64 bit integer.

Returns a random floating-point value between 0.0 and 1.0 (inclusive).

float randf_range(from: float, to: float) 🔗

Returns a random floating-point value between from and to (inclusive).

float randfn(mean: float, deviation: float) 🔗

Returns a normally-distributed, pseudo-random floating-point value from the specified mean and a standard deviation. This is also known as a Gaussian distribution.

Note: This method uses the Box-Muller transform algorithm.

Returns a random unsigned 32-bit integer. Use remainder to obtain a random value in the interval [0, N - 1] (where N is smaller than 2^32).

int randi_range(from: int, to: int) 🔗

Returns a random signed 32-bit integer between from and to (inclusive). If to is lesser than from, they are swapped.

Randomizes the seed (or the internal state) of the random number generator. The current implementation uses a number based on the device's time.

Note: This function is called automatically when the project is run. If you need to fix the seed to have consistent, reproducible results, use seed() to initialize the random number generator.

float remap(value: float, istart: float, istop: float, ostart: float, ostop: float) 🔗

Maps a value from range [istart, istop] to [ostart, ostop]. See also lerp() and inverse_lerp(). If value is outside [istart, istop], then the resulting value will also be outside [ostart, ostop]. If this is not desired, use clamp() on the result of this function.

For complex use cases where multiple ranges are needed, consider using Curve or Gradient instead.

Note: If istart == istop, the return value is undefined (most likely NaN, INF, or -INF).

int rid_allocate_id() 🔗

Allocates a unique ID which can be used by the implementation to construct an RID. This is used mainly from native extensions to implement servers.

RID rid_from_int64(base: int) 🔗

Creates an RID from a base. This is used mainly from native extensions to build servers.

float rotate_toward(from: float, to: float, delta: float) 🔗

Rotates from toward to by the delta amount. Will not go past to.

Similar to move_toward(), but interpolates correctly when the angles wrap around @GDScript.TAU.

If delta is negative, this function will rotate away from to, toward the opposite angle, and will not go past the opposite angle.

Variant round(x: Variant) 🔗

Rounds x to the nearest whole number, with halfway cases rounded away from 0. Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

See also floor(), ceil(), and snapped().

Note: For better type safety, use roundf(), roundi(), Vector2.round(), Vector3.round(), or Vector4.round().

float roundf(x: float) 🔗

Rounds x to the nearest whole number, with halfway cases rounded away from 0.

A type-safe version of round(), returning a float.

int roundi(x: float) 🔗

Rounds x to the nearest whole number, with halfway cases rounded away from 0.

A type-safe version of round(), returning an int.

void seed(base: int) 🔗

Sets the seed for the random number generator to base. Setting the seed manually can ensure consistent, repeatable results for most random functions.

Variant sign(x: Variant) 🔗

Returns the same type of Variant as x, with -1 for negative values, 1 for positive values, and 0 for zeros. For nan values it returns 0.

Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

Note: For better type safety, use signf(), signi(), Vector2.sign(), Vector2i.sign(), Vector3.sign(), Vector3i.sign(), Vector4.sign(), or Vector4i.sign().

float signf(x: float) 🔗

Returns -1.0 if x is negative, 1.0 if x is positive, and 0.0 if x is zero. For nan values of x it returns 0.0.

Returns -1 if x is negative, 1 if x is positive, and 0 if x is zero.

float sin(angle_rad: float) 🔗

Returns the sine of angle angle_rad in radians.

float sinh(x: float) 🔗

Returns the hyperbolic sine of x.

float smoothstep(from: float, to: float, x: float) 🔗

Returns a smooth cubic Hermite interpolation between 0 and 1.

For positive ranges (when from <= to) the return value is 0 when x <= from, and 1 when x >= to. If x lies between from and to, the return value follows an S-shaped curve that smoothly transitions from 0 to 1.

For negative ranges (when from > to) the function is mirrored and returns 1 when x <= to and 0 when x >= from.

This S-shaped curve is the cubic Hermite interpolator, given by f(y) = 3*y^2 - 2*y^3 where y = (x-from) / (to-from).

Compared to ease() with a curve value of -1.6521, smoothstep() returns the smoothest possible curve with no sudden changes in the derivative. If you need to perform more advanced transitions, use Tween or AnimationPlayer.

Comparison between smoothstep() and ease(x, -1.6521) return values

Smoothstep() return values with positive, zero, and negative ranges

Variant snapped(x: Variant, step: Variant) 🔗

Returns the multiple of step that is the closest to x. This can also be used to round a floating-point number to an arbitrary number of decimals.

The returned value is the same type of Variant as step. Supported types: int, float, Vector2, Vector2i, Vector3, Vector3i, Vector4, Vector4i.

See also ceil(), floor(), and round().

Note: For better type safety, use snappedf(), snappedi(), Vector2.snapped(), Vector2i.snapped(), Vector3.snapped(), Vector3i.snapped(), Vector4.snapped(), or Vector4i.snapped().

float snappedf(x: float, step: float) 🔗

Returns the multiple of step that is the closest to x. This can also be used to round a floating-point number to an arbitrary number of decimals.

A type-safe version of snapped(), returning a float.

int snappedi(x: float, step: int) 🔗

Returns the multiple of step that is the closest to x.

A type-safe version of snapped(), returning an int.

float sqrt(x: float) 🔗

Returns the square root of x, where x is a non-negative number.

Note: Negative values of x return NaN ("Not a Number"). In C#, if you need negative inputs, use System.Numerics.Complex.

int step_decimals(x: float) 🔗

Returns the position of the first non-zero digit, after the decimal point. Note that the maximum return value is 10, which is a design decision in the implementation.

String str(...) vararg 🔗

Converts one or more arguments of any Variant type to a String in the best way possible.

Variant str_to_var(string: String) 🔗

Converts a formatted string that was returned by var_to_str() to the original Variant.

float tan(angle_rad: float) 🔗

Returns the tangent of angle angle_rad in radians.

float tanh(x: float) 🔗

Returns the hyperbolic tangent of x.

Variant type_convert(variant: Variant, type: int) 🔗

Converts the given variant to the given type, using the Variant.Type values. This method is generous with how it handles types, it can automatically convert between array types, convert numeric Strings to int, and converting most things to String.

If the type conversion cannot be done, this method will return the default value for that type, for example converting Rect2 to Vector2 will always return Vector2.ZERO. This method will never show error messages as long as type is a valid Variant type.

The returned value is a Variant, but the data inside and its type will be the same as the requested type.

String type_string(type: int) 🔗

Returns a human-readable name of the given type, using the Variant.Type values.

int typeof(variable: Variant) 🔗

Returns the internal type of the given variable, using the Variant.Type values.

See also type_string().

PackedByteArray var_to_bytes(variable: Variant) 🔗

Encodes a Variant value to a byte array, without encoding objects. Deserialization can be done with bytes_to_var().

Note: If you need object serialization, see var_to_bytes_with_objects().

Note: Encoding Callable is not supported and will result in an empty value, regardless of the data.

PackedByteArray var_to_bytes_with_objects(variable: Variant) 🔗

Encodes a Variant value to a byte array. Encoding objects is allowed (and can potentially include executable code). Deserialization can be done with bytes_to_var_with_objects().

Note: Encoding Callable is not supported and will result in an empty value, regardless of the data.

String var_to_str(variable: Variant) 🔗

Converts a Variant variable to a formatted String that can then be parsed using str_to_var().

Note: Converting Signal or Callable is not supported and will result in an empty value for these types, regardless of their data.

Variant weakref(obj: Variant) 🔗

Returns a WeakRef instance holding a weak reference to obj. Returns an empty WeakRef instance if obj is null. Prints an error and returns null if obj is neither Object-derived nor null.

A weak reference to an object is not enough to keep the object alive: when the only remaining references to a referent are weak references, garbage collection is free to destroy the referent and reuse its memory for something else. However, until the object is actually destroyed the weak reference may return the object even if there are no strong references to it.

Variant wrap(value: Variant, min: Variant, max: Variant) 🔗

Wraps the Variant value between min and max. min is inclusive while max is exclusive. This can be used for creating loop-like behavior or infinite surfaces.

Variant types int and float are supported. If any of the arguments is float, this function returns a float, otherwise it returns an int.

float wrapf(value: float, min: float, max: float) 🔗

Wraps the float value between min and max. min is inclusive while max is exclusive. This can be used for creating loop-like behavior or infinite surfaces.

Note: If min is 0, this is equivalent to fposmod(), so prefer using that instead. wrapf() is more flexible than using the fposmod() approach by giving the user control over the minimum value.

int wrapi(value: int, min: int, max: int) 🔗

Wraps the integer value between min and max. min is inclusive while max is exclusive. This can be used for creating loop-like behavior or infinite surfaces.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var error = method_that_returns_error()
if error != OK:
    printerr("Failure!")

# Or, alternatively:
if error:
    printerr("Still failing!")
```

Example 2 (markdown):
```markdown
# Array of elem_type.
hint_string = "%d:" % [elem_type]
hint_string = "%d/%d:%s" % [elem_type, elem_hint, elem_hint_string]
# Two-dimensional array of elem_type (array of arrays of elem_type).
hint_string = "%d:%d:" % [TYPE_ARRAY, elem_type]
hint_string = "%d:%d/%d:%s" % [TYPE_ARRAY, elem_type, elem_hint, elem_hint_string]
# Three-dimensional array of elem_type (array of arrays of arrays of elem_type).
hint_string = "%d:%d:%d:" % [TYPE_ARRAY, TYPE_ARRAY, elem_type]
hint_string = "%d:%d:%d/%d:%s" % [TYPE_ARRAY, TYPE_ARRAY, elem_type, elem_hint, elem_hint_string]
```

Example 3 (css):
```css
// Array of elemType.
hintString = $"{elemType:D}:";
hintString = $"{elemType:}/{elemHint:D}:{elemHintString}";
// Two-dimensional array of elemType (array of arrays of elemType).
hintString = $"{Variant.Type.Array:D}:{elemType:D}:";
hintString = $"{Variant.Type.Array:D}:{elemType:D}/{elemHint:D}:{elemHintString}";
// Three-dimensional array of elemType (array of arrays of arrays of elemType).
hintString = $"{Variant.Type.Array:D}:{Variant.Type.Array:D}:{elemType:D}:";
hintString = $"{Variant.Type.Array:D}:{Variant.Type.Array:D}:{elemType:D}/{elemHint:D}:{elemHintString}";
```

Example 4 (sql):
```sql
hint_string = "%d:" % [TYPE_INT] # Array of integers.
hint_string = "%d/%d:1,10,1" % [TYPE_INT, PROPERTY_HINT_RANGE] # Array of integers (in range from 1 to 10).
hint_string = "%d/%d:Zero,One,Two" % [TYPE_INT, PROPERTY_HINT_ENUM] # Array of integers (an enum).
hint_string = "%d/%d:Zero,One,Three:3,Six:6" % [TYPE_INT, PROPERTY_HINT_ENUM] # Array of integers (an enum).
hint_string = "%d/%d:*.png" % [TYPE_STRING, PROPERTY_HINT_FILE] # Array of strings (file paths).
hint_string = "%d/%d:Texture2D" % [TYPE_OBJECT, PROPERTY_HINT_RESOURCE_TYPE] # Array of textures.

hint_string = "%d:%d:" % [TYPE_ARRAY, TYPE_FLOAT] # Two-dimensional array of floats.
hint_string = "%d:%d/%d:" % [TYPE_ARRAY, TYPE_STRING, PROPERTY_HINT_MULTILINE_TEXT] # Two-dimensional array of multiline strings.
hint_string = "%d:%d/%d:-1,1,0.1" % [TYPE_ARRAY, TYPE_FLOAT, PROPERTY_HINT_RANGE] # Two-dimensional array of floats (in range from -1 to 1).
hint_string = "%d:%d/%d:Texture2D" % [TYPE_ARRAY, TYPE_OBJECT, PROPERTY_HINT_RESOURCE_TYPE] # Two-dimensional array of textures.
```

---
