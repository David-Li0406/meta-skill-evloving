# Godot - Export

**Pages:** 28

---

## Upgrading from Godot 4.4 to Godot 4.5 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.5.html

**Contents:**
- Upgrading from Godot 4.4 to Godot 4.5
- Breaking changes
  - Core
  - Rendering
  - GLTF
  - Text
  - XR
  - Editor plugins
- Behavior changes
  - TileMapLayer

For most games and apps made with 4.4 it should be relatively safe to migrate to 4.5. This page intends to cover everything you need to pay attention to when migrating your project.

If you are migrating from 4.4 to 4.5, the breaking changes listed here might affect you. Changes are grouped by areas/systems.

In order to support new Google Play requirements Android now requires targeting .NET 9 when exporting C# projects to Android, other platforms continue to use .NET 8 as the minimum required version but newer versions are supported and encouraged.

If you are using C# in your project and want to export to Android, you will need to upgrade your project to .NET 9 (see Upgrading to a new .NET version for instructions).

This article indicates whether each breaking change affects GDScript and whether the C# breaking change is binary compatible or source compatible:

Binary compatible - Existing binaries will load and execute successfully without recompilation, and the run-time behavior won't change.

Source compatible - Source code will compile successfully without changes when upgrading Godot.

Method set_scope replaced by set_method

Method get_rpc_config renamed to get_node_rpc_config

Method set_name changes name parameter type from String to StringName

Method file_dialog_show adds a new parent_window_id optional parameter

Method file_dialog_with_options_show adds a new parent_window_id optional parameter

Method texture_create_from_extension adds a new mipmaps optional parameter

Method instance_reset_physics_interpolation removed

Method instance_set_interpolated removed

In C#, the enum RenderingDevice.Features breaks compatibility because of the way the bindings generator detects the enum prefix. New members were added to the enum in GH-103941 that caused the enum member Address to be renamed to BufferDeviceAddress.

Property byte_offset changes type metadata from int32 to int64

Property component_type changes type from int to GLTFAccessor::GLTFComponentType

Property count changes type metadata from int32 to int64

Property sparse_count changes type metadata from int32 to int64

Property sparse_indices_byte_offset changes type metadata from int32 to int64

Property sparse_indices_component_type changes type from int to GLTFAccessor::GLTFComponentType

Property sparse_values_byte_offset changes type metadata from int32 to int64

Property byte_length changes type metadata from int32 to int64

Property byte_offset changes type metadata from int32 to int64

Property byte_stride changes type metadata from int32 to int64

As a result of changing the type metadata, the C# bindings changed the type from int (32-bytes) to long (64-bytes).

Method draw_char adds a new oversampling optional parameter

Method draw_char_outline adds a new oversampling optional parameter

Method draw_multiline_string adds a new oversampling optional parameter

Method draw_multiline_string_outline adds a new oversampling optional parameter

Method draw_string adds a new oversampling optional parameter

Method draw_string_outline adds a new oversampling optional parameter

Method draw_char adds a new oversampling optional parameter

Method draw_char_outline adds a new oversampling optional parameter

Method draw_multiline_string adds a new oversampling optional parameter

Method draw_multiline_string_outline adds a new oversampling optional parameter

Method draw_string adds a new oversampling optional parameter

Method draw_string_outline adds a new oversampling optional parameter

Method add_image adds a new alt_text optional parameter

Method add_image replaced size_in_percent parameter by width_in_percent and height_in_percent

Method push_strikethrough adds optional color parameter

Method push_table adds a new name optional parameter

Method push_underline adds optional color parameter

Method update_image replaced size_in_percent parameter by width_in_percent and height_in_percent

Method draw adds a new oversampling optional parameter

Method draw_outline adds a new oversampling optional parameter

Method draw adds a new oversampling optional parameter

Method draw_dropcap adds a new oversampling optional parameter

Method draw_dropcap_outline adds a new oversampling optional parameter

Method draw_line adds a new oversampling optional parameter

Method draw_line_outline adds a new oversampling optional parameter

Method draw_outline adds a new oversampling optional parameter

Method font_draw_glyph adds a new oversampling optional parameter

Method font_draw_glyph_outline adds a new oversampling optional parameter

Method shaped_text_draw adds a new oversampling optional parameter

Method shaped_text_draw_outline adds a new oversampling optional parameter

Method add_button adds a new alt_text optional parameter

Method _font_draw_glyph adds a new oversampling optional parameter

Method _font_draw_glyph_outline adds a new oversampling optional parameter

Method _shaped_text_draw adds a new oversampling optional parameter

Method _shaped_text_draw_outline adds a new oversampling optional parameter

Method register_composition_layer_provider changes extension parameter type from OpenXRExtensionWrapperExtension to OpenXRExtensionWrapper

Method register_projection_views_extension changes extension parameter type from OpenXRExtensionWrapperExtension to OpenXRExtensionWrapper

Method unregister_composition_layer_provider changes extension parameter type from OpenXRExtensionWrapperExtension to OpenXRExtensionWrapper

Method unregister_projection_views_extension changes extension parameter type from OpenXRExtensionWrapperExtension to OpenXRExtensionWrapper

OpenXRBindingModifierEditor

Type OpenXRBindingModifierEditor changed API type from Core to Editor

OpenXRInteractionProfileEditor

Type OpenXRInteractionProfileEditor changed API type from Core to Editor

OpenXRInteractionProfileEditorBase

Type OpenXRInteractionProfileEditorBase changed API type from Core to Editor

Classes OpenXRBindingModifierEditor, OpenXRInteractionProfileEditor, and OpenXRInteractionProfileEditorBase are only available in the editor. Using them outside of the editor will result in a compilation error.

In C#, this means the types are moved from the GodotSharp assembly to the GodotSharpEditor assembly. Make sure to wrap code that uses these types in a #if TOOLS block to ensure they are not included in an exported game.

This change was also backported to 4.4.1.

Method get_forced_export_files adds a new preset optional parameter

EditorUndoRedoManager

Method create_action adds a new mark_unsaved optional parameter

EditorExportPlatformExtension

Method _get_option_icon changes return type from ImageTexture to Texture2D

In 4.5, some behavior changes have been introduced, which might require you to adjust your project.

TileMapLayer.get_coords_for_body_rid() will return different values in 4.5 compared to 4.4, as TileMapLayer physics chunking is enabled by default. Higher values of TileMapLayer.physics_quadrant_size will make this function less precise. To get the exact cell coordinates like in 4.4 and prior versions, you need to set TileMapLayer.physics_quadrant_size to 1, which disables physics chunking.

A fix has been made to the 3D model importers to correctly handle non-joint nodes within a skeleton hierarchy (GH-104184). To preserve compatibility, the default behavior is to import existing files with the same behavior as before (GH-107352). New .gltf, .glb, .blend, and .fbx files (without a corresponding .import file) will be imported with the new behavior. However, for existing files, if you want to use the new behavior, you must change the "Naming Version" option at the bottom of the Import dock:

Resource.duplicate(true) (which performs deep duplication) now only duplicates resources internal to the resource file it's called on. In 4.4, this duplicated everything instead, including external resources. If you were deep-duplicating a resource that contained references to other external resources, those external resources aren't duplicated anymore. You must call Resource.duplicate_deep(RESOURCE_DEEP_DUPLICATE_ALL) instead to keep the old behavior.

ProjectSettings.add_property_info() now prints a warning when the dictionary parameter has missing keys or invalid keys. Most importantly, it will now warn when a usage key is passed, as this key is not used. This was also the case before 4.5, but it was silently ignored instead. As a reminder, to set property usage information correctly, you must use ProjectSettings.set_as_basic(), ProjectSettings.set_restart_if_changed(), or ProjectSettings.set_as_internal() instead.

In C#, StringExtensions.PathJoin now avoids adding an extra path separator when the original string is empty, or when the appended path starts with a path separator (GH-105281).

In C#, StringExtensions.GetExtension now returns an empty string instead of the original string when the original string does not contain an extension (GH-108041).

In C#, the Quaternion(Vector3, Vector3) constructor now correctly creates a quaternion representing the shortest arc between the two input vectors. Previously, it would return incorrect values for certain inputs (GH-107618).

By default, the regions in a NavigationServer map now update asynchronously using threads to improve performance. This can cause additional delay in the update due to thread synchronisation. The asynchronous region update can be toggled with the navigation/world/region_use_async_iterations project setting.

The merging of navmeshes in the NavigationServer has changed processing order. Regions now merge and cache internal navmeshes first, then the remaining free edges are merged by the navigation map. If a project had navigation map synchronisation errors before, it might now have shifted affected edges, making already existing errors in a layout more noticeable in the pathfinding. The navigation/2d_or_3d/merge_rasterizer_cell_scale project setting can be set to a lower value to increase the detail of the rasterization grid (with 0.01 being the smallest cell size possible). If edge merge errors still persist with the lowest possible rasterization scale value, the error may be caused by overlap: two navmeshes are stacked on top of each other, causing geometry conflict.

When the 3D physics engine is set to Jolt Physics, you will now always have overlaps between Area3D and static bodies reported by default, as the physics/jolt_physics_3d/simulation/areas_detect_static_bodies project setting has been removed (GH-105746). If you still want such overlaps to be ignored, you will need to change the collision mask or layer of either the Area3D or the static body instead.

In GDScript, calls to functions RichTextLabel::add_image and RichTextLabel::update_image will continue to work, but the size_in_percent argument will now be used as the value for width_in_percent and height_in_percent will default to false (GH-107347). To restore the previous behavior, you can explicitly set height_in_percent to the same value you were passing as size_in_percent.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting projects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html

**Contents:**
- Exporting projects
- Why export?
  - On PC
  - On mobile
- Export menu
  - Export templates
  - Resource options
- Configuration files
- Exporting from the command line
- PCK versus ZIP pack file formats

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Originally, Godot did not have any means to export projects. The developers would compile the proper binaries and build the packages for each platform manually.

When more developers (and even non-programmers) started using it, and when our company started taking more projects at the same time, it became evident that this was a bottleneck.

Distributing a game project on PC with Godot is rather easy. Drop the Godot binary in the same directory as the project.godot file, then compress the project directory and you are done.

It sounds simple, but there are probably a few reasons why the developer may not want to do this. The first one is that it may not be desirable to distribute loads of files. Some developers may not like curious users peeking at how the game was made, others may find it inelegant, and so on. Another reason is that the developer might prefer a specially-compiled binary, which is smaller in size, more optimized and does not include tools like the editor and debugger.

Finally, Godot has a simple but efficient system for creating DLCs as extra package files.

The same scenario on mobile platforms is a little worse. To distribute a project on those devices, a binary for each of those platforms is built, then added to a native project together with the game data.

This can be troublesome because it means that the developer must be familiarized with the SDK of each platform before even being able to export. While learning each SDK is always encouraged, it can be frustrating to be forced to do it at an undesired time.

There is also another problem with this approach: different devices prefer some data in different formats to run. The main example of this is texture compression. All PC hardware uses S3TC (BC) compression and that has been standardized for more than a decade, but mobile devices use different formats for texture compression, such as ETC1 and ETC2.

After many attempts at different export workflows, the current one has proven to work the best. At the time of this writing, not all platforms are supported yet, but the supported platforms continue to grow.

To open the export menu, click the Export button:

The export menu will open. However, it will be completely empty. This is because we need to add an export preset.

To create an export preset, click the Add… button at the top of the export menu. This will open a drop-down list of platforms to choose from for an export preset.

The default options are often enough to export, so tweaking them is usually not necessary. However, many platforms require additional tools (SDKs) to be installed to be able to export. Additionally, Godot needs export templates installed to create packages. The export menu will complain when something is missing and will not allow the user to export for that platform until they resolve it:

At that time, the user is expected to come back to the documentation and follow instructions on how to properly set up that platform.

The buttons at the bottom of the menu allow you to export the project in a few different ways:

Export All: Export the project as a playable build (Godot executable and project data) for all the presets defined. All presets must have an Export Path defined for this to work.

Export Project: Export the project as a playable build (Godot executable and project data) for the selected preset.

Export PCK/ZIP: Export the project resources as a PCK or ZIP package. This is not a playable build, it only exports the project data without a Godot executable.

Apart from setting up the platform, the export templates must be installed to be able to export projects. They can be obtained as a TPZ file (which is a renamed ZIP archive) from the download page of the website.

Once downloaded, they can be installed using the Install Export Templates option in the editor:

When exporting, Godot makes a list of all the files to export and then creates the package. There are 3 different modes for exporting:

Export all resources in the project

Export selected scenes (and dependencies)

Export selected resources (and dependencies)

Export all resources in the project will export every resource in the project. Export selected scenes and Export selected resources gives you a list of the scenes or resources in the project, and you have to select every scene or resource you want to export.

Export all resources in the project except resources checked below does exactly what it says, everything will be exported except for what you select in the list.

Export as dedicated server will remove all visuals from a project and replace them with a placeholder. This includes Cubemap, CubemapArray, Material, Mesh, Texture2D, Texture2DArray, Texture3D. You can also go into the list of files and specify specific visual resources that you do wish to keep.

Files and folders whose name begin with a period will never be included in the exported project. This is done to prevent version control folders like .git from being included in the exported PCK file.

Below the list of resources are two filters that can be setup. The first allows non-resource files such as .txt, .json and .csv to be exported with the project. The second filter can be used to exclude every file of a certain type without manually deselecting every one. For example, .png files.

The export configuration is stored in two files that can both be found in the project directory:

export_presets.cfg: This file contains the vast majority of the export configuration and can be safely committed to version control. There is nothing in here that you would normally have to keep secret.

.godot/export_credentials.cfg: This file contains export options that are considered confidential, like passwords and encryption keys. It should generally not be committed to version control or shared with others unless you know exactly what you are doing.

Since the credentials file is usually kept out of version control systems, some export options will be missing if you clone the project to a new machine. The easiest way to deal with this is to copy the file manually from the old location to the new one.

In production, it is useful to automate builds, and Godot supports this with the --export-release and --export-debug command line parameters. Exporting from the command line still requires an export preset to define the export parameters. A basic invocation of the command would be:

This will export to some_name.exe, assuming there is a preset called "Windows Desktop" and the template can be found. (The export preset name must be written within quotes if it contains spaces or special characters.) The output path is relative to the project path or absolute; it does not respect the directory the command was invoked from.

The output file extension should match the one used by the Godot export process:

macOS: .app or .zip (or .dmg when exporting from macOS)

Linux: Any extension (including none). .x86_64 is typically used for 64-bit x86 binaries.

You can also configure it to export only the PCK or ZIP file, allowing a single exported main pack file to be used with multiple Godot executables. When doing so, the export preset name must still be specified on the command line:

It is often useful to combine the --export-release flag with the --path flag, so that you do not need to cd to the project folder before running the command:

See Command line tutorial for more information about using Godot from the command line.

Each format has its upsides and downsides. PCK is the default and recommended format for most use cases, but you may want to use a ZIP archive instead depending on your needs.

Uncompressed format. Larger file size, but faster to read/write.

Not readable and writable using tools normally present on the user's operating system, even though there are third-party tools to extract and create PCK files.

Compressed format. Smaller file size, but slower to read/write.

Readable and writable using tools normally present on the user's operating system. This can be useful to make modding easier (see also Exporting packs, patches, and mods).

Due to a known bug, when using a ZIP file as a pack file, the exported binary will not try to use it automatically. Therefore, you have to create a launcher script that the player can double-click or run from a terminal to launch the project:

