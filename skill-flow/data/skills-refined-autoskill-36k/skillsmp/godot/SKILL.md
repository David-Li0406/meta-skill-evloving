---
name: godot
description: Complete Godot Engine knowledge base combining official documentation and source code analysis. Use for Godot projects, GDScript/C# coding, scene setup, node systems, 2D/3D development, physics, animation, UI, shaders, or any Godot-specific questions.
---

# Godot Engine - Complete Knowledge Base

Complete Godot Engine knowledge base combining official documentation and source code analysis. This skill synthesizes knowledge from multiple sources to provide comprehensive guidance for game development with Godot.

## 📚 Sources

This skill synthesizes knowledge from multiple sources:

- ✅ **Official Documentation**: https://docs.godotengine.org/en/stable/
  - 50+ pages of getting started tutorials
  - 66 pages of scripting documentation (GDScript & C#)
  - 20 pages of 2D development guides
  - 59 pages of 3D development guides
  - 12 pages of animation documentation
  - 29 pages of physics documentation
  - Plus audio, networking, shaders, UI, export, and more

- ✅ **GitHub Repository**: [godotengine/godot](https://github.com/godotengine/godot)
  - 105,707+ stars (one of the most popular game engines)
  - C++ codebase (85.3%) with C# support (3.2%)
  - Active development with 17,272 open issues
  - MIT License - fully open source

## 📦 About Godot Engine

Godot is a feature-packed, cross-platform game engine designed to create 2D and 3D games. It offers a fully-fledged game editor with integrated tools including code editor, animation editor, tilemap editor, shader editor, debugger, and profiler.

**Key Features:**
- **Multi-platform**: Export to desktop, mobile, web, and consoles (with porting)
- **Programming Languages**: GDScript (Godot's custom language), C#, and C++ via GDExtension
- **2D & 3D**: Dedicated renderers for both 2D and 3D with specific tools
- **Free & Open Source**: MIT license, no royalties, full source code access
- **Lightweight**: Full engine download under 100MB
- **Active Community**: Large community with regular updates and extensive documentation

**Repository Statistics:**
- **Primary Language:** C++ (85.3%)
- **Secondary Languages:** C# (3.2%), C (3.0%), Java (2.8%), GLSL (1.7%)
- **Stars:** 105,707
- **License:** MIT License
- **Homepage:** https://godotengine.org
- **Topics:** game-engine, godot, godotengine, open-source, multi-platform, gamedev, game-development

## 💡 When to Use This Skill

### Primary Use Cases

This skill should be triggered when:
- **Working with Godot projects** - Scene setup, node hierarchy, resource management
- **Asking about Godot features or APIs** - Node types, built-in functions, signals
- **Implementing Godot solutions** - Game mechanics, UI systems, data persistence
- **Debugging Godot code** - GDScript/C# errors, performance issues, node path problems
- **Learning Godot best practices** - Architecture patterns, optimization techniques

### Specific Scenarios

**From repository analysis and documentation:**

Use this skill when you need to:
- **Understand how to use Godot** - Editor interface, project structure, workflow
- **Look up API documentation** - Node classes, methods, properties, signals
- **Find real-world usage examples** - Code patterns from official docs and codebase
- **Review design patterns and architecture** - Scene organization, autoloads, signals vs direct calls
- **Check for known issues or recent changes** - GitHub issues, release notes, version differences
- **Explore 2D/3D development** - Sprites, meshes, lighting, physics, navigation
- **Work with animations** - AnimationPlayer, AnimationTree, tweening, skeletons
- **Implement physics** - Rigid bodies, collision detection, character controllers
- **Create UI systems** - Control nodes, themes, localization
- **Write custom shaders** - Visual shaders, shader language, post-processing
- **Export your game** - Platform-specific settings, optimization, distribution

## 🎯 Quick Reference

### Programming Languages in Godot

**GDScript** (Recommended for beginners):
- Godot's custom language designed for the engine
- Lightweight Python-like syntax
- Tightly integrated with Godot's APIs
- Fast iteration with hot-reloading

**C#** (For experienced developers):
- Full C# 9.0+ support
- Popular in the games industry
- Strong typing and Visual Studio integration
- Access to .NET ecosystem

**GDExtension** (For performance-critical code):
- Write high-performance code in C++ or other languages
- No need to recompile the engine
- Integrate third-party libraries and SDKs

### Essential Code Patterns

**From official documentation:**

#### 1. Basic Node Lifecycle

```gdscript
# GDScript - Basic lifecycle methods
extends Node2D

func _init():
    # Called when object is created (before entering tree)
    pass

func _enter_tree():
    # Called when node enters scene tree
    pass

func _ready():
    # Called when node is ready, after all children are ready
    print("Hello world!")

func _process(delta):
    # Called every frame
    # Use for framerate-dependent updates
    pass

func _physics_process(delta):
    # Called every physics frame (fixed timestep)
    # Use for physics and movement
    pass

func _exit_tree():
    # Called when node leaves scene tree
    pass
```

```csharp
// C# - Basic lifecycle methods
using Godot;

public partial class MyNode : Node2D
{
    // Constructor (equivalent to _init)
    public MyNode() {}

    public override void _EnterTree()
    {
        // Called when node enters scene tree
    }

    public override void _Ready()
    {
        // Called when node is ready
        GD.Print("Hello world!");
    }

    public override void _Process(double delta)
    {
        // Called every frame
    }

    public override void _PhysicsProcess(double delta)
    {
        // Called every physics frame
    }

    public override void _ExitTree()
    {
        // Called when node leaves scene tree
    }
}
```

#### 2. Using Signals (Godot's Event System)

```gdscript
# Connecting to a built-in signal
func _ready():
    $Button.button_down.connect(_on_button_pressed)

func _on_button_pressed():
    print("Button was pressed!")

# Custom signal
signal health_changed(new_health)

func take_damage(amount):
    health -= amount
    health_changed.emit(health)
```

```csharp
// Connecting to a built-in signal
public override void _Ready()
{
    GetNode<Button>("Button").ButtonDown += OnButtonPressed;
}

private void OnButtonPressed()
{
    GD.Print("Button was pressed!");
}

// Custom signal (delegate)
[Signal]
public delegate void HealthChangedEventHandler(int newHealth);

public void TakeDamage(int amount)
{
    health -= amount;
    EmitSignal(SignalName.HealthChanged, health);
}
```

#### 3. Loading and Preloading Resources

```gdscript
# Preload - loads at compile time (best for constants)
const PlayerScene = preload("res://player.tscn")

# Load - loads at runtime (best for dynamic loading)
func load_enemy():
    var enemy_scene = load("res://enemy.tscn")
    var enemy = enemy_scene.instantiate()
    add_child(enemy)
```

```csharp
// C# uses ResourceLoader for all loading
public void LoadEnemy()
{
    var enemyScene = GD.Load<PackedScene>("res://enemy.tscn");
    var enemy = enemyScene.Instantiate();
    AddChild(enemy);
}
```

#### 4. 3D Transforms (Avoiding Euler Angles)

```gdscript
# BAD: Don't use rotation property for gameplay
# rotation_degrees.y += 90  # This can cause gimbal lock

# GOOD: Use transform methods
# Rotate around local Y axis
rotate_object_local(Vector3.UP, deg_to_rad(90))

# Rotate around parent's Y axis
rotate_y(deg_to_rad(90))

# Move in local forward direction
translate_object_local(Vector3.FORWARD * speed)

# Get forward direction for shooting
var forward_direction = transform.basis.z
bullet.linear_velocity = forward_direction * bullet_speed
```

```csharp
// GOOD: Use transform methods
// Rotate around local Y axis
RotateObjectLocal(Vector3.Up, Mathf.DegToRad(90));

// Rotate around parent's Y axis
RotateY(Mathf.DegToRad(90));

// Move in local forward direction
TranslateObjectLocal(Vector3.Forward * Speed);

// Get forward direction for shooting
var forwardDirection = Transform.Basis.Z;
bullet.LinearVelocity = forwardDirection * BulletSpeed;
```

#### 5. Animation Method Track

```gdscript
# Create a call method track programmatically
func create_method_animation_track():
    var animation = $AnimationPlayer.get_animation("idle")
    var track_index = animation.add_track(Animation.TYPE_METHOD)

    var jump_velocity = -400.0
    var multiplier = randf_range(0.8, 1.2)

    var method_dictionary = {
        "method": "jump",
        "args": [jump_velocity, multiplier],
    }

    animation.track_set_path(track_index, ".")
    animation.track_insert_key(track_index, 0.6, method_dictionary, 0)

func jump(jump_velocity, multiplier):
    velocity.y = jump_velocity * multiplier
```

```csharp
// Create a call method track programmatically
public void CreateAnimationTrack()
{
    var animationPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
    var animation = animationPlayer.GetAnimation("idle");
    var trackIndex = animation.AddTrack(Animation.TrackType.Method);

    var jumpVelocity = -400.0;
    var multiplier = GD.RandRange(0.8, 1.2);

    var methodDictionary = new Godot.Collections.Dictionary
    {
        { "method", MethodName.Jump },
        { "args", new Godot.Collections.Array { jumpVelocity, multiplier } }
    };

    animation.TrackSetPath(trackIndex, ".");
    animation.TrackInsertKey(trackIndex, 0.6, methodDictionary, 0);
}

private void Jump(float jumpVelocity, float multiplier)
{
    Velocity = new Vector2(Velocity.X, jumpVelocity * multiplier);
}
```

#### 6. Navigation Layers (Pathfinding)

```gdscript
# Enable/disable navigation layers with bitmask helpers
func change_layers():
    var region = get_node("NavigationRegion2D")

    # Enable 4th layer for this region
    region.navigation_layers = enable_bitmask_inx(region.navigation_layers, 4)

    # Disable 1st layer for this region
    region.navigation_layers = disable_bitmask_inx(region.navigation_layers, 1)

    var agent = get_node("NavigationAgent2D")
    # Make agent ignore regions with 4th layer
    agent.navigation_layers = disable_bitmask_inx(agent.navigation_layers, 4)

static func is_bitmask_inx_enabled(_bitmask: int, _index: int) -> bool:
    return _bitmask & (1 << _index) != 0

static func enable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask | (1 << _index)

static func disable_bitmask_inx(_bitmask: int, _index: int) -> int:
    return _bitmask & ~(1 << _index)
```

```csharp
using Godot;

public partial class MyNode2D : Node2D
{
    private Rid _map;
    private Vector2 _startPosition;
    private Vector2 _targetPosition;

    private void ChangeLayers()
    {
        NavigationRegion2D region = GetNode<NavigationRegion2D>("NavigationRegion2D");

        // Enable the 4th layer for this region
        region.NavigationLayers = EnableBitmaskInx(region.NavigationLayers, 4);

        // Disable the 1st layer for this region
        region.NavigationLayers = DisableBitmaskInx(region.NavigationLayers, 1);

        NavigationAgent2D agent = GetNode<NavigationAgent2D>("NavigationAgent2D");

        // Make agent ignore regions with 4th layer
        agent.NavigationLayers = DisableBitmaskInx(agent.NavigationLayers, 4);
    }

    private static bool IsBitmaskInxEnabled(int bitmask, int index)
    {
        return (bitmask & (1 << index)) != 0;
    }

    private static int EnableBitmaskInx(int bitmask, int index)
    {
        return bitmask | (1 << index);
    }

    private static int DisableBitmaskInx(int bitmask, int index)
    {
        return bitmask & ~(1 << index);
    }
}
```

#### 7. Using MeshDataTool for Procedural Geometry

```gdscript
# MeshDataTool is for dynamically altering existing mesh geometry
var mdt = MeshDataTool.new()
mdt.create_from_surface(mesh, 0)

# Get mesh information
var vertex_count = mdt.get_vertex_count()
var faces = mdt.get_vertex_faces(0)  # Faces containing vertex[0]
var normal = mdt.get_face_normal(1)  # Normal of second face

# Transform vertices
for i in range(vertex_count):
    var vert = mdt.get_vertex(i)
    vert *= 2.0  # Scale vertex by doubling size
    mdt.set_vertex(i, vert)

# Commit changes back to mesh
mdt.commit_to_surface(mesh)
```

### Node System Basics

Godot uses a tree-based node system where everything is a Node:

- **Node**: Base class for all objects in the scene tree
- **Node2D**: Base for 2D nodes (has position, rotation, scale in 2D)
- **Node3D**: Base for 3D nodes (has 3D transform)
- **Control**: Base for UI nodes
- **Resource**: Data assets (textures, sounds, scenes)

**Common Node Paths:**
- `$NodeName` - Shorthand for `get_node("NodeName")` (relative path)
- `%"Node Name"` - For nodes with spaces in names
- `/root` - Global autoload singleton
- `self` - Current node

### Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

The Godot codebase extensively uses these design patterns:
- **Strategy**: 19 instances - Interchangeable algorithms
- **Builder**: 2 instances - Complex object construction

*Total: 21 high-confidence patterns detected*

### Notifications System

Every Object in Godot implements a `_notification` method that responds to engine callbacks:

```gdscript
func _notification(what):
    match what:
        NOTIFICATION_READY:
            # Equivalent to _ready()
            pass
        NOTIFICATION_PROCESS:
            # Equivalent to _process()
            pass
        NOTIFICATION_PARENTED:
            # Called when node is added as child
            pass
        NOTIFICATION_UNPARENTED:
            # Called when node is removed
            pass
        NOTIFICATION_DRAW:
            # For CanvasItem nodes - request redraw
            pass
```

## 🧪 Code Examples by Category

### Getting Started Examples

**Learn GDScript From Zero** - Interactive browser-based GDScript course:
- Complete beginner course with interactive practices
- Open-source project
- Access at: Learn GDScript From Zero app

**Prerequisites:**
- For beginners: Start with GDScript (simpler, designed for Godot)
- For experienced programmers: Use C# (industry standard, .NET ecosystem)
- General programming knowledge: Object-oriented concepts (classes, objects) are essential

### 2D Development Examples

**2D Lights and Shadows Setup:**

```gdscript
# Required nodes for 2D lighting:
# - CanvasModulate: Darkens the scene (ambient color)
# - PointLight2D: Omnidirectional or spot lights
# - DirectionalLight2D: Sunlight or moonlight
# - LightOccluder2D: Shadow casters
# - Sprite2D/TileMapLayer: Receivers

# Enable shadows on a light
$PointLight2D.shadow_enabled = true

# Set light texture
$PointLight2D.texture = preload("res://light_texture.png")
```

**2D Particle Systems:**
- Use GPUParticles2D for GPU-accelerated particles
- Configurable: Amount, Lifetime, Speed Scale, Explosiveness
- Process material controls particle behavior

### 3D Development Examples

**ImmediateMesh for Dynamic Geometry:**

```gdscript
extends MeshInstance3D

func _ready():
    # Begin drawing triangles
    mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLES)

    # Add vertices with attributes
    mesh.surface_set_normal(Vector3(0, 0, 1))
    mesh.surface_set_uv(Vector2(0, 0))
    mesh.surface_add_vertex(Vector3(-1, -1, 0))

    mesh.surface_set_normal(Vector3(0, 0, 1))
    mesh.surface_set_uv(Vector2(0, 1))
    mesh.surface_add_vertex(Vector3(-1, 1, 0))

    mesh.surface_set_normal(Vector3(0, 0, 1))
    mesh.surface_set_uv(Vector2(1, 1))
    mesh.surface_add_vertex(Vector3(1, 1, 0))

    # End drawing
    mesh.surface_end()

func _process(delta):
    # For dynamic geometry, clear and redraw each frame
    mesh.clear_surfaces()
    mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLES)
    # ... add vertices ...
    mesh.surface_end()
```

### Physics Examples

**Using NavigationLayers:**
- NavigationLayers control which navigation meshes are considered in path queries
- Work like physics layers (bitmask-based)
- Performance-friendly alternative to enabling/disabling regions
- Change agent layers for immediate effect on next path query

### Animation Examples

**Animation Track Types:**
1. **Property Track** - Basic property animation
2. **Position 3D / Rotation 3D / Scale 3D Track** - Optimized for 3D transforms
3. **Blend Shape Track** - For MeshInstance3D blend shapes
4. **Call Method Track** - Call functions at precise times
5. **Bezier Curve Track** - Animate properties with curves
6. **Audio Playback Track** - Sync audio with animation
7. **Animation Playback Track** - Sequence other animation players

### Scripting Examples

**Script Editor Features:**
- Fully-integrated code editor for GDScript and C#
- Syntax highlighting, auto-indentation, syntax checking
- Multiple carets (Alt + Left Click)
- Auto-completion of variables, functions, constants
- Inline refactoring (Ctrl + D)
- Mass find and replace across project files
- Bookmarks and breakpoints for debugging

**External Editor Support:**
- VSCode and Emacs plugins for GDScript
- Visual Studio for C# on Windows
- Blender for 3D scene import

## 🔧 API Reference

*Extracted from codebase analysis (C2.5)*

### Core Classes

**Node** - Base class for all scene objects
- `add_child(node)` - Add child node
- `get_node(path)` - Get node by path
- `get_tree()` - Access SceneTree
- `queue_free()` - Queue for deletion

**Node2D** - 2D transform node
- `position`, `rotation`, `scale` - 2D transform properties
- `global_position` - World space position
- `move_local_x(delta)` - Move in local X

**Node3D** - 3D transform node
- `position`, `rotation_degrees`, `scale` - 3D transform
- `global_transform` - World space transform
- `rotate(axis, angle)` - Rotate around axis
- `look_at(target)` - Look at target position

**Resource** - Data assets
- `load(path)` - Load resource from disk
- `preload(path)` - Preload at compile time (GDScript only)

## ⚠️ Known Issues

*Recent issues from GitHub (as of 2026-01-22)*

- **#111668**: Crash apparently random [`needs work, needs testing, crash`]
- **#113036**: No margin between the `Toggle Favorite` button and highlight border in project manager [`bug, usability, topic:gui`]
- **#115244**: Empty descriptions when hovering `FileDialog` theme items from inspector
- **#115221**: Overextended dropdown menus with blank space at the bottom on v4.6-RC2 [`bug, platform:linuxbsd, topic:editor, regression`]
- **#115241**: Alt-dragging text file into script window creates nonexistent type annotation

*See `references/issues.md` for complete list*

### Recent Releases
- **3.6.2-stable** (2025-10-23): Godot 3.6.2 stable release
- **4.5.1-stable** (2025-10-15): Godot 4.5.1 stable release
- **4.5-stable** (2025-09-15): Godot 4.5 stable release

## 📖 Reference Documentation

### Documentation Structure

Organized by source type and confidence level:

#### **From Official Documentation** (High Confidence)

- **[Getting Started](references/getting_started.md)** (50 pages)
  - Introduction to Godot
  - Step-by-step tutorials
  - Editor interface
  - GDScript basics
  - Project setup

- **[Scripting](references/scripting.md)** (66 pages)
  - GDScript reference
  - C# in Godot
  - Script editor usage
  - Coding best practices
  - Debugging tools

- **[2D Development](references/2d.md)** (20 pages)
  - 2D lights and shadows
  - 2D particle systems
  - 2D skeletons
  - 2D navigation
  - Tilemaps

- **[3D Development](references/3d.md)** (59 pages)
  - 3D transforms and coordinate systems
  - Procedural geometry (MeshDataTool, ImmediateMesh)
  - 3D particle systems
  - Cameras and viewport
  - 3D optimization

- **[Animation](references/animation.md)** (12 pages)
  - Animation track types
  - 2D skeletons
  - Cutout animation
  - AnimationPlayer and AnimationTree

- **[Physics](references/physics.md)** (29 pages)
  - Physics introduction
  - Rigid bodies
  - Collision detection
  - Navigation and pathfinding
  - Character controllers

- **[Additional Topics]**
  - **[Audio](references/audio.md)** - Audio systems and sound
  - **[Networking](references/networking.md)** - Multiplayer and network programming
  - **[Shaders](references/shaders.md)** - Visual and code shaders
  - **[UI](references/ui.md)** - Control nodes and interfaces
  - **[Export](references/export.md)** - Platform export and publishing
  - **[Other](references/other.md)** - Miscellaneous topics

#### **From GitHub Repository** (High Confidence)

- **[GitHub Analysis](references/github/)**
  - Repository metadata
  - Source code structure
  - Architecture patterns
  - Known issues and discussions

#### **From Codebase Analysis** (Medium Confidence)

- **[Architecture](references/codebase_analysis/ARCHITECTURE.md)**
  - Design patterns detected (Strategy, Builder)
  - Code organization
  - Performance characteristics
  - Best practices from source code

## 🛠️ Working with This Skill

### For Beginners

1. **Start here:** Read `references/getting_started.md` for foundational concepts
2. **Learn GDScript:** Use the "Learn GDScript From Zero" app (interactive browser course)
3. **Follow tutorials:** Your First 2D Game, Your First 3D Game
4. **Explore examples:** Check the example projects in the asset library

### For Intermediate Users

1. **Specific features:** Use category-specific reference files (2d.md, 3d.md, etc.)
2. **Code examples:** Extract patterns from the Quick Reference section above
3. **API reference:** Look up specific nodes and methods in official docs
4. **Best practices:** Review design patterns and architecture sections

### For Advanced Users

1. **Source code:** Explore the C++ codebase through GitHub analysis
2. **Performance:** Check optimization guides in 3D and physics docs
3. **Extension:** Learn GDExtension for C++ integrations
4. **Contributing:** Review known issues and architecture for contributions

### Navigation Tips

- **Search:** Use Ctrl+F in reference files to find specific topics
- **Code examples:** All code blocks have language tags for syntax highlighting
- **Links:** Original documentation URLs preserved in each section
- **Table of Contents:** Each reference file has a TOC for quick navigation

## 🎓 Key Concepts

### Scene Tree and Nodes

Godot uses a tree-based architecture where everything is a Node in a SceneTree:

- **Scenes** (.tscn) are reusable components with a tree of nodes
- **Instancing** allows reusing scenes multiple times
- **Inheritance** lets scenes extend other scenes
- **Autoload** creates global singletons accessible from anywhere

### Resources vs Nodes

- **Nodes** are objects in the scene tree (have position, process frames)
- **Resources** are data assets (textures, sounds, scripts)
- Resources are shared by reference (efficient memory usage)
- Use `resource_local_to_scene` for unique resource instances

### Signals

Godot's event system for decoupled communication:
- Built-in signals (e.g., `button_down`, `body_entered`)
- Custom signals with `signal` keyword (GDScript) or `[Signal]` attribute (C#)
- Connect using `connect()` method or editor interface
- Emit signals with `.emit()` (GDScript) or `EmitSignal()` (C#)

### autoload Singletons

Global scripts accessible from anywhere:
- Configure in Project Settings → Autoload
- Access via `GlobalName.script_method()` or `GlobalName.variable`
- Use for global state, utility functions, and shared data

### Data Preferences (Best Practices)

**When to use preloading vs loading:**
- `preload()` - Use for constants, assets known at compile time
- `load()` - Use for dynamic assets, runtime decisions

**When to use static vs dynamic levels:**
- Small games → Static level (load everything at once)
- Large/procedural games → Dynamic level (load/unload chunks)

**Node property initialization order:**
1. Initial value assignment (no setter)
2. `_init()` assignment (setter triggered)
3. Exported value assignment (setter triggered, from Inspector)

## 🔄 Updating This Skill

To refresh this skill with updated documentation:

1. Re-run the documentation scraper with updated configuration
2. The skill will be rebuilt with the latest information
3. Reference files will preserve new content and examples
4. Quick reference patterns will be re-extracted from latest docs

## 📚 Additional Resources

- **Official Website:** https://godotengine.org
- **Documentation:** https://docs.godotengine.org
- **Asset Library:** https://godotengine.org/asset-library
- **GitHub:** https://github.com/godotengine/godot
- **Community:** Discord, Reddit, Forums (links on official site)

---

*This skill synthesizes knowledge from official Godot documentation and the godotengine/godot GitHub repository. Last updated: 2026-01-22*

*Generated by Skill Seekers - Multi-source documentation synthesis tool*
