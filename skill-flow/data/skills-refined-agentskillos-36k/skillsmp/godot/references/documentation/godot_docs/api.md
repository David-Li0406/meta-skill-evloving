# Godot_Docs - Api

**Pages:** 4

---

## Documentation changelog — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/docs_changelog.html

**Contents:**
- Documentation changelog
- New pages since version 4.3
  - 2D
  - 3D
  - Debug
  - Editor
  - Performance
  - Physics
  - Rendering
  - Shaders

The documentation is continually being improved. New releases include new pages, fixes and updates to existing pages, and many updates to the class reference. Below is a list of new pages added since version 3.0.

This document only contains new pages so not all changes are reflected, many pages have been substantially updated but are not reflected in this document.

Third-person camera with spring arm

Reducing stutter from shader (pipeline) compilations

Physics Interpolation

Using physics interpolation

Advanced physics interpolation

2D and 3D physics interpolation

Overview of renderers

Handling compatibility breakages

The .gdextension file

Upgrading from Godot 4.2 to Godot 4.3

A better XR start script

Where to go from here

OpenXR composition layers

2D coordinate systems and 2D transforms

Upgrading from Godot 4.1 to Godot 4.2

Runtime file loading and saving

Godot Android library

Internal rendering architecture

Upgrading from Godot 4.0 to Godot 4.1

Troubleshooting physics issues

Faking global illumination

Introduction to global illumination

Mesh level of detail (LOD)

Signed distance field global illumination (SDFGI)

Visibility ranges (HLOD)

Volumetric fog and fog volumes

Variable rate shading

Physical light and camera units

Retargeting 3D Skeletons

Custom platform ports

Upgrading from Godot 3 to Godot 4

Large world coordinates

Custom performance monitors

Using compute shaders

Managing editor features

GDScript documentation comments

3D rendering limitations

Version control systems

Configuring an IDE: Code::Blocks

Default editor shortcuts

Exporting for dedicated servers

Controllers, gamepads, and joysticks

Random number generation

HTML5 shell class reference

Collision shapes (2D)

Collision shapes (3D)

Creating script templates

Evaluating expressions

GDScript warning system (split from Static typing in GDScript)

Gradle builds for Android

Recording with microphone

Sync the gameplay with audio and music

Beziers, curves and paths

Localization using gettext (PO files)

Introduction to shaders

Your second 3D shader

Godot Android plugins

Visual Shader plugins

Using multiple threads

Using the SurfaceTool

Using the MeshDataTool

Optimization using MultiMeshes

Optimization using Servers

Complying with licenses

Static typing in GDScript

Applying object-oriented principles in Godot

When to use scenes versus scripts

Autoloads versus regular nodes

When and how to avoid using nodes for everything

2D lights and shadows

Prototyping levels with CSG

Animating thousands of fish with MultiMeshInstance3D

Controlling thousands of fish with Particles

Using a SubViewport as a texture

Custom post-processing

Converting GLSL to Godot shaders

Advanced post-processing

Introduction to shaders

Making main screen plugins

Custom HTML page for Web export

Fixing jitter, stutter and input lag

Running code in the editor

Change scenes manually

Optimizing a build for size

Compiling with PCK encryption key

Binding to external libraries

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Applying object-oriented principles in Godot — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/what_are_godot_classes.html

**Contents:**
- Applying object-oriented principles in Godot
- How scripts work in the engine
- Scenes
- User-contributed notes

The engine offers two main ways to create reusable objects: scripts and scenes. Neither of these technically define classes under the hood.

Still, many best practices using Godot involve applying object-oriented programming principles to the scripts and scenes that compose your game. That is why it's useful to understand how we can think of them as classes.

This guide briefly explains how scripts and scenes work in the engine's core to help you understand how they work under the hood.

The engine provides built-in classes like Node. You can extend those to create derived types using a script.

These scripts are not technically classes. Instead, they are resources that tell the engine a sequence of initializations to perform on one of the engine's built-in classes.

Godot's internal classes have methods that register a class's data with a ClassDB. This database provides runtime access to class information. ClassDB contains information about classes like:

This ClassDB is what objects check against when performing an operation like accessing a property or calling a method. It checks the database's records and the object's base types' records to see if the object supports the operation.

Attaching a Script to your object extends the methods, properties, and signals available from the ClassDB.

Even scripts that don't use the extends keyword implicitly inherit from the engine's base RefCounted class. As a result, you can instantiate scripts without the extends keyword from code. Since they extend RefCounted though, you cannot attach them to a Node.