Save the launcher script and place it in the same folder as the exported binary. On Linux, make sure to give executable permissions to the launcher script using the command chmod +x launch.sh.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
godot --export-release "Windows Desktop" some_name.exe
```

Example 2 (unknown):
```unknown
godot --export-pack "Windows Desktop" some_name.pck
```

Example 3 (unknown):
```unknown
godot --path /path/to/project --export-release "Windows Desktop" some_name.exe
```

Example 4 (markdown):
```markdown
:: launch.bat (Windows)
@echo off
my_project.exe --main-pack my_project.zip

# launch.sh (Linux)
./my_project.x86_64 --main-pack my_project.zip
```

---

## Blender ESCN exporter — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/escn_exporter/index.html

**Contents:**
- Blender ESCN exporter

To export from Blender to Godot 4.x, use one of the available 3D formats.

The plugin Godot Blender Exporter is not maintained or supported in Godot 4.x. While not officially supported, the plugin may partially work for some Godot and Blender versions, particularly before Blender version 4.0. For complete docs on the Blender exporter, see the previous version of this page.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting packs, patches, and mods — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html

**Contents:**
- Exporting packs, patches, and mods
- Use cases
- Overview of PCK/ZIP files
- Generating PCK files
- Opening PCK or ZIP files at runtime
  - Troubleshooting
- Summary
- User-contributed notes

Oftentimes, one would like to add functionality to one's game after it has been deployed.

Examples of this include...

Downloadable Content: the ability to add features and content to one's game.

Patches: the ability to fix a bug that is present in a shipped product.

Mods: grant other people the ability to create content for one's game.

These tools help developers to extend their development beyond the initial release.

Godot enables this via a feature called resource packs (PCK files, with the .pck extension, or ZIP files).

incremental updates/patches

no source code disclosure needed for mods

more modular project structure

users don't have to replace the entire game

The first part of using them involves exporting and delivering the project to players. Then, when one wants to add functionality or content later on, they just deliver the updates via PCK/ZIP files to the users.

PCK/ZIP files usually contain, but are not limited to:

any other asset suitable for import into the game

The PCK/ZIP files can even be an entirely different Godot project, which the original game loads in at runtime.

It is possible to load both PCK and ZIP files as additional packs at the same time. See PCK versus ZIP pack file formats for a comparison of the two formats.

If you want to load loose files at runtime (not packed in a PCK or ZIP by Godot), consider using Runtime file loading and saving instead. This is useful for loading user-generated content that is not made with Godot, without requiring users to pack their mods into a specific file format.

The downside of this approach is that it's less transparent to the game logic, as it will not benefit from the same resource management as PCK/ZIP files.

In order to pack all resources of a project into a PCK file, open the project and go to Project > Export and click on Export PCK/ZIP. Also, make sure to have an export preset selected while doing so.

Another method would be to export from the command line with --export-pack. The output file must with a .pck or .zip file extension. The export process will build that type of file for the chosen platform.

If one wishes to support mods for their game, they will need their users to create similarly exported files. Assuming the original game expects a certain structure for the PCK's resources and/or a certain interface for its scripts, then either...

The developer must publicize documentation of these expected structures/ interfaces, expect modders to install Godot Engine, and then also expect those modders to conform to the documentation's defined API when building mod content for the game (so that it will work). Users would then use Godot's built in exporting tools to create a PCK file, as detailed above.

The developer uses Godot to build a GUI tool for adding their exact API content to a project. This Godot tool must either run on a tools-enabled build of the engine or have access to one (distributed alongside or perhaps in the original game's files). The tool can then use the Godot executable to export a PCK file from the command line with OS.execute(). The game itself shouldn't use a tool-build of the engine (for security), so it's best to keep the modding tool and game separate.

To load a PCK or ZIP file, one uses the ProjectSettings singleton. The following example expects a mod.pck file in the directory of the game's executable. The PCK or ZIP file contains a mod_scene.tscn test scene in its root.

By default, if you import a file with the same file path/name as one you already have in your project, the imported one will replace it. This is something to watch out for when creating DLC or mods. You can solve this problem by using a tool that isolates mods to a specific mods subfolder.

However, it is also a way of creating patches for one's own game. A PCK/ZIP file of this kind can fix the content of a previously loaded PCK/ZIP (therefore, the order in which packs are loaded matters).

To opt out of this behavior, pass false as the second argument to ProjectSettings.load_resource_pack().

For a C# project, you need to build the DLL and place it in the project directory first. Then, before loading the resource pack, you need to load its DLL as follows: Assembly.LoadFile("mod.dll")

If you are loading a resource pack and are not noticing any changes, it may be due to the pack being loaded too late. This is particularly the case with menu scenes that may preload other scenes using preload(). This means that loading a pack in the menu will not affect the other scene that was already preloaded.

To avoid this, you need to load the pack as early as possible. To do so, create a new autoload script and call ProjectSettings.load_resource_pack() in the autoload script's _init() function, rather than _enter_tree() or _ready().

This tutorial explains how to add mods, patches, or DLC to a game. The most important thing is to identify how one plans to distribute future content for their game and develop a workflow that is customized for that purpose. Godot should make that process smooth regardless of which route a developer pursues.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _your_function():
    # This could fail if, for example, mod.pck cannot be found.
    var success = ProjectSettings.load_resource_pack(OS.get_executable_path().get_base_dir().path_join("mod.pck"))

    if success:
        # Now one can use the assets as if they had them in the project from the start.
        var imported_scene = load("res://mod_scene.tscn")
```

Example 2 (sql):
```sql
private void YourFunction()
{
    // This could fail if, for example, mod.pck cannot be found.
    var success = ProjectSettings.LoadResourcePack(OS.get_executable_path().get_base_dir().path_join("mod.pck));

    if (success)
    {
        // Now one can use the assets as if they had them in the project from the start.
        var importedScene = (PackedScene)ResourceLoader.Load("res://mod_scene.tscn");
    }
}
```

---

## Feature tags — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/feature_tags.html

**Contents:**
- Feature tags
- Introduction
- Default features
- Custom features
- Overriding project settings
- Default overrides
- Taking feature tags into account when reading project settings
- Customizing the build
- User-contributed notes

Godot has a special system to tag availability of features. Each feature is represented as a string, which can refer to many of the following:

Platform architecture (64-bit or 32-bit, x86 or ARM).

Platform type (desktop, mobile, Web).

Supported texture compression algorithms on the platform.

Whether a build is debug or release (debug includes the editor).

Whether the project is running from the editor or a "standalone" binary.

Features can be queried at runtime from the singleton API by calling:

OS feature tags are used by GDExtension to determine which libraries to load. For example, a library for linux.debug.editor.x86_64 will be loaded only on a debug editor build for Linux x86_64.

Here is a list of most feature tags in Godot. Keep in mind they are case-sensitive:

Running on Android (but not within a Web browser)

Running on *BSD (but not within a Web browser)

Running on Linux (but not within a Web browser)

Running on macOS (but not within a Web browser)

Running on iOS (but not within a Web browser)

Running on visionOS (but not within a Web browser)

Running on Linux or *BSD

Running on a debug build (including the editor)

Running on a release build

Running on an editor build

Running on an editor build, and inside the editor

Running on an editor build, and running the project

Running on a non-editor (export template) build

Running on a double-precision build

Running on a single-precision build

Running on a 64-bit build (any architecture)

Running on a 32-bit build (any architecture)

Running on a 64-bit x86 build

Running on a 32-bit x86 build

Running on an x86 build (any bitness)

Running on a 64-bit ARM build

Running on a 32-bit ARM build

Running on an ARM build (any bitness)

Running on a 64-bit RISC-V build

Running on a RISC-V build (any bitness)

Running on a 64-bit PowerPC build

Running on a 32-bit PowerPC build

Running on a PowerPC build (any bitness)

Running on a 64-bit WebAssembly build (not yet possible)

Running on a 32-bit WebAssembly build

Running on a WebAssembly build (any bitness)

Host OS is a mobile platform

Host OS is a PC platform (desktop/laptop)

Host OS is a Web browser

Running without threading support

Running with threading support

Host OS is a Web browser running on Android

Host OS is a Web browser running on iOS

Host OS is a Web browser running on Linux or *BSD

Host OS is a Web browser running on macOS

Host OS is a Web browser running on Windows

Textures using ETC1 compression are supported

Textures using ETC2 compression are supported

Textures using S3TC (DXT/BC) compression are supported

Movie Maker mode is active

Project was exported with shader baking enabled (only applies to the exported project, not when running in the editor)

Project was exported as a dedicated server (only applies to the exported project, not when running in the editor)

With the exception of texture compression, web_<platform> and movie feature tags, default feature tags are immutable. This means that they will not change depending on runtime conditions. For example, OS.has_feature("mobile") will return false when running a project exported to Web on a mobile device.

To check whether a project exported to Web is running on a mobile device, use OS.has_feature("web_android") or OS.has_feature("web_ios").

It is possible to add custom features to a build; use the relevant field in the export preset used to generate it:

Custom feature tags are only used when running the exported project (including with One-click deploy). They are not used when running the project from the editor, even if the export preset marked as Runnable for your current platform has custom feature tags defined.

Custom feature tags are also not used in EditorExportPlugin scripts. Instead, feature tags in EditorExportPlugin will reflect the device the editor is currently running on.

Features can be used to override specific configuration values in the Project Settings. This allows you to better customize any configuration when doing a build.

In the following example, a different icon is added for the demo build of the game (which was customized in a special export preset, which, in turn, includes only demo levels).

The desired configuration is selected, which effectively copies its properties to the panel above (1). The "demo_build" feature tag is selected (2). The configuration is added to the project settings (3).

After overriding, a new field is added for this specific configuration.

When using the project settings "override.cfg" functionality (which is unrelated to feature tags), remember that feature tags still apply. Therefore, make sure to also override the setting with the desired feature tag(s) if you want them to override base project settings on all platforms and configurations.

There are already a lot of settings that come with overrides by default; they can be found in many sections of the project settings.

By default, feature tags are not taken into account when reading project settings using the typical approaches (ProjectSettings.get_setting or ProjectSettings.get). Instead, you must use ProjectSettings.get_setting_with_override.

For example, with the following project settings:

Using ProjectSettings.get_setting("section/subsection/example") will return "Release" regardless of whether a debug build is currently running. On the other hand, ProjectSettings.get_setting_with_override("section/subsection/example") will obey feature tags and will return "Debug" if using a debug build.

Feature tags can be used to customize a build process too, by writing a custom ExportPlugin. They are also used to specify which shared library is loaded and exported in GDExtension.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
OS.has_feature(name)
```

Example 2 (unknown):
```unknown
OS.HasFeature(name);
```

Example 3 (json):
```json
[section]

