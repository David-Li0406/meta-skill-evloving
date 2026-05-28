# Godot_Docs - Other

**Pages:** 25

---

## Godot Docs – 4.5 branch — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/

**Contents:**
- Godot Docs – 4.5 branch
- Get involved
- Offline documentation

Godot's documentation is available in various languages and versions. Expand the "Read the Docs" panel at the bottom of the sidebar to see the list.

Welcome to the official documentation of Godot Engine, the free and open source community-driven 2D and 3D game engine! If you are new to this documentation, we recommend that you read the introduction page to get an overview of what this documentation has to offer.

The table of contents in the sidebar should let you easily access the documentation for your topic of interest. You can also use the search function in the top-left corner.

Godot Engine is an open source project developed by a community of volunteers. The documentation team can always use your feedback and help to improve the tutorials and class reference. If you don't understand something, or cannot find what you are looking for in the docs, help us make the documentation better by letting us know!

Submit an issue or pull request on the GitHub repository, help us translate the documentation into your language, or talk to us on the #documentation channel on the Godot Contributors Chat!

To browse the documentation offline, you can download an HTML copy (updated every Monday): stable, latest, 3.6. Extract the ZIP archive then open the top-level index.html in a web browser.

For mobile devices or e-readers, you can also download an ePub copy (updated every Monday): stable, latest, 3.6. Extract the ZIP archive then open the GodotEngine.epub file in an e-book reader application.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## List of features — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/list_of_features.html

**Contents:**
- List of features
- Platforms
- Editor
- Rendering
- 2D graphics
- 2D tools
- 2D physics
- 3D graphics
- 3D tools
- 3D physics

This page aims to list all features currently supported by Godot.

This page lists features supported by the current stable version of Godot. Some of these features are not available in the 3.x release series.

See System requirements for hardware and software version requirements.

Can run both the editor and exported projects:

Windows (x86 and ARM, 64-bit and 32-bit).

macOS (x86 and ARM, 64-bit only).

Linux (x86 and ARM, 64-bit and 32-bit).

Binaries are statically linked and can run on any distribution if compiled on an old enough base distribution.

Official binaries are compiled using the Godot Engine buildroot, allowing for binaries that work across common Linux distributions.

Android (editor support is experimental).

Web browsers. Experimental in 4.0, using Godot 3.x is recommended instead when targeting HTML5.

Linux supports rv64 (RISC-V), ppc64 & ppc32 (PowerPC), and loongarch64. However you must compile the editor for that platform (as well as export templates) yourself, no official downloads are currently provided. RISC-V compiling instructions can be found on the Compiling for Linux, *BSD page.

Runs exported projects:

Godot aims to be as platform-independent as possible and can be ported to new platforms with relative ease.

Projects written in C# using Godot 4 currently cannot be exported to the web platform. To use C# on that platform, consider Godot 3 instead. Android and iOS platform support is available as of Godot 4.2, but is experimental and some limitations apply.

Built-in script editor.

Support for external script editors such as Visual Studio Code or Vim.

Support for debugging in threads is available since 4.2.

Visual profiler with CPU and GPU time indications for each step of the rendering pipeline.

Performance monitoring tools, including custom performance monitors.

Live script reloading.

Changes will reflect in the editor and will be kept after closing the running project.

Changes won't reflect in the editor and won't be kept after closing the running project.

Live camera replication.

Move the in-editor camera and see the result in the running project.

Built-in offline class reference documentation.

Use the editor in dozens of languages contributed by the community.

Editor plugins can be downloaded from the asset library to extend editor functionality.

Create your own plugins using GDScript to add new features or speed up your workflow.

Download projects from the asset library in the Project Manager and import them directly.

Godot 4 includes three renderers:

Forward+. The most advanced renderer, suited for desktop platforms only. Used by default on desktop platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Mobile. Fewer features, but renders simple scenes faster. Suited for mobile and desktop platforms. Used by default on mobile platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Compatibility, sometimes called GL Compatibility. The least advanced renderer, suited for low-end desktop and mobile platforms. Used by default on the web platform. This renderer uses OpenGL as the rendering driver.

See Overview of renderers for a detailed comparison of the rendering methods.

Sprite, polygon and line rendering.

High-level tools to draw lines and polygons such as Polygon2D and Line2D, with support for texturing.

AnimatedSprite2D as a helper for creating animated sprites.

Pseudo-3D support including preview in the editor.

2D lighting with normal maps and specular maps.

Point (omni/spot) and directional 2D lights.

Hard or soft shadows (adjustable on a per-light basis).

Custom shaders can access a real-time SDF representation of the 2D scene based on LightOccluder2D nodes, which can be used for improved 2D lighting effects including 2D global illumination.

Font rendering using bitmaps, rasterization using FreeType or multi-channel signed distance fields (MSDF).

Bitmap fonts can be exported using tools like BMFont, or imported from images (for fixed-width fonts only).

Dynamic fonts support monochrome fonts as well as colored fonts (e.g. for emoji). Supported formats are TTF, OTF, WOFF1 and WOFF2.

Dynamic fonts support optional font outlines with adjustable width and color.

Dynamic fonts support variable fonts and OpenType features including ligatures.

Dynamic fonts support simulated bold and italic when the font file lacks those styles.

Dynamic fonts support oversampling to keep fonts sharp at higher resolutions.

Dynamic fonts support subpixel positioning to make fonts crisper at low sizes.

Dynamic fonts support LCD subpixel optimizations to make fonts even crisper at low sizes.

Signed distance field fonts can be scaled at any resolution without requiring re-rasterization. Multi-channel usage makes SDF fonts scale down to lower sizes better compared to monochrome SDF fonts.

GPU-based particles with support for custom particle shaders.

Optional 2D HDR rendering for better glow capabilities.

TileMaps for 2D tile-based level design.

2D camera with built-in smoothing and drag margins.

Path2D node to represent a path in 2D space.

Can be drawn in the editor or generated procedurally.

PathFollow2D node to make nodes follow a Path2D.

2D geometry helper class.

Animatable bodies (for objects moving only by script or animation, such as doors and platforms).

Areas to detect bodies entering or leaving it.

Built-in shapes: line, box, circle, capsule, world boundary (infinite plane).

Collision polygons (can be drawn manually or generated from a sprite in the editor).

HDR rendering with sRGB.

Perspective, orthographic and frustum-offset cameras.

When using the Forward+ renderer, a depth prepass is used to improve performance in complex scenes by reducing the cost of overdraw.

Variable rate shading on supported GPUs in Forward+ and Mobile.

Physically-based rendering (built-in material features):

Follows the Disney PBR model.

Supports Burley, Lambert, Lambert Wrap (half-Lambert) and Toon diffuse shading modes.

Supports Schlick-GGX, Toon and Disabled specular shading modes.

Uses a roughness-metallic workflow with support for ORM textures.

Uses horizon specular occlusion (Filament model) to improve material appearance.

Parallax/relief mapping with automatic level of detail based on distance.

Detail mapping for the albedo and normal maps.

Sub-surface scattering and transmittance.

Screen-space refraction with support for material roughness (resulting in blurry refraction).

Proximity fade (soft particles) and distance fade.

Distance fade can use alpha blending or dithering to avoid going through the transparent pipeline.

Dithering can be determined on a per-pixel or per-object basis.

Directional lights (sun/moon). Up to 4 per scene.

Omnidirectional lights.

Spot lights with adjustable cone angle and attenuation.

Specular, indirect light, and volumetric fog energy can be adjusted on a per-light basis.

Adjustable light "size" for fake area lights (will also make shadows blurrier).

Optional distance fade system to fade distant lights and their shadows, improving performance.

When using the Forward+ renderer (default on desktop), lights are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of lights that can be used on a mesh.

When using the Mobile renderer, up to 8 omni lights and 8 spot lights can be displayed per mesh resource. Baked lighting can be used to overcome this limit if needed.

DirectionalLight: Orthogonal (fastest), PSSM 2-split and 4-split. Supports blending between splits.

OmniLight: Dual paraboloid (fast) or cubemap (slower but more accurate). Supports colored projector textures in the form of panoramas.

SpotLight: Single texture. Supports colored projector textures.

Shadow normal offset bias and shadow pancaking to decrease the amount of visible shadow acne and peter-panning.

PCSS-like shadow blur based on the light size and distance from the surface the shadow is cast on.

Adjustable shadow blur on a per-light basis.

Global illumination with indirect lighting:

Baked lightmaps (fast, but can't be updated at runtime).

Supports baking indirect light only or baking both direct and indirect lighting. The bake mode can be adjusted on a per-light basis to allow for hybrid light baking setups.

Supports lighting dynamic objects using automatic and manually placed probes.

Optionally supports directional lighting and rough reflections based on spherical harmonics.

Lightmaps are baked on the GPU using compute shaders (much faster compared to CPU lightmapping). Baking can only be performed from the editor, not in exported projects.

Supports GPU-based denoising with JNLM, or CPU/GPU-based denoising with OIDN.

Voxel-based GI probes. Supports dynamic lights and dynamic occluders, while also supporting reflections. Requires a fast baking step which can be performed in the editor or at runtime (including from an exported project).

Signed-distance field GI designed for large open worlds. Supports dynamic lights, but not dynamic occluders. Supports reflections. No baking required.

Screen-space indirect lighting (SSIL) at half or full resolution. Fully real-time and supports any kind of emissive light source (including decals).

VoxelGI and SDFGI use a deferred pass to allow for rendering GI at half resolution to improve performance (while still having functional MSAA support).

Voxel-based reflections (when using GI probes) and SDF-based reflections (when using signed distance field GI). Voxel-based reflections are visible on transparent surfaces, while rough SDF-based reflections are visible on transparent surfaces.

Fast baked reflections or slow real-time reflections using ReflectionProbe. Parallax box correction can optionally be enabled.

Screen-space reflections with support for material roughness.

Reflection techniques can be mixed together for greater accuracy or scalability.

When using the Forward+ renderer (default on desktop), reflection probes are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of reflection probes that can be used on a mesh.

When using the Mobile renderer, up to 8 reflection probes can be displayed per mesh resource. When using the Compatibility renderer, up to 2 reflection probes can be displayed per mesh resource.

Supports albedo, emissive, ORM, and normal mapping.

Texture channels are smoothly overlaid on top of the underlying material, with support for normal/ORM-only decals.

Support for normal fade to fade the decal depending on its incidence angle.

Does not rely on runtime mesh generation. This means decals can be used on complex skinned meshes with no performance penalty, even if the decal moves every frame.

Support for nearest, bilinear, trilinear or anisotropic texture filtering (configured globally).

Optional distance fade system to fade distant decals, improving performance.

When using the Forward+ renderer (default on desktop), decals are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of decals that can be used on a mesh.

When using the Mobile renderer, up to 8 decals can be displayed per mesh resource.

Panorama sky (using an HDRI).

Procedural sky and Physically-based sky that respond to the DirectionalLights in the scene.

Support for custom sky shaders, which can be animated.

The radiance map used for ambient and specular light can be updated in real-time depending on the quality settings chosen.

Exponential depth fog.

Exponential height fog.

Support for automatic fog color depending on the sky color (aerial perspective).

Support for sun scattering in the fog.

Support for controlling how much fog rendering should affect the sky, with separate controls for traditional and volumetric fog.

Support for making specific materials ignore fog.

Global volumetric fog that reacts to lights and shadows.

Volumetric fog can take indirect light into account when using VoxelGI or SDFGI.

Fog volume nodes that can be placed to add fog to specific areas (or remove fog from specific areas). Supported shapes include box, ellipse, cone, cylinder, and 3D texture-based density maps.

Each fog volume can have its own custom shader.

Can be used together with traditional fog.

GPU-based particles with support for subemitters (2D + 3D), trails (2D + 3D), attractors (3D only) and collision (2D + 3D).

3D particle attractor shapes supported: box, sphere and 3D vector fields.

3D particle collision shapes supported: box, sphere, baked signed distance field and real-time heightmap (suited for open world weather effects).

2D particle collision is handled using a signed distance field generated in real-time based on LightOccluder2D nodes in the scene.

Trails can use the built-in ribbon trail and tube trail meshes, or custom meshes with skeletons.

Support for custom particle shaders with manual emission.

Tonemapping (Linear, Reinhard, Filmic, ACES, AgX).

Automatic exposure adjustments based on viewport brightness (and manual exposure override).

Near and far depth of field with adjustable bokeh simulation (box, hexagon, circle).

Screen-space ambient occlusion (SSAO) at half or full resolution.

Glow/bloom with optional bicubic upscaling and several blend modes available: Screen, Soft Light, Add, Replace, Mix.

Glow can have a colored dirt map texture, acting as a lens dirt effect.

Glow can be used as a screen-space blur effect.

Color correction using a one-dimensional ramp or a 3D LUT texture.

Roughness limiter to reduce the impact of specular aliasing.

Brightness, contrast and saturation adjustments.

Nearest, bilinear, trilinear or anisotropic filtering.

Filtering options are defined on a per-use basis, not a per-texture basis.

Basis Universal (slow, but results in smaller files).

BPTC for high-quality compression (not supported on macOS).

ETC2 (not supported on macOS).

S3TC (not supported on mobile/Web platforms).

Temporal antialiasing (TAA).

AMD FidelityFX Super Resolution 2.2 antialiasing (FSR2), which can be used at native resolution as a form of high-quality temporal antialiasing.

Multi-sample antialiasing (MSAA), for both 2D antialiasing and 3D antialiasing.

Fast approximate antialiasing (FXAA).

Super-sample antialiasing (SSAA) using bilinear 3D scaling and a 3D resolution scale above 1.0.

Alpha antialiasing, MSAA alpha to coverage and alpha hashing on a per-material basis.

Support for rendering 3D at a lower resolution while keeping 2D rendering at the original scale. This can be used to improve performance on low-end systems or improve visuals on high-end systems.

Resolution scaling uses bilinear filtering, AMD FidelityFX Super Resolution 1.0 (FSR1) or AMD FidelityFX Super Resolution 2.2 (FSR2).

Texture mipmap LOD bias is adjusted automatically to improve quality at lower resolution scales. It can also be modified with a manual offset.

Most effects listed above can be adjusted for better performance or to further improve quality. This can be helpful when using Godot for offline rendering.

Built-in meshes: cube, cylinder/cone, (hemi)sphere, prism, plane, quad, torus, ribbon, tube.

GridMaps for 3D tile-based level design.

Constructive solid geometry (intended for prototyping).

Tools for procedural geometry generation.

Path3D node to represent a path in 3D space.

Can be drawn in the editor or generated procedurally.

PathFollow3D node to make nodes follow a Path3D.

3D geometry helper class.

Support for exporting the current scene as a glTF 2.0 file, both from the editor and at runtime from an exported project.

Animatable bodies (for objects moving only by script or animation, such as doors and platforms).

Vehicle bodies (intended for arcade physics, not simulation).

Areas to detect bodies entering or leaving it.

Built-in shapes: cuboid, sphere, capsule, cylinder, world boundary (infinite plane).

Generate triangle collision shapes for any mesh from the editor.

Generate one or several convex collision shapes for any mesh from the editor.

2D: Custom vertex, fragment, and light shaders.

3D: Custom vertex, fragment, light, and sky shaders.

Text-based shaders using a shader language inspired by GLSL.

Visual shader editor.

Support for visual shader plugins.

Object-oriented design pattern with scripts extending nodes.

Signals and groups for communicating between scripts.

Support for cross-language scripting.

Many 2D, 3D and 4D linear algebra data types such as vectors and transforms.

High-level interpreted language with optional static typing.

Syntax inspired by Python. However, GDScript is not based on Python.

Syntax highlighting is provided on GitHub.

Use threads to perform asynchronous actions or make use of multiple processor cores.

Packaged in a separate binary to keep file sizes and dependencies down.

Supports .NET 8 and higher.

Full support for the C# 12.0 syntax and features.

Supports Windows, Linux, and macOS. Since Godot 4.2, experimental support for Android and iOS is also available.

On the iOS platform only some architectures are supported: arm64.

The web platform is currently unsupported. To use C# on that platform, consider Godot 3 instead.

Using an external editor is recommended to benefit from IDE functionality.

GDExtension (C, C++, Rust, D, ...):

When you need it, link to native libraries for higher performance and third-party integrations.

For scripting game logic, GDScript or C# are recommended if their performance is suitable.

Official GDExtension bindings for C and C++.

Use any build system and language features you wish.

Actively developed GDExtension bindings for D, Swift, and Rust bindings provided by the community. (Some of these bindings may be experimental and not production-ready).

Mono, stereo, 5.1 and 7.1 output.

Non-positional and positional playback in 2D and 3D.

Optional Doppler effect in 2D and 3D.

Support for re-routable audio buses and effects with dozens of effects included.

Support for polyphony (playing several sounds from a single AudioStreamPlayer node).

Support for random volume and pitch.

Support for real-time pitch scaling.

Support for sequential/random sample selection, including repetition prevention when using random sample selection.

Listener2D and Listener3D nodes to listen from a position different than the camera.

Support for procedural audio generation.

Audio input to record microphones.

No support for MIDI output yet.

Linux: PulseAudio or ALSA.

Support for custom import plugins.

Images: See Importing images.

WAV with optional IMA-ADPCM compression.

3D scenes: See Importing 3D scenes.

glTF 2.0 (recommended).

.blend (by calling Blender's glTF export functionality transparently).

FBX (by calling FBX2glTF transparently).

Wavefront OBJ (static scenes only, can be loaded directly as a mesh or imported as a 3D scene).

Support for loading glTF 2.0 scenes at runtime, including from an exported project.

3D meshes use Mikktspace to generate tangents on import, which ensures consistency with other 3D applications such as Blender.

Input mapping system using hardcoded input events or remappable input actions.

Axis values can be mapped to two different actions with a configurable deadzone.

Use the same code to support both keyboards and gamepads.

Keys can be mapped in "physical" mode to be independent of the keyboard layout.

The mouse cursor can be visible, hidden, captured or confined within the window.

When captured, raw input will be used on Windows and Linux to sidestep the OS' mouse acceleration settings.

Gamepad input (up to 8 simultaneous controllers).

Pen/tablet input with pressure support.

A* algorithm in 2D and 3D.

Navigation meshes with dynamic obstacle avoidance in 2D and 3D.

Generate navigation meshes from the editor or at runtime (including from an exported project).

Low-level TCP networking using StreamPeer and TCPServer.

Low-level UDP networking using PacketPeer and UDPServer.

Low-level HTTP requests using HTTPClient.

High-level HTTP requests using HTTPRequest.

Supports HTTPS out of the box using bundled certificates.

High-level multiplayer API using UDP and ENet.

Automatic replication using remote procedure calls (RPCs).

Supports unreliable, reliable and ordered transfers.

WebSocket client and server, available on all platforms.

WebRTC client and server, available on all platforms.

Support for UPnP to sidestep the requirement to forward ports when hosting a server behind a NAT.

Full support for Unicode including emoji.

Store localization strings using CSV or gettext.

Support for generating gettext POT and PO files from the editor.

Use localized strings in your project automatically in GUI elements or by using the tr() function.

Support for pluralization and translation contexts when using gettext translations.

Support for bidirectional typesetting, text shaping and OpenType localized forms.

Automatic UI mirroring for right-to-left locales.

Support for pseudolocalization to test your project for i18n-friendliness.

Spawn multiple independent windows within a single process.

Move, resize, minimize, and maximize windows spawned by the project.

Change the window title and icon.

Request attention (will cause the title bar to blink on most platforms).

Uses borderless fullscreen by default on Windows for fast alt-tabbing, but can optionally use exclusive fullscreen to reduce input lag.

Borderless windows (fullscreen or non-fullscreen).

Ability to keep a window always on top.

Global menu integration on macOS.

Execute commands in a blocking or non-blocking manner (including running multiple instances of the same project).

Open file paths and URLs using default or custom protocol handlers (if registered on the system).

Parse custom command line arguments.

Any Godot binary (editor or exported project) can be used as a headless server by starting it with the --headless command line argument. This allows running the engine without a GPU or display server.

In-app purchases on Android and iOS.

Support for advertisements using third-party modules.

Out of the box support for OpenXR.

Including support for popular desktop headsets like the Valve Index, WMR headsets, and Quest over Link.

Support for Android-based headsets using OpenXR through a plugin.

Including support for popular stand alone headsets like the Meta Quest 1/2/3 and Pro, Pico 4, Magic Leap 2, and Lynx R1.

Out of the box limited support for visionOS Apple headsets.

Currently only exporting an application for use on a flat plane within the headset is supported. Immersive experiences are not supported.

Other devices supported through an XR plugin structure.

Various advanced toolkits are available that implement common features required by XR applications.

Godot's GUI is built using the same Control nodes used to make games in Godot. The editor UI can easily be extended in many ways using add-ons.

Checkboxes, check buttons, radio buttons.

Text entry using LineEdit (single line) and TextEdit (multiple lines). TextEdit also supports code editing features such as displaying line numbers and syntax highlighting.

Dropdown menus using PopupMenu and OptionButton.

RichTextLabel for text formatted using BBCode, with support for animated custom effects.

Trees (can also be used to represent tables).

Color picker with RGB and HSV modes.

Controls can be rotated and scaled.

Anchors to keep GUI elements in a specific corner, edge or centered.

Containers to place GUI elements automatically following certain rules.

Flow layouts (similar to autowrapping text).

Margin, centered and aspect ratio layouts.

Draggable splitter layouts.

Scale to multiple resolutions using the canvas_items or viewport stretch modes.

Support any aspect ratio using anchors and the expand stretch aspect.

Built-in theme editor.

Generate a theme based on the current editor theme settings.

Procedural vector-based theming using StyleBoxFlat.

Supports rounded/beveled corners, drop shadows, per-border widths and antialiasing.

Texture-based theming using StyleBoxTexture.

Godot's small distribution size can make it a suitable alternative to frameworks like Electron or Qt.

Direct kinematics and inverse kinematics.

Support for animating any property with customizable interpolation.

Support for calling methods in animation tracks.

Support for playing sounds in animation tracks.

Support for Bézier curves in animation.

Scenes and resources can be saved in text-based or binary formats.

Text-based formats are human-readable and more friendly to version control.

Binary formats are faster to save/load for large scenes/resources.

Read and write text or binary files using FileAccess.

Can optionally be compressed or encrypted.

Read and write JSON files.

Read and write INI-style configuration files using ConfigFile.

Can (de)serialize any Godot datatype, including Vector2/3, Color, ...

Read XML files using XMLParser.

Load and save images, audio/video, fonts and ZIP archives in an exported project without having to go through Godot's import system.

Pack game data into a PCK file (custom format optimized for fast seeking), into a ZIP archive, or directly into the executable for single-file distribution.

Export additional PCK files that can be read by the engine to support mods and DLCs.

Video playback with built-in support for Ogg Theora.

Movie Maker mode to record videos from a running project with synchronized audio and perfect frame pacing.

Low-level access to servers which allows bypassing the scene tree's overhead when needed.

Command line interface for automation.

Export and deploy projects using continuous integration platforms.

Shell completion scripts are available for Bash, zsh and fish.

Print colored text to standard output on all platforms using print_rich.

The editor can detect features used in a project and create a compilation profile, which can be used to create smaller export template binaries with unneeded features disabled.

Support for C++ modules statically linked into the engine binary.

Most built-in modules can be disabled at compile-time to reduce binary size in custom builds. See Optimizing a build for size for details.

Engine and editor written in C++17.

Can be compiled using GCC, Clang and MSVC. MinGW is also supported.

Friendly towards packagers. In most cases, system libraries can be used instead of the ones provided by Godot. The build system doesn't download anything. Builds can be fully reproducible.

Licensed under the permissive MIT license.

Open development process with contributions welcome.

The Godot proposals repository lists features that have been requested by the community and may be implemented in future Godot releases.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## System requirements — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/system_requirements.html

**Contents:**
- System requirements
- Godot editor
  - Desktop or laptop PC - Minimum
  - Mobile device (smartphone/tablet) - Minimum
  - Desktop or laptop PC - Recommended
  - Mobile device (smartphone/tablet) - Recommended
- Exported Godot project
  - Desktop or laptop PC - Minimum
  - Mobile device (smartphone/tablet) - Minimum
  - Desktop or laptop PC - Recommended

This page contains system requirements for the editor and exported projects. These specifications are given for informative purposes only, but they can be referred to if you're looking to build or upgrade a system to use Godot on.

These are the minimum specifications required to run the Godot editor and work on a simple 2D or 3D project:

Windows: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core 2 Duo SU9400, Apple M1

Linux: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4

Forward+ renderer: Integrated graphics with full Vulkan 1.0 support

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Mobile renderer: Integrated graphics with full Vulkan 1.0 support

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Compatibility renderer: Integrated graphics with full OpenGL 3.3 support

Example: Intel HD Graphics 2500 (Ivy Bridge), AMD Radeon R5 Graphics (Kaveri)

200 MB (used for the executable, project files and cache). Exporting projects requires downloading export templates separately (1.3 GB after installation).

Native editor: Windows 10, macOS 10.13 (Compatibility) or macOS 10.15 (Forward+/Mobile), Linux distribution released after 2018

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

If your x86_64 CPU does not support SSE4.2, you can still run the 32-bit Godot executable which only has a SSE2 requirement (all x86_64 CPUs support SSE2).

While supported on Linux, we have no official minimum requirements for running on rv64 (RISC-V), ppc64 & ppc32 (PowerPC), and loongarch64. In addition you must compile the editor for that platform (as well as export templates) yourself, no official downloads are currently provided. RISC-V compiling instructions can be found on the Compiling for Linux, *BSD page.

Android: SoC with any 32-bit or 64-bit ARM or x86 CPU

Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430

iOS: Cannot run the editor

Forward+ renderer: SoC featuring GPU with full Vulkan 1.0 support

Example: Qualcomm Adreno 505, Mali-G71 MP2

Mobile renderer: SoC featuring GPU with full Vulkan 1.0 support

Example: Qualcomm Adreno 505, Mali-G71 MP2

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.0 support

Example: Qualcomm Adreno 306, Mali-T628 MP6

200 MB (used for the executable, project files and cache) Exporting projects requires downloading export templates separately (1.3 GB after installation)

Native editor: Android 6.0 (Compatibility) or Android 9.0 (Forward+/Mobile)

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

These are the recommended specifications to get a smooth experience with the Godot editor on a simple 2D or 3D project:

Windows: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core i5-8500, Apple M1

Linux: x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking

Forward+ renderer: Dedicated graphics with full Vulkan 1.2 support

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Mobile renderer: Dedicated graphics with full Vulkan 1.2 support

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Compatibility renderer: Dedicated graphics with full OpenGL 4.6 support

Example: NVIDIA GeForce GTX 650 (Kepler), AMD Radeon HD 7750 (GCN 1.0)

1.5 GB (used for the executable, project files, all export templates and cache)

Native editor: Windows 10, macOS 10.15, Linux distribution released after 2020

Web editor: Latest version of Firefox, Chrome, Edge, Safari, Opera

Android: SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more

Example: Qualcomm Snapdragon 845, Samsung Exynos 9810

iOS: Cannot run the editor

Forward+ renderer: SoC featuring GPU with full Vulkan 1.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

Mobile renderer: SoC featuring GPU with full Vulkan 1.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

1.5 GB (used for the executable, project files, all export templates and cache)

Native editor: Android 9.0

Web editor: Latest version of Firefox, Chrome, Edge, Safari, Opera, Samsung Internet

The requirements below are a baseline for a simple 2D or 3D project, with basic scripting and few visual flourishes. CPU, GPU, RAM and storage requirements will heavily vary depending on your project's scope, its renderer, viewport resolution and graphics settings chosen. Other programs running on the system while the project is running will also compete for resources, including RAM and video RAM.

It is strongly recommended to do your own testing on low-end hardware to make sure your project runs at the desired speed. To provide scalability for low-end hardware, you will also need to introduce a graphics options menu to your project.

These are the minimum specifications required to run a simple 2D or 3D project exported with Godot:

Windows: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core 2 Duo SU9400, Apple M1

Linux: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4

Forward+ renderer: Integrated graphics with full Vulkan 1.0 support, Metal 3 support (macOS) or Direct3D 12 (12_0 feature level) support (Windows)

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Mobile renderer: Integrated graphics with full Vulkan 1.0 support, Metal 3 support (macOS) or Direct3D 12 (12_0 feature level) support (Windows)

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Compatibility renderer: Integrated graphics with full OpenGL 3.3 support or Direct3D 11 support (Windows).

Example: Intel HD Graphics 2500 (Ivy Bridge), AMD Radeon R5 Graphics (Kaveri)

For native exports: 2 GB

For web exports: 4 GB

150 MB (used for the executable, project files and cache)

For native exports: Windows 10, macOS 10.13 (Compatibility), macOS 10.15 (Forward+/Mobile, Vulkan), macOS 13.0 (Forward+/Mobile, Metal), Linux distribution released after 2018

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

Android: SoC with any 32-bit or 64-bit ARM or x86 CPU

Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430

iOS: SoC with any 64-bit ARM CPU

Example: Apple A7 (iPhone 5S)

Forward+ renderer: SoC featuring GPU with full Vulkan 1.0 support, or Metal 3 support (iOS/iPadOS)

Example (Vulkan): Qualcomm Adreno 505, Mali-G71 MP2, Apple A12 (iPhone XR/XS)

Example (Metal): Apple A11 (iPhone 8/X)

Mobile renderer: SoC featuring GPU with full Vulkan 1.0 support, or Metal 3 support (iOS/iPadOS)

Example (Vulkan): Qualcomm Adreno 505, Mali-G71 MP2, Apple A12 (iPhone XR/XS)

Example (Metal): Apple A11 (iPhone 8/X)

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.0 support

Example: Qualcomm Adreno 306, Mali-T628 MP6, Apple A7 (iPhone 5S)

For native exports: 1 GB

For web exports: 2 GB

150 MB (used for the executable, project files and cache)

For native exports: Android 6.0 (Compatibility), Android 9.0 (Forward+/Mobile), iOS 12.0 (Forward+/Mobile, Vulkan), iOS 16.0 (Forward+/Mobile, Metal)

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

These are the recommended specifications to get a smooth experience with a simple 2D or 3D project exported with Godot:

Windows: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core i5-8500, Apple M1

Linux: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv7 or ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking

Forward+ renderer: Dedicated graphics with full Vulkan 1.2 support, Metal 3 support (macOS), or Direct3D 12 (12_0 feature level) support (Windows)

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Mobile renderer: Dedicated graphics with full Vulkan 1.2 support, Metal 3 support (macOS), or Direct3D 12 (12_0 feature level) support (Windows)

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Compatibility renderer: Dedicated graphics with full OpenGL 4.6 support

Example: NVIDIA GeForce GTX 650 (Kepler), AMD Radeon HD 7750 (GCN 1.0)

For native exports: 4 GB

For web exports: 8 GB

150 MB (used for the executable, project files and cache)

For native exports: Windows 10, macOS 10.15 (Forward+/Mobile, Vulkan), macOS 13.0 (Forward+/Mobile, Metal), Linux distribution released after 2020

For web exports: Latest version of Firefox, Chrome, Edge, Safari, Opera

Android: SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more

Example: Qualcomm Snapdragon 845, Samsung Exynos 9810

iOS: SoC with 64-bit ARM CPU

Example: Apple A14 (iPhone 12)

Forward+ renderer: SoC featuring GPU with full Vulkan 1.2 support, or Metal 3 support (iOS/iPadOS)

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

Mobile renderer: SoC featuring GPU with full Vulkan 1.2 support, or Metal 3 support (iOS/iPadOS)

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

For native exports: 2 GB

For web exports: 4 GB

150 MB (used for the executable, project files and cache)

For native exports: Android 9.0, iOS 14.1 (Forward+/Mobile, Vulkan), iOS 16.0 (Forward+/Mobile, Metal)

For web exports: Latest version of Firefox, Chrome, Edge, Safari, Opera, Samsung Internet

Godot doesn't use OpenGL/OpenGL ES extensions introduced after OpenGL 3.3/OpenGL ES 3.0, but GPUs supporting newer OpenGL/OpenGL ES versions generally have fewer driver issues.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Frequently asked questions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/faq.html

**Contents:**
- Frequently asked questions
- What can I do with Godot? How much does it cost? What are the license terms?
- Which platforms are supported by Godot?
- Which programming languages are supported in Godot?
- What is GDScript and why should I use it?
- What were the motivations behind creating GDScript?
- Which programming language is fastest?
- What 3D model formats does Godot support?
- Will [insert closed SDK such as FMOD, GameWorks, etc.] be supported in Godot?
- How can I extend Godot?

Godot is Free and open source Software available under the OSI-approved MIT license. This means it is free as in "free speech" as well as in "free beer."

You are free to download and use Godot for any purpose: personal, non-profit, commercial, or otherwise.

You are free to modify, distribute, redistribute, and remix Godot to your heart's content, for any reason, both non-commercially and commercially.

All the contents of this accompanying documentation are published under the permissive Creative Commons Attribution 3.0 (CC BY 3.0) license, with attribution to "Juan Linietsky, Ariel Manzur and the Godot Engine community."

Logos and icons are generally under the same Creative Commons license. Note that some third-party libraries included with Godot's source code may have different licenses.

For full details, look at the COPYRIGHT.txt as well as the LICENSE.txt and LOGO_LICENSE.txt files in the Godot repository.

Also, see the license page on the Godot website.

Android (experimental)

For exporting your games:

Both 32- and 64-bit binaries are supported where it makes sense, with 64 being the default. Official macOS builds support Apple Silicon natively as well as x86_64.

Some users also report building and using Godot successfully on ARM-based systems with Linux, like the Raspberry Pi.

The Godot team can't provide an open source console export due to the licensing terms imposed by console manufacturers. Regardless of the engine you use, though, releasing games on consoles is always a lot of work. You can read more about Console support in Godot.

For more on this, see the sections on exporting and compiling Godot yourself.

Godot 3 also had support for Universal Windows Platform (UWP). This platform port was removed in Godot 4 due to lack of maintenance, and it being deprecated by Microsoft. It is still available in the current stable release of Godot 3 for interested users.

The officially supported languages for Godot are GDScript, C#, and C++. See the subcategories for each language in the scripting section.

If you are just starting out with either Godot or game development in general, GDScript is the recommended language to learn and use since it is native to Godot. While scripting languages tend to be less performant than lower-level languages in the long run, for prototyping, developing Minimum Viable Products (MVPs), and focusing on Time-To-Market (TTM), GDScript will provide a fast, friendly, and capable way of developing your games.

Note that C# support is still relatively new, and as such, you may encounter some issues along the way. C# support is also currently missing on the web platform. Our friendly and hard-working development community is always ready to tackle new problems as they arise, but since this is an open source project, we recommend that you first do some due diligence yourself. Searching through discussions on open issues is a great way to start your troubleshooting.

As for new languages, support is possible via third parties with GDExtensions. (See the question about plugins below). Work is currently underway, for example, on unofficial bindings for Godot to Python and Nim.

GDScript is Godot's integrated scripting language. It was built from the ground up to maximize Godot's potential in the least amount of code, affording both novice and expert developers alike to capitalize on Godot's strengths as fast as possible. If you've ever written anything in a language like Python before, then you'll feel right at home. For examples and a complete overview of the power GDScript offers you, check out the GDScript scripting guide.

There are several reasons to use GDScript, but the most salient reason is the overall reduction of complexity.

The original intent of creating a tightly integrated, custom scripting language for Godot was two-fold: first, it reduces the amount of time necessary to get up and running with Godot, giving developers a rapid way of exposing themselves to the engine with a focus on productivity; second, it reduces the overall burden of maintenance, attenuates the dimensionality of issues, and allows the developers of the engine to focus on squashing bugs and improving features related to the engine core, rather than spending a lot of time trying to get a small set of incremental features working across a large set of languages.

Since Godot is an open source project, it was imperative from the start to prioritize a more integrated and seamless experience over attracting additional users by supporting more familiar programming languages, especially when supporting those more familiar languages would result in a worse experience. We understand if you would rather use another language in Godot (see the list of supported options above). That being said, if you haven't given GDScript a try, try it for three days. Just like Godot, once you see how powerful it is and how rapid your development becomes, we think GDScript will grow on you.

More information about getting comfortable with GDScript or dynamically typed languages can be found in the GDScript: An introduction to dynamic languages tutorial.

In the early days, the engine used the Lua scripting language. Lua can be fast thanks to LuaJIT, but creating bindings to an object-oriented system (by using fallbacks) was complex and slow and took an enormous amount of code. After some experiments with Python, that also proved difficult to embed.

The main reasons for creating a custom scripting language for Godot were:

Poor threading support in most script VMs, and Godot uses threads (Lua, Python, Squirrel, JavaScript, ActionScript, etc.).

Poor class-extending support in most script VMs, and adapting to the way Godot works is highly inefficient (Lua, Python, JavaScript).

Many existing languages have horrible interfaces for binding to C++, resulting in a large amount of code, bugs, bottlenecks, and general inefficiency (Lua, Python, Squirrel, JavaScript, etc.). We wanted to focus on a great engine, not a great number of integrations.

No native vector types (Vector3, Transform3D, etc.), resulting in highly reduced performance when using custom types (Lua, Python, Squirrel, JavaScript, ActionScript, etc.).

Garbage collector results in stalls or unnecessarily large memory usage (Lua, Python, JavaScript, ActionScript, etc.).

Difficulty integrating with the code editor for providing code completion, live editing, etc. (all of them).

GDScript was designed to curtail the issues above, and more.

In most games, the scripting language itself is not the cause of performance problems. Instead, performance is slowed by inefficient algorithms (which are slow in all languages), by GPU performance, or by the common C++ engine code like physics or navigation. All languages supported by Godot are fast enough for general-purpose scripting. You should choose a language based on other factors, like ease-of-use, familiarity, platform support, or language features.

In general, the performance of C# and GDScript is within the same order of magnitude, and C++ is faster than both.

Comparing GDScript performance to C# is tricky, since C# can be faster in some specific cases. The C# language itself tends to be faster than GDScript, which means that C# can be faster in situations with few calls to Godot engine code. However, C# can be slower than GDScript when making many Godot API calls, due to the cost of marshalling. C#'s performance can also be brought down by garbage collection which occurs at random and unpredictable moments. This can result in stuttering issues in complex projects, and is not exclusive to Godot.

C++, using GDExtension, will almost always be faster than either C# or GDScript. However, C++ is less easy to use than C# or GDScript, and is slower to develop with.

You can also use multiple languages within a single project, with cross-language scripting, or by using GDExtension and scripting languages together. Be aware that doing so comes with its own complications.

You can find detailed information on supported formats, how to export them from your 3D modeling software, and how to import them for Godot in the Importing 3D scenes documentation.

The aim of Godot is to create a free and open source MIT-licensed engine that is modular and extendable. There are no plans for the core engine development community to support any third-party, closed-source/proprietary SDKs, as integrating with these would go against Godot's ethos.

That said, because Godot is open source and modular, nothing prevents you or anyone else interested in adding those libraries as a module and shipping your game with them, as either open- or closed-source.

To see how support for your SDK of choice could still be provided, look at the Plugins question below.

If you know of a third-party SDK that is not supported by Godot but that offers free and open source integration, consider starting the integration work yourself. Godot is not owned by one person; it belongs to the community, and it grows along with ambitious community contributors like you.

For extending Godot, like creating Godot Editor plugins or adding support for additional languages, take a look at EditorPlugins and tool scripts.

Also, see the official blog post on GDExtension, a way to develop native extensions for Godot:

Introducing GDNative's successor, GDExtension

You can also take a look at the GDScript implementation, the Godot modules, as well as the Jolt physics engine integration for Godot. This would be a good starting point to see how another third-party library integrates with Godot.

Since you don't need to actually install Godot on your system to run it, this means desktop integration is not performed automatically. There are two ways to overcome this. You can install Godot from Steam (all platforms), Scoop (Windows), Homebrew (macOS) or Flathub (Linux). This will automatically perform the required steps for desktop integration.

Alternatively, you can manually perform the steps that an installer would do for you:

Move the Godot executable to a stable location (i.e. outside of your Downloads folder), so you don't accidentally move it and break the shortcut in the future.

Right-click the Godot executable and choose Create Shortcut.

Move the created shortcut to %APPDATA%\Microsoft\Windows\Start Menu\Programs. This is the user-wide location for shortcuts that will appear in the Start menu. You can also pin Godot in the task bar by right-clicking the executable and choosing Pin to Task Bar.

Drag the extracted Godot application to /Applications/Godot.app, then drag it to the Dock if desired. Spotlight will be able to find Godot as long as it's in /Applications or ~/Applications.

Move the Godot binary to a stable location (i.e. outside of your Downloads folder), so you don't accidentally move it and break the shortcut in the future.

Rename and move the Godot binary to a location present in your PATH environment variable. This is typically /usr/local/bin/godot or /usr/bin/godot. Doing this requires administrator privileges, but this also allows you to run the Godot editor from a terminal by entering godot.

If you cannot move the Godot editor binary to a protected location, you can keep the binary somewhere in your home directory, and modify the Path= line in the .desktop file linked below to contain the full absolute path to the Godot binary.

Save this .desktop file to $HOME/.local/share/applications/. If you have administrator privileges, you can also save the .desktop file to /usr/local/share/applications to make the shortcut available for all users.

In its default configuration, Godot is semi-portable. Its executable can run from any location (including non-writable locations) and never requires administrator privileges.

However, configuration files will be written to the user-wide configuration or data directory. This is usually a good approach, but this means configuration files will not carry across machines if you copy the folder containing the Godot executable. See File paths in Godot projects for more information.

If true portable operation is desired (e.g. for use on a USB stick), follow the steps in Self-contained mode.

Godot aims for cross-platform compatibility and open standards first and foremost. OpenGL and Vulkan are the technologies that are both open and available on (nearly) all platforms. Thanks to this design decision, a project developed with Godot on Windows will run out of the box on Linux, macOS, and more.

While Vulkan and OpenGL remain our primary focus for their open standard and cross-platform benefits, Godot 4.3 introduced experimental support for Direct3D 12. This addition aims to enhance performance and compatibility on platforms where Direct3D 12 is prevalent, such as Windows and Xbox. However, Vulkan and OpenGL will continue as the default rendering drivers on all platforms, including Windows.

Godot intentionally does not include features that can be implemented by add-ons unless they are used very often. One example of something not used often is advanced artificial intelligence functionality.

There are several reasons for this:

Code maintenance and surface for bugs. Every time we accept new code in the Godot repository, existing contributors often take the responsibility of maintaining it. Some contributors don't always stick around after getting their code merged, which can make it difficult for us to maintain the code in question. This can lead to poorly maintained features with bugs that are never fixed. On top of that, the "API surface" that needs to be tested and checked for regressions keeps increasing over time.

Ease of contribution. By keeping the codebase small and tidy, it can remain fast and easy to compile from source. This makes it easier for new contributors to get started with Godot, without requiring them to purchase high-end hardware.

Keeping the binary size small for the editor. Not everyone has a fast Internet connection. Ensuring that everyone can download the Godot editor, extract it and run it in less than 5 minutes makes Godot more accessible to developers in all countries.

Keeping the binary size small for export templates. This directly impacts the size of projects exported with Godot. On mobile and web platforms, keeping file sizes low is important to ensure fast installation and loading on underpowered devices. Again, there are many countries where high-speed Internet is not readily available. To add to this, strict data usage caps are often in effect in those countries.

For all the reasons above, we have to be selective of what we can accept as core functionality in Godot. This is why we are aiming to move some core functionality to officially supported add-ons in future versions of Godot. In terms of binary size, this also has the advantage of making you pay only for what you actually use in your project. (In the meantime, you can compile custom export templates with unused features disabled to optimize the distribution size of your project.)

This question pops up often and it's probably thanks to the misunderstanding created by Apple when they originally doubled the resolution of their devices. It made people think that having the same assets in different resolutions was a good idea, so many continued towards that path. That originally worked to a point and only for Apple devices, but then several Android and Apple devices with different resolutions and aspect ratios were created, with a very wide range of sizes and DPIs.

The most common and proper way to achieve this is to, instead, use a single base resolution for the game and only handle different screen aspect ratios. This is mostly needed for 2D, as in 3D, it's just a matter of camera vertical or horizontal FOV.

Choose a single base resolution for your game. Even if there are devices that go up to 1440p and devices that go down to 400p, regular hardware scaling in your device will take care of this at little or no performance cost. The most common choices are either near 1080p (1920x1080) or 720p (1280x720). Keep in mind the higher the resolution, the larger your assets, the more memory they will take and the longer the time it will take for loading.

Use the stretch options in Godot; canvas items stretching while keeping aspect ratios works best. Check the Multiple resolutions tutorial on how to achieve this.

Determine a minimum resolution and then decide if you want your game to stretch vertically or horizontally for different aspect ratios, or if there is one aspect ratio and you want black bars to appear instead. This is also explained in Multiple resolutions.

For user interfaces, use the anchoring to determine where controls should stay and move. If UIs are more complex, consider learning about Containers.

And that's it! Your game should work in multiple resolutions.

When it's ready! See When is the next release out? for more information.

We recommend using Godot 4.x for new projects, but depending on the feature set you need, it may be better to use 3.x instead. See Which version should I use for a new project? for more information.

Some new versions are safer to upgrade to than others. In general, whether you should upgrade depends on your project's circumstances. See Should I upgrade my project to use new engine versions? for more information.

You can find a detailed comparison of the renderers in Overview of renderers.

Awesome! As an open source project, Godot thrives off of the innovation and the ambition of developers like you.

The best way to start contributing to Godot is by using it and reporting any issues that you might experience. A good bug report with clear reproduction steps helps your fellow contributors fix bugs quickly and efficiently. You can also report issues you find in the online documentation.

If you feel ready to submit your first PR, pick any issue that resonates with you from one of the links above and try your hand at fixing it. You will need to learn how to compile the engine from sources, or how to build the documentation. You also need to get familiar with Git, a version control system that Godot developers use.

We explain how to work with the engine source, how to edit the documentation, and what other ways to contribute are there in our documentation for contributors.

We are always looking for suggestions about how to improve the engine. User feedback is the main driving force behind our decision-making process, and limitations that you might face while working on your project are a great data point for us when considering engine enhancements.

If you experience a usability problem or are missing a feature in the current version of Godot, start by discussing it with our community. There may be other, perhaps better, ways to achieve the desired result that community members could suggest. And you can learn if other users experience the same issue, and figure out a good solution together.

If you come up with a well-defined idea for the engine, feel free to open a proposal issue. Try to be specific and concrete while describing your problem and your proposed solution — only actionable proposals can be considered. It is not required, but if you want to implement it yourself, that's always appreciated!

If you only have a general idea without specific details, you can open a proposal discussion. These can be anything you want, and allow for a free-form discussion in search of a solution. Once you find one, a proposal issue can be opened.

Please, read the readme document before creating a proposal to learn more about the process.

Yes! Godot features an extensive built-in UI system, and its small distribution size can make it a suitable alternative to frameworks like Electron or Qt.

When creating a non-game application, make sure to enable low-processor mode in the Project Settings to decrease CPU and GPU usage.

Check out Material Maker and Pixelorama for examples of open source applications made with Godot.

Godot is meant to be used with its editor. We recommend you give it a try, as it will most likely save you time in the long term. There are no plans to make Godot usable as a library, as it would make the rest of the engine more convoluted and difficult to use for casual users.

If you want to use a rendering library, look into using an established rendering engine instead. Keep in mind rendering engines usually have smaller communities compared to Godot. This will make it more difficult to find answers to your questions.

Godot does not use a standard GUI toolkit like GTK, Qt or wxWidgets. Instead, Godot uses its own user interface toolkit, rendered using OpenGL ES or Vulkan. This toolkit is exposed in the form of Control nodes, which are used to render the editor (which is written in C++). These Control nodes can also be used in projects from any scripting language supported by Godot.

This custom toolkit makes it possible to benefit from hardware acceleration and have a consistent appearance across all platforms. On top of that, it doesn't have to deal with the LGPL licensing caveats that come with GTK or Qt. Lastly, this means Godot is "eating its own dog food" since the editor itself is one of the most complex users of Godot's UI system.

This custom UI toolkit can't be used as a library, but you can still use Godot to create non-game applications by using the editor.

Godot uses the SCons build system. There are no plans to switch to a different build system in the near future. There are many reasons why we have chosen SCons over other alternatives. For example:

Godot can be compiled for a dozen different platforms: all PC platforms, all mobile platforms, many consoles, and WebAssembly.

Developers often need to compile for several of the platforms at the same time, or even different targets of the same platform. They can't afford reconfiguring and rebuilding the project each time. SCons can do this with no sweat, without breaking the builds.

SCons will never break a build no matter how many changes, configurations, additions, removals etc.

Godot's build process is not simple. Several files are generated by code (binders), others are parsed (shaders), and others need to offer customization (modules). This requires complex logic which is easier to write in an actual programming language (like Python) rather than using a mostly macro-based language only meant for building.

Godot's build process makes heavy use of cross-compiling tools. Each platform has a specific detection process, and all these must be handled as specific cases with special code written for each.

Please try to keep an open mind and get at least a little familiar with SCons if you are planning to build Godot yourself.

Like many other libraries (Qt as an example), Godot does not make use of STL (with a few exceptions such as threading primitives). We believe STL is a great general-purpose library, but we had special requirements for Godot.

STL templates create very large symbols, which results in huge debug binaries. We use few templates with very short names instead.

Most of our containers cater to special needs, like Vector, which uses copy on write and we use to pass data around, or the RID system, which requires O(1) access time for performance. Likewise, our hash map implementations are designed to integrate seamlessly with internal engine types.

Our containers have memory tracking built-in, which helps better track memory usage.

For large arrays, we use pooled memory, which can be mapped to either a preallocated buffer or virtual memory.

We use our custom String type, as the one provided by STL is too basic and lacks proper internationalization support.

Check out Godot's container types for alternatives.

We believe games should not crash, no matter what. If an unexpected situation happens, Godot will print an error (which can be traced even to script), but then it will try to recover as gracefully as possible and keep going.

Additionally, exceptions significantly increase the binary size for the executable and result in increased compile times.

Godot does not use an ECS and relies on inheritance instead. While there is no universally better approach, we found that using an inheritance-based approach resulted in better usability while still being fast enough for most use cases.

That said, nothing prevents you from making use of composition in your project by creating child Nodes with individual scripts. These nodes can then be added and removed at runtime to dynamically add and remove behaviors.

More information about Godot's design choices can be found in this article.

While Godot internally attempts to use cache coherency as much as possible, we believe users don't need to be forced to use DOD practices.

DOD is mostly a cache coherency optimization that can only provide significant performance improvements when dealing with dozens of thousands of objects which are processed every frame with little modification. That is, if you are moving a few hundred sprites or enemies per frame, DOD won't result in a meaningful improvement in performance. In such a case, you should consider a different approach to optimization.

The vast majority of games do not need this and Godot provides handy helpers to do the job for most cases when you do.

If a game needs to process such a large amount of objects, our recommendation is to use C++ and GDExtensions for performance-heavy tasks and GDScript (or C#) for the rest of the game.

See How to contribute.

See the corresponding page on the Godot website.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Complying with licenses — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/complying_with_licenses.html

**Contents:**
- Complying with licenses
- What are licenses?
- Requirements
- Inclusion
  - Credits screen
  - Licenses screen
  - Output log
  - Accompanying file
  - Printed manual
  - Link to the license

The recommendations in this page are not legal advice. They are provided in good faith to help users navigate license attribution requirements.

Godot is created and distributed under the MIT License. It doesn't have a sole owner, as every contributor that submits code to the project does it under this same license and keeps ownership of their contribution.

The license is the legal requirement for you (or your company) to use and distribute the software (and derivative projects, including games made with it). Your game or project can have a different license, but it still needs to comply with the original one.

This section covers compliance with licenses from a user perspective. If you are interested in licence compliance as a contributor, you can find guidelines here.

Alongside the Godot license text, remember to also list third-party notices for assets you're using, such as textures, models, sounds, music and fonts. This includes free assets, which often come with licenses that require attribution.

In the case of the MIT license, the only requirement is to include the license text somewhere in your game or derivative project.

This text reads as follows:

Beside its own MIT license, Godot includes code from a number of third-party libraries. See Third-party licenses for details.

Your games do not need to be under the same license. You are free to release your Godot projects under any license and to create commercial games with the engine.

The license text must be made available to the user. The license doesn't specify how the text has to be included, but here are the most common approaches (you only need to implement one of them, not all).

Include the above license text somewhere in the credits screen. It can be at the bottom after showing the rest of the credits. Most large studios use this approach with open source licenses.

Some games have a special menu (often in the settings) to display licenses. This menu is typically accessed with a button called Third-party Licenses or Open Source Licenses.

Printing the license text using the print() function may be enough on platforms where a global output log is readable. This is the case on desktop platforms, Android and HTML5 (but not iOS).

If the game is distributed on desktop platforms, a file containing the license text can be added to the software that is installed to the user PC.

If the game includes a printed manual, the license text can be included there.

The Godot Engine developers consider that a link to godotengine.org/license in your game documentation or credits would be an acceptable way to satisfy the license terms.

Godot provides several methods to get license information in the Engine singleton. This allows you to source the license information directly from the engine binary, which prevents the information from becoming outdated if you update engine versions.

For the engine itself:

Engine.get_license_text

For third-party components used by the engine:

Engine.get_license_info

Engine.get_copyright_info

Godot itself contains software written by third parties, which is compatible with, but not covered by Godot's MIT license.

Many of these dependencies are distributed under permissive open source licenses which require attribution by explicitly citing their copyright statement and license text in the final product's documentation.

Given the scope of the Godot project, this is fairly difficult to do thoroughly. For the Godot editor, the full documentation of third-party copyrights and licenses is provided in the COPYRIGHT.txt file.

A good option for end users to document third-party licenses is to include this file in your project's distribution, which you can e.g. rename to GODOT_COPYRIGHT.txt to prevent any confusion with your own code and assets.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
This game uses Godot Engine, available under the following license:

Copyright (c) 2014-present Godot Engine contributors.
Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Godot release policy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/release_policy.html

**Contents:**
- Godot release policy
- Godot versioning
- Release support timeline
- Which version should I use for a new project?
- Should I upgrade my project to use new engine versions?
- When is the next release out?
- What are the criteria for compatibility across engine versions?

Godot's release policy is in constant evolution. The description below provides a general idea of what to expect, but what will actually happen depends on the choices of core contributors and the needs of the community at a given time.

Godot loosely follows Semantic Versioning with a major.minor.patch versioning system, albeit with an interpretation of each term adapted to the complexity of a game engine:

The major version is incremented when major compatibility breakages happen which imply significant porting work to move projects from one major version to another.

For example, porting Godot projects from Godot 3.x to Godot 4.x requires running the project through a conversion tool, and then performing a number of further adjustments manually for what the tool could not do automatically.

The minor version is incremented for feature releases that do not break compatibility in a major way. Minor compatibility breakage in very specific areas may happen in minor versions, but the vast majority of projects should not be affected or require significant porting work.

This is because Godot, as a game engine, covers many areas like rendering, physics, and scripting. Fixing bugs or implementing new features in one area might sometimes require changing a feature's behavior or modifying a class's interface, even if the rest of the engine API remains backwards compatible.

Upgrading to a new minor version is recommended for all users, but some testing is necessary to ensure that your project still behaves as expected.

The patch version is incremented for maintenance releases which focus on fixing bugs and security issues, implementing new requirements for platform support, and backporting safe usability enhancements. Patch releases are backwards compatible.

Patch versions may include minor new features which do not impact the existing API, and thus have no risk of impacting existing projects.

Updating to new patch versions is therefore considered safe and strongly recommended to all users of a given stable branch.

We call major.minor combinations stable branches. Each stable branch starts with a major.minor release (without the 0 for patch) and is further developed for maintenance releases in a Git branch of the same name (for example patch updates for the 4.0 stable branch are developed in the 4.0 Git branch).

Stable branches are supported at least until the next stable branch is released and has received its first patch update. In practice, we support stable branches on a best effort basis for as long as they have active users who need maintenance updates.

Whenever a new major version is released, we make the previous stable branch a long-term supported release, and do our best to provide fixes for issues encountered by users of that branch who cannot port complex projects to the new major version. This was the case for the 2.1 branch, and is the case for the 3.x branch.

In a given minor release series, only the latest patch release receives support. If you experience an issue using an older patch release, please upgrade to the latest patch release of that series and test again before reporting an issue on GitHub.

Development. Receives new features, usability and performance improvements, as well as bug fixes, while under development.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for security and platform support issues only.

No longer supported (last update: 4.1.4).

No longer supported (last update: 4.0.4).

Beta. Receives new features, usability and performance improvements, as well as bug fixes, while under development.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for security and platform support issues only.

No longer supported (last update: 3.4.5).

No longer supported (last update: 3.3.4).

No longer supported (last update: 3.2.3).

No longer supported (last update: 3.1.2).

No longer supported (last update: 3.0.6).

No longer supported (last update: 2.1.6).

No longer supported (last update: 2.0.4.1).

Legend: Full support – Partial support – No support (end of life) – Development version

Pre-release Godot versions aren't intended to be used in production and are provided for testing purposes only.

See Upgrading from Godot 3 to Godot 4 for instructions on migrating a project from Godot 3.x to 4.x.

We recommend using Godot 4.x for new projects, as the Godot 4.x series will be supported long after 3.x stops receiving updates in the future. One caveat is that a lot of third-party documentation hasn't been updated for Godot 4.x yet. If you have to follow a tutorial designed for Godot 3.x, we recommend keeping Upgrading from Godot 3 to Godot 4 open in a separate tab to check which methods have been renamed (if you get a script error while trying to use a specific node or method that was renamed in Godot 4.x).

If your project requires a feature that is missing in 4.x (such as GLES2/WebGL 1.0), you should use Godot 3.x for a new project instead.

Upgrading software while working on a project is inherently risky, so consider whether it's a good idea for your project before attempting an upgrade. Also, make backups of your project or use version control to prevent losing data in case the upgrade goes wrong.

That said, we do our best to keep minor and especially patch releases compatible with existing projects.

The general recommendation is to upgrade your project to follow new patch releases, such as upgrading from 4.0.2 to 4.0.3. This ensures you get bug fixes, security updates and platform support updates (which is especially important for mobile platforms). You also get continued support, as only the last patch release receives support on official community platforms.

For minor releases, you should determine whether it's a good idea to upgrade on a case-by-case basis. We've made a lot of effort in making the upgrade process as seamless as possible, but some breaking changes may be present in minor releases, along with a greater risk of regressions. Some fixes included in minor releases may also change a class' expected behavior as required to fix some bugs. This is especially the case in classes marked as experimental in the documentation.

Major releases bring a lot of new functionality, but they also remove previously existing functionality and may raise hardware requirements. They also require much more work to upgrade to compared to minor releases. As a result, we recommend sticking with the major release you've started your project with if you are happy with how your project currently works. For example, if your project was started with 3.5, we recommend upgrading to 3.5.2 and possibly 3.6 in the future, but not to 4.0+, unless your project really needs the new features that come with 4.0+.

While Godot contributors aren't working under any deadlines, we strive to publish minor releases relatively frequently.

In particular, after the very long release cycle for 4.0, we are pivoting to a faster-paced development workflow, 4.1 released 4 months after 4.0, and 4.2 released 4 months after 4.1.

Frequent minor releases will enable us to ship new features faster (possibly as experimental), get user feedback quickly, and iterate to improve those features and their usability. Likewise, the general user experience will be improved more steadily with a faster path to the end users.

Maintenance (patch) releases are released as needed with potentially very short development cycles, to provide users of the current stable branch with the latest bug fixes for their production needs.

There is currently no planned release date for the next 3.x minor version, 3.7. The current stable release, 3.6, may be the last stable branch of Godot 3.x. Godot 3.x is supported on a best-effort basis, as long as contributors continue to maintain it.

This section is intended to be used by contributors to determine which changes are safe for a given release. The list is not exhaustive; it only outlines the most common situations encountered during Godot's development.

The following changes are acceptable in patch releases:

Fixing a bug in a way that has no major negative impact on most projects, such as a visual or physics bug. Godot's physics engine is not deterministic, so physics bug fixes are not considered to break compatibility. If fixing a bug has a negative impact that could impact a lot of projects, it should be made optional (e.g. using a project setting or separate method).

Adding a new optional parameter to a method.

Small-scale editor usability tweaks.

Note that we tend to be more conservative with the fixes we allow in each subsequent patch release. For instance, 4.0.1 may receive more impactful fixes than 4.0.4 would.

The following changes are acceptable in minor releases, but not patch releases:

Significant new features.

Renaming a method parameter. In C#, method parameters can be passed by name (but not in GDScript). As a result, this can break some projects that use C#.

Deprecating a method, member variable, or class. This is done by adding a deprecated flag to its class reference, which will show up in the editor. When a method is marked as deprecated, it's slated to be removed in the next major release.

Changes that affect the default project theme's visuals.

Bug fixes which significantly change the behavior or the output, with the aim to meet user expectations better. In comparison, in patch releases, we may favor keeping a buggy behavior so we don't break existing projects which likely already rely on the bug or use a workaround.

Performance optimizations that result in visual changes.

The following changes are considered compatibility-breaking and can only be performed in a new major release:

Renaming or removing a method, member variable, or class.

Modifying a node's inheritance tree by making it inherit from a different class.

Changing the default value of a project setting value in a way that affects existing projects. To only affect new projects, the project manager should write a modified project.godot instead.

Since Godot 5.0 hasn't been branched off yet, we currently discourage making compatibility-breaking changes of this kind.

When modifying a method's signature in any fashion (including adding an optional parameter), a GDExtension compatibility method must be created. This ensures that existing GDExtensions continue to work across patch and minor releases, so that users don't have to recompile them. See Handling compatibility breakages for more information.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Best practices — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html

**Contents:**
- Best practices

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Scene organization — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html

**Contents:**
- Scene organization
- How to build relationships effectively
- Choosing a node tree structure
- User-contributed notes

This article covers topics related to the effective organization of scene content. Which nodes should you use? Where should you place them? How should they interact?

When Godot users begin crafting their own scenes, they often run into the following problem:

They create their first scene and fill it with content only to eventually end up saving branches of their scene into separate scenes as the nagging feeling that they should split things up starts to accumulate. However, they then notice that the hard references they were able to rely on before are no longer possible. Re-using the scene in multiple places creates issues because the node paths do not find their targets and signal connections established in the editor break.

To fix these problems, you must instantiate the sub-scenes without them requiring details about their environment. You need to be able to trust that the sub-scene will create itself without being picky about how it's used.

One of the biggest things to consider in OOP is maintaining focused, singular-purpose classes with loose coupling to other parts of the codebase. This keeps the size of objects small (for maintainability) and improves their reusability.

These OOP best practices have several implications for best practices in scene structure and script usage.

If at all possible, you should design scenes to have no dependencies. That is, you should create scenes that keep everything they need within themselves.

If a scene must interact with an external context, experienced developers recommend the use of Dependency Injection. This technique involves having a high-level API provide the dependencies of the low-level API. Why do this? Because classes which rely on their external environment can inadvertently trigger bugs and unexpected behavior.

To do this, you must expose data and then rely on a parent context to initialize it:

Connect to a signal. Extremely safe, but should be used only to "respond" to behavior, not start it. By convention, signal names are usually past-tense verbs like "entered", "skill_activated", or "item_collected".

Call a method. Used to start behavior.

Initialize a Callable property. Safer than a method as ownership of the method is unnecessary. Used to start behavior.

Initialize a Node or other Object reference.

Initialize a NodePath.

These options hide the points of access from the child node. This in turn keeps the child loosely coupled to its environment. You can reuse it in another context without any extra changes to its API.

Although the examples above illustrate parent-child relationships, the same principles apply towards all object relations. Nodes which are siblings should only be aware of their own hierarchies while an ancestor mediates their communications and references.

The same principles also apply to non-Node objects that maintain dependencies on other objects. Whichever object owns the other objects should manage the relationships between them.

You should favor keeping data in-house (internal to a scene), though, as placing a dependency on an external context, even a loosely coupled one, still means that the node will expect something in its environment to be true. The project's design philosophies should prevent this from happening. If not, the code's inherent liabilities will force developers to use documentation to keep track of object relations on a microscopic scale; this is otherwise known as development hell. Writing code that relies on external documentation to use it safely is error-prone by default.

To avoid creating and maintaining such documentation, you convert the dependent node ("child" above) into a tool script that implements _get_configuration_warnings(). Returning a non-empty PackedStringArray from it will make the Scene dock generate a warning icon with the string(s) as a tooltip by the node. This is the same icon that appears for nodes such as the Area2D node when it has no child CollisionShape2D nodes defined. The editor then self-documents the scene through the script code. No content duplication via documentation is necessary.

A GUI like this can better inform project users of critical information about a Node. Does it have external dependencies? Have those dependencies been satisfied? Other programmers, and especially designers and writers, will need clear instructions in the messages telling them what to do to configure it.

So, why does all this complex switcheroo work? Well, because scenes operate best when they operate alone. If unable to work alone, then working with others anonymously (with minimal hard dependencies, i.e. loose coupling) is the next best thing. Inevitably, changes may need to be made to a class, and if these changes cause it to interact with other scenes in unforeseen ways, then things will start to break down. The whole point of all this indirection is to avoid ending up in a situation where changing one class results in adversely affecting other classes dependent on it.

Scripts and scenes, as extensions of engine classes, should abide by all OOP principles. Examples include...

You might start to work on a game but get overwhelmed by the vast possibilities before you. You might know what you want to do, what systems you want to have, but where do you put them all? How you go about making your game is always up to you. You can construct node trees in countless ways. If you are unsure, this guide can give you a sample of a decent structure to start with.

A game should always have an "entry point"; somewhere you can definitively track where things begin so that you can follow the logic as it continues elsewhere. It also serves as a bird's eye view of all other data and logic in the program. For traditional applications, this is normally a "main" function. In Godot, it's a Main node.

Node "Main" (main.gd)

The main.gd script will serve as the primary controller of your game.

Then you have an in-game "World" (a 2D or 3D one). This can be a child of Main. In addition, you will need a primary GUI for your game that manages the various menus and widgets the project needs.

Node2D/Node3D "World" (game_world.gd)

Control "GUI" (gui.gd)

When changing levels, you can then swap out the children of the "World" node. Changing scenes manually gives you full control over how your game world transitions.

The next step is to consider what gameplay systems your project requires. If you have a system that...

tracks all of its data internally

should be globally accessible

should exist in isolation

... then you should create an autoload 'singleton' node.

For smaller games, a simpler alternative with less control would be to have a "Game" singleton that simply calls the SceneTree.change_scene_to_file() method to swap out the main scene's content. This structure more or less keeps the "World" as the main game node.

Any GUI would also need to be either a singleton, a transitory part of the "World", or manually added as a direct child of the root. Otherwise, the GUI nodes would also delete themselves during scene transitions.

If you have systems that modify other systems' data, you should define those as their own scripts or scenes, rather than autoloads. For more information, see Autoloads versus regular nodes.

Each subsystem within your game should have its own section within the SceneTree. You should use parent-child relationships only in cases where nodes are effectively elements of their parents. Does removing the parent reasonably mean that the children should also be removed? If not, then it should have its own place in the hierarchy as a sibling or some other relation.

In some cases, you need these separated nodes to also position themselves relative to each other. You can use the RemoteTransform / RemoteTransform2D nodes for this purpose. They will allow a target node to conditionally inherit selected transform elements from the Remote* node. To assign the target NodePath, use one of the following:

A reliable third party, likely a parent node, to mediate the assignment.

A group, to pull a reference to the desired node (assuming there will only ever be one of the targets).

When you should do this is subjective. The dilemma arises when you must micro-manage when a node must move around the SceneTree to preserve itself. For example...

Add a "player" node to a "room".

Need to change rooms, so you must delete the current room.

Before the room can be deleted, you must preserve and/or move the player.

If memory is not a concern, you can...

Move the player to the new room.

If memory is a concern, instead you will need to...

Move the player somewhere else in the tree.

Instantiate and add the new room.

Re-add the player to the new room.

The issue is that the player here is a "special case" where the developers must know that they need to handle the player this way for the project. The only way to reliably share this information as a team is to document it. Keeping implementation details in documentation is dangerous. It's a maintenance burden, strains code readability, and unnecessarily bloats the intellectual content of a project.

In a more complex game with larger assets, it can be a better idea to keep the player somewhere else in the SceneTree entirely. This results in:

No "special cases" that must be documented and maintained somewhere.

No opportunity for errors to occur because these details are not accounted for.

In contrast, if you ever need a child node that does not inherit the transform of its parent, you have the following options:

The declarative solution: place a Node in between them. Since it doesn't have a transform, they won't pass this information to its children.

The imperative solution: Use the top_level property for the CanvasItem or Node3D node. This will make the node ignore its inherited transform.

If building a networked game, keep in mind which nodes and gameplay systems are relevant to all players versus those just pertinent to the authoritative server. For example, users do not all need to have a copy of every players' "PlayerController" logic - they only need their own. Keeping them in a separate branch from the "world" can help simplify the management of game connections and the like.

The key to scene organization is to consider the SceneTree in relational terms rather than spatial terms. Are the nodes dependent on their parent's existence? If not, then they can thrive all by themselves somewhere else. If they are dependent, then it stands to reason that they should be children of that parent (and likely part of that parent's scene if they aren't already).

Does this mean nodes themselves are components? Not at all. Godot's node trees form an aggregation relationship, not one of composition. But while you still have the flexibility to move nodes around, it is still best when such moves are unnecessary by default.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# Parent
$Child.signal_name.connect(method_on_the_object)

# Child
signal_name.emit() # Triggers parent-defined behavior.
```

Example 2 (unknown):
```unknown
// Parent
GetNode("Child").Connect("SignalName", Callable.From(ObjectWithMethod.MethodOnTheObject));

// Child
EmitSignal("SignalName"); // Triggers parent-defined behavior.
```

Example 3 (php):
```php
// Parent
Node *node = get_node<Node>("Child");
if (node != nullptr) {
    // Note that get_node may return a nullptr, which would make calling the connect method crash the engine if "Child" does not exist!
    // So unless you are 1000% sure get_node will never return a nullptr, it's a good idea to always do a nullptr check.
    node->connect("signal_name", callable_mp(this, &ObjectWithMethod::method_on_the_object));
}

// Child
emit_signal("signal_name"); // Triggers parent-defined behavior.
```

Example 4 (markdown):
```markdown
# Parent
$Child.method_name = "do"

# Child, assuming it has String property 'method_name' and method 'do'.
call(method_name) # Call parent-defined method (which child must own).
```

---

## When to use scenes versus scripts — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/scenes_versus_scripts.html

**Contents:**
- When to use scenes versus scripts
- Anonymous types
- Named types
- Performance of Script vs PackedScene
- Conclusion
- User-contributed notes

We've already covered how scenes and scripts are different. Scripts define an engine class extension with imperative code, scenes with declarative code.

Each system's capabilities are different as a result. Scenes can define how an extended class initializes, but not what its behavior actually is. Scenes are often used in conjunction with a script, the scene declaring a composition of nodes, and the script adding behavior with imperative code.

It is possible to completely define a scenes' contents using a script alone. This is, in essence, what the Godot Editor does, only in the C++ constructor of its objects.

But, choosing which one to use can be a dilemma. Creating script instances is identical to creating in-engine classes whereas handling scenes requires a change in API:

Also, scripts will operate a little slower than scenes due to the speed differences between engine and script code. The larger and more complex the node, the more reason there is to build it as a scene.

Scripts can be registered as a new type within the editor itself. This displays it as a new type in the node or resource creation dialog with an optional icon. This way, the user's ability to use the script is much more streamlined. Rather than having to...

Know the base type of the script they would like to use.

Create an instance of that base type.

Add the script to the node.

With a registered script, the scripted type instead becomes a creation option like the other nodes and resources in the system. The creation dialog even has a search bar to look up the type by name.

There are two systems for registering types:

Editor-only. Typenames are not accessible at runtime.

Does not support inherited custom types.

An initializer tool. Creates the node with the script. Nothing more.

Editor has no type-awareness of the script or its relationship to other engine types or scripts.

Allows users to define an icon.

Works for all scripting languages because it deals with Script resources in abstract.

Set up using EditorPlugin.add_custom_type.

Editor and runtime accessible.

Displays inheritance relationships in full.

Creates the node with the script, but can also change types or extend the type from the editor.

Editor is aware of inheritance relationships between scripts, script classes, and engine C++ classes.

Allows users to define an icon.

Engine developers must add support for languages manually (both name exposure and runtime accessibility).

The Editor scans project folders and registers any exposed names for all scripting languages. Each scripting language must implement its own support for exposing this information.

Both methodologies add names to the creation dialog, but script classes, in particular, also allow for users to access the typename without loading the script resource. Creating instances and accessing constants or static methods is viable from anywhere.

With features like these, one may wish their type to be a script without a scene due to the ease of use it grants users. Those developing plugins or creating in-house tools for designers to use will find an easier time of things this way.

On the downside, it also means having to use largely imperative programming.

One last aspect to consider when choosing scenes and scripts is execution speed.

As the size of objects increases, the scripts' necessary size to create and initialize them grows much larger. Creating node hierarchies demonstrates this. Each Node's logic could be several hundred lines of code in length.

The code example below creates a new Node, changes its name, assigns a script to it, sets its future parent as its owner so it gets saved to disk along with it, and finally adds it as a child of the Main node:

Script code like this is much slower than engine-side C++ code. Each instruction makes a call to the scripting API which leads to many "lookups" on the back-end to find the logic to execute.

Scenes help to avoid this performance issue. PackedScene, the base type that scenes inherit from, defines resources that use serialized data to create objects. The engine can process scenes in batches on the back-end and provide much better performance than scripts.

In the end, the best approach is to consider the following:

If one wishes to create a basic tool that is going to be re-used in several different projects and which people of all skill levels will likely use (including those who don't label themselves as "programmers"), then chances are that it should probably be a script, likely one with a custom name/icon.

If one wishes to create a concept that is particular to their game, then it should always be a scene. Scenes are easier to track/edit and provide more security than scripts.

If one would like to give a name to a scene, then they can still sort of do this by declaring a script class and giving it a scene as a constant. The script becomes, in effect, a namespace:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (javascript):
```javascript
const MyNode = preload("my_node.gd")
const MyScene = preload("my_scene.tscn")
var node = Node.new()
var my_node = MyNode.new() # Same method call.
var my_scene = MyScene.instantiate() # Different method call.
var my_inherited_scene = MyScene.instantiate(PackedScene.GEN_EDIT_STATE_MAIN) # Create scene inheriting from MyScene.
```

Example 2 (swift):
```swift
using Godot;

public partial class Game : Node
{
    public static CSharpScript MyNode { get; } =
        GD.Load<CSharpScript>("res://Path/To/MyNode.cs");
    public static PackedScene MyScene { get; } =
        GD.Load<PackedScene>("res://Path/To/MyScene.tscn");
    private Node _node;
    private Node _myNode;
    private Node _myScene;
    private Node _myInheritedScene;

    public Game()
    {
        _node = new Node();
        _myNode = MyNode.New().As<Node>();
        // Different than calling new() or MyNode.New(). Instantiated from a PackedScene.
        _myScene = MyScene.Instantiate();
        // Create scene inheriting from MyScene.
        _myInheritedScene = MyScene.Instantiate(PackedScene.GenEditState.Main);
    }
}
```

Example 3 (gdscript):
```gdscript
# main.gd
extends Node

func _init():
    var child = Node.new()
    child.name = "Child"
    child.script = preload("child.gd")
    add_child(child)
    child.owner = self
```

Example 4 (csharp):
```csharp
using Godot;

public partial class Main : Node
{
    public Node Child { get; set; }

    public Main()
    {
        Child = new Node();
        Child.Name = "Child";
        var childID = Child.GetInstanceId();
        Child.SetScript(GD.Load<Script>("res://Path/To/Child.cs"));
        // SetScript() causes the C# wrapper object to be disposed, so obtain a new
        // wrapper for the Child node using its instance ID before proceeding.
        Child = (Node)GodotObject.InstanceFromId(childID);
        AddChild(Child);
        Child.Owner = this;
    }
}
```

---

## Autoloads versus regular nodes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/autoloads_versus_internal_nodes.html

**Contents:**
- Autoloads versus regular nodes
- The cutting audio issue
- Managing shared functionality or data
- When you should use an Autoload
- User-contributed notes

Godot offers a feature to automatically load nodes at the root of your project, allowing you to access them globally, that can fulfill the role of a Singleton: Singletons (Autoload). These autoloaded nodes are not freed when you change the scene from code with SceneTree.change_scene_to_file.

In this guide, you will learn when to use the Autoload feature, and techniques you can use to avoid it.

Other engines can encourage the use of creating manager classes, singletons that organize a lot of functionality into a globally accessible object. Godot offers many ways to avoid global state thanks to the node tree and signals.

For example, let's say we are building a platformer and want to collect coins that play a sound effect. There's a node for that: the AudioStreamPlayer. But if we call the AudioStreamPlayer while it is already playing a sound, the new sound interrupts the first.

A solution is to code a global, autoloaded sound manager class. It generates a pool of AudioStreamPlayer nodes that cycle through as each new request for sound effects comes in. Say we call that class Sound, you can use it from anywhere in your project by calling Sound.play("coin_pickup.ogg"). This solves the problem in the short term but causes more problems:

Global state: one object is now responsible for all objects' data. If the Sound class has errors or doesn't have an AudioStreamPlayer available, all the nodes calling it can break.

Global access: now that any object can call Sound.play(sound_path) from anywhere, there's no longer an easy way to find the source of a bug.

Global resource allocation: with a pool of AudioStreamPlayer nodes stored from the start, you can either have too few and face bugs, or too many and use more memory than you need.

About global access, the problem is that any code anywhere could pass wrong data to the Sound autoload in our example. As a result, the domain to explore to fix the bug spans the entire project.

When you keep code inside a scene, only one or two scripts may be involved in audio.

Contrast this with each scene keeping as many AudioStreamPlayer nodes as it needs within itself and all these problems go away:

Each scene manages its own state information. If there is a problem with the data, it will only cause issues in that one scene.

Each scene accesses only its own nodes. Now, if there is a bug, it's easy to find which node is at fault.

Each scene allocates exactly the amount of resources it needs.

Another reason to use an Autoload can be that you want to reuse the same method or data across many scenes.

In the case of functions, you can create a new type of Node that provides that feature for an individual scene using the class_name keyword in GDScript.

When it comes to data, you can either:

Create a new type of Resource to share the data.

Store the data in an object to which each node has access, for example using the owner property to access the scene's root node.

GDScript supports the creation of static functions using static func. When combined with class_name, this makes it possible to create libraries of helper functions without having to create an instance to call them. The limitation of static functions is that they can't reference member variables, non-static functions or self.

Since Godot 4.1, GDScript also supports static variables using static var. This means you can now share variables across instances of a class without having to create a separate autoload.

Still, autoloaded nodes can simplify your code for systems with a wide scope. If the autoload is managing its own information and not invading the data of other objects, then it's a great way to create systems that handle broad-scoped tasks. For example, a quest or a dialogue system.

An autoload is not necessarily a singleton. Nothing prevents you from instantiating copies of an autoloaded node. An autoload is only a tool that makes a node load automatically as a child of the root of your scene tree, regardless of your game's node structure or which scene you run, e.g. by pressing the F6 key.

As a result, you can get the autoloaded node, for example an autoload called Sound, by calling get_node("/root/Sound").

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## When and how to avoid using nodes for everything — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/node_alternatives.html

**Contents:**
- When and how to avoid using nodes for everything
- User-contributed notes

Nodes are cheap to produce, but even they have their limits. A project may have tens of thousands of nodes all doing things. The more complex their behavior though, the larger the strain each one adds to a project's performance.

Godot provides more lightweight objects for creating APIs which nodes use. Be sure to keep these in mind as options when designing how you wish to build your project's features.

Object: The ultimate lightweight object, the original Object must use manual memory management. With that said, it isn't too difficult to create one's own custom data structures, even node structures, that are also lighter than the Node class.

Example: See the Tree node. It supports a high level of customization for a table of content with an arbitrary number of rows and columns. The data that it uses to generate its visualization though is actually a tree of TreeItem Objects.

Advantages: Simplifying one's API to smaller scoped objects helps improve its accessibility and improve iteration time. Rather than working with the entire Node library, one creates an abbreviated set of Objects from which a node can generate and manage the appropriate sub-nodes.

One should be careful when handling them. One can store an Object into a variable, but these references can become invalid without warning. For example, if the object's creator decides to delete it out of nowhere, this would trigger an error state when one next accesses it.

RefCounted: Only a little more complex than Object. They track references to themselves, only deleting loaded memory when no further references to themselves exist. These are useful in the majority of cases where one needs data in a custom class.

Example: See the FileAccess object. It functions just like a regular Object except that one need not delete it themselves.

Advantages: same as the Object.

Resource: Only slightly more complex than RefCounted. They have the innate ability to serialize/deserialize (i.e. save and load) their object properties to/from Godot resource files.

Example: Scripts, PackedScene (for scene files), and other types like each of the AudioEffect classes. Each of these can be saved and loaded, therefore they extend from Resource.

Advantages: Much has already been said on Resource's advantages over traditional data storage methods. In the context of using Resources over Nodes though, their main advantage is in Inspector-compatibility. While nearly as lightweight as Object/RefCounted, they can still display and export properties in the Inspector. This allows them to fulfill a purpose much like sub-Nodes on the usability front, but also improve performance if one plans to have many such Resources/Nodes in their scenes.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Godot interfaces — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/godot_interfaces.html

**Contents:**
- Godot interfaces
- Acquiring object references
- Accessing data or logic from an object
- User-contributed notes

Often one needs scripts that rely on other objects for features. There are 2 parts to this process:

Acquiring a reference to the object that presumably has the features.

Accessing the data or logic from the object.

The rest of this tutorial outlines the various ways of doing all this.

For all Objects, the most basic way of referencing them is to get a reference to an existing object from another acquired instance.

The same principle applies for RefCounted objects. While users often access Node and Resource this way, alternative measures are available.

Instead of property or method access, one can get Resources by load access.

There are many ways in which a language can load such resources.

When designing how objects will access data, don't forget that one can pass resources around as references as well.

Keep in mind that loading a resource fetches the cached resource instance maintained by the engine. To get a new object, one must duplicate an existing reference or instantiate one from scratch with new().

Nodes likewise have an alternative access point: the SceneTree.

Godot's scripting API is duck-typed. This means that if a script executes an operation, Godot doesn't validate that it supports the operation by type. It instead checks that the object implements the individual method.

For example, the CanvasItem class has a visible property. All properties exposed to the scripting API are in fact a setter and getter pair bound to a name. If one tried to access CanvasItem.visible, then Godot would do the following checks, in order:

If the object has a script attached, it will attempt to set the property through the script. This leaves open the opportunity for scripts to override a property defined on a base object by overriding the setter method for the property.

If the script does not have the property, it performs a HashMap lookup in the ClassDB for the "visible" property against the CanvasItem class and all of its inherited types. If found, it will call the bound setter or getter. For more information about HashMaps, see the data preferences docs.

If not found, it does an explicit check to see if the user wants to access the "script" or "meta" properties.

If not, it checks for a _set/_get implementation (depending on type of access) in the CanvasItem and its inherited types. These methods can execute logic that gives the impression that the Object has a property. This is also the case with the _get_property_list method.

Note that this happens even for non-legal symbol names, such as names starting with a digit or containing a slash.

As a result, this duck-typed system can locate a property either in the script, the object's class, or any class that object inherits, but only for things which extend Object.

Godot provides a variety of options for performing runtime checks on these accesses:

A duck-typed property access. These will be property checks (as described above). If the operation isn't supported by the object, execution will halt.

A method check. In the case of CanvasItem.visible, one can access the methods, set_visible and is_visible like any other method.

Outsource the access to a Callable. These may be useful in cases where one needs the max level of freedom from dependencies. In this case, one relies on an external context to setup the method.

These strategies contribute to Godot's flexible design. Between them, users have a breadth of tools to meet their specific needs.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var obj = node.object # Property access.
var obj = node.get_object() # Method access.
```

Example 2 (unknown):
```unknown
GodotObject obj = node.Object; // Property access.
GodotObject obj = node.GetObject(); // Method access.
```

Example 3 (swift):
```swift
# If you need an "export const var" (which doesn't exist), use a conditional
# setter for a tool script that checks if it's executing in the editor.
# The `@tool` annotation must be placed at the top of the script.
@tool

# Load resource during scene load.
var preres = preload(path)
# Load resource when program reaches statement.
var res = load(path)

# Note that users load scenes and scripts, by convention, with PascalCase
# names (like typenames), often into constants.
const MyScene = preload("my_scene.tscn") # Static load
const MyScript = preload("my_script.gd")

# This type's value varies, i.e. it is a variable, so it uses snake_case.
@export var script_type: Script

# Must configure from the editor, defaults to null.
@export var const_script: Script:
    set(value):
        if Engine.is_editor_hint():
            const_script = value

# Warn users if the value hasn't been set.
func _get_configuration_warnings():
    if not const_script:
        return ["Must initialize property 'const_script'."]

    return []
```

Example 4 (json):
```json
// Tool script added for the sake of the "const [Export]" example.
[Tool]
public MyType
{
    // Property initializations load during Script instancing, i.e. .new().
    // No "preload" loads during scene load exists in C#.

    // Initialize with a value. Editable at runtime.
    public Script MyScript = GD.Load<Script>("res://Path/To/MyScript.cs");

    // Initialize with same value. Value cannot be changed.
    public readonly Script MyConstScript = GD.Load<Script>("res://Path/To/MyScript.cs");

    // Like 'readonly' due to inaccessible setter.
    // But, value can be set during constructor, i.e. MyType().
    public Script MyNoSetScript { get; } = GD.Load<Script>("res://Path/To/MyScript.cs");

    // If need a "const [Export]" (which doesn't exist), use a
    // conditional setter for a tool script that checks if it's executing
    // in the editor.
    private PackedScene _enemyScn;

    [Export]
    public PackedScene EnemyScn
    {
        get { return _enemyScn; }
        set
        {
            if (Engine.IsEditorHint())
            {
                _enemyScn = value;
            }
        }
    };

    // Warn users if the value hasn't been set.
    public string[] _GetConfigurationWarnings()
    {
        if (EnemyScn == null)
        {
            return ["Must initialize property 'EnemyScn'."];
        }
        return [];
    }
}
```

---

## Godot notifications — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/godot_notifications.html

**Contents:**
- Godot notifications
- _process vs. _physics_process vs. *_input
- _init vs. initialization vs. export
- _ready vs. _enter_tree vs. NOTIFICATION_PARENTED
- User-contributed notes

Every Object in Godot implements a _notification method. Its purpose is to allow the Object to respond to a variety of engine-level callbacks that may relate to it. For example, if the engine tells a CanvasItem to "draw", it will call _notification(NOTIFICATION_DRAW).

Some of these notifications, like draw, are useful to override in scripts. So much so that Godot exposes many of them with dedicated functions:

_ready(): NOTIFICATION_READY

_enter_tree(): NOTIFICATION_ENTER_TREE

_exit_tree(): NOTIFICATION_EXIT_TREE

_process(delta): NOTIFICATION_PROCESS

_physics_process(delta): NOTIFICATION_PHYSICS_PROCESS

_draw(): NOTIFICATION_DRAW

What users might not realize is that notifications exist for types other than Node alone, for example:

Object::NOTIFICATION_POSTINITIALIZE: a callback that triggers during object initialization. Not accessible to scripts.

Object::NOTIFICATION_PREDELETE: a callback that triggers before the engine deletes an Object, i.e. a "destructor".

And many of the callbacks that do exist in Nodes don't have any dedicated methods, but are still quite useful.

Node::NOTIFICATION_PARENTED: a callback that triggers anytime one adds a child node to another node.

Node::NOTIFICATION_UNPARENTED: a callback that triggers anytime one removes a child node from another node.

One can access all these custom notifications from the universal _notification() method.

Methods in the documentation labeled as "virtual" are also intended to be overridden by scripts.

A classic example is the _init method in Object. While it has no NOTIFICATION_* equivalent, the engine still calls the method. Most languages (except C#) rely on it as a constructor.

So, in which situation should one use each of these notifications or virtual functions?

Use _process() when one needs a framerate-dependent delta time between frames. If code that updates object data needs to update as often as possible, this is the right place. Recurring logic checks and data caching often execute here, but it comes down to the frequency at which one needs the evaluations to update. If they don't need to execute every frame, then implementing a Timer-timeout loop is another option.

Use _physics_process() when one needs a framerate-independent delta time between frames. If code needs consistent updates over time, regardless of how fast or slow time advances, this is the right place. Recurring kinematic and object transform operations should execute here.

While it is possible, to achieve the best performance, one should avoid making input checks during these callbacks. _process() and _physics_process() will trigger at every opportunity (they do not "rest" by default). In contrast, *_input() callbacks will trigger only on frames in which the engine has actually detected the input.

One can check for input actions within the input callbacks just the same. If one wants to use delta time, one can fetch it from the related delta time methods as needed.

If the script initializes its own node subtree, without a scene, that code should execute in _init(). Other property or SceneTree-independent initializations should also run here.

The C# equivalent to GDScript's _init() method is the constructor.

_init() triggers before _enter_tree() or _ready(), but after a script creates and initializes its properties. When instantiating a scene, property values will set up according to the following sequence:

Initial value assignment: the property is assigned its initialization value, or its default value if one is not specified. If a setter exists, it is not used.

_init() assignment: the property's value is replaced by any assignments made in _init(), triggering the setter.

Exported value assignment: an exported property's value is again replaced by any value set in the Inspector, triggering the setter.

As a result, instantiating a script versus a scene may affect both the initialization and the number of times the engine calls the setter.

When instantiating a scene connected to the first executed scene, Godot will instantiate nodes down the tree (making _init() calls) and build the tree going downwards from the root. This causes _enter_tree() calls to cascade down the tree. Once the tree is complete, leaf nodes call _ready. A node will call this method once all child nodes have finished calling theirs. This then causes a reverse cascade going up back to the tree's root.

When instantiating a script or a standalone scene, nodes are not added to the SceneTree upon creation, so no _enter_tree() callbacks trigger. Instead, only the _init() call occurs. When the scene is added to the SceneTree, the _enter_tree() and _ready() calls occur.

If one needs to trigger behavior that occurs as nodes parent to another, regardless of whether it occurs as part of the main/active scene or not, one can use the PARENTED notification. For example, here is a snippet that connects a node's method to a custom signal on the parent node without failing. Useful on data-centric nodes that one might create at runtime.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# Allows for recurring operations that don't trigger script logic
# every frame (or even every fixed frame).
func _ready():
    var timer = Timer.new()
    timer.autostart = true
    timer.wait_time = 0.5
    add_child(timer)
    timer.timeout.connect(func():
        print("This block runs every 0.5 seconds")
    )
```

Example 2 (gdscript):
```gdscript
using Godot;

public partial class MyNode : Node
{
    // Allows for recurring operations that don't trigger script logic
    // every frame (or even every fixed frame).
    public override void _Ready()
    {
        var timer = new Timer();
        timer.Autostart = true;
        timer.WaitTime = 0.5;
        AddChild(timer);
        timer.Timeout += () => GD.Print("This block runs every 0.5 seconds");
    }
}
```

Example 3 (php):
```php
using namespace godot;

class MyNode : public Node {
    GDCLASS(MyNode, Node)

public:
    // Allows for recurring operations that don't trigger script logic
    // every frame (or even every fixed frame).
    virtual void _ready() override {
        Timer *timer = memnew(Timer);
        timer->set_autostart(true);
        timer->set_wait_time(0.5);
        add_child(timer);
        timer->connect("timeout", callable_mp(this, &MyNode::run));
    }

    void run() {
        UtilityFunctions::print("This block runs every 0.5 seconds.");
    }
};
```

Example 4 (gdscript):
```gdscript
# Called every frame, even when the engine detects no input.
func _process(delta):
    if Input.is_action_just_pressed("ui_select"):
        print(delta)

# Called during every input event.
func _unhandled_input(event):
    match event.get_class():
        "InputEventKey":
            if Input.is_action_just_pressed("ui_accept"):
                print(get_process_delta_time())
```

---

## Project organization — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html

**Contents:**
- Project organization
- Introduction
- Organization
- Style guide
- Importing
  - Ignoring specific folders
- Case sensitivity
- User-contributed notes

Since Godot has no restrictions on project structure or filesystem usage, organizing files when learning the engine can seem challenging. This tutorial suggests a workflow which should be a good starting point. We will also cover using version control with Godot.

Godot is scene-based in nature, and uses the filesystem as-is, without metadata or an asset database.

Unlike other engines, many resources are contained within the scene itself, so the amount of files in the filesystem is considerably lower.

Considering that, the most common approach is to group assets as close to scenes as possible; when a project grows, it makes it more maintainable.

As an example, one can usually place into a single folder their basic assets, such as sprite images, 3D model meshes, materials, and music, etc. They can then use a separate folder to store built levels that use them.

For consistency across projects, we recommend following these guidelines:

Use snake_case for folder and file names (with the exception of C# scripts). This sidesteps case sensitivity issues that can crop up after exporting a project on Windows. C# scripts are an exception to this rule, as the convention is to name them after the class name which should be in PascalCase.

Use PascalCase for node names, as this matches built-in node casing.

In general, keep third-party resources in a top-level addons/ folder, even if they aren't editor plugins. This makes it easier to track which files are third-party. There are some exceptions to this rule; for instance, if you use third-party game assets for a character, it makes more sense to include them within the same folder as the character scenes and scripts.

Godot versions prior to 3.0 did the import process from files outside the project. While this can be useful in large projects, it resulted in an organization hassle for most developers.

Because of this, assets are now transparently imported from within the project folder.

To prevent Godot from importing files contained in a specific folder, create an empty file called .gdignore in the folder (the leading . is required). This can be useful to speed up the initial project importing.

To create a file whose name starts with a dot on Windows, place a dot at both the beginning and end of the filename (".gdignore."). Windows will automatically remove the trailing dot when you confirm the name.

Alternatively, you can use a text editor such as Notepad++ or use the following command in a command prompt: type nul > .gdignore

Once the folder is ignored, resources in that folder can't be loaded anymore using the load() and preload() methods. Ignoring a folder will also automatically hide it from the FileSystem dock, which can be useful to reduce clutter.

Note that the .gdignore file's contents are ignored, which is why the file should be empty. It does not support patterns like .gitignore files do.

Windows and recent macOS versions use case-insensitive filesystems by default, whereas Linux distributions use a case-sensitive filesystem by default. This can cause issues after exporting a project, since Godot's PCK virtual filesystem is case-sensitive. To avoid this, it's recommended to stick to snake_case naming for all files in the project (and lowercase characters in general).

You can break this rule when style guides say otherwise (such as the C# style guide). Still, be consistent to avoid mistakes.

On Windows 10, to further avoid mistakes related to case sensitivity, you can also make the project folder case-sensitive. After enabling the Windows Subsystem for Linux feature, run the following command in a PowerShell window:

If you haven't enabled the Windows Subsystem for Linux, you can enter the following line in a PowerShell window running as Administrator then reboot when asked:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
/project.godot
/docs/.gdignore  # See "Ignoring specific folders" below
/docs/learning.html
/models/town/house/house.dae
/models/town/house/window.png
/models/town/house/door.png
/characters/player/cubio.dae
/characters/player/cubio.png
/characters/enemies/goblin/goblin.dae
/characters/enemies/goblin/goblin.png
/characters/npcs/suzanne/suzanne.dae
/characters/npcs/suzanne/suzanne.png
/levels/riverdale/riverdale.scn
```

Example 2 (jsx):
```jsx
# To enable case-sensitivity:
fsutil file setcasesensitiveinfo <path to project folder> enable

# To disable case-sensitivity:
fsutil file setcasesensitiveinfo <path to project folder> disable
```

Example 3 (unknown):
```unknown
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

---

## Version control systems — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html

**Contents:**
- Version control systems
- Introduction
- Version control plugins
  - Official Git plugin
- Files to exclude from VCS
- Working with Git on Windows
- Git LFS
- User-contributed notes

Godot aims to be VCS-friendly and generate mostly readable and mergeable files.

Godot also supports the use of version control systems in the editor itself. However, version control in the editor requires a plugin for the specific VCS you're using.

As of July 2023, there is only a Git plugin available, but the community may create additional VCS plugins.

Using Git from inside the editor is supported with an official plugin. You can find the latest releases on GitHub.

Documentation on how to use the Git plugin can be found on its wiki.

This lists files and folders that should be ignored from version control in Godot 4.1 and later.

The list of files of folders that should be ignored from version control in Godot 3.x and Godot 4.0 is entirely different. This is important, as Godot 3.x and 4.0 may store sensitive credentials in export_presets.cfg (unlike Godot 4.1 and later).

If you are using Godot 3, check the 3.5 version of this documentation page instead.

There are some files and folders Godot automatically creates when opening a project in the editor for the first time. To avoid bloating your version control repository with generated data, you should add them to your VCS ignore:

.godot/: This folder stores various project cache data.

*.translation: These files are binary imported translations generated from CSV files.

You can make the Godot project manager generate version control metadata for you automatically when creating a project. When choosing the Git option, this creates .gitignore and .gitattributes files in the project root:

Creating version control metadata in the project manager's New Project dialog

In existing projects, select the Project menu at the top of the editor, then choose Version Control > Generate Version Control Metadata. This creates the same files as if the operation was performed in the project manager.

Most Git for Windows clients are configured with the core.autocrlf set to true. This can lead to files unnecessarily being marked as modified by Git due to their line endings being converted from LF to CRLF automatically.

It is better to set this option as:

Creating version control metadata using the project manager or editor will automatically enforce LF line endings using the .gitattributes file. In this case, you don't need to change your Git configuration.

Git LFS (Large File Storage) is a Git extension that allows you to manage large files in your repository. It replaces large files with text pointers inside Git, while storing the file contents on a remote server. This is useful for managing large assets, such as textures, audio files, and 3D models, without bloating your Git repository.

When using Git LFS you will want to ensure it is setup before you commit any files to your repository. If you have already committed files to your repository, you will need to remove them from the repository and re-add them after setting up Git LFS.

It is possible to use git lfs migrate to convert existing files in your repository, but this is more in-depth and requires a good understanding of Git.

A common approach is setting up a new repository with Git LFS (and a proper .gitattributes), then copying the files from the old repository to the new one. This way, you can ensure that all files are tracked by LFS from the start.

To use Git LFS with Godot, you need to install the Git LFS extension and configure it to track the file types you want to manage. You can do this by running the following command in your terminal:

This will create a .gitattributes file in your repository that tells Git to use LFS for the specified file types. You can add more file types by modifying the .gitattributes file. For example, to track all GLB files, you can do this by running the following command in your terminal:

When you add or modify files that are tracked by LFS, Git will automatically store them in LFS instead of the regular Git history. You can push and pull LFS files just like regular Git files, but keep in mind that LFS files are stored separately from the rest of your Git history. This means that you may need to install Git LFS on any machine that you clone the repository to in order to access the LFS files.

Below is an example .gitattributes file that you can use as a starting point for Git LFS. These file types were chosen because they are commonly used, but you can modify the list to include any binary types you may have in your project.

For more information on Git LFS, check the official documentation: https://git-lfs.github.com/ and https://docs.github.com/en/repositories/working-with-files/managing-large-files.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
git config --global core.autocrlf input
```

Example 2 (unknown):
```unknown
git lfs install
```

Example 3 (unknown):
```unknown
git lfs track "*.glb"
```

Example 4 (markdown):
```markdown
# Normalize EOL for all files that Git considers text files.
* text=auto eol=lf

# Git LFS Tracking (Assets)

# 3D Models
*.fbx filter=lfs diff=lfs merge=lfs -text
*.gltf filter=lfs diff=lfs merge=lfs -text
*.glb filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text

# Images
*.png filter=lfs diff=lfs merge=lfs -text
*.svg filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
*.tga filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text
*.exr filter=lfs diff=lfs merge=lfs -text
*.hdr filter=lfs diff=lfs merge=lfs -text
*.dds filter=lfs diff=lfs merge=lfs -text

# Audio
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text

# Font & Icon
*.ttf filter=lfs diff=lfs merge=lfs -text
*.otf filter=lfs diff=lfs merge=lfs -text
*.ico filter=lfs diff=lfs merge=lfs -text

# Godot LFS Specific
*.scn filter=lfs diff=lfs merge=lfs -text
*.res filter=lfs diff=lfs merge=lfs -text
*.material filter=lfs diff=lfs merge=lfs -text
*.anim filter=lfs diff=lfs merge=lfs -text
*.mesh filter=lfs diff=lfs merge=lfs -text
*.lmbake filter=lfs diff=lfs merge=lfs -text
```

---

## Troubleshooting — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/troubleshooting.html

**Contents:**
- Troubleshooting
- The editor runs slowly and uses all my CPU and GPU resources, making my computer noisy
- The editor stutters and flickers on my variable refresh rate monitor (G-Sync/FreeSync)
- The editor or project takes a very long time to start
- The Godot editor appears frozen after clicking the system console
- The Godot editor's macOS dock icon gets duplicated every time it is manually moved
- Some text such as "NO DC" appears in the top-left corner of the Project Manager and editor window
- A microphone or "refresh" icon appears in the bottom-right corner of the Project Manager and editor window
- The editor or project appears overly sharp or blurry
- The editor or project appears to have washed out colors

This page lists common issues encountered when using Godot and possible solutions.

See Using the Web editor for caveats specific to the Web version of the Godot editor.

This is a known issue, especially on macOS since most Macs have Retina displays. Due to Retina displays' higher pixel density, everything has to be rendered at a higher resolution. This increases the load on the GPU and decreases perceived performance.

There are several ways to improve performance and battery life:

In 3D, click the Perspective button in the top left corner and enable Half Resolution. The 3D viewport will now be rendered at half resolution, which can be up to 4 times faster.

Open the Editor Settings and increase the value of Low Processor Mode Sleep (µsec) to 33000 (30 FPS). This value determines the amount of microseconds between frames to render. Higher values will make the editor feel less reactive, but will help decrease CPU and GPU usage significantly.

If you have a node that causes the editor to redraw continuously (such as particles), hide it and show it using a script in the _ready() method. This way, it will be hidden in the editor, but will still be visible in the running project.

This is a known issue. Variable refresh rate monitors need to adjust their gamma curves continuously to emit a consistent amount of light over time. This can cause flicker to appear in dark areas of the image when the refresh rate varies a lot, which occurs as the Godot editor only redraws when necessary.

There are several workarounds for this:

Enable Interface > Editor > Update Continuously in the Editor Settings. Keep in mind this will increase power usage and heat/noise emissions since the editor will now be rendering constantly, even if nothing has changed on screen. To alleviate this, you can increase Low Processor Mode Sleep (µsec) to 33000 (30 FPS) in the Editor Settings. This value determines the amount of microseconds between frames to render. Higher values will make the editor feel less reactive, but will help decrease CPU and GPU usage significantly.

Alternatively, disable variable refresh rate on your monitor or in the graphics driver.

VRR flicker can be reduced on some displays using the VRR Control or Fine Tune Dark Areas options in your monitor's OSD. These options may increase input lag or result in crushed blacks.

If using an OLED display, use the Black (OLED) editor theme preset in the Editor Settings. This hides VRR flicker thanks to OLED's perfect black levels.

When using one of the Vulkan-based renderers (Forward+ or Mobile), the first startup is expected to be relatively long. This is because shaders need to be compiled before they can be cached. Shaders also need to be cached again after updating Godot, after updating graphics drivers or after switching graphics cards.

If the issue persists after the first startup, this is a known bug on Windows when you have specific USB peripherals connected. In particular, Corsair's iCUE software seems to cause this bug. Try updating your USB peripherals' drivers to their latest version. If the bug persists, you need to disconnect the specific peripheral before opening the editor. You can then connect the peripheral again.

Firewall software such as Portmaster may also cause the debug port to be blocked. This causes the project to take a long time to start, while being unable to use debugging features in the editor (such as viewing print() output). You can work this around by changing the debug port used by the project in the Editor Settings (Network > Debug > Remote Port). The default is 6007; try another value that is greater than 1024, such as 7007.

On Windows, when loading the project for the first time after the PC is turned on, Windows Defender will cause the filesystem cache validation on project startup to take significantly longer. This is especially noticeable in projects with a large number of files. Consinder adding the project folder to the list of exclusions by going to Virus & threat protection > Virus & threat protection settings > Add or remove exclusions.

When running Godot on Windows with the system console enabled, you can accidentally enable selection mode by clicking inside the command window. This Windows-specific behavior pauses the application to let you select text inside the system console. Godot cannot override this system-specific behavior.

To solve this, select the system console window and press Enter to leave selection mode.

If you open the Godot editor and manually change the position of the dock icon, then restart the editor, you will get a duplicate dock icon all the way to the right of the dock.

This is due to a design limitation of the macOS dock. The only known way to resolve this would be to merge the project manager and editor into a single process, which means the project manager would no longer spawn a separate process when starting the editor. While using a single process instance would bring several benefits, it isn't planned to be done in the near future due to the complexity of the task.

To avoid this issue, keep the Godot editor's dock icon at its default location as created by macOS.

This is caused by the NVIDIA graphics driver injecting an overlay to display information.

To disable this overlay on Windows, restore your graphics driver settings to the default values in the NVIDIA Control Panel.

To disable this overlay on Linux, open nvidia-settings, go to X Screen 0 > OpenGL Settings then uncheck Enable Graphics API Visual Indicator.

This is caused by the NVIDIA graphics driver injecting an overlay to display instant replay information on ShadowPlay recording. This overlay can only be seen on Windows, as Linux does not have support for ShadowPlay.

To disable this overlay, press Alt + Z (default shortcut for the NVIDIA overlay) and disable Settings > HUD Layout > Status Indicator in the NVIDIA overlay.

Alternatively, you can install the new NVIDIA app <https://www.nvidia.com/en-us/software/nvidia-app/> which replaces GeForce Experience and does not suffer from this issue. Unlike GeForce Experience, the NVIDIA app draws the replay indicator in the corner of the screen as opposed to the corner of each window.

Correct appearance (left), oversharpened appearance due to graphics driver sharpening (right)

If the editor or project appears overly sharp, this is likely due to image sharpening being forced on all Vulkan or OpenGL applications by your graphics driver. You can disable this behavior in the graphics driver's control panel:

NVIDIA (Windows): Open the start menu and choose NVIDIA Control Panel. Open the Manage 3D settings tab on the left. In the list in the middle, scroll to Image Sharpening and set it to Sharpening Off.

AMD (Windows): Open the start menu and choose AMD Software. Click the settings "cog" icon in the top-right corner. Go to the Graphics tab then disable Radeon Image Sharpening.

If the editor or project appears overly blurry, this is likely due to FXAA being forced on all Vulkan or OpenGL applications by your graphics driver.

NVIDIA (Windows): Open the start menu and choose NVIDIA Control Panel. Open the Manage 3D settings tab on the left. In the list in the middle, scroll to Fast Approximate Antialiasing and set it to Application Controlled.

NVIDIA (Linux): Open the applications menu and choose NVIDIA X Server Settings. Select to Antialiasing Settings on the left, then uncheck Enable FXAA.

AMD (Windows): Open the start menu and choose AMD Software. Click the settings "cog" icon in the top-right corner. Go to the Graphics tab, scroll to the bottom and click Advanced to unfold its settings. Disable Morphological Antialiasing.

Third-party vendor-independent utilities such as vkBasalt may also force sharpening or FXAA on all Vulkan applications. You may want to check their configuration as well.

After changing options in the graphics driver or third-party utilities, restart Godot to make the changes effective.

If you still wish to force sharpening or FXAA on other applications, it's recommended to do so on a per-application basis using the application profiles system provided by graphics drivers' control panels.

On Windows, this is usually caused by incorrect OS or monitor settings, as Godot currently does not support HDR output (even though it may internally render in HDR).

As most displays are not designed to display SDR content in HDR mode, it is recommended to disable HDR in the Windows settings when not running applications that use HDR output. On Windows 11, this can be done by pressing Windows + Alt + B (this shortcut is part of the Xbox Game Bar app). To toggle HDR automatically based on applications currently running, you can use AutoActions.

If you insist on leaving HDR enabled, it is possible to somewhat improve the result by ensuring the display is configured to use HGIG tonemapping (as opposed to DTM), then using the Windows HDR calibration app. It is also strongly recommended to use Windows 11 instead of Windows 10 when using HDR. The end result will still likely be inferior to disabling HDR on the display, though.

Support for HDR output is planned in a future release.

This is a known issue on Linux with NVIDIA graphics when using the proprietary driver. There is no definitive fix yet, as suspend on Linux + NVIDIA is often buggy when OpenGL or Vulkan is involved. The Compatibility rendering method (which uses OpenGL) is generally less prone to suspend-related issues compared to the Forward+ and Mobile renderers (which use Vulkan).

The NVIDIA driver offers an experimental option to preserve video memory after suspend which may resolve this issue. This option has been reported to work better with more recent NVIDIA driver versions.

To avoid losing work, save scenes in the editor before putting the PC to sleep.

This is usually caused by forgetting to specify a filter for non-resource files in the Export dialog. By default, Godot will only include actual resources into the PCK file. Some files commonly used, such as JSON files, are not considered resources. For example, if you load test.json in the exported project, you need to specify *.json in the non-resource export filter. See Resource options for more information.

Also, note that files and folders whose names begin with a period will never be included in the exported project. This is done to prevent version control folders like .git from being included in the exported PCK file.

On Windows, this can also be due to case sensitivity issues. If you reference a resource in your script with a different case than on the filesystem, loading will fail once you export the project. This is because the virtual PCK filesystem is case-sensitive, while Windows's filesystem is case-insensitive by default.

This could be caused by a number of things such as an editor plugin, GDExtension addon, or something else. In this scenario it's recommended that you open the project in recovery mode, and attempt to find and fix whatever is causing the crashes. See the Project Manager page for more information.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using the Project Manager — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/project_manager.html

**Contents:**
- Using the Project Manager
- Creating and importing projects
  - Using the file browser
- Opening and importing projects
- Downloading demos and templates
- Managing projects with tags
- Recovery Mode
- User-contributed notes

When you launch Godot, the first window you see is the Project Manager. It lets you create, remove, import, or play game projects:

To change the editors language click on the Settings Button in the top right corner:

In Project Manager Settings, you can change the interface language from the language dropdown menu, which is the system default language by default.

You can also change the theme of the editor, the display scale for different interface element sizes, and the availability of online functionality using network mode. If network mode is online, Godot will also check and inform you about new versions of Godot.

The directory naming convention can also be changed to replace spaces according to the chosen format when creating folders automatically.

To create a new project:

Click the Create button on the top-left of the window.

Give the project a name, then open the file browser using the Browse button, and choose an empty folder on your computer to save the files. Alternatively, you can enable Create Folder option to automatically create a new sub-folder with the project name, following the directory naming convention set in the settings. An empty folder will show a green tick on the right.

Select one of the renderers (this can also be changed later).

Click the Create & Edit button to create the project folder and open it in the editor.

You can optionally choose a version control system. Currently, only git is supported and it needs the Godot Git Plugin to be installed, either manually or using the Asset Library. To learn more about the Godot Git Plugin, see its wiki.

From the Create New Project window, click the Browse button to open Godot's file browser. You can pick a location or type the folder's path in the Path field, after choosing a drive.

Left of the path field on the top row contains arrows to navigate backward and forward through the last visited locations. The up arrow navigates to parent folder. On the right side of the path field, there are buttons to refresh the current folder's contents, favorite/unfavorite the current folder, and show/hide hidden folders.

Next, the buttons to switch the display type of the folders and files between grid view and list view are seen.

The last button on the right will create a new folder.

Favorited folders will be displayed on the left side under the Favorites section. You can sort the favorites using the up and down buttons in this section. Last chosen folders will be listed under the Recent list.

The next time you open the Project Manager, you'll see your new project in the list. Double click on it to open it in the editor.

You can similarly import existing projects using the Import button. Locate the folder that contains the project or the project.godot file to import and edit it.

Alternatively, it is possible to choose a zip file to be automatically extracted by Godot.

When the folder path is correct, you'll see a green checkmark.

From the Asset Library tab you can download open source project templates and demos from the Asset Library to help you get started faster.

The first time you open this tab you'll notice that it's asking you to go online. For privacy reasons the project manager, and Godot editor, can't access the internet by default. To enable accessing the internet click the Go Online button. This will also allow project manager to notify you about updates. If you wish to turn this off in the future go into project manager settings and change Network Mode to "Offline"

Now that Godot is connected to the internet you can download a demo or template, to do this:

On the page that opens, click the download button.

Once it finished downloading, click install and choose where you want to save the project.

For users with a lot of projects on one PC it can be a lot to keep track of. To aid in this Godot allows you to create project tags. To add a tag to a project click on the project in the project manager, then click on the Manage Tags button

This will open up the manage project tags window. To add a tag click the plus button.

Type out the tag name, and click OK. Your project will now have a tag added to it. These tags can be used for any other project in your project manager.

To show projects with a specific tag only, you can click on the tags or write tag: and type the tag you would like to search for in the filter bar. To limit the results using multiple tags, you can click on another tag or add tag: after a space and type another tag in the filter bar.

In addition, tags will stay with projects. So if you tag your project, send it to another machine, and import it into the project manager you will see the tags you created.

To remove a tag from your project manager it must be removed from all the projects it's used by. Once that's done close the project manager, open it up again, and the tag should be gone.

If a project is immediately crashing on startup, or crashing frequently during editing it can be opened in recovery mode, to attempt to make it more stable while looking for the source of the crashing to fix it.

Usually a project should open in recovery mode automatically when you re-open it after a crash. If it doesn't you can manually open recovery mode by selecting the project in the project manager, to do that select the project from your list of projects, click the dropdown button next to the edit node, and select Edit in recovery mode.

While in recovery mode the following are disabled:

Automatic scene restoring

It is recommended that you backup your project before editing it in recovery mode.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Inspector Dock — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/inspector_dock.html

**Contents:**
- Inspector Dock
- Usage
- User-contributed notes

The Inspector dock lists all properties of an object, resource, or node. It will update the list of the properties as you select a different node from the Scene Tree dock, or if you use Open command from the FileSystem's context menu.

This page explains how the Inspector dock works in-depth. You will learn how to edit properties, fold and unfold areas, use the search bar, and more.

If the inspector dock is visible, clicking on a node in the scene tree will automatically display its properties. If it is not visible, you can show it by navigating to Editor > Editor Docks > Inspector.

At the top of the dock are the file and navigation buttons.

Opens a new window to select and create a resource in the memory and edit it.

Opens a resource from the FileSystem to edit.

Saves the currently edited resource to disk.

Edit Resource from Clipboard by pasting the copied resource.

Copy Resource to clipboard.

Show in FileSystem if the resource is already saved.

Make Resource Built-In to work in a built-in resource, not the one from the disk.

The "<" and ">" arrows let you navigate through your edited object history.

The button next to them opens the history list for a quicker navigation. If you created multiple resources in the memory, you will also see them here.

Below, you can find the selected node's icon, its name, and the quick button to open its documentation on the right side. Clicking on the node's name itself will list the sub-resources of this node if there are any.

Then comes the search bar. Type anything in it to filter displayed properties. Delete the text to clear the search. This search is case insensitive and also searches letter by letter as you type. For instance, if you type vsb, one of the results you see will be Visibility property as this property contains all of these letters.

Before discussing the tool button next to the filter bar, it is worth mentioning what you actually see below it and how it is structured.

Properties are grouped inside their respective classes as sections. You can expand each section to view the related properties.

You can also open the documentation of each class by right-clicking on a class and selecting Open Documentation. Similarly, you can right click on a property and copy or paste its value, copy the property path, favorite it to be shown on the top of the inspector, or open its documentation page.

If you hover your mouse over a property, you will see the description of what it does as well as how it can be called inside the script.

You can directly change the values by clicking, typing, or selecting from the menu. If the property is a number or a slider, you can keep your left mouse button pressed and drag to change the values.

If a node's property is a sub-resource, you can click on the down arrow to pick a resource type, or load one using the Quick Load or Load options. Alternatively, a supported resource can be dragged from the FileSystem. Once you start dragging, the compatible property will be highlighted. Simply drop it on the appropriate property's value.

After loading a sub-resource, you can click on it to see its properties or adjust them.

The values with different values than their original values will have a revert icon (). Clicking on this icon reverts the value to its original state. If the values are linked with each other, they will have a chain icon and changing one will change others as well. You can unchain them by clicking on this icon.

If you are changing a property a lot, you may consider favoriting it by right-clicking and choosing Favorite Property. This will show it at the top of the inspector for all objects of this class.

Now that we have a better understanding of the terms, we can proceed with the tool menu. If you click the tool menu icon next to the filter bar, a drop-down menu will offer various view and edit options.

Expand All: Expands all sections showing all available properties.

Collapse All: Collapses all properties showing only classes and the sections.

Expand Non-Default: Only expands the sections where the original value is different than the current value (the properties with a revert icon ()).

Property Name Style: This section determines how the properties' text is displayed in the inspector. Raw uses the property's own naming, Capitalized uses title case by changing the initial letters of each word to uppercase and removing underscores, Localized displays the translation of the properties if you are using the Editor in a language other than English.

Copy Properties: Copies all properties of the current node with their current values.

Paste Properties: Pastes the copied properties from the clipboard. Useful to apply the common properties of one node to another.

Make Sub-Resources Unique: By default, a duplicated node shares the sub-resources of the original node. Changing one parameter of the sub-resource in one node, affects the other one. Clicking this option makes each sub-resource used in this node unique, separated from other nodes.

If a node has exported variables in its attached script, you will also see these in the inspector. The first image in this section has one for the Player node: Action Suffix. See GDScript exported properties for more on this topic.

Refer to Customizing the interface for dock customization options.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Project Settings — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/project_settings.html

**Contents:**
- Project Settings
- Changing project settings
  - Changing project settings from code
- Reading project settings
- Manually editing project.godot
- Advanced project settings
- User-contributed notes

There are dozens of settings you can change to control a project's execution, including physics, rendering, and windowing settings. These settings can be changed from the Project Settings window, from code, or by manually editing the project.godot file. You can see a full list of settings in the ProjectSettings class.

Internally, Godot stores the settings for a project in a project.godot file, a plain text file in INI format. While this is human-readable and version control friendly, it's not the most convenient to edit. For that reason, the Project Settings window is available to edit these settings. To open the Project Settings, select Project > Project Settings from the main menu.

The Project Settings window

The Project Settings window is mainly used to change settings in the General tab. Additionally, there are tabs for the Input Map, Localization, Globals, Plugins, and Import Defaults. Usage of these other tabs is documented elsewhere.

The General tab of the project settings window works much like the inspector. It displays a list of project settings which you can change, just like inspector properties. There is a list of categories on the left, which you can use to select related groups of settings. You can also search for a specific setting with the Filter Settings field.

Each setting has a default value. Settings can be reset to their default values by clicking the circular arrow Reset button next to each property.

You can use set_setting() to change a setting's value from code:

However, many project settings are only read once when the game starts. After that, changing the setting with set_setting() will have no effect. Instead, most settings have a corresponding property or method on a runtime class like Engine or DisplayServer:

In general, project settings are duplicated at runtime in the Engine, PhysicsServer2D, PhysicsServer3D, RenderingServer, Viewport, or Window classes. In the ProjectSettings class reference, settings links to their equivalent runtime property or method.

You can read project settings with get_setting() or get_setting_with_override():

Since many project settings are only read once at startup, the value in the project settings may no longer be accurate. In these cases, it's better to read the value from the runtime equivalent property or method:

You can open the project.godot file using a text editor and manually change project settings. Note that if the project.godot file does not have a stored value for a particular setting, it is implicitly the default value of that setting. This means that if you are manually editing the file, you may have to write in both the setting name and the value.

In general, it is recommended to use the Project Settings window rather than manually edit project.godot.

The advanced project settings

By default, only some project settings are shown. To see all the project settings, enable the Advanced Settings toggle.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
ProjectSettings.set_setting("application/run/max_fps", 60)
ProjectSettings.set_setting("display/window/size/mode", DisplayServer.WINDOW_MODE_WINDOWED)
```

Example 2 (unknown):
```unknown
ProjectSettings.SetSetting("application/run/max_fps", 60);
ProjectSettings.SetSetting("display/window/size/mode", (int)DisplayServer.WindowMode.Windowed);
```

Example 3 (unknown):
```unknown
Engine.max_fps = 60
DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
```

Example 4 (unknown):
```unknown
Engine.MaxFps = 60;
DisplayServer.WindowSetMode(DisplayServer.WindowMode.Windowed);
```

---

## Default editor shortcuts — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/default_key_mapping.html

**Contents:**
- Default editor shortcuts
- General editor actions
- Bottom panels
- 2D / CanvasItem editor
- 3D / Spatial editor
- Text editor
- Script editor
- Editor output
- Debugger
- File dialog

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Many Godot editor functions can be executed with keyboard shortcuts. This page lists functions which have associated shortcuts by default, but many others are available for customization in editor settings as well. To change keys associated with these and other actions navigate to Editor > Editor Settings > Shortcuts.

While some actions are universal, a lot of shortcuts are specific to individual tools. For this reason it is possible for some key combinations to be assigned to more than one function. The correct action will be performed depending on the context.

While Windows and Linux builds of the editor share most of the default settings, some shortcuts may differ for macOS version. This is done for better integration of the editor into macOS ecosystem. Users fluent with standard shortcuts on that OS should find Godot Editor's default key mapping intuitive.

Distraction Free Mode

editor/distraction_free_mode

editor/reopen_closed_scene

Ctrl + Shift + Alt + S

Cmd + Shift + Opt + S

editor/save_all_scenes

editor/quick_open_scene

editor/quick_open_script

editor/quit_to_project_list

editor/take_screenshot

editor/fullscreen_mode

editor/play_custom_scene

editor/bottom_panel_expand

editor/command_palette

Only bottom panels that are always available have a default shortcut assigned. Others must be manually bound in the Editor Settings if desired.

Toggle Last Opened Panel

editor/toggle_last_opened_bottom_panel

Toggle Animation Bottom Panel

bottom_panels/toggle_animation_bottom_panel

Toggle Audio Bottom Panel

bottom_panels/toggle_audio_bottom_panel

Toggle Debugger Bottom Panel

bottom_panels/toggle_debugger_bottom_panel

Toggle FileSystem Bottom Panel

bottom_panels/toggle_filesystem_bottom_panel

Toggle Output Bottom Panel

bottom_panels/toggle_output_bottom_panel

Toggle Shader Editor Bottom Panel

bottom_panels/toggle_shader_editor_bottom_panel

canvas_item_editor/zoom_plus

canvas_item_editor/zoom_minus

canvas_item_editor/zoom_reset

canvas_item_editor/pan_view

canvas_item_editor/select_mode

canvas_item_editor/move_mode

canvas_item_editor/rotate_mode

canvas_item_editor/scale_mode

canvas_item_editor/ruler_mode

canvas_item_editor/use_smart_snap

canvas_item_editor/use_grid_snap

Multiply grid step by 2

canvas_item_editor/multiply_grid_step

Divide grid step by 2

canvas_item_editor/divide_grid_step

canvas_item_editor/show_grid

canvas_item_editor/show_helpers

canvas_item_editor/show_guides

canvas_item_editor/center_selection

canvas_item_editor/frame_selection

canvas_item_editor/preview_canvas_scale

canvas_item_editor/anim_insert_key

Insert Key (Existing Tracks)

canvas_item_editor/anim_insert_key_existing_tracks

Make Custom Bones from Nodes

canvas_item_editor/skeleton_make_bones

canvas_item_editor/anim_clear_pose

spatial_editor/freelook_toggle

spatial_editor/freelook_left

spatial_editor/freelook_right

spatial_editor/freelook_forward

spatial_editor/freelook_backwards

spatial_editor/freelook_up

spatial_editor/freelook_down

Freelook Speed Modifier

spatial_editor/freelook_speed_modifier

Freelook Slow Modifier

spatial_editor/freelook_slow_modifier

spatial_editor/tool_select

spatial_editor/tool_move

spatial_editor/tool_rotate

spatial_editor/tool_scale

spatial_editor/local_coords

spatial_editor/snap_to_floor

spatial_editor/top_view

spatial_editor/bottom_view

spatial_editor/front_view

spatial_editor/rear_view

spatial_editor/right_view

spatial_editor/left_view

Switch Perspective/Orthogonal View

spatial_editor/switch_perspective_orthogonal

spatial_editor/insert_anim_key

spatial_editor/focus_origin

spatial_editor/focus_selection

Align Transform with View

spatial_editor/align_transform_with_view

Align Rotation with View

spatial_editor/align_rotation_with_view

spatial_editor/1_viewport

spatial_editor/2_viewports

spatial_editor/2_viewports_alt

spatial_editor/3_viewports

spatial_editor/3_viewports_alt

spatial_editor/4_viewports

script_text_editor/cut

script_text_editor/copy

script_text_editor/paste

script_text_editor/select_all

script_text_editor/find

script_text_editor/find_next

script_text_editor/find_previous

script_text_editor/find_in_files

script_text_editor/replace

script_text_editor/replace_in_files

script_text_editor/undo

script_text_editor/redo

script_text_editor/move_up

script_text_editor/move_down

script_text_editor/delete_line

script_text_editor/toggle_comment

script_text_editor/toggle_fold_line

Ctrl + Alt + Down Arrow

Cmd + Shift + Down Arrow

script_text_editor/duplicate_lines

script_text_editor/duplicate_selection

Ctrl + Shift + Down Arrow

Shift + Opt + Down Arrow

common/ui_text_caret_add_below

Ctrl + Shift + Up Arrow

Shift + Opt + Up Arrow

common/ui_text_caret_add_above

Select Next Occurrence

common/ui_text_add_selection_for_next_occurrence

script_text_editor/complete_symbol

script_text_editor/evaluate_selection

Trim Trailing Whitespace

script_text_editor/trim_trailing_whitespace

script_text_editor/convert_to_uppercase

script_text_editor/convert_to_lowercase

script_text_editor/capitalize

Convert Indent to Spaces

script_text_editor/convert_indent_to_spaces

Convert Indent to Tabs

script_text_editor/convert_indent_to_tabs

script_text_editor/auto_indent

script_text_editor/toggle_bookmark

script_text_editor/goto_next_bookmark

Go to Previous Bookmark

script_text_editor/goto_previous_bookmark

script_text_editor/goto_function

script_text_editor/goto_line

script_text_editor/toggle_breakpoint

Remove All Breakpoints

script_text_editor/remove_all_breakpoints

Go to Next Breakpoint

script_text_editor/goto_next_breakpoint

Go to Previous Breakpoint

script_text_editor/goto_previous_breakpoint

script_text_editor/contextual_help

script_editor/find_next

script_editor/find_previous

script_editor/find_in_files

Shift + Alt + Up Arrow

Shift + Opt + Up Arrow

script_editor/window_move_up

Shift + Alt + Down Arrow

Shift + Opt + Down Arrow

script_editor/window_move_down

script_editor/next_script

script_editor/prev_script

script_editor/reopen_closed_script

Ctrl + Shift + Alt + S

Cmd + Shift + Opt + S

script_editor/save_all

script_editor/reload_script_soft

script_editor/history_previous

script_editor/history_next

script_editor/close_file

script_editor/run_file

script_editor/toggle_scripts_panel

script_editor/zoom_in

script_editor/zoom_out

script_editor/reset_zoom

file_dialog/go_forward

file_dialog/toggle_hidden_files

file_dialog/toggle_favorite

file_dialog/toggle_mode

file_dialog/create_folder

file_dialog/focus_path

file_dialog/move_favorite_up

file_dialog/move_favorite_down

filesystem_dock/copy_path

filesystem_dock/duplicate

filesystem_dock/delete

scene_tree/add_child_node

scene_tree/batch_rename

scene_tree/copy_node_path

scene_tree/delete_no_confirm

animation_editor/duplicate_selection

animation_editor/duplicate_selection_transposed

animation_editor/delete_selection

animation_editor/goto_next_step

animation_editor/goto_prev_step

tiles_editor/selection_tool

tiles_editor/paint_tool

tiles_editor/line_tool

tiles_editor/rect_tool

tiles_editor/bucket_tool

tiles_editor/flip_tile_horizontal

tiles_editor/flip_tile_vertical

tiles_editor/rotate_tile_left

tiles_editor/rotate_tile_right

tileset_editor/next_shape

tileset_editor/previous_shape

tileset_editor/editmode_region

tileset_editor/editmode_collision

tileset_editor/editmode_occlusion

tileset_editor/editmode_navigation

tileset_editor/editmode_bitmask

tileset_editor/editmode_priority

tileset_editor/editmode_icon

tileset_editor/editmode_z_index

project_manager/new_project

project_manager/import_project

project_manager/scan_projects

project_manager/edit_project

project_manager/run_project

project_manager/rename_project

project_manager/remove_project

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using the Android editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/using_the_android_editor.html

**Contents:**
- Using the Android editor
- Android devices support
- Runtime Permissions
- Tips & Tricks
- Limitations & known issues
- User-contributed notes

In 2023, we added an Android port of the editor that can be used to create, develop, and export 2D and 3D projects on Android devices.

The app can be downloaded from the Godot download page or from the Google Play Store.

The Android editor is in early access, while we continue to refine the experience. See Limitations & known issues below.

The Android editor requires devices running Android 5 Lollipop or higher, with at least OpenGL 3 support. This includes (not exhaustive):

Android tablets, foldables and large phones

Android-powered netbooks

Chromebooks supporting Android apps

All files access permission: Enables the editor to create, import, and read project files from any file locations on the device. Without this permission, the editor is still functional, but has limited access to the device's files and directories.

REQUEST_INSTALL_PACKAGES: Enables the editor to install exported project APKs.

RECORD_AUDIO: Requested when the audio/driver/enable_input project setting is enabled.

For the best experience and high level of productivity, connecting a bluetooth keyboard & mouse is recommended to interact with the Android editor. The Android editor supports all of the usual shortcuts and key mappings.

When interacting with keyboard & mouse, you can decrease the size of the scrollbar using the interface/touchscreen/increase_scrollbar_touch_area editor setting.

For 2D projects, the block coding plugin can provide a block-based visual alternative to composing scripts when lacking a connected hardware keyboard.

On smaller devices, enabling and using picture-in-picture (PiP) mode provides the ability to easily transition between the Editor and the Play window.

PiP can be enabled via the run/window_placement/play_window_pip_mode editor setting.

The run/window_placement/android_window editor setting can be used to specify whether the Play window should always launch in PiP mode.

Note: In PiP mode, the Play window does not have input access.

Syncing projects via Git can be done by downloading an Android Git client. We recommend the Termux terminal, an Android terminal emulator which provides access to common terminal utilities such Git and SSH.

Note: To use Git with the Termux terminal, you'll need to grant WRITE permission to the terminal. This can be done by running the following command from within the terminal: termux-setup-storage

GDExtension plugins work as expected, but require the plugin developer to provide native Android binaries.

Here are the known limitations and issues of the Android editor:

No gradle build support.

No support for Android plugins as they require gradle build support. GDExtensions plugins are supported.

No support for external script editors.

While available, the Vulkan Forward+ renderer is not recommended due to severe performance issues.

UX not optimized for Android phones form-factor.

Android Go devices lacks the All files access permission required for device read/write access. As a workaround, when using an Android Go device, it's recommended to create new projects only in the Android Documents or Downloads directories.

The editor doesn't properly resume when Don't keep activities is enabled in the Developer Options.

There is a bug with the Samsung keyboard that causes random input to be inserted when writing scripts. It's recommended to use the Google keyboard (Gboard) instead.

See the list of open issues on GitHub related to the Android editor for a list of known bugs.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using the Web editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/using_the_web_editor.html

**Contents:**
- Using the Web editor
- Browser support
- Limitations
- Importing a project
- Editing and running a project
- Where are my project files?
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

There is a Web editor you can use to work on new or existing projects.

The web editor is in a preliminary stage. While its feature set may be sufficient for educational purposes, it is currently not recommended for production work. See Limitations below.

The Web editor requires support for WebAssembly's SharedArrayBuffer. This is in turn required to support threading in the browser. The following desktop browsers support WebAssembly threading and can therefore run the web editor:

Opera and Safari are not supported yet. Safari may work in the future once proper threading support is added.

Mobile browsers are currently not supported.

The web editor only supports the Compatibility rendering method, as there is no stable way to run Vulkan applications on the web yet.

If you use Linux, due to poor Firefox WebGL performance, it's recommended to use a Chromium-based browser instead of Firefox.

Due to limitations on the Godot or Web platform side, the following features are currently missing:

No GDExtension support.

No debugging support. This means GDScript debugging/profiling, live scene editing, the Remote Scene tree dock and other features that rely on the debugger protocol will not work.

No project exporting. As a workaround, you can download the project source using Project > Tools > Download Project Source and export it using a native version of the Godot editor.

The editor won't warn you when closing the tab with unsaved changes.

No lightmap baking support. You can still use existing lightmaps if they were baked with a native version of the Godot editor (e.g. by importing an existing project).

The following features are unlikely to be supported due to inherent limitations of the Web platform:

No support for external script editors.

No support for Android one-click deploy.

See the list of open issues on GitHub related to the web editor for a list of known bugs.

To import an existing project, the current process is as follows:

Specify a ZIP file to preload on the HTML5 filesystem using the Preload project ZIP input.

Run the editor by clicking Start Godot editor. The Godot Project Manager should appear after 10-20 seconds. On slower machines or connections, loading may take up to a minute.

In the dialog that appears at the middle of the window, specify a name for the folder to create then click the Create Folder button (it doesn't have to match the ZIP archive's name).

Click Install & Edit and the project will open in the editor.

It's important to place the project folder somewhere in /home/web_user/. If your project folder is placed outside /home/web_user/, you will lose your project when closing the editor!

When you follow the steps described above, the project folder will always be located in /home/web_user/projects, keeping it safe.

Unlike the native version of Godot, the web editor is constrained to a single window. Therefore, it cannot open a new window when running the project. Instead, when you run the project by clicking the Run button or pressing F5, it will appear to "replace" the editor window.

The web editor offers an alternative way to deal with the editor and game windows (which are now "tabs"). You can switch between the Editor and Game tabs using the buttons on the top. You can also close the running game or editor by clicking the × button next to those tabs.

Due to browser security limitations, the editor will save the project files to the browser's IndexedDB storage. This storage isn't accessible as a regular folder on your machine, but is abstracted away in a database.

You can download the project files as a ZIP archive by using Project > Tools > Download Project Source. This can be used to export the project using a native Godot editor, since exporting from the web editor isn't supported yet.

In the future, it may be possible to use the HTML5 FileSystem API to store the project files on the user's filesystem as the native editor would do. However, this isn't implemented yet.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Command line tutorial — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html

**Contents:**
- Command line tutorial
- Command line reference
- Path
- Setting the project path
- Creating a project
- Running the editor
- Erasing a scene
- Running the game
- Debugging
- Exporting

Some developers like using the command line extensively. Godot is designed to be friendly to them, so here are the steps for working entirely from the command line. Given the engine relies on almost no external libraries, initialization times are pretty fast, making it suitable for this workflow.

On Windows and Linux, you can run a Godot binary in a terminal by specifying its relative or absolute path.

On macOS, the process is different due to Godot being contained within a .app bundle (which is a folder, not a file). To run a Godot binary from a terminal on macOS, you have to cd to the folder where the Godot application bundle is located, then run Godot.app/Contents/MacOS/Godot followed by any command line arguments. If you've renamed the application bundle from Godot to another name, make sure to edit this command line accordingly.

Available in editor builds, debug export templates and release export templates.

Available in editor builds and debug export templates only.

Only available in editor builds.

Note that unknown command line arguments have no effect whatsoever. The engine will not warn you when using a command line argument that doesn't exist with a given build type.

Display the list of command line options.

Display the version string.

Use verbose stdout mode.

Quiet mode, silences stdout messages. Errors are still displayed.

Do not print engine version and rendering method header on startup.

Separator for user-provided arguments. Following arguments are not used by the engine, but can be read from OS.get_cmdline_user_args().

Start the editor instead of running the scene.

-p, --project-manager

Start the Project Manager, even if a project is auto-detected.

"Start the editor in recovery mode, which disables features that can typically cause startup crashes, such as tool scripts, editor plugins, GDExtension addons, and others.

Start the editor debug server (<protocol>://<host/IP>[:<port>], e.g. tcp://127.0.0.1:6007)

Use the specified port for the GDScript Debug Adapter Protocol. Recommended port range [1024, 49151].

Use the specified port for the GDScript Language Server Protocol. Recommended port range [1024, 49151].

Quit after the first iteration.

Quit after the given number of iterations. Set to 0 to disable.

-l, --language <locale>

Use a specific locale. <locale> follows the format language_Script_COUNTRY_VARIANT where language is a 2 or 3-letter language code in lowercase and the rest is optional. See Locale codes for more details.

Path to a project (<directory> must contain a 'project.godot' file).

Path or UID of a scene in the project that should be started.

Scan folders upwards for 'project.godot' file.

Path to a pack (.pck) file to load.

--render-thread <mode>

Render thread mode ('unsafe', 'safe', 'separate'). See Thread Model for more details.

--remote-fs <address>

Remote filesystem (<host/IP>[:<port>] address).

--remote-fs-password <password>

Password for remote filesystem.

--audio-driver <driver>

Audio driver. Use --help first to display the list of available drivers.

--display-driver <driver>

Display driver (and rendering driver). Use --help first to display the list of available drivers.

--audio-output-latency <ms>

Override audio output latency in milliseconds (default is 15 ms). Lower values make sound playback more reactive but increase CPU usage, and may result in audio cracking if the CPU can't keep up

--rendering-method <renderer>

Renderer name. Requires driver support.

--rendering-driver <driver>

Rendering driver (depends on display driver). Use --help first to display the list of available drivers.

--gpu-index <device_index>

Use a specific GPU (run with --verbose to get available device list).

--text-driver <driver>

Text driver (Fonts, BiDi, shaping).

--tablet-driver <driver>

Pen tablet input driver.

Enable headless mode (--display-driver headless --audio-driver Dummy). Useful for servers and with --script.

Write output/error log to the specified path instead of the default location defined by the project. <file> path should be absolute or relative to the project directory.

Run the engine in a way that a movie is written (usually with .avi or .png extension). --fixed-fps is forced when enabled, but can be used to change movie FPS. --disable-vsync can speed up movie writing but makes interaction more difficult. --quit-after can be used to specify the number of frames to write.

Request fullscreen mode.

Request a maximized window.

Request windowed mode.

Request an always-on-top window.

Request window resolution.

Request window position.

Request window screen.

Use a single window (no separate subwindows).

Select XR mode ('default', 'off', 'on').

Request parented to window.

--accessibility <mode>

Select accessibility mode ['auto' (when screen reader is running, default), 'always', 'disabled'].

Debug (local stdout debugger).

Breakpoint list as source::line comma-separated pairs, no spaces (use %20 instead).

--ignore-error-breaks

If debugger is connected, prevents sending error breakpoints.

Enable profiling in the script debugger.

Show a GPU profile of the tasks that took the most time during frame rendering.

Enable graphics API validation layers for debugging.

Abort on GPU errors (usually validation layer errors), may help see the problem if your system freezes.

--generate-spirv-debug-info

Generate SPIR-V debug information. This allows source-level shader debugging with RenderDoc.

--extra-gpu-memory-tracking

Enables additional memory tracking (see class reference for RenderingDevice.get_driver_and_device_memory_report() and linked methods). Currently only implemented for Vulkan. Enabling this feature may cause crashes on some systems due to buggy drivers or bugs in the Vulkan Loader. See https://github.com/godotengine/godot/issues/95967

--accurate-breadcrumbs

Force barriers between breadcrumbs. Useful for narrowing down a command causing GPU resets. Currently only implemented for Vulkan.

Remote debug (<protocol>://<host/IP>[:<port>], e.g. tcp://127.0.0.1:6007).

--single-threaded-scene

Scene tree runs in single-threaded mode. Sub-thread groups are disabled and run on the main thread.

Show collision shapes when running the scene.

Show path lines when running the scene.

Show navigation polygons when running the scene.

Show navigation avoidance debug visuals when running the scene.

Print all StringName allocations to stdout when the engine quits.

--debug-canvas-item-redraw

Display a rectangle each time a canvas item requests a redraw (useful to troubleshoot low processor mode).

Set a maximum number of frames per second rendered (can be used to limit power usage). A value of 0 results in unlimited framerate.

Simulate high CPU load (delay each frame by <ms> milliseconds). Do not use as a FPS limiter; use --max-fps instead.

Force time scale (higher values are faster, 1.0 is normal speed).

Forces disabling of vertical synchronization, even if enabled in the project settings. Does not override driver-level V-Sync enforcement.

--disable-render-loop

Disable render loop so rendering only occurs when called explicitly from script.

--disable-crash-handler

Disable crash handler when supported by the platform code.

Force a fixed number of frames per second. This setting disables real-time synchronization.

--delta-smoothing <enable>

Enable or disable frame delta smoothing ('enable', 'disable').

Print the frames per second to the stdout.

--editor-pseudolocalization

Enable pseudolocalization for the editor and the project manager.

-s, --script <script>

Run a script. <script> must be a resource path relative to the project (myscript.gd will be interpreted as res://myscript.gd) or an absolute filesystem path (for example on Windows C:/tmp/myscript.gd)

--main-loop <main_loop_name>

Run a MainLoop specified by its global class name.

Only parse for errors and quit (use with --script).

Starts the editor, waits for any resources to be imported, and then quits. Implies --editor and --quit.

--export-release <preset> <path>

Export the project in release mode using the given preset and output path. The preset name should match one defined in 'export_presets.cfg'. <path> should be absolute or relative to the project directory, and include the filename for the binary (e.g. 'builds/game.exe'). The target directory must exist.

--export-debug <preset> <path>

Like --export-release, but use debug template. Implies --import.

--export-pack <preset> <path>

Like --export-release, but only export the game pack for the given preset. The <path> extension determines whether it will be in PCK or ZIP format. Implies --import.

--export-patch <preset> <path>

Export pack with changed files only. See --export-pack description for other considerations.

List of patches to use with --export-patch. The list is comma-separated.

--install-android-build-template

Install the Android build template. Used in conjunction with --export-release or --export-debug.

--convert-3to4 [<max_file_kb>] [<max_line_size>]

Convert project from Godot 3.x to Godot 4.x.

--validate-conversion-3to4 [<max_file_kb>] [<max_line_size>]

Show what elements will be renamed when converting project from Godot 3.x to Godot 4.x.

Dump the engine API reference to the given <path> in XML format, merging if existing files are found.

Disallow dumping the base types (used with --doctool).

--gdscript-docs <path>

Rather than dumping the engine API, generate API reference from the inline documentation in the GDScript files found in <path> (used with --doctool).

Build the scripting solutions (e.g. for C# projects). Implies --editor and requires a valid project to edit.

--dump-gdextension-interface

Generate GDExtension header file 'gdnative_interface.h' in the current folder. This file is the base file required to implement a GDExtension.

Generate JSON dump of the Godot API for GDExtension bindings named 'extension_api.json' in the current folder.

--validate-extension-api <path>

Validate an extension API file dumped (with the option above) from a previous version of the engine to ensure API compatibility. If incompatibilities or errors are detected, the return code will be non-zero.

Benchmark the run time and print it to console.

--benchmark-file <path>

Benchmark the run time and save it to a given file in JSON format. The path should be absolute.

Run unit tests. Use --test --help for more information.

It is recommended to place your Godot editor binary in your PATH environment variable, so it can be executed easily from any place by typing godot. You can do so on Linux by placing the Godot binary in /usr/local/bin and making sure it is called godot (case-sensitive).

To achieve this on Windows or macOS easily, you can install Godot using Scoop (on Windows) or Homebrew (on macOS). This will automatically make the copy of Godot installed available in the PATH:

Depending on where your Godot binary is located and what your current working directory is, you may need to set the path to your project for any of the following commands to work correctly.

When running the editor, this can be done by giving the path to the project.godot file of your project as either the first argument, like this:

For all commands, this can be done by using the --path argument:

For example, the full command for exporting your game (as explained below) might look like this:

When starting from a subdirectory of your project, use the --upwards argument for Godot to automatically find the project.godot file by recursively searching the parent directories.

For example, running a scene (as explained below) nested in a subdirectory might look like this when your working directory is in the same path:

Creating a project from the command line can be done by navigating the shell to the desired place and making a project.godot file.

The project can now be opened with Godot.

Running the editor is done by executing Godot with the -e flag. This must be done from within the project directory or by setting the project path as explained above, otherwise the command is ignored and the Project Manager appears.

When passing in the full path to the project.godot file, the -e flag may be omitted.

If a scene has been created and saved, it can be edited later by running the same code with that scene as argument.

Godot is friends with your filesystem and will not create extra metadata files. Use rm to erase a scene file. Make sure nothing references that scene. Otherwise, an error will be thrown upon opening the project.

To run the game, execute Godot within the project directory or with the project path as explained above.

Note that passing in the project.godot file will always run the editor instead of running the game.

When a specific scene needs to be tested, pass that scene to the command line.

Catching errors in the command line can be a difficult task because they scroll quickly. For this, a command line debugger is provided by adding -d. It works for running either the game or a single scene.

Exporting the project from the command line is also supported. This is especially useful for continuous integration setups.

Using the --headless command line argument is required on platforms that do not have GPU access (such as continuous integration). On platforms with GPU access, --headless prevents a window from spawning while the project is exporting.

The preset name must match the name of an export preset defined in the project's export_presets.cfg file. If the preset name contains spaces or special characters (such as "Windows Desktop"), it must be surrounded with quotes.

To export a debug version of the game, use the --export-debug switch instead of --export-release. Their parameters and usage are the same.

To export only a PCK file, use the --export-pack option followed by the preset name and output path, with the file extension, instead of --export-release or --export-debug. The output path extension determines the package's format, either PCK or ZIP.

When specifying a relative path as the path for --export-release, --export-debug or --export-pack, the path will be relative to the directory containing the project.godot file, not relative to the current working directory.

It is possible to run a .gd script from the command line. This feature is especially useful in large projects, e.g. for batch conversion of assets or custom import/export.

The script must inherit from SceneTree or MainLoop.

Here is an example sayhello.gd, showing how it works:

If no project.godot exists at the path, current path is assumed to be the current working directory (unless --path is specified).

The script path will be interpreted as a resource path relative to the project, here res://sayhello.gd. You can also use an absolute filesystem path instead, which is useful if the script is located outside of the project directory.

The first line of sayhello.gd above is commonly referred to as a shebang. If the Godot binary is in your PATH as godot, it allows you to run the script as follows in modern Linux distributions, as well as macOS:

If the above doesn't work in your current version of Linux or macOS, you can always have the shebang run Godot straight from where it is located as follows:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# Add "Extras" bucket
scoop bucket add extras

# Standard editor:
scoop install godot

# Editor with C# support (will be available as `godot-mono` in `PATH`):
scoop install godot-mono
```

Example 2 (markdown):
```markdown
# Standard editor:
brew install godot

# Editor with C# support (will be available as `godot-mono` in `PATH`):
brew install godot-mono
```

Example 3 (unknown):
```unknown
godot path_to_your_project/project.godot [other] [commands] [and] [args]
```

Example 4 (unknown):
```unknown
godot --path path_to_your_project [other] [commands] [and] [args]
```

---

## Using an external text editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/external_editor.html

**Contents:**
- Using an external text editor
- Automatically reloading your changes
- Using External Editor in Debugger
- Official editor plugins
- LSP/DAP support
  - Visual Studio Code
  - Emacs
- User-contributed notes

This page explains how to code using an external text editor.

To code C# in an external editor, see the C# guide to configure an external editor.

Godot can be used with an external text editor, such as Sublime Text or Visual Studio Code. Browse to the relevant editor settings: Editor > Editor Settings > Text Editor > External

Text Editor > External section of the Editor Settings

There are two text fields: the executable path and command-line flags. The flags allow you to integrate the editor with Godot, passing it the file path to open and other relevant arguments. Godot will replace the following placeholders in the flags string:

The absolute path to the project directory

The absolute path to the file

The column number of the error

The line number of the error

Some example Exec Flags for various editors include:

{file} --line {line} --column {col}

{project} --line {line} {file}

{project} --goto {file}:{line}:{col}

"+call cursor({line}, {col})" {file}

emacs +{line}:{col} {file}

{project} {file}:{line}:{col}

*: Arguments are not automatically detected, so you must fill them in manually.

Since Godot 4.5, Exec Flags are automatically detected for all editors listed above (unless denoted with an asterisk). You don't need to paste them from this page for it to work, unless your editor has an executable name not recognized automatically (e.g. a fork of an editor listed here).

For Visual Studio Code on Windows, you will have to point to the code.cmd file.

For Emacs, you can call emacsclient instead of emacs if you use the server mode.

For Visual Studio, you will have to open the solution file .sln manually to get access to the IDE features. Additionally, it will not go to a specific line.

To have the Godot Editor automatically reload any script that has been changed by an external text editor, enable Editor > Editor Settings > Text Editor > Behavior > Auto Reload Scripts on External Change.

Using external editor in debugger is determined by a separate option in settings. For details, see Script editor debug tools and options.

We have official plugins for the following code editors:

Godot supports the Language Server Protocol (LSP) for code completion and the Debug Adapter Protocol (DAP) for debugging. You can check the LSP client list and DAP client list to find if your editor supports them. If this is the case, you should be able to take advantage of these features without the need of a custom plugin.

To use these protocols, a Godot instance must be running on your current project. You should then configure your editor to communicate to the running adapter ports in Godot, which by default are 6005 for LSP, and 6006 for DAP. You can change these ports and other settings in the Editor Settings, under the Network > Language Server and Network > Debug Adapter sections respectively.

Below are some configuration steps for specific editors:

You need to install the official Visual Studio Code plugin.

For LSP, follow these instructions to change the default LSP port. The connection status can be checked on the status bar:

For DAP, specify the debugServer property in your launch.json file:

Check the official instructions to configure LSP, and DAP.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "GDScript Godot",
            "type": "godot",
            "request": "launch",
            "project": "${workspaceFolder}",
            "port": 6007,
            "debugServer": 6006,
        }
    ]
}
```

---

## Using the engine compilation configuration editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/using_engine_compilation_configuration_editor.html

**Contents:**
- Using the engine compilation configuration editor
- Limitations
- User-contributed notes

Godot comes with a large set of built-in features. While this is convenient, this also means its binary size is larger than it could be, especially for projects that only use a small portion of its feature set.

To help reduce binary size, it is possible to compile custom export templates with certain features disabled. This is described in detail in Optimizing a build for size. However, determining which features need to be disabled can be a tedious task. The engine compilation configuration editor aims to address this by providing an interface to view and manage these features easily, while also being able to detect the features currently being used in the project.

The Project > Tools > Engine Compilation Configuration Editor allows you to create and manage build profiles for your Godot project.

From now on, you have two possibilities:

View the list and manually uncheck features that you don't need.

Use the Detect from Project button to automatically detect features currently used in the project and disable unused features. Note that this will override the existing list of features, so if you have manually unchecked some items, their state will be reset based on whether the project actually uses the feature.

Opening the Engine Compilation Configuration Editor

Once you click Detect from Project, the project detection step will run. This can take from a few seconds up to several minutes depending on the project size. Once detection is complete, you'll see an updated list of features with some features disabled:

Updated features list after using feature detection (example from the 3D platformer demo)

Unchecking features in this dialog will not reduce binary size directly on export. Since it is only possible to actually remove features from the binary at compile-time, you still need to compile custom export templates with the build profile specified to actually benefit from the engine compilation configuration editor.

You can now save the build profile by clicking Save As at the top. The build profile can be saved in any location, but it's a good idea to save it somewhere in your project folder and add it to version control to be able to go back to it later when needed. This also allows using version control to track changes to the build profile.

The build profile is a JSON file (and .gdbuild extension) that looks like this after detection in the above example:

This file can be passed as a SCons option when compiling export templates:

The buildsystem will use this to disable unused classes and reduce binary size as a result.

The Detect from Project functionality relies on reading the project's scenes and scripts. It will not be able to detect used features in the following scenarios:

Features that are used in GDScripts that are procedurally created then run at runtime.

Features that are used in expressions.

Features that are used in GDExtensions, unless the language binding allows for defining used classes and the extension makes use of the functionality. See GH-104129 for details.

Features that are used in external PCKs loaded at runtime.

Certain edge cases may exist. If unsure, please open an issue on GitHub with a minimal reproduction project attached.

You can achieve further size reductions by passing other options that reduce binary size. See Optimizing a build for size for more information.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (json):
```json
{
    "disabled_build_options": {
        "disable_navigation_3d": true,
        "disable_xr": true,
        "module_godot_physics_3d_enabled": false,
        "module_msdfgen_enabled": false,
        "module_openxr_enabled": false
    },
    "disabled_classes": [
        "AESContext",
        ...
        "ZIPReader"
    ],
    "type": "build_profile"
}
```

Example 2 (unknown):
```unknown
scons target=template_release build_profile=/path/to/profile.gdbuild
```

---