The behavior of scenes has many similarities to classes, so it can make sense to think of a scene as a class. Scenes are reusable, instantiable, and inheritable groups of nodes. Creating a scene is similar to having a script that creates nodes and adds them as children using add_child().

We often pair a scene with a scripted root node that makes use of the scene's nodes. As such, the script extends the scene by adding behavior through imperative code.

The content of a scene helps to define:

What nodes are available to the script.

How they are organized.

How they are initialized.

What signal connections they have with each other.

Why is any of this important to scene organization? Because instances of scenes are objects. As a result, many object-oriented principles that apply to written code also apply to scenes: single responsibility, encapsulation, and others.

The scene is always an extension of the script attached to its root node, so you can interpret it as part of a class.

Most of the techniques explained in this best practices series build on this point.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Data preferences — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/data_preferences.html

**Contents:**
- Data preferences
- Array vs. Dictionary vs. Object
- Enumerations: int vs. string
- AnimatedTexture vs. AnimatedSprite2D vs. AnimationPlayer vs. AnimationTree
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Ever wondered whether one should approach problem X with data structure Y or Z? This article covers a variety of topics related to these dilemmas.

This article makes references to "[something]-time" operations. This terminology comes from algorithm analysis' Big O Notation.

Long-story short, it describes the worst-case scenario of runtime length. In laymen's terms:

"As the size of a problem domain increases, the runtime length of the algorithm..."

Constant-time, O(1): "...does not increase."

Logarithmic-time, O(log n): "...increases at a slow rate."

Linear-time, O(n): "...increases at the same rate."

Imagine if one had to process 3 million data points within a single frame. It would be impossible to craft the feature with a linear-time algorithm since the sheer size of the data would increase the runtime far beyond the time allotted. In comparison, using a constant-time algorithm could handle the operation without issue.

By and large, developers want to avoid engaging in linear-time operations as much as possible. But, if one keeps the scale of a linear-time operation small, and if one does not need to perform the operation often, then it may be acceptable. Balancing these requirements and choosing the right algorithm / data structure for the job is part of what makes programmers' skills valuable.

Godot stores all variables in the scripting API in the Variant class. Variants can store Variant-compatible data structures such as Array and Dictionary as well as Objects.

Godot implements Array as a Vector<Variant>. The engine stores the Array contents in a contiguous section of memory, i.e. they are in a row adjacent to each other.

For those unfamiliar with C++, a Vector is the name of the array object in traditional C++ libraries. It is a "templated" type, meaning that its records can only contain a particular type (denoted by angled brackets). So, for example, a PackedStringArray would be something like a Vector<String>.

Contiguous memory stores imply the following operation performance:

Iterate: Fastest. Great for loops.

Op: All it does is increment a counter to get to the next record.

Insert, Erase, Move: Position-dependent. Generally slow.

Op: Adding/removing/moving content involves moving the adjacent records over (to make room / fill space).

Fast add/remove from the end.

Slow add/remove from an arbitrary position.

Slowest add/remove from the front.

If doing many inserts/removals from the front, then...

do a loop which executes the Array changes at the end.

This makes only 2 copies of the array (still constant time, but slow) versus copying roughly 1/2 of the array, on average, N times (linear time).

Get, Set: Fastest by position. E.g. can request 0th, 2nd, 10th record, etc. but cannot specify which record you want.

Op: 1 addition operation from array start position up to desired index.

Find: Slowest. Identifies the index/position of a value.

Op: Must iterate through array and compare values until one finds a match.

Performance is also dependent on whether one needs an exhaustive search.

If kept ordered, custom search operations can bring it to logarithmic time (relatively fast). Laymen users won't be comfortable with this though. Done by re-sorting the Array after every edit and writing an ordered-aware search algorithm.

Godot implements Dictionary as a HashMap<Variant, Variant, VariantHasher, StringLikeVariantComparator>. The engine stores a small array (initialized to 2^3 or 8 records) of key-value pairs. When one attempts to access a value, they provide it a key. It then hashes the key, i.e. converts it into a number. The "hash" is used to calculate the index into the array. As an array, the HM then has a quick lookup within the "table" of keys mapped to values. When the HashMap becomes too full, it increases to the next power of 2 (so, 16 records, then 32, etc.) and rebuilds the structure.

Hashes are to reduce the chance of a key collision. If one occurs, the table must recalculate another index for the value that takes the previous position into account. In all, this results in constant-time access to all records at the expense of memory and some minor operational efficiency.

Hashing every key an arbitrary number of times.