subsection/example = "Release"
subsection/example.debug = "Debug"
```

---

## Exporting for Linux — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_linux.html

**Contents:**
- Exporting for Linux
- Environment variables
- Export options
- User-contributed notes

This page describes how to export a Godot project to Linux. If you're looking to compile editor or export template binaries from source instead, read Compiling for Linux, *BSD.

The simplest way to distribute a game for PC is to copy the executable (godot), compress the folder and send it to someone else. However, this is often not desired.

Godot offers a more elegant approach for PC distribution when using the export system. When exporting for Linux, the exporter takes all the project files and creates a data.pck file. This file is bundled with a specially optimized binary that is smaller, faster and does not contain the editor and debugger.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

You can find a full list of export options available in the EditorExportPlatformLinuxBSD class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting for macOS — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html

**Contents:**
- Exporting for macOS
- Requirements
- Code signing and notarization
  - If you have an Apple Developer ID Certificate and exporting from macOS
    - To sign exported app
    - To notarize exported app
  - If you have an Apple Developer ID Certificate and exporting from Linux or Windows
    - To sign exported app
    - To notarize exported app
  - If you do not have an Apple Developer ID Certificate

This page describes how to export a Godot project to macOS. If you're looking to compile editor or export template binaries from source instead, read Compiling for macOS.

macOS apps exported with the official export templates are exported as a single "Universal 2" binary .app bundle, a folder with a specific structure which stores the executable, libraries and all the project files. This bundle can be exported as is, packed in a ZIP archive, or packed in a DMG disk image (only supported when exporting from macOS). Universal binaries for macOS support both Intel x86_64 and ARM64 (Apple Silicon) architectures.

Due to file system limitations, .app bundles exported from Windows lack the executable flag and won't run on macOS. Projects exported as .zip are not affected by this issue. To run .app bundles exported from Windows on macOS, transfer the .app to a device running macOS or Linux and use the chmod +x {executable_name} terminal command to add the executable permission. The main executable located in the Contents/MacOS/ subfolder, as well as optional helper executables in the Contents/Helpers/ subfolder, should have the executable permission for the .app bundle to be valid.

Download the Godot export templates. Use the Godot menu: Editor > Manage Export Templates.

A valid and unique Bundle identifier should be set in the Application section of the export options.

Projects exported without code signing and notarization will be blocked by Gatekeeper if they are downloaded from unknown sources, see the Running Godot apps on macOS page for more information.

By default, macOS will run only applications that are signed and notarized. If you use any other signing configuration, see Running Godot apps on macOS for workarounds.

To notarize an app, you must have a valid Apple Developer ID Certificate.

Install Xcode command line tools and open Xcode at least once or run the sudo xcodebuild -license accept command to accept license agreement.

Select Xcode codesign in the Code Signing > Codesign option.

Set valid Apple ID certificate identity (certificate "Common Name") in the Code Signing > Identity section.

Select Xcode altool in the Notarization > Notarization option.

Disable the Debugging entitlement.

Set valid Apple ID login / app. specific password or App Store Connect API UUID / Key in the Notarization section.

You can use the xcrun notarytool history command to check notarization status and use the xcrun notarytool log {ID} command to download the notarization log.

If you encounter notarization issues, see Resolving common notarization issues for more info.

After notarization is completed, staple the ticket to the exported project.

Install PyOxidizer rcodesign, and configure the path to rcodesign in the Editor Settings > Export > macOS > rcodesign.

Select PyOxidizer rcodesign in the Code Signing > Codesign option.

Set valid Apple ID PKCS #12 certificate file and password in the Code Signing section.

Select PyOxidizer rcodesign in the Notarization > Notarization option.

Disable the Debugging entitlement.

Set valid App Store Connect API UUID / Key in the Notarization section.

You can use the rcodesign notary-log command to check notarization status.

After notarization is completed, use the rcodesign staple command to staple the ticket to the exported project.

Select Built-in (ad-hoc only) in the Code Signing > Codesign option.

Select Disabled in the Notarization > Notarization option.

In this case Godot will use an ad-hoc signature, which will make running an exported app easier for the end users, see the Running Godot apps on macOS page for more information.

Tool to use for code signing.

The "Full Name" or "Common Name" of the signing identity, store in the macOS keychain. [1]

The PKCS #12 certificate file. [2]

Password for the certificate file. [2]

Array of command line arguments passed to the code signing tool.

This option is visible only when signing with Xcode codesign.

These options are visible only when signing with PyOxidizer rcodesign.

Tool to use for notarization.

Apple ID account name (email address). [3]

Apple ID app-specific password. See Using app-specific passwords to enable two-factor authentication and create app password. [3]

Team ID ("Organization Unit"), if your Apple ID belongs to multiple teams (optional). [3]

Apple App Store Connect API issuer UUID.

Apple App Store Connect API key.

You should set either Apple ID Name/Password or App Store Connect API UUID/Key.

These options are visible only when notarizing with Xcode altool.

See Notarizing macOS Software Before Distribution for more info.

Hardened Runtime entitlements manage security options and resource access policy. See Hardened Runtime for more info.

Allow JIT Code Execution [4]

Allows creating writable and executable memory for JIT code. If you are using add-ons with dynamic or self-modifying native code, enable them according to the add-on documentation.

Allow Unsigned Executable Memory [4]

Allows creating writable and executable memory without JIT restrictions. If you are using add-ons with dynamic or self-modifying native code, enable them according to the add-on documentation.

Allow DYLD Environment Variables [4]

Allows app to uss dynamic linker environment variables to inject code. If you are using add-ons with dynamic or self-modifying native code, enable them according to the add-on documentation.

Disable Library Validation

Allows app to load arbitrary libraries and frameworks. Enable it if you are using GDExtension add-ons or ad-hoc signing, or want to support user-provided external add-ons.

Enable if you need to use the microphone or other audio input sources, if it's enabled you should also provide usage message in the privacy/microphone_usage_description option.

Enable if you need to use the camera, if it's enabled you should also provide usage message in the privacy/camera_usage_description option.

Enable if you need to use location information from Location Services, if it's enabled you should also provide usage message in the privacy/location_usage_description option.

[5] Enable to allow access contacts in the user's address book, if it's enabled you should also provide usage message in the privacy/address_book_usage_description option.

[5] Enable to allow access to the user's calendar, if it's enabled you should also provide usage message in the privacy/calendar_usage_description option.

[5] Enable to allow access to the user's Photos library, if it's enabled you should also provide usage message in the privacy/photos_library_usage_description option.

[5] Enable to allow app to send Apple events to other apps.

[6] You can temporarily enable this entitlement to use native debugger (GDB, LLDB) with the exported app. This entitlement should be disabled for production export.

The Allow JIT Code Execution, Allow Unsigned Executable Memory and Allow DYLD Environment Variables entitlements are always enabled for the Godot Mono exports, and are not visible in the export options.

These features aren't supported by Godot out of the box, enable them only if you are using add-ons which require them.

To notarize an app, you must disable the Debugging entitlement.

The App Sandbox restricts access to user data, networking and devices. Sandboxed apps can't access most of the file system, can't use custom file dialogs and execute binaries (using OS.execute and OS.create_process) outside the .app bundle. See App Sandbox for more info.

To distribute an app through the App Store, you must enable the App Sandbox.

Enable to allow app to listen for incoming network connections.

Enable to allow app to establish outgoing network connections.

Enable to allow app to interact with USB devices. This entitlement is required to use wired controllers.

Enable to allow app to interact with Bluetooth devices. This entitlement is required to use wireless controllers.

Allows read or write access to the user's "Downloads" folder.

Allows read or write access to the user's "Pictures" folder.

Allows read or write access to the user's "Music" folder.

Allows read or write access to the user's "Movies" folder.

Files User Selected [7]

Allows read or write access to arbitrary folder. To gain access, a folder must be selected from the native file dialog by the user.

List of helper executables to embedded to the app bundle. Sandboxed app are limited to execute only these executable.

You can optionally provide usage messages for various folders in the privacy/*_folder_usage_description options.

You can override default entitlements by selecting custom entitlements file, in this case all other entitlement are ignored.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

Options / Codesign / Certificate File

GODOT_MACOS_CODESIGN_CERTIFICATE_FILE

Options / Codesign / Certificate Password

GODOT_MACOS_CODESIGN_CERTIFICATE_PASSWORD

Options / Codesign / Provisioning Profile

GODOT_MACOS_CODESIGN_PROVISIONING_PROFILE

Options / Notarization / API UUID

GODOT_MACOS_NOTARIZATION_API_UUID

Options / Notarization / API Key

GODOT_MACOS_NOTARIZATION_API_KEY

Options / Notarization / API Key ID

GODOT_MACOS_NOTARIZATION_API_KEY_ID

Options / Notarization / Apple ID Name

GODOT_MACOS_NOTARIZATION_APPLE_ID_NAME

Options / Notarization / Apple ID Password

GODOT_MACOS_NOTARIZATION_APPLE_ID_PASSWORD

You can find a full list of export options available in the EditorExportPlatformMacOS class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting for Windows — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_windows.html

**Contents:**
- Exporting for Windows
- Changing the executable icon
- Code signing
  - Setup
- Environment variables
- Export options
- User-contributed notes

This page describes how to export a Godot project to Windows. If you're looking to compile editor or export template binaries from source instead, read Compiling for Windows.

The simplest way to distribute a game for PC is to copy the executable (godot.exe), compress the folder and send it to someone else. However, this is often not desired.

Godot offers a more elegant approach for PC distribution when using the export system. When exporting for Windows, the exporter takes all the project files and creates a data.pck file. This file is bundled with a specially optimized binary that is smaller, faster and does not contain the editor and debugger.

Godot will automatically use whatever image is set as your project's icon in the project settings, and convert it to an ICO file for the exported project. If you want to manually create an ICO file for greater control over how the icon looks at different resolutions then see the Manually changing application icon for Windows page.

Godot is capable of automatic code signing on export. To do this you must have the Windows SDK (on Windows) or osslsigncode (on any other OS) installed. You will also need a package signing certificate, information on creating one can be found here.

If you export for Windows with embedded PCK files, you will not be able to sign the program as it will break.

On Windows, PCK embedding is also known to cause false positives in antivirus programs. Therefore, it's recommended to avoid using it unless you're distributing your project via Steam as it bypasses code signing and antivirus checks.

Settings need to be changed in two places. First, in the editor settings, under Export > Windows. Click on the folder next to the Sign Tool setting, if you're using Windows navigate to and select SignTool.exe, if you're on a different OS select osslsigncode.

The second location is the Windows export preset, which can be found in Project > Export.... Add a windows desktop preset if you haven't already. Under options there is a code signing category.

Enabled must be set to true, and Identity must be set to the signing certificate. The other settings can be adjusted as needed. Once this is Done Godot will sign your project on export.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

Options / Codesign / Identity Type

GODOT_WINDOWS_CODESIGN_IDENTITY_TYPE

Options / Codesign / Identity

GODOT_WINDOWS_CODESIGN_IDENTITY

Options / Codesign / Password

GODOT_WINDOWS_CODESIGN_PASSWORD

You can find a full list of export options available in the EditorExportPlatformWindows class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting for Android — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html

**Contents:**
- Exporting for Android
- Install OpenJDK 17
- Download the Android SDK
- Setting it up in Godot
- Providing launcher icons
- Exporting for Google Play Store
- Optimizing the file size
- Environment variables
- Export options
- User-contributed notes

This page describes how to export a Godot project to Android. If you're looking to compile export template binaries from source instead, read Compiling for Android.

Exporting for Android has fewer requirements than compiling Godot for Android. The following steps detail what is needed to set up the Android SDK and the engine.

Projects written in C# can be exported to Android as of Godot 4.2, but support is experimental and some limitations apply.

Download and install OpenJDK 17.

Higher versions of the JDK are also supported, but we recommend using JDK 17 for optimal compatibility and stability.

Download and install the Android SDK.

You can install the Android SDK using Android Studio Iguana (version 2023.2.1) or later.

Run it once to complete the SDK setup using these instructions.

Ensure that the required packages are installed as well.

Android SDK Platform-Tools version 35.0.0 or later

Android SDK Build-Tools version 35.0.0

Android SDK Platform 35

Android SDK Command-line Tools (latest)

Ensure that the NDK and CMake are installed and configured.

CMake version 3.10.2.4988404

NDK version r28b (28.1.13356709)

Alternatively, you can install the Android SDK with the sdkmanager command line tool.

Install the command line tools package using these instructions.

Once the command line tools are installed, run the following sdkmanager command to complete the setup process:

If you are using Linux, do not use an Android SDK provided by your distribution's repositories as it will often be outdated.

Enter the Editor Settings screen (under the Godot tab for macOS, or the Editor tab for other platforms). This screen contains the editor settings for the user account in the computer (it's independent of the project).

Scroll down to the section where the Android settings are located:

In that screen, 2 paths need to be set:

Java SDK Path should be the location where OpenJDK 17 was installed.

Android Sdk Path should be the location where the Android SDK was installed. - For example %LOCALAPPDATA%\Android\Sdk\ on Windows or /Users/$USER/Library/Android/sdk/ on macOS.

Once that is configured, everything is ready to export to Android!

If you get an error saying "Could not install to device.", make sure you do not have an application with the same Android package name already installed on the device (but signed with a different key).

If you have an application with the same Android package name but a different signing key already installed on the device, you must remove the application in question from the Android device before exporting to Android again.

Launcher icons are used by Android launcher apps to represent your application to users. Godot only requires high-resolution icons (for xxxhdpi density screens) and will automatically generate lower-resolution variants.

There are three types of icons:

Main Icon: The "classic" icon. This will be used on all Android versions up to Android 8 (Oreo), exclusive. Must be at least 192×192 px.

Adaptive Icons: Starting from Android 8 (inclusive), Adaptive Icons were introduced. Applications will need to include separate background and foreground icons to have a native look. The user's launcher application will control the icon's animation and masking. Must be at least 432×432 px.

Themed Icons (optional): Starting from Android 13 (inclusive), Themed Icons were introduced. Applications will need to include a monochrome icon to enable this feature. The user's launcher application will control the icon's theme. Must be at least 432×432 px.

It's important to adhere to some rules when designing adaptive icons. Google Design has provided a nice article that helps to understand those rules and some of the capabilities of adaptive icons.

The most important adaptive icon design rule is to have your icon critical elements inside the safe zone: a centered circle with a diameter of 66dp (264 pixels on xxxhdpi) to avoid being clipped by the launcher.

If you don't provide the requested icons (except for Monochrome), Godot will replace them using a fallback chain, trying the next in line when the current one fails:

Main Icon: Provided main icon -> Project icon -> Default Godot main icon.

Adaptive Icon Foreground: Provided foreground icon -> Provided main icon -> Project icon -> Default Godot foreground icon.

Adaptive Icon Background: Provided background icon -> Default Godot background icon.

It's highly recommended to provide all the requested icons with their specified resolutions. This way, your application will look great on all Android devices and versions.

All new apps uploaded to Google Play after August 2021 must be an AAB (Android App Bundle) file.

Uploading an AAB or APK to Google's Play Store requires you to sign using a non-debug keystore file; such a file can be generated like this:

This keystore and key are used to verify your developer identity, remember the password and keep it in a safe place! It is suggested to use only upper and lowercase letters and numbers. Special characters may cause errors. Use Google's Android Developer guides to learn more about app signing.

Now fill in the following forms in your Android Export Presets:

Release: Enter the path to the keystore file you just generated.

Release User: Replace with the key alias.

Release Password: Key password. Note that the keystore password and the key password currently have to be the same.

Don't forget to uncheck the Export With Debug checkbox while exporting.

If you're working with APKs and not AABs, by default, the APK will contain native libraries for both ARMv7 and ARMv8 architectures. This increases its size significantly. To create a smaller file, uncheck either Armeabi-v 7a or Arm 64 -v 8a in your project's Android export preset. This will create an APK that only contains a library for a single architecture. Note that applications targeting ARMv7 can also run on ARMv8 devices, but the opposite is not true. The reason you don't do this to save space with AABs is that Google automatically splits up the AAB on their backend, so the user only downloads what they need.

You can optimize the size further by compiling an Android export template with only the features you need. See Optimizing a build for size for more information.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

Options / Keystore / Debug

GODOT_ANDROID_KEYSTORE_DEBUG_PATH

Options / Keystore / Debug User

GODOT_ANDROID_KEYSTORE_DEBUG_USER

Options / Keystore / Debug Password

GODOT_ANDROID_KEYSTORE_DEBUG_PASSWORD

Options / Keystore / Release

GODOT_ANDROID_KEYSTORE_RELEASE_PATH

Options / Keystore / Release User

GODOT_ANDROID_KEYSTORE_RELEASE_USER

Options / Keystore / Release Password

GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD

You can find a full list of export options available in the EditorExportPlatformAndroid class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
sdkmanager --sdk_root=<android_sdk_path> "platform-tools" "build-tools;35.0.0" "platforms;android-35" "cmdline-tools;latest" "cmake;3.10.2.4988404" "ndk;28.1.13356709"
```

Example 2 (unknown):
```unknown
keytool -v -genkey -keystore mygame.keystore -alias mygame -keyalg RSA -validity 10000
```

---

## Exporting for the Web — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html

**Contents:**
- Exporting for the Web
- Export file name
- WebGL version
- Mobile considerations
- Audio playback
- Export options
  - Thread and extension support
  - Exporting as a Progressive Web App (PWA)
- Limitations
  - Using cookies for data persistence

This page describes how to export a Godot project to HTML5. If you're looking to compile editor or export template binaries from source instead, read Compiling for the Web.

HTML5 export allows publishing games made in Godot Engine to the browser. This requires support for WebAssembly and WebGL 2.0 in the user's browser.

Projects written in C# using Godot 4 currently cannot be exported to the web. See this blog post for more information.

To use C# on web platforms, use Godot 3 instead.

Use the browser-integrated developer console, usually opened with F12 or Ctrl + Shift + I (Cmd + Option + I on macOS), to view debug information like JavaScript, engine, and WebGL errors.

If the shortcut doesn't work, it's because Godot actually captures the input. You can still open the developer console by accessing the browser's menu.

Due to security concerns with SharedArrayBuffer due to various exploits, the use of multiple threads for the Web platform has multiple drawbacks, including requiring specific server-side headers and complete cross-origin isolation (meaning no ads, nor third-party integrations on the website hosting your game).

Since Godot 4.3, Godot supports exporting your game on a single thread, which solves this issue. While it has some drawbacks on its own (it cannot use threads, and is not as performant as the multi-threaded export), it doesn't require as much overhead to install. It is also more compatible overall with stores like itch.io or Web publishers like Poki or CrazyGames. The single-threaded export works very well on macOS and iOS too, where it always had compatibility issues with multiple threads exports.

For these reasons, it is the preferred and now default way to export your games on the Web.

For more information, see this blog post about single-threaded Web export.

See the list of open issues on GitHub related to the web export for a list of known bugs.

We suggest users to export their Web projects with index.html as the file name. index.html is usually the default file loaded by web servers when accessing the parent directory, usually hiding the name of that file.

The Godot 4 Web export expects some files to be named the same name as the one set in the initial export. Some issues could occur if some exported files are renamed, including the main HTML file.

Godot 4.0 and later can only target WebGL 2.0 (using the Compatibility rendering method). Forward+/Mobile are not supported on the web platform, as these rendering methods are designed around modern low-level graphics APIs. Godot currently does not support WebGPU, which is a prerequisite for allowing Forward+/Mobile to run on the web platform.

See Can I use WebGL 2.0 for a list of browser versions supporting WebGL 2.0. Note that Safari has several issues with WebGL 2.0 support that other browsers don't have, so we recommend using a Chromium-based browser or Firefox if possible.

The Web export can run on mobile platforms with some caveats. While native Android and iOS exports will always perform better by a significant margin, the Web export allows people to run your project without going through app stores.