Hash operations are constant-time, so even if an algorithm must do more than one, as long as the number of hash calculations doesn't become too dependent on the density of the table, things will stay fast. Which leads to...

Maintaining an ever-growing size for the table.

HashMaps maintain gaps of unused memory interspersed in the table on purpose to reduce hash collisions and maintain the speed of accesses. This is why it constantly increases in size exponentially by powers of 2.

As one might be able to tell, Dictionaries specialize in tasks that Arrays do not. An overview of their operational details is as follows:

Op: Iterate over the map's internal vector of hashes. Return each key. Afterwards, users then use the key to jump to and return the desired value.

Insert, Erase, Move: Fastest.

Op: Hash the given key. Do 1 addition operation to look up the appropriate value (array start + offset). Move is two of these (one insert, one erase). The map must do some maintenance to preserve its capabilities:

update ordered List of records.

determine if table density mandates a need to expand table capacity.

The Dictionary remembers in what order users inserted its keys. This enables it to execute reliable iterations.

Get, Set: Fastest. Same as a lookup by key.

Op: Same as insert/erase/move.

Find: Slowest. Identifies the key of a value.

Op: Must iterate through records and compare the value until a match is found.

Note that Godot does not provide this feature out-of-the-box (because they aren't meant for this task).

Godot implements Objects as stupid, but dynamic containers of data content. Objects query data sources when posed questions. For example, to answer the question, "do you have a property called, 'position'?", it might ask its script or the ClassDB. One can find more information about what objects are and how they work in the Applying object-oriented principles in Godot article.

The important detail here is the complexity of the Object's task. Every time it performs one of these multi-source queries, it runs through several iteration loops and HashMap lookups. What's more, the queries are linear-time operations dependent on the Object's inheritance hierarchy size. If the class the Object queries (its current class) doesn't find anything, the request defers to the next base class, all the way up until the original Object class. While these are each fast operations in isolation, the fact that it must make so many checks is what makes them slower than both of the alternatives for looking up data.

When developers mention how slow the scripting API is, it is this chain of queries they refer to. Compared to compiled C++ code where the application knows exactly where to go to find anything, it is inevitable that scripting API operations will take much longer. They must locate the source of any relevant data before they can attempt to access it.

The reason GDScript is slow is because every operation it performs passes through this system.

C# can process some content at higher speeds via more optimized bytecode. But, if the C# script calls into an engine class' content or if the script tries to access something external to it, it will go through this pipeline.

NativeScript C++ goes even further and keeps everything internal by default. Calls into external structures will go through the scripting API. In NativeScript C++, registering methods to expose them to the scripting API is a manual task. It is at this point that external, non-C++ classes will use the API to locate them.

So, assuming one extends from Reference to create a data structure, like an Array or Dictionary, why choose an Object over the other two options?

Control: With objects comes the ability to create more sophisticated structures. One can layer abstractions over the data to ensure the external API doesn't change in response to internal data structure changes. What's more, Objects can have signals, allowing for reactive behavior.

Clarity: Objects are a reliable data source when it comes to the data that scripts and engine classes define for them. Properties may not hold the values one expects, but one doesn't need to worry about whether the property exists in the first place.

Convenience: If one already has a similar data structure in mind, then extending from an existing class makes the task of building the data structure much easier. In comparison, Arrays and Dictionaries don't fulfill all use cases one might have.

Objects also give users the opportunity to create even more specialized data structures. With it, one can design their own List, Binary Search Tree, Heap, Splay Tree, Graph, Disjoint Set, and any host of other options.

"Why not use Node for tree structures?" one might ask. Well, the Node class contains things that won't be relevant to one's custom data structure. As such, it can be helpful to construct one's own node type when building tree structures.

From here, one can then create their own structures with specific features, limited only by their imagination.

Most languages offer an enumeration type option. GDScript is no different, but unlike most other languages, it allows one to use either integers or strings for the enum values (the latter only when using the @export_enum annotation in GDScript). The question then arises, "which should one use?"

The short answer is, "whichever you are more comfortable with." This is a feature specific to GDScript and not Godot scripting in general; The languages prioritizes usability over performance.

On a technical level, integer comparisons (constant-time) will happen faster than string comparisons (linear-time). If one wants to keep up other languages' conventions though, then one should use integers.

The primary issue with using integers comes up when one wants to print an enum value. As integers, attempting to print MY_ENUM will print 5 or what-have-you, rather than something like "MyEnum". To print an integer enum, one would have to write a Dictionary that maps the corresponding string value for each enum.

If the primary purpose of using an enum is for printing values and one wishes to group them together as related concepts, then it makes sense to use them as strings. That way, a separate data structure to execute on the printing is unnecessary.

Under what circumstances should one use each of Godot's animation classes? The answer may not be immediately clear to new Godot users.

AnimatedTexture is a texture that the engine draws as an animated loop rather than a static image. Users can manipulate...

the rate at which it moves across each section of the texture (FPS).

the number of regions contained within the texture (frames).

Godot's RenderingServer then draws the regions in sequence at the prescribed rate. The good news is that this involves no extra logic on the part of the engine. The bad news is that users have very little control.

Also note that AnimatedTexture is a Resource unlike the other Node objects discussed here. One might create a Sprite2D node that uses AnimatedTexture as its texture. Or (something the others can't do) one could add AnimatedTextures as tiles in a TileSet and integrate it with a TileMapLayer for many auto-animating backgrounds that all render in a single batched draw call.

The AnimatedSprite2D node, in combination with the SpriteFrames resource, allows one to create a variety of animation sequences through spritesheets, flip between animations, and control their speed, regional offset, and orientation. This makes them well-suited to controlling 2D frame-based animations.

If one needs to trigger other effects in relation to animation changes (for example, create particle effects, call functions, or manipulate other peripheral elements besides the frame-based animation), then one will need to use an AnimationPlayer node in conjunction with the AnimatedSprite2D.

AnimationPlayers are also the tool one will need to use if they wish to design more complex 2D animation systems, such as...

Cut-out animations: editing sprites' transforms at runtime.

2D Mesh animations: defining a region for the sprite's texture and rigging a skeleton to it. Then one animates the bones which stretch and bend the texture in proportion to the bones' relationships to each other.

While one needs an AnimationPlayer to design each of the individual animation sequences for a game, it can also be useful to combine animations for blending, i.e. enabling smooth transitions between these animations. There may also be a hierarchical structure between animations that one plans out for their object. These are the cases where the AnimationTree shines. One can find an in-depth guide on using the AnimationTree here.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Object
class_name TreeNode

var _parent: TreeNode = null
var _children := []

func _notification(p_what):
    match p_what:
        NOTIFICATION_PREDELETE:
            # Destructor.
            for a_child in _children:
                a_child.free()
```

Example 2 (swift):
```swift
using Godot;
using System.Collections.Generic;

// Can decide whether to expose getters/setters for properties later
public partial class TreeNode : GodotObject
{
    private TreeNode _parent = null;

    private List<TreeNode> _children = [];

    public override void _Notification(int what)
    {
        switch (what)
        {
            case NotificationPredelete:
                foreach (TreeNode child in _children)
                {
                    node.Free();
                }
                break;
        }
    }
}
```

---

## Logic preferences — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/logic_preferences.html

**Contents:**
- Logic preferences
- Adding nodes and changing properties: which first?
- Loading vs. preloading
- Large levels: static vs. dynamic
- User-contributed notes

Ever wondered whether one should approach problem X with strategy Y or Z? This article covers a variety of topics related to these dilemmas.

When initializing nodes from a script at runtime, you may need to change properties such as the node's name or position. A common dilemma is, when should you change those values?

It is the best practice to change values on a node before adding it to the scene tree. Some property's setters have code to update other corresponding values, and that code can be slow! For most cases, this code has no impact on your game's performance, but in heavy use cases such as procedural generation, it can bring your game to a crawl.

For these reasons, it is usually best practice to set the initial values of a node before adding it to the scene tree. There are some exceptions where values can't be set before being added to the scene tree, like setting global position.

In GDScript, there exists the global preload method. It loads resources as early as possible to front-load the "loading" operations and avoid loading resources while in the middle of performance-sensitive code.

Its counterpart, the load method, loads a resource only when it reaches the load statement. That is, it will load a resource in-place which can cause slowdowns when it occurs in the middle of sensitive processes. The load() function is also an alias for ResourceLoader.load(path) which is accessible to all scripting languages.

So, when exactly does preloading occur versus loading, and when should one use either? Let's see an example:

Preloading allows the script to handle all the loading the moment one loads the script. Preloading is useful, but there are also times when one doesn't wish for it. To distinguish these situations, there are a few things one can consider:

If one cannot determine when the script might load, then preloading a resource, especially a scene or script, could result in further loads one does not expect. This could lead to unintentional, variable-length load times on top of the original script's load operations.

If something else could replace the value (like a scene's exported initialization), then preloading the value has no meaning. This point isn't a significant factor if one intends to always create the script on its own.

If one wishes only to 'import' another class resource (script or scene), then using a preloaded constant is often the best course of action. However, in exceptional cases, one may wish not to do this:

If the 'imported' class is liable to change, then it should be a property instead, initialized either using an @export or a load() (and perhaps not even initialized until later).

If the script requires a great many dependencies, and one does not wish to consume so much memory, then one may wish to, load and unload various dependencies at runtime as circumstances change. If one preloads resources into constants, then the only way to unload these resources would be to unload the entire script. If they are instead loaded properties, then one can set them to null and remove all references to the resource entirely (which, as a RefCounted-extending type, will cause the resources to delete themselves from memory).

If one is creating a large level, which circumstances are most appropriate? Should they create the level as one static space? Or should they load the level in pieces and shift the world's content as needed?

Well, the simple answer is, "when the performance requires it." The dilemma associated with the two options is one of the age-old programming choices: does one optimize memory over speed, or vice versa?

The naive answer is to use a static level that loads everything at once. But, depending on the project, this could consume a large amount of memory. Wasting users' RAM leads to programs running slow or outright crashing from everything else the computer tries to do at the same time.

No matter what, one should break larger scenes into smaller ones (to aid in reusability of assets). Developers can then design a node that manages the creation/loading and deletion/unloading of resources and nodes in real-time. Games with large and varied environments or procedurally generated elements often implement these strategies to avoid wasting memory.

On the flip side, coding a dynamic system is more complex, i.e. uses more programmed logic, which results in opportunities for errors and bugs. If one isn't careful, they can develop a system that bloats the technical debt of the application.

As such, the best options would be...

To use a static level for smaller games.

If one has the time/resources on a medium/large game, create a library or plugin that can code the management of nodes and resources. If refined over time, so as to improve usability and stability, then it could evolve into a reliable tool across projects.

Code the dynamic logic for a medium/large game because one has the coding skills, but not the time or resources to refine the code (game's gotta get done). Could potentially refactor later to outsource the code into a plugin.

For an example of the various ways one can swap scenes around at runtime, please see the "Change scenes manually" documentation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# my_buildings.gd
extends Node

# Note how constant scripts/scenes have a different naming scheme than
# their property variants.

# This value is a constant, so it spawns when the Script object loads.
# The script is preloading the value. The advantage here is that the editor
# can offer autocompletion since it must be a static path.
const BuildingScn = preload("res://building.tscn")

# 1. The script preloads the value, so it will load as a dependency
#    of the 'my_buildings.gd' script file. But, because this is a
#    property rather than a constant, the object won't copy the preloaded
#    PackedScene resource into the property until the script instantiates
#    with .new().
#
# 2. The preloaded value is inaccessible from the Script object alone. As
#    such, preloading the value here actually does not benefit anyone.
#
# 3. Because the user exports the value, if this script stored on
#    a node in a scene file, the scene instantiation code will overwrite the
#    preloaded initial value anyway (wasting it). It's usually better to
#    provide null, empty, or otherwise invalid default values for exports.
#
# 4. It is when one instantiates this script on its own with .new() that
#    one will load "office.tscn" rather than the exported value.
@export var a_building : PackedScene = preload("office.tscn")

# Uh oh! This results in an error!
# One must assign constant values to constants. Because `load` performs a
# runtime lookup by its very nature, one cannot use it to initialize a
# constant.
const OfficeScn = load("res://office.tscn")

# Successfully loads and only when one instantiates the script! Yay!
var office_scn = load("res://office.tscn")
```

Example 2 (gdscript):
```gdscript
using Godot;

// C# and other languages have no concept of "preloading".
public partial class MyBuildings : Node
{
    //This is a read-only field, it can only be assigned when it's declared or during a constructor.
    public readonly PackedScene Building = ResourceLoader.Load<PackedScene>("res://building.tscn");

    public PackedScene ABuilding;

    public override void _Ready()
    {
        // Can assign the value during initialization.
        ABuilding = GD.Load<PackedScene>("res://Office.tscn");
    }
}
```

Example 3 (php):
```php
using namespace godot;

class MyBuildings : public Node {
    GDCLASS(MyBuildings, Node)

public:
    const Ref<PackedScene> building = ResourceLoader::get_singleton()->load("res://building.tscn");
    Ref<PackedScene> a_building;

    virtual void _ready() override {
        // Can assign the value during initialization.
        a_building = ResourceLoader::get_singleton()->load("res://office.tscn");
    }
};
```

---