Remember that CPU and GPU performance is at a premium when running on mobile devices. This is even more the case when running a project exported to Web (as it's WebAssembly instead of native code). See Performance section of the documentation for advice on optimizing your project. If your project runs on platforms other than Web, you can use Feature tags to apply low-end-oriented settings when running the project exported to Web.

To speed up loading times on mobile devices, you should also compile an optimized export template with unused features disabled. Depending on the features used by your project, this can reduce the size of the WebAssembly payload significantly, making it faster to download and initialize (even when cached).

Since Godot 4.3, audio playback is done using the Web Audio API on the web platform. This Sample playback mode allows for low latency even when the project is exported without thread support, but it has several limitations:

AudioEffects are not supported.

Reverberation and doppler effects are not supported.

Procedural audio generation is not supported.

Positional audio may not always work correctly depending on the node's properties.

To use Godot's own audio playback system on the web platform, you can change the default playback mode using the Audio > General > Default Playback Type.web project setting, or change the Playback Type property to Stream on an AudioStreamPlayer, AudioStreamPlayer2D or AudioStreamPlayer3D node. This leads to increased latency (especially when thread support is disabled), but it allows the full suite of Godot's audio features to work.

If a runnable web export template is available, a button appears between the Stop scene and Play edited Scene buttons in the editor to quickly open the game in the default browser for testing.

If your project uses GDExtension, Extension Support needs to be enabled.

If you plan to use VRAM compression make sure that VRAM Texture Compression is enabled for the targeted platforms (enabling both For Desktop and For Mobile will result in a bigger, but more compatible export).

If a path to a Custom HTML shell file is given, it will be used instead of the default HTML page. See Custom HTML page for Web export.

Head Include is appended into the <head> element of the generated HTML page. This allows to, for example, load webfonts and third-party JavaScript APIs, include CSS, or run JavaScript code.

The window size will automatically match the browser window size by default. If you want to use a fixed size instead regardless of the browser window size, change Canvas Resize Policy to None. This allows controlling the window size with custom JavaScript code in the HTML shell. You can also set it to Project to make it behave closer to a native export, according to the project settings.

Each project must generate their own HTML file. On export, several text placeholders are replaced in the generated HTML file specifically for the given export options. Any direct modifications to that HTML file will be lost in future exports. To customize the generated file, use the Custom HTML shell option.

If Thread Support is enabled, the exported project will be able to make use of multithreading to improve performance. This also allows for low-latency audio playback when the playback type is set to Stream (instead of the default Sample that is used in web exports). Enabling this feature requires the use of cross-origin isolation headers, which are described in the Serving the files section below.

If Extensions Support is enabled, GDExtensions will be able to be loaded. Note that GDExtensions still need to be specifically compiled for the web platform to work. Like thread support, enabling this feature requires the use of cross-origin isolation headers.

If Progressive Web App > Enable is enabled, it will have several effects:

Configure high-resolution icons, a display mode and screen orientation. These are configured at the end of the Progressive Web App section in the export options. These options are used if the user adds the project to their device's homescreen, which is common on mobile platforms. This is also supported on desktop platforms, albeit in a more limited capacity.

Allow the project to be loaded without an Internet connection if it has been loaded at least once beforehand. This works thanks to the service worker that is installed when the project is first loaded in the user's browser. This service worker provides a local fallback when no Internet connection is available.

Note that web browsers can choose to evict the cached data if the user runs low on disk space, or if the user hasn't opened the project for a while. To ensure data is cached for a longer duration, the user can bookmark the page, or ideally add it to their device's home screen.

If the offline data is not available because it was evicted from the cache, you can configure an Offline Page that will be displayed in this case. The page must be in HTML format and will be saved on the client's machine the first time the project is loaded.

Ensure cross-origin isolation headers are always present, even if the web server hasn't been configured to send them. This allows exports with threads enabled to work when hosted on any website, even if there is no way for you to control the headers it sends.

This behavior can be disabled by unchecking Enable Cross Origin Isolation Headers in the Progressive Web App section.

For security and privacy reasons, many features that work effortlessly on native platforms are more complicated on the web platform. Following is a list of limitations you should be aware of when porting a Godot game to the web.

Browser vendors are making more and more functionalities only available in secure contexts, this means that such features are only be available if the web page is served via a secure HTTPS connection (localhost is usually exempt from such requirement).

Users must allow cookies (specifically IndexedDB) if persistence of the user:// file system is desired. When playing a game presented in an iframe, third-party cookies must also be enabled. Incognito/private browsing mode also prevents persistence.

The method OS.is_userfs_persistent() can be used to check if the user:// file system is persistent, but can give false positives in some cases.

The project will be paused by the browser when the tab is no longer the active tab in the user's browser. This means functions such as _process() and _physics_process() will no longer run until the tab is made active again by the user (by switching back to the tab). This can cause networked games to disconnect if the user switches tabs for a long duration.

This limitation does not apply to unfocused browser windows. Therefore, on the user's side, this can be worked around by running the project in a separate window instead of a separate tab.

Browsers do not allow arbitrarily entering full screen. The same goes for capturing the cursor. Instead, these actions have to occur as a response to a JavaScript input event. In Godot, this means entering full screen from within a pressed input event callback such as _input or _unhandled_input. Querying the Input singleton is not sufficient, the relevant input event must currently be active.

For the same reason, the full screen project setting doesn't work unless the engine is started from within a valid input event handler. This requires customization of the HTML page.

Some browsers restrict autoplay for audio on websites. The easiest way around this limitation is to request the player to click, tap or press a key/button to enable audio, for instance when displaying a splash screen at the start of your game.

Google offers additional information about their Web Audio autoplay policies.

Apple's Safari team also posted additional information about their Auto-Play Policy Changes for macOS.

Access to microphone requires a secure context.

Since Godot 4.3, by default Web exports will use samples instead of streams to play audio.

This is due to the way browsers prefer to play audio and the lack of processing power available when exporting Web games with the Use Threads export option off.

Please note that audio effects aren't yet implemented for samples.

Low-level networking is not implemented due to lacking support in browsers.

Currently, only HTTP client, HTTP requests, WebSocket (client) and WebRTC are supported.

The HTTP classes also have several restrictions on the HTML5 platform:

Accessing or changing the StreamPeer is not possible

Threaded/Blocking mode is not available

Cannot progress more than once per frame, so polling in a loop will freeze

Host verification cannot be disabled

Subject to same-origin policy

Clipboard synchronization between engine and the operating system requires a browser supporting the Clipboard API, additionally, due to the API asynchronous nature might not be reliable when accessed from GDScript.

Requires a secure context.

Gamepads will not be detected until one of their button is pressed. Gamepads might have the wrong mapping depending on the browser/OS/gamepad combination, sadly the Gamepad API does not provide a reliable way to detect the gamepad information necessary to remap them based on model/vendor/OS due to privacy considerations.

Requires a secure context.

Exporting for the web generates several files to be served from a web server, including a default HTML page for presentation. A custom HTML file can be used, see Custom HTML page for Web export.

Only when exporting with Use Threads, to ensure low audio latency and the ability to use Thread in web exports, Godot 4 web exports use SharedArrayBuffer. This requires a secure context, while also requiring the following CORS headers to be set when serving the files:

If you don't control the web server or are unable to add response headers, check Progressive Web App > Enable in the export options. This applies a service worker-based workaround that allows the project to run by simulating the presence of these response headers. A secure context is still required in this case.

If the client doesn't receive the required response headers or the service worker-based workaround is not applied, the project will not run.

The generated .html file can be used as DirectoryIndex in Apache servers and can be renamed to e.g. index.html at any time. Its name is never depended on by default.

The HTML page draws the game at maximum size within the browser window. This way, it can be inserted into an <iframe> with the game's size, as is common on most web game hosting sites.

The other exported files are served as they are, next to the .html file, names unchanged. The .wasm file is a binary WebAssembly module implementing the engine. The .pck file is the Godot main pack containing your game. The .js file contains start-up code and is used by the .html file to access the engine. The .png file contains the boot splash image.

The .pck file is binary, usually delivered with the MIME-type application/octet-stream. The .wasm file is delivered as application/wasm.

Delivering the WebAssembly module (.wasm) with a MIME-type other than application/wasm can prevent some start-up optimizations.

Delivering the files with server-side compression is recommended especially for the .pck and .wasm files, which are usually large in size. The WebAssembly module compresses particularly well, down to around a quarter of its original size with gzip compression. Consider using Brotli precompression if supported on your web server for further file size savings.

Hosts that provide on-the-fly compression: GitHub Pages (gzip)

Hosts that don't provide on-the-fly compression: itch.io, GitLab Pages (supports manual gzip precompression)

The Godot repository includes a Python script to host a local web server. This script is intended for testing the web editor, but it can also be used to test exported projects.

Save the linked script to a file called serve.py, move this file to the folder containing the exported project's index.html, then run the following command in a command prompt within the same folder:

On Windows, you can open a command prompt in the current folder by holding Shift and right-clicking on empty space in Windows Explorer, then choosing Open PowerShell window here.

This will serve the contents of the current folder and open the default web browser automatically.

Note that for production use cases, this Python-based web server should not be used. Instead, you should use an established web server such as Apache or nginx.

See the dedicated page on how to interact with JavaScript and access some unique Web browser features.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

If you use one-click deploy in multiple projects, you may notice that one of the projects you've previously deployed is shown instead of the project you're currently working on. This is due to service worker caching which currently lacks an automated cache busting mechanism.

As a workaround, you can manually unregister the current service worker so that the cache is reset. This also allows a new service worker to be registered. In Chromium-based browsers, open the Developer Tools by pressing F12 or Ctrl + Shift + I (Cmd + Option + I on macOS), then click on the Application tab in DevTools (it may be hidden behind a chevron icon if the devtools pane is narrow). You can either check Update on reload and reload the page, or click Unregister next to the service worker that is currently registered, then reload the page.

Unregistering the service worker in Chromium-based browsers' DevTools

The procedure is similar in Firefox. Open developer tools by pressing F12 or Ctrl + Shift + I (Cmd + Option + I on macOS), click on the Application tab in DevTools (it may be hidden behind a chevron icon if the devtools pane is narrow). Click Unregister next to the service worker that is currently registered, then reload the page.

Unregistering the service worker in Firefox's DevTools

You can find a full list of export options available in the EditorExportPlatformWeb class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Example 2 (markdown):
```markdown
# You may need to replace `python` with `python3` on some platforms.
python serve.py --root .
```

---

## Exporting for visionOS — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_visionos.html

**Contents:**
- Exporting for visionOS
- User-contributed notes

This page describes how to export a Godot project to visionOS. If you're looking to compile export template binaries from source instead, see Compiling for visionOS.

Exporting instructions for visionOS are currently identical to Compiling for iOS, except you should add a visionOS export preset instead of iOS. See the linked page for details.

Note that currently, only exporting an application for use on a flat plane within the headset is supported. Immersive experiences are not supported.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## One-click deploy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/one-click_deploy.html

**Contents:**
- One-click deploy
- What is one-click deploy?
- Supported platforms
- Using one-click deploy
- Troubleshooting
  - Android
  - Web
- User-contributed notes

One-click deploy is a feature that is available once a platform is properly configured and a supported device is connected to the computer. Since things can go wrong at many levels (platform may not be configured correctly, SDK may be incorrectly installed, device may be improperly configured, etc.), it's good to let the user know that it exists.

After adding an Android export preset marked as Runnable, Godot can detect when a USB device is connected to the computer and offer the user to automatically export, install and run the project (in debug mode) on the device. This feature is called one-click deploy.

One-click deploy is only available once you've added an export template marked as Runnable in the Export dialog. You can mark several export presets as runnable, but only one preset per platform may be marked as runnable. If you mark a second preset in a given platform as runnable, the other preset will no longer be marked as runnable.

Android: Exports the project with debugging enabled and runs it on the connected device.

Make sure to follow the steps described in Exporting for Android. Otherwise, the one-click deploy button won't appear.

If you have more than one device connected, Godot will ask you which device the project should be exported to.

iOS: Exports the project with debugging enabled and runs it on the connected device.

Make sure to follow the steps described in Exporting for iOS. Otherwise, the one-click deploy button won't appear.

For each new bundle identifier, export the project, open it in the Xcode, and build at least once to create new provisioning profile or create a provisioning profile in the Apple Developer account dashboard.

If you have more than one device connected, Godot will ask you which device the project should be exported to.

Desktop platforms: Exports the project with debugging enabled and runs it on the remote computer via SSH.

Web: Starts a local web server and runs the exported project by opening the default web browser. This is only accessible on localhost by default. See Troubleshooting for making the exported project accessible on remote devices.

Enable developer mode on your mobile device then enable USB debugging in the device's settings.

After enabling USB debugging, connect the device to your PC using a USB cable.

For advanced users, it should also be possible to use wireless ADB.

Install Xcode, accept Xcode license and login with your Apple Developer account.

If you are using Xcode 14 or earlier, install ios-deploy and set path to ios-deploy in the Editor Settings (see Export ⇾ iOS ⇾ iOS Deploy).

Pair your mobile device with a Mac.

Enable developer mode on your device.

Device can be connected via USB or local network.

Make sure the device is on the same local network and a correct network interface is selected in the editor settings (see Network ⇾ Debug ⇾ Remote Host). By default, the editor is listening for localhost connections only.

Device screen should be unlocked.

Enable SSH Remote Deploy and configure connection settings in the project export setting.

Make sure there is an export preset marked as Runnable for the target platform (Android, iOS or Web).

If everything is configured correctly and with no errors, platform-specific icons will appear in the top-right corner of the editor.

Click the button to export to the desired platform in one click.

If you can't see the device in the list of devices when running the adb devices command in a terminal, it will not be visible by Godot either. To resolve this:

Check if USB debugging is enabled and authorized on the device. Try unlocking your device and accepting the authorization prompt if you see any. If you can't see this prompt, running adb devices on your PC should make the authorization prompt appear on the device.

Try revoking the debugging authorization in the device's developer settings, then follow the steps again.

Try using USB debugging instead of wireless debugging or vice versa. Sometimes, one of those can work better than the other.

On Linux, you may be missing the required udev rules for your device to be recognized.

By default, the web server started by the editor is only accessible from localhost. This means the web server can't be reached by other devices on the local network or the Internet (if port forwarding is set up on the router). This is done for security reasons, as you may not want other devices to be able to access the exported project while you're testing it. Binding to localhost also prevents a firewall popup from appearing when you use one-click deploy for the web platform.

To make the local web server accessible over the local network, you'll need to change the Export > Web > HTTP Host editor setting to 0.0.0.0. You will also need to enable Export > Web > Use TLS as SharedArrayBuffer requires the use of a secure connection to work, unless connecting to localhost. However, since other clients will be connecting to a remote device, the use of TLS is absolutely required here.

To make the local web server accessible over the Internet, you'll also need to forward the Export > Web > HTTP Port port specified in the Editor Settings (8060 by default) in TCP on your router. This is usually done by accessing your router's web interface then adding a NAT rule for the port in question. For IPv6 connections, you should allow the port in the router's IPv6 firewall instead. Like for local network devices, you will also need to enable Export > Web > Use TLS.

When Use TLS is enabled, you will get a warning from your web browser as Godot will use a temporary self-signed certificate. You can safely ignore it and bypass the warning by clicking Advanced and then Proceed to (address).

If you have an SSL/TLS certificate that is trusted by browsers, you can specify the paths to the key and certificate files in the Export > Web > TLS Key and Export > Web > TLS Certificate. This will only work if the project is accessed through a domain name that is part of the TLS certificate.

When using one-click deploy on different projects, it's possible that a previously edited project is being shown instead. This is due to service worker caching not being cleared automatically. See Troubleshooting for instructions on unregistering the service worker, which will effectively clear the cache and resolve the issue.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Manually changing application icon for Windows — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/changing_application_icon_for_windows.html

**Contents:**
- Manually changing application icon for Windows
- Creating a custom ICO file
- Changing the taskbar icon
- Changing the file icon
- Testing the result
- User-contributed notes

Windows applications use a Windows only format called ICO for their file icon and taskbar icon. Since Godot 4.1, Godot can create an ICO file for you based on the icon file defined in the Windows export preset. Supported formats are PNG, WebP, and SVG. If no icon is defined in the Windows export preset, the application/config/icon project setting is used automatically instead.

This means you no longer need to follow the steps in this section to manually create an ICO file, unless you wish to have control over the icon design depending on its displayed size.

You can create your application icon in any program but you will have to convert it to an ICO file using a program such as GIMP.

This video tutorial goes over how to export an ICO file with GIMP.

It is also possible to convert a PNG image to an hiDPI-friendly ICO file using this ImageMagick command:

Depending on which version of ImageMagick you installed, you might need to leave out the magick and run this command instead:

For the ICO file to effectively replace the default Godot icon, it must contain all the sizes included in the default Godot icon: 16×16, 32×32, 48×48, 64×64, 128×128, 256×256. If the ICO file does not contain all the sizes, the default Godot icon will be kept for the sizes that weren't overridden.

The above ImageMagick command takes this into account.

The taskbar icon is the icon that shows up on the taskbar when your project is running.

To change the taskbar icon, go to Project > Project Settings > Application > Config, make sure Advanced Settings are enabled to see the setting, then go to Windows Native Icon. Click on the folder icon and select your ICO file.

This setting only changes the icon for your exported game on Windows. To set the icon for macOS, use Macos Native Icon. And for any other platform, use the Icon setting.

The file icon is the icon of the executable that you click on to start the project.

To do that, you will need to specify the icon when exporting. Go to Project > Export. Assuming you have already created a Windows Desktop preset, select your icon in ICO format in the Application > Icon field.

You can now export the project. If it worked correctly, you should see this:

If your icon isn't showing up properly try clearing the icon cache. To do so, open the Run dialog and enter ie4uinit.exe -ClearIconCache or ie4uinit.exe -show.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

Example 2 (unknown):
```unknown
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

---

## Running Godot apps on macOS — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/running_on_macos.html

**Contents:**
- Running Godot apps on macOS
- App is signed, notarized and distributed via App Store
- App is signed, notarized and distributed outside App Store
- App is signed (including ad-hoc signatures) but not notarized
- App is not signed, executable is linker-signed
- Neither app nor executable is signed (relevant for Apple Silicon Macs only)
- User-contributed notes

This page covers running Godot projects on macOS. If you haven't exported your project yet, read Exporting for macOS first.

By default, macOS will run only applications that are signed and notarized.

When running an app from the Downloads folder or when still in quarantine, Gatekeeper will perform path randomization as a security measure. This breaks access to relative paths from the app, which the app relies upon to work. To resolve this issue, move the app to the /Applications folder.

In general, macOS apps should avoid relying on relative paths from the application folder.

Depending on the way a macOS app is signed and distributed, the following scenarios are possible:

App developers need to join the Apple Developer Program, and configure signing and notarization options during export, then upload the app to the App Store.

The app should run out of the box, without extra user interaction required.

App developers need to join the Apple Developer Program, and configure signing and notarization options during export, then distribute the app as ".DMG" or ".ZIP" archive.

When you run the app for the first time, the following dialog is displayed:

Click Open to start the app.

If you see the following warning dialog, your Mac is set up to allow apps only from the App Store.

To allow third-party apps, open System Preferences, click Security & Privacy, then click General, unlock settings, and select App Store and identified developers.

App developer used self-signed certificate or ad-hoc signing (default Godot behavior for exported project).

When you run the app for the first time, the following dialog is displayed:

To run this app, you can temporarily override Gatekeeper:

Either open System Preferences, click Security & Privacy, then click General, and click Open Anyway.

Or, right-click (Control-click) on the app icon in the Finder window and select Open from the menu.

Then click Open in the confirmation dialog.

Enter your password if you're prompted.

Another option is to disable Gatekeeper entirely. Note that this does decrease the security of your computer by allowing you to run any software you want. To do this, run sudo spctl --master-disable in the Terminal, enter your password, and then the Anywhere option will be available:

Note that Gatekeeper will re-enable itself when macOS updates.

App is built using official export templates, but it is not signed.

When you run the app for the first time, the following dialog is displayed:

To run this app, you should remove the quarantine extended file attribute manually:

Open Terminal.app (press Cmd + Space and enter Terminal).

Navigate to the folder containing the target application.

Use the cd path_to_the_app_folder command, e.g. cd ~/Downloads/ if it's in the Downloads folder.

Run the command xattr -dr com.apple.quarantine "Unsigned Game.app" (including quotation marks and .app extension).

App is built using custom export templates, compiled using OSXCross, and it is not signed at all.

When you run the app for the first time, the following dialog is displayed:

To run this app, you can ad-hoc sign it yourself:

Install Xcode for the App Store, start it and confirm command line tools installation.

Open Terminal.app (press Cmd + Space and enter Terminal).

Navigate to the folder containing the target application.

Use the cd path_to_the_app_folder command, e.g. cd ~/Downloads/ if it's in the Downloads folder.

Run the following commands:

xattr -dr com.apple.quarantine "Unsigned Game.app" (including quotation marks and ".app" extension).

codesign -s - --force --deep "Unsigned Game.app" (including quotation marks and ".app" extension).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Exporting for iOS — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html

**Contents:**
- Exporting for iOS
- Requirements
- Export a Godot project to Xcode
- Active development considerations
  - Steps to link a Godot project folder to Xcode
- Plugins for iOS
- Environment variables
- Troubleshooting
  - xcode-select points at wrong SDK location
- Export options

This page describes how to export a Godot project to iOS. If you're looking to compile export template binaries from source instead, read Compiling for iOS.

These are the steps to load a Godot project in Xcode. This allows you to build and deploy to an iOS device, build a release for the App Store, and do everything else you can normally do with Xcode.

Projects written in C# can be exported to iOS as of Godot 4.2, but support is experimental and some limitations apply.

You must export for iOS from a computer running macOS with Xcode installed.

Download the Godot export templates. Use the Godot menu: Editor > Manage Export Templates

In the Godot editor, open the Export window from the Project menu. When the Export window opens, click Add.. and select iOS.

The App Store Team ID and (Bundle) Identifier options in the Application category are required. Leaving them blank will cause the exporter to throw an error.

After you click Export Project, there are still two important options left:

Path is an empty folder that will contain the exported Xcode project files.

File will be the name of the Xcode project and several project specific files and directories.

This tutorial uses exported_xcode_project_name, but you will use your project's name. When you see exported_xcode_project_name in the following steps, replace it with the name you used instead.

Avoid using spaces when you choose your exported_xcode_project_name as this can lead to corruption in your XCode project file.

When the export completes, the output folder should look like this:

Exporting for the iOS simulator is currently not supported as per GH-102149.

Apple Silicon Macs can run iOS apps natively, so you can run exported iOS projects directly on an Apple Silicon Mac without needing the iOS simulator.

Opening exported_xcode_project_name.xcodeproj lets you build and deploy like any other iOS app.

The above method creates an exported project that you can build for release, but you have to re-export every time you make a change in Godot.

While developing, you can speed this process up by linking your Godot project files directly into your app.

In the following example:

exported_xcode_project_name is the name of the exported iOS application (as above).

godot_project_to_export is the name of the Godot project.

godot_project_to_export must not be the same as exported_xcode_project_name to prevent signing issues in Xcode.

Start from an exported iOS project (follow the steps above).

In Finder, drag the Godot project folder into the Xcode file browser.

In the dialog, make sure to select Action: Reference files in place and Groups: Create folders. Uncheck Targets: exported_xcode_project_name.

See the godot_project_to_export folder in the Xcode file browser.

Select the godot project in the Project navigator. Then on the other side of the XCode window, in the File Inspector, make these selections:

Location: Relative to Project

Build Rules: Apply Once to Folder

add your project to Target Membership

Delete exported_xcode_project_name.pck from the Xcode project in the project navigator.

8. Open exported_xcode_project_name-Info.plist and add a string property named godot_path (this is the real key name) with a value godot_project_to_export (this is the name of your project)

That's it! You can now edit your project in the Godot editor and build it in Xcode when you want to run it on a device.

Special iOS plugins can be used in Godot. Check out the Plugins for iOS page.

You can use the following environment variables to set export options outside of the editor. During the export process, these override the values that you set in the export menu.

Encryption / Encryption Key

GODOT_SCRIPT_ENCRYPTION_KEY

Options / Application / Provisioning Profile UUID Debug

GODOT_IOS_PROVISIONING_PROFILE_UUID_DEBUG

Options / Application / Provisioning Profile UUID Release

GODOT_IOS_PROVISIONING_PROFILE_UUID_RELEASE

xcode-select is a tool that comes with Xcode and among other things points at iOS SDKs on your Mac. If you have Xcode installed, opened it, agreed to the license agreement, and installed the command line tools, xcode-select should point at the right location for the iPhone SDK. If it somehow doesn't, Godot will fail exporting to iOS with an error that may look like this:

In this case, Godot is trying to find the Platforms folder containing the iPhone SDK inside the /Library/Developer/CommandLineTools/ folder, but the Platforms folder with the iPhone SDK is actually located under /Applications/Xcode.app/Contents/Developer. To verify this, you can open up Terminal and run the following command to see what xcode-select points at:

To fix xcode-select pointing at a wrong location, enter this command in Terminal:

After running this command, Godot should be able to successfully export to iOS.

You can find a full list of export options available in the EditorExportPlatformIOS class reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (jsx):
```jsx
MSB3073: The command ""clang" <LOTS OF PATHS AND COMMAND LINE ARGUMENTS HERE>
"/Library/Developer/CommandLineTools/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"" exited with code 1.
```

Example 2 (sql):
```sql
xcode-select -p
```

Example 3 (sql):
```sql
sudo xcode-select -switch /Applications/Xcode.app
```

---

## Exporting for dedicated servers — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html

**Contents:**
- Exporting for dedicated servers
- Editor versus export template
- Export approaches
- Exporting a project for a dedicated server
- Starting the dedicated server
- Next steps
- User-contributed notes

If you want to run a dedicated server for your project on a machine that doesn't have a GPU or display server available, you'll need to run Godot with the headless display server and Dummy audio driver.

Since Godot 4.0, this can be done by running a Godot binary on any platform with the --headless command line argument, or running a project exported as dedicated server. You do not need to use a specialized server binary anymore, unlike Godot 3.x.

It is possible to use either an editor or export template (debug or release) binary in headless mode. Which one you should use depends on your use case:

Export template: Use this one for running dedicated servers. It does not contain editor functionality, and is therefore smaller and more optimized.

Editor: This binary contains editor functionality and is intended to be used for exporting projects. This binary can be used to run dedicated servers, but it's not recommended as it's larger and less optimized.

There are two ways to export a project for a server:

Create a separate export preset for the platform that will host the server, then export your project as usual.

Export a PCK file only, preferably for the platform that matches the platform that will host the server. Place this PCK file in the same folder as an export template binary, rename the binary to have the same name as the PCK (minus the file extension), then run the binary.

Both methods should result in identical output. The rest of the page will focus on the first approach.

See Exporting projects for more information.

If you export a project as usual when targeting a server, you will notice that the PCK file is just as large as for the client. This is because it includes all resources, including those the server doesn't need (such as texture data). Additionally, headless mode won't be automatically used; the user will have to specify --headless to make sure no window spawns.

Many resources such as textures can be stripped from the PCK file to greatly reduce its size. Godot offers a way to do this for textures and materials in a way that preserves references in scene or resource files (built-in or external).

To begin doing so, make sure you have a dedicated export preset for your server, then select it, go to its Resources tab and change its export mode:

Choosing the Export as dedicated server export mode in the export preset

When this export mode is chosen, the dedicated_server feature tag is automatically added to the exported project.

If you do not wish to use this export mode but still want the feature tag, you can write the name dedicated_server in the Features tab of the export preset. This will also force --headless when running the exported project.

After selecting this export mode, you will be presented with a list of resources in the project:

Choosing resources to keep, keep with stripped visuals or remove

Ticking a box allows you to override options for the specified file or folder. Checking boxes does not affect which files are exported; this is done by the options selected for each checkbox instead.

Files within a checked folder will automatically use the parent's option by default, which is indicated by the (Inherited) suffix for the option name (and the option name being grayed out). To change the option for a file whose option is currently inherited, you must tick the box next to it first.

Strip Visuals: Export this resource, with visual files (textures and materials) replaced by placeholder classes. Placeholder classes store the image size (as it's sometimes used to position elements in a 2D scene), but nothing else.

Keep: Export this resource as usual, with visual files intact.

Remove: The file is not included in the PCK. This is useful to ignore scenes and resources that only the client needs. If you do so, make sure the server doesn't reference these client-only scenes and resources in any way.

The general recommendation is to use Strip Visuals whenever possible, unless the server needs to access image data such as pixels' colors. For example, if your server generates collision data based on an image's contents, you need to use Keep for that particular image.

To check the file structure of your exported PCK, use the Export PCK/ZIP... button with a .zip file extension, then open the resulting ZIP file in a file manager.

Be careful when using the Remove mode, as scenes/resources that reference a removed file will no longer be able to load successfully.

If you wish to remove specific resources but make the scenes still be able to load without them, you'll have to remove the reference in the scene file and load the files to the nodes' properties using load() in a script. This approach can be used to strip resources that Godot doesn't support replacing with placeholders yet, such as audio.

Removing textures is often what makes the greatest impact on the PCK size, so it is recommended to stick with Strip Visuals at first.

With the above options used, a PCK for the client (which exports all resources normally) will look as follows:

The PCK's file structure for the server will look as follows:

If both your client and server are part of the same Godot project, you will have to add a way to start the server directly using a command-line argument.

If you exported the project using the Export as dedicated server export mode (or have added dedicated_server as a custom feature tag), you can use the dedicated_server feature tag to detect whether a dedicated server PCK is being used:

If you also wish to host a server when using the built-in --headless command line argument, this can be done by adding the following code snippet in your main scene (or an autoload)'s _ready() method:

If you wish to use a custom command line argument, this can be done by adding the following code snippet in your main scene (or an autoload)'s _ready() method:

It's a good idea to add at least one of the above command-line arguments to start a server, as it can be used to test server functionality from the command line without having to export the project.

If your client and server are separate Godot projects, your server should most likely be configured in a way where running the main scene starts a server automatically.

On Linux, to make your dedicated server restart after a crash or system reboot, you can create a systemd service. This also lets you view server logs in a more convenient fashion, with automatic log rotation provided by systemd. When making your project hostable as a systemd service, you should also enable the application/run/flush_stdout_on_print project setting. This way, journald (the systemd logging service) can collect logs while the process is running.

If you have experience with containers, you could also look into wrapping your dedicated server in a Docker container. This way, it can be used more easily in an automatic scaling setup (which is outside the scope of this tutorial).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
.
├── .godot
│   ├── exported
│   │   └── 133200997
│   │       └── export-78c237d4bfdb4e1d02e0b5f38ddfd8bd-scene.scn
│   ├── global_script_class_cache.cfg
│   ├── imported
│   │   ├── map_data.png-ce840618f399a990343bfc7298195a13.ctex
│   │   ├── music.ogg-fa883da45ae49695a3d022f64e60aee2.oggvorbisstr
│   │   └── sprite.png-7958af25f91bb9dbae43f35388f8e840.ctex
│   └── uid_cache.bin
├── client
│   ├── music.ogg.import
│   └── sprite.png.import
├── server
│   └── map_data.png.import
├── test
│   └── scene.gd
└── unused
│   └── development_test.gd
├── project.binary
├── scene.gd
├── scene.tscn.remap
```

Example 2 (unknown):
```unknown
.
├── .godot
│   ├── exported
│   │   └── 3400186661
│   │       ├── export-78c237d4bfdb4e1d02e0b5f38ddfd8bd-scene.scn
│   │       ├── export-7958af25f91bb9dbae43f35388f8e840-sprite.res  # Placeholder texture
│   │       └── export-fa883da45ae49695a3d022f64e60aee2-music.res
│   ├── global_script_class_cache.cfg
│   ├── imported
│   │   └── map_data.png-ce840618f399a990343bfc7298195a13.ctex
│   └── uid_cache.bin
├── client
│   ├── music.ogg.import
│   └── sprite.png.import  # Points to placeholder texture
└── server
│   └── map_data.png.import
├── project.binary
├── scene.gd
├── scene.tscn.remap
```

Example 3 (markdown):
```markdown
# Note: Feature tags are case-sensitive.
if OS.has_feature("dedicated_server"):
    # Run your server startup code here...
    pass
```

Example 4 (json):
```json
// Note: Feature tags are case-sensitive.
if (OS.HasFeature("dedicated_server"))
{
    // Run your server startup code here...
}
```

---

## Android — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/android/index.html

**Contents:**
- Android

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Platform-specific — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/index.html

**Contents:**
- Platform-specific

Godot supports both running the editor and exporting projects on several platforms. Usage of the engine is generally similar across platforms, but there are some platform-specific considerations, which are covered in this section.

For platform-specific versions of the editor, see Using the XR editor, Using the Android editor, and Using the Web editor. For exporting to specific platforms, see the Export section.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Godot Android plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html

**Contents:**
- Godot Android plugins
- Introduction
- Android plugin
  - v2 Architecture
  - v2 Packaging format
- Building a v2 Android plugin
  - Building a v2 Android plugin with GDExtension capabilities
  - Migrating a v1 Android plugin to v2
- Packaging a v2 Android plugin
  - Packaging a v2 Android plugin with GDExtension capabilities

Android plugins are powerful tools to extend the capabilities of the Godot engine by tapping into the functionality provided by Android platforms and ecosystem.

For example in Godot 4, Android plugins are used to support multiple Android-based XR platforms without encumbering the core codebase with vendor specific code or binaries.

Version 1 (v1) of the Android plugin system was introduced in Godot 3 and compatible with Godot 4.0 and 4.1. That version allowed developers to augment the Godot engine with Java, Kotlin and native functionality.

Starting in Godot 4.2, Android plugins built on the v1 architecture are now deprecated. Instead, Godot 4.2 introduces a new Version 2 (v2) architecture for Android plugins.

Godot Android plugin leverages the Gradle build system.

Building on the previous v1 architecture, Android plugins continue to be derived from the Android archive library.

At its core, a Godot Android plugin v2 is an Android library with a dependency on the Godot Android library, and a custom Android library manifest.

This architecture allows Android plugins to extend the functionality of the engine with:

Android platform APIs

Kotlin and Java libraries

Native libraries (via JNI)

GDExtension libraries

Each plugin has an init class extending from the GodotPlugin class which is provided by the Godot Android library.

The GodotPlugin class provides APIs to access the running Godot instance and hook into its lifecycle. It is loaded at runtime by the Godot engine.

v1 Android plugins required a custom gdap configuration file that was used by the Godot Editor to detect and load them. However this approach had several drawbacks, primary ones being that it lacked flexibility and departed from the existing Godot EditorExportPlugin format, delivery and installation flow.

This has been resolved for v2 Android plugins by deprecating the gdap packaging and configuration mechanism in favor of the existing Godot EditorExportPlugin packaging format. The EditorExportPlugin API in turn has been extended to properly support Android plugins.

A github project template is provided at https://github.com/m4gr3d/Godot-Android-Plugin-Template as a quickstart for building Godot Android plugins for Godot 4.2+. You can follow the template README to set up your own Godot Android plugin project.

To provide further understanding, here is a break-down of the steps used to create the project template:

Create an Android library module using these instructions

Add the Godot Android library as a dependency by updating the module's gradle build file:

The Godot Android library is hosted on MavenCentral, and updated for each release.

Create GodotAndroidPlugin, an init class for the plugin extending GodotPlugin.

If the plugin exposes Kotlin or Java methods to be called from GDScript, they must be annotated with @UsedByGodot. The name called from GDScript must match the method name exactly. There is no coercing snake_case to camelCase. For example, from GDScript:

If the plugin uses signals, the init class must return the set of signals used by overriding GodotPlugin::getPluginSignals(). To emit signals, the plugin can use the GodotPlugin::emitSignal(...) method.

Update the plugin AndroidManifest.xml file with the following meta-data:

PluginName is the name of the plugin

plugin.init.ClassFullName is the full component name (package + class name) of the plugin init class (e.g: org.godotengine.plugin.android.template.GodotAndroidPlugin).

Create the EditorExportPlugin configuration to package the plugin. The steps used to create the configuration can be seen in the Packaging a v2 Android plugin section.

Similar to GDNative support in v1 Android plugins, v2 Android plugins support the ability to integrate GDExtension capabilities.

A github project template is provided at https://github.com/m4gr3d/GDExtension-Android-Plugin-Template as a quickstart for building GDExtension Android plugins for Godot 4.2+. You can follow the template's README to set up your own Godot Android plugin project.

Use the following steps if you have a v1 Android plugin you want to migrate to v2:

Update the plugin's manifest file:

Change the org.godotengine.plugin.v1 prefix to org.godotengine.plugin.v2

Update the Godot Android library build dependency:

You can continue using the godot-lib.<version>.<status>.aar binary from Godot's download page if that's your preference. Make sure it's updated to the latest stable version.

Or you can switch to the MavenCentral provided dependency:

After updating the Godot Android library dependency, sync or build the plugin and resolve any compile errors:

The Godot instance provided by GodotPlugin::getGodot() no longer has access to an android.content.Context reference. Use GodotPlugin::getActivity() instead.

Delete the gdap configuration file(s) and follow the instructions in the Packaging a v2 Android plugin section to set up the plugin configuration.

As mentioned, a v2 Android plugin is now provided to the Godot Editor as an EditorExportPlugin plugin, so it shares a lot of the same packaging steps.

Add the plugin output binaries within the plugin directory (e.g: in addons/<plugin_name>/)

Add the tool script for the export functionality within the plugin directory (e.g: in addons/<plugin_name>/)

The created script must be a @tool script, or else it will not work properly

The export tool script is used to configure the Android plugin and hook it within the Godot Editor's export process. It should look something like this:

Create a plugin.cfg. This is an INI file with metadata about your plugin:

For reference, here is the folder structure for the Godot Android plugin project template. At build time, the contents of the export_scripts_template directory as well as the generated plugin binaries are copied to the addons/<plugin_name> directory:

For GDExtension, we follow the same steps as for Packaging a v2 Android plugin and add the GDExtension config file in the same location as plugin.cfg.

For reference, here is the folder structure for the GDExtension Android plugin project template. At build time, the contents of the export_scripts_template directory as well as the generated plugin binaries are copied to the addons/<plugin_name> directory:

Here is what the plugin.gdextension config file should look like:

Of note is the android_aar_plugin field that specifies this GDExtension module is provided as part of a v2 Android plugin. During the export process, this will indicate to the Godot Editor that the GDExtension native shared libraries are exported by the Android plugin AAR binaries.

For GDExtension Android plugins, the plugin init class must override GodotPlugin::getPluginGDExtensionLibrariesPaths(), and return the paths to the bundled GDExtension libraries config files (*.gdextension).

The paths must be relative to the Android library's assets directory. At runtime, the plugin will provide these paths to the Godot engine which will use them to load and initialize the bundled GDExtension libraries.

Godot 4.2 or higher is required

v2 Android plugin requires the use of the Gradle build process.

The provided github project templates include demo Godot projects for quick testing.

Copy the plugin's output directory (addons/<plugin_name>) to the target Godot project's directory

Open the project in the Godot Editor; the Editor should detect the plugin

Navigate to Project -> Project Settings... -> Plugins, and ensure the plugin is enabled

Install the Godot Android build template by clicking on Project -> Install Android Build Template...

Navigate to Project -> Export...

In the Export window, create an Android export preset

In the Android export preset, scroll to Gradle Build and set Use Gradle Build to true

Update the project's scripts as needed to access the plugin's functionality. For example:

Connect an Android device to your machine and run the project on it

Since they are also Android libraries, Godot v2 Android plugins can be stripped from their EditorExportPlugin packaging and provided as raw AAR binaries for use as libraries alongside the Godot Android library by Android apps.

If targeting this use-case, make sure to include additional instructions for how the AAR binaries should be included (e.g: custom additions to the Android app's manifest).

Godot Android Plugins Samples

Godot Android Plugin Template

GDExtension Android Plugin Template

To make it easier to access the exposed Java / Kotlin APIs in the Godot Editor, it's recommended to provide one (or multiple) gdscript wrapper class(es) for your plugin users to interface with.

If planning to use the GDExtension functionality in the Godot Editor, it is recommended that the GDExtension's native binaries are compiled not just for Android, but also for the OS onto which developers / users intend to run the Godot Editor. Not doing so may prevent developers / users from writing code that accesses the plugin from within the Godot Editor.

This may involve creating dummy plugins for the host OS just so the API is published to the editor. You can use the godot-cpp-template github template for reference on how to do so.

Check adb logcat for possible problems, then:

Check that the methods exposed by the plugin used the following Java types: void, boolean, int, float, java.lang.String, org.godotengine.godot.Dictionary, int[], byte[], float[], java.lang.String[].

More complex datatypes are not supported for now.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
dependencies {
    implementation("org.godotengine:godot:4.2.0.stable")
}
```

Example 2 (gdscript):
```gdscript
if Engine.has_singleton("MyPlugin"):
    var singleton = Engine.get_singleton("MyPlugin")
    print(singleton.myPluginFunction("World"))
```

Example 3 (typescript):
```typescript
<meta-data
    android:name="org.godotengine.plugin.v2.[PluginName]"
    android:value="[plugin.init.ClassFullName]" />
```

Example 4 (json):
```json
dependencies {
    implementation("org.godotengine:godot:4.2.0.stable")
}
```

---

## Godot Android library — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/android/android_library.html

**Contents:**
- Godot Android library
- Using the Godot Android library
- Godot Android plugins
- Embedding Godot in existing Android projects
  - 1. Create the Android app
  - 2. Create the Godot project
  - 3. Build and run the app
- User-contributed notes

The Godot Engine for Android platforms is designed to be used as an Android library. This architecture enables several key features on Android platforms:

Ability to integrate the Gradle build system within the Godot Editor, which provides the ability to leverage more components from the Android ecosystem such as libraries and tools

Ability to make the engine portable and embeddable:

Key in enabling the port of the Godot Editor to Android and mobile XR devices

Key in allowing the integration and reuse of Godot's capabilities within existing codebase

Below we describe some of the use-cases and scenarios this architecture enables.

The Godot Android library is packaged as an AAR archive file and hosted on MavenCentral along with its documentation.

It provides access to Godot APIs and capabilities on Android platforms for the following non-exhaustive use-cases.

Android plugins are powerful tools to extend the capabilities of the Godot Engine by tapping into the functionality provided by Android platforms and ecosystem.

An Android plugin is an Android library with a dependency on the Godot Android library which the plugin uses to integrate into the engine's lifecycle and to access Godot APIs, granting it powerful capabilities such as GDExtension support which allows to update / mod the engine behavior as needed.

For more information, see Godot Android plugins.

The Godot Engine can be embedded within existing Android applications or libraries, allowing developers to leverage mature and battle-tested code and libraries better suited to a specific task.

The hosting component is responsible for driving the engine lifecycle via Godot's Android APIs. These APIs can also be used to provide bidirectional communication between the host and the embedded Godot instance allowing for greater control over the desired experience.

We showcase how this is done using a sample Android app that embeds the Godot Engine as an Android view, and uses it to render 3D glTF models.

The GLTF Viewer sample app uses an Android RecyclerView component to create a list of glTF items, populated from Kenney's Food Kit pack. When an item on the list is selected, the app's logic interacts with the embedded Godot Engine to render the selected glTF item as a 3D model.

The sample app source code can be found on GitHub. Follow the instructions on its README to build and install it.

Below we break-down the steps used to create the GLTF Viewer app.

Currently only a single instance of the Godot Engine is supported per process. You can configure the process the Android Activity runs under using the android:process attribute.

Automatic resizing / orientation configuration events are not supported and may cause a crash. You can disable those events:

By locking to a specific orientation using the android:screenOrientation attribute.

By declaring that the Activity will handle these configuration events using the android:configChanges attribute.

The Android sample app was created using Android Studio and using Gradle as the build system.

The Android ecosystem provides multiple tools, IDEs, build systems for creating Android apps so feel free to use what you're familiar with, and update the steps below accordingly (contributions to this documentation are welcomed as well!).

Set up an Android application project. It may be a brand new empty project, or an existing project

Add the maven dependency for the Godot Android library

If using gradle, add the following to the dependency section of the app's gradle build file. Make sure to update <version> to the latest version of the Godot Android library:

If using gradle, include the following aaptOptions configuration under the android > defaultConfig section of the app's gradle build file. Doing so allows gradle to include Godot's hidden directories when building the app binary.

If your build system does not support including hidden directories, you can configure the Godot project to not use hidden directories by deselecting Application > Config > Use Hidden Project Data Directory in the Project Settings.

Create / update the application's Activity that will be hosting the Godot Engine instance. For the sample app, this is MainActivity

The host Activity should implement the GodotHost interface

The sample app uses Fragments to organize its UI, so it uses GodotFragment, a fragment component provided by the Godot Android library to automatically host and manage the Godot Engine instance.

The Godot Android library also provide GodotActivity, an Activity component that can be extended to automatically host and manage the Godot Engine instance.

Alternatively, applications can directly create a Godot instance, host and manage it themselves.

Using GodotHost#getHostPlugins(...), the sample app creates a runtime GodotPlugin instance that's used to send signals to the gdscript logic

The runtime GodotPlugin can also be used by gdscript logic to access JVM methods. For more information, see Godot Android plugins.

Add any additional logic that will be used by your application

For the sample app, this includes adding the ItemsSelectionFragment fragment (and related classes), a fragment used to build and show the list of glTF items

Open the AndroidManifest.xml file, and configure the orientation if needed using the android:screenOrientation attribute

If needed, disable automatic resizing / orientation configuration changes using the android:configChanges attribute

On Android, Godot's project files are exported to the assets directory of the generated apk binary.

We leverage that architecture to bind our Android app and Godot project together by creating the Godot project in the Android app's assets directory.

Note that it's also possible to create the Godot project in a separate directory and export it as a PCK or ZIP file to the Android app's assets directory. Using this approach requires passing the --main-pack <pck_or_zip_filepath_relative_to_assets_dir> argument to the hosted Godot Engine instance using GodotHost#getCommandLine().

The instructions below and the sample app follow the first approach of creating the Godot project in the Android app's assets directory.

As mentioned in the note above, open the Godot Editor and create a Godot project directly (no subfolder) in the assets directory of the Android application project

See the sample app's Godot project for reference

Configure the Godot project as desired

Make sure the orientation set for the Godot project matches the one set in the Android app's manifest

For Android, make sure textures/vram_compression/import_etc2_astc is set to true

Update the Godot project script logic as needed

For the sample app, the script logic queries for the runtime GodotPlugin instance and uses it to register for signals fired by the app logic

The app logic fires a signal every time an item is selected in the list. The signal contains the filepath of the glTF model, which is used by the gdscript logic to render the model.

Once you complete configuration of your Godot project, build and run the Android app. If set up correctly, the host Activity will initialize the embedded Godot Engine on startup. The Godot Engine will check the assets directory for project files to load (unless configured to look for a main pack), and will proceed to run the project.

While the app is running on device, you can check Android logcat to investigate any errors or crashes.

For reference, check the build and install instructions for the GLTF Viewer sample app.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
implementation("org.godotengine:godot:<version>")
```

Example 2 (typescript):
```typescript
android {

  defaultConfig {
      // The default ignore pattern for the 'assets' directory includes hidden files and
      // directories which are used by Godot projects, so we override it with the following.
      aaptOptions {
          ignoreAssetsPattern "!.svn:!.git:!.gitignore:!.ds_store:!*.scc:<dir>_*:!CVS:!thumbs.db:!picasa.ini:!*~"
      }
    ...
```

Example 3 (swift):
```swift
private var godotFragment: GodotFragment? = null

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    setContentView(R.layout.activity_main)

    val currentGodotFragment = supportFragmentManager.findFragmentById(R.id.godot_fragment_container)
    if (currentGodotFragment is GodotFragment) {
        godotFragment = currentGodotFragment
    } else {
        godotFragment = GodotFragment()
        supportFragmentManager.beginTransaction()
            .replace(R.id.godot_fragment_container, godotFragment!!)
            .commitNowAllowingStateLoss()
    }

    ...
```

Example 4 (jsx):
```jsx
<activity android:name=".MainActivity"
    android:screenOrientation="fullUser"
    android:configChanges="orientation|screenSize|smallestScreenSize|screenLayout"
    android:exported="true">

    ...
</activity>
```

---

## Integrating with Android APIs — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/android/javaclasswrapper_and_androidruntimeplugin.html

**Contents:**
- Integrating with Android APIs
- JavaClassWrapper (Godot singleton)
- AndroidRuntime plugin
  - Example: Show an Android toast
  - Example: Vibrate the device
  - Example: Accessing inner classes
  - Example: Calling a constructor
- User-contributed notes

The Android platform has numerous APIs as well as a rich ecosystem of third-party libraries with wide and diverse functionality, like push notifications, analytics, authentication, ads, etc...

These don't make sense in Godot core itself so Godot has long provided an Android plugin system. The Android plugin system enables developers to create Godot Android plugins using Java or Kotlin code, which provides an interface to access and use Android APIs or third-party libraries in Godot projects from GDScript, C# or GDExtension.

Writing an Android plugin however requires knowledge of Java or Kotlin code, which most Godot developers do not have. As such there are many Android APIs and third-party libraries that don't have a Godot plugin that developers can interface with. In fact, this is one of the main reasons that developers cite for not being able to switch to Godot from other game engines.

To address this, we've introduced a couple of tools in Godot 4.4 to simplify the process for developers to access Android APIs and third-party libraries.

JavaClassWrapper is a Godot singleton which allows creating instances of Java / Kotlin classes and calling methods on them using only GDScript, C# or GDExtension.

In the code snippet above, JavaClassWrapper is used from GDScript to access the Java LocalDateTime and DateTimeFormatter classes. Through JavaClassWrapper, we can call the Java classes methods directly from GDScript as if they were GDScript methods.

JavaClassWrapper is great, but to do many things on Android, you need access to various Android lifecycle / runtime objects. AndroidRuntime plugin is a built-in Godot Android plugin that allows you to do this.

Combining JavaClassWrapper and AndroidRuntime plugin allows developers to access and use Android APIs without switching away from GDScript, or using any tools aside from Godot itself. This is huge for the adoption of Godot for Android development:

If you need to do something simple, or only use a small part of a third-party library, you don't have to make a plugin

It allows developers to quickly integrate Android functionality

It allows developers to create Godot addons using only GDScript and JavaClassWrapper (no Java or Kotlin needed)

For exports using gradle, Godot will automatically include .jar or .aar files it find in the project addons directory. So to use a third-party library, you can just drop its .jar or .aar file in the addons directory, and call its method directly from GDScript using JavaClassWrapper.

Java inner classes can be accessed using the $ sign:

A constructor is invoked by calling a method with the same name as the class.

This example creates an intent to send a text:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
class MyAndroidSingleton(godot: Godot?) : GodotPlugin(godot) {
        @UsedByGodot
        fun doSomething(value: String) {
                // ...
        }
}
```

Example 2 (gdscript):
```gdscript
var LocalDateTime = JavaClassWrapper.wrap("java.time.LocalDateTime")
var DateTimeFormatter = JavaClassWrapper.wrap("java.time.format.DateTimeFormatter")

var datetime = LocalDateTime.now()
var formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss")

print(datetime.format(formatter))
```

Example 3 (php):
```php
# Retrieve the AndroidRuntime singleton.
var android_runtime = Engine.get_singleton("AndroidRuntime")
if android_runtime:
    # Retrieve the Android Activity instance.
    var activity = android_runtime.getActivity()

    # Create a Godot Callable to wrap the toast display logic.
    var toast_callable = func():
        # Use JavaClassWrapper to retrieve the android.widget.Toast class, then make and show a toast using the class APIs.
        var ToastClass = JavaClassWrapper.wrap("android.widget.Toast")
        ToastClass.makeText(activity, "This is a test", ToastClass.LENGTH_LONG).show()

    # Wrap the Callable in a Java Runnable and run it on the Android UI thread to show the toast.
    activity.runOnUiThread(android_runtime.createRunnableFromGodotCallable(toast_callable))
```

Example 4 (gdscript):
```gdscript
# Retrieve the AndroidRuntime singleton.
var android_runtime = Engine.get_singleton("AndroidRuntime")
if android_runtime:
    # Retrieve the Android Vibrator system service and check if the device supports it.
    var vibrator_service = android_runtime.getApplicationContext().getSystemService("vibrator")
    if vibrator_service and vibrator_service.hasVibrator():
        # Configure and run a VibrationEffect.
        var VibrationEffect = JavaClassWrapper.wrap("android.os.VibrationEffect")
        var effect = VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE)
        vibrator_service.vibrate(effect)
```

---

## The JavaScriptBridge singleton — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/web/javascript_bridge.html

**Contents:**
- The JavaScriptBridge singleton
- Interacting with JavaScript
- Callbacks
- Can I use my favorite library?
- The eval interface
- Downloading files
- User-contributed notes

In web builds, the JavaScriptBridge singleton allows interaction with JavaScript and web browsers, and can be used to implement some functionalities unique to the web platform.

Sometimes, when exporting Godot for the Web, it might be necessary to interface with external JavaScript code like third-party SDKs, libraries, or simply to access browser features that are not directly exposed by Godot.

The JavaScriptBridge singleton provides methods to wrap a native JavaScript object into a Godot JavaScriptObject that tries to feel natural in the context of Godot scripting (e.g. GDScript and C#).

The JavaScriptBridge.get_interface() method retrieves an object in the global scope.

The JavaScriptBridge.create_object() creates a new object via the JavaScript new constructor.

As you can see, by wrapping JavaScript objects into JavaScriptObject you can interact with them like they were native Godot objects, calling their methods, and retrieving (or even setting) their properties.

Base types (int, floats, strings, booleans) are automatically converted (floats might lose precision when converted from Godot to JavaScript). Anything else (i.e. objects, arrays, functions) are seen as JavaScriptObjects themselves.

Calling JavaScript code from Godot is nice, but sometimes you need to call a Godot function from JavaScript instead.

This case is a bit more complicated. JavaScript relies on garbage collection, while Godot uses reference counting for memory management. This means you have to explicitly create callbacks (which are returned as JavaScriptObjects themselves) and you have to keep their reference.

Arguments passed by JavaScript to the callback will be passed as a single Godot Array.

Callback methods created via JavaScriptBridge.get_interface() (_my_callback in the above example) must take exactly one Array argument, which is going to be the JavaScript arguments object converted to an array. Otherwise, the callback method will not be called.

Here is another example that asks the user for the Notification permission and waits asynchronously to deliver a notification if the permission is granted:

You most likely can. First, you have to include your library in the page. You can customize the Head Include during export (see below), or even write your own template.

In the example below, we customize the Head Include to add an external library (axios) from a content delivery network, and a second <script> tag to define our own custom function:

We can then access both the library and the function from Godot, like we did in previous examples:

The eval method works similarly to the JavaScript function of the same name. It takes a string as an argument and executes it as JavaScript code. This allows interacting with the browser in ways not possible with script languages integrated into Godot.

The value of the last JavaScript statement is converted to a GDScript value and returned by eval() under certain circumstances:

JavaScript number is returned as float

JavaScript boolean is returned as bool

JavaScript string is returned as String

JavaScript ArrayBuffer, TypedArray, and DataView are returned as PackedByteArray

Any other JavaScript value is returned as null.

HTML5 export templates may be built without support for the singleton to improve security. With such templates, and on platforms other than HTML5, calling JavaScriptBridge.eval will also return null. The availability of the singleton can be checked with the web feature tag:

GDScript's multi-line strings, surrounded by 3 quotes """ as in my_func3() above, are useful to keep JavaScript code readable.

The eval method also accepts a second, optional Boolean argument, which specifies whether to execute the code in the global execution context, defaulting to false to prevent polluting the global namespace:

Downloading files (e.g. a save game) from the Godot Web export to the user's computer can be done by directly interacting with JavaScript, but given it is a very common use case, Godot exposes this functionality to scripting via a dedicated JavaScriptBridge.download_buffer() function which lets you download any generated buffer.

Here is a minimal example on how to use it:

And here is a more complete example on how to download a previously saved file:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node

func _ready():
    # Retrieve the `window.console` object.
    var console = JavaScriptBridge.get_interface("console")
    # Call the `window.console.log()` method.
    console.log("test")
```

Example 2 (gdscript):
```gdscript
extends Node

func _ready():
    # Call the JavaScript `new` operator on the `window.Array` object.
    # Passing 10 as argument to the constructor:
    # JS: `new Array(10);`
    var arr = JavaScriptBridge.create_object("Array", 10)
    # Set the first element of the JavaScript array to the number 42.
    arr[0] = 42
    # Call the `pop` function on the JavaScript array.
    arr.pop()
    # Print the value of the `length` property of the array (9 after the pop).
    print(arr.length)
```

Example 3 (gdscript):
```gdscript
extends Node

# Here we create a reference to the `_my_callback` function (below).
# This reference will be kept until the node is freed.
var _callback_ref = JavaScriptBridge.create_callback(_my_callback)

func _ready():
    # Get the JavaScript `window` object.
    var window = JavaScriptBridge.get_interface("window")
    # Set the `window.onbeforeunload` DOM event listener.
    window.onbeforeunload = _callback_ref

func _my_callback(args):
    # Get the first argument (the DOM event in our case).
    var js_event = args[0]
    # Call preventDefault and set the `returnValue` property of the DOM event.
    js_event.preventDefault()
    js_event.returnValue = ''
```

Example 4 (gdscript):
```gdscript
extends Node

# Here we create a reference to the `_on_permissions` function (below).
# This reference will be kept until the node is freed.
var _permission_callback = JavaScriptBridge.create_callback(_on_permissions)

func _ready():
    # NOTE: This is done in `_ready` for simplicity, but SHOULD BE done in response
    # to user input instead (e.g. during `_input`, or `button_pressed` event, etc.),
    # otherwise it might not work.

    # Get the `window.Notification` JavaScript object.
    var notification = JavaScriptBridge.get_interface("Notification")
    # Call the `window.Notification.requestPermission` method which returns a JavaScript
    # Promise, and bind our callback to it.
    notification.requestPermission().then(_permission_callback)

func _on_permissions(args):
    # The first argument of this callback is the string "granted" if the permission is granted.
    var permission = args[0]
    if permission == "granted":
        print("Permission granted, sending notification.")
        # Create the notification: `new Notification("Hi there!")`
        JavaScriptBridge.create_object("Notification", "Hi there!")
    else:
        print("No notification permission.")
```

---

## Web — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/web/index.html

**Contents:**
- Web

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## iOS plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/ios/index.html

**Contents:**
- iOS plugins

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Creating iOS plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/ios/ios_plugin.html

**Contents:**
- Creating iOS plugins
- Loading and using an existing plugin
- Creating an iOS plugin
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

This page explains what iOS plugins can do for you, how to use an existing plugin, and the steps to code a new one.

iOS plugins allow you to use third-party libraries and support iOS-specific features like In-App Purchases, GameCenter integration, ARKit support, and more.

An iOS plugin requires a .gdip configuration file, a binary file which can be either .a static library or .xcframework containing .a static libraries, and possibly other dependencies. To use it, you need to:

Copy the plugin's files to your Godot project's res://ios/plugins directory. You can also group files in a sub-directory, like res://ios/plugins/my_plugin.

The Godot editor automatically detects and imports .gdip files inside res://ios/plugins and its subdirectories.

You can find and activate detected plugins by going to Project -> Export... -> iOS and in the Options tab, scrolling to the Plugins section.

When a plugin is active, you can access it in your code using Engine.get_singleton():

The plugin's files have to be in the res://ios/plugins/ directory or a subdirectory, otherwise the Godot editor will not automatically detect them.

At its core, a Godot iOS plugin is an iOS library (.a archive file or .xcframework containing static libraries) with the following requirements:

The library must have a dependency on the Godot engine headers.

The library must come with a .gdip configuration file.

An iOS plugin can have the same functionality as a Godot module but provides more flexibility and doesn't require to rebuild the engine.

Here are the steps to get a plugin's development started. We recommend using Xcode as your development environment.

The Godot iOS Plugins.

The Godot iOS plugin template gives you all the boilerplate you need to get your iOS plugin started.

To build an iOS plugin:

Create an Objective-C static library for your plugin inside Xcode.

Add the Godot engine header files as a dependency for your plugin library in HEADER_SEARCH_PATHS. You can find the setting inside the Build Settings tab:

Download the Godot engine source from the Godot GitHub page.

Run SCons to generate headers. You can learn the process by reading Compiling for iOS. You don't have to wait for compilation to complete to move forward as headers are generated before the engine starts to compile.

You should use the same header files for iOS plugins and for the iOS export template.

In the Build Settings tab, specify the compilation flags for your static library in OTHER_CFLAGS. The most important ones are -fcxx-modules, -fmodules, and -DDEBUG if you need debug support. Other flags should be the same you use to compile Godot. For instance:

Add the required logic for your plugin and build your library to generate a .a file. You will probably need to build both debug and release target .a files. Depending on your needs, pick either or both. If you need both debug and release .a files, their name should match following pattern: [PluginName].[TargetType].a. You can also build the static library with your SCons configuration.

The iOS plugin system also supports .xcframework files. To generate one, you can use a command such as:

Create a Godot iOS Plugin configuration file to help the system detect and load your plugin:

The configuration file extension must be gdip (e.g.: MyPlugin.gdip).

The configuration file format is as follow:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
if Engine.has_singleton("MyPlugin"):
    var singleton = Engine.get_singleton("MyPlugin")
    print(singleton.foo())
```

Example 2 (unknown):
```unknown
-DPTRCALL_ENABLED -DDEBUG_ENABLED -DDEBUG_MEMORY_ALLOC -DDISABLE_FORCED_INLINE -DTYPED_METHOD_BIND
```

Example 3 (unknown):
```unknown
xcodebuild -create-xcframework -library [DeviceLibrary].a -library [SimulatorLibrary].a -output [PluginName].xcframework
```

Example 4 (typescript):
```typescript
[config]
    name="MyPlugin"
    binary="MyPlugin.a"

    initialization="init_my_plugin"
    deinitialization="deinit_my_plugin"

    [dependencies]
    linked=[]
    embedded=[]
    system=["Foundation.framework"]

    capabilities=["arkit", "metal"]

    files=["data.json"]

    linker_flags=["-ObjC"]

    [plist]
    PlistKeyWithDefaultType="Some Info.plist key you might need"
    StringPlistKey:string="String value"
    IntegerPlistKey:integer=42
    BooleanPlistKey:boolean=true
    RawPlistKey:raw="
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
    "
    StringPlistKeyToInput:string_input="Type something"

The ``config`` section and fields are required and defined as follow:

    -   **name**: name of the plugin

    -   **binary**: this should be the filepath of the plugin library (``a`` or ``xcframework``) file.

        -   The filepath can be relative (e.g.: ``MyPlugin.a``, ``MyPlugin.xcframework``) in which case it's relative to the directory where the ``gdip`` file is located.
        -   The filepath can be absolute: ``res://some_path/MyPlugin.a`` or ``res://some_path/MyPlugin.xcframework``.
        -   In case you need multitarget library usage, the filename should be ``MyPlugin.a`` and ``.a`` files should be named as ``MyPlugin.release.a`` and ``MyPlugin.debug.a``.
        -   In case you use multitarget ``xcframework`` libraries, their filename in the configuration should be ``MyPlugin.xcframework``. The ``.xcframework`` files should be named as ``MyPlugin.release.xcframework`` and ``MyPlugin.debug.xcframework``.

The ``dependencies`` and ``plist`` sections are optional and defined as follow:

    -   **dependencies**:

        -   **linked**: contains a list of iOS frameworks that the iOS application should be linked with.

        -   **embedded**: contains a list of iOS frameworks or libraries that should be both linked and embedded into the resulting iOS application.

        -   **system**: contains a list of iOS system frameworks that are required for plugin.

        -   **capabilities**: contains a list of iOS capabilities that is required for plugin. A list of available capabilities can be found at `Apple UIRequiredDeviceCapabilities documentation page <https://developer.apple.com/documentation/bundleresources/information_property_list/uirequireddevicecapabilities>`_.

        -   **files**: contains a list of files that should be copied on export. This is useful for data files or images.

        -   **linker_flags**: contains a list of linker flags to add to the Xcode project when exporting the plugin.

    -   **plist**: should have keys and values that should be present in ``Info.plist`` file.

        -   Each line should follow pattern: ``KeyName:KeyType=KeyValue``
        -   Supported values for ``KeyType`` are ``string``, ``integer``, ``boolean``, ``raw``, ``string_input``
        -   If no type is used (e.g.: ``KeyName="KeyValue"``) ``string`` type will be used.
        -   If ``raw`` type is used value for corresponding key will be stored in ``Info.plist`` as is.
        -   If ``string_input`` type is used you will be able to modify value in Export window.
```

---

## Custom HTML page for Web export — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/web/customizing_html5_shell.html

**Contents:**
- Custom HTML page for Web export
- Setup
- Starting the project
- Customizing the behavior
- Customizing the presentation
- Debugging
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

While Web export templates provide a default HTML page fully capable of launching the project without any further customization, it may be beneficial to create a custom HTML page. While the game itself cannot easily be directly controlled from the outside yet, such page allows to customize the initialization process for the engine.

Some use-cases where customizing the default page is useful include:

Loading files from a different directory than the page;

Loading a .zip file instead of a .pck file as the main pack;

Loading the engine from a different directory than the main pack file;

Adding a click-to-play button so that games can be started in the fullscreen mode;

Loading some extra files before the engine starts, making them available in the project file system as soon as possible;

Passing custom command line arguments, e.g. -s to start a MainLoop script.

The default HTML page is available in the Godot Engine repository at /misc/dist/html/full-size.html but the following template can be used as a much simpler example:

As shown by the example above, it is mostly a regular HTML document, with few placeholders which needs to be replaced during export, an html <canvas> element, and some simple JavaScript code that calls the Engine() class.

The only required placeholders are:

$GODOT_URL: The name of the main JavaScript file, which provides the Engine() class required to start the engine and that must be included in the HTML as a <script>. The name is generated from the Export Path during the export process.

$GODOT_CONFIG: A JavaScript object, containing the export options and can be later overridden. See EngineConfig for the full list of overrides.

The following optional placeholders will enable some extra features in your custom HTML template.

$GODOT_PROJECT_NAME: The project name as defined in the Name setting in Project Settings > Application > Config. It is a good idea to use it as a <title> in your template.

$GODOT_HEAD_INCLUDE: A custom string to include in the HTML document just before the end of the <head> tag. It is customized in the export options under the Html / Head Include section. While you fully control the HTML page you create, this variable can be useful for configuring parts of the HTML head element from the Godot Editor, e.g. for different Web export presets.

$GODOT_SPLASH: The path to the image used as the boot splash as defined in the Image setting in Project Settings > Application > Boot Splash.

$GODOT_SPLASH_COLOR The splash screen background color as defined in the BG Color setting in Project Settings > Application > Boot Splash, converted to a hex color code.

$GODOT_SPLASH_CLASSES: This placeholder provides a string of setting names and their values, which affect the splash screen. This string is meant to be used as a set of CSS class names, which allows styling the splash image based on the splash project settings. The following settings from Project Settings > Application > Boot Splash are provided, represented by the class names shown below depending on the setting's boolean value:

Show Image: show-image--true, show-image--false

Fullsize: fullsize--true, fullsize--false

Use Filter: use-filter--true, use-filter--false

When the custom page is ready, it can be selected in the export options under the Html / Custom Html Shell section.

To be able to start the game, you need to write a script that initializes the engine — the control code. This process consists of three steps, but as shown here, most of them can be skipped depending on how much customization is needed.

See the HTML5 shell class reference, for the full list of methods and options available.

First, the engine must be loaded, then it needs to be initialized, and after this the project can finally be started. You can perform every of these steps manually and with great control. However, in the simplest case all you need to do is to create an instance of the Engine() class with the exported configuration, and then call the engine.startGame method optionally overriding any EngineConfig parameters.

This snippet of code automatically loads and initializes the engine before starting the game. It uses the given configuration to load the engine. The engine.startGame method is asynchronous and returns a Promise. This allows your control code to track if the game was loaded correctly without blocking execution or relying on polling.

In case your project needs to have special control over the start arguments and dependency files, the engine.start method can be used instead. Note, that this method do not automatically preload the pck file, so you will probably want to manually preload it (and any other extra file) via the engine.preloadFile method.

Optionally, you can also manually engine.init to perform specific actions after the module initialization, but before the engine starts.

This process is a bit more complex, but gives you full control over the engine startup process.

To load the engine manually the Engine.load() static method must be called. As this method is static, multiple engine instances can be spawned if the share the same wasm.

Multiple instances cannot be spawned by default, as the engine is immediately unloaded after it is initialized. To prevent this from happening see the unloadAfterInit override option. It is still possible to unload the engine manually afterwards by calling the Engine.unload() static method. Unloading the engine frees browser memory by unloading files that are no longer needed once the instance is initialized.

In the Web environment several methods can be used to guarantee that the game will work as intended.

If you target a specific version of WebGL, or just want to check if WebGL is available at all, you can call the Engine.isWebGLAvailable() method. It optionally takes an argument that allows to test for a specific major version of WebGL.

As the real executable file does not exist in the Web environment, the engine only stores a virtual filename formed from the base name of loaded engine files. This value affects the output of the OS.get_executable_path() method and defines the name of the automatically started main pack. The executable override option can be used to override this value.

Several configuration options can be used to further customize the look and behavior of the game on your page.

By default, the first canvas element on the page is used for rendering. To use a different canvas element the canvas override option can be used. It requires a reference to the DOM element itself.

The way the engine resize the canvas can be configured via the canvasResizePolicy override option.

If your game takes some time to load, it may be useful to display a custom loading UI which tracks the progress. This can be achieved with the onProgress callback option, which allows to set up a callback function that will be called regularly as the engine loads new bytes.

Be aware that in some cases total can be 0. This means that it cannot be calculated.

If your game supports multiple languages, the locale override option can be used to force a specific locale, provided you have a valid language code string. It may be good to use server-side logic to determine which languages a user may prefer. This way the language code can be taken from the Accept-Language HTTP header, or determined by a GeoIP service.

To debug exported projects, it may be useful to read the standard output and error streams generated by the engine. This is similar to the output shown in the editor console window. By default, standard console.log and console.warn are used for the output and error streams respectively. This behavior can be customized by setting your own functions to handle messages.

Use the onPrint override option to set a callback function for the output stream, and the onPrintError override option to set a callback function for the error stream.

When handling the engine output, keep in mind that it may not be desirable to print it out in the finished product.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (html):
```html
<!DOCTYPE html>
<html>
    <head>
        <title>My Template</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <canvas id="canvas"></canvas>
        <script src="$GODOT_URL"></script>
        <script>
            var engine = new Engine($GODOT_CONFIG);
            engine.startGame();
        </script>
    </body>
</html>
```

Example 2 (javascript):
```javascript
const engine = new Engine($GODOT_CONFIG);
engine.startGame({
    /* optional override configuration, eg. */
    // unloadAfterInit: false,
    // canvasResizePolicy: 0,
    // ...
});
```

Example 3 (javascript):
```javascript
const myWasm = 'mygame.wasm';
const myPck = 'mygame.pck';
const engine = new Engine();
Promise.all([
    // Load and init the engine
    engine.init(myWasm),
    // And the pck concurrently
    engine.preloadFile(myPck),
]).then(() => {
    // Now start the engine.
    return engine.start({ args: ['--main-pack', myPck] });
}).then(() => {
    console.log('Engine has started!');
});
```

Example 4 (css):
```css
const canvasElement = document.querySelector("#my-canvas-element");
engine.startGame({ canvas: canvasElement });
```

---

## Console support in Godot — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/platform/consoles.html

**Contents:**
- Console support in Godot
- Console porting process
- Console publishing process
- Third-party support
- Middleware
- User-contributed notes

In order to develop for consoles in Godot, you need access to the console SDK and export templates for it. These export templates need to be developed either by yourself or someone hired to do it, or provided by a third-party company.

Currently, the only console Godot officially supports is Steam Deck (through the official Linux export templates).

The reasons other consoles are not officially supported are the risks of legal liability, disproportionate cost, and open source licensing issues. The reasons are explained in more detail in this article About Official Console Ports

As explained, however, it is possible to port your games to consoles thanks to services provided by third-party companies.

In practice, the process is quite similar to Unity and Unreal Engine. In other words, there is no engine that is legally allowed to distribute console export templates without requiring the user to prove that they are a licensed console developer.

Regardless of the engine used to create the game, the process to publish a game to a console platform is as follows:

Register a developer account on the console manufacturer's website, then sign NDAs and publishing contracts. This requires you to have a registered legal entity.

Gain access to the publishing platform by passing the acceptance process. This can take up to several months. Note that this step is significantly easier if an established publisher is backing your game. Nintendo is generally known to be more accepting of smaller developers, but this is not guaranteed.

Get access to developer tools and order a console specially made for developers (devkit). The cost of those devkits is confidential.

Port your game to the console platform or pay a company to do it.

To be published, your game needs to be rated in the regions you'd like to sell it in. For example, game ratings are handled by ESRB in North America, and PEGI in Europe. Indie developers can generally get a rating for cheaper compared to more established developers.

Due to the complexity of the process, many studios and developers prefer to outsource console porting.

You can read more about the console publishing process in this article: Godot and consoles, all you need to know

Console ports of Godot are offered by third-party companies (which have ported Godot on their own). Some of these companies also offer publishing of your games to various consoles.

The following is a list of some of the providers:

Lone Wolf Technology offers Switch and Playstation 4 porting and publishing of Godot games.

Pineapple Works offers Nintendo Switch 1 & 2, Xbox One & Xbox Series X/S, PlayStation 5 porting and publishing of Godot games (GDScript/C#).

RAWRLAB games offers Switch porting of Godot games.

mazette! games offers Switch, Xbox One and Xbox Series X/S porting and publishing of Godot games.

Olde Sküül offers Switch, Xbox One, Playstation 4 & Playstation 5 porting and publishing of Godot games.

Tuanisapps offers Switch porting and publishing of Godot games.

Seaven Studio offers Switch, Xbox One, Xbox Series, PlayStation 4 & PlayStation 5 porting of Godot games.

Sickhead Games offers console porting to Nintendo Switch, PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X/S for Godot games.

If your company offers porting, or porting and publishing services for Godot games, feel free to contact the Godot Foundation to add your company to the list above.

Middleware ports are available through the console vendor's website. They provide you with a version of Godot that can natively run on the console. Typically, you do the actual work of adapting your game to the various consoles yourself. In other words, the middleware provided has ported Godot to the console, you just need to port your game, which is significantly less work in most cases.

W4 Games offers official middleware ports for Nintendo Switch, Xbox Series X/S, and Playstation 5.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Deploying to Android — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/deploying_to_android.html

**Contents:**
- Deploying to Android
- Setup
- Gradle Android build
- Installing the vendors plugin
- Creating the export presets
- Running on your device from the Godot editor
- User-contributed notes

Most standalone headsets run on Android and OpenXR support is making its way to these platforms.

Before following the OpenXR-specific instructions here, you'll need to first setup your system to export to Android in general, including:

Installing OpenJDK 17

Installing Android Studio

Configuring the location of the Android SDK in Godot

See Exporting for Android for the full details, and return here when you've finished these steps.

While the Mobile Vulkan renderer has many optimizations targeted at mobile devices, we're still working out the kinks. It is highly advisable to use the compatibility renderer (OpenGL) for the time being when targeting Android based XR devices.

Official support for the Android platform wasn't added to the OpenXR specification initially resulting in various vendors creating custom loaders to make OpenXR available on their headsets. While the long term expectation is that all vendors will adopt the official OpenXR loader, for now these loaders need to be added to your project.

In order to include the vendor-specific OpenXR loader into your project, you will need to setup a gradle Android build.

Select Install Android Build Template... from the Project menu:

This will create a folder called android inside of your project that contains all the runtime files needed on Android. You can now customize this installation. Godot won't show this in the editor but you can find it with a file browser.

You can read more about gradle builds here: Gradle builds for Android.

The vendors plugin can be downloaded from the asset library, search for "OpenXR vendors" and install the one named "Godot OpenXR Vendors plugin v4".

You will find the installed files inside the addons folder. Alternatively you can manually install the vendors plugin by downloading it from the release page here. You will need to copy the assets/addons/godotopenxrvendors folder from the zip file into your projects addons folder.

You can find the main repository of the vendors plugin here.

You will need to setup a separate export preset for each device, as each device will need its own loader included.

Open Project and select Export... Click on Add.. and select Android. Next change the name of the export preset for the device you're setting this up for, say Meta Quest. And enable Use Gradle Build. If you want to use one-click deploy (described below), ensure that Runnable is enabled.

If the vendors plugins were installed correctly you should find entries for the different headsets under XR Features. Change the XR Mode to OpenXR, then select the entry for your headset if you see one. If you don't see one enable the Khronos plugin.

Scroll to the bottom of the list and you'll find additional XR feature sections, currently only Meta XR Features, Pico XR Features, Magicleap XR Features and Khronos XR Features for HTC are available. You will need to select the appropriate settings if you wish to use these features.

If you've setup your export settings as described above, and your headset is connected to your computer and correctly recognized, you can launch it directly from the Godot editor using One-click deploy:

For some devices on some platforms, you may need to perform some extra steps in order for your device to be recognized correctly, so be sure to check the developer documentation from your headset vendor.

For example, with the Meta Quest 2, you need to enable developer mode on the headset, and if you're on Windows, you'll need to install special ADB drivers. See the official Meta Quest developer documentation for more details.

If you're having any issues with one-click deploy, check the Troubleshooting section.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
