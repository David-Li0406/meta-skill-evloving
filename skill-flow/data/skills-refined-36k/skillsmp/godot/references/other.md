# Godot - Other

**Pages:** 131

---

## All classes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/index.html

**Contents:**
- All classes
- Globals
- Nodes
- Resources
- Other objects
- Editor-only
- Variant types

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

## Best practices — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html

**Contents:**
- Best practices

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

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

## Using the XR editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/using_the_xr_editor.html

**Contents:**
- Using the XR editor
- XR devices support
- Runtime Permissions
- Tips & Tricks
- Limitations & known issues
- User-contributed notes

In 2024, we introduced the Godot XR editor, a version of the Godot editor designed to run natively on XR devices, enabling the creation, development and export of 2D, 3D, and XR apps and games directly on device.

The app can be downloaded from the Meta Horizon Store, or from the Godot download page.

The XR editor is in early access, while we continue to refine the experience. See Limitations & known issues below.

For now, the Godot XR editor is only available for the following Meta Quest devices running Meta Horizon OS v69 or higher:

We are working to add support for more XR devices, including PCVR devices.

All files access permission: Enables the editor to create, import, and read project files from any file locations on the device. Without this permission, the editor is still functional, but has limited access to the device's files and directories.

REQUEST_INSTALL_PACKAGES: Enables the editor to install exported project APKs.

RECORD_AUDIO: Requested when the audio/driver/enable_input project setting is enabled.

USE_SCENE: Required to enable and access the scene APIs when running an XR project.

For the best experience and high level of productivity, connecting a bluetooth keyboard & mouse is recommended to interact with the XR editor. The XR editor supports all of the usual shortcuts and key mappings.

When interacting with tracked controllers or tracked hands, you can toggle on the interface/touchscreen/enable_long_press_as_right_click editor setting to enable right-click by long press.

When interacting with tracked controllers or tracked hands, you can increase the size of the scrollbar using the interface/touchscreen/increase_scrollbar_touch_area editor setting.

Theater View can be used to fullscreen the Editor window.

Enable Seamless Multitasking, available in the Quest Experimental Settings, to enable the ability to quickly transition between a running XR project and the Editor window.

When developing a non-XR project, the Godot editor app icon will provide the ability to switch between the Editor window and the Play window when the latter is active, using Quest's App menu feature.

When developing and running an XR project, you can bring back the Editor window by:

Pressing on the Meta button to invoke the menu bar

Clicking on the Godot editor app icon to summon the App menu, and select the Editor window tile.

Syncing projects via Git can be done by downloading an Android Git client. We recommend the Termux terminal, an Android terminal emulator which provides access to common terminal utilities such Git and SSH.

Note: To use Git with the Termux terminal, you'll need to grant WRITE permission to the terminal. This can be done by running the following command from within the terminal: termux-setup-storage

GDExtension plugins work as expected, but require the plugin developer to provide native Android binaries.

Here are the known limitations and issues of the XR editor:

No Meta Quest 2 support due to the limited amount of memory on the device. However advanced users can grab the XR editor APK from the download page and sideload it onto their device if they desire to do so.

No gradle build support.

No support for Android plugins as they require gradle build support. GDExtension plugins are supported.

No support for external script editors.

While available, the Vulkan Forward+ renderer is not recommended due to severe performance issues.

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

## Customizing the interface — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/customizing_editor.html

**Contents:**
- Customizing the interface
- Moving and resizing docks
- Splitting the script or shader editor to its own window
- Customizing editor layouts
- Customizing editor settings
- User-contributed notes

Godot's interface lives in a single window by default. Since Godot 4.0, you can split several elements to separate windows to better make use of multi-monitor setups.

Click and drag on the edge of any dock or panel to resize it horizontally or vertically:

Resizing a dock in the editor

Click the "3 vertical dots" icon at the top of any dock to change its location, or split it to a separate window by choosing Make Floating in the submenu that appears:

Moving a dock in the editor

To move a floating dock back to the editor window, close the dock window using the × button in the top-right corner of the window (or in the top-left corner on macOS). Alternatively, you can press Alt + F4 while the split window is focused.

This feature is only available on platforms that support spawning multiple windows: Windows, macOS and Linux.

This feature is also not available if Single Window Mode is enabled in the Editor Settings.

Since Godot 4.1, you can split the script or shader editor to its own window.

To split the script editor to its own window, click the corresponding button in the top-right corner of the script editor:

Splitting the script editor to its own window

To split the shader editor to its own window, click the corresponding button in the top-right corner of the script editor:

Splitting the shader editor to its own window

To go back to the previous state (with the script/shader editor embedded in the editor window), close the split window using the × button in the top-right corner of the window (or in the top-left corner on macOS). Alternatively, you can press Alt + F4 while the split window is focused.

You may want to save and load a dock configuration depending on the kind of task you're working on. For instance, when working on animating a character, it may be more convenient to have docks laid out in a different fashion compared to when you're designing a level.

For this purpose, Godot provides a way to save and restore editor layouts. Before saving a layout, make changes to the docks you'd like to save. The following changes are persisted to the saved layout:

Making a dock floating.

Changing a floating dock's position or size.

FileSystem dock properties: split mode, display mode, sorting order, file list display mode, selected paths and unfolded paths.

Splitting the script or shader editor to its own window is not persisted as part of a layout.

After making changes, open the Editor menu at the top of the editor then choose Editor Layouts > Save. Enter a name for the layout, then click Save. If you've already saved an editor layout, you can choose to override an existing layout using the list.

After making changes, open the Editor menu at the top of the editor then choose Editor Layouts. In the dropdown list, you will see a list of saved editor layouts, plus Default which is a hardcoded editor layout that can't be removed. The default layout matches a fresh Godot installation with no changes made to the docks' positions and sizes, and no floating docks.

You can remove a layout using the Delete option in the Editor Layouts dropdown.

If you name the saved layout Default (case-sensitive), the default editor layout will be overwritten. Note that the Default does not appear in the list of layouts to overwrite until you overwrite it once, but you can still write its name manually.

You can go back to the standard default layout by removing the Default layout after overriding it. (This option does not appear if you haven't overridden the default layout yet.)

Editor layouts are saved to a file named editor_layouts.cfg in the configuration path of the Editor data paths.

In the Editor menu at the top of the editor, you can find an Editor Settings option. This opens a window similar to the Project Settings, but with settings used by the editor. These settings are shared across all projects and are not saved in the project files.

The Editor Settings window

Some commonly changed settings are:

Interface > Editor > Editor Language: Controls the language the editor displays in. To make English tutorials easier to follow, you may want to change this to English so that menu names are identical to names referred to by tutorials. The language can also be changed in the top-right corner of the project manager.

Interface > Editor > Display Scale: Controls how large UI elements display on screen. The default Auto setting finds a suitable value based on your display's DPI and resolution. Due to engine limitations, it only takes the display-provided scaling factor on macOS, not on Windows or Linux.

Interface > Editor > Single Window Mode: If enabled, this forces the editor to use a single window. This disables certain features such as splitting the script/shaders editor to their own window. Single-window mode can be more stable, especially on Linux when using Wayland.

Interface > Theme > Preset: The editor theme preset to use. The Light theme preset may be easier to read if you're outdoors or in a room with sunlight. The Black (OLED) preset can reduce power consumption on OLED displays, which are increasingly common in laptops and phones/tablets.

FileSystem > Directories > Autoscan Project Path: This can be set to a folder path that will be automatically scanned for projects in the project manager every time it starts.

FileSystem > Directories > Default Project Path: Controls the default location where new projects are created in the project manager.

Editors > 3D > Emulate Numpad: This allows using the top row 0-9 keys in the 3D editor as their equivalent numpad keys. It's recommended to enable this option if you don't have a number pad on your keyboard.

Editors > 3D > Emulate 3 Button Mouse: This allows using the pan, zoom and orbit modifiers in the 3D editor even when not holding down any mouse button. It's recommended to enable this option if you're using a trackpad.

See the EditorSettings class reference for a complete description of most editor settings. You can also hover an editor setting's name with the mouse in the Editor Settings to show its description.

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

## Managing editor features — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/managing_editor_features.html

**Contents:**
- Managing editor features
- Introduction
- Creating a profile
- Sharing a profile
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

In certain situations, it may be desirable to limit what features can be used in the Godot editor. For example, a UI designer on a team who doesn't need to see 3D features, or an educator slowly introducing features to students. Godot has a built-in system called "feature profiles" to do this.

With feature profiles, major features and nodes can be hidden from the editor. This only hides parts of the interface and does not actually remove support for these features, so scenes and scripts relying on those features will still work fine. This also means feature profiles are not an optimization technique. For information on how to optimize Godot see Performance.

To manage editor features go to Editor > Manage Editor Features. This will open the Manage Editor Feature Profiles window. By default there will be no profile. Click on Create Profile and give it a name. You will then see a list of all the features in the Godot editor.

The first section allows major editor features to be removed, such as the 3D editor or scripting editor. Below the main features is every class and node in Godot, which can be disabled as well. Click on a node and all of its properties and options will be listed in the Extra Items box, these can all be individually disabled.

To share profiles between editors click on the Export button. Save the custom profile somewhere as a .profile file. To use this in another editor open that editor's Manage Editor Feature Profiles window and click import, then select the .profile file.

This process is potentially cumbersome however if a large amount of computers need custom profiles. As an alternative, you can enable self-contained mode for Godot, which allows putting all editor configuration in the same folder as the editor binary. See Self-contained mode for details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Upgrading from Godot 3 to Godot 4 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html

**Contents:**
- Upgrading from Godot 3 to Godot 4
- Should I upgrade to Godot 4?
  - Advantages of upgrading
  - Disadvantages of upgrading
  - Caveats of upgrading
- Preparing before the upgrade (optional)
- Running the project upgrade tool
  - Using the Project Manager
  - Using the command line
- Fixing the project after running the project upgrade tool

Before beginning the upgrade process, it's worth thinking about the advantages and disadvantages that upgrading would bring to your project.

Along with the new features present in 4.0, upgrading gives the following advantages:

Many bugs are fixed in 4.0, but cannot be resolved in 3.x for various reasons (such as graphics API differences or backwards compatibility).

4.x will enjoy a longer support period. Godot 3.x will continue to be supported for some time after 4.0 is released, but it will eventually stop receiving support.

See Documentation changelog for a list of pages documenting new features in Godot 4.0, and List of features for a list of all features in Godot.

If you don't need any features present in Godot 4.x, you may want to stay on Godot 3.x for the following reasons:

Godot 4's baseline hardware requirements (such as memory usage) are slightly higher, both for the editor and exported projects. This was required for the implementation of some core optimizations.

Since Godot 4 includes more features than Godot 3, Godot 4's binary size for exported projects is larger. While this can be mitigated by optimizing a build for size, a 4.0 build with a given set of enabled modules will remain larger compared to a 3.x build with the same modules. This can be an issue for exporting to the Web, as binary size directly influences how fast the engine can initialize (regardless of download speed).

Godot 4 does not and will not have support for GLES2 rendering. (There is still support for GLES3 rendering using the new Compatibility renderer, which means that devices without Vulkan support can still run Godot 4.)

If you are targeting very old hardware such as Intel Sandy Bridge (2nd generation) integrated graphics, this will prevent the project from running on such hardware after upgrading. Software OpenGL implementations can be used to bypass this limitation, but they're too slow for gaming.

Since Godot 4 is a complete rewrite in many aspects, some features have unfortunately been lost in the process. Some of these features may be restored in future Godot releases:

Bullet physics was removed in favor of GodotPhysics. This only affects 3D projects that used the default physics engine (which was Bullet) and didn't manually change it to GodotPhysics. There are no plans to re-add Bullet physics in core, but a third-party add-on could be created for it thanks to GDExtension.

By default, rendering in 2D is no longer performed in HDR, which means "overbright" modulate values have no visible effect. Since Godot 4.2, you can enable the project setting HDR 2D to perform 2D rendering in HDR. See also Using glow in 2D.

While rendering still happens in HDR in 3D when using the Forward+ or Mobile renderers, Viewports cannot return HDR data anymore. This is planned to be restored at some point in the future.

Mono was replaced by .NET 6. This means exporting C# projects to Android, iOS and HTML5 is no longer supported for now. Exporting C# projects to desktop platforms is still supported, and as of 4.2 there's experimental support for exporting to mobile platforms. Support for exporting C# projects to more platforms will be restored in future 4.x releases as upstream support improves.

You can find a more complete list of functional regressions by searching for issues labeled "regression" but not "bug" on GitHub.

If you want to be ready to upgrade to Godot 4 in the future, consider using Tweener and the Time singleton in your project. These classes are both available in Godot 3.5 and later.

This way, you won't be relying on the deprecated Tween node and OS time functions, both of which are removed in Godot 4.0.

It's also a good idea to rename external shaders so that their extension is .gdshader instead of .shader. Godot 3.x supports both extensions, but only .gdshader is supported in Godot 4.0.

Make a full backup of your project before upgrading! The project upgrade tool will not perform any backups of the project that is being upgraded.

You can backup a project by using version control, or by copying the project folder to another location.

To use the project upgrade tool:

Open the Godot 4 Project Manager.

Import the Godot 3.x project using the Import button, or use the Scan button to find the project within a folder.

Double-click the imported project (or select the project then choose Edit).

You will see a dialog appearing with two options: Convert project.godot Only and Convert Full Project. After ensuring your project is backed up (see the above warning), choose Convert Full Project. Convert project.godot Only is intended to be used for advanced use cases only, in case the conversion tool fails.

Wait until the project conversion process finishes. This can take up to a few minutes for large projects with lots of scenes.

When the Project Manager interface becomes available again, double-click the project (or select the project then choose Edit) to open it in the editor.

If you hit conversion issues due to some project files being too large or long, you can use the command line to upgrade the project (see below). This will allow you to override the converter's size limits.

To use the project upgrade tool from the command line, it's recommended to validate the project conversion by running the Godot editor binary with the following arguments:

If the list of planned upgrades looks good to you, run the following command on the Godot editor binary to upgrade project files:

[<max_file_kb>] and [<max_line_size>] are optional arguments to specify the maximum size of files to be converted (in kilobytes and lines). The default limits are 4 MB and 100,000 lines respectively. If a file hits either of those limits, it will not be upgraded by the project converter. This is useful to prevent large resources from slowing down the upgrade to a crawl.

If you still want large files to be converted by the project upgrade tool, increase the size limits when running the project upgrade tool. For example, running the Godot editor binary with those arguments increases both limits by a 10× factor:

Only Godot 3.0 and later projects can be upgraded using the project conversion tool found in the Godot 4 editor.

It's recommended to ensure that your project is up-to-date with the latest 3.x stable release before running the project upgrade tool.

After upgrading the project, you may notice that certain things don't look as they should. Scripts will likely contain various errors as well (possibly hundreds in large projects). This is because the project upgrade tool cannot cater to all situations. Therefore, a large part of the upgrade process remains manual.

The list below refers to nodes which were simply renamed for consistency or clarity in Godot 4.0. The project upgrade tool renames them automatically in your scripts.

One noteworthy set of renames is 3D nodes, which all got a 3D suffix added for consistency with their 2D counterparts. For example, Area is now Area3D.

For ease of searching, this table lists all nodes and resources that were renamed and are automatically converted, excluding the ones which only involved adding a 3D suffix to the old name:

ARVRPositionalTracker

EditorSpatialGizmoPlugin

EditorNode3DGizmoPlugin

NavigationMeshInstance

NavigationPolygonInstance

ParticleProcessMaterial

Physics2DDirectBodyState

PhysicsDirectBodyState2D

Physics2DDirectSpaceState

PhysicsDirectSpaceState2D

Physics2DShapeQueryParameters

PhysicsShapeQueryParameters2D

Physics2DTestMotionResult

PhysicsTestMotionResult2D

VisibleOnScreenEnabler3D

VisibleOnScreenNotifier3D

VisibleOnScreenNotifier2D

VisibleOnScreenNotifier3D

VisualShaderNodeScalarConstant

VisualShaderNodeFloatConstant

VisualShaderNodeScalarFunc

VisualShaderNodeFloatFunc

VisualShaderNodeScalarOp

VisualShaderNodeFloatOp

VisualShaderNodeScalarClamp

VisualShaderNodeClamp

VisualShaderNodeVectorClamp

VisualShaderNodeClamp

VisualShaderNodeScalarInterp

VisualShaderNodeVectorInterp

VisualShaderNodeVectorScalarMix

VisualShaderNodeScalarSmoothStep

VisualShaderNodeSmoothStep

VisualShaderNodeVectorSmoothStep

VisualShaderNodeSmoothStep

VisualShaderNodeVectorScalarSmoothStep

VisualShaderNodeSmoothStep

VisualShaderNodeVectorScalarStep

VisualShaderNodeScalarSwitch

VisualShaderNodeSwitch

VisualShaderNodeScalarTransformMult

VisualShaderNodeTransformOp

VisualShaderNodeScalarDerivativeFunc

VisualShaderNodeDerivativeFunc

VisualShaderNodeVectorDerivativeFunc

VisualShaderNodeDerivativeFunc

VisualShaderNodeBooleanUniform

VisualShaderNodeBooleanParameter

VisualShaderNodeColorUniform

VisualShaderNodeColorParameter

VisualShaderNodeScalarUniform

VisualShaderNodeFloatParameter

VisualShaderNodeCubeMapUniform

VisualShaderNodeCubeMapParameter

VisualShaderNodeTextureUniform

VisualShaderNodeTexture2DParameter

VisualShaderNodeTextureUniformTriplanar

VisualShaderNodeTextureParameterTriplanar

VisualShaderNodeTransformUniform

VisualShaderNodeTransformParameter

VisualShaderNodeVec3Uniform

VisualShaderNodeVec3Parameter

VisualShaderNodeUniform

VisualShaderNodeParameter

VisualShaderNodeUniformRef

VisualShaderNodeParameterRef

Due to how the project upgrade tool works, not all API renames can be performed automatically. The list below contains all renames that must be performed manually using the script editor.

If you cannot find a node or resource in the list below, refer to the above table to find its new name.

You can use the Replace in Files dialog to speed up replacement by pressing Ctrl + Shift + R while the script editor is open. However, be careful as the Replace in Files dialog doesn't offer any way to undo a replacement. Use version control to commit your upgrade work regularly. Command line tools such as sd can also be used if you need something more flexible than the editor's Replace in Files dialog.

If using C#, remember to search for outdated API usage with PascalCase notation in the project (and perform the replacement with PascalCase notation).

File and Directory classes were replaced by FileAccess and DirAccess, which have an entirely different API. Several methods are now static, which means you can call them directly on FileAccess or DirAccess without having to create an instance of that class.

Screen and window-related methods from the OS singleton (such as OS.get_screen_size()) were moved to the DisplayServer singleton. Method naming was also changed to use the DisplayServer.<object>_<get/set>_property() form instead. For example, OS.get_screen_size() becomes DisplayServer.screen_get_size().

Time and date methods from the OS singleton were moved to the Time singleton. (The Time singleton is also available in Godot 3.5 and later.)

You may have to replace some instance() calls with instantiate(). The converter should handle this automatically, but this relies on custom code that may not work in 100% of situations.

AcceptDialog's set_autowrap() is now set_autowrap_mode().

AnimationNode's process() is now _process() (note the leading underscore, which denotes a virtual method).

AnimationPlayer's add_animation() is now add_animation_library() and now uses an AnimationLibrary.

AnimationTree's set_process_mode() is now set_process_callback().

Array's empty() is now is_empty().

Array's invert() is now reverse().

Array's remove() is now remove_at().

AStar2D and AStar3D's get_points() is now get_points_id().

BaseButton's set_event() is now set_shortcut().

Camera2D's get_h_offset() is now get_drag_horizontal_offset().

Camera2D's get_v_offset() is now get_drag_vertical_offset().

Camera2D's set_h_offset() is now set_drag_horizontal_offset().

Camera2D's set_v_offset() is now set_drag_vertical_offset().

CanvasItem's raise() is now move_to_front().

CanvasItem's update() is now queue_redraw().

Control's get_stylebox() is now get_theme_stylebox().

Control's set_tooltip() is now set_tooltip_text().

EditorNode3DGizmoPlugin's create_gizmo() is now _create_gizmo() (note the leading underscore, which denotes a virtual method).

ENetMultiplayerPeer's get_peer_port() is now get_peer().

FileDialog's get_mode() is now get_file_mode().

FileDialog's set_mode() is now set_file_mode().

GraphNode's get_offset() is now get_position_offset().

GridMap's map_to_world() is now map_to_local().

GridMap's world_to_map() is now local_to_map().

Image's get_rect() is now get_region().

ImmediateGeometry's set_normal() is now surface_set_normal().

ImmediateMesh's set_color() is now surface_set_color().

ImmediateMesh's set_uv() is now surface_set_uv().

ItemList's get_v_scroll() is now get_v_scroll_bar().

MultiPlayerAPI's get_network_connected_peers() is now get_peers().

MultiPlayerAPI's get_network_peer() is now get_peer().

MultiPlayerAPI's get_network_unique_id() is now get_unique_id().

MultiPlayerAPI's has_network_peer() is now has_multiplayer_peer().

MultiplayerAPI's is_refusing_new_network_connections() is now is_refusing_new_connections().

PacketPeerUDP's is_listening() is now is_bound().

PacketPeerUDP's listen() is now bind().

ParticleProcessMaterial's set_flag() is now set_particle_flag().

PhysicsTestMotionResult2D's get_motion() is now get_travel().

RenderingServer's get_render_info() is now get_rendering_info().

ResourceFormatLoader's get_dependencies() is now _get_dependencies() (note the leading underscore, which denotes a virtual method).

ResourceFormatLoader's load() is now _load().

SceneTree's change_scene() is now change_scene_to_file().

Shortcut's is_valid() is now has_valid_event().

TileMap's map_to_world() is now map_to_local().

TileMap's world_to_map() is now local_to_map().

Transform2D's xform() is mat * vec and xform_inv() is vec * mat.

XRPositionalTracker's get_name() is now get_tracker_name().

XRPositionalTracker's get_type() is now get_tracker_type().

XRPositionalTracker's _set_name() is now get_tracker_name().

If a property is listed here, its associated getter and setter methods must also be renamed manually if used in the project. For example, PathFollow2D and PathFollow3D's set_offset() and get_offset() must be renamed to set_progress() and get_progress() respectively.

AudioServer's device is now output_device.

BaseButton's group is now button_group.

Camera3D's zfar is now far.

Camera3D's znear is now near

Control's margin is now offset.

InputEventMouseButton's doubleclick is now double_click.

InputEventWithModifiers's alt is now alt_pressed.

InputEventWithModifiers's command is now command_pressed.

InputEventWithModifiers's control is now ctrl_pressed.

InputEventWithModifiers's meta is now meta_pressed.

InputEventWithModifiers's shift is now shift_pressed.

Label's percent_visible is now visible_ratio.

MultiPlayerAPI's refuse_new_network_connections is now refuse_new_connections.

Node's filename is now scene_file_path.

PathFollow2D's rotate is now rotates.

PathFollow2D and PathFollow3D's offset is now progress.

RectangleShape2D's extents is now size

TextureProgressBar's percent_visible is now show_percentage.

Theme's off is now unchecked.

Theme's ofs is now offset.

Theme's on is now checked.

Window's window_title is now title.

WorldMarginShape2D's d is now distance.

The extents property on CSG nodes and VoxelGI will have to be replaced with size, with the set value halved (as they're no longer half-extents). This also affects its setter/getter methods set_extents() and get_extents().

The Engine.editor_hint property was removed in favor of the Engine.is_editor_hint() method. This is because it's read-only, and properties in Godot are not used for read-only values.

CPUParticles2D's FLAG_MAX is now PARTICLE_FLAG_MAX.

FileSystemDock's instantiate is now instance.

CanvasItem's hide is now hidden. This rename does not apply to the hide() method, only the signal.

Tween's tween_all_completed is now loop_finished.

EditorSettings' changed is now settings_changed.

Color names are now uppercase and use underscores between words. For example, Color.palegreen is now Color.PALE_GREEN.

MainLoop's NOTIFICATION_ constants were duplicated to Node which means you can remove the MainLoop. prefix when referencing them.

MainLoop's NOTIFICATION_WM_QUIT_REQUEST is now NOTIFICATION_WM_CLOSE_REQUEST.

Several project settings were renamed, and some of them had their enums changed in incompatible ways (such as shadow filter quality). This means you may need to set some project settings' values again. Make sure the Advanced toggle is enabled in the project settings dialog so you can see all project settings.

Graphics quality settings were moved from Environment properties to project settings. This was done to make runtime quality adjustments easier, without having to access the currently active Environment resource then modify its properties.

As a result, you will have to configure Environment quality settings in the project settings as old Environment quality settings aren't converted automatically to project settings.

If you have a graphics settings menu that changed environment properties in Godot 3.x, you will have to change its code to call RenderingServer methods that affect environment effects' quality. Only the "base" toggle of each environment effect and its visual knobs remain within the Environment resource.

There have been some changes to shaders that aren't covered by the upgrade tool. You will need to make some manual changes, especially if your shader uses coordinate space transformations or a custom light() function.

The .shader file extension is no longer supported, which means you must rename .shader files to .gdshader and update references accordingly in scene/resource files using an external text editor.

Some notable changes you will need to perform in shaders are:

Texture filter and repeat modes are now set on individual uniforms, rather than the texture files themselves.

hint_albedo is now source_color.

hint_color is now source_color.

Built in matrix variables were renamed.

Particles shaders no longer use the vertex() processor function. Instead they use start() and process().

In the Forward+ and Mobile renderers, normalized device coordinates now have a Z-range of [0.0,1.0] instead of [-1.0,1.0]. When reconstructing NDC from SCREEN_UV and depth, use vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, depth); instead of vec3 ndc = vec3(SCREEN_UV, depth) * 2.0 - 1.0;. The Compatibility renderer is unchanged, using the same NDC Z-range as 3.x.

The lighting model changed. If your shader has a custom light() function, you may need to make changes to get the same visual result.

In 4.3 and up, the reverse Z depth buffer technique is now implemented, which may break advanced shaders. See Introducing Reverse Z (AKA I'm sorry for breaking your shader).

See Shading language for more information.

This list is not exhaustive. If you made all the changes mentioned here and your shader still doesn't work, try asking for help in one of the community channels.

Some changes performed between Godot 3.x and 4 are not renames, but they still break backwards compatibility due to different default behavior.

The most notable examples of this are:

Lifecycle functions such as _ready() and _process() no longer implicitly call parent classes' functions that have the same name. Instead, you must use super() at the top of a lifecycle function in the child class so that the parent class function is called first.

Both String and StringName are now exposed to GDScript. This allows for greater optimization, as StringName is specifically designed to be used for "constant" strings that are created once and reused many times. These types are not strictly equivalent to each other, which means is_same("example", &"example") returns false. Although in most cases they are interchangeable ("example" == &"example" returns true), sometimes you may have to replace "example" with &"example".

GDScript setter and getter syntax was changed, but it's only partially converted by the conversion tool. In most cases, manual changes are required to make setters and getters working again.

GDScript signal connection syntax was changed. The conversion tool will use the string-based syntax which is still present in Godot 4, but it's recommended to switch to the Signal-based syntax described on the linked page. This way, strings are no longer involved, which avoids issues with signal name errors that can only be discovered at runtime.

Built-in scripts that are tool scripts do not get the tool keyword converted to the @tool annotation.

The Tween node was removed in favor of Tweeners, which are also available in Godot 3.5 and later. See the original pull request for details.

randomize() is now automatically called on project load, so deterministic randomness with the global RandomNumberGenerate instance requires manually setting a seed in a script's _ready() function.

call_group(), set_group() and notify_group() are now immediate by default. If calling an expensive function, this may result in stuttering when used on a group containing a large number of nodes. To use deferred calls like before, replace call_group(...) with call_group_flags(SceneTree.GROUP_CALL_DEFERRED, ...) (and do the same with set_group() and notify_group() respectively).

Instead of rotation_degrees, the rotation property is exposed to the editor, which is automatically displayed as degrees in the Inspector dock. This may break animations, as the conversion is not handled automatically by the conversion tool.

AABB's has_no_surface() was inverted and renamed to has_surface().

AABB and Rect2's has_no_area() was inverted and renamed to has_area().

AnimatedTexture's fps property was replaced by speed_scale, which works the same as AnimationPlayer's playback_speed property.

AnimatedSprite2D and AnimatedSprite3D now allow negative speed_scale values. This may break animations if you relied on speed_scale being internally clamped to 0.0.

AnimatedSprite2D and AnimatedSprite3D's playing property was removed. Use play()/stop() method instead OR configure autoplay animation via the SpriteFrames bottom panel (but not both at once).

Array's slice() second parameter (end) is now exclusive, instead of being inclusive. For example, this means that [1, 2, 3].slice(0, 1) now returns [1] instead of [1, 2].

BaseButton's signals are now button_up and button_down. The pressed property is now button_pressed.

Camera2D's rotating property was replaced by ignore_rotation, which has inverted behavior.

Camera2D's zoom property was inverted: higher values are now more zoomed in, instead of less.

Node's remove_and_skip() method was removed. If you need to reimplement it in a script, you can use the old C++ implementation as a reference.

OS.get_system_time_secs() should be converted to Time.get_time_dict_from_system()["second"].

ResourceSaver's save() method now has its arguments swapped around (resource: Resource, path: String). This also applies to ResourceFormatSaver's _save() method.

A StreamPeerTCP must have poll() called on it to update its state, instead of relying on get_status() automatically polling: GH-59582

String's right() method has changed behavior: it now returns a number of characters from the right of the string, rather than the right side of the string from a given position. If you need the old behavior, you can use substr() instead.

is_connected_to_host() was removed from StreamPeerTCP and PacketPeerUDP as per GH-59582. get_status() can be used in StreamPeerTCP instead. is_socket_connected() can be used in PacketPeerUDP instead.

In _get_property_list(), the or_lesser property hint string is now or_less.

In _get_property_list(), the noslider property hint string is now no_slider.

VisualShaderNodeVec4Parameter now takes a Vector4 as parameter instead of a Quaternion.

Removed or replaced nodes/resources

This lists all nodes that were replaced by another node requiring different configuration. The setup must be done from scratch again, as the project converter doesn't support updating existing setups:

Closest approximation

AnimationTreePlayer was deprecated since Godot 3.1.

See Using Lightmap global illumination.

Camera's pyramid shape was moved to :ref:'class_Camera3D'.

Replaced by other 2D Navigation nodes.

Replaced by other 3D Navigation nodes.

Has different parameters and more noise types such as cellular. No support for 4D noise as it's absent from the FastNoiseLite library.

ToolButton was Button with the Flat property enabled by default.

CanvasItem has a new Y Sort Enabled property in 4.0.

VisibleOnScreenNotifier3D can act as a replacement.

Portal and room occlusion culling was replaced by raster occlusion culling (OccluderInstance3D node), which requires a different setup process.

Geometry occlusion culling was replaced by raster occlusion culling (OccluderInstance3D node), which requires a different setup process.

If loading an old project, the node will be replaced with its Closest approximation automatically (even if not using the project upgrade tool).

Threading APIs have changed in 4.0. For example, the following code snippet in Godot 3.x must be modified to work in 4.0:

Thread.is_active() is no longer used and should be converted to Thread.is_alive().

See the changelog for a full list of changes between Godot 3.x and 4.

If you've saved an ArrayMesh resource to a .res or .tres file, the format used in 4.0 is not compatible with the one used in 3.x. You will need to go through the process of importing the source mesh file and saving it as an ArrayMesh resource again.

The editor/renames_map_3_to_4.cpp source file lists all automatic renames performed by the project upgrade tool. Lines that are commented out refer to API renames that cannot be performed automatically.

Godot 3.x and 4.0 use different editor settings files. This means their settings can be changed independently from each other.

If you wish to port over your Godot 3.x settings to Godot 4, open the editor settings folder and copy editor_settings-3.tres to editor_settings-4.tres while the Godot 4 editor is closed.

Many settings' names and categories have changed since Godot 3.x. Editor settings whose name or category has changed won't carry over to Godot 4.0; you will have to set their values again.

Godot 3.x and 4.x have entirely different lists of files and folders that should be ignored by your version control system.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# [<max_file_kb>] [<max_line_size>] are optional arguments.
# Remove them if you aren't changing their values.
path/to/godot.binary --path /path/to/project/folder --validate-conversion-3to4 [<max_file_kb>] [<max_line_size>]
```

Example 2 (markdown):
```markdown
# [<max_file_kb>] [<max_line_size>] are optional arguments.
# Remove them if you aren't changing their values.
path/to/godot.binary --path /path/to/project/folder --convert-3to4 [<max_file_kb>] [<max_line_size>]
```

Example 3 (unknown):
```unknown
path/to/godot.binary --path /path/to/project/folder --convert-3to4 40000 1000000
```

Example 4 (swift):
```swift
# 3.x
var start_success = new_thread.start(self, "__threaded_background_loader",
    [resource_path, thread_num]
)

# 4.0
var start_success = new_thread.start(__threaded_background_loader.bind(resource_path, thread_num))
```

---

## Upgrading from Godot 4.1 to Godot 4.2 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.2.html

**Contents:**
- Upgrading from Godot 4.1 to Godot 4.2
- Breaking changes
  - Core
  - Animation
  - GUI nodes
  - Rendering
  - Text
  - GraphEdit
  - TileMap
  - XR

For most games and apps made with 4.1 it should be relatively safe to migrate to 4.2. This page intends to cover everything you need to pay attention to when migrating your project.

If you are migrating from 4.1 to 4.2, the breaking changes listed here might affect you. Changes are grouped by areas/systems.

The Mesh resource format has changed in 4.2 to allow for vertex and attribute compression. This allows for improved rendering performance, especially on platforms constrained by memory bandwidth such as mobile.

It is still possible to load the Godot 4.0-4.1 Mesh formats, but it is not possible to load the Godot 4.2 Mesh format in prior Godot versions. When opening a Godot project made with a version prior to 4.2, you may be presented with an upgrade dialog that offers two options:

Restart & Upgrade: Upgrades the mesh format for all meshes in the project and saves the result to disk. Once chosen, this option prevents downgrading the project to a Godot version prior to 4.2. Set up a version control system and push your changes before choosing this option!

Upgrade Only: Upgrades the mesh format in-memory without writing it to disk. This allows downgrading the project to a Godot version older than 4.2 if you need to do so in the future. The downside is that loading the project will be slower every time as the mesh format needs to be upgraded every time the project is loaded. These increased loading times will also affect the exported project. The number and complexity of Mesh resources determines how much loading times are affected.

If this dialog doesn't appear, use Project > Tools > Upgrade Mesh Surfaces… at the top of the editor.

This article indicates whether each breaking change affects GDScript and whether the C# breaking change is binary compatible or source compatible:

Binary compatible - Existing binaries will load and execute successfully without recompilation, and the runtime behavior won't change.

Source compatible - Source code will compile successfully without changes when upgrading Godot.

Constant NOTIFICATION_NODE_RECACHE_REQUESTED removed

Method _post_process_key_value moved to base class AnimationMixer

Method add_animation_library moved to base class AnimationMixer

Method advance moved to base class AnimationMixer

Signal animation_finished moved to base class AnimationMixer

Signal animation_started moved to base class AnimationMixer

Signal animation_libraries_updated moved to base class AnimationMixer

Signal animation_list_changed moved to base class AnimationMixer

Property audio_max_polyphony moved to base class AnimationMixer

Signal caches_cleared moved to base class AnimationMixer

Method clear_caches moved to base class AnimationMixer

Method find_animation moved to base class AnimationMixer

Method find_animation_library moved to base class AnimationMixer

Method get_animation moved to base class AnimationMixer

Method get_animation_library moved to base class AnimationMixer

Method get_animation_library_list moved to base class AnimationMixer

Method get_animation_list moved to base class AnimationMixer

Method has_animation moved to base class AnimationMixer

Method has_animation_library moved to base class AnimationMixer

Property method_call_mode renamed to callback_mode_method and moved to base class AnimationMixer

Property playback_active renamed to active and moved to base class AnimationMixer

Property playback_process_mode renamed to callback_mode_process and moved to base class AnimationMixer

Method remove_animation_library moved to base class AnimationMixer

Method rename_animation_library moved to base class AnimationMixer

Property reset_on_save moved to base class AnimationMixer

Property root_node moved to base class AnimationMixer

Method set_reset_on_save_enabled moved to base class AnimationMixer

Method seek adds a new update_only optional parameter

Method _post_process_key_value moved to base class AnimationMixer

Property active moved to base class AnimationMixer

Method advance moved to base class AnimationMixer

Signal animation_finished moved to base class AnimationMixer

Signal animation_started moved to base class AnimationMixer

Property audio_max_polyphony moved to base class AnimationMixer

Method get_root_motion_position moved to base class AnimationMixer

Method get_root_motion_position_accumulator moved to base class AnimationMixer

Method get_root_motion_rotation moved to base class AnimationMixer

Method get_root_motion_rotation_accumulator moved to base class AnimationMixer

Method get_root_motion_scale moved to base class AnimationMixer

Method get_root_motion_scale_accumulator moved to base class AnimationMixer

Property process_callback renamed to callback_mode_process and moved to base class AnimationMixer

Property root_motion_track moved to base class AnimationMixer

Property tree_root changes type from AnimationNode to AnimationRootNode

Method add_icon_shortcut adds a new allow_echo optional parameter

Method add_shortcut adds a new allow_echo optional parameter

Method clear adds a new free_submenus optional parameter

Method add_image adds new key, pad, tooltip, and size_in_percent optional parameters

Method add_surface changes flags parameter type from uint32 to uint64

Method get_surface_format changes return type from uint32 to uint64

Method commit_to_surface adds a new compression_flags optional parameter

Method get_format changes return type from uint32 to uint64

Enum field BarrierMask.BARRIER_MASK_RASTER changes value from 1 to 9

Enum field BarrierMask.BARRIER_MASK_ALL_BARRIERS changes value from 7 to 32767

Enum field BarrierMask.BARRIER_MASK_NO_BARRIER changes value from 8 to 32768

Method shader_create_from_bytecode adds a new placeholder_rid optional parameter

Method shader_get_vertex_input_attribute_ask changes return type from uint32 to uint64

Method commit changes flags parameter type from uint32 to uint64

Method set_fallbacks replaced with fallbacks property

Method get_fallbacks replaced with fallbacks property

Method find_variation adds new spacing_top, spacing_bottom, spacing_space, and spacing_glyph optional parameters

Property arrange_nodes_button_hidden renamed to show_arrange_button

Method get_zoom_hbox renamed to get_menu_hbox

Property snap_distance renamed to snapping_distance

Property use_snap renamed to snapping_enabled

Property comment removed

Signal close_request renamed to delete_request and moved to base class GraphElement

Property draggable moved to base class GraphElement

Property draggable moved to base class GraphElement

Signal dragged moved to base class GraphElement

Method get_connection_input_color removed

Method get_connection_input_count removed

Method get_connection_input_height removed

Method get_connection_input_position removed

Method get_connection_input_slot removed

Method get_connection_input_type removed

Method get_connection_output_color removed

Method get_connection_output_count removed

Method get_connection_output_height removed

Method get_connection_output_position removed

Method get_connection_output_slot removed

Method get_connection_output_type removed

Property language removed

Signal node_deselected moved to base class GraphElement

Signal node_selected moved to base class GraphElement

Property overlay removed

Property position_offset moved to base class GraphElement

Signal position_offset_changed moved to base class GraphElement

Signal raise_request moved to base class GraphElement

Property resizable moved to base class GraphElement

Signal resize_request moved to base class GraphElement

Property selectable moved to base class GraphElement

Property selected moved to base class GraphElement

Property show_close removed

Property text_direction removed

Property cell_quadrant_size renamed to rendering_quadrant_size

Property environment_blend_mode added

This change breaks compatibility in C# because the new property conflicts with the name of an existing enum and the C# bindings generator gives priority to properties, so the enum type was renamed from EnvironmentBlendMode to EnvironmentBlendModeEnum.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Migrating to a new version — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/index.html

**Contents:**
- Migrating to a new version

Godot loosely follows a semantic versioning system, where compatibility is assumed between minor and patch releases, while major releases can break it. As such, it is generally not recommended to move projects between major versions during their development, especially if you've been working on them for a significant amount of time.

Still, new features, usability improvements, or paradigm shifts in engine's internals may incentivize you to upgrade. Below is a list of articles that should assist you when upgrading your project between versions. Each article would try its best to document every important difference and provide you with a migration path.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Upgrading from Godot 4.0 to Godot 4.1 — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.1.html

**Contents:**
- Upgrading from Godot 4.0 to Godot 4.1
- Breaking changes
  - Core
  - Animation
  - 2D nodes
  - 3D nodes
  - GUI nodes
  - Physics
  - Rendering
  - Navigation

For most games and apps made with 4.0, it should be relatively safe to migrate to 4.1. This page intends to cover everything you need to pay attention to when migrating your project.

If you are migrating from 4.0 to 4.1, the breaking changes listed here might affect you. Changes are grouped by areas/systems.

The GDExtension API completely breaks compatibility in 4.1, so it's not included in the table below. See the Updating your GDExtension for 4.1 section for more information.

This article indicates whether each breaking change affects GDScript and whether the C# breaking change is binary compatible or source compatible:

Binary compatible - Existing binaries will load and execute successfully without recompilation, and the runtime behavior won't change.

Source compatible - Source code will compile successfully without changes when upgrading Godot.

Method looking_at adds a new use_model_front optional parameter

Method get_meta_list changes return type from PackedStringArray to Array[StringName]

Method looking_at adds a new use_model_front optional parameter

Method create_action adds a new backward_undo_ops optional parameter

Method wait_for_task_completion changes return type from void to Error

Method _process adds a new test_only parameter

Method blend_input adds a new test_only optional parameter

Method blend_node adds a new test_only optional parameter

AnimationNodeStateMachinePlayback

Method get_travel_path changes return type from PackedStringArray to Array[StringName]

Property lookahead removed

Method segment_intersects_convex changes planes parameter type from untyped Array to Array[Plane]

Method create_multiple_convex_collisions adds a new settings optional parameter

Method look_at adds a new use_model_front optional parameter

Method look_at_from_position adds a new use_model_front optional parameter

Method add_code_completion_option adds a new location optional parameter

Method push_list adds a new bullet optional parameter

Method push_paragraph adds a new justification_flags optional parameter

Method push_paragraph adds a new tab_stops optional parameter

Method edit_selected adds a new force_edit optional parameter

Property priority changes type from float to int

Property priority changes type from float to int

PhysicsDirectSpaceState2D

Method collide_shape changes return type from Array[PackedVector2Array] to Array[Vector2]

PhysicsDirectSpaceState3D

Method collide_shape changes return type from Array[PackedVector3Array] to Array[Vector3]

Method get_version_list changes return type from PackedStringArray to Array[StringName]

Method draw_list_begin changes storage_textures parameter type from untyped Array to Array[RID]

Method global_shader_parameter_get_list changes return type from PackedStringArray to Array[StringName]

Method add_triangle_fan changes tangents parameter type from untyped Array to Array[Plane]

Method set_velocity replaced with velocity property

Property time_horizon split into time_horizon_agents and time_horizon_obstacles

Property agent_height_offset renamed to path_height_offset

Property ignore_y removed

Method set_velocity replaced with velocity property

Property time_horizon split into time_horizon_agents and time_horizon_obstacles

Property estimate_radius removed

Method get_rid renamed to get_agent_rid

Property estimate_radius removed

Method get_rid renamed to get_agent_rid

Method agent_set_callback renamed to agent_set_avoidance_callback

Method agent_set_target_velocity removed

Method agent_set_time_horizon split into agent_set_time_horizon_agents and agent_set_time_horizon_obstacles

Method agent_set_callback renamed to agent_set_avoidance_callback

Method agent_set_target_velocity removed

Method agent_set_time_horizon split into agent_set_time_horizon_agents and agent_set_time_horizon_obstacles

WebRTCPeerConnectionExtension

Method _create_data_channel changes return type from Object to WebRTCDataChannel

AnimationTrackEditPlugin

Type AnimationTrackEditPlugin removed

Type EditorInterface changes inheritance from Node to Object

Method set_movie_maker_enabled replaced with movie_maker_enabled property

Method is_movie_maker_enabled replaced with movie_maker_enabled property

EditorResourcePreviewGenerator

Method _generate adds a new metadata parameter

Method _generate_from_path adds a new metadata parameter

EditorUndoRedoManager

Method create_action adds a new backward_undo_ops optional parameter

In 4.1, some behavior changes have been introduced, which might require you to adjust your project.

When input events should reach SubViewports and their children, SubViewportContainer.mouse_filter now needs to be MOUSE_FILTER_STOP or MOUSE_FILTER_PASS. See GH-79271 for details.

Multiple layered SubViewportContainer nodes, that should all receive mouse input events, now need to be replaced by Area2D nodes. See GH-79128 for details.

Viewport nodes, that have Physics Picking enabled, now automatically set InputEvents as handled. See GH-79897 for workarounds.

In order to fix a serious bug, in Godot 4.1 we had to break binary compatibility in a big way and source compatibility in a small way.

This means that GDExtensions made for Godot 4.0 will need to be recompiled for Godot 4.1 (using the 4.1 branch of godot-cpp), with a small change to their source code.

In Godot 4.0, your "entry_symbol" function looks something like this:

However, for Godot 4.1, it should look like:

There are two small changes:

The first argument changes from const GDExtensionInterface *p_interface to GDExtensionInterfaceGetProcAddress p_get_proc_address

The constructor for the init_obj variable now receives p_get_proc_address as its first parameter

You also need to add an extra compatibility_minimum line to your .gdextension file, so that it looks something like:

This lets Godot know that your GDExtension has been updated and is safe to load in Godot 4.1.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (css):
```css
GDExtensionBool GDE_EXPORT example_library_init(const GDExtensionInterface *p_interface, const GDExtensionClassLibraryPtr p_library, GDExtensionInitialization *r_initialization) {
    godot::GDExtensionBinding::InitObject init_obj(p_interface, p_library, r_initialization);

    init_obj.register_initializer(initialize_example_module);
    init_obj.register_terminator(uninitialize_example_module);
    init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

    return init_obj.init();
}
```

Example 2 (css):
```css
GDExtensionBool GDE_EXPORT example_library_init(GDExtensionInterfaceGetProcAddress p_get_proc_address, const GDExtensionClassLibraryPtr p_library, GDExtensionInitialization *r_initialization) {
    godot::GDExtensionBinding::InitObject init_obj(p_get_proc_address, p_library, r_initialization);

    init_obj.register_initializer(initialize_example_module);
    init_obj.register_terminator(uninitialize_example_module);
    init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

    return init_obj.init();
}
```

Example 3 (json):
```json
[configuration]

entry_symbol = "example_library_init"
compatibility_minimum = 4.1
```

---

## Importing translations — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_translations.html

**Contents:**
- Importing translations
- Games and internationalization
- Supported formats
- User-contributed notes

The gaming community isn't monolingual or monocultural. It's made up of many different languages and cultures - just like the Godot community! If you want to allow players to experience your game in their language, one of things you'll need to provide is text translations, which Godot supports via internationalized text.

In regular desktop or mobile applications, internationalized text is usually located in resource files (or .po files for GNU stuff). Games, however, can use several orders of magnitude more text than applications, so they must support efficient methods for dealing with loads of multilingual text.

There are two approaches to generate multilingual language games and applications. Both are based on a key:value system. The first is to use one of the languages as the key (usually English), the second is to use a specific identifier. The first approach is probably easier for development if a game is released first in English, later in other languages, but a complete nightmare if working with many languages at the same time.

In general, games use the second approach and a unique ID is used for each string. This allows you to revise the text while it is being translated to other languages. The unique ID can be a number, a string, or a string with a number (it's just a unique string anyway).

To complete the picture and allow efficient support for translations, Godot has a special importer that can read CSV files. Most spreadsheet editors can export to this format, so the only requirement is that the files have a special arrangement. See Localization using spreadsheets for detailed info on formatting and importing CSVs.

If you need a more powerful file format, Godot also supports loading translations written in the gettext .po format. See Localization using gettext (PO files) for details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Assets pipeline — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/index.html

**Contents:**
- Assets pipeline

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Import process — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html

**Contents:**
- Import process
- Importing assets in Godot
- Changing import parameters
- Reimporting multiple assets
- Automatic reimport
- Files generated
- Changing import resource type
- Changing default import parameters
- Further reading
- User-contributed notes

To import assets in Godot, place your assets (image files, scenes, audio files, fonts, etc) directly in the project folder. There are 2 ways to achieve this:

For any file type: Copy files manually with your operating system's file manager.

For file types that can be imported by Godot: Drag-and-drop files from the operating system's file manager to the editor's FileSystem dock. This only works with resource file types (i.e. file types that Godot can import).

Godot will automatically import these files internally and keep the imported resources hidden in a res://.godot/imported/ folder.

This means that when trying to access imported assets through code, you need to use the Resource Loader as it will automatically take into account where the internal files are saved. If you try and access an imported asset using the FileAccess class, it will work in the editor, but it will break in the exported project.

However, the Resource Loader cannot access non-imported files. Only the FileAccess class can.

Import parameters are only present in non-native Godot resource types. This means Godot's own scene and resource file formats (.tscn, .scn, .tres, .res) don't have import options you can select in the Import dock.

To change the import parameters of an asset in Godot, select the relevant resource in the FileSystem dock:

After adjusting the parameters, click Reimport. Be careful: if you select another file in the FileSystem dock before clicking Reimport, changes will be discarded. After clicking Reimport, the chosen parameters will only be used for this asset and on future reimports.

Changing the import parameters of several assets at the same time is also possible. Select all of them together in the FileSystem dock and the exposed parameters will apply to all of them when reimporting.

While working on a project you may find that several assets need to have the same parameters changed, such as enabling mipmaps, but you only want those specific parameters changed. To do this, select every asset you want to reimport in the file system. In the import tab there will now be a checkbox to the left of every import parameter.

Select the checkbox of the parameters you want to change on your imported assets, then change the parameters normally. Finally, click the reimport button and every selected asset will be reimported with only those parameters changed.

When the MD5 checksum of the source asset changes, Godot will perform an automatic reimport of it, applying the preset configured for that specific asset.

Importing will add an extra <asset>.import file next to the source file, containing the import configuration.

Make sure to commit these files to your version control system, as these files contain important metadata.

Additionally, extra assets will be present in the hidden res://.godot/imported/ folder:

If any of the files present in this folder is erased (or the whole folder), the asset or assets will be reimported automatically. As such, committing the .godot/ folder to the version control system is not recommended. While committing this folder can shorten reimporting time when checking out on another computer, it requires considerably more space and bandwidth.

The default version control metadata that can be generated on project creation will automatically ignore the .godot/ folder.

Some source assets can be imported as different types of resources. For this, select the relevant type of resource desired then click Reimport:

Select Keep File (exported as is) as resource type to skip file import, files with this resource type will be preserved as is during project export.

Select Skip File (not exported) as resource type to skip file import and ignore file during project export.

Different types of projects might require different defaults. Changing the import options to a predefined set of options can be achieved by using the Preset... Menu. Besides some resource types offering presets, the default settings can be saved and cleared too:

The default import parameters for a given resource type can be changed project-wide using the Import Defaults tab of the Project Settings dialog:

This workflow takes a little time to get used to, but it enforces a more correct way to deal with resources.

There are many types of assets available for import. Continue reading to understand how to work with all of them:

Importing audio samples

Importing translations

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (python):
```python
ls
example.png
example.png.import
project.godot
```

Example 2 (unknown):
```unknown
ls .godot/imported
example.png-218a8f2b3041327d8a5756f3a245f83b.ctex
example.png-218a8f2b3041327d8a5756f3a245f83b.md5
```

---

## Importing images — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html

**Contents:**
- Importing images
- Supported image formats
- Importing textures
  - Changing import type
  - Detect 3D
- Import options
  - Compress > Mode
  - Compress > High Quality
  - Compress > HDR Compression
  - Compress > Normal Map

Godot can import the following image formats:

BMP (.bmp) - No support for 16-bit per pixel images. Only 1-bit, 4-bit, 8-bit, 24-bit, and 32-bit per pixel images are supported.

DirectDraw Surface (.dds) - If mipmaps are present in the texture, they will be loaded directly. This can be used to achieve effects using custom mipmaps.

Khronos Texture (.ktx) - Decoding is done using libktx. Only supports 2D images. Cubemaps, texture arrays and de-padding are not supported.

OpenEXR (.exr) - Supports HDR (highly recommended for panorama skies).

Radiance HDR (.hdr) - Supports HDR (highly recommended for panorama skies).

JPEG (.jpg, .jpeg) - Doesn't support transparency per the format's limitations.

PNG (.png) - Precision is limited to 8 bits per channel upon importing (no HDR images).

Truevision Targa (.tga)

SVG (.svg) - SVGs are rasterized using ThorVG when importing them. Support is limited; complex vectors may not render correctly. Text must be converted to paths; otherwise, it won't appear in the rasterized image. You can check whether ThorVG can render a certain vector correctly using its web-based viewer. For complex vectors, rendering them to PNGs using Inkscape is often a better solution. This can be automated thanks to its command-line interface.

WebP (.webp) - WebP files support transparency and can be compressed lossily or losslessly. The precision is limited to 8 bits per channel.

If you've compiled the Godot editor from source with specific modules disabled, some formats may not be available.

The default action in Godot is to import images as textures. Textures are stored in video memory. Their pixel data can't be accessed directly from the CPU without converting them back to an Image in a script. This is what makes drawing them efficient.

There are over a dozen import options that can be adjusted after selecting an image in the FileSystem dock:

Import options in the Import dock after selecting an image in the FileSystem dock. Some of these options are only visible with certain compression modes.

It is possible to choose other types of imported resources in the Import dock:

BitMap: 1-bit monochrome texture (intended to be used as a click mask in TextureButton and TouchScreenButton). This resource type cannot be displayed directly onto 2D or 3D nodes, but the pixel values can be queried from a script using get_bit.

Cubemap: Import the texture as a 6-sided cubemap, with interpolation between the cubemap's sides (seamless cubemaps), which can be sampled in custom shaders.

CubemapArray: Import the texture as a collection of 6-sided cubemaps, which can be sampled in custom shaders. This resource type can only be displayed when using the Forward+ or Mobile renderers, not the Compatibility renderer.

Font Data (Monospace Image Font): Import the image as a bitmap font where all characters have the same width. See Using Fonts.

Image: Import the image as-is. This resource type cannot be displayed directly onto 2D or 3D nodes, but the pixel values can be queried from a script using get_pixel.

Texture2D: Import the image as a 2-dimensional texture, suited for display on 2D and 3D surfaces. This is the default import mode.

Texture2DArray: Import the image as a collection of 2-dimensional textures. Texture2DArray is similar to a 3-dimensional texture, but without interpolation between layers. Built-in 2D and 3D shaders cannot display texture arrays, so you must create a custom shader in 2D or 3D to display a texture from a texture array.

Texture3D: Import the image as a 3-dimensional texture. This is not a 2D texture applied onto a 3D surface. Texture3D is similar to a texture array, but with interpolation between layers. Texture3D is typically used for FogMaterial density maps in volumetric fog, particle attractor vector fields, Environment 3D LUT color correction, and custom shaders.

TextureAtlas: Import the image as an atlas of different textures. Can be used to reduce memory usage for animated 2D sprites. Only supported in 2D due to missing support in built-in 3D shaders.

For Cubemap, the expected image order is X+, X-, Y+, Y-, Z+, Z- (in Godot's coordinate system, so Y+ is "up" and Z- is "forward"). Here are templates you can use for cubemap images (right-click > Save Link As…):

2×3 cubemap template (default layout option)

The default import options (no mipmaps and Lossless compression) are suited for 2D, but are not ideal for most 3D projects. Detect 3D makes Godot aware of when a texture is used in a 3D scene (such as a texture in a BaseMaterial3D). If this happens, several import options are changed so the texture flags are friendlier to 3D. Mipmaps are enabled and the compression mode is changed to VRAM Compressed unless Detect 3D > Compress To is changed. The texture is also reimported automatically.

A message is printed to the Output panel when a texture is detected to be used in 3D.

If you run into quality issues when a texture is detected to be used in 3D (e.g. for pixel art textures), change the Detect 3D > Compress To option before using the texture in 3D, or change Compress > Mode to Lossless after using the texture in 3D. This is preferable to disabling Detect 3D, as mipmap generation remains enabled to prevent textures from looking grainy at a distance.

In Godot 4.0, changing the texture filter and repeat mode is no longer done in the import options.

Instead, texture filter and repeat modes are changed in the CanvasItem properties in 2D (with a project setting acting as a default), and in a per-material configuration in 3D. In custom shaders, filter and repeat mode is changed on the sampler2D uniform using hints described in the Shading language documentation.

Images are one of the largest assets in a game. To handle them efficiently, they need to be compressed. Godot offers several compression methods, depending on the use case.

Lossless: This is the default and most common compression mode for 2D assets. It shows assets without any kind of artifacting, and disk compression is decent. It will use considerably more amount of video memory than VRAM Compression, though. This is also the recommended setting for pixel art.

Lossy: This is a good choice for large 2D assets. It has some artifacts, but less than VRAM compression and the file size is several times lower compared to Lossless or VRAM Uncompressed. Video memory usage isn't decreased by this mode; it's the same as with Lossless or VRAM Uncompressed.

VRAM Compressed: This is the default and most common compression mode for 3D assets. Size on disk is reduced and video memory usage is also decreased considerably (usually by a factor between 4 and 6). This mode should be avoided for 2D as it exhibits noticeable artifacts, especially for lower-resolution textures.

VRAM Uncompressed: Only useful for formats that can't be compressed, such as raw floating-point images.

Basis Universal: This alternative VRAM compression mode encodes the texture to a format that can be transcoded to most GPU-compressed formats at load-time. This provides very small files that make use of VRAM compression, at the cost of lower quality compared to VRAM Compressed and slow compression times. VRAM usage is usually the same as VRAM Compressed. Basis Universal does not support floating-point image formats (the engine will internally fall back to VRAM Compressed instead).

Even in 3D, "pixel art" textures should have VRAM compression disabled as it will negatively affect their appearance, without improving performance significantly due to their low resolution.

In this table, each of the 5 options are described together with their advantages and disadvantages ( = best, = worst):

Stored as Lossless WebP / PNG

Stored as S3TC, BPTC or ETC2 depending on platform

Transcoded to VRAM Compressed format

Estimated memory usage for a single RGBA8 texture with mipmaps enabled:

In the above table, memory usage will be reduced by 25% for images that do not have an alpha channel (RGB8). Memory usage will be further decreased by 25% for images that have mipmaps disabled.

Notice how at larger resolutions, the impact of VRAM compression is much greater. With a 4:1 compression ratio (6:1 for opaque textures with S3TC), VRAM compression effectively allows a texture to be twice as large on each axis, while using the same amount of memory on the GPU.

VRAM compression also reduces the memory bandwidth required to sample the texture, which can speed up rendering in memory bandwidth-constrained scenarios (which are frequent on integrated graphics and mobile). These factors combined make VRAM compression a must-have for 3D games with high-resolution textures.

You can preview how much memory a texture takes by double-clicking it in the FileSystem dock, then looking at the Inspector:

Previewing a texture in the Inspector. Credit: Red Brick 03 - Poly Haven

High-quality VRAM texture compression is only supported in the Forward+ and Mobile renderers.

When using the Compatibility renderer, this option is always considered disabled.

If enabled, uses BPTC compression on desktop platforms and ASTC compression on mobile platforms. When using BPTC, BC7 is used for SDR textures and BC6H is used for HDR textures.

If disabled (default), uses the faster but lower-quality S3TC compression on desktop platforms and ETC2 on mobile/web platforms. When using S3TC, DXT1 (BC1) is used for opaque textures and DXT5 (BC3) is used for transparent or normal map (RGTC) textures.

BPTC and ASTC support VRAM compression for HDR textures, but S3TC and ETC2 do not (see HDR Compression below).

This option only has an effect on textures that are imported as HDR formats in Godot (.hdr and .exr files).

If set to Disabled, never uses VRAM compression for HDR textures, regardless of whether they're opaque or transparent. Instead, the texture is converted to RGBE9995 (9-bits per channel + 5-bit exponent = 32 bits per pixel) to reduce memory usage compared to a half-float or single-precision float image format.

If set to Opaque Only (default), only uses VRAM compression for opaque HDR textures. This is due to a limitation of HDR formats, as there is no VRAM-compressed HDR format that supports transparency at the same time.

If set to Always, will force VRAM compression even for HDR textures with an alpha channel. To perform this, the alpha channel is discarded on import.

When using a texture as normal map, only the red and green channels are required. Given regular texture compression algorithms produce artifacts that don't look that nice in normal maps, the RGTC compression format is the best fit for this data. Forcing this option to Enable will make Godot import the image as RGTC compressed. By default, it's set to Detect. This means that if the texture is ever detected to be used as a normal map, it will be changed to Enable and reimported automatically.

Note that RGTC compression affects the resulting normal map image. You will have to adjust custom shaders that use the normal map's blue channel to take this into account. Built-in material shaders already ignore the blue channel in a normal map (regardless of the actual normal map's contents).

In the example below, the normal map with RGTC compression is able to preserve its detail much better, while using the same amount of memory as a standard RGBA VRAM-compressed texture:

Normal map with standard VRAM compression (left) and with RGTC VRAM compression (right)

Godot requires the normal map to use the X+, Y+ and Z+ coordinates, which is known as an OpenGL-style normal map. If you've imported a material made to be used with another engine, it may be DirectX-style. In this case, the normal map needs to be converted by enabling the Normal Map Invert Y import option.

More information about normal maps (including a coordinate order table for popular engines) can be found here.

If set to sRGB Friendly (default), prevents the RG color format from being used as it does not support sRGB color.

If set to Optimized, allows the RG color format to be used if the texture does not use the blue channel.

A third option Normal Map (RG Channels) is only available in layered textures (Cubemap, CubemapArray, Texture2DArray and Texture3D). This forces all layers from the texture to be imported with the RG color format, with only the red and green channels preserved. RGTC compression is able to preserve its detail much better, while using the same amount of memory as a standard RGBA VRAM-compressed texture. This only has an effect on textures with the VRAM Compressed or Basis Universal compression modes.

If enabled, smaller versions of the texture are generated on import. For example, a 64×64 texture will generate 6 mipmaps (32×32, 16×16, 8×8, 4×4, 2×2, 1×1). This has several benefits:

Textures will not become grainy in the distance (in 3D), or if scaled down due to camera zoom or CanvasItem scale (in 2D).

Performance will improve if the texture is displayed in the distance, since sampling smaller versions of the original texture is faster and requires less memory bandwidth.

The downside of mipmaps is that they increase memory usage by roughly 33%.

It's recommended to enable mipmaps in 3D. However, in 2D, this should only be enabled if your project visibly benefits from having mipmaps enabled. If the camera never zooms out significantly, there won't be a benefit to enabling mipmaps but memory usage will increase.

Mipmaps > Limit is currently not implemented and has no effect when changed.

If set to a value greater than -1, limits the maximum number of mipmaps that can be generated. This can be decreased if you don't want textures to become too low-resolution at extreme distances, at the cost of some graininess.

The color channel to consider as a roughness map in this texture. Only effective if Roughness > Src Normal is not empty.

The path to the texture to consider as a normal map for roughness filtering on import. Specifying this can help decrease specular aliasing slightly in 3D.

Roughness filtering on import is only used in 3D rendering, not 2D.

This puts pixels of the same surrounding color in transition from transparent to opaque areas. For textures displayed with bilinear filtering, this helps mitigate the outline effect when exporting images from an image editor.

It's recommended to leave this enabled (as it is by default), unless this causes issues for a particular image.

An alternative to fixing darkened borders with Fix Alpha Border is to use premultiplied alpha. By enabling this option, the texture will be converted to this format. A premultiplied alpha texture requires specific materials to be displayed correctly:

In 2D, a CanvasItemMaterial will need to be created and configured to use the Premul Alpha blend mode on CanvasItems that use this texture. In custom canvas item shaders, render_mode blend_premul_alpha; should be used.

In 3D, a BaseMaterial3D will need to be created and configured to use the Premul Alpha blend mode on materials that use this texture. In custom spatial shaders, render_mode blend_premul_alpha; should be used.

Godot requires the normal map to use the X+, Y+ and Z+ coordinates, which is known as an OpenGL-style normal map. If you've imported a material made to be used with another engine, it may be DirectX-style. In this case, the normal map needs to be converted by enabling the Normal Map Invert Y import option.

More information about normal maps (including a coordinate order table for popular engines) can be found here.

Some HDR images you can find online may be broken and contain sRGB color data (instead of linear color data). It is advised not to use those files. If you absolutely have to, enabling this option on will make them look correct.

Enabling HDR as sRGB on well-formatted HDR images will cause the resulting image to look too dark, so leave this disabled if unsure.

Some HDR panorama images you can find online may contain extremely bright pixels, due to being taken from real life sources without any clipping.

While these HDR panorama images are accurate to real life, this can cause the radiance map generated by Godot to contain sparkles when used as a background sky. This can be seen in material reflections (even on rough materials in extreme cases). Enabling HDR Clamp Exposure can resolve this using a smart clamping formula that does not introduce visible clipping – glow will keep working when looking at the background sky.

If set to a value greater than 0, the size of the texture is limited on import to a value smaller than or equal to the value specified here. For non-square textures, the size limit affects the longer dimension, with the shorter dimension scaled to preserve aspect ratio. Resizing is performed using cubic interpolation.

This can be used to reduce memory usage without affecting the source images, or avoid issues with textures not displaying on mobile/web platforms (as these usually can't display textures larger than 4096×4096).

This changes the Compress > Mode option that is used when a texture is detected as being used in 3D.

Changing this import option only has an effect if a texture is detected as being used in 3D. Changing this to Disabled then reimporting will not change the existing compress mode on a texture (if it's detected to be used in 3D), but choosing VRAM Compressed or Basis Universal will.

This is only available for SVG images.

The scale the SVG should be rendered at, with 1.0 being the original design size. Higher values result in a larger image. Note that unlike font oversampling, this affects the physical size the SVG is rendered at in 2D. See also Editor > Scale With Editor Scale below.

This is only available for SVG images.

If true, scales the imported image to match the editor's display scale factor. This should be enabled for editor plugin icons and custom class icons, but should be left disabled otherwise.

This is only available for SVG images.

If checked, converts the imported image's colors to match the editor's icon and font color palette. This assumes the image uses the exact same colors as Godot's own color palette for editor icons, with the source file designed for a dark editor theme. This should be enabled for editor plugin icons and custom class icons, but should be left disabled otherwise.

As the SVG library used in Godot doesn't support rasterizing text found in SVG images, text must be converted to a path first. Otherwise, text won't appear in the rasterized image.

There are two ways to achieve this in a non-destructive manner, so you can keep editing the original text afterwards:

Select your text object in Inkscape, then duplicate it in place by pressing Ctrl + D and use Path > Object to Path. Hide the original text object afterwards using the Layers and Objects dock.

Use the Inkscape command line to export an SVG from another SVG file with text converted to paths:

To support multiple resolutions with crisp visuals at high resolutions, you will need to use high-resolution source images (suited for the highest resolution you wish to support without blurriness, which is typically 4K in modern desktop games).

There are 2 ways to proceed:

Use a high base resolution in the project settings (such as 4K), then use the textures at original scale. This is an easier approach.

Use a low base resolution in the project settings (such as 1080p), then downscale textures when using them. This is often more difficult and can make various calculations in script tedious, so the approach described above is recommended instead.

After doing this, you may notice that textures become grainy at lower viewport resolutions. To resolve this, enable Mipmaps on textures used in 2D in the Import dock. This will increase memory usage.

Enabling mipmaps can also make textures appear blurrier, but you can choose to make textures sharper (at the cost of some graininess) by setting Rendering > Textures > Default Filters > Texture Mipmap Bias to a negative value.

While there's no "one size fits all" recommendation, here are some general recommendations for choosing texture sizes in 3D:

The size of a texture should be adjusted to have a consistent texel density compared to surrounding objects. While this cannot be ensured perfectly when sticking to power-of-two texture sizes, it's usually possible to keep texture detail fairly consistent throughout a 3D scene.

The smaller the object appears on screen, the smaller its texture should be. For example, a tree that only appears in the background doesn't need a texture resolution as high as other objects the player may be able to walk close to.

Using power-of-two texture sizes is recommended, but is not required. Textures don't have to be square – sizes such as 1024×512 are acceptable.

There are diminishing returns to using large texture sizes, despite the increased memory usage and loading times. Most modern 3D games not using a pixel art style stick to 2048×2048 textures on average, with 1024×1024 and 512×512 for textures spanning smaller surfaces.

When working with physically-based materials in 3D, you can reduce memory usage and file size without affecting quality too much by using a lower resolution for certain texture maps. This works especially well for textures that only feature low-frequency detail (such as a normal map for a snow texture).

If you have control over how the 3D models are created, these tips are also worth exploring:

When working with 3D models that are mostly symmetrical, you may be able to use mirrored UVs to double the effective texel density. This may look unnatural when used on human faces though.

When working with 3D models using a low-poly style and plain colors, you can rely on vertex colors instead of textures to represent colors on the model's surfaces.

Images can be loaded and saved at runtime using runtime file loading and saving, including from an exported project.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
inkscape --export-text-to-path --export-filename svg_with_text_converted_to_path.svg svg_with_text.svg
```

---

## Binary serialization API — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html

**Contents:**
- Binary serialization API
- Introduction
- Full Objects vs Object instance IDs
- Packet specification
  - 0: null
  - 1: bool
  - 2: int
  - 3: float
  - 4: String
  - 5: Vector2

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Godot has a serialization API based on Variant. It's used for converting data types to an array of bytes efficiently. This API is exposed via the global bytes_to_var() and var_to_bytes() functions, but it is also used in the get_var and store_var methods of FileAccess as well as the packet APIs for PacketPeer. This format is not used for binary scenes and resources.

If a variable is serialized with full_objects = true, then any Objects contained in the variable will be serialized and included in the result. This is recursive.

If full_objects = false, then only the instance IDs will be serialized for any Objects contained in the variable.

The packet is designed to be always padded to 4 bytes. All values are little-endian-encoded. All packets have a 4-byte header representing an integer, specifying the type of data.

The lowest value two bytes are used to determine the type, while the highest value two bytes contain flags:

Following this is the actual packet contents, which varies for each type of packet. Note that this assumes Godot is compiled with single-precision floats, which is the default. If Godot was compiled with double-precision floats, the length of "Float" fields within data structures should be 8, and the offset should be (offset - 4) * 2 + 4. The "float" type itself always uses double precision.

0 for False, 1 for True

If no flags are set (flags == 0), the integer is sent as a 32 bit integer:

32-bit signed integer

If flag ENCODE_FLAG_64 is set (flags & 1 == 1), the integer is sent as a 64-bit integer:

64-bit signed integer

If no flags are set (flags == 0), the float is sent as a 32 bit single precision:

IEEE 754 single-precision float

If flag ENCODE_FLAG_64 is set (flags & 1 == 1), the float is sent as a 64-bit double precision number:

IEEE 754 double-precision float

String length (in bytes)

This field is padded to 4 bytes.

The X component of the X column vector, accessed via [0][0]

The Y component of the X column vector, accessed via [0][1]

The X component of the Y column vector, accessed via [1][0]

The Y component of the Y column vector, accessed via [1][1]

The X component of the origin vector, accessed via [2][0]

The Y component of the origin vector, accessed via [2][1]

The X component of the X column vector, accessed via [0][0]

The Y component of the X column vector, accessed via [0][1]

The Z component of the X column vector, accessed via [0][2]

The X component of the Y column vector, accessed via [1][0]

The Y component of the Y column vector, accessed via [1][1]

The Z component of the Y column vector, accessed via [1][2]

The X component of the Z column vector, accessed via [2][0]

The Y component of the Z column vector, accessed via [2][1]

The Z component of the Z column vector, accessed via [2][2]

The X component of the X column vector, accessed via [0][0]

The Y component of the X column vector, accessed via [0][1]

The Z component of the X column vector, accessed via [0][2]

The X component of the Y column vector, accessed via [1][0]

The Y component of the Y column vector, accessed via [1][1]

The Z component of the Y column vector, accessed via [1][2]

The X component of the Z column vector, accessed via [2][0]

The Y component of the Z column vector, accessed via [2][1]

The Z component of the Z column vector, accessed via [2][2]

The X component of the origin vector, accessed via [3][0]

The Y component of the origin vector, accessed via [3][1]

The Z component of the origin vector, accessed via [3][2]

Red (typically 0..1, can be above 1 for overbright colors)

Green (typically 0..1, can be above 1 for overbright colors)

Blue (typically 0..1, can be above 1 for overbright colors)

String length, or new format (val&0x80000000!=0 and NameCount=val&0x7FFFFFFF)

Flags (absolute: val&1 != 0 )

For each Name and Sub-Name

Every name string is padded to 4 bytes.

An Object could be serialized in three different ways: as a null value, with full_objects = false, or with full_objects = true.

Zero (32-bit signed integer)

The Object instance ID (64-bit signed integer)

Class name (String length)

Class name (UTF-8 encoded string)

The number of properties that are serialized

Property name (String length)

Property name (UTF-8 encoded string)

Property value, using this same format

Not all properties are included. Only properties that are configured with the PROPERTY_USAGE_STORAGE flag set will be serialized. You can add a new usage flag to a property by overriding the _get_property_list method in your class. You can also check how property usage is configured by calling Object._get_property_list See PropertyUsageFlags for the possible usage flags.

val&0x7FFFFFFF = elements, val&0x80000000 = shared (bool)

Then what follows is, for amount of "elements", pairs of key and value, one after the other, using this same format.

val&0x7FFFFFFF = elements, val&0x80000000 = shared (bool)

Then what follows is, for amount of "elements", values one after the other, using this same format.

The array data is padded to 4 bytes.

Array length (Integers)

32-bit signed integer

Array length (Integers)

64-bit signed integer

Array length (Floats)

32-bit IEEE 754 single-precision float

Array length (Floats)

64-bit IEEE 754 double-precision float

Array length (Strings)

Every string is padded to 4 bytes.

Red (typically 0..1, can be above 1 for overbright colors)

Green (typically 0..1, can be above 1 for overbright colors)

Blue (typically 0..1, can be above 1 for overbright colors)

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
base_type = val & 0xFFFF;
flags = val >> 16;
```

---

## Background loading — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html

**Contents:**
- Background loading
- Using ResourceLoader
- Example
- User-contributed notes

Commonly, games need to load resources asynchronously. When switching the main scene of your game (e.g. going to a new level), you might want to show a loading screen with some indication that progress is being made, or you may want to load additional resources during gameplay.

The standard load method (ResourceLoader.load or GDScript's simpler load) blocks your thread, making your game appear unresponsive while the resource is being loaded.

One way around this is using ResourceLoader to load resources asynchronously in background threads.

Generally, you queue requests to load resources for a path using ResourceLoader.load_threaded_request, which will then be loaded in threads in the background.

You can check the status with ResourceLoader.load_threaded_get_status. Progress can be obtained by passing an array variable via progress which will return a one element array containing the percentage.

Finally, you retrieve loaded resources by calling ResourceLoader.load_threaded_get.

Once you call load_threaded_get(), either the resource finished loading in the background and will be returned instantly or the load will block at this point like load() would. If you want to guarantee this does not block, you either need to ensure there is enough time between requesting the load and retrieving the resource or you need to check the status manually.

This example demonstrates how to load a scene in the background. We will have a button spawn an enemy when pressed. The enemy will be Enemy.tscn which we will load on _ready and instantiate when pressed. The path will be "Enemy.tscn" which is located at res://Enemy.tscn.

First, we will start a request to load the resource and connect the button:

Now _on_button_pressed will be called when the button is pressed. This method will be used to spawn an enemy.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
const ENEMY_SCENE_PATH : String = "Enemy.tscn"

func _ready():
    ResourceLoader.load_threaded_request(ENEMY_SCENE_PATH)
    self.pressed.connect(_on_button_pressed)
```

Example 2 (gdscript):
```gdscript
using Godot;

public partial class MyButton : Button
{
    private const string EnemyScenePath = "Enemy.tscn";

    public override void _Ready()
    {
        ResourceLoader.LoadThreadedRequest(EnemyScenePath);
        Pressed += OnButtonPressed;
    }
}
```

Example 3 (gdscript):
```gdscript
func _on_button_pressed(): # Button was pressed.
    # Obtain the resource now that we need it.
    var enemy_scene = ResourceLoader.load_threaded_get(ENEMY_SCENE_PATH)
    # Instantiate the enemy scene and add it to the current scene.
    var enemy = enemy_scene.instantiate()
    add_child(enemy)
```

Example 4 (gdscript):
```gdscript
private void OnButtonPressed() // Button was pressed.
{
    // Obtain the resource now that we need it.
    var enemyScene = (PackedScene)ResourceLoader.LoadThreadedGet(EnemyScenePath);
    // Instantiate the enemy scene and add it to the current scene.
    var enemy = enemyScene.Instantiate();
    AddChild(enemy);
}
```

---

## File and data I/O — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/index.html

**Contents:**
- File and data I/O

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## File paths in Godot projects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html

**Contents:**
- File paths in Godot projects
- Path separators
- Accessing files in the project folder (res://)
- Accessing persistent user data (user://)
- File logging
- Converting paths to absolute paths or "local" paths
- Editor data paths
  - Self-contained mode
- User-contributed notes

This page explains how file paths work inside Godot projects. You will learn how to access paths in your projects using the res:// and user:// notations, and where Godot stores project and editor files on your and your users' systems.

To make supporting multiple platforms easier, Godot uses UNIX-style path separators (forward slash /). These work on all platforms, including Windows.

Instead of writing paths like C:\Projects\Game, in Godot, you should write C:/Projects/Game.

Windows-style path separators (backward slash \) are also supported in some path-related methods, but they need to be doubled (\\), as \ is normally used as an escape for characters with a special meaning.

This makes it possible to work with paths returned by other Windows applications. We still recommend using only forward slashes in your own code to guarantee that everything will work as intended.

The String class offers over a dozen methods to work with strings that represent file paths:

String.filecasecmp_to()

String.filenocasecmp_to()

String.get_base_dir()

String.get_basename()

String.get_extension()

String.is_absolute_path()

String.is_relative_path()

String.is_valid_filename()

String.simplify_path()

String.validate_filename()

Godot considers that a project exists in any folder that contains a project.godot text file, even if the file is empty. The folder that contains this file is your project's root folder.

You can access any file relative to it by writing paths starting with res://, which stands for resources. For example, you can access an image file character.png located in the project's root folder in code with the following path: res://character.png.

To store persistent data files, like the player's save or settings, you want to use user:// instead of res:// as your path's prefix. This is because when the game is running, the project's file system will likely be read-only.

The user:// prefix points to a different directory on the user's device. Unlike res://, the directory pointed at by user:// is created automatically and guaranteed to be writable to, even in an exported project.

The location of the user:// folder depends on what is configured in the Project Settings:

By default, the user:// folder is created within Godot's editor data path in the app_userdata/[project_name] folder. This is the default so that prototypes and test projects stay self-contained within Godot's data folder.

If application/config/use_custom_user_dir is enabled in the Project Settings, the user:// folder is created next to Godot's editor data path, i.e. in the standard location for applications data.

By default, the folder name will be inferred from the project name, but it can be further customized with application/config/custom_user_dir_name. This path can contain path separators, so you can use it e.g. to group projects of a given studio with a Studio Name/Game Name structure.

On desktop platforms, the actual directory paths for user:// are:

[project_name] is based on the application name defined in the Project Settings, but you can override it on a per-platform basis using feature tags.

On mobile platforms, this path is unique to the project and is not accessible by other applications for security reasons.

On HTML5 exports, user:// will refer to a virtual filesystem stored on the device via IndexedDB. (Interaction with the main filesystem can still be performed through the JavaScriptBridge singleton.)

Documentation on file logging has been moved to Logging.

You can use ProjectSettings.globalize_path() to convert a "local" path like res://path/to/file.txt to an absolute OS path. For example, ProjectSettings.globalize_path() can be used to open "local" paths in the OS file manager using OS.shell_open() since it only accepts native OS paths.

To convert an absolute OS path to a "local" path starting with res:// or user://, use ProjectSettings.localize_path(). This only works for absolute paths that point to files or folders in your project's root or user:// folders.

The editor uses different paths for editor data, editor settings, and cache, depending on the platform. By default, these paths are:

Editor data contains export templates and project-specific data.

Editor settings contains the main editor settings configuration file as well as various other user-specific customizations (editor layouts, feature profiles, script templates, etc.).

Cache contains data generated by the editor, or stored temporarily. It can safely be removed when Godot is closed.

Godot complies with the XDG Base Directory Specification on Linux/*BSD. You can override the XDG_DATA_HOME, XDG_CONFIG_HOME and XDG_CACHE_HOME environment variables to change the editor and project data paths.

If you use Godot packaged as a Flatpak, the editor data paths will be located in subfolders in ~/.var/app/org.godotengine.Godot/.

If you create a file called ._sc_ or _sc_ in the same directory as the editor binary (or in MacOS/Contents/ for a macOS editor .app bundle), Godot will enable self-contained mode. This mode makes Godot write all editor data, settings, and cache to a directory named editor_data/ in the same directory as the editor binary. You can use it to create a portable installation of the editor.

The Steam release of Godot uses self-contained mode by default.

Self-contained mode is not supported in exported projects yet. To read and write files relative to the executable path, use OS.get_executable_path(). Note that writing files in the executable path only works if the executable is placed in a writable location (i.e. not Program Files or another directory that is read-only for regular users).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Internationalization — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/i18n/index.html

**Contents:**
- Internationalization

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Runtime file loading and saving — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/runtime_file_loading_and_saving.html

**Contents:**
- Runtime file loading and saving
- Plain text and binary files
- Images
- Audio/video files
- 3D scenes
- Fonts
- ZIP archives
- User-contributed notes

See Saving games for information on saving and loading game progression.

Sometimes, exporting packs, patches, and mods is not ideal when you want players to be able to load user-generated content in your project. It requires users to generate a PCK or ZIP file through the Godot editor, which contains resources imported by Godot.

Example use cases for runtime file loading and saving include:

Loading texture packs designed for the game.

Loading user-provided audio tracks and playing them back in an in-game radio station.

Loading custom levels or 3D models that can be designed with any 3D DCC that can export to glTF or FBX (including glTF scenes saved by Godot at runtime).

Using user-provided fonts for menus and HUD.

Saving/loading a file format that can contain multiple files but can still easily be read by other applications (ZIP).

Loading files created by another game or program, or even game data files from another game not made with Godot.

Runtime file loading can be combined with HTTP requests to load resources from the Internet directly.

Do not use this runtime loading approach to load resources that are part of the project, as it's less efficient and doesn't allow benefiting from Godot's resource handling functionality (such as translation remaps). See Import process for details.

You can see how saving and loading works in action using the Run-time File Saving and Loading (Serialization) demo project.

Godot's FileAccess class provides methods to access files on the filesystem for reading and writing:

To handle custom binary formats (such as loading file formats not supported by Godot), FileAccess provides several methods to read/write integers, floats, strings and more. These FileAccess methods have names that start with get_ and store_.

If you need more control over reading binary files or need to read binary streams that are not part of a file, PackedByteArray provides several helper methods to decode/encode series of bytes to integers, floats, strings and more. These PackedByteArray methods have names that start with decode_ and encode_. See also Binary serialization API.

Image's Image.load_from_file static method handles everything, from format detection based on file extension to reading the file from disk.

If you need error handling or more control (such as changing the scale an SVG is loaded at), use one of the following methods depending on the file format:

Image.load_jpg_from_buffer

Image.load_ktx_from_buffer

Image.load_png_from_buffer

Image.load_svg_from_buffer or Image.load_svg_from_string

Image.load_tga_from_buffer

Image.load_webp_from_buffer

Several image formats can also be saved by Godot at runtime using the following methods:

Image.save_png or Image.save_png_to_buffer

Image.save_webp or Image.save_webp_to_buffer

Image.save_jpg or Image.save_jpg_to_buffer

Image.save_exr or Image.save_exr_to_buffer (only available in editor builds, cannot be used in exported projects)

The methods with the to_buffer suffix save the image to a PackedByteArray instead of the filesystem. This is useful to send the image over the network or into a ZIP archive without having to write it on the filesystem. This can increase performance by reducing I/O utilization.

If displaying the loaded image on a 3D surface, make sure to call Image.generate_mipmaps so that the texture doesn't look grainy when viewed at a distance. This is also useful in 2D when following instructions on reducing aliasing when downsampling.

Example of loading an image and displaying it in a TextureRect node (which requires conversion to ImageTexture):

Godot supports loading Ogg Vorbis, MP3, and WAV audio at runtime. Note that not all files with a .ogg extension are Ogg Vorbis files. Some may be Ogg Theora videos, or contain Opus audio within an Ogg container. These files will not load correctly as audio files in Godot.

Example of loading an Ogg Vorbis audio file in an AudioStreamPlayer node:

Example of loading an Ogg Theora video file in a VideoStreamPlayer node:

Godot has first-class support for glTF 2.0, both in the editor and exported projects. Using GLTFDocument and GLTFState together, Godot can load and save glTF files in exported projects, in both text (.gltf) and binary (.glb) formats. The binary format should be preferred as it's faster to write and smaller, but the text format is easier to debug.

Since Godot 4.3, FBX scenes can also be loaded (but not saved) at runtime using the FBXDocument and FBXState classes. The code to do so is the same as glTF, but you will need to replace all instances of GLTFDocument and GLTFState with FBXDocument and FBXState in the code samples below. There are known issues with runtime FBX loading, so using glTF instead is preferred for now.

Example of loading a glTF scene and appending its root node to the scene:

When loading a glTF scene, a base path must be set so that external resources like textures can be loaded correctly. When loading from a file, the base path is automatically set to the folder containing the file. When loading from a buffer, this base path must be manually set as there is no way for Godot to infer this path.

To set the base path, set GLTFState.base_path on your GLTFState instance before calling GLTFDocument.append_from_buffer or GLTFDocument.append_from_file.

FontFile.load_dynamic_font supports the following font file formats: TTF, OTF, WOFF, WOFF2, PFB, PFM

On the other hand, FontFile.load_bitmap_font supports the BMFont format (.fnt or .font).

Additionally, it is possible to load any font that is installed on the system using Godot's support for System fonts.

Example of loading a font file automatically according to its file extension, then adding it as a theme override to a Label node:

Godot supports reading and writing ZIP archives using the ZIPReader and ZIPPacker classes. This supports any ZIP file, including files generated by Godot's "Export PCK/ZIP" functionality (although these will contain imported Godot resources rather than the original project files).

Use ProjectSettings.load_resource_pack to load PCK or ZIP files exported by Godot as additional data packs. That approach is preferred for DLCs, as it makes interacting with additional data packs seamless (virtual filesystem).

This ZIP archive support can be combined with runtime image, 3D scene and audio loading to provide a seamless modding experience without requiring users to go through the Godot editor to generate PCK/ZIP files.

Example that lists files in a ZIP archive in an ItemList node, then writes contents read from it to a new ZIP archive (essentially duplicating the archive):

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func save_file(content):
    var file = FileAccess.open("/path/to/file.txt", FileAccess.WRITE)
    file.store_string(content)

func load_file():
    var file = FileAccess.open("/path/to/file.txt", FileAccess.READ)
    var content = file.get_as_text()
    return content
```

Example 2 (csharp):
```csharp
private void SaveFile(string content)
{
    using var file = FileAccess.Open("/Path/To/File.txt", FileAccess.ModeFlags.Write);
    file.StoreString(content);
}

private string LoadFile()
{
    using var file = FileAccess.Open("/Path/To/File.txt", FileAccess.ModeFlags.Read);
    string content = file.GetAsText();
    return content;
}
```

Example 3 (sql):
```sql
# Load an image of any format supported by Godot from the filesystem.
var image = Image.load_from_file(path)
# Optionally, generate mipmaps if displaying the texture on a 3D surface
# so that the texture doesn't look grainy when viewed at a distance.
#image.generate_mipmaps()
$TextureRect.texture = ImageTexture.create_from_image(image)

# Save the loaded Image to a PNG image.
image.save_png("/path/to/file.png")

# Save the converted ImageTexture to a PNG image.
$TextureRect.texture.get_image().save_png("/path/to/file.png")
```

Example 4 (sql):
```sql
// Load an image of any format supported by Godot from the filesystem.
var image = Image.LoadFromFile(path);
// Optionally, generate mipmaps if displaying the texture on a 3D surface
// so that the texture doesn't look grainy when viewed at a distance.
// image.GenerateMipmaps();
GetNode<TextureRect>("TextureRect").Texture = ImageTexture.CreateFromImage(image);

// Save the loaded Image to a PNG image.
image.SavePng("/Path/To/File.png");

// Save the converted ImageTexture to a PNG image.
GetNode<TextureRect>("TextureRect").Texture.GetImage().SavePng("/Path/To/File.png");
```

---

## Internationalizing games — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html

**Contents:**
- Internationalizing games
- Introduction
- Configuring the imported translation
- Localizing resources
- Automatically setting a language
- Locale vs. language
- Converting keys to text
  - Placeholders
  - Translation contexts
  - Pluralization

While indie or niche games usually do not need localization, games targeting a more massive market often require localization. Godot offers many tools to make this process more straightforward, so this tutorial is more like a collection of tips and tricks.

Localization is usually done by specific studios hired for the job. Despite the huge amount of software and file formats available for this, the most common way to do localization to this day is still with spreadsheets. The process of creating the spreadsheets and importing them is already covered in the Importing translations tutorial. If you haven't read the Importing translations page before, we recommend you give it a read before reading this page.

We will be using the official demo as an example; you can download it from the Asset Library.

Translations can get updated and re-imported when they change, but they still have to be added to the project. This is done in Project → Project Settings → Localization:

The above dialog is used to add or remove translations project-wide.

It is also possible to instruct Godot to use alternate versions of assets (resources) depending on the current language. This can be used for localized images such as in-game billboards or localized voices.

The Remaps tab can be used for this:

Select the resource to be remapped then add some alternatives for each locale.

The resource remapping system isn't supported for DynamicFonts. To use different fonts depending on the language's script, use the DynamicFont fallback system instead, which lets you define as many fallback fonts as you want.

The upside of the DynamicFont fallback system is that it works regardless of the current language, making it ideal for things like multiplayer chat where the text language may not match the client's language.

It is recommended to default to the user's preferred language which can be obtained via OS.get_locale_language(). If your game is not available in that language, it will fall back to the Fallback in Project Settings > Internationalization > Locale, or to en if empty. Nevertheless letting players change the language in game is recommended for various reasons (e.g. translation quality or player preference).

A locale is commonly a combination of a language with a region or country, but can also contain information like a script or a variant.

en_GB: English in Great Britain / British English

en_US: English in the USA / American English

en_DE: English in Germany

Indie games generally only need to care about language, but read on for more information.

Why locales exist can be illustrated through the USA and Great Britain. Both speak the same language (English), yet differ in many aspects: - Spelling: E.g. gray (USA), grey (GB) - Use of words: E.g. eggplant (USA), aubergine (GB) - Units or currencies: E.g. feet/inches (USA), metres/cm (GB)

It can get more complex however. Imagine you offer different content in Europe and in China (e.g. in an MMO). You will need to translate each of those content variations into many languages and store and load them accordingly.

Some controls, such as Button and Label, will automatically fetch a translation if their text matches a translation key. For example, if a label's text is "MAIN_SCREEN_GREETING1" and that key exists in the current translation, then the text will automatically be translated.

This automatic translation behavior may be undesirable in certain cases. For instance, when using a Label to display a player's name, you most likely don't want the player's name to be translated if it matches a translation key. To disable automatic translation on a specific node, disable Localization > Auto Translate in the inspector.

In code, the Object.tr() function can be used. This will just look up the text in the translations and convert it if found:

If no text is displayed after changing the language, try to use a different font. The default project font only supports a subset of the Latin-1 character set, which cannot be used to display languages like Russian or Chinese.

A good resource for multilingual fonts is Noto Fonts. Make sure to download the correct variation if you're using a less common language.

Once you've downloaded the font, load the TTF file into a DynamicFont resource and use it as a custom font of your Control node. For better reusability, associate a new a Theme resource to your root Control node and define the DynamicFont as the Default Font in the theme.

To feature placeholders in your translated strings, use GDScript format strings or the equivalent feature in C#. This lets translators move the location of the placeholder in the string freely, which allows translations to sound more natural. Named placeholders with the String.format() function should be used whenever possible, as they also allow translators to choose the order in which placeholders appear:

If you're using plain English as source strings (rather than message codes LIKE_THIS), you may run into ambiguities when you have to translate the same English string to different strings in certain target languages. You can optionally specify a translation context to resolve this ambiguity and allow target languages to use different strings, even though the source string is identical:

Most languages require different strings depending on whether an object is in singular or plural form. However, hardcoding the "is plural" condition depending on whether there is more than 1 object is not valid in all languages.

Some languages have more than two plural forms, and the rules on the number of objects required for each plural form vary. Godot offers support for pluralization so that the target locales can handle this automatically.

Pluralization is meant to be used with positive (or zero) integer numbers only. Negative and floating-point values usually represent physical entities for which singular and plural don't clearly apply.

This can be combined with a context if needed:

Providing pluralized translations is only supported with Localization using gettext (PO files), not CSV.

The same text in different languages can vary greatly in length. For this, make sure to read the tutorial on Size and anchors, as dynamically adjusting control sizes may help. Container can be useful, as well as the text wrapping options available in Label.

To check whether your UI can accommodate translations with longer strings than the original, you can enable pseudolocalization in the advanced Project Settings. This will replace all your localizable strings with longer versions of themselves, while also replacing some characters in the original strings with accented versions (while still being readable). Placeholders are kept as-is, so that they keep working when pseudolocalization is enabled.

For example, the string Hello world, this is %s! becomes [Ĥéłłô ŵôŕłd́, ŧh̀íš íš %s!] when pseudolocalization is enabled.

While looking strange at first, pseudolocalization has several benefits:

It lets you spot non-localizable strings quickly, so you can go over them and make them localizable (if it makes sense to do so).

It lets you check UI elements that can't fit long strings. Many languages will feature much longer translations than the source text, so it's important to ensure your UI can accommodate longer-than-usual strings.

It lets you check whether your font contains all the characters required to support various languages. However, since the goal of pseudolocalization is to keep the original strings readable, it's not an effective test for checking whether a font can support CJK or right-to-left languages.

The project settings allow you to tune pseudolocalization behavior, so that you can disable parts of it if desired.

Godot has a server handling low-level translation management called the TranslationServer. Translations can be added or removed during runtime; the current language can also be changed at runtime.

Arabic and Hebrew are written from right to left (except for the numbers and Latin words mixed in), and the user interface for these languages should be mirrored as well. In some languages the shape of a glyph changes depending on the surrounding characters.

Support for bidirectional writing systems and UI mirroring is transparent, you don't usually need to change anything or have any knowledge of the specific writing system.

For RTL languages, Godot will automatically do the following changes to the UI:

Mirrors left/right anchors and margins.

Swaps left and right text alignment.

Mirrors horizontal order of the child controls in the containers, and items in Tree/ItemList controls.

Uses mirrored order of the internal control elements (e.g. OptionButton dropdown button, checkbox alignment, List column order, Tree item icons and connecting line alignment, e.t.c.), in some cases mirrored controls use separate theme styles.

Coordinate system is not mirrored, and non-UI nodes (sprites, e.t.c) are not affected.

It is possible to override text and control layout direction by using the following control properties:

text_direction, sets the base text direction. When set to "auto", direction depends on the first strong directional character in the text according to the Unicode Bidirectional Algorithm,

language, overrides current project locale.

structured_text_bidi_override property and _structured_text_parser callback, enables special handling for structured text.

layout_direction, overrides control mirroring.

You can see how right-to-left typesetting works in action using the BiDI and Font Features demo project.

Some languages are written without spaces. In those languages, word and line breaking require more than rules over character sequences. Godot includes ICU rule and dictionary-based break iterator data, but this data is not included in exported projects by default.

To include it, go to Project → Project Settings, enable Internationalization → Locale → Include Text Server Data, then export the project. Break iterator data is about 4 MB in size.

Unicode BiDi algorithm is designed to work with natural text and it's incapable of handling text with the higher level order, like file names, URIs, email addresses, regular expressions or source code.

For example, the path for this shown directory structure will be displayed incorrectly (top "LineEdit" control). "File" type structured text override splits text into segments, then BiDi algorithm is applied to each of them individually to correctly display directory names in any language and preserve correct order of the folders (bottom "LineEdit" control).

Custom callbacks provide a way to override BiDi for the other types of structured text.

Controls specifically designed for number input or output (e.g. ProgressBar, SpinBox) will use localized numbering system automatically, for the other control TextServer.format_number(string, language) can be used to convert Western Arabic numbers (0..9) to the localized numbering system and TextServer.parse_number(string, language) to convert it back.

Icons with left and right pointing arrows which may need to be reversed for Arabic and Hebrew locales, in case they indicate movement or direction (e.g. back/forward buttons). Otherwise, they can remain the same.

You may want to test a project's translation before releasing it. Godot provides three ways to do this.

First, in the Project Settings, under Internationalization > Locale (with advanced settings enabled), there is a Test property. Set this property to the locale code of the language you want to test. Godot will run the project with that locale when the project is run (either from the editor or when exported).

Keep in mind that since this is a project setting, it will show up in version control when it is set to a non-empty value. Therefore, it should be set back to an empty value before committing changes to version control.

Second, from within the editor go to the top bar and click on View on the top bar, then go down to Preview Translation and select the language you want to preview.

All text in scenes in the editor should now be displayed using the selected language.

Translations can also be tested when running Godot from the command line. For example, to test a game in French, the following argument can be supplied:

The project name becomes the app name when exporting to different operating systems and platforms. To specify the project name in more than one language go to Project > Project Settings> Application > Config. From here click on the button that says Localizable String (Size 0). Now there should be a button below that which says Add Translation. Click on that and it will take you to a page where you can choose the language (and country if needed) for your project name translation. After doing that you can now type in the localized name.

If you are unsure about the language code to use, refer to the list of locale codes.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
var language = "automatic"
# Load here language from the user settings file
if language == "automatic":
   var preferred_language = OS.get_locale_language()
   TranslationServer.set_locale(preferred_language)
else:
   TranslationServer.set_locale(language)
```

Example 2 (unknown):
```unknown
level.text = tr("LEVEL_5_NAME")
status.text = tr("GAME_STATUS_%d" % status_index)
```

Example 3 (unknown):
```unknown
level.Text = Tr("LEVEL_5_NAME");
status.Text = Tr($"GAME_STATUS_{statusIndex}");
```

Example 4 (markdown):
```markdown
# The placeholder's locations can be changed, but not their order.
# This will probably not suffice for some target languages.
message.text = tr("%s picked up the %s") % ["Ogre", "Sword"]

# The placeholder's locations and order can be changed.
# Additionally, this form gives more context for translators to work with.
message.text = tr("{character} picked up the {weapon}").format({character = "Ogre", weapon = "Sword"})
```

---

## Saving games — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html

**Contents:**
- Saving games
- Introduction
- Identify persistent objects
- Serializing
- Saving and reading data
- Some notes
- JSON vs binary serialization
  - JSON limitations
  - Binary serialization
- User-contributed notes

Save games can be complicated. For example, it may be desirable to store information from multiple objects across multiple levels. Advanced save game systems should allow for additional information about an arbitrary number of objects. This will allow the save function to scale as the game grows more complex.

If you're looking to save user configuration, you can use the ConfigFile class for this purpose.

You can see how saving and loading works in action using the Saving and Loading (Serialization) demo project.

Firstly, we should identify what objects we want to keep between game sessions and what information we want to keep from those objects. For this tutorial, we will use groups to mark and handle objects to be saved, but other methods are certainly possible.

We will start by adding objects we wish to save to the "Persist" group. We can do this through either the GUI or script. Let's add the relevant nodes using the GUI:

Once this is done, when we need to save the game, we can get all objects to save them and then tell them all to save with this script:

The next step is to serialize the data. This makes it much easier to read from and store to disk. In this case, we're assuming each member of group Persist is an instanced node and thus has a path. GDScript has the helper class JSON to convert between dictionary and string. Our node needs to contain a save function that returns this data. The save function will look like this:

This gives us a dictionary with the style { "variable_name":value_of_variable }, which will be useful when loading.

As covered in the File system tutorial, we'll need to open a file so we can write to it or read from it. Now that we have a way to call our groups and get their relevant data, let's use the class JSON to convert it into an easily stored string and store them in a file. Doing it this way ensures that each line is its own object, so we have an easy way to pull the data out of the file as well.

Game saved! Now, to load, we'll read each line. Use the parse method to read the JSON string back to a dictionary, and then iterate over the dict to read our values. But we'll need to first create the object and we can use the filename and parent values to achieve that. Here is our load function:

Now we can save and load an arbitrary number of objects laid out almost anywhere across the scene tree! Each object can store different data depending on what it needs to save.

We have glossed over setting up the game state for loading. It's ultimately up to the project creator where much of this logic goes. This is often complicated and will need to be heavily customized based on the needs of the individual project.

Additionally, our implementation assumes no Persist objects are children of other Persist objects. Otherwise, invalid paths would be created. To accommodate nested Persist objects, consider saving objects in stages. Load parent objects first so they are available for the add_child() call when child objects are loaded. You will also need a way to link children to parents as the NodePath will likely be invalid.

For simple game state, JSON may work and it generates human-readable files that are easy to debug.

But JSON has many limitations. If you need to store more complex game state or a lot of it, binary serialization may be a better approach.

Here are some important gotchas to know about when using JSON.

Filesize: JSON stores data in text format, which is much larger than binary formats.

Data types: JSON only offers a limited set of data types. If you have data types that JSON doesn't have, you will need to translate your data to and from types that JSON can handle. For example, some important types that JSON can't parse are: Vector2, Vector3, Color, Rect2, and Quaternion.

Custom logic needed for encoding/decoding: If you have any custom classes that you want to store with JSON, you will need to write your own logic for encoding and decoding those classes.

Binary serialization is an alternative approach for storing game state, and you can use it with the functions get_var and store_var of FileAccess.

Binary serialization should produce smaller files than JSON.

Binary serialization can handle most common data types.

Binary serialization requires less custom logic for encoding and decoding custom classes.

Note that not all properties are included. Only properties that are configured with the PROPERTY_USAGE_STORAGE flag set will be serialized. You can add a new usage flag to a property by overriding the _get_property_list method in your class. You can also check how property usage is configured by calling Object._get_property_list. See PropertyUsageFlags for the possible usage flags.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var save_nodes = get_tree().get_nodes_in_group("Persist")
for node in save_nodes:
    # Now, we can call our save function on each node.
```

Example 2 (swift):
```swift
var saveNodes = GetTree().GetNodesInGroup("Persist");
foreach (Node saveNode in saveNodes)
{
    // Now, we can call our save function on each node.
}
```

Example 3 (gdscript):
```gdscript
func save():
    var save_dict = {
        "filename" : get_scene_file_path(),
        "parent" : get_parent().get_path(),
        "pos_x" : position.x, # Vector2 is not supported by JSON
        "pos_y" : position.y,
        "attack" : attack,
        "defense" : defense,
        "current_health" : current_health,
        "max_health" : max_health,
        "damage" : damage,
        "regen" : regen,
        "experience" : experience,
        "tnl" : tnl,
        "level" : level,
        "attack_growth" : attack_growth,
        "defense_growth" : defense_growth,
        "health_growth" : health_growth,
        "is_alive" : is_alive,
        "last_attack" : last_attack
    }
    return save_dict
```

Example 4 (csharp):
```csharp
public Godot.Collections.Dictionary<string, Variant> Save()
{
    return new Godot.Collections.Dictionary<string, Variant>()
    {
        { "Filename", SceneFilePath },
        { "Parent", GetParent().GetPath() },
        { "PosX", Position.X }, // Vector2 is not supported by JSON
        { "PosY", Position.Y },
        { "Attack", Attack },
        { "Defense", Defense },
        { "CurrentHealth", CurrentHealth },
        { "MaxHealth", MaxHealth },
        { "Damage", Damage },
        { "Regen", Regen },
        { "Experience", Experience },
        { "Tnl", Tnl },
        { "Level", Level },
        { "AttackGrowth", AttackGrowth },
        { "DefenseGrowth", DefenseGrowth },
        { "HealthGrowth", HealthGrowth },
        { "IsAlive", IsAlive },
        { "LastAttack", LastAttack }
    };
}
```

---

## Locale codes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/i18n/locales.html

**Contents:**
- Locale codes
- List of supported language codes
- List of supported script codes
- List of supported country codes
- User-contributed notes

Locale code has the following format: language_Script_COUNTRY_VARIANT, where:

language - 2 or 3-letter language code, in lower case.

Script - optional, 4-letter script code, in title case.

COUNTRY - optional, 2-letter country code, in upper case.

VARIANT - optional, language variant, region and, sort order. A variant can have any number of underscored keywords.

American Sign Language

Seselwa Creole French

Jamaican Creole English

Chimborazo Highland Quichua

Central Atlas Tamazight

Standard Moroccan Tamazight

Unified Canadian Aboriginal

Anatolian Hieroglyphs

Nyiakeng Puachue Hmong

Inscriptional Pahlavi

Inscriptional Parthian

Bosnia and Herzegovina

Caribbean Netherlands

Cocos (Keeling) Islands

Central African Republic

South Georgia and South Sandwich Islands

Heard Island and McDonald Islands

British Indian Ocean Territory

Northern Mariana Islands

St. Pierre and Miquelon

St. Helena, Ascension and Tristan da Cunha

Svalbard and Jan Mayen

Sao Tome and Principe

Turks and Caicos Islands

French Southern Territories

U.S. Outlying Islands

United States of America

St. Vincent and the Grenadines

British Virgin Islands

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using InputEvent — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html

**Contents:**
- Using InputEvent
- What is it?
- How does it work?
- Anatomy of an InputEvent
- Input actions
- InputMap
- User-contributed notes

Managing input is usually complex, no matter the OS or platform. To ease this a little, a special built-in type is provided, InputEvent. This datatype can be configured to contain several types of input events. Input events travel through the engine and can be received in multiple locations, depending on the purpose.

Here is a quick example, closing your game if the escape key is hit:

However, it is cleaner and more flexible to use the provided InputMap feature, which allows you to define input actions and assign them different keys. This way, you can define multiple keys for the same action (e.g. the keyboard escape key and the start button on a gamepad). You can then more easily change this mapping in the project settings without updating your code, and even build a key mapping feature on top of it to allow your game to change the key mapping at runtime!

You can set up your InputMap under Project > Project Settings > Input Map and then use those actions like this:

Every input event is originated from the user/player (though it's possible to generate an InputEvent and feed them back to the engine, which is useful for gestures). The DisplayServer for each platform will read events from the operating system, then feed them to the root Window.

The window's Viewport does quite a lot of stuff with the received input, in order:

If the Viewport is embedding Windows, the Viewport tries to interpret the event in its capability as a Window-Manager (e.g. for resizing or moving Windows).

Next if an embedded Window is focused, the event is sent to that Window and processed in the Window's Viewport and afterwards treated as handled. If no embedded Window is focused, the event is sent to the nodes of the current viewport in the following order.

First of all, the standard Node._input() function will be called in any node that overrides it (and hasn't disabled input processing with Node.set_process_input()). If any function consumes the event, it can call Viewport.set_input_as_handled(), and the event will not spread any more. This ensures that you can filter all events of interest, even before the GUI. For gameplay input, Node._unhandled_input() is generally a better fit, because it allows the GUI to intercept the events.

Second, it will try to feed the input to the GUI, and see if any control can receive it. If so, the Control will be called via the virtual function Control._gui_input() and the signal "gui_input" will be emitted (this function is re-implementable by script by inheriting from it). If the control wants to "consume" the event, it will call Control.accept_event() and the event will not spread any more. Use the Control.mouse_filter property to control whether a Control is notified of mouse events via Control._gui_input() callback, and whether these events are propagated further.

If so far no one consumed the event, the Node._shortcut_input() callback will be called if overridden (and not disabled with Node.set_process_shortcut_input()). This happens only for InputEventKey, InputEventShortcut and InputEventJoypadButton. If any function consumes the event, it can call Viewport.set_input_as_handled(), and the event will not spread any more. The shortcut input callback is ideal for treating events that are intended as shortcuts.

If so far no one consumed the event, the Node._unhandled_key_input() callback will be called if overridden (and not disabled with Node.set_process_unhandled_key_input()). This happens only if the event is an InputEventKey. If any function consumes the event, it can call Viewport.set_input_as_handled(), and the event will not spread any more. The unhandled key input callback is ideal for key events.

If so far no one consumed the event, the Node._unhandled_input() callback will be called if overridden (and not disabled with Node.set_process_unhandled_input()). If any function consumes the event, it can call Viewport.set_input_as_handled(), and the event will not spread any more. The unhandled input callback is ideal for full-screen gameplay events, so they are not received when a GUI is active.

If no one wanted the event so far, and Object Picking is turned on, the event is used for object picking. For the root viewport, this can also be enabled in Project Settings. In the case of a 3D scene if a Camera3D is assigned to the Viewport, a ray to the physics world (in the ray direction from the click) will be cast. If this ray hits an object, it will call the CollisionObject3D._input_event() function in the relevant physics object. In the case of a 2D scene, conceptually the same happens with CollisionObject2D._input_event().

When sending events to its child and descendant nodes, the viewport will do so, as depicted in the following graphic, in a reverse depth-first order, starting with the node at the bottom of the scene tree, and ending at the root node. Excluded from this process are Windows and SubViewports.

This order doesn't apply to Control._gui_input(), which uses a different method based on event location or focused Control. GUI mouse events also travel up the scene tree, subject to the Control.mouse_filter restrictions described above. However, since these events target specific Controls, only direct ancestors of the targeted Control node receive the event. GUI keyboard and joypad events do not travel up the scene tree, and can only be handled by the Control that received them. Otherwise, they will be propagated as non-GUI events through Node._unhandled_input().

Since Viewports don't send events to other SubViewports, one of the following methods has to be used:

Use a SubViewportContainer, which automatically sends events to its child SubViewports after Node._input() or Control._gui_input().

Implement event propagation based on the individual requirements.

In accordance with Godot's node-based design, this enables specialized child nodes to handle and consume particular events, while their ancestors, and ultimately the scene root, can provide more generalized behavior if needed.

InputEvent is just a base built-in type, it does not represent anything and only contains some basic information, such as event ID (which is increased for each event), device index, etc.

There are several specialized types of InputEvent, described in the table below:

Contains a keycode and Unicode value, as well as modifiers.

InputEventMouseButton

Contains click information, such as button, modifiers, etc.

InputEventMouseMotion

Contains motion information, such as relative and absolute positions and speed.

InputEventJoypadMotion

Contains Joystick/Joypad analog axis information.

InputEventJoypadButton

Contains Joystick/Joypad button information.

InputEventScreenTouch

Contains multi-touch press/release information. (only available on mobile devices)

Contains multi-touch drag information. (only available on mobile devices)

InputEventMagnifyGesture

Contains a position, a factor as well as modifiers.

Contains a position, a delta as well as modifiers.

Contains MIDI-related information.

Contains a generic action. These events are often generated by the programmer as feedback. (more on this below)

Input actions are a grouping of zero or more InputEvents into a commonly understood title (for example, the default "ui_left" action grouping both joypad-left input and a keyboard's left arrow key). They are not required to represent an InputEvent but are useful because they abstract various inputs when programming the game logic.

The same code to work on different devices with different inputs (e.g., keyboard on PC, Joypad on console).

Input to be reconfigured at runtime.

Actions to be triggered programmatically at runtime.

Actions can be created from the Project Settings menu in the Input Map tab and assigned input events.

Any event has the methods InputEvent.is_action(), InputEvent.is_pressed() and InputEvent.is_echo().

Alternatively, it may be desired to supply the game back with an action from the game code (a good example of this is detecting gestures). The Input singleton has a method for this: Input.parse_input_event(). You would normally use it like this:

See Creating input actions for a tutorial on adding input actions in the project settings.

Customizing and re-mapping input from code is often desired. If your whole workflow depends on actions, the InputMap singleton is ideal for reassigning or creating different actions at runtime. This singleton is not saved (must be modified manually) and its state is run from the project settings (project.godot). So any dynamic system of this type needs to store settings in the way the programmer best sees fit.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (go):
```go
func _unhandled_input(event):
    if event is InputEventKey:
        if event.pressed and event.keycode == KEY_ESCAPE:
            get_tree().quit()
```

Example 2 (json):
```json
public override void _UnhandledInput(InputEvent @event)
{
    if (@event is InputEventKey eventKey)
    {
        if (eventKey.Pressed && eventKey.Keycode == Key.Escape)
        {
            GetTree().Quit();
        }
    }
}
```

Example 3 (gdscript):
```gdscript
func _process(delta):
    if Input.is_action_pressed("ui_right"):
        # Move right.
```

Example 4 (gdscript):
```gdscript
public override void _Process(double delta)
{
    if (Input.IsActionPressed("ui_right"))
    {
        // Move right.
    }
}
```

---

## Input handling — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/inputs/index.html

**Contents:**
- Input handling

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Customizing the mouse cursor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/inputs/custom_mouse_cursor.html

**Contents:**
- Customizing the mouse cursor
- Using project settings
- Using a script
- Cursor list
- User-contributed notes

You might want to change the appearance of the mouse cursor in your game in order to suit the overall design. There are two ways to customize the mouse cursor:

Using project settings. This is simpler, but more limited.

Using a script. This is more customizable, but involves scripting.

You could display a "software" mouse cursor by hiding the mouse cursor and moving a Sprite2D to the cursor position in a _process() method, but this will add at least one frame of latency compared to a "hardware" mouse cursor. Therefore, it's recommended to use the approach described here whenever possible.

If you have to use the "software" approach, consider adding an extrapolation step to better display the actual mouse input.

Open the Project Settings and go to Display > Mouse Cursor. You will see the settings Custom Image, Custom Image Hotspot, and Tooltip Position Offset.

Custom Image is the desired image that you would like to set as the mouse cursor. Custom Hotspot is the point in the image that you would like to use as the cursor's detection point.

The custom image must be 256×256 pixels at most. To avoid rendering issues, sizes of 128×128 or smaller are recommended.

On the web platform, the maximum allowed cursor image size is 128×128.

Create a Node and attach the following script.

Check Input.set_custom_mouse_cursor()'s documentation for more information on usage and platform-specific caveats.

There are multiple mouse cursors you can define, documented in the Input.CursorShape enum. Which ones you want to use depends on your use case.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node


# Load the custom images for the mouse cursor.
var arrow = load("res://arrow.png")
var beam = load("res://beam.png")


func _ready():
    # Changes only the arrow shape of the cursor.
    # This is similar to changing it in the project settings.
    Input.set_custom_mouse_cursor(arrow)

    # Changes a specific shape of the cursor (here, the I-beam shape).
    Input.set_custom_mouse_cursor(beam, Input.CURSOR_IBEAM)
```

Example 2 (gdscript):
```gdscript
using Godot;

public partial class MyNode : Node
{
    public override void _Ready()
    {
        // Load the custom images for the mouse cursor.
        var arrow = ResourceLoader.Load("res://arrow.png");
        var beam = ResourceLoader.Load("res://beam.png");

        // Changes only the arrow shape of the cursor.
        // This is similar to changing it in the project settings.
        Input.SetCustomMouseCursor(arrow);

        // Changes a specific shape of the cursor (here, the I-beam shape).
        Input.SetCustomMouseCursor(beam, Input.CursorShape.Ibeam);
    }
}
```

---

## Math — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/math/index.html

**Contents:**
- Math

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Vector math — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/math/vector_math.html

**Contents:**
- Vector math
- Introduction
- Coordinate systems (2D)
- Vector operations
  - Member access
  - Adding vectors
  - Scalar multiplication
- Practical applications
  - Movement
  - Pointing toward a target

This tutorial is a short and practical introduction to linear algebra as it applies to game development. Linear algebra is the study of vectors and their uses. Vectors have many applications in both 2D and 3D development and Godot uses them extensively. Developing a good understanding of vector math is essential to becoming a strong game developer.

This tutorial is not a formal textbook on linear algebra. We will only be looking at how it is applied to game development. For a broader look at the mathematics, see https://www.khanacademy.org/math/linear-algebra

In 2D space, coordinates are defined using a horizontal axis (x) and a vertical axis (y). A particular position in 2D space is written as a pair of values such as (4, 3).

If you're new to computer graphics, it might seem odd that the positive y axis points downwards instead of upwards, as you probably learned in math class. However, this is common in most computer graphics applications.

Any position in the 2D plane can be identified by a pair of numbers in this way. However, we can also think of the position (4, 3) as an offset from the (0, 0) point, or origin. Draw an arrow pointing from the origin to the point:

This is a vector. A vector represents a lot of useful information. As well as telling us that the point is at (4, 3), we can also think of it as an angle θ (theta) and a length (or magnitude) m. In this case, the arrow is a position vector - it denotes a position in space, relative to the origin.

A very important point to consider about vectors is that they only represent relative direction and magnitude. There is no concept of a vector's position. The following two vectors are identical:

Both vectors represent a point 4 units to the right and 3 units below some starting point. It does not matter where on the plane you draw the vector, it always represents a relative direction and magnitude.

You can use either method (x and y coordinates or angle and magnitude) to refer to a vector, but for convenience, programmers typically use the coordinate notation. For example, in Godot, the origin is the top-left corner of the screen, so to place a 2D node named Node2D 400 pixels to the right and 300 pixels down, use the following code:

Godot supports both Vector2 and Vector3 for 2D and 3D usage, respectively. The same mathematical rules discussed in this article apply to both types, and wherever we link to Vector2 methods in the class reference, you can also check out their Vector3 counterparts.

The individual components of the vector can be accessed directly by name.

When adding or subtracting two vectors, the corresponding components are added:

We can also see this visually by adding the second vector at the end of the first:

Note that adding a + b gives the same result as b + a.

Vectors represent both direction and magnitude. A value representing only magnitude is called a scalar. Scalars use the float type in Godot.

A vector can be multiplied by a scalar:

Multiplying a vector by a positive scalar does not change its direction, only its magnitude. Multiplying with a negative scalar results in a vector in the opposite direction. This is how you scale a vector.

Let's look at two common uses for vector addition and subtraction.

A vector can represent any quantity with a magnitude and direction. Typical examples are: position, velocity, acceleration, and force. In this image, the spaceship at step 1 has a position vector of (1, 3) and a velocity vector of (2, 1). The velocity vector represents how far the ship moves each step. We can find the position for step 2 by adding the velocity to the current position.

Velocity measures the change in position per unit of time. The new position is found by adding the velocity multiplied by the elapsed time (here assumed to be one unit, e.g. 1 s) to the previous position.

In a typical 2D game scenario, you would have a velocity in pixels per second, and multiply it by the delta parameter (time elapsed since the previous frame) from the _process() or _physics_process() callbacks.

In this scenario, you have a tank that wishes to point its turret at a robot. Subtracting the tank's position from the robot's position gives the vector pointing from the tank to the robot.

To find a vector pointing from A to B, use B - A.

A vector with magnitude of 1 is called a unit vector. They are also sometimes referred to as direction vectors or normals. Unit vectors are helpful when you need to keep track of a direction.

Normalizing a vector means reducing its length to 1 while preserving its direction. This is done by dividing each of its components by its magnitude. Because this is such a common operation, Godot provides a dedicated normalized() method for this:

Because normalization involves dividing by the vector's length, you cannot normalize a vector of length 0. Attempting to do so would normally result in an error. In GDScript though, trying to call the normalized() method on a vector of length 0 leaves the value untouched and avoids the error for you.

A common use of unit vectors is to indicate normals. Normal vectors are unit vectors aligned perpendicularly to a surface, defining its direction. They are commonly used for lighting, collisions, and other operations involving surfaces.

For example, imagine we have a moving ball that we want to bounce off a wall or other object:

The surface normal has a value of (0, -1) because this is a horizontal surface. When the ball collides, we take its remaining motion (the amount left over when it hits the surface) and reflect it using the normal. In Godot, there is a bounce() method to handle this. Here is a code example of the above diagram using a CharacterBody2D:

The dot product is one of the most important concepts in vector math, but is often misunderstood. Dot product is an operation on two vectors that returns a scalar. Unlike a vector, which contains both magnitude and direction, a scalar value has only magnitude.

The formula for dot product takes two common forms:

The mathematical notation ||A|| represents the magnitude of vector A, and Ax means the x component of vector A.

However, in most cases it is easiest to use the built-in dot() method. Note that the order of the two vectors does not matter:

The dot product is most useful when used with unit vectors, making the first formula reduce to just cos(θ). This means we can use the dot product to tell us something about the angle between two vectors:

When using unit vectors, the result will always be between -1 (180°) and 1 (0°).

We can use this fact to detect whether an object is facing toward another object. In the diagram below, the player P is trying to avoid the zombies A and B. Assuming a zombie's field of view is 180°, can they see the player?

The green arrows fA and fB are unit vectors representing the zombie's facing direction and the blue semicircle represents its field of view. For zombie A, we find the direction vector AP pointing to the player using P - A and normalize it, however, Godot has a helper method to do this called direction_to(). If the angle between this vector and the facing vector is less than 90°, then the zombie can see the player.

In code it would look like this:

Like the dot product, the cross product is an operation on two vectors. However, the result of the cross product is a vector with a direction that is perpendicular to both. Its magnitude depends on their relative angle. If two vectors are parallel, the result of their cross product will be a null vector.

The cross product is calculated like this:

With Godot, you can use the built-in Vector3.cross() method:

The cross product is not mathematically defined in 2D. The Vector2.cross() method is a commonly used analog of the 3D cross product for 2D vectors.

In the cross product, order matters. a.cross(b) does not give the same result as b.cross(a). The resulting vectors point in opposite directions.

One common use of cross products is to find the surface normal of a plane or surface in 3D space. If we have the triangle ABC we can use vector subtraction to find two edges AB and AC. Using the cross product, AB × AC produces a vector perpendicular to both: the surface normal.

Here is a function to calculate a triangle's normal:

In the dot product section above, we saw how it could be used to find the angle between two vectors. However, in 3D, this is not enough information. We also need to know what axis to rotate around. We can find that by calculating the cross product of the current facing direction and the target direction. The resulting perpendicular vector is the axis of rotation.

For more information on using vector math in Godot, see the following articles:

Matrices and transforms

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
$Node2D.position = Vector2(400, 300)
```

Example 2 (csharp):
```csharp
var node2D = GetNode<Node2D>("Node2D");
node2D.Position = new Vector2(400, 300);
```

Example 3 (csharp):
```csharp
# Create a vector with coordinates (2, 5).
var a = Vector2(2, 5)
# Create a vector and assign x and y manually.
var b = Vector2()
b.x = 3
b.y = 1
```

Example 4 (csharp):
```csharp
// Create a vector with coordinates (2, 5).
var a = new Vector2(2, 5);
// Create a vector and assign x and y manually.
var b = new Vector2();
b.X = 3;
b.Y = 1;
```

---

## Advanced vector math — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/math/vectors_advanced.html

**Contents:**
- Advanced vector math
- Planes
  - Distance to plane
  - Away from the origin
  - Constructing a plane in 2D
  - Some examples of planes
- Collision detection in 3D
- More information
- User-contributed notes

The dot product has another interesting property with unit vectors. Imagine that perpendicular to that vector (and through the origin) passes a plane. Planes divide the entire space into positive (over the plane) and negative (under the plane), and (contrary to popular belief) you can also use their math in 2D:

Unit vectors that are perpendicular to a surface (so, they describe the orientation of the surface) are called unit normal vectors. Though, usually they are just abbreviated as normals. Normals appear in planes, 3D geometry (to determine where each face or vertex is siding), etc. A normal is a unit vector, but it's called normal because of its usage. (Just like we call (0,0) the Origin!).

The plane passes by the origin and the surface of it is perpendicular to the unit vector (or normal). The side the vector points to is the positive half-space, while the other side is the negative half-space. In 3D this is exactly the same, except that the plane is an infinite surface (imagine an infinite, flat sheet of paper that you can orient and is pinned to the origin) instead of a line.

Now that it's clear what a plane is, let's go back to the dot product. The dot product between a unit vector and any point in space (yes, this time we do dot product between vector and position), returns the distance from the point to the plane:

But not just the absolute distance, if the point is in the negative half space the distance will be negative, too:

This allows us to tell which side of the plane a point is.

I know what you are thinking! So far this is nice, but real planes are everywhere in space, not only passing through the origin. You want real plane action and you want it now.

Remember that planes not only split space in two, but they also have polarity. This means that it is possible to have perfectly overlapping planes, but their negative and positive half-spaces are swapped.

With this in mind, let's describe a full plane as a normal N and a distance from the origin scalar D. Thus, our plane is represented by N and D. For example:

For 3D math, Godot provides a Plane built-in type that handles this.

Basically, N and D can represent any plane in space, be it for 2D or 3D (depending on the amount of dimensions of N) and the math is the same for both. It's the same as before, but D is the distance from the origin to the plane, travelling in N direction. As an example, imagine you want to reach a point in the plane, you will just do:

This will stretch (resize) the normal vector and make it touch the plane. This math might seem confusing, but it's actually much simpler than it seems. If we want to tell, again, the distance from the point to the plane, we do the same but adjusting for distance:

The same thing, using a built-in function:

This will, again, return either a positive or negative distance.

Flipping the polarity of the plane can be done by negating both N and D. This will result in a plane in the same position, but with inverted negative and positive half spaces:

Godot also implements this operator in Plane. So, using the format below will work as expected:

So, remember, the plane's main practical use is that we can calculate the distance to it. So, when is it useful to calculate the distance from a point to a plane? Let's see some examples.

Planes clearly don't come out of nowhere, so they must be built. Constructing them in 2D is easy, this can be done from either a normal (unit vector) and a point, or from two points in space.

In the case of a normal and a point, most of the work is done, as the normal is already computed, so calculate D from the dot product of the normal and the point.

For two points in space, there are actually two planes that pass through them, sharing the same space but with normal pointing to the opposite directions. To compute the normal from the two points, the direction vector must be obtained first, and then it needs to be rotated 90 degrees to either side:

The rest is the same as the previous example. Either point_a or point_b will work, as they are in the same plane:

Doing the same in 3D is a little more complex and is explained further down.

Here is an example of what planes are useful for. Imagine you have a convex polygon. For example, a rectangle, a trapezoid, a triangle, or just any polygon where no faces bend inwards.

For every segment of the polygon, we compute the plane that passes by that segment. Once we have the list of planes, we can do neat things, for example checking if a point is inside the polygon.

We go through all planes, if we can find a plane where the distance to the point is positive, then the point is outside the polygon. If we can't, then the point is inside.

Code should be something like this:

Pretty cool, huh? But this gets much better! With a little more effort, similar logic will let us know when two convex polygons are overlapping too. This is called the Separating Axis Theorem (or SAT) and most physics engines use this to detect collision.

With a point, just checking if a plane returns a positive distance is enough to tell if the point is outside. With another polygon, we must find a plane where all the other polygon points return a positive distance to it. This check is performed with the planes of A against the points of B, and then with the planes of B against the points of A:

Code should be something like this:

As you can see, planes are quite useful, and this is the tip of the iceberg. You might be wondering what happens with non convex polygons. This is usually just handled by splitting the concave polygon into smaller convex polygons, or using a technique such as BSP (which is not used much nowadays).

This is another bonus bit, a reward for being patient and keeping up with this long tutorial. Here is another piece of wisdom. This might not be something with a direct use case (Godot already does collision detection pretty well) but it's used by almost all physics engines and collision detection libraries :)

Remember that converting a convex shape in 2D to an array of 2D planes was useful for collision detection? You could detect if a point was inside any convex shape, or if two 2D convex shapes were overlapping.

Well, this works in 3D too, if two 3D polyhedral shapes are colliding, you won't be able to find a separating plane. If a separating plane is found, then the shapes are definitely not colliding.

To refresh a bit a separating plane means that all vertices of polygon A are in one side of the plane, and all vertices of polygon B are in the other side. This plane is always one of the face-planes of either polygon A or polygon B.

In 3D though, there is a problem to this approach, because it is possible that, in some cases a separating plane can't be found. This is an example of such situation:

To avoid it, some extra planes need to be tested as separators, these planes are the cross product between the edges of polygon A and the edges of polygon B

So the final algorithm is something like:

For more information on using vector math in Godot, see the following article:

Matrices and transforms

If you would like additional explanation, you should check out 3Blue1Brown's excellent video series Essence of Linear Algebra.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var distance = normal.dot(point)
```

Example 2 (gdscript):
```gdscript
var distance = normal.Dot(point);
```

Example 3 (gdscript):
```gdscript
var point_in_plane = N*D
```

Example 4 (gdscript):
```gdscript
var pointInPlane = N * D;
```

---

## Interpolation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/math/interpolation.html

**Contents:**
- Interpolation
- Vector interpolation
- Transform interpolation
- Smoothing motion
- User-contributed notes

Interpolation is a common operation in graphics programming, which is used to blend or transition between two values. Interpolation can also be used to smooth movement, rotation, etc. It's good to become familiar with it in order to expand your horizons as a game developer.

The basic idea is that you want to transition from A to B. A value t, represents the states in-between.

For example, if t is 0, then the state is A. If t is 1, then the state is B. Anything in-between is an interpolation.

Between two real (floating-point) numbers, an interpolation can be described as:

And often simplified to:

The name of this type of interpolation, which transforms a value into another at constant speed is "linear". So, when you hear about Linear Interpolation, you know they are referring to this formula.

There are other types of interpolations, which will not be covered here. A recommended read afterwards is the Bezier page.

Vector types (Vector2 and Vector3) can also be interpolated, they come with handy functions to do it Vector2.lerp() and Vector3.lerp().

For cubic interpolation, there are also Vector2.cubic_interpolate() and Vector3.cubic_interpolate(), which do a Bezier style interpolation.

Here is example pseudo-code for going from point A to B using interpolation:

It will produce the following motion:

It is also possible to interpolate whole transforms (make sure they have either uniform scale or, at least, the same non-uniform scale). For this, the function Transform3D.interpolate_with() can be used.

Here is an example of transforming a monkey from Position1 to Position2:

Using the following pseudocode:

And again, it will produce the following motion:

Interpolation can be used to smoothly follow a moving target value, such as a position or a rotation. Each frame, lerp() moves the current value towards the target value by a fixed percentage of the remaining difference between the values. The current value will smoothly move towards the target, slowing down as it gets closer. Here is an example of a circle following the mouse using interpolation smoothing:

Here is how it looks:

This is useful for smoothing camera movement, for allies following the player (ensuring they stay within a certain range), and for many other common game patterns.

Despite using delta, the formula used above is framerate-dependent, because the weight parameter of lerp() represents a percentage of the remaining difference in values, not an absolute amount to change. In _physics_process(), this is usually fine because physics is expected to maintain a constant framerate, and therefore delta is expected to remain constant.

For a framerate-independent version of interpolation smoothing that can also be used in process(), use the following formula instead:

Deriving this formula is beyond the scope of this page. For an explanation, see Improved Lerp Smoothing or watch Lerp smoothing is broken.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
interpolation = A * (1 - t) + B * t
```

Example 2 (unknown):
```unknown
interpolation = A + (B - A) * t
```

Example 3 (gdscript):
```gdscript
var t = 0.0

func _physics_process(delta):
    t += delta * 0.4

    $Sprite2D.position = $A.position.lerp($B.position, t)
```

Example 4 (json):
```json
private float _t = 0.0f;

public override void _PhysicsProcess(double delta)
{
    _t += (float)delta * 0.4f;

    Marker2D a = GetNode<Marker2D>("A");
    Marker2D b = GetNode<Marker2D>("B");
    Sprite2D sprite = GetNode<Sprite2D>("Sprite2D");

    sprite.Position = a.Position.Lerp(b.Position, _t);
}
```

---

## Using NavigationMaps — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmaps.html

**Contents:**
- Using NavigationMaps
- Default navigation maps
- Creating new navigation maps
- User-contributed notes

A NavigationMap is an abstract navigation world on the NavigationServer identified by a NavigationServer RID.

A map can hold and connect a near infinite number of navigation regions with navigation meshes to build the traversable areas of a game world for pathfinding.

A map can contain avoidance agents. Collision avoidance will be calculated based on the agents present in the map.

Different NavigationMaps are completely isolated from each other but navigation regions and avoidance agents can switch between different maps. Switches will become effective on NavigationServer synchronization.

By default Godot creates a navigation map for each World2D and World3D of the root viewport.

The 2D default navigation map RID can be obtained with get_world_2d().get_navigation_map() from any Node2D inheriting Node.

The 3D default navigation map RID can be obtained with get_world_3d().get_navigation_map() from any Node3D inheriting Node.

The NavigationServer can create and support as many navigation maps as required for specific gameplay. Additional navigation maps are created and handled by using the NavigationServer API directly e.g. to support different avoidance agent or actor locomotion types.

For example uses of different navigation maps see Support different actor types and Support different actor locomotion.

Each navigation map individually synchronizes queued changes to its navigation regions and avoidance agents. A navigation map that has not received changes will consume little to no processing time. Navigation regions and avoidance agents can only be part of a single navigation map but they can switch map at any time.

A navigation map switch will take effect only after the next NavigationServer synchronization.

There is no difference between navigation maps created with the NavigationServer2D API or the NavigationServer3D API.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node2D

func _ready() -> void:
    var default_navigation_map_rid: RID = get_world_2d().get_navigation_map()
```

Example 2 (gdscript):
```gdscript
public partial class MyNode2D : Node2D
{
    public override void _Ready()
    {
        Rid defaultNavigationMapRid = GetWorld2D().NavigationMap;
    }
}
```

Example 3 (gdscript):
```gdscript
extends Node3D

func _ready() -> void:
    var default_navigation_map_rid: RID = get_world_3d().get_navigation_map()
```

Example 4 (gdscript):
```gdscript
public partial class MyNode3D : Node3D
{
    public override void _Ready()
    {
        Rid defaultNavigationMapRid = GetWorld3D().NavigationMap;
    }
}
```

---

## Beziers, curves and paths — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/math/beziers_and_curves.html

**Contents:**
- Beziers, curves and paths
- Quadratic Bezier
- Cubic Bezier
- Adding control points
- Curve2D, Curve3D, Path and Path2D
- Evaluating
- Drawing
- Traversal
- User-contributed notes

Bezier curves are a mathematical approximation of natural geometric shapes. We use them to represent a curve with as little information as possible and with a high level of flexibility.

Unlike more abstract mathematical concepts, Bezier curves were created for industrial design. They are a popular tool in the graphics software industry.

They rely on interpolation, which we saw in the previous article, combining multiple steps to create smooth curves. To better understand how Bezier curves work, let's start from its simplest form: Quadratic Bezier.

Take three points, the minimum required for Quadratic Bezier to work:

To draw a curve between them, we first interpolate gradually over the two vertices of each of the two segments formed by the three points, using values ranging from 0 to 1. This gives us two points that move along the segments as we change the value of t from 0 to 1.

We then interpolate q0 and q1 to obtain a single point r that moves along a curve.

This type of curve is called a Quadratic Bezier curve.

(Image credit: Wikipedia)

Building upon the previous example, we can get more control by interpolating between four points.

We first use a function with four parameters to take four points as an input, p0, p1, p2 and p3:

We apply a linear interpolation to each couple of points to reduce them to three:

We then take our three points and reduce them to two:

Here is the full function:

The result will be a smooth curve interpolating between all four points:

(Image credit: Wikipedia)

Cubic Bezier interpolation works the same in 3D, just use Vector3 instead of Vector2.

Building upon Cubic Bezier, we can change the way two of the points work to control the shape of our curve freely. Instead of having p0, p1, p2 and p3, we will store them as:

point0 = p0: Is the first point, the source

control0 = p1 - p0: Is a vector relative to the first control point

control1 = p3 - p2: Is a vector relative to the second control point

point1 = p3: Is the second point, the destination

This way, we have two points and two control points which are relative vectors to the respective points. If you've used graphics or animation software before, this might look familiar:

This is how graphics software presents Bezier curves to the users, and how they work and look in Godot.

There are two objects that contain curves: Curve3D and Curve2D (for 3D and 2D respectively).

They can contain several points, allowing for longer paths. It is also possible to set them to nodes: Path3D and Path2D (also for 3D and 2D respectively):

Using them, however, may not be completely obvious, so following is a description of the most common use cases for Bezier curves.

Only evaluating them may be an option, but in most cases it's not very useful. The big drawback with Bezier curves is that if you traverse them at constant speed, from t = 0 to t = 1, the actual interpolation will not move at constant speed. The speed is also an interpolation between the distances between points p0, p1, p2 and p3 and there is not a mathematically simple way to traverse the curve at constant speed.

Let's do an example with the following pseudocode:

As you can see, the speed (in pixels per second) of the circle varies, even though t is increased at constant speed. This makes beziers difficult to use for anything practical out of the box.

Drawing beziers (or objects based on the curve) is a very common use case, but it's also not easy. For pretty much any case, Bezier curves need to be converted to some sort of segments. This is normally difficult, however, without creating a very high amount of them.

The reason is that some sections of a curve (specifically, corners) may require considerable amounts of points, while other sections may not:

Additionally, if both control points were 0, 0 (remember they are relative vectors), the Bezier curve would just be a straight line (so drawing a high amount of points would be wasteful).

Before drawing Bezier curves, tessellation is required. This is often done with a recursive or divide and conquer function that splits the curve until the curvature amount becomes less than a certain threshold.

The Curve classes provide this via the Curve2D.tessellate() function (which receives optional stages of recursion and angle tolerance arguments). This way, drawing something based on a curve is easier.

The last common use case for the curves is to traverse them. Because of what was mentioned before regarding constant speed, this is also difficult.

To make this easier, the curves need to be baked into equidistant points. This way, they can be approximated with regular interpolation (which can be improved further with a cubic option). To do this, just use the Curve3D.sample_baked() method together with Curve2D.get_baked_length(). The first call to either of them will bake the curve internally.

Traversal at constant speed, then, can be done with the following pseudo-code:

And the output will, then, move at constant speed:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
func _quadratic_bezier(p0: Vector2, p1: Vector2, p2: Vector2, t: float):
    var q0 = p0.lerp(p1, t)
    var q1 = p1.lerp(p2, t)
```

Example 2 (csharp):
```csharp
private Vector2 QuadraticBezier(Vector2 p0, Vector2 p1, Vector2 p2, float t)
{
    Vector2 q0 = p0.Lerp(p1, t);
    Vector2 q1 = p1.Lerp(p2, t);
}
```

Example 3 (gdscript):
```gdscript
var r = q0.lerp(q1, t)
return r
```

Example 4 (csharp):
```csharp
Vector2 r = q0.Lerp(q1, t);
return r;
```

---

## Navigation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/index.html

**Contents:**
- Navigation

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using NavigationServer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html

**Contents:**
- Using NavigationServer
- Communicating with the NavigationServer
- Threading and Synchronization
- 2D and 3D NavigationServer differences
- Waiting for synchronization
- Server Avoidance Callbacks
- User-contributed notes

2D and 3D version of the NavigationServer are available as NavigationServer2D and NavigationServer3D respectively.

To work with the NavigationServer means to prepare parameters for a query that can be sent to the NavigationServer for updates or requesting data.

To reference the internal NavigationServer objects like maps, regions and agents RIDs are used as identification numbers. Every navigation related node in the scene tree has a function that returns the RID for this node.

The NavigationServer does not update every change immediately but waits until the end of the physics frame to synchronize all the changes together.

Waiting for synchronization is required to apply changes to all maps, regions and agents. Synchronization is done because some updates like a recalculation of the entire navigation map are very expensive and require updated data from all other objects. Also the NavigationServer uses a threadpool by default for some functionality like avoidance calculation between agents.

Waiting is not required for most get() functions that only request data from the NavigationServer without making changes. Note that not all data will account for changes made in the same frame. E.g. if an avoidance agent changed the navigation map this frame the agent_get_map() function will still return the old map before the synchronization. The exception to this are nodes that store their values internally before sending the update to the NavigationServer. When a getter on a node is used for a value that was updated in the same frame it will return the already updated value stored on the node.

The NavigationServer is thread-safe as it places all API calls that want to make changes in a queue to be executed in the synchronization phase. Synchronization for the NavigationServer happens in the middle of the physics frame after scene input from scripts and nodes are all done.

The important takeaway is that most NavigationServer changes take effect after the next physics frame and not immediately. This includes all changes made by navigation related nodes in the scene tree or through scripts.

All setters and delete functions require synchronization.

NavigationServer2D and NavigationServer3D are equivalent in functionality for their dimension.

Technically it is possible to use the tools for creating navigation meshes in one dimension for the other dimension, e.g. baking a 2D navigation mesh with the 3D NavigationMesh when using flat 3D source geometry or creating 3D flat navigation meshes with the polygon outline draw tools of NavigationRegion2D and NavigationPolygons.

At the start of the game, a new scene or procedural navigation changes any path query to a NavigationServer will return empty or wrong.

The navigation map is still empty or not updated at this point. All nodes from the scene tree need to first upload their navigation related data to the NavigationServer. Each added or changed map, region or agent need to be registered with the NavigationServer. Afterward the NavigationServer requires a physics frame for synchronization to update the maps, regions and agents.

One workaround is to make a deferred call to a custom setup function (so all nodes are ready). The setup function makes all the navigation changes, e.g. adding procedural stuff. Afterwards the function waits for the next physics frame before continuing with path queries.

If RVO avoidance agents are registered for avoidance callbacks the NavigationServer dispatches their velocity_computed signals just before the PhysicsServer synchronization.

To learn more about NavigationAgents see Using NavigationAgents.

The simplified order of execution for NavigationAgents that use avoidance:

physics frame starts.

_physics_process(delta).

velocity property is set on NavigationAgent Node.

Agent sends velocity and position to NavigationServer.

NavigationServer waits for synchronization.

NavigationServer synchronizes and computes avoidance velocities for all registered avoidance agents.

NavigationServer sends safe velocity vector with signals for each registered avoidance agents.

Agents receive the signal and move their parent e.g. with move_and_slide or linear_velocity.

PhysicsServer synchronizes.

Therefore moving a physicsbody actor in the callback function with the safe velocity is perfectly thread- and physics-safe as all happens inside the same physics frame before the PhysicsServer commits to changes and does its own calculations.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node3D

func _ready():
    # Use call deferred to make sure the entire scene tree nodes are setup
    # else await on 'physics_frame' in a _ready() might get stuck.
    custom_setup.call_deferred()

func custom_setup():

    # Create a new navigation map.
    var map: RID = NavigationServer3D.map_create()
    NavigationServer3D.map_set_up(map, Vector3.UP)
    NavigationServer3D.map_set_active(map, true)

    # Create a new navigation region and add it to the map.
    var region: RID = NavigationServer3D.region_create()
    NavigationServer3D.region_set_transform(region, Transform3D())
    NavigationServer3D.region_set_map(region, map)

    # Create a procedural navigation mesh for the region.
    var new_navigation_mesh: NavigationMesh = NavigationMesh.new()
    var vertices: PackedVector3Array = PackedVector3Array([
        Vector3(0, 0, 0),
        Vector3(9.0, 0, 0),
        Vector3(0, 0, 9.0)
    ])
    new_navigation_mesh.set_vertices(vertices)
    var polygon: PackedInt32Array = PackedInt32Array([0, 1, 2])
    new_navigation_mesh.add_polygon(polygon)
    NavigationServer3D.region_set_navigation_mesh(region, new_navigation_mesh)

    # Wait for NavigationServer sync to adapt to made changes.
    await get_tree().physics_frame

    # Query the path from the navigation server.
    var start_position: Vector3 = Vector3(0.1, 0.0, 0.1)
    var target_position: Vector3 = Vector3(1.0, 0.0, 1.0)
    var optimize_path: bool = true

    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        map,
        start_position,
        target_position,
        optimize_path
    )

    print("Found a path!")
    print(path)
```

Example 2 (swift):
```swift
using Godot;

public partial class MyNode3D : Node3D
{
    public override void _Ready()
    {
        // Use call deferred to make sure the entire scene tree nodes are setup
        // else await on 'physics_frame' in a _Ready() might get stuck.
        CallDeferred(MethodName.CustomSetup);
    }

    private async void CustomSetup()
    {
        // Create a new navigation map.
        Rid map = NavigationServer3D.MapCreate();
        NavigationServer3D.MapSetUp(map, Vector3.Up);
        NavigationServer3D.MapSetActive(map, true);

        // Create a new navigation region and add it to the map.
        Rid region = NavigationServer3D.RegionCreate();
        NavigationServer3D.RegionSetTransform(region, Transform3D.Identity);
        NavigationServer3D.RegionSetMap(region, map);

        // Create a procedural navigation mesh for the region.
        var newNavigationMesh = new NavigationMesh()
        {
            Vertices =
            [
                new Vector3(0.0f, 0.0f, 0.0f),
                new Vector3(9.0f, 0.0f, 0.0f),
                new Vector3(0.0f, 0.0f, 9.0f),
            ],
        };
        int[] polygon = [0, 1, 2];
        newNavigationMesh.AddPolygon(polygon);
        NavigationServer3D.RegionSetNavigationMesh(region, newNavigationMesh);

        // Wait for NavigationServer sync to adapt to made changes.
        await ToSignal(GetTree(), SceneTree.SignalName.PhysicsFrame);

        // Query the path from the navigation server.
        var startPosition = new Vector3(0.1f, 0.0f, 0.1f);
        var targetPosition = new Vector3(1.0f, 0.0f, 1.0f);

        Vector3[] path = NavigationServer3D.MapGetPath(map, startPosition, targetPosition, optimize: true);

        GD.Print("Found a path!");
        GD.Print((Variant)path);
    }
}
```

---

## Using NavigationPaths — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationpaths.html

**Contents:**
- Using NavigationPaths
- Obtaining a NavigationPath
- User-contributed notes

Navigation paths can be directly queried from the NavigationServer and do not require any additional nodes or objects as long as the navigation map has a navigation mesh to work with.

To obtain a 2D path, use NavigationServer2D.map_get_path(map, from, to, optimize, navigation_layers).

To obtain a 3D path, use NavigationServer3D.map_get_path(map, from, to, optimize, navigation_layers).

For more customizable navigation path queries that require additional setup see Using NavigationPathQueryObjects.

One of the required parameters for the query is the RID of the navigation map. Each game world has a default navigation map automatically created. The default navigation maps can be retrieved with get_world_2d().get_navigation_map() from any Node2D inheriting node or get_world_3d().get_navigation_map() from any Node3D inheriting node. The second and third parameters are the starting position and the target position as Vector2 for 2D or Vector3 for 3D.

If the optimized parameter is true, path positions will be shortened along polygon corners with an additional funnel algorithm pass. This works well for free movement on navigation meshes with unequally sized polygons as the path will hug around corners along the polygon corridor found by the A* algorithm. With small cells the A* algorithm creates a very narrow funnel corridor that can create ugly corner paths when used with grids.

If the optimized parameter is false, path positions will be placed at the center of each polygon edge. This works well for pure grid movement on navigation meshes with equally sized polygons as the path will go through the center of the grid cells. Outside of grids due to polygons often covering large open areas with a single, long edge this can create paths with unnecessary long detours.

A returned path by the NavigationServer will be a PackedVector2Array for 2D or a PackedVector3Array for 3D. These are just a memory-optimized Array of vector positions. All position vectors inside the array are guaranteed to be inside a NavigationPolygon or NavigationMesh. The path array, if not empty, has the navigation mesh position closest to the starting position at the first index path[0] position. The closest available navigation mesh position to the target position is the last index path[path.size()-1] position. All indexes between are the path points that an actor should follow to reach the target without leaving the navigation mesh.

If the target position is on a different navigation mesh that is not merged or connected the navigation path will lead to the closest possible position on the starting position navigation mesh.

The following script moves a Node3D inheriting node along a navigation path using the default navigation map by setting the target position with set_movement_target().

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends Node2D

# Basic query for a navigation path using the default navigation map.

func get_navigation_path(p_start_position: Vector2, p_target_position: Vector2) -> PackedVector2Array:
    if not is_inside_tree():
        return PackedVector2Array()

    var default_map_rid: RID = get_world_2d().get_navigation_map()
    var path: PackedVector2Array = NavigationServer2D.map_get_path(
        default_map_rid,
        p_start_position,
        p_target_position,
        true
    )
    return path
```

Example 2 (csharp):
```csharp
using Godot;
using System;

public partial class MyNode2D : Node2D
{
    // Basic query for a navigation path using the default navigation map.

    private Vector2[] GetNavigationPath(Vector2 startPosition, Vector2 targetPosition)
    {
        if (!IsInsideTree())
        {
            return Array.Empty<Vector2>();
        }

        Rid defaultMapRid = GetWorld2D().NavigationMap;
        Vector2[] path = NavigationServer2D.MapGetPath(
            defaultMapRid,
            startPosition,
            targetPosition,
            true
        );
        return path;
    }
}
```

Example 3 (swift):
```swift
extends Node3D

# Basic query for a navigation path using the default navigation map.

func get_navigation_path(p_start_position: Vector3, p_target_position: Vector3) -> PackedVector3Array:
    if not is_inside_tree():
        return PackedVector3Array()

    var default_map_rid: RID = get_world_3d().get_navigation_map()
    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        default_map_rid,
        p_start_position,
        p_target_position,
        true
    )
    return path
```

Example 4 (csharp):
```csharp
using Godot;
using System;

public partial class MyNode3D : Node3D
{
    // Basic query for a navigation path using the default navigation map.

    private Vector3[] GetNavigationPath(Vector3 startPosition, Vector3 targetPosition)
    {
        if (!IsInsideTree())
        {
            return Array.Empty<Vector3>();
        }

        Rid defaultMapRid = GetWorld3D().NavigationMap;
        Vector3[] path = NavigationServer3D.MapGetPath(
            defaultMapRid,
            startPosition,
            targetPosition,
            true
        );
        return path;
    }
}
```

---

## Using NavigationPathQueryObjects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationpathqueryobjects.html

**Contents:**
- Using NavigationPathQueryObjects
- Creating a basic path query
- Path postprocessing options
- Path simplification
- Path metadata
- Excluding or including regions
- Path clipping and limits
- User-contributed notes

Path query parameters expose various options to improve pathfinding performance or lower memory consumption.

They cater to more advanced pathfinding needs that the high-level nodes can not always cover.

See the respective option sections below.

NavigationPathQueryObjects can be used together with NavigationServer.query_path() to obtain a heavily customized navigation path including optional metadata about the path.

This requires more setup compared to obtaining a normal NavigationPath but lets you tailor the pathfinding and provided path data to the different needs of a project.

NavigationPathQueryObjects consist of a pair of objects, a NavigationPathQueryParameters object holding the customization options for the query and a NavigationPathQueryResult that receives (regular) updates with the resulting path and metadata from the query.

2D and 3D versions of NavigationPathQueryParameters are available as NavigationPathQueryParameters2D and NavigationPathQueryParameters3D respectively.

2D and 3D versions of NavigationPathQueryResult are available as NavigationPathQueryResult2D and NavigationPathQueryResult3D respectively.

Both parameters and result are used as a pair with the NavigationServer.query_path() function.

For the available customization options, see further below. See also the descriptions for each parameter in the class reference.

While not a strict requirement, both objects are intended to be created once in advance, stored in a persistent variable for the agent and reused for every followup path query with updated parameters.

Reusing the same objects improves performance when frequently creating objects or allocating memory.

The following script creates the objects and provides a query_path() function to create new navigation paths. The resulting path is identical to using NavigationServer.map_get_path() while reusing the objects.

Path post-processing differences depending on navigation mesh polygon layout.

A path query search travels from the closest navigation mesh polygon edge to the closest edge along the available polygons. If possible it builds a polygon corridor towards the target position polygon.

This raw "search" polygon corridor path is not very optimized and usually a bad fit for agents to travel along. E.g. the closest edge point on a navigation mesh polygon might cause a huge detour for agents on larger polygons. In order to improve the quality of paths returned by the query various path_postprocessing options exist.

The PATH_POSTPROCESSING_CORRIDORFUNNEL post-processing shortens paths by funneling paths around corners inside the available polygon corridor.

This is the default post-processing and usually also the most useful as it gives the shortest path result inside the available polygon corridor. If the polygon corridor is already suboptimal, e.g. due to a suboptimal navigation mesh layout, the funnel can snap to unexpected polygon corners causing detours.

The PATH_POSTPROCESSING_EDGECENTERED post-processing forces all path points to be placed in the middle of the crossed polygon edges inside the available polygon corridor.

This post-processing is usually only useful when used with strictly tile-like navigation mesh polygons that are all evenly sized and where the expected path following is also constrained to cell centers, e.g. typical grid game with movement constrained to grid cell centers.

The PATH_POSTPROCESSING_NONE post-processing returns the path as is how the pathfinding traveled inside the available polygon corridor.

This post-processing is very useful for debug as it shows how the path search traveled from closest edge point to closet edge point and what polygons it picked. A lot of unexpected or suboptimal path results can be immediately explained by looking at this raw path and polygon corridor.

Path simplification can help steering agents or agents that jitter on thin polygon edges.

Path point difference with or without path simplification.

If simplify_path is enabled a variant of the Ramer-Douglas-Peucker path simplification algorithm is applied to the path. This algorithm straightens paths by removing less relevant path points depending on the simplify_epsilon used.

Path simplification helps with all kinds of agent movement problems in "open fields" that are caused by having many unnecessary polygon edges. E.g. a terrain mesh when baked to a navigation mesh can cause an excessive polygon count due to all the small (but for pathfinding almost meaningless) height variations in the terrain.

Path simplification also helps with "steering" agents because they only have more critical corner path points to aim for.

Path simplification is an additional final post-processing of the path. It adds extra performance costs to the query so only enable when actually needed.

Path simplification is exposed on the NavigationServer as a generic function. It can be used outside of navigation queries for all kinds of position arrays as well.

Disabling unneeded path metadata options can improve performance and lower memory consumption.

A path query can return additional metadata for every path point.

The PATH_METADATA_INCLUDE_TYPES flag collects an array with the primitive information about the point owners, e.g. if a point belongs to a region or link.

The PATH_METADATA_INCLUDE_RIDS flag collects an array with the RIDs of the point owners. Depending on point owner primitive, these RIDs can be used with the various NavigationServer functions related to regions or links.

The PATH_METADATA_INCLUDE_OWNERS flag collects an array with the ObjectIDs of the point owners. These object IDs can be used with @GlobalScope.instance_from_id() to retrieve the node behind that object instance, e.g. a NavigationRegion or NavigationLink node.

By default all path metadata is collected as this metadata can be essential for more advanced navigation gameplay.

E.g. to know what path point maps to what object or node owner inside the SceneTree.

E.g. to know if a path point is the start or end of a navigation link that requires scripted takeover.

For the most basic path uses metadata is not always needed. Path metadata collection can be selectively disabled to gain some performance and reduce memory consumption.

Region filters can greatly help with performance on large navigation maps that are region partitioned.

Query parameters allow limiting the pathfinding to specific region navigation meshes.

If a large navigation map is well partitioned into smaller regions this can greatly help with performance as the query can skip a large number of polygons at one of the earliest checks in the path search.

By default and if left empty all regions of the queried navigation map are included.

If a region RID is added to the excluded_regions array the region's navigation mesh will be ignored in the path search.

If a region RID is added to the included_regions array the region's navigation mesh will be considered in the path search and also all other regions not included will be ignored as well.

If a region ends up both included and excluded it is considered excluded.

Region filters are very effective for performance when paired with navigation region chunks that are aligned on a grid. This way the filter can be set to only include the start position chunk and surrounding chunks instead of the entire navigation map.

Even if the target might be outside these surrounding chunks (can always add more "rings") the pathfinding will try to create a path to the polygon closest to the target. This usually creates half-paths heading in the general direction that are good enough, all for a fraction of the performance cost of a full map search.

The following addition to the basic path query script showcases the idea how to integrate a region chunk mapping with the region filters. This is not a full working example.

Sensibly set limits can greatly help with performance on large navigation maps, especially when targets end up being unreachable.

Clipping returned paths to specific distances.

Query parameters allow clipping returned paths to specific lengths. These options clip the path as a part of post-processing. The path is still searched as if at full length, so it will have the same quality. Path length clipping can be helpful in creating paths that better fit constrained gameplay, e.g. tactical games with limited movement ranges.

The path_return_max_length property can be used to clip the returned path to a specific max length.

The path_return_max_radius property can be used to clip the returned path inside a circle (2D) or sphere (3D) radius around the start position.

Query parameters allow limiting the path search to only search up to a specific distance or a specific number of searched polygons. These options are for performance and affect the path search directly.

The path_search_max_distance property can be used to stop the path search when going over this distance from the start position.

The path_search_max_polygons property can be used to stop the path search when going over this searched polygon number.

When the path search is stopped by reaching a limit the path resets and creates a path from the start position polygon to the polygon found so far that is closest to the target position.

While good for performance, if path search limit values are set too low they can affect the path quality very negatively. Depending on polygon layout and search pattern the returned paths might go into completely wrong directions instead of the direction of the target.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends Node2D

# Prepare query objects.
var query_parameters := NavigationPathQueryParameters2D.new()
var query_result := NavigationPathQueryResult2D.new()

func query_path(p_start_position: Vector2, p_target_position: Vector2, p_navigation_layers: int = 1) -> PackedVector2Array:
    if not is_inside_tree():
        return PackedVector2Array()

    var map: RID = get_world_2d().get_navigation_map()

    if NavigationServer2D.map_get_iteration_id(map) == 0:
        # This map has never synced and is empty, no point in querying it.
        return PackedVector2Array()

    query_parameters.map = map
    query_parameters.start_position = p_start_position
    query_parameters.target_position = p_target_position
    query_parameters.navigation_layers = p_navigation_layers

    NavigationServer2D.query_path(query_parameters, query_result)
    var path: PackedVector2Array = query_result.get_path()

    return path
```

Example 2 (swift):
```swift
extends Node3D

# Prepare query objects.
var query_parameters := NavigationPathQueryParameters3D.new()
var query_result := NavigationPathQueryResult3D.new()

func query_path(p_start_position: Vector3, p_target_position: Vector3, p_navigation_layers: int = 1) -> PackedVector3Array:
    if not is_inside_tree():
        return PackedVector3Array()

    var map: RID = get_world_3d().get_navigation_map()

    if NavigationServer3D.map_get_iteration_id(map) == 0:
        # This map has never synced and is empty, no point in querying it.
        return PackedVector3Array()

    query_parameters.map = map
    query_parameters.start_position = p_start_position
    query_parameters.target_position = p_target_position
    query_parameters.navigation_layers = p_navigation_layers

    NavigationServer3D.query_path(query_parameters, query_result)
    var path: PackedVector3Array = query_result.get_path()

    return path
```

Example 3 (swift):
```swift
extends Node2D

# ...

var chunk_id_to_region_rid: Dictionary[Vector2i, RID] = {}

func query_path(p_start_position: Vector2, p_target_position: Vector2, p_navigation_layers: int = 1) -> PackedVector2Array:

    # ...

    var regions_around_start_position: Array[RID] = []

    var chunk_rings: int = 1 # Increase for very small regions or more quality.
    var start_chunk_id: Vector2i = floor(p_start_position / float(chunk_size))

    for y: int in range(start_chunk_id.y - chunk_rings, start_chunk_id.y + chunk_rings):
        for x: int in range(start_chunk_id.x - chunk_rings, start_chunk_id.x + chunk_rings):
            var chunk_id: Vector2i = Vector2i(x, y)
            if chunk_id_to_region_rid.has(chunk_id):
                var region: RID = chunk_id_to_region_rid[chunk_id]
                regions_around_start_position.push_back(region)

    query_parameters.included_regions = regions_around_start_position

    # ...
```

Example 4 (swift):
```swift
extends Node3D

# ...

var chunk_id_to_region_rid: Dictionary[Vector3i, RID] = {}

func query_path(p_start_position: Vector3, p_target_position: Vector3, p_navigation_layers: int = 1) -> PackedVector3Array:

    # ...

    var regions_around_start_position: Array[RID] = []

    var chunk_rings: int = 1 # Increase for very small regions or more quality.
    var start_chunk_id: Vector3i = floor(p_start_position / float(chunk_size))
    var y: int = 0 # Assume a planar navigation map for simplicity.

    for z: int in range(start_chunk_id.z - chunk_rings, start_chunk_id.z + chunk_rings):
        for x: int in range(start_chunk_id.x - chunk_rings, start_chunk_id.x + chunk_rings):
            var chunk_id: Vector3i = Vector3i(x, y, z)
            if chunk_id_to_region_rid.has(chunk_id):
                var region: RID = chunk_id_to_region_rid[chunk_id]
                regions_around_start_position.push_back(region)

    query_parameters.included_regions = regions_around_start_position

    # ...
```

---

## Using NavigationObstacles — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationobstacles.html

**Contents:**
- Using NavigationObstacles
- Obstacles and navigation mesh
- Obstacles and agent avoidance
  - Static avoidance obstacles
  - Dynamic avoidance obstacles
- Procedural obstacles
- User-contributed notes

2D and 3D versions of NavigationObstacles nodes are available as NavigationObstacle2D and NavigationObstacle3D respectively.

Navigation obstacles are dual purpose in that they can affect both the navigation mesh baking, and the agent avoidance.

With affect_navigation_mesh enabled the obstacle will affect navigation mesh when baked.

With avoidance_enabled the obstacle will affect avoidance agents.

Avoidance is enabled by default. If the obstacle is not used for avoidance disable enabled_avoidance to save performance.

Navigation obstacles affecting navigation mesh baking.

For navigation mesh baking, obstacles can be used to discard parts of all other source geometry inside the obstacle shape.

This can be used to stop navigation meshes being baked in unwanted places, e.g. inside "solid" geometry like thick walls or on top of other geometry that should not be included for gameplay like roofs.

Navigation obstacles discard of unwanted navigation mesh.

An obstacle does not add geometry in the baking process, it only removes geometry. It does so by nullifying all the (voxel) cells with rasterized source geometry that are within the obstacle shape. As such its effect and shape detail is limited to the cell resolution used by the baking process.

For more details on the navigation mesh baking see Using navigation meshes.

The property affect_navigation_mesh makes the obstacle contribute to the navigation mesh baking. It will be parsed or unparsed like all other node objects in a navigation mesh baking process.

The carve_navigation_mesh property makes the shape unaffected by offsets of the baking, e.g. the offset added by the navigation mesh agent_radius. It will basically act as a stencil and cut into the already offset navigation mesh surface. It will still be affected by further postprocessing of the baking process like edge simplification.

The obstacle shape and placement is defined with the height and vertices properties, and the global_position of the obstacle. The y-axis value of any Vector3 used for the vertices is ignored as the obstacle is projected on a flat horizontal plane.

When baking navigation meshes in scripts obstacles can be added procedurally as a projected obstruction. Obstacles are not involved in the source geometry parsing so adding them just before baking is enough.

For avoidance navigation obstacles can be used either as static or dynamic obstacles to affect avoidance controlled agents.

When used statically NavigationObstacles constrain avoidance controlled agents outside or inside a polygon defined area.

When used dynamically NavigationObstacles push away avoidance controlled agents in a radius around them.

An avoidance obstacle is considered static when its vertices property is populated with an outline array of positions to form a polygon.

Static obstacle drawn in the editor to block or contain navigation agents.

Static obstacles act as hard do-not-cross boundaries for avoidance using agents, e.g. similar to physics collision but for avoidance.

Static obstacles define their boundaries with an array of outline vertices (positions), and in case of 3D with an additional height property.

Static obstacles only work for agents that use the 2D avoidance mode.

Static obstacles define through winding order of the vertices if agents are pushed out or sucked in.

Static obstacles can not change their position. They can only be warped to a new position and rebuilt from scratch. Static obstacles as a result are ill-suited for usages where the position is changed every frame, as the constant rebuild has a high performance cost.

Static obstacles that are warped to another position can not be predicted by agents. This creates the risk of getting agents stuck should a static obstacle be warped on top of agents.

When the 2D avoidance is used in 3D the y-axis of Vector3 vertices is ignored. Instead, the global y-axis position of the obstacle is used as the elevation level. Agents will ignore static obstacles in 3D that are below or above them. This is automatically determined by global y-axis position of both obstacle and agent as the elevation level as well as their respective height properties.

An avoidance obstacle is considered dynamic when its radius property is greater than zero.

Dynamic obstacles act as a soft please-move-away-from-me object for avoidance using agents, e.g. similar to how they avoid other agents.

Dynamic obstacles define their boundaries with a single radius for a 2D circle, or in case of 3D avoidance a sphere shape.

Dynamic obstacles can change their position every frame without additional performance cost.

Dynamic obstacles with a set velocity can be predicted in their movement by agents.

Dynamic obstacles are not a reliable way to constrain agents in crowded or narrow spaces.

While both static and dynamic properties can be active at the same time on the same obstacle this is not recommended for performance. Ideally when an obstacle is moving the static vertices are removed and instead the radius activated. When the obstacle reaches the new final position it should gradually enlarge its radius to push all other agents away. With enough created safe space around the obstacle it should add the static vertices again and remove the radius. This helps avoid getting agents stuck in the suddenly appearing static obstacle when the rebuilt static boundary is finished.

Similar to agents the obstacles can make use of the avoidance_layers bitmask. All agents with a matching bit on their own avoidance mask will avoid the obstacle.

New obstacles can be created in a script without a Node by using the NavigationServer directly.

Obstacles created with scripts require at least a map and a position. For dynamic use a radius is required. For static use an array of vertices is required.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
var obstacle_outline = PackedVector2Array([
    Vector2(-50, -50),
    Vector2(50, -50),
    Vector2(50, 50),
    Vector2(-50, 50)
])

var navigation_mesh = NavigationPolygon.new()
var source_geometry = NavigationMeshSourceGeometryData2D.new()

NavigationServer2D.parse_source_geometry_data(navigation_mesh, source_geometry, $MyTestRootNode)

var obstacle_carve: bool = true

source_geometry.add_projected_obstruction(obstacle_outline, obstacle_carve)

NavigationServer2D.bake_from_source_geometry_data(navigation_mesh, source_geometry)
```

Example 2 (csharp):
```csharp
Vector2[] obstacleOutline
[
    new Vector2(-50, -50),
    new Vector2(50, -50),
    new Vector2(50, 50),
    new Vector2(-50, 50),
];

var navigationMesh = new NavigationPolygon();
var sourceGeometry = new NavigationMeshSourceGeometryData2D();

NavigationServer2D.ParseSourceGeometryData(navigationMesh, sourceGeometry, GetNode<Node2D>("MyTestRootNode"));

bool obstacleCarve = true;

sourceGeometry.AddProjectedObstruction(obstacleOutline, obstacleCarve);
NavigationServer2D.BakeFromSourceGeometryData(navigationMesh, sourceGeometry);
```

Example 3 (csharp):
```csharp
var obstacle_outline = PackedVector3Array([
    Vector3(-5, 0, -5),
    Vector3(5, 0, -5),
    Vector3(5, 0, 5),
    Vector3(-5, 0, 5)
])

var navigation_mesh = NavigationMesh.new()
var source_geometry = NavigationMeshSourceGeometryData3D.new()

NavigationServer3D.parse_source_geometry_data(navigation_mesh, source_geometry, $MyTestRootNode)

var obstacle_elevation: float = $MyTestObstacleNode.global_position.y
var obstacle_height: float = 50.0
var obstacle_carve: bool = true

source_geometry.add_projected_obstruction(obstacle_outline, obstacle_elevation, obstacle_height, obstacle_carve)

NavigationServer3D.bake_from_source_geometry_data(navigation_mesh, source_geometry)
```

Example 4 (csharp):
```csharp
Vector3[] obstacleOutline =
[
    new Vector3(-5, 0, -5),
    new Vector3(5, 0, -5),
    new Vector3(5, 0, 5),
    new Vector3(-5, 0, 5),
];

var navigationMesh = new NavigationMesh();
var sourceGeometry = new NavigationMeshSourceGeometryData3D();

NavigationServer3D.ParseSourceGeometryData(navigationMesh, sourceGeometry, GetNode<Node3D>("MyTestRootNode"));

float obstacleElevation = GetNode<Node3D>("MyTestObstacleNode").GlobalPosition.Y;
float obstacleHeight = 50.0f;
bool obstacleCarve = true;

sourceGeometry.AddProjectedObstruction(obstacleOutline, obstacleElevation, obstacleHeight, obstacleCarve);
NavigationServer3D.BakeFromSourceGeometryData(navigationMesh, sourceGeometry);
```

---

## Navigation debug tools — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_debug_tools.html

**Contents:**
- Navigation debug tools
- Enabling navigation debug
- Navigation debug settings
- Debug navigation mesh polygons
- Debug edge connections
- Debug performance
- User-contributed notes

The debug tools, properties and functions are only available in Godot debug builds. Do not use any of them in code that will be part of a release build.

The navigation debug visualizations are enabled by default inside the editor. To visualize navigation meshes and connections at runtime too, enable the option Visible Navigation in the editor Debug menu.

In Godot debug builds the navigation debug can also be toggled through the NavigationServer singletons from scripts.

Debug visualizations are currently based on Nodes in the SceneTree. If the NavigationServer2D or NavigationServer3D APIs are used exclusively then changes will not be reflected by the debug navigation tools.

The appearance of navigation debug can be changed in the ProjectSettings under debug/shapes/navigation. Certain debug features can also be enabled or disabled at will but may require a scene restart to take effect.

If enable_edge_lines is enabled, the edges of navigation mesh polygons will be highlighted. If enable_edge_lines_xray is also enabled, the edges of navigation meshes will be visible through geometry.

If enable_geometry_face_random_color is enabled, the color of each navigation mesh face will be mixed with a random color that is itself mixed with the color specified in geometry_face_color.

When two navigation meshes are connected within edge_connection_margin distance, the connection is overlaid. The color of the overlay is controlled by edge_connection_color. The connections can be made visible through geometry with enable_edge_connections_xray.

Edge connections are only visible when the NavigationServer is active.

To measure NavigationServer performance a dedicated monitor exists that can be found within the Editor Debugger under Debugger->Monitors->Navigation Process.

Navigation Process shows how long the NavigationServer spends updating its internals this update frame in milliseconds. Navigation Process works similar to Process for visual frame rendering and Physics Process for collision and fixed updates.

Navigation Process accounts for all updates to navigation maps, navigation regions and navigation agents as well as all the avoidance calculations for the update frame.

Navigation Process does NOT include pathfinding performance cause pathfinding operates on the navigation map data independently from the server process update.

Navigation Process should be in general kept as low and as stable as possible for runtime performance to avoid frame rate issues. Note that since the NavigationServer process update happens in the middle of the physics update an increase in Navigation Process will automatically increase Physics Process by the same amount.

Navigation also provides more detailed statistics about the current navigation related objects and navigation map composition on the NavigationServer.

Navigation statistics shown here can not be judged as good or bad for performance as it depends entirely on the project what can be considered as reasonable or horribly excessive.

Navigation statistics help with identifying performance bottlenecks that are less obvious because the source might not always have a visible representation. E.g. pathfinding performance issues created by overly detailed navigation meshes with thousand of edges / polygons or problems caused by procedural navigation gone wrong.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
NavigationServer2D.set_debug_enabled(false)
NavigationServer3D.set_debug_enabled(true)
```

Example 2 (unknown):
```unknown
NavigationServer2D.SetDebugEnabled(false);
NavigationServer3D.SetDebugEnabled(true);
```

---

## Using NavigationAgents — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html

**Contents:**
- Using NavigationAgents
- NavigationAgent Pathfinding
- NavigationAgent Pathfollowing
  - Pathfollowing common problems
- NavigationAgent Avoidance
- NavigationAgent Script Templates
- User-contributed notes

NavigationsAgents are helper nodes that combine functionality for pathfinding, path following and agent avoidance for a Node2D/3D inheriting parent node. They facilitate common calls to the NavigationServer API on behalf of the parent actor node in a more convenient manner for beginners.

2D and 3D version of NavigationAgents are available as NavigationAgent2D and NavigationAgent3D respectively.

New NavigationAgent nodes will automatically join the default navigation map on the World2D/World3D.

NavigationsAgent nodes are optional and not a hard requirement to use the navigation system. Their entire functionality can be replaced with scripts and direct calls to the NavigationServer API.

For more advanced uses consider Using NavigationPathQueryObjects over NavigationAgent nodes.

NavigationAgents query a new navigation path on their current navigation map when their target_position is set with a global position.

The result of the pathfinding can be influenced with the following properties.

The navigation_layers bitmask can be used to limit the navigation meshes that the agent can use.

The pathfinding_algorithm controls how the pathfinding travels through the navigation mesh polygons in the path search.

The path_postprocessing sets if or how the raw path corridor found by the pathfinding is altered before it is returned.

The path_metadata_flags enable the collection of additional path point meta data returned by the path.

The simplify_path and simplify_epsilon properties can be used to remove less critical points from the path.

Disabling path meta flags will disable related signal emissions on the agent.

After a target_position has been set for the agent, the next position to follow in the path can be retrieved with the get_next_path_position() function.

Once the next path position is received, move the parent actor node of the agent towards this path position with your own movement code.

The navigation system never moves the parent node of a NavigationAgent. The movement is entirely in the hands of users and their custom scripts.

NavigationAgents have their own internal logic to proceed with the current path and call for updates.

The get_next_path_position() function is responsible for updating many of the agent's internal states and properties. The function should be repeatedly called once every physics_process until is_navigation_finished() tells that the path is finished. The function should not be called after the target position or path end has been reached as it can make the agent jitter in place due to the repeated path updates. Always check very early in script with is_navigation_finished() if the path is already finished.

The following distance properties influence the path following behavior.

At path_desired_distance from the next path position, the agent advances its internal path index to the subsequent next path position.

At target_desired_distance from the target path position, the agent considers the target position to be reached and the path at its end.

At path_max_distance from the ideal path to the next path position, the agent requests a new path because it was pushed too far off.

The important updates are all triggered with the get_next_path_position() function when called in _physics_process().

NavigationAgents can be used with process but are still limited to a single update that happens in physics_process.

Script examples for various nodes commonly used with NavigationAgents can be found further below.

There are some common user problems and important caveats to consider when writing agent movement scripts.

If an agent queries a path before the navigation map synchronisation, e.g. in a _ready() function, the path might return empty. In this case the get_next_path_position() function will return the same position as the agent parent node and the agent will consider the path end reached. This is fixed by making a deferred call or using a callback e.g. waiting for the navigation map changed signal.

This is usually caused by very frequent path updates every single frame, either deliberate or by accident (e.g. max path distance set too short). The pathfinding needs to find the closest position that are valid on navigation mesh. If a new path is requested every single frame the first path positions might end up switching constantly in front and behind the agent's current position, causing it to dance between the two positions.

If an agent moves very fast it might overshoot the path_desired_distance check without ever advancing the path index. This can lead to the agent backtracking to the path point now behind it until it passes the distance check to increase the path index. Increase the desired distances accordingly for your agent speed and update rate usually fixes this as well as a more balanced navigation mesh polygon layout with not too many polygon edges cramped together in small spaces.

Same as with stuck dancing agents between two positions, this is usually caused by very frequent path updates every single frame. Depending on your navigation mesh layout, and especially when an agent is directly placed over a navigation mesh edge or edge connection, expect path positions to be sometimes slightly "behind" your actors current orientation. This happens due to precision issues and can not always be avoided. This is usually only a visible problem if actors are instantly rotated to face the current path position.

This section explains how to use the navigation avoidance specific to NavigationAgents.

In order for NavigationAgents to use the avoidance feature the avoidance_enabled property must be set to true.

The velocity_computed signal of the NavigationAgent node must be connected to receive the safe velocity calculation result.

Set the velocity of the NavigationAgent node in _physics_process() to update the agent with the current velocity of the agent's parent node.

While avoidance is enabled on the agent the safe_velocity vector will be received with the velocity_computed signal every physics frame. This velocity vector should be used to move the NavigationAgent's parent node in order to avoidance collision with other avoidance using agents or avoidance obstacles.

Only other agents on the same map that are registered for avoidance themself will be considered in the avoidance calculation.

The following NavigationAgent properties are relevant for avoidance:

The property height is available in 3D only. The height together with the current global y-axis position of the agent determines the vertical placement of the agent in the avoidance simulation. Agents using the 2D avoidance will automatically ignore other agents or obstacles that are below or above them.

The property radius controls the size of the avoidance circle, or in case of 3D sphere, around the agent. This area describes the agents body and not the avoidance maneuver distance.

The property neighbor_distance controls the search radius of the agent when searching for other agents that should be avoided. A lower value reduces processing cost.

The property max_neighbors controls how many other agents are considered in the avoidance calculation if they all have overlapping radius. A lower value reduces processing cost but a too low value may result in agents ignoring the avoidance.

The properties time_horizon_agents and time_horizon_obstacles control the avoidance prediction time for other agents or obstacles in seconds. When agents calculate their safe velocities they choose velocities that can be kept for this amount of seconds without colliding with another avoidance object. The prediction time should be kept as low as possible as agents will slow down their velocities to avoid collision in that timeframe.

The property max_speed controls the maximum velocity allowed for the agents avoidance calculation. If the agents parents moves faster than this value the avoidance safe_velocity might not be accurate enough to avoid collision.

The property use_3d_avoidance switches the agent between the 2D avoidance (xz axis) and the 3D avoidance (xyz axis) on the next update. Note that 2D avoidance and 3D avoidance run in separate avoidance simulations so agents split between them do not affect each other.

The properties avoidance_layers and avoidance_mask are bitmasks similar to e.g. physics layers. Agents will only avoid other avoidance objects that are on an avoidance layer that matches at least one of their own avoidance mask bits.

The avoidance_priority makes agents with a higher priority ignore agents with a lower priority. This can be used to give certain agents more importance in the avoidance simulation, e.g. important non-playable characters, without constantly changing their entire avoidance layers or mask.

Avoidance exists in its own space and has no information from navigation meshes or physics collision. Behind the scene avoidance agents are just circles with different radius on a flat 2D plane or spheres in an otherwise empty 3D space. NavigationObstacles can be used to add some environment constrains to the avoidance simulation, see Using NavigationObstacles.

Avoidance does not affect the pathfinding. It should be seen as an additional option for constantly moving objects that cannot be (re)baked to a navigation mesh efficiently in order to move around them.

RVO avoidance makes implicit assumptions about natural agent behavior. E.g. that agents move on reasonable passing sides that can be assigned when they encounter each other. This means that very clinical avoidance test scenarios will commonly fail. E.g. agents moved directly against each other with perfect opposite velocities will fail because the agents can not get their passing sides assigned.

Using the NavigationAgent avoidance_enabled property is the preferred option to toggle avoidance. The following code snippets can be used to toggle avoidance on agents, create or delete avoidance callbacks or switch avoidance modes.

The following sections provides script templates for nodes commonly used with NavigationAgents.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends NavigationAgent2D

func _ready() -> void:
    var agent: RID = get_rid()
    # Enable avoidance
    NavigationServer2D.agent_set_avoidance_enabled(agent, true)
    # Create avoidance callback
    NavigationServer2D.agent_set_avoidance_callback(agent, Callable(self, "_avoidance_done"))

    # Disable avoidance
    NavigationServer2D.agent_set_avoidance_enabled(agent, false)
    # Delete avoidance callback
    NavigationServer2D.agent_set_avoidance_callback(agent, Callable())
```

Example 2 (gdscript):
```gdscript
using Godot;

public partial class MyNavigationAgent2D : NavigationAgent2D
{
    public override void _Ready()
    {
        Rid agent = GetRid();
        // Enable avoidance
        NavigationServer2D.AgentSetAvoidanceEnabled(agent, true);
        // Create avoidance callback
        NavigationServer2D.AgentSetAvoidanceCallback(agent, Callable.From(AvoidanceDone));

        // Disable avoidance
        NavigationServer2D.AgentSetAvoidanceEnabled(agent, false);
        //Delete avoidance callback
        NavigationServer2D.AgentSetAvoidanceCallback(agent, default);
    }

    private void AvoidanceDone() { }
}
```

Example 3 (gdscript):
```gdscript
extends NavigationAgent3D

func _ready() -> void:
    var agent: RID = get_rid()
    # Enable avoidance
    NavigationServer3D.agent_set_avoidance_enabled(agent, true)
    # Create avoidance callback
    NavigationServer3D.agent_set_avoidance_callback(agent, Callable(self, "_avoidance_done"))
    # Switch to 3D avoidance
    NavigationServer3D.agent_set_use_3d_avoidance(agent, true)

    # Disable avoidance
    NavigationServer3D.agent_set_avoidance_enabled(agent, false)
    # Delete avoidance callback
    NavigationServer3D.agent_set_avoidance_callback(agent, Callable())
    # Switch to 2D avoidance
    NavigationServer3D.agent_set_use_3d_avoidance(agent, false)
```

Example 4 (gdscript):
```gdscript
using Godot;

public partial class MyNavigationAgent3D : NavigationAgent3D
{
    public override void _Ready()
    {
        Rid agent = GetRid();
        // Enable avoidance
        NavigationServer3D.AgentSetAvoidanceEnabled(agent, true);
        // Create avoidance callback
        NavigationServer3D.AgentSetAvoidanceCallback(agent, Callable.From(AvoidanceDone));
        // Switch to 3D avoidance
        NavigationServer3D.AgentSetUse3DAvoidance(agent, true);

        // Disable avoidance
        NavigationServer3D.AgentSetAvoidanceEnabled(agent, false);
        //Delete avoidance callback
        NavigationServer3D.AgentSetAvoidanceCallback(agent, default);
        // Switch to 2D avoidance
        NavigationServer3D.AgentSetUse3DAvoidance(agent, false);
    }

    private void AvoidanceDone() { }
}
```

---

## Using NavigationLinks — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationlinks.html

**Contents:**
- Using NavigationLinks
- Navigation link script templates
- User-contributed notes

NavigationLinks are used to connect navigation mesh polygons from NavigationRegion2D and NavigationRegion3D over arbitrary distances for pathfinding.

NavigationLinks are also used to consider movement shortcuts in pathfinding available through interacting with gameplay objects e.g. ladders, jump pads or teleports.

2D and 3D versions of NavigationJumplinks nodes are available as NavigationLink2D and NavigationLink3D respectively.

Different NavigationRegions can connect their navigation meshes without the need for a NavigationLink as long as they have overlapping edges or edges that are within navigation map edge_connection_margin. As soon as the distance becomes too large, building valid connections becomes a problem - a problem that NavigationLinks can solve.

See Using NavigationRegions to learn more about the use of navigation regions. See Connecting navigation meshes to learn more about how to connect navigation meshes.

NavigationLinks share many properties with NavigationRegions like navigation_layers. NavigationLinks add a single connection between two positions over an arbitrary distance compared to NavigationRegions that add a more local traversable area with a navigation mesh resource.

NavigationLinks have a start_position and end_position and can go in both directions when bidirectional is enabled. When placed a navigationlink connects the navigation mesh polygons closest to its start_position and end_position within search radius for pathfinding.

The polygon search radius can be configured globally in the ProjectSettings under navigation/2d_or_3d/default_link_connection_radius or set for each navigation map individually using the NavigationServer.map_set_link_connection_radius() function.

Both start_position and end_position have debug markers in the Editor. The arrows indicate which direction the link can be travelled across, and the visible radius of a position shows the polygon search radius. All navigation mesh polygons inside are compared and the closest is picked for the edge connection. If no valid polygon is found within the search radius the navigation link gets disabled.

The link debug visuals can be changed in the Editor ProjectSettings under debug/shapes/navigation. The visibility of the debug can also be controlled in the Editor 3D Viewport gizmo menu.

A navigation link does not provide any specialized movement through the link. Instead, when an agent reaches the position of a link, game code needs to react (e.g. through area triggers) and provide means for the agent to move through the link to end up at the links other position (e.g. through teleport or animation). Without that an agent will attempt to move itself along the path of the link. You could end up with an agent walking over a bottomless pit instead of waiting for a moving platform, or walking through a teleporter and proceeding through a wall.

The following script uses the NavigationServer to create a new navigation link.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node2D

var link_rid: RID
var link_start_position: Vector2
var link_end_position: Vector2

func _ready() -> void:
    link_rid = NavigationServer2D.link_create()

    var link_owner_id: int = get_instance_id()
    var link_enter_cost: float = 1.0
    var link_travel_cost: float = 1.0
    var link_navigation_layers: int = 1
    var link_bidirectional: bool = true

    NavigationServer2D.link_set_owner_id(link_rid, link_owner_id)
    NavigationServer2D.link_set_enter_cost(link_rid, link_enter_cost)
    NavigationServer2D.link_set_travel_cost(link_rid, link_travel_cost)
    NavigationServer2D.link_set_navigation_layers(link_rid, link_navigation_layers)
    NavigationServer2D.link_set_bidirectional(link_rid, link_bidirectional)

    # Enable the link and set it to the default navigation map.
    NavigationServer2D.link_set_enabled(link_rid, true)
    NavigationServer2D.link_set_map(link_rid, get_world_2d().get_navigation_map())

    # Move the 2 link positions to their intended global positions.
    NavigationServer2D.link_set_start_position(link_rid, link_start_position)
    NavigationServer2D.link_set_end_position(link_rid, link_end_position)
```

Example 2 (csharp):
```csharp
using Godot;

public partial class MyNode2D : Node2D
{
    private Rid _linkRid;
    private Vector2 _linkStartPosition;
    private Vector2 _linkEndPosition;

    public override void _Ready()
    {
        _linkRid = NavigationServer2D.LinkCreate();

        ulong linkOwnerId = GetInstanceId();
        float linkEnterCost = 1.0f;
        float linkTravelCost = 1.0f;
        uint linkNavigationLayers = 1;
        bool linkBidirectional = true;

        NavigationServer2D.LinkSetOwnerId(_linkRid, linkOwnerId);
        NavigationServer2D.LinkSetEnterCost(_linkRid, linkEnterCost);
        NavigationServer2D.LinkSetTravelCost(_linkRid, linkTravelCost);
        NavigationServer2D.LinkSetNavigationLayers(_linkRid, linkNavigationLayers);
        NavigationServer2D.LinkSetBidirectional(_linkRid, linkBidirectional);

        // Enable the link and set it to the default navigation map.
        NavigationServer2D.LinkSetEnabled(_linkRid, true);
        NavigationServer2D.LinkSetMap(_linkRid, GetWorld2D().NavigationMap);

        // Move the 2 link positions to their intended global positions.
        NavigationServer2D.LinkSetStartPosition(_linkRid, _linkStartPosition);
        NavigationServer2D.LinkSetEndPosition(_linkRid, _linkEndPosition);
    }
}
```

Example 3 (gdscript):
```gdscript
extends Node3D

var link_rid: RID
var link_start_position: Vector3
var link_end_position: Vector3

func _ready() -> void:
    link_rid = NavigationServer3D.link_create()

    var link_owner_id: int = get_instance_id()
    var link_enter_cost: float = 1.0
    var link_travel_cost: float = 1.0
    var link_navigation_layers: int = 1
    var link_bidirectional: bool = true

    NavigationServer3D.link_set_owner_id(link_rid, link_owner_id)
    NavigationServer3D.link_set_enter_cost(link_rid, link_enter_cost)
    NavigationServer3D.link_set_travel_cost(link_rid, link_travel_cost)
    NavigationServer3D.link_set_navigation_layers(link_rid, link_navigation_layers)
    NavigationServer3D.link_set_bidirectional(link_rid, link_bidirectional)

    # Enable the link and set it to the default navigation map.
    NavigationServer3D.link_set_enabled(link_rid, true)
    NavigationServer3D.link_set_map(link_rid, get_world_3d().get_navigation_map())

    # Move the 2 link positions to their intended global positions.
    NavigationServer3D.link_set_start_position(link_rid, link_start_position)
    NavigationServer3D.link_set_end_position(link_rid, link_end_position)
```

Example 4 (csharp):
```csharp
using Godot;

public partial class MyNode3D : Node3D
{
    private Rid _linkRid;
    private Vector3 _linkStartPosition;
    private Vector3 _linkEndPosition;

    public override void _Ready()
    {
        _linkRid = NavigationServer3D.LinkCreate();

        ulong linkOwnerId = GetInstanceId();
        float linkEnterCost = 1.0f;
        float linkTravelCost = 1.0f;
        uint linkNavigationLayers = 1;
        bool linkBidirectional = true;

        NavigationServer3D.LinkSetOwnerId(_linkRid, linkOwnerId);
        NavigationServer3D.LinkSetEnterCost(_linkRid, linkEnterCost);
        NavigationServer3D.LinkSetTravelCost(_linkRid, linkTravelCost);
        NavigationServer3D.LinkSetNavigationLayers(_linkRid, linkNavigationLayers);
        NavigationServer3D.LinkSetBidirectional(_linkRid, linkBidirectional);

        // Enable the link and set it to the default navigation map.
        NavigationServer3D.LinkSetEnabled(_linkRid, true);
        NavigationServer3D.LinkSetMap(_linkRid, GetWorld3D().NavigationMap);

        // Move the 2 link positions to their intended global positions.
        NavigationServer3D.LinkSetStartPosition(_linkRid, _linkStartPosition);
        NavigationServer3D.LinkSetEndPosition(_linkRid, _linkEndPosition);
    }
}
```

---

## Support different actor area access — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_different_actor_area_access.html

**Contents:**
- Support different actor area access
- User-contributed notes

A typical example for different area access in gameplay are doors that connect rooms with different navigation meshes and are not accessible by all actors all the time.

Add a NavigationRegion at the door position. Add an appropriate navigation mesh the size of the door that can connect with the surrounding navigation meshes. In order to control access, enable / disable navigation layer bits so path queries that use the same navigation layer bits can find a path through the "door" navigation mesh.

The bitmask can act as a set of door keys or abilities and only actors with at least one matching and enabled bit layer in their pathfinding query will find a path through this region. See Using NavigationLayers for more information on how to work with navigation layers and the bitmask.

The entire "door" region can also be enabled / disable if required but if disabled will block access for all path queries.

Prefer working with navigation layers in path queries whenever possible as enabling or disabling navigation layers on a region triggers a costly recalculation of the navigation map connections.

Changing navigation layers will only affect new path queries but not automatically update existing paths.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Optimizing Navigation Performance — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_optimizing_performance.html

**Contents:**
- Optimizing Navigation Performance
- Performance problems with parsing scene tree nodes
- Performance problems with navigation mesh baking
- Performance problems with NavigationAgent path queries
- Performance problems with the actual path search
- Performance problems with navigation map synchronization
- User-contributed notes

Common Navigation related performance problems can be categorized into the following topics:

Performance problems with parsing scene tree nodes for navigation mesh baking.

Performance problems with baking the actual navigation mesh.

Performance problems with NavigationAgent path queries.

Performance problems with the actual path search.

Performance problems with synchronizing the navigation map.

In the following sections information can be found on how to identify and fix or at least mitigate their impact on framerates.

Prefer using simple shapes with as few edges as possible e.g. nothing rounded like a circle, sphere or torus.

Prefer using physics collision shapes over complex visual meshes as source geometry as meshes need to be copied from the GPU and are commonly much more detailed than necessary.

In general avoid using very complex geometry as source geometry for baking navigation meshes. E.g. never use a very detailed visual mesh, as parsing its shape to data arrays and voxelizing it for the navigation mesh baking will take a long time for no real quality gain on the final navigation mesh. Instead, use a very simplified level of detail version of a shape. Even better, use very primitive shapes like boxes and rectangles that only roughly cover the same geometry but still yield a baked result good enough for pathfinding.

Prefer using simple physics collision shapes over visual meshes, as the source geometry for baking navigation meshes. Physics shapes are by default very limited and optimized shapes that are easy and quick to parse. A visual mesh on the other hand can range from simple to complex. On top, to gain access to visual mesh data the parser needs to request the mesh data arrays from the RenderingServer as visual mesh data is stored directly on the GPU and is not cached on the CPU. This requires locking the RenderingServer thread and can severely impact framerate at runtime while the rendering runs multi-threaded. If the rendering runs single-threaded, the framerate impact might be even worse and the mesh parsing might freeze the entire game for a few seconds on complex meshes.

At runtime, always prefer to use a background thread for baking navigation meshes.

Increase NavigationMesh cell_size and cell_height to create less voxels.

Change the SamplePartitionType from watershed to monotone or layers to gain baking performance.

NEVER scale source geometry with nodes to avoid precision errors. Most scale applies only visually and shapes that are very large at their base scale require still a lot of extra processing even while downscaled.

Baking navigation meshes at runtime should always be done in a background thread if possible. Even small sized navigation meshes can take far longer to bake than what is possible to squeeze into a single frame, at least if the framerate should stay at a bearable level.

Complexity of source geometry data parsed from scene tree nodes has big impact on baking performance as everything needs to be mapped to a grid / voxels. For runtime baking performance the NavigationMesh cell size and cell height should be set as high as possible without causing navigation mesh quality problems for a game. If cell size or cell height is set too low the baking is forced to create an excessive amount of voxels to process the source geometry. If the source geometry spans over a very large game world it is even possible that the baking process runs out of memory in the middle and crashes the game. The partition type can also be lowered depending on how complex the games source geometry is to gain some performance. E.g. games with mostly flat surfaces with blocky geometry can get away with the monotone or layers mode that are a lot faster to bake (e.g. because they require no distance field pass).

Never scale source geometry with nodes. Not only can it result in a lot of precision errors with wrongly matched vertices and edges but also some scaling only exists as visuals and not in the actual parsed data. E.g. if a mesh is downscaled visually in the Editor, e.g. the scale set to 0.001 on a MeshInstance, the mesh still requires a gigantic and very complex voxel grid to be processed for the baking.

Avoid unnecessary path resets and queries every frame in NavigationAgent scripts.

Avoid updating all NavigationAgent paths in the same frame.

Logical errors and wasteful operations in the custom NavigationAgent scripts are very common causes of performance issues, e.g. watch out for resetting the path every single frame. By default NavigationAgents are optimized to only query new paths when the target position changes, the navigation map changes or they are forced too far away from the desired path distance.

E.g. when AI should move to the player, the target position should not be set to the player position every single frame as this queries a new path every frame. Instead, the distance from the current target position to the player position should be compared and only when the player has moved too far away a new target position should be set.

Do not check beforehand if a target position is reachable every frame. What looks like an innocent check is the equivalent of an expensive path query behind the scene. If the plan is to request a new path anyway should the position be reachable, a path should be queried directly. By looking at the last position of the returned path and if that position is in a "reachable" distance to the checked position it answers the "is this position reachable?" question. This avoids doing the equivalent of two full path queries every frame for the same NavigationAgent.

Divide the total number of NavigationAgents into update groups or use random timers so that they do not all request new paths in the same frame.

Optimize overdetailed navigation meshes by reducing the amount of polygons and edges.

The cost of the actual path search correlates directly with the amount of navigation mesh polygons and edges and not the real size of a game world. If a giant game world uses very optimized navigation meshes with only few polygons that cover large areas, performance should be acceptable. If the game world is splintered into very small navigation meshes that each have tiny polygons (like for TileMaps) pathfinding performance will be reduced.

A common problem is a sudden performance drop when a target position is not reachable in a path query. This performance drop is "normal" and the result of a too large, too unoptimized navigation mesh with way to much polygons and edges to search through. In normal path searches where the target position can be reached quickly the pathfinding will do an early exit as soon as the position is reached which can hide this lack of optimization for a while. If the target position can not be reached the pathfinding has to do a far longer search through the available polygons to confirm that the position is absolutely not reachable.

Merge navigation meshes polygons by vertex instead of by edge connection wherever possible.

When changes are made to e.g. navigation meshes or navigation regions, the NavigationServer needs to synchronize the navigation map. Depending on the complexity of navigation meshes, this can take a significant amount of time which may impact the framerate.

The NavigationServer merges navigation meshes either by vertex or by edge connection. The merge by vertex happens when the two vertex of two different edges land in the same map grid cells. This is a rather quick and low-cost operation. The merge by edge connection happens in a second pass for all still unmerged edges. All the free edges are checked for possible edge connections by both distance and angle which is rather costly.

So apart from the general rule to have as few polygon edges as possible, as many edges as possible should be merged by vertex upfront so only a few edges are left for the more costly edge connection calculation. The debug Navigation PerformanceMonitor can be used to get statistics on how many polygons and edges are available and how many of them are unmerged or not merged by vertex. If the ratio between vertex merged and edge connections is way off (vertex should be significantly higher) the navigation meshes are properly created or placed very inefficient.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Support different actor locomotion — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_different_actor_locomotion.html

**Contents:**
- Support different actor locomotion
- User-contributed notes

To support different actor locomotion like crouching and crawling, a similar map setup as supporting Support different actor types is required.

Bake different navigation meshes with an appropriate height for crouched or crawling actors so they can find paths through those narrow sections in your game world.

When an actor changes locomotion state, e.g. stands up, starts crouching or crawling, query the appropriate map for a path.

If the avoidance behavior should also change with the locomotion e.g. only avoid while standing or only avoid other agents in the same locomotion state, switch the actor's avoidance agent to another avoidance map with each locomotion change.

While a path query can be execute immediately for multiple maps, the avoidance agent map switch will only take effect after the next server synchronization.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
func update_path():

    if actor_standing:
        path = NavigationServer3D.map_get_path(standing_navigation_map_rid, start_position, target_position, true)
    elif actor_crouching:
        path = NavigationServer3D.map_get_path(crouched_navigation_map_rid, start_position, target_position, true)
    elif actor_crawling:
        path = NavigationServer3D.map_get_path(crawling_navigation_map_rid, start_position, target_position, true)

func change_agent_avoidance_state():

    if actor_standing:
        NavigationServer3D.agent_set_map(avoidance_agent_rid, standing_navigation_map_rid)
    elif actor_crouching:
        NavigationServer3D.agent_set_map(avoidance_agent_rid, crouched_navigation_map_rid)
    elif actor_crawling:
        NavigationServer3D.agent_set_map(avoidance_agent_rid, crawling_navigation_map_rid)
```

Example 2 (json):
```json
private void UpdatePath()
{
    if (_actorStanding)
    {
        _path = NavigationServer3D.MapGetPath(_standingNavigationMapRid, _startPosition, _targetPosition, true);
    }
    else if (_actorCrouching)
    {
        _path = NavigationServer3D.MapGetPath(_crouchedNavigationMapRid, _startPosition, _targetPosition, true);
    }
    else if (_actorCrawling)
    {
        _path = NavigationServer3D.MapGetPath(_crawlingNavigationMapRid, _startPosition, _targetPosition, true);
    }
}

private void ChangeAgentAvoidanceState()
{
    if (_actorStanding)
    {
        NavigationServer3D.AgentSetMap(_avoidanceAgentRid, _standingNavigationMapRid);
    }
    else if (_actorCrouching)
    {
        NavigationServer3D.AgentSetMap(_avoidanceAgentRid, _crouchedNavigationMapRid);
    }
    else if (_actorCrawling)
    {
        NavigationServer3D.AgentSetMap(_avoidanceAgentRid, _crawlingNavigationMapRid);
    }
}
```

---

## Performance — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/index.html

**Contents:**
- Performance
- Introduction
- Common
- CPU
- GPU
- 3D
- Threads

Godot follows a balanced performance philosophy. In the performance world, there are always tradeoffs, which consist of trading speed for usability and flexibility. Some practical examples of this are:

Rendering large amounts of objects efficiently is easy, but when a large scene must be rendered, it can become inefficient. To solve this, visibility computation must be added to the rendering. This makes rendering less efficient, but at the same time, fewer objects are rendered. Therefore, the overall rendering efficiency is improved.

Configuring the properties of every material for every object that needs to be rendered is also slow. To solve this, objects are sorted by material to reduce the costs. At the same time, sorting has a cost.

In 3D physics, a similar situation happens. The best algorithms to handle large amounts of physics objects (such as SAP) are slow at insertion/removal of objects and raycasting. Algorithms that allow faster insertion and removal, as well as raycasting, will not be able to handle as many active objects.

And there are many more examples of this! Game engines strive to be general-purpose in nature. Balanced algorithms are always favored over algorithms that might be fast in some situations and slow in others, or algorithms that are fast but are more difficult to use.

Godot is not an exception to this. While it is designed to have backends swappable for different algorithms, the default backends prioritize balance and flexibility over performance.

With this clear, the aim of this tutorial section is to explain how to get the maximum performance out of Godot. While the tutorials can be read in any order, it is a good idea to start from General optimization tips.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CPU optimization — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html

**Contents:**
- CPU optimization
- Measuring performance
- CPU profilers
- External profilers
- Manually timing functions
- Caches
- Languages
  - GDScript
  - C#
  - Other languages

We have to know where the "bottlenecks" are to know how to speed up our program. Bottlenecks are the slowest parts of the program that limit the rate that everything can progress. Focusing on bottlenecks allows us to concentrate our efforts on optimizing the areas which will give us the greatest speed improvement, instead of spending a lot of time optimizing functions that will lead to small performance improvements.

For the CPU, the easiest way to identify bottlenecks is to use a profiler.

Profilers run alongside your program and take timing measurements to work out what proportion of time is spent in each function.

The Godot IDE conveniently has a built-in profiler. It does not run every time you start your project: it must be manually started and stopped. This is because, like most profilers, recording these timing measurements can slow down your project significantly.

After profiling, you can look back at the results for a frame.

Results of a profile of one of the demo projects.

We can see the cost of built-in processes such as physics and audio, as well as seeing the cost of our own scripting functions at the bottom.

Time spent waiting for various built-in servers may not be counted in the profilers. This is a known bug.

When a project is running slowly, you will often see an obvious function or process taking a lot more time than others. This is your primary bottleneck, and you can usually increase speed by optimizing this area.

For more info about using Godot's built-in profiler, see Debugger panel.

Although the Godot IDE profiler is very convenient and useful, sometimes you need more power, and the ability to profile the Godot engine source code itself.

You can use a number of third-party C++ profilers to do this.

Example results from Callgrind, which is part of Valgrind.

From the left, Callgrind is listing the percentage of time within a function and its children (Inclusive), the percentage of time spent within the function itself, excluding child functions (Self), the number of times the function is called, the function name, and the file or module.

In this example, we can see nearly all time is spent under the Main::iteration() function. This is the master function in the Godot source code that is called repeatedly. It causes frames to be drawn, physics ticks to be simulated, and nodes and scripts to be updated. A large proportion of the time is spent in the functions to render a canvas (66%), because this example uses a 2D benchmark. Below this, we see that almost 50% of the time is spent outside Godot code in libglapi and i965_dri (the graphics driver). This tells us the a large proportion of CPU time is being spent in the graphics driver.

This is actually an excellent example because, in an ideal world, only a very small proportion of time would be spent in the graphics driver. This is an indication that there is a problem with too much communication and work being done in the graphics API. This specific profiling led to the development of 2D batching, which greatly speeds up 2D rendering by reducing bottlenecks in this area.

Another handy technique, especially once you have identified the bottleneck using a profiler, is to manually time the function or area under test. The specifics vary depending on the language, but in GDScript, you would do the following:

When manually timing functions, it is usually a good idea to run the function many times (1,000 or more times), instead of just once (unless it is a very slow function). The reason for doing this is that timers often have limited accuracy. Moreover, CPUs will schedule processes in a haphazard manner. Therefore, an average over a series of runs is more accurate than a single measurement.

As you attempt to optimize functions, be sure to either repeatedly profile or time them as you go. This will give you crucial feedback as to whether the optimization is working (or not).

CPU caches are something else to be particularly aware of, especially when comparing timing results of two different versions of a function. The results can be highly dependent on whether the data is in the CPU cache or not. CPUs don't load data directly from the system RAM, even though it's huge in comparison to the CPU cache (several gigabytes instead of a few megabytes). This is because system RAM is very slow to access. Instead, CPUs load data from a smaller, faster bank of memory called cache. Loading data from cache is very fast, but every time you try and load a memory address that is not stored in cache, the cache must make a trip to main memory and slowly load in some data. This delay can result in the CPU sitting around idle for a long time, and is referred to as a "cache miss".

This means that the first time you run a function, it may run slowly because the data is not in the CPU cache. The second and later times, it may run much faster because the data is in the cache. Due to this, always use averages when timing, and be aware of the effects of cache.

Understanding caching is also crucial to CPU optimization. If you have an algorithm (routine) that loads small bits of data from randomly spread out areas of main memory, this can result in a lot of cache misses, a lot of the time, the CPU will be waiting around for data instead of doing any work. Instead, if you can make your data accesses localised, or even better, access memory in a linear fashion (like a continuous list), then the cache will work optimally and the CPU will be able to work as fast as possible.

Godot usually takes care of such low-level details for you. For example, the Server APIs make sure data is optimized for caching already for things like rendering and physics. Still, you should be especially aware of caching when writing GDExtensions.

Godot supports a number of different languages, and it is worth bearing in mind that there are trade-offs involved. Some languages are designed for ease of use at the cost of speed, and others are faster but more difficult to work with.

Built-in engine functions run at the same speed regardless of the scripting language you choose. If your project is making a lot of calculations in its own code, consider moving those calculations to a faster language.

GDScript is designed to be easy to use and iterate, and is ideal for making many types of games. However, in this language, ease of use is considered more important than performance. If you need to make heavy calculations, consider moving some of your project to one of the other languages.

C# is popular and has first-class support in Godot. It offers a good compromise between speed and ease of use. Beware of possible garbage collection pauses and leaks that can occur during gameplay, though. A common approach to workaround issues with garbage collection is to use object pooling, which is outside the scope of this guide.

Third parties provide support for several other languages, including Rust.

Godot is written in C++. Using C++ will usually result in the fastest code. However, on a practical level, it is the most difficult to deploy to end users' machines on different platforms. Options for using C++ include GDExtensions and custom modules.

Consider using threads when making a lot of calculations that can run in parallel to each other. Modern CPUs have multiple cores, each one capable of doing a limited amount of work. By spreading work over multiple threads, you can move further towards peak CPU efficiency.

The disadvantage of threads is that you have to be incredibly careful. As each CPU core operates independently, they can end up trying to access the same memory at the same time. One thread can be reading to a variable while another is writing: this is called a race condition. Before you use threads, make sure you understand the dangers and how to try and prevent these race conditions. Threads can make debugging considerably more difficult.

For more information on threads, see Using multiple threads.

Although Nodes are an incredibly powerful and versatile concept, be aware that every node has a cost. Built-in functions such as _process() and _physics_process() propagate through the tree. This housekeeping can reduce performance when you have a very large numbers of nodes (how many exactly depends on the target platform and can range from thousands to tens of thousands so ensure that you profile performance on all target platforms during development).

Each node is handled individually in the Godot renderer. Therefore, a smaller number of nodes with more in each can lead to better performance.

One quirk of the SceneTree is that you can sometimes get much better performance by removing nodes from the SceneTree, rather than by pausing or hiding them. You don't have to delete a detached node. You can for example, keep a reference to a node, detach it from the scene tree using Node.remove_child(node), then reattach it later using Node.add_child(node). This can be very useful for adding and removing areas from a game, for example.

You can avoid the SceneTree altogether by using Server APIs. For more information, see Optimization using Servers.

In some situations, physics can end up becoming a bottleneck. This is particularly the case with complex worlds and large numbers of physics objects.

Here are some techniques to speed up physics:

Try using simplified versions of your rendered geometry for collision shapes. Often, this won't be noticeable for end users, but can greatly increase performance.

Try removing objects from physics when they are out of view / outside the current area, or reusing physics objects (maybe you allow 8 monsters per area, for example, and reuse these).

Another crucial aspect to physics is the physics tick rate. In some games, you can greatly reduce the tick rate, and instead of for example, updating physics 60 times per second, you may update them only 30 or even 20 times per second. This can greatly reduce the CPU load.

The downside of changing physics tick rate is you can get jerky movement or jitter when the physics update rate does not match the frames per second rendered. Also, decreasing the physics tick rate will increase input lag. It's recommended to stick to the default physics tick rate (60 Hz) in most games that feature real-time player movement.

The solution to jitter is to use fixed timestep interpolation, which involves smoothing the rendered positions and rotations over multiple frames to match the physics. Godot has built-in physics interpolation which you can read about here. Performance-wise, interpolation is a very cheap operation compared to running a physics tick. It's orders of magnitude faster, so this can be a significant performance win while also reducing jitter.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var time_start = Time.get_ticks_usec()

# Your function you want to time
update_enemies()

var time_end = Time.get_ticks_usec()
print("update_enemies() took %d microseconds" % time_end - time_start)
```

Example 2 (gdscript):
```gdscript
var timeStart = Time.GetTicksUsec();

// Your function you want to time.
UpdateEnemies();

var timeEnd = Time.GetTicksUsec();
GD.Print($"UpdateEnemies() took {timeEnd - timeStart} microseconds");
```

---

## Optimization using Servers — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html

**Contents:**
- Optimization using Servers
- Servers
- RIDs
- Creating a sprite
- Instantiating a Mesh into 3D space
- Creating a 2D RigidBody and moving a sprite with it
- Getting data from the servers
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Engines like Godot provide increased ease of use thanks to their high-level constructs and features. Most of them are accessed and used via the Scene System. Using nodes and resources simplifies project organization and asset management in complex games.

There are, of course, always drawbacks:

There is an extra layer of complexity.

Performance is lower than when using simple APIs directly.

It is not possible to use multiple threads to control them.

More memory is needed.

In many cases, this is not really a problem (Godot is very optimized, and most operations are handled with signals, so no polling is required). Still, sometimes it can be. For example, dealing with tens of thousands of instances for something that needs to be processed every frame can be a bottleneck.

This type of situation makes programmers regret they are using a game engine and wish they could go back to a more handcrafted, low-level implementation of game code.

Still, Godot is designed to work around this problem.

You can see how using low-level servers works in action using the Bullet Shower demo project

One of the most interesting design decisions for Godot is the fact that the whole scene system is optional. While it is not currently possible to compile it out, it can be completely bypassed.

At the core, Godot uses the concept of Servers. They are very low-level APIs to control rendering, physics, sound, etc. The scene system is built on top of them and uses them directly. The most common servers are:

RenderingServer: handles everything related to graphics.

PhysicsServer3D: handles everything related to 3D physics.

PhysicsServer2D: handles everything related to 2D physics.

AudioServer: handles everything related to audio.

Explore their APIs and you will realize that all the functions provided are low-level implementations of everything Godot allows you to do.

The key to using servers is understanding Resource ID (RID) objects. These are opaque handles to the server implementation. They are allocated and freed manually. Almost every function in the servers requires RIDs to access the actual resource.

Most Godot nodes and resources contain these RIDs from the servers internally, and they can be obtained with different functions. In fact, anything that inherits Resource can be directly casted to an RID. Not all resources contain an RID, though: in such cases, the RID will be empty. The resource can then be passed to server APIs as an RID.

Resources are reference-counted (see RefCounted), and references to a resource's RID are not counted when determining whether the resource is still in use. Make sure to keep a reference to the resource outside the server, or else both it and its RID will be erased.

For nodes, there are many functions available:

For CanvasItem, the CanvasItem.get_canvas_item() method will return the canvas item RID in the server.

For CanvasLayer, the CanvasLayer.get_canvas() method will return the canvas RID in the server.

For Viewport, the Viewport.get_viewport_rid() method will return the viewport RID in the server.

For 3D, the World3D resource (obtainable in the Viewport and Node3D nodes) contains functions to get the RenderingServer Scenario, and the PhysicsServer Space. This allows creating 3D objects directly with the server API and using them.

For 2D, the World2D resource (obtainable in the Viewport and CanvasItem nodes) contains functions to get the RenderingServer Canvas, and the Physics2DServer Space. This allows creating 2D objects directly with the server API and using them.

The VisualInstance3D class, allows getting the scenario instance and instance base via the VisualInstance3D.get_instance() and VisualInstance3D.get_base() respectively.

Try exploring the nodes and resources you are familiar with and find the functions to obtain the server RIDs.

It is not advised to control RIDs from objects that already have a node associated. Instead, server functions should always be used for creating and controlling new ones and interacting with the existing ones.

This is an example of how to create a sprite from code and move it using the low-level CanvasItem API.

The Canvas Item API in the server allows you to add draw primitives to it. Once added, they can't be modified. The Item needs to be cleared and the primitives re-added (this is not the case for setting the transform, which can be done as many times as desired).

Primitives are cleared this way:

The 3D APIs are different from the 2D ones, so the instantiation API must be used.

This creates a RigidBody2D using the PhysicsServer2D API, and moves a CanvasItem when the body moves.

The 3D version should be very similar, as 2D and 3D physics servers are identical (using RigidBody3D and PhysicsServer3D respectively).

Try to never request any information from RenderingServer, PhysicsServer2D or PhysicsServer3D by calling functions unless you know what you are doing. These servers will often run asynchronously for performance and calling any function that returns a value will stall them and force them to process anything pending until the function is actually called. This will severely decrease performance if you call them every frame (and it won't be obvious why).

Because of this, most APIs in such servers are designed so it's not even possible to request information back, until it's actual data that can be saved.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node2D


# RenderingServer expects references to be kept around.
var texture


func _ready():
    # Create a canvas item, child of this node.
    var ci_rid = RenderingServer.canvas_item_create()
    # Make this node the parent.
    RenderingServer.canvas_item_set_parent(ci_rid, get_canvas_item())
    # Draw a texture on it.
    # Remember, keep this reference.
    texture = load("res://my_texture.png")
    # Add it, centered.
    RenderingServer.canvas_item_add_texture_rect(ci_rid, Rect2(-texture.get_size() / 2, texture.get_size()), texture)
    # Add the item, rotated 45 degrees and translated.
    var xform = Transform2D().rotated(deg_to_rad(45)).translated(Vector2(20, 30))
    RenderingServer.canvas_item_set_transform(ci_rid, xform)
```

Example 2 (csharp):
```csharp
public partial class MyNode2D : Node2D
{
    // RenderingServer expects references to be kept around.
    private Texture2D _texture;

    public override void _Ready()
    {
        // Create a canvas item, child of this node.
        Rid ciRid = RenderingServer.CanvasItemCreate();
        // Make this node the parent.
        RenderingServer.CanvasItemSetParent(ciRid, GetCanvasItem());
        // Draw a texture on it.
        // Remember, keep this reference.
        _texture = ResourceLoader.Load<Texture2D>("res://MyTexture.png");
        // Add it, centered.
        RenderingServer.CanvasItemAddTextureRect(ciRid, new Rect2(-_texture.GetSize() / 2, _texture.GetSize()), _texture.GetRid());
        // Add the item, rotated 45 degrees and translated.
        Transform2D xform = Transform2D.Identity.Rotated(Mathf.DegToRad(45)).Translated(new Vector2(20, 30));
        RenderingServer.CanvasItemSetTransform(ciRid, xform);
    }
}
```

Example 3 (unknown):
```unknown
RenderingServer.canvas_item_clear(ci_rid)
```

Example 4 (unknown):
```unknown
RenderingServer.CanvasItemClear(ciRid);
```

---

## General optimization tips — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html

**Contents:**
- General optimization tips
- Introduction
  - Smoke and mirrors
  - The nature of slowness
- Measuring performance
  - Limitations
- Detective work
  - Hypothesis testing
  - Binary search
- Profilers

In an ideal world, computers would run at infinite speed. The only limit to what we could achieve would be our imagination. However, in the real world, it's all too easy to produce software that will bring even the fastest computer to its knees.

Thus, designing games and other software is a compromise between what we would like to be possible, and what we can realistically achieve while maintaining good performance.

To achieve the best results, we have two approaches:

And preferably, we will use a blend of the two.

Part of working smarter is recognizing that, in games, we can often get the player to believe they're in a world that is far more complex, interactive, and graphically exciting than it really is. A good programmer is a magician, and should strive to learn the tricks of the trade while trying to invent new ones.

To the outside observer, performance problems are often lumped together. But in reality, there are several different kinds of performance problems:

A slow process that occurs every frame, leading to a continuously low frame rate.

An intermittent process that causes "spikes" of slowness, leading to stalls.

A slow process that occurs outside of normal gameplay, for instance, when loading a level.

Each of these are annoying to the user, but in different ways.

Probably the most important tool for optimization is the ability to measure performance - to identify where bottlenecks are, and to measure the success of our attempts to speed them up.

There are several methods of measuring performance, including:

Putting a start/stop timer around code of interest.

Using the Godot profiler.

Using external CPU profilers.

Using external GPU profilers/debuggers such as NVIDIA Nsight Graphics, Radeon GPU Profiler, PIX (Direct3D 12 only), Xcode (Metal only), or Arm Performance Studio.

Checking the frame rate (with V-Sync disabled). Third-party utilities such as RivaTuner Statistics Server (Windows), Special K (Windows), or MangoHud (Linux) can also be useful here.

Using an unofficial debug menu add-on.

Be very aware that the relative performance of different areas can vary on different hardware. It's often a good idea to measure timings on more than one device. This is especially the case if you're targeting mobile devices.

CPU profilers are often the go-to method for measuring performance. However, they don't always tell the whole story.

Bottlenecks are often on the GPU, "as a result" of instructions given by the CPU.

Spikes can occur in the operating system processes (outside of Godot) "as a result" of instructions used in Godot (for example, dynamic memory allocation).

You may not always be able to profile specific devices like a mobile phone due to the initial setup required.

You may have to solve performance problems that occur on hardware you don't have access to.

As a result of these limitations, you often need to use detective work to find out where bottlenecks are.

Detective work is a crucial skill for developers (both in terms of performance, and also in terms of bug fixing). This can include hypothesis testing, and binary search.

Say, for example, that you believe sprites are slowing down your game. You can test this hypothesis by:

Measuring the performance when you add more sprites, or take some away.

This may lead to a further hypothesis: does the size of the sprite determine the performance drop?

You can test this by keeping everything the same, but changing the sprite size, and measuring performance.

If you know that frames are taking much longer than they should, but you're not sure where the bottleneck lies. You could begin by commenting out approximately half the routines that occur on a normal frame. Has the performance improved more or less than expected?

Once you know which of the two halves contains the bottleneck, you can repeat this process until you've pinned down the problematic area.

Profilers allow you to time your program while running it. Profilers then provide results telling you what percentage of time was spent in different functions and areas, and how often functions were called.

This can be very useful both to identify bottlenecks and to measure the results of your improvements. Sometimes, attempts to improve performance can backfire and lead to slower performance. Always use profiling and timing to guide your efforts.

For more info about using Godot's built-in profiler, see The Profiler.

Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%.

The messages are very important:

Developer time is limited. Instead of blindly trying to speed up all aspects of a program, we should concentrate our efforts on the aspects that really matter.

Efforts at optimization often end up with code that is harder to read and debug than non-optimized code. It is in our interests to limit this to areas that will really benefit.

Just because we can optimize a particular bit of code, it doesn't necessarily mean that we should. Knowing when and when not to optimize is a great skill to develop.

One misleading aspect of the quote is that people tend to focus on the subquote "premature optimization is the root of all evil". While premature optimization is (by definition) undesirable, performant software is the result of performant design.

The danger with encouraging people to ignore optimization until necessary, is that it conveniently ignores that the most important time to consider performance is at the design stage, before a key has even hit a keyboard. If the design or algorithms of a program are inefficient, then no amount of polishing the details later will make it run fast. It may run faster, but it will never run as fast as a program designed for performance.

This tends to be far more important in game or graphics programming than in general programming. A performant design, even without low-level optimization, will often run many times faster than a mediocre design with low-level optimization.

Of course, in practice, unless you have prior knowledge, you are unlikely to come up with the best design the first time. Instead, you'll often make a series of versions of a particular area of code, each taking a different approach to the problem, until you come to a satisfactory solution. It's important not to spend too much time on the details at this stage until you have finalized the overall design. Otherwise, much of your work will be thrown out.

It's difficult to give general guidelines for performant design because this is so dependent on the problem. One point worth mentioning though, on the CPU side, is that modern CPUs are nearly always limited by memory bandwidth. This has led to a resurgence in data-oriented design, which involves designing data structures and algorithms for cache locality of data and linear access, rather than jumping around in memory.

Assuming we have a reasonable design, and taking our lessons from Knuth, our first step in optimization should be to identify the biggest bottlenecks - the slowest functions, the low-hanging fruit.

Once we've successfully improved the speed of the slowest area, it may no longer be the bottleneck. So we should test/profile again and find the next bottleneck on which to focus.

Profile / Identify bottleneck.

Some profilers will even tell you which part of a function (which data accesses, calculations) are slowing things down.

As with design, you should concentrate your efforts first on making sure the algorithms and data structures are the best they can be. Data access should be local (to make best use of CPU cache), and it can often be better to use compact storage of data (again, always profile to test results). Often, you precalculate heavy computations ahead of time. This can be done by performing the computation when loading a level, by loading a file containing precalculated data, or by storing the results of complex calculations into a script constant and reading its value.

Once algorithms and data are good, you can often make small changes in routines which improve performance. For instance, you can move some calculations outside of loops or transform nested for loops into non-nested loops. (This should be feasible if you know a 2D array's width or height in advance.)

Always retest your timing/bottlenecks after making each change. Some changes will increase speed, others may have a negative effect. Sometimes, a small positive effect will be outweighed by the negatives of more complex code, and you may choose to leave out that optimization.

The proverb "a chain is only as strong as its weakest link" applies directly to performance optimization. If your project is spending 90% of the time in function A, then optimizing A can have a massive effect on performance.

In this example, improving this bottleneck A by a factor of 9× decreases overall frame time by 5× while increasing frames per second by 5×.

However, if something else is running slowly and also bottlenecking your project, then the same improvement can lead to less dramatic gains:

In this example, even though we have hugely optimized function A, the actual gain in terms of frame rate is quite small.

In games, things become even more complicated because the CPU and GPU run independently of one another. Your total frame time is determined by the slower of the two.

In this example, we optimized the CPU hugely again, but the frame time didn't improve because we are GPU-bottlenecked.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (yaml):
```yaml
A: 9 ms
Everything else: 1 ms
Total frame time: 10 ms
```

Example 2 (yaml):
```yaml
A: 1 ms
Everything else: 1ms
Total frame time: 2 ms
```

Example 3 (yaml):
```yaml
A: 9 ms
Everything else: 50 ms
Total frame time: 59 ms
```

Example 4 (yaml):
```yaml
A: 1 ms
Everything else: 50 ms
Total frame time: 51 ms
```

---

## Using multiple threads — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/using_multiple_threads.html

**Contents:**
- Using multiple threads
- Threads
- Creating a Thread
- Mutexes
- Semaphores
- User-contributed notes

Threads allow simultaneous execution of code. It allows off-loading work from the main thread.

Godot supports threads and provides many handy functions to use them.

If using other languages (C#, C++), it may be easier to use the threading classes they support.

Before using a built-in class in a thread, read Thread-safe APIs first to check whether it can be safely used in a thread.

To create a thread, use the following code:

Your function will, then, run in a separate thread until it returns. Even if the function has returned already, the thread must collect it, so call Thread.wait_to_finish(), which will wait until the thread is done (if not done yet), then properly dispose of it.

Creating threads is a slow operation, especially on Windows. To avoid unnecessary performance overhead, make sure to create threads before heavy processing is needed instead of creating threads just-in-time.

For example, if you need multiple threads during gameplay, you can create threads while the level is loading and only actually start processing with them later on.

Additionally, locking and unlocking of mutexes can also be an expensive operation. Locking should be done carefully; avoid locking too often (or for too long).

Accessing objects or data from multiple threads is not always supported (if you do it, it will cause unexpected behaviors or crashes). Read the Thread-safe APIs documentation to understand which engine APIs support multiple thread access.

When processing your own data or calling your own functions, as a rule, try to avoid accessing the same data directly from different threads. You may run into synchronization problems, as the data is not always updated between CPU cores when modified. Always use a Mutex when accessing a piece of data from different threads.

When calling Mutex.lock(), a thread ensures that all other threads will be blocked (put on suspended state) if they try to lock the same mutex. When the mutex is unlocked by calling Mutex.unlock(), the other threads will be allowed to proceed with the lock (but only one at a time).

Here is an example of using a Mutex:

Sometimes you want your thread to work "on demand". In other words, tell it when to work and let it suspend when it isn't doing anything. For this, Semaphores are used. The function Semaphore.wait() is used in the thread to suspend it until some data arrives.

The main thread, instead, uses Semaphore.post() to signal that data is ready to be processed:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var thread: Thread

# The thread will start here.
func _ready():
    thread = Thread.new()
    # You can bind multiple arguments to a function Callable.
    thread.start(_thread_function.bind("Wafflecopter"))


# Run here and exit.
# The argument is the bound data passed from start().
func _thread_function(userdata):
    # Print the userdata ("Wafflecopter")
    print("I'm a thread! Userdata is: ", userdata)


# Thread must be disposed (or "joined"), for portability.
func _exit_tree():
    thread.wait_to_finish()
```

Example 2 (cpp):
```cpp
#pragma once

#include <godot_cpp/classes/node.hpp>
#include <godot_cpp/classes/thread.hpp>

namespace godot {
    class MultithreadingDemo : public Node {
        GDCLASS(MultithreadingDemo, Node);

    private:
        Ref<Thread> worker;

    protected:
        static void _bind_methods();
        void _notification(int p_what);

    public:
        MultithreadingDemo();
        ~MultithreadingDemo();

        void demo_threaded_function();
    };
} // namespace godot
```

Example 3 (cpp):
```cpp
#include "multithreading_demo.h"

#include <godot_cpp/classes/engine.hpp>
#include <godot_cpp/classes/os.hpp>
#include <godot_cpp/classes/time.hpp>
#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/variant/utility_functions.hpp>

using namespace godot;

void MultithreadingDemo::_bind_methods() {
    ClassDB::bind_method(D_METHOD("threaded_function"), &MultithreadingDemo::demo_threaded_function);
}

void MultithreadingDemo::_notification(int p_what) {
    // Prevents this from running in the editor, only during game mode. In Godot 4.3+ use Runtime classes.
    if (Engine::get_singleton()->is_editor_hint()) {
        return;
    }

    switch (p_what) {
        case NOTIFICATION_READY: {
            worker.instantiate();
            worker->start(callable_mp(this, &MultithreadingDemo::demo_threaded_function), Thread::PRIORITY_NORMAL);
        } break;
        case NOTIFICATION_EXIT_TREE: { // Thread must be disposed (or "joined"), for portability.
            // Wait until it exits.
            if (worker.is_valid()) {
                worker->wait_to_finish();
            }

            worker.unref();
        } break;
    }
}

MultithreadingDemo::MultithreadingDemo() {
    // Initialize any variables here.
}

MultithreadingDemo::~MultithreadingDemo() {
    // Add your cleanup here.
}

void MultithreadingDemo::demo_threaded_function() {
    UtilityFunctions::print("demo_threaded_function started!");
    int i = 0;
    uint64_t start = Time::get_singleton()->get_ticks_msec();
    while (Time::get_singleton()->get_ticks_msec() - start < 5000) {
        OS::get_singleton()->delay_msec(10);
        i++;
    }

    UtilityFunctions::print("demo_threaded_function counted to: ", i, ".");
}
```

Example 4 (gdscript):
```gdscript
var counter := 0
var mutex: Mutex
var thread: Thread


# The thread will start here.
func _ready():
    mutex = Mutex.new()
    thread = Thread.new()
    thread.start(_thread_function)

    # Increase value, protect it with Mutex.
    mutex.lock()
    counter += 1
    mutex.unlock()


# Increment the value from the thread, too.
func _thread_function():
    mutex.lock()
    counter += 1
    mutex.unlock()


# Thread must be disposed (or "joined"), for portability.
func _exit_tree():
    thread.wait_to_finish()
    print("Counter is: ", counter) # Should be 2.
```

---

## GPU optimization — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html

**Contents:**
- GPU optimization
- Introduction
- Draw calls, state changes, and APIs
  - 2D batching
  - 3D batching
  - Reuse shaders and materials
- Pixel cost versus vertex cost
- Pixel/fragment shaders and fill rate
  - Reading textures
  - Texture compression

The demand for new graphics features and progress almost guarantees that you will encounter graphics bottlenecks. Some of these can be on the CPU side, for instance in calculations inside the Godot engine to prepare objects for rendering. Bottlenecks can also occur on the CPU in the graphics driver, which sorts instructions to pass to the GPU, and in the transfer of these instructions. And finally, bottlenecks also occur on the GPU itself.

Where bottlenecks occur in rendering is highly hardware-specific. Mobile GPUs in particular may struggle with scenes that run easily on desktop.

Understanding and investigating GPU bottlenecks is slightly different to the situation on the CPU. This is because, often, you can only change performance indirectly by changing the instructions you give to the GPU. Also, it may be more difficult to take measurements. In many cases, the only way of measuring performance is by examining changes in the time spent rendering each frame.

The following section is not relevant to end-users, but is useful to provide background information that is relevant in later sections.

Godot sends instructions to the GPU via a graphics API (Vulkan, OpenGL, OpenGL ES or WebGL). The communication and driver activity involved can be quite costly, especially in OpenGL, OpenGL ES and WebGL. If we can provide these instructions in a way that is preferred by the driver and GPU, we can greatly increase performance.

Nearly every API command in OpenGL requires a certain amount of validation to make sure the GPU is in the correct state. Even seemingly simple commands can lead to a flurry of behind-the-scenes housekeeping. Therefore, the goal is to reduce these instructions to a bare minimum and group together similar objects as much as possible so they can be rendered together, or with the minimum number of these expensive state changes.

In 2D, the costs of treating each item individually can be prohibitively high - there can easily be thousands of them on the screen. This is why 2D batching is used. Multiple similar items are grouped together and rendered in a batch, via a single draw call, rather than making a separate draw call for each item. In addition, this means state changes, material and texture changes can be kept to a minimum.

In 3D, we still aim to minimize draw calls and state changes. However, it can be more difficult to batch together several objects into a single draw call. 3D meshes tend to comprise hundreds or thousands of triangles, and combining large meshes in real-time is prohibitively expensive. The costs of joining them quickly exceeds any benefits as the number of triangles grows per mesh. A much better alternative is to join meshes ahead of time (static meshes in relation to each other). This can be done by artists, or programmatically within Godot using an add-on.

There is also a cost to batching together objects in 3D. Several objects rendered as one cannot be individually culled. An entire city that is off-screen will still be rendered if it is joined to a single blade of grass that is on screen. Thus, you should always take objects' locations and culling into account when attempting to batch 3D objects together. Despite this, the benefits of joining static objects often outweigh other considerations, especially for large numbers of distant or low-poly objects.

For more information on 3D specific optimizations, see Optimizing 3D performance.

The Godot renderer is a little different to what is out there. It's designed to minimize GPU state changes as much as possible. StandardMaterial3D does a good job at reusing materials that need similar shaders. If custom shaders are used, make sure to reuse them as much as possible. Godot's priorities are:

Reusing Materials: The fewer different materials in the scene, the faster the rendering will be. If a scene has a huge amount of objects (in the hundreds or thousands), try reusing the materials. In the worst case, use atlases to decrease the amount of texture changes.

Reusing Shaders: If materials can't be reused, at least try to reuse shaders. Note: shaders are automatically reused between StandardMaterial3Ds that share the same configuration (features that are enabled or disabled with a check box) even if they have different parameters.

If a scene has, for example, 20,000 objects with 20,000 different materials each, rendering will be slow. If the same scene has 20,000 objects, but only uses 100 materials, rendering will be much faster.

You may have heard that the lower the number of polygons in a model, the faster it will be rendered. This is really relative and depends on many factors.

On a modern PC and console, vertex cost is low. GPUs originally only rendered triangles. This meant that every frame:

All vertices had to be transformed by the CPU (including clipping).

All vertices had to be sent to the GPU memory from the main RAM.

Nowadays, all this is handled inside the GPU, greatly increasing performance. 3D artists usually have the wrong feeling about polycount performance because 3D modeling software (such as Blender, 3ds Max, etc.) need to keep geometry in CPU memory for it to be edited, reducing actual performance. Game engines rely on the GPU more, so they can render many triangles much more efficiently.

On mobile devices, the story is different. PC and console GPUs are brute-force monsters that can pull as much electricity as they need from the power grid. Mobile GPUs are limited to a tiny battery, so they need to be a lot more power efficient.

To be more efficient, mobile GPUs attempt to avoid overdraw. Overdraw occurs when the same pixel on the screen is being rendered more than once. Imagine a town with several buildings. GPUs don't know what is visible and what is hidden until they draw it. For example, a house might be drawn and then another house in front of it (which means rendering happened twice for the same pixel). PC GPUs normally don't care much about this and just throw more pixel processors to the hardware to increase performance (which also increases power consumption).

Using more power is not an option on mobile so mobile devices use a technique called tile-based rendering which divides the screen into a grid. Each cell keeps the list of triangles drawn to it and sorts them by depth to minimize overdraw. This technique improves performance and reduces power consumption, but takes a toll on vertex performance. As a result, fewer vertices and triangles can be processed for drawing.

Additionally, tile-based rendering struggles when there are small objects with a lot of geometry within a small portion of the screen. This forces mobile GPUs to put a lot of strain on a single screen tile, which considerably decreases performance as all the other cells must wait for it to complete before displaying the frame.

To summarize, don't worry about vertex count on mobile, but avoid concentration of vertices in small parts of the screen. If a character, NPC, vehicle, etc. is far away (which means it looks tiny), use a smaller level of detail (LOD) model. Even on desktop GPUs, it's preferable to avoid having triangles smaller than the size of a pixel on screen.

Pay attention to the additional vertex processing required when using:

Skinning (skeletal animation)

Vertex-lit objects (common on mobile)

In contrast to vertex processing, the costs of fragment (per-pixel) shading have increased dramatically over the years. Screen resolutions have increased: the area of a 4K screen is 8,294,400 pixels, versus 307,200 for an old 640×480 VGA screen. That is 27 times the area! Also, the complexity of fragment shaders has exploded. Physically-based rendering requires complex calculations for each fragment.

You can test whether a project is fill rate-limited quite easily. Turn off V-Sync to prevent capping the frames per second, then compare the frames per second when running with a large window, to running with a very small window. You may also benefit from similarly reducing your shadow map size if using shadows. Usually, you will find the FPS increases quite a bit using a small window, which indicates you are to some extent fill rate-limited. On the other hand, if there is little to no increase in FPS, then your bottleneck lies elsewhere.

You can increase performance in a fill rate-limited project by reducing the amount of work the GPU has to do. You can do this by simplifying the shader (perhaps turn off expensive options if you are using a StandardMaterial3D), or reducing the number and size of textures used. Also, when using non-unshaded particles, consider forcing vertex shading in their material to decrease the shading cost.

On supported hardware, Variable rate shading can be used to reduce shading processing costs without impacting the sharpness of edges on the final image.

When targeting mobile devices, consider using the simplest possible shaders you can reasonably afford to use.

The other factor in fragment shaders is the cost of reading textures. Reading textures is an expensive operation, especially when reading from several textures in a single fragment shader. Also, consider that filtering may slow it down further (trilinear filtering between mipmaps, and averaging). Reading textures is also expensive in terms of power usage, which is a big issue on mobiles.

If you use third-party shaders or write your own shaders, try to use algorithms that require as few texture reads as possible.

By default, Godot compresses textures of 3D models when imported using video RAM (VRAM) compression. Video RAM compression isn't as efficient in size as PNG or JPG when stored, but increases performance enormously when drawing large enough textures.

This is because the main goal of texture compression is bandwidth reduction between memory and the GPU.

In 3D, the shapes of objects depend more on the geometry than the texture, so compression is generally not noticeable. In 2D, compression depends more on shapes inside the textures, so the artifacts resulting from 2D compression are more noticeable.

As a warning, most Android devices do not support texture compression of textures with transparency (only opaque), so keep this in mind.

Even in 3D, "pixel art" textures should have VRAM compression disabled as it will negatively affect their appearance, without improving performance significantly due to their low resolution.

Post-processing effects and shadows can also be expensive in terms of fragment shading activity. Always test the impact of these on different hardware.

Reducing the size of shadowmaps can increase performance, both in terms of writing and reading the shadowmaps. On top of that, the best way to improve performance of shadows is to turn shadows off for as many lights and objects as possible. Smaller or distant OmniLights/SpotLights can often have their shadows disabled with only a small visual impact.

Transparent objects present particular problems for rendering efficiency. Opaque objects (especially in 3D) can be essentially rendered in any order and the Z-buffer will ensure that only the front most objects get shaded. Transparent or blended objects are different. In most cases, they cannot rely on the Z-buffer and must be rendered in "painter's order" (i.e. from back to front) to look correct.

Transparent objects are also particularly bad for fill rate, because every item has to be drawn even if other transparent objects will be drawn on top later on.

Opaque objects don't have to do this. They can usually take advantage of the Z-buffer by writing to the Z-buffer only first, then only performing the fragment shader on the "winning" fragment, the object that is at the front at a particular pixel.

Transparency is particularly expensive where multiple transparent objects overlap. It is usually better to use transparent areas as small as possible to minimize these fill rate requirements, especially on mobile, where fill rate is very expensive. Indeed, in many situations, rendering more complex opaque geometry can end up being faster than using transparency to "cheat".

If you are aiming to release on multiple platforms, test early and test often on all your platforms, especially mobile. Developing a game on desktop but attempting to port it to mobile at the last minute is a recipe for disaster.

In general, you should design your game for the lowest common denominator, then add optional enhancements for more powerful platforms. For example, you may want to use the Compatibility rendering method for both desktop and mobile platforms where you target both.

As described above, GPUs on mobile devices work in dramatically different ways from GPUs on desktop. Most mobile devices use tile renderers. Tile renderers split up the screen into regular-sized tiles that fit into super fast cache memory, which reduces the number of read/write operations to the main memory.

There are some downsides though. Tiled rendering can make certain techniques much more complicated and expensive to perform. Tiles that rely on the results of rendering in different tiles or on the results of earlier operations being preserved can be very slow. Be very careful to test the performance of shaders, viewport textures and post processing.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Thread-safe APIs — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html

**Contents:**
- Thread-safe APIs
- Threads
- Global scope
- Scene tree
- Rendering
- GDScript arrays, dictionaries
- Resources
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Threads are used to balance processing power across CPUs and cores. Godot supports multithreading, but not in the whole engine.

Below is a list of ways multithreading can be used in different areas of Godot.

Global Scope singletons are all thread-safe. Accessing servers from threads is supported (for RenderingServer and Physics servers, ensure threaded or thread-safe operation is enabled in the project settings!).

This makes them ideal for code that creates dozens of thousands of instances in servers and controls them from threads. Of course, it requires a bit more code, as this is used directly and not within the scene tree.

Interacting with the active scene tree is NOT thread-safe. Make sure to use mutexes when sending data between threads. If you want to call functions from a thread, the call_deferred function may be used:

However, creating scene chunks (nodes in tree arrangement) outside the active tree is fine. This way, parts of a scene can be built or instantiated in a thread, then added in the main thread:

Still, this is only really useful if you have one thread loading data. Attempting to load or create scene chunks from multiple threads may work, but you risk resources (which are only loaded once in Godot) tweaked by the multiple threads, resulting in unexpected behaviors or crashes.

Only use more than one thread to generate scene data if you really know what you are doing and you are sure that a single resource is not being used or set in multiple ones. Otherwise, you are safer just using the servers API (which is fully thread-safe) directly and not touching scene or resources.

Instancing nodes that render anything in 2D or 3D (such as Sprite) is not thread-safe by default. To make rendering thread-safe, set the Rendering > Driver > Thread Model project setting to Multi-Threaded.

Note that the Multi-Threaded thread model has several known bugs, so it may not be usable in all scenarios.

You should avoid calling functions involving direct interaction with the GPU on other threads, such as creating new textures or modifying and retrieving image data, these operations can lead to performance stalls because they require synchronization with the RenderingServer, as data needs to be transmitted to or updated on the GPU.

In GDScript, reading and writing elements from multiple threads is OK, but anything that changes the container size (resizing, adding or removing elements) requires locking a mutex.

Modifying a unique resource from multiple threads is not supported. However handling references on multiple threads is supported, hence loading resources on a thread is as well - scenes, textures, meshes, etc - can be loaded and manipulated on a thread and then added to the active scene on the main thread. The limitation here is as described above, one must be careful not to load the same resource from multiple threads at once, therefore it is easiest to use one thread for loading and modifying resources, and then the main thread for adding them.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# Unsafe:
node.add_child(child_node)
# Safe:
node.add_child.call_deferred(child_node)
```

Example 2 (unknown):
```unknown
// Unsafe:
node.AddChild(childNode);
// Safe:
node.CallDeferred(Node.MethodName.AddChild, childNode);
```

Example 3 (gdscript):
```gdscript
var enemy_scene = load("res://enemy_scene.scn")
var enemy = enemy_scene.instantiate()
enemy.add_child(weapon) # Set a weapon.
world.add_child.call_deferred(enemy)
```

Example 4 (typescript):
```typescript
PackedScene enemyScene = GD.Load<PackedScene>("res://EnemyScene.scn");
Node enemy = enemyScene.Instantiate<Node>();
enemy.AddChild(weapon);
world.CallDeferred(Node.MethodName.AddChild, enemy);
```

---

## Editor plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/editor/index.html

**Contents:**
- Editor plugins

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/index.html

**Contents:**
- Plugins

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Installing plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/editor/installing_plugins.html

**Contents:**
- Installing plugins
- Finding plugins
- Installing a plugin
- Enabling a plugin
- User-contributed notes

Godot features an editor plugin system with numerous plugins developed by the community. Plugins can extend the editor's functionality with new nodes, additional docks, convenience features, and more.

The preferred way to find Godot plugins is to use the Asset Library. While it can be browsed online, it's more convenient to use it directly from the editor. To do so, click the AssetLib tab at the top of the editor:

You can also find assets on code hosting websites such as GitHub.

Some repositories describe themselves as "plugins" but may not actually be editor plugins. This is especially the case for scripts that are intended to be used in a running project. You don't need to enable such plugins to use them. Download them and extract the files in your project folder.

One way to distinguish editor plugins from non-editor plugins is to look for a plugin.cfg file in the repository that hosts the plugin. If the repository contains a plugin.cfg file in a folder placed in the addons/ folder, then it is an editor plugin.

To install a plugin, download it as a ZIP archive. On the Asset Library, this can be done using the Download button, either from the editor or using the Web interface.

On GitHub, if a plugin has tags (versions) declared, go to the Releases tab to download a stable release. This ensures you download a version that was declared to be stable by its author.

On GitHub, if the plugin doesn't have any tags declared, use the Download ZIP button to download a ZIP of the latest revision:

Extract the ZIP archive and move the addons/ folder it contains into your project folder. If your project already contains an addons/ folder, move the plugin's addons/ folder into your project folder to merge the new folder contents with the existing one. Your file manager may ask you whether to write into the folder; answer Yes. No files will be overwritten in the process.

To enable the freshly installed plugin, open Project > Project Settings at the top of the editor then go the Plugins tab. If the plugin was packaged correctly, you should see it in the list of plugins. Click on the Enable checkbox to enable the plugin.

You can use the plugin immediately after enabling it; there's no need to restart the editor. Likewise, disabling a plugin can be done without having to restart the editor.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Import plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/editor/import_plugins.html

**Contents:**
- Import plugins
- Introduction
- Configuration
- The EditorImportPlugin class
- Options and presets
- The import method
- Platform variants and generated files
- Trying the plugin
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

This tutorial assumes you already know how to make generic plugins. If in doubt, refer to the Making plugins page. This also assumes you are acquainted with Godot's import system.

An import plugin is a special type of editor tool that allows custom resources to be imported by Godot and be treated as first-class resources. The editor itself comes bundled with a lot of import plugins to handle the common resources like PNG images, Collada and glTF models, Ogg Vorbis sounds, and many more.

This tutorial shows how to create an import plugin to load a custom text file as a material resource. This text file will contain three numeric values separated by comma, which represents the three channels of a color, and the resulting color will be used as the albedo (main color) of the imported material. In this example it contains the pure blue color (zero red, zero green, and full blue):

First we need a generic plugin that will handle the initialization and destruction of our import plugin. Let's add the plugin.cfg file first:

Then we need the material_import.gd file to add and remove the import plugin when needed:

When this plugin is activated, it will create a new instance of the import plugin (which we'll soon make) and add it to the editor using the add_import_plugin() method. We store a reference to it in a class member import_plugin so we can refer to it later when removing it. The remove_import_plugin() method is called when the plugin is deactivated to clean up the memory and let the editor know the import plugin isn't available anymore.

Note that the import plugin is a reference type, so it doesn't need to be explicitly released from memory with the free() function. It will be released automatically by the engine when it goes out of scope.

The main character of the show is the EditorImportPlugin class. It is responsible for implementing the methods that are called by Godot when it needs to know how to deal with files.

Let's begin to code our plugin, one method at time:

The first method is the _get_importer_name(). This is a unique name for your plugin that is used by Godot to know which import was used in a certain file. When the files needs to be reimported, the editor will know which plugin to call.

The _get_visible_name() method is responsible for returning the name of the type it imports and it will be shown to the user in the Import dock.

You should choose this name as a continuation to "Import as", e.g. "Import as Silly Material". You can name it whatever you want but we recommend a descriptive name for your plugin.

Godot's import system detects file types by their extension. In the _get_recognized_extensions() method you return an array of strings to represent each extension that this plugin can understand. If an extension is recognized by more than one plugin, the user can select which one to use when importing the files.

Common extensions like .json and .txt might be used by many plugins. Also, there could be files in the project that are just data for the game and should not be imported. You have to be careful when importing to validate the data. Never expect the file to be well-formed.

The imported files are saved in the .import folder at the project's root. Their extension should match the type of resource you are importing, but since Godot can't tell what you'll use (because there might be multiple valid extensions for the same resource), you need to declare what will be used in the import.

Since we're importing a Material, we'll use the special extension for such resource types. If you are importing a scene, you can use scn. Generic resources can use the res extension. However, this is not enforced in any way by the engine.

The imported resource has a specific type, so the editor can know which property slot it belongs to. This allows drag and drop from the FileSystem dock to a property in the Inspector.

In our case it's a StandardMaterial3D, which can be applied to 3D objects.

If you need to import different types from the same extension, you have to create multiple import plugins. You can abstract the import code on another file to avoid duplication in this regard.

Your plugin can provide different options to allow the user to control how the resource will be imported. If a set of selected options is common, you can also create different presets to make it easier for the user. The following image shows how the options will appear in the editor:

Since there might be many presets and they are identified with a number, it's a good practice to use an enum so you can refer to them using names.

Now that the enum is defined, let's keep looking at the methods of an import plugin:

The _get_preset_count() method returns the amount of presets that this plugins defines. We only have one preset now, but we can make this method future-proof by returning the size of our Presets enumeration.

Here we have the _get_preset_name() method, which gives names to the presets as they will be presented to the user, so be sure to use short and clear names.

We can use the match statement here to make the code more structured. This way it's easy to add new presets in the future. We use the catch all pattern to return something too. Although Godot won't ask for presets beyond the preset count you defined, it's always better to be on the safe side.

If you have only one preset you could simply return its name directly, but if you do this you have to be careful when you add more presets.

This is the method which defines the available options. _get_import_options() returns an array of dictionaries, and each dictionary contains a few keys that are checked to customize the option as it's shown to the user. The following table shows the possible keys:

The name of the option. When showed, underscores become spaces and first letters are capitalized.

The default value of the option for this preset.

One of the PropertyHint values to use as hint.

The hint text of the property. The same as you'd add in the export statement in GDScript.

One of the PropertyUsageFlags values to define the usage.

The name and default_value keys are mandatory, the rest are optional.

Note that the _get_import_options method receives the preset number, so you can configure the options for each different preset (especially the default value). In this example we use the match statement, but if you have lots of options and the presets only change the value you may want to create the array of options first and then change it based on the preset.

The _get_import_options method is called even if you don't define presets (by making _get_preset_count return zero). You have to return an array even it's empty, otherwise you can get errors.

For the _get_option_visibility() method, we simply return true because all of our options (i.e. the single one we defined) are visible all the time.

If you need to make certain option visible only if another is set with a certain value, you can add the logic in this method.

The heavy part of the process, responsible for converting the files into resources, is covered by the _import() method. Our sample code is a bit long, so let's split in a few parts:

The first part of our import method opens and reads the source file. We use the FileAccess class to do that, passing the source_file parameter which is provided by the editor.

If there's an error when opening the file, we return it to let the editor know that the import wasn't successful.

This code takes the line of the file it read before and splits it in pieces that are separated by a comma. If there are more or less than the three values, it considers the file invalid and reports an error.

Then it creates a new Color variable and sets its values according to the input file. If the use_red_anyway option is enabled, then it sets the color as a pure red instead.

This part makes a new StandardMaterial3D that is the imported resource. We create a new instance of it and then set its albedo color as the value we got before.

This is the last part and quite an important one, because here we save the made resource to the disk. The path of the saved file is generated and informed by the editor via the save_path parameter. Note that this comes without the extension, so we add it using string formatting. For this we call the _get_save_extension method that we defined earlier, so we can be sure that they won't get out of sync.

We also return the result from the ResourceSaver.save() method, so if there's an error in this step, the editor will know about it.

You may have noticed that our plugin ignored two arguments of the import method. Those are return arguments (hence the r at the beginning of their name), which means that the editor will read from them after calling your import method. Both of them are arrays that you can fill with information.

The r_platform_variants argument is used if you need to import the resource differently depending on the target platform. While it's called platform variants, it is based on the presence of feature tags, so even the same platform can have multiple variants depending on the setup.

To import a platform variant, you need to save it with the feature tag before the extension, and then push the tag to the r_platform_variants array so the editor can know that you did.

For example, let's say we save a different material for a mobile platform. We would need to do something like the following:

The r_gen_files argument is meant for extra files that are generated during your import process and need to be kept. The editor will look at it to understand the dependencies and make sure the extra file is not inadvertently deleted.

This is also an array and should be filled with full paths of the files you save. As an example, let's create another material for the next pass and save it in a different file:

This has been theoretical, but now that the import plugin is done, let's test it. Make sure you created the sample file (with the contents described in the introduction section) and save it as test.mtxt. Then activate the plugin in the Project Settings.

If everything goes well, the import plugin is added to the editor and the file system is scanned, making the custom resource appear on the FileSystem dock. If you select it and focus the Import dock, you can see the only option to select there.

Create a MeshInstance3D node in the scene, and for its Mesh property set up a new SphereMesh. Unfold the Material section in the Inspector and then drag the file from the FileSystem dock to the material property. The object will update in the viewport with the blue color of the imported material.

Go to Import dock, enable the "Use Red Anyway" option, and click on "Reimport". This will update the imported material and should automatically update the view showing the red color instead.

And that's it! Your first import plugin is done! Now get creative and make plugins for your own beloved formats. This can be quite useful to write your data in a custom format and then use it in Godot as if they were native resources. This shows how the import system is powerful and extendable.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
[plugin]

name="Silly Material Importer"
description="Imports a 3D Material from an external text file."
author="Yours Truly"
version="1.0"
script="material_import.gd"
```

Example 2 (gdscript):
```gdscript
# material_import.gd
@tool
extends EditorPlugin


var import_plugin


func _enter_tree():
    import_plugin = preload("import_plugin.gd").new()
    add_import_plugin(import_plugin)


func _exit_tree():
    remove_import_plugin(import_plugin)
    import_plugin = null
```

Example 3 (gdscript):
```gdscript
# import_plugin.gd
@tool
extends EditorImportPlugin


func _get_importer_name():
    return "demos.sillymaterial"
```

Example 4 (go):
```go
func _get_visible_name():
    return "Silly Material"
```

---

## Making main screen plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/editor/making_main_screen_plugins.html

**Contents:**
- Making main screen plugins
- What this tutorial covers
- Initializing the plugin
- Main screen scene
- Update the plugin script
- Try the plugin
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Main screen plugins allow you to create new UIs in the central part of the editor, which appear next to the "2D", "3D", "Script", "Game", and "AssetLib" buttons. Such editor plugins are referred as "Main screen plugins".

This tutorial leads you through the creation of a basic main screen plugin. For the sake of simplicity, our main screen plugin will contain a single button that prints text to the console.

First create a new plugin from the Plugins menu. For this tutorial, we'll put it in a folder called main_screen, but you can use any name you'd like.

The plugin script will come with _enter_tree() and _exit_tree() methods, but for a main screen plugin we need to add a few extra methods. Add five extra methods such that the script looks like this:

The important part in this script is the _has_main_screen() function, which is overloaded so it returns true. This function is automatically called by the editor on plugin activation, to tell it that this plugin adds a new center view to the editor. For now, we'll leave this script as-is and we'll come back to it later.

Create a new scene with a root node derived from Control (for this example plugin, we'll make the root node a CenterContainer). Select this root node, and in the viewport, click the Layout menu and select Full Rect. You also need to enable the Expand vertical size flag in the inspector. The panel now uses all the space available in the main viewport.

Next, let's add a button to our example main screen plugin. Add a Button node, and set the text to "Print Hello" or similar. Add a script to the button like this:

Then connect the "pressed" signal to itself. If you need help with signals, see the Using signals article.

We are done with the main screen panel. Save the scene as main_panel.tscn.

We need to update the main_screen_plugin.gd script so the plugin instances our main panel scene and places it where it needs to be. Here is the full plugin script:

A couple of specific lines were added. MainPanel is a constant that holds a reference to the scene, and we instance it into main_panel_instance.

The _enter_tree() function is called before _ready(). This is where we instance the main panel scene, and add them as children of specific parts of the editor. We use EditorInterface.get_editor_main_screen() to obtain the main editor screen and add our main panel instance as a child to it. We call the _make_visible(false) function to hide the main panel so it doesn't compete for space when first activating the plugin.

The _exit_tree() function is called when the plugin is deactivated. If the main screen still exists, we call queue_free() to free the instance and remove it from memory.

The _make_visible() function is overridden to hide or show the main panel as needed. This function is automatically called by the editor when the user clicks on the main viewport buttons at the top of the editor.

The _get_plugin_name() and _get_plugin_icon() functions control the displayed name and icon for the plugin's main viewport button.

Another function you can add is the handles() function, which allows you to handle a node type, automatically focusing the main screen when the type is selected. This is similar to how clicking on a 3D node will automatically switch to the 3D viewport.

Activate the plugin in the Project Settings. You'll observe a new button next to 2D, 3D, Script above the main viewport. Clicking it will take you to your new main screen plugin, and the button in the middle will print text.

If you would like to try a finished version of this plugin, check out the plugin demos here: https://github.com/godotengine/godot-demo-projects/tree/master/plugins

If you would like to see a more complete example of what main screen plugins are capable of, check out the 2.5D demo projects here: https://github.com/godotengine/godot-demo-projects/tree/master/misc/2.5d

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
@tool
extends EditorPlugin


func _enter_tree():
    pass


func _exit_tree():
    pass


func _has_main_screen():
    return true


func _make_visible(visible):
    pass


func _get_plugin_name():
    return "Main Screen Plugin"


func _get_plugin_icon():
    return EditorInterface.get_editor_theme().get_icon("Node", "EditorIcons")
```

Example 2 (json):
```json
#if TOOLS
using Godot;

[Tool]
public partial class MainScreenPlugin : EditorPlugin
{
    public override void _EnterTree()
    {

    }

    public override void _ExitTree()
    {

    }

    public override bool _HasMainScreen()
    {
        return true;
    }

    public override void _MakeVisible(bool visible)
    {

    }

    public override string _GetPluginName()
    {
        return "Main Screen Plugin";
    }

    public override Texture2D _GetPluginIcon()
    {
        return EditorInterface.Singleton.GetEditorTheme().GetIcon("Node", "EditorIcons");
    }
}
#endif
```

Example 3 (gdscript):
```gdscript
@tool
extends Button


func _on_print_hello_pressed():
    print("Hello from the main screen plugin!")
```

Example 4 (json):
```json
using Godot;

[Tool]
public partial class PrintHello : Button
{
    private void OnPrintHelloPressed()
    {
        GD.Print("Hello from the main screen plugin!");
    }
}
```

---

## Multiple resolutions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html

**Contents:**
- Multiple resolutions
- The problem of multiple resolutions
- One size fits all
- Base size
- Resizing
- Stretch settings
  - Stretch Mode
  - Stretch Aspect
  - Stretch Scale
  - Stretch Scale Mode

Developers often have trouble understanding how to best support multiple resolutions in their games. For desktop and console games, this is more or less straightforward, as most screen aspect ratios are 16:9 and resolutions are standard (720p, 1080p, 1440p, 4K, …).

For mobile games, at first, it was easy. For many years, the iPhone and iPad used the same resolution. When Retina was implemented, they just doubled the pixel density; most developers had to supply assets in default and double resolutions.

Nowadays, this is no longer the case, as there are plenty of different screen sizes, densities, and aspect ratios. Non-conventional sizes are also becoming increasingly popular, such as ultrawide displays.

For 3D rendering, there is not much of a need to support multiple resolutions. Thanks to its vector-based nature, 3D geometry will just fill the screen based on the viewport size. For 2D and game UIs, this is a different matter, as art needs to be created using specific pixel sizes in software such as Photoshop, GIMP or Krita.

Since layouts, aspect ratios, resolutions, and pixel densities can change so much, it is no longer possible to design UIs for every specific screen. Another method must be used.

The most common approach is to use a single base resolution and then fit it to everything else. This resolution is how most players are expected to play the game (given their hardware). For mobile, Google has useful stats online, and for desktop, Steam also does.

As an example, Steam shows that the most common primary display resolution is 1920×1080, so a sensible approach is to develop a game for this resolution, then handle scaling for different sizes and aspect ratios.

Godot provides several useful tools to do this easily.

You can see how Godot's support for multiple resolutions works in action using the Multiple Resolutions and Aspect Ratios demo project.

A base size for the window can be specified in the Project Settings under Display → Window.

However, what it does is not completely obvious; the engine will not attempt to switch the monitor to this resolution. Rather, think of this setting as the "design size", i.e. the size of the area that you work with in the editor. This setting corresponds directly to the size of the blue rectangle in the 2D editor.

There is often a need to support devices with screen and window sizes that are different from this base size. Godot offers many ways to control how the viewport will be resized and stretched to different screen sizes.

On this page, window refers to the screen area allotted to your game by the system, while viewport refers to the root object (accessible from get_tree().root) which the game controls to fill this screen area. This viewport is a Window instance. Recall from the introduction that all Window objects are viewports.

To configure the stretch base size at runtime from a script, use the get_tree().root.content_scale_size property (see Window.content_scale_size). Changing this value can indirectly change the size of 2D elements. However, to provide a user-accessible scaling option, using Stretch Scale is recommended as it's easier to adjust.

Godot follows a modern approach to multiple resolutions. The engine will never change the monitor's resolution on its own. While changing the monitor's resolution is the most efficient approach, it's also the least reliable approach as it can leave the monitor stuck on a low resolution if the game crashes. This is especially common on macOS or Linux which don't handle resolution changes as well as Windows.

Changing the monitor's resolution also removes any control from the game developer over filtering and aspect ratio stretching, which can be important to ensure correct display for pixel art games.

On top of that, changing the monitor's resolution makes alt-tabbing in and out of a game much slower since the monitor has to change resolutions every time this is done.

There are several types of devices, with several types of screens, which in turn have different pixel density and resolutions. Handling all of them can be a lot of work, so Godot tries to make the developer's life a little easier. The Viewport node has several functions to handle resizing, and the root node of the scene tree is always a viewport (scenes loaded are instanced as a child of it, and it can always be accessed by calling get_tree().root or get_node("/root")).

In any case, while changing the root Viewport params is probably the most flexible way to deal with the problem, it can be a lot of work, code and guessing, so Godot provides a set of parameters in the project settings to handle multiple resolutions.

To render 3D at a lower resolution than 2D elements (without needing separate viewports), you can use Godot's resolution scaling support. This is a good way to improve performance significantly in GPU-bottlenecked scenarios. This works with any stretch mode and stretch aspect combination.

Stretch settings are located in the project settings and provide several options:

The Stretch Mode setting defines how the base size is stretched to fit the resolution of the window or screen. The animations below use a "base size" of just 16×9 pixels to demonstrate the effect of different stretch modes. A single sprite, also 16×9 pixels in size, covers the entire viewport, and a diagonal Line2D is added on top of it:

Stretch Mode = Disabled (default): No stretching happens. One unit in the scene corresponds to one pixel on the screen. In this mode, the Stretch Aspect setting has no effect.

Stretch Mode = Canvas Items: In this mode, the base size specified in width and height in the project settings is stretched to cover the whole screen (taking the Stretch Aspect setting into account). This means that everything is rendered directly at the target resolution. 3D is unaffected, while in 2D, there is no longer a 1:1 correspondence between sprite pixels and screen pixels, which may result in scaling artifacts.

Stretch Mode = Viewport: Viewport scaling means that the size of the root Viewport is set precisely to the base size specified in the Project Settings' Display section. The scene is rendered to this viewport first. Finally, this viewport is scaled to fit the screen (taking the Stretch Aspect setting into account).

To configure the stretch mode at runtime from a script, use the get_tree().root.content_scale_mode property (see Window.content_scale_mode and the ContentScaleMode enum).

The second setting is the stretch aspect. Note that this only takes effect if Stretch Mode is set to something other than Disabled.

In the animations below, you will notice gray and black areas. The black areas are added by the engine and cannot be drawn into. The gray areas are part of your scene, and can be drawn to. The gray areas correspond to the region outside the blue frame you see in the 2D editor.

Stretch Aspect = Ignore: Ignore the aspect ratio when stretching the screen. This means that the original resolution will be stretched to exactly fill the screen, even if it's wider or narrower. This may result in nonuniform stretching: things looking wider or taller than designed.

Stretch Aspect = Keep: Keep aspect ratio when stretching the screen. This means that the viewport retains its original size regardless of the screen resolution, and black bars will be added to the top/bottom of the screen ("letterboxing") or the sides ("pillarboxing").

This is a good option if you know the aspect ratio of your target devices in advance, or if you don't want to handle different aspect ratios.

Stretch Aspect = Keep Width: Keep aspect ratio when stretching the screen. If the screen is wider than the base size, black bars are added at the left and right (pillarboxing). But if the screen is taller than the base resolution, the viewport will be grown in the vertical direction (and more content will be visible to the bottom). You can also think of this as "Expand Vertically".

This is usually the best option for creating GUIs or HUDs that scale, so some controls can be anchored to the bottom (Size and anchors).

Stretch Aspect = Keep Height: Keep aspect ratio when stretching the screen. If the screen is taller than the base size, black bars are added at the top and bottom (letterboxing). But if the screen is wider than the base resolution, the viewport will be grown in the horizontal direction (and more content will be visible to the right). You can also think of this as "Expand Horizontally".

This is usually the best option for 2D games that scroll horizontally (like runners or platformers).

Stretch Aspect = Expand: Keep aspect ratio when stretching the screen, but keep neither the base width nor height. Depending on the screen aspect ratio, the viewport will either be larger in the horizontal direction (if the screen is wider than the base size) or in the vertical direction (if the screen is taller than the original size).

To support both portrait and landscape mode with a similar automatically determined scale factor, set your project's base resolution to be a square (1:1 aspect ratio) instead of a rectangle. For instance, if you wish to design for 1280×720 as the base resolution but wish to support both portrait and landscape mode, use 720×720 as the project's base window size in the Project Settings.

To allow the user to choose their preferred screen orientation at runtime, remember to set Display > Window > Handheld > Orientation to sensor.

To configure the stretch aspect at runtime from a script, use the get_tree().root.content_scale_aspect property (see Window.content_scale_aspect and the ContentScaleAspect enum).

The Scale setting allows you to add an extra scaling factor on top of what the Stretch options above already provide. The default value of 1.0 means that no additional scaling occurs.

For example, if you set Scale to 2.0 and leave Stretch Mode on Disabled, each unit in your scene will correspond to 2×2 pixels on the screen. This is a good way to provide scaling options for non-game applications.

If Stretch Mode is set to canvas_items, 2D elements will be scaled relative to the base window size, then multiplied by the Scale setting. This can be exposed to players to allow them to adjust the automatically determined scale to their liking, for better accessibility.

If Stretch Mode is set to viewport, the viewport's resolution is divided by Scale. This makes pixels look larger and reduces rendering resolution (with a given window size), which can improve performance.

To configure the stretch scale at runtime from a script, use the get_tree().root.content_scale_factor property (see Window.content_scale_factor).

You can also adjust the scale at which the default project theme is generated using the GUI > Theme > Default Theme Scale project setting. This can be used to create more logically-sized UIs at base resolutions that are significantly higher or lower than the default. However, this project setting cannot be changed at runtime, as its value is only read once when the project starts.

Since Godot 4.2, the Stretch Scale Mode setting allows you to constrain the automatically determined scale factor (as well as the manually specified Stretch Scale setting) to integer values. By default, this setting is set to fractional, which allows any scale factor to be applied (including fractional values such as 2.5). When set to integer, the value is rounded down to the nearest integer. For example, instead of using a scale factor of 2.5, it would be rounded down to 2.0. This is useful to prevent distortion when displaying pixel art.

Compare this pixel art which is displayed with the viewport stretch mode, with the stretch scale mode set to fractional:

Checkerboard doesn't look "even". Line widths in the logo and text varies wildly.

This pixel art is also displayed with the viewport stretch mode, but the stretch scale mode is set to integer this time:

Checkerboard looks perfectly even. Line widths are consistent.

For example, if your viewport base size is 640×360 and the window size is 1366×768:

When using fractional, the viewport is displayed at a resolution of 1366×768 (scale factor is roughly 2.133×). The entire window space is used. Each pixel in the viewport corresponds to 2.133×2.133 pixels in the displayed area. However, since displays can only display "whole" pixels, this will lead to uneven pixel scaling which results in incorrect appearance of pixel art.

When using integer, the viewport is displayed at a resolution of 1280×720 (scale factor is 2×). The remaining space is filled with black bars on all four sides, so that each pixel in the viewport corresponds to 2×2 pixels in the displayed area.

This setting is effective with any stretch mode. However, when using the disabled stretch mode, it will only affect the Stretch Scale setting by rounding it down to the nearest integer value. This can be used for 3D games that have a pixel art UI, so that the visible area in the 3D viewport doesn't reduce in size (which occurs when using canvas_items or viewport stretch mode with the integer scale mode).

Games should use the Exclusive Fullscreen window mode, as opposed to Fullscreen which is designed to prevent Windows from automatically treating the window as if it was exclusive fullscreen.

Fullscreen is meant to be used by GUI applications that want to use per-pixel transparency without a risk of having it disabled by the OS. It achieves this by leaving a 1-pixel line at the bottom of the screen. By contrast, Exclusive Fullscreen uses the actual screen size and allows Windows to reduce jitter and input lag for fullscreen games.

When using integer scaling, this is particularly important as the 1-pixel height reduction from the Fullscreen mode can cause integer scaling to use a smaller scale factor than expected.

The following settings are recommended to support multiple resolutions and aspect ratios well.

Set the base window width to 1920 and window height to 1080. If you have a display smaller than 1920×1080, set Window Width Override and Window Height Override to lower values to make the window smaller when the project starts.

Alternatively, if you're targeting high-end devices primarily, set the base window width to 3840 and window height to 2160. This allows you to provide higher resolution 2D assets, resulting in crisper visuals at the cost of higher memory usage and file sizes. You'll also want to increase GUI > Theme > Default Theme Scale to a value between 2.0 and 3.0 to ensure UI elements remain readable.

Note that this will make non-mipmapped textures grainy on low resolution devices, so make sure to follow the instructions described in Reducing aliasing on downsampling.

Set the stretch mode to canvas_items.

Set the stretch aspect to expand. This allows for supporting multiple aspect ratios and makes better use of tall smartphone displays (such as 18:9 or 19:9 aspect ratios).

Configure Control nodes' anchors to snap to the correct corners using the Layout menu.

For 3D games, consider exposing Resolution scaling in the game's options menu to allow players to adjust the 3D rendering resolution separately from UI elements. This is useful for performance tuning, especially on lower-end hardware.

Set the base window size to the viewport size you intend to use. Most pixel art games use viewport sizes between 256×224 and 640×480. 640×360 is a good baseline, as it scales to 1280×720, 1920×1080, 2560×1440, and 3840×2160 without any black bars when using integer scaling. Higher viewport sizes will require using higher resolution artwork, unless you intend to show more of the game world at a given time.

Set the stretch mode to viewport.

Set the stretch aspect to keep to enforce a single aspect ratio (with black bars). As an alternative, you can set the stretch aspect to expand to support multiple aspect ratios.

If using the expand stretch aspect, Configure Control nodes' anchors to snap to the correct corners using the Layout menu.

Set the stretch scale mode to integer. This prevents uneven pixel scaling from occurring, which makes pixel art not display as intended.

The viewport stretch mode provides low-resolution rendering that is then stretched to the final window size. If you are OK with sprites being able to move or rotate in "sub-pixel" positions or wish to have a high resolution 3D viewport, you should use the canvas_items stretch mode instead of the viewport stretch mode.

Godot is configured to use landscape mode by default. This means you don't need to change the display orientation project setting.

Set the base window width to 1280 and window height to 720.

Alternatively, if you're targeting high-end devices primarily, set the base window width to 1920 and window height to 1080. This allows you to provide higher resolution 2D assets, resulting in crisper visuals at the cost of higher memory usage and file sizes. Many devices have even higher resolution displays (1440p), but the difference with 1080p is barely visible given the small size of smartphone displays. You'll also want to increase GUI > Theme > Default Theme Scale to a value between 1.5 and 2.0 to ensure UI elements remain readable.

Note that this will make non-mipmapped textures grainy on low resolution devices, so make sure to follow the instructions described in Reducing aliasing on downsampling.

Set the stretch mode to canvas_items.

Set the stretch aspect to expand. This allows for supporting multiple aspect ratios and makes better use of tall smartphone displays (such as 18:9 or 19:9 aspect ratios).

Configure Control nodes' anchors to snap to the correct corners using the Layout menu.

To better support tablets and foldable phones (which frequently feature displays with aspect ratios close to 4:3), consider using a base resolution that has a 4:3 aspect ratio while following the rest of the instructions here. For instance, you can set the base window width to 1280 and the base window height to 960.

Set the base window width to 720 and window height to 1280.

Alternatively, if you're targeting high-end devices primarily, set the base window width to 1080 and window height to 1920. This allows you to provide higher resolution 2D assets, resulting in crisper visuals at the cost of higher memory usage and file sizes. Many devices have even higher resolution displays (1440p), but the difference with 1080p is barely visible given the small size of smartphone displays. You'll also want to increase GUI > Theme > Default Theme Scale to a value between 1.5 and 2.0 to ensure UI elements remain readable.

Note that this will make non-mipmapped textures grainy on low resolution devices, so make sure to follow the instructions described in Reducing aliasing on downsampling.

Set Display > Window > Handheld > Orientation to portrait.

Set the stretch mode to canvas_items.

Set the stretch aspect to expand. This allows for supporting multiple aspect ratios and makes better use of tall smartphone displays (such as 18:9 or 19:9 aspect ratios).

Configure Control nodes' anchors to snap to the correct corners using the Layout menu.

To better support tablets and foldable phones (which frequently feature displays with aspect ratios close to 4:3), consider using a base resolution that has a 3:4 aspect ratio while following the rest of the instructions here. For instance, you can set the base window width to 960 and the base window height to 1280.

Set the base window width and height to the smallest window size that you intend to target. This is not required, but this ensures that you design your UI with small window sizes in mind.

Keep the stretch mode to its default value, disabled.

Keep the stretch aspect to its default value, ignore (its value won't be used since the stretch mode is disabled).

You can define a minimum window size by calling get_window().set_min_size() in a script's _ready() function. This prevents the user from resizing the application below a certain size, which could break the UI layout.

Add a setting in the application's settings to change the root viewport's stretch scale, so that the UI can be made larger to account for hiDPI displays. See also the section on hiDPI support below.

By default, Godot projects are considered DPI-aware by the operating system. This is controlled by the Display > Window > DPI > Allow hiDPI project setting, which should be left enabled whenever possible. Disabling DPI awareness can break fullscreen behavior on Windows.

Since Godot projects are DPI-aware, they may appear at a very small window size when launching on an hiDPI display (proportionally to the screen resolution). For a game, the most common way to work around this issue is to make them fullscreen by default. Alternatively, you could set the window size in an autoload's _ready() function according to the screen size.

To ensure 2D elements don't appear too small on hiDPI displays:

For games, use the canvas_items or viewport stretch modes so that 2D elements are automatically resized according to the current window size.

For non-game applications, use the disabled stretch mode and set the stretch scale to a value corresponding to the display scale factor in an autoload's _ready() function. The display scale factor is set in the operating system's settings and can be queried using screen_get_scale. This method is currently implemented on Android, iOS, Linux (Wayland only), macOS and Web. On other platforms, you'll have to implement a method to guess the display scale factor based on the screen resolution (with a setting to let the user override this if needed). This is the approach currently used by the Godot editor.

The Allow hiDPI setting is only effective on Windows and macOS. It's ignored on all other platforms.

The Godot editor itself is always marked as DPI-aware. Running the project from the editor will only be DPI-aware if Allow hiDPI is enabled in the Project Settings.

If the game has a very high base resolution (e.g. 3840×2160), aliasing might appear when downsampling to something considerably lower like 1280×720.

To resolve this, you can enable mipmaps on all your 2D textures. However, enabling mipmaps will increase memory usage which can be an issue on low-end mobile devices.

Once scaling for different resolutions is accounted for, make sure that your user interface also scales for different aspect ratios. This can be done using anchors and/or containers.

The 3D Camera node's Keep Aspect property defaults to the Keep Height scaling mode (also called Hor+). This is usually the best value for desktop games and mobile games in landscape mode, as widescreen displays will automatically use a wider field of view.

However, if your 3D game is intended to be played in portrait mode, it may make more sense to use Keep Width instead (also called Vert-). This way, smartphones with an aspect ratio taller than 16:9 (e.g. 19:9) will use a taller field of view, which is more logical here.

To render 3D at a different resolution from 2D elements (such as the UI), use Godot's resolution scaling functionality. This allows you to control the resolution scale factor used for 3D without needing to use a separate Viewport node. This can either be used to improve performance by rendering 3D at a lower resolution, or improve quality via supersampling.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Running code in the editor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html

**Contents:**
- Running code in the editor
- What is @tool?
- How to use @tool
- Important information
- Try @tool out
- Editing variables
- Getting notified when resources change
- Reporting node configuration warnings
- Running one-off scripts using EditorScript
- Instancing scenes

@tool is a powerful line of code that, when added at the top of your script, makes it execute in the editor. You can also decide which parts of the script execute in the editor, which in game, and which in both.

You can use it for doing many things, but it is mostly useful in level design for visually presenting things that are hard to predict ourselves. Here are some use cases:

If you have a cannon that shoots cannonballs affected by physics (gravity), you can draw the cannonball's trajectory in the editor, making level design a lot easier.

If you have jumppads with varying jump heights, you can draw the maximum jump height a player would reach if it jumped on one, also making level design easier.

If your player doesn't use a sprite, but draws itself using code, you can make that drawing code execute in the editor to see your player.

@tool scripts run inside the editor, and let you access the scene tree of the currently edited scene. This is a powerful feature which also comes with caveats, as the editor does not include protections for potential misuse of @tool scripts. Be extremely cautious when manipulating the scene tree, especially via Node.queue_free, as it can cause crashes if you free a node while the editor runs logic involving it.

To turn a script into a tool, add the @tool annotation at the top of your code.

To check if you are currently in the editor, use: Engine.is_editor_hint().

For example, if you want to execute some code only in the editor, use:

On the other hand, if you want to execute code only in game, simply negate the same statement:

Pieces of code that do not have either of the 2 conditions above will run both in-editor and in-game.

Here is how a _process() function might look for you:

The general rule is that any other GDScript that your tool script uses must *also* be a tool. The editor is not able to construct instances from GDScript files without @tool, which means you cannot call methods or reference member variables from them otherwise. However, since static methods, constants and enums can be used without creating an instance, it is possible to call them or reference them from a @tool script onto other non-tool scripts. One exception to this are static variables. If you try to read a static variable's value in a script that does not have @tool, it will always return null but won't print a warning or error when doing so. This restriction does not apply to static methods, which can be called regardless of whether the target script is in tool mode.

Extending a @tool script does not automatically make the extending script a @tool. Omitting @tool from the extending script will disable tool behavior from the super class. Therefore, the extending script should also specify the @tool annotation.

Modifications in the editor are permanent, with no undo/redo possible. For example, in the next section when we remove the script, the node will keep its rotation. Be careful to avoid making unwanted modifications. Consider setting up version control to avoid losing work in case you make a mistake.

Using the debugger and breakpoints on tool scripts is not currently supported. Breakpoints placed in the script editor or using the breakpoint keyword are ignored. You can use print statements to display the contents of variables instead.

Add a Sprite2D node to your scene and set the texture to Godot icon. Attach and open a script, and change it to this:

Save the script and return to the editor. You should now see your object rotate. If you run the game, it will also rotate.

You may need to restart the editor. This is a known bug found in all Godot 4 versions: GH-66381.

If you don't see the changes, reload the scene (close it and open it again).

Now let's choose which code runs when. Modify your _process() function to look like this:

Save the script. Now the object will spin clockwise in the editor, but if you run the game, it will spin counter-clockwise.

Add and export a variable speed to the script. To update the speed and also reset the rotation angle add a setter set(new_speed) which is executed with the input from the inspector. Modify _process() to include the rotation speed.

Code from other nodes doesn't run in the editor. Your access to other nodes is limited. You can access the tree and nodes, and their default properties, but you can't access user variables. If you want to do so, other nodes have to run in the editor too.

Sometimes you want your tool to use a resource. However, when you change a property of that resource in the editor, the set() method of your tool will not be called.

To get around this problem you first have to make your resource a tool and make it emit the changed signal whenever a property is set:

You then want to connect the signal when a new resource is set:

Lastly, remember to disconnect the signal as the old resource being used and changed somewhere else would cause unneeded updates.

Godot uses a node configuration warning system to warn users about incorrectly configured nodes. When a node isn't configured correctly, a yellow warning sign appears next to the node's name in the Scene dock. When you hover or click on the icon, a warning message pops up. You can use this feature in your scripts to help you and your team avoid mistakes when setting up scenes.

When using node configuration warnings, when any value that should affect or remove the warning changes, you need to call update_configuration_warnings . By default, the warning only updates when closing and reopening the scene.

Sometimes, you need to run code just one time to automate a certain task that is not available in the editor out of the box. Some examples might be:

Use as a playground for GDScript or C# scripting without having to run a project. print() output is displayed in the editor Output panel.

Scale all light nodes in the currently edited scene, as you noticed your level ends up looking too dark or too bright after placing lights where desired.

Replace nodes that were copy-pasted with scene instances to make them easier to modify later.

This is available in Godot by extending EditorScript in a script. This provides a way to run individual scripts in the editor without having to create an editor plugin.

To create an EditorScript, right-click a folder or empty space in the FileSystem dock then choose New > Script.... In the script creation dialog, click the tree icon to choose an object to extend from (or enter EditorScript directly in the field on the left, though note this is case-sensitive):

Creating an editor script in the script editor creation dialog

This will automatically select a script template that is suited for EditorScripts, with a _run() method already inserted:

This _run() method is executed when you use File > Run or the keyboard shortcut Ctrl + Shift + X while the EditorScript is the currently open script in the script editor. This keyboard shortcut is only effective when currently focused on the script editor.

Scripts that extend EditorScript must be @tool scripts to function.

EditorScripts can only be run from the Godot script editor. If you are using an external editor, open the script inside the Godot script editor to run it.

EditorScripts have no undo/redo functionality, so make sure to save your scene before running one if the script is designed to modify any data.

To access nodes in the currently edited scene, use the EditorScript.get_scene method which returns the root Node of the currently edited scene. Here's an example that recursively gets all nodes in the currently edited scene and doubles the range of all OmniLight3D nodes:

You can change the currently edited scene at the top of the editor even while the Script view is open. This will affect the return value of EditorScript.get_scene, so make sure you've selected the scene you intend to iterate upon before running the script.

You can instantiate packed scenes normally and add them to the scene currently opened in the editor. By default, nodes or scenes added with Node.add_child(node) are not visible in the Scene tree dock and are not persisted to disk. If you wish the node or scene to be visible in the scene tree dock and persisted to disk when saving the scene, you need to set the child node's owner property to the currently edited scene root.

If you are using @tool:

If you are using EditorScript:

Using @tool improperly can yield many errors. It is advised to first write the code how you want it, and only then add the @tool annotation to the top. Also, make sure to separate code that runs in-editor from code that runs in-game. This way, you can find bugs more easily.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
if Engine.is_editor_hint():
    # Code to execute when in editor.
```

Example 2 (json):
```json
if (Engine.IsEditorHint())
{
    // Code to execute when in editor.
}
```

Example 3 (unknown):
```unknown
if not Engine.is_editor_hint():
    # Code to execute when in game.
```

Example 4 (json):
```json
if (!Engine.IsEditorHint())
{
    // Code to execute when in game.
}
```

---

## Overview of renderers — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html

**Contents:**
- Overview of renderers
- Introduction
  - Renderers, rendering drivers, and RenderingDevice
- Choosing a renderer
  - Switching between renderers
- Feature comparison
  - Overall comparison
  - Lights and shadows
  - Global Illumination
  - Environment and post-processing

This page gives an overview of Godot's renderers, focusing on the differences between their rendering features. For more technical details on the renderers, see Internal rendering architecture.

Godot 4 includes three renderers:

Forward+. The most advanced renderer, suited for desktop platforms only. Used by default on desktop platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Mobile. Fewer features, but renders simple scenes faster. Suited for mobile and desktop platforms. Used by default on mobile platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Compatibility, sometimes called GL Compatibility. The least advanced renderer, suited for low-end desktop and mobile platforms. Used by default on the web platform. This renderer uses OpenGL as the rendering driver.

Godot's rendering abstraction layers.

The renderer, or rendering method, determines which features are available. Most of the time, this is the only thing you need to think about. Godot's renderers are Forward+, Mobile, and Compatibility.

The rendering driver tells the GPU what to do, using a graphics API. Godot can use the OpenGL, Vulkan, Direct3D 12, and Metal rendering drivers. Not every GPU supports every rendering driver, and therefore not every GPU supports all renderers. Vulkan, Direct3D 12, and Metal are modern, low-level graphics APIs, and requires newer hardware. OpenGL is an older graphics API that runs on most hardware.

RenderingDevice is a rendering backend, an abstraction layer between the renderer and the rendering driver. It is used by the Forward+ and Mobile renderers, and these renderers are sometimes called "RenderingDevice-based renderers".

Choosing a renderer is a complex question, and depends on your hardware and the which platforms you are developing for. As a starting point:

You are developing for desktop.

You have relatively new hardware which supports Vulkan, Direct3D 12, or Metal.

You are developing a 3D game.

You want to use the most advanced rendering features.

You are developing for newer mobile devices, desktop XR, or desktop.

You have relatively new hardware which supports Vulkan, Direct3D 12, or Metal.

You are developing a 3D game.

You want to use advanced rendering features, subject to the limitations of mobile hardware.

Choose Compatibility if:

You are developing for older mobile devices, older desktop devices, or standalone XR. The Compatibility renderer supports the widest range of hardware.

You are developing for web. In this case, Compatibility is the only choice.

You have older hardware which does not support Vulkan. In this case, Compatibility is the only choice.

You are developing a 2D game, or a 3D game which does not need advanced rendering features.

You want the best performance possible on all devices and don't need advanced rendering features.

Keep in mind every game is unique, and this is only a starting point. For example, you might choose to use the Compatibility renderer even though you have the latest GPU, so you can support the widest range of hardware. Or you might want to use the Forward+ renderer for a 2D game, so you can advanced features like compute shaders.

In the editor, you can always switch between renderers by clicking on the renderer name in the upper-right corner of the editor.

Switching between renderers may require some manual tweaks to your scene, lighting, and environment, since each renderer is different. In general, switching between the Mobile and Forward+ renderers will require fewer adjustments than switching between the Compatibility renderer and the Forward+ or Mobile renderers.

Since Godot 4.4, when using Forward+ or Mobile, if Vulkan is not supported, the engine will fall back to Direct3D 12 and vice versa. If the attempted fallback driver is not supported either, the engine will then fall back to Compatibility when the RenderingDevice backend is not supported. This allows the project to run anyway, but it may look different than the intended appearance due to the more limited renderer. This behavior can be disabled in the project settings by unchecking Rendering > Rendering Device > Fallback to OpenGL 3.

This is not a complete list of the features of each renderer. If a feature is not listed here, it is available in all renderers, though it may be much faster on some renderers. For a list of all features in Godot, see List of features.

Hardware with RenderingDevice support is hardware which can run Vulkan, Direct3D 12, or Metal.

Newer or high-end. Requires Vulkan, Direct3D 12, or Metal support.

Newer or high-end. Requires Vulkan, Direct3D 12, or Metal support.

Runs on old and low-end hardware

✔️ Yes, but slower than Compatibility.

✔️ Yes, but slowest of all renderers.

Runs on hardware without RenderingDevice support

Mobile, low-end desktop, web.

⚠️ Supported, but poorly optimized. Use Mobile or Compatibility instead.

✔️ Yes. Recommended for standalone headsets.

✔️ Yes. Recommended for desktop headsets.

⚠️ Supported, but poorly optimized. Use Mobile or Compatibility instead.

✔️ Yes, but Compatibility is usually good enough for 2D.

✔️ Yes, but Compatibility is usually good enough for 2D.

2D and core 3D features.

Most rendering features.

All rendering features.

2D rendering features

Core 3D rendering features

Advanced rendering features

⚠️ Yes, limited by mobile hardware.

✔️ Yes. All rendering features are supported.

⚠️ Some new rendering features are added to Compatibility. Features are added after Mobile and Forward+.

✔️ Most new rendering features are added to Mobile. Mobile usually gets new features as Forward+ does.

✔️ All new features are added to Forward+. As the focus of new development, Forward+ gets features first.

Low base cost, but high scaling cost.

Medium base cost, and medium scaling cost.

Highest base cost, and low scaling cost.

Vulkan, Direct3D 12, or Metal.

Vulkan, Direct3D 12, or Metal.

See 3D lights and shadows for more information.

8 per mesh. Can be increased.

8 per mesh, 256 per view.

512 per cluster. Can be increased.

8 per mesh. Can be increased.

8 per mesh, 256 per view.

512 per cluster. Can be increased.

Maximum DirectionalLights

PCSS for OmniLight and SpotLight

PCSS for DirectionalLight

Light projector textures

See Introduction to global illumination for more information.

✔️ Supported, 2 per mesh.

✔️ Supported, 8 per mesh.

✔️ Supported, unlimited.

⚠️ Rendering of baked lightmaps is supported. Baking requires hardware with RenderingDevice support.

Screen-Space Indirect Lighting (SSIL)

Signed Distance Field Global Illumination (SDFGI)

See Environment and post-processing for more information.

Fog (Depth and Height)

Screen-Space Reflections

Screen-Space Ambient Occlusion (SSAO)

Screen-Space Indirect Lighting (SSIL)

Signed Distance Field Global Illumination (SDFGI)

Custom post-processing with fullscreen quad

Custom post-processing with CompositorEffects

See 3D antialiasing for more information.

Screen-space roughness limiter

See Standard Material 3D and ORM Material 3D for more information.

Sub-surface scattering

See Shading reference for more information.

Normal/Roughness texture

⚠️ Supported, but comes with a performance penalty on older devices.

Variable rate shading

Adaptive and Mailbox VSync modes

RenderingDevice access

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Rendering — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/index.html

**Contents:**
- Rendering

Most rendering topics are covered in 2D rendering and 3D rendering.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using Viewports — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/viewports.html

**Contents:**
- Using Viewports
- Introduction
- Input
- Listener
- Cameras (2D & 3D)
- Scale & stretching
- Worlds
- Capture
- Viewport Container
- Rendering

Think of a Viewport as a screen onto which the game is projected. In order to see the game, we need to have a surface on which to draw it. That surface is the Root Viewport.

SubViewports are a kind of Viewport that can be added to the scene so that there are multiple surfaces to draw on. When we are drawing to a SubViewport, we call it a render target. We can access the contents of a render target by accessing its corresponding texture. By using a SubViewport as render target, we can either render multiple scenes simultaneously or we can render to a ViewportTexture which is applied to an object in the scene, for example a dynamic skybox.

SubViewports have a variety of use cases, including:

Rendering 3D objects within a 2D game

Rendering 2D elements in a 3D game

Rendering dynamic textures

Generating procedural textures at runtime

Rendering multiple cameras in the same scene

What all these use cases have in common is that you are given the ability to draw objects to a texture as if it were another screen and can then choose what to do with the resulting texture.

Another kind of Viewports in Godot are Windows. They allow their content to be projected onto a window. While the Root Viewport is a Window, they are less flexible. If you want to use the texture of a Viewport, you'll be working with SubViewports most of the time.

Viewports are also responsible for delivering properly adjusted and scaled input events to their children nodes. By default SubViewports don't automatically receive input, unless they receive it from their direct SubViewportContainer parent node. In this case, input can be disabled with the Disable Input property.

For more information on how Godot handles input, please read the Input Event Tutorial.

Godot supports 3D sound (in both 2D and 3D nodes). More on this can be found in the Audio Streams Tutorial. For this type of sound to be audible, the Viewport needs to be enabled as a listener (for 2D or 3D). If you are using a SubViewport to display your World3D or World2D, don't forget to enable this!

When using a Camera3D or Camera2D, it will always display on the closest parent Viewport (going towards the root). For example, in the following hierarchy:

CameraA will display on the Root Viewport and it will draw MeshA. CameraB will be captured by the SubViewport along with MeshB. Even though MeshB is in the scene hierarchy, it will still not be drawn to the Root Viewport. Similarly, MeshA will not be visible from the SubViewport because SubViewports only capture nodes below them in the hierarchy.

There can only be one active camera per Viewport, so if there is more than one, make sure that the desired one has the current property set, or make it the current camera by calling:

By default, cameras will render all objects in their world. In 3D, cameras can use their cull_mask property combined with the VisualInstance3D's layer property to restrict which objects are rendered.

SubViewports have a size property, which represents the size of the SubViewport in pixels. For SubViewports which are children of SubViewportContainers, these values are overridden, but for all others, this sets their resolution.

It is also possible to scale the 2D content and make the SubViewport resolution different from the one specified in size, by calling:

For information on scaling and stretching with the Root Viewport visit the Multiple Resolutions Tutorial

For 3D, a Viewport will contain a World3D. This is basically the universe that links physics and rendering together. Node3D-based nodes will register using the World3D of the closest Viewport. By default, newly created Viewports do not contain a World3D but use the same as their parent Viewport. The Root Viewport always contains a World3D, which is the one objects are rendered to by default.

A World3D can be set in a Viewport using the World 3D property, that will separate all children nodes of this Viewport and will prevent them from interacting with the parent Viewport's World3D. This is especially useful in scenarios where, for example, you might want to show a separate character in 3D imposed over the game (like in StarCraft).

As a helper for situations where you want to create Viewports that display single objects and don't want to create a World3D, Viewport has the option to use its Own World3D. This is useful when you want to instance 3D characters or objects in World2D.

For 2D, each Viewport always contains its own World2D. This suffices in most cases, but in case sharing them may be desired, it is possible to do so by setting world_2d on the Viewport through code.

For an example of how this works, see the demo projects 3D in 2D and 2D in 3D respectively.

It is possible to query a capture of the Viewport contents. For the Root Viewport, this is effectively a screen capture. This is done with the following code:

But if you use this in _ready() or from the first frame of the Viewport's initialization, you will get an empty texture because there is nothing to get as texture. You can deal with it using (for example):

If the SubViewport is a child of a SubViewportContainer, it will become active and display anything it has inside. The layout looks like this:

The SubViewport will cover the area of its parent SubViewportContainer completely if Stretch is set to true in the SubViewportContainer.

The size of the SubViewportContainer cannot be smaller than the size of the SubViewport.

Due to the fact that the Viewport is an entryway into another rendering surface, it exposes a few rendering properties that can be different from the project settings. You can choose to use a different level of MSAA for each Viewport. The default behavior is Disabled.

If you know that the Viewport is only going to be used for 2D, you can Disable 3D. Godot will then restrict how the Viewport is drawn. Disabling 3D is slightly faster and uses less memory compared to enabled 3D. It's a good idea to disable 3D if your viewport doesn't render anything in 3D.

If you need to render 3D shadows in the viewport, make sure to set the viewport's positional_shadow_atlas_size property to a value higher than 0. Otherwise, shadows won't be rendered. By default, the equivalent project setting is set to 4096 on desktop platforms and 2048 on mobile platforms.

Godot also provides a way of customizing how everything is drawn inside Viewports using Debug Draw. Debug Draw allows you to specify a mode which determines how the Viewport will display things drawn inside it. Debug Draw is Disabled by default. Some other options are Unshaded, Overdraw, and Wireframe. For a full list, refer to the Viewport Documentation.

Debug Draw = Disabled (default): The scene is drawn normally.

Debug Draw = Unshaded: Unshaded draws the scene without using lighting information so all the objects appear flatly colored in their albedo color.

Debug Draw = Overdraw: Overdraw draws the meshes semi-transparent with an additive blend so you can see how the meshes overlap.

Debug Draw = Wireframe: Wireframe draws the scene using only the edges of triangles in the meshes.

Debug Draw modes are currently not supported when using the Compatibility rendering method. They will appear as regular draw modes.

When rendering to a SubViewport, whatever is inside will not be visible in the scene editor. To display the contents, you have to draw the SubViewport's ViewportTexture somewhere. This can be requested via code using (for example):

Or it can be assigned in the editor by selecting "New ViewportTexture"

and then selecting the Viewport you want to use.

Every frame, the Viewport's texture is cleared away with the default clear color (or a transparent color if Transparent BG is set to true). This can be changed by setting Clear Mode to Never or Next Frame. As the name implies, Never means the texture will never be cleared, while next frame will clear the texture on the next frame and then set itself to Never.

By default, re-rendering of the SubViewport happens when its ViewportTexture has been drawn in a frame. If visible, it will be rendered, otherwise, it will not. This behavior can be changed by setting Update Mode to Never, Once, Always, or When Parent Visible. Never and Always will never or always re-render respectively. Once will re-render the next frame and change to Never afterwards. This can be used to manually update the Viewport. This flexibility allows users to render an image once and then use the texture without incurring the cost of rendering every frame.

Make sure to check the Viewport demos. They are available in the viewport folder of the demos archive, or at https://github.com/godotengine/godot-demo-projects/tree/master/viewport.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
camera.make_current()
```

Example 2 (unknown):
```unknown
camera.MakeCurrent();
```

Example 3 (unknown):
```unknown
sub_viewport.set_size_2d_override(Vector2i(width, height)) # Custom size for 2D.
sub_viewport.set_size_2d_override_stretch(true) # Enable stretch for custom size.
```

Example 4 (unknown):
```unknown
subViewport.Size2DOverride = new Vector2I(width, height); // Custom size for 2D.
subViewport.Size2DOverrideStretch = true; // Enable stretch for custom size.
```

---

## The Compositor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/compositor.html

**Contents:**
- The Compositor
- Compositor effects
- User-contributed notes

The compositor is a new feature in Godot 4 that allows control over the rendering pipeline when rendering the contents of a Viewport.

It can be configured on a WorldEnvironment node where it applies to all Viewports, or it can be configured on a Camera3D and apply only to the Viewport using that camera.

The Compositor resource is used to configure the compositor. To get started, create a new compositor on the appropriate node:

The compositor is currently a feature that is only supported by the Mobile and Forward+ renderers.

Compositor effects allow you to insert additional logic into the rendering pipeline at various stages. This is an advanced feature that requires a high level of understanding of the rendering pipeline to use to its best advantage.

As the core logic of the compositor effect is called from the rendering pipeline it is important to note that this logic will thus run within the thread on which rendering takes place. Care needs to be taken to ensure we don't run into threading issues.

To illustrate how to use compositor effects we'll create a simple post processing effect that allows you to write your own shader code and apply this full screen through a compute shader. You can find the finished demo project here.

We start by creating a new script called post_process_shader.gd. We'll make this a tool script so we can see the compositor effect work in the editor. We need to extend our node from CompositorEffect. We must also give our script a class name.

Next we're going to define a constant for our shader template code. This is the boilerplate code that makes our compute shader work.

For more information on how compute shaders work, please check Using compute shaders.

The important bit here is that for every pixel on our screen, our main function is executed and inside of this we load the current color value of our pixel, execute our user code, and write our modified color back to our color image.

#COMPUTE_CODE gets replaced by our user code.

In order to set our user code, we need an export variable. We'll also define a few script variables we'll be using:

Note the use of a Mutex in our code. Most of our implementation gets called from the rendering engine and thus runs within our rendering thread.

We need to ensure that we set our new shader code, and mark our shader code as dirty, without our render thread accessing this data at the same time.

Next we initialize our effect.

The main thing here is setting our effect_callback_type which tells the rendering engine at what stage of the render pipeline to call our code.

Currently we only have access to the stages of the 3D rendering pipeline!

We also get a reference to our rendering device, which will come in very handy.

We also need to clean up after ourselves, for this we react to the NOTIFICATION_PREDELETE notification:

Note that we do not use our mutex here even though we create our shader inside of our render thread. The methods on our rendering server are thread safe and free_rid will be postponed cleaning up the shader until after any frames currently being rendered are finished.

Also note that we are not freeing our pipeline. The rendering device does dependency tracking and as the pipeline is dependent on the shader, it will be automatically freed when the shader is destructed.

From this point onwards our code will run on the rendering thread.

Our next step is a helper function that will recompile the shader if the user code was changed.

At the top of this method we again use our mutex to protect accessing our user shader code and our is dirty flag. We make a local copy of the user shader code if our user shader code is dirty.

If we don't have a new code fragment, we return true if we already have a valid pipeline.

If we do have a new code fragment we embed it in our template code and then compile it.

The code shown here compiles our new code in runtime. This is great for prototyping as we can immediately see the effect of the changed shader.

This prevents precompiling and caching this shader which may be an issues on some platforms such as consoles. Note that the demo project comes with an alternative example where a glsl file contains the entire compute shader and this is used. Godot is able to precompile and cache the shader with this approach.

Finally we need to implement our effect callback, the rendering engine will call this at the right stage of rendering.

At the start of this method we check if we have a rendering device, if our callback type is the correct one, and check if we have our shader.

The check for the effect type is only a safety mechanism. We've set this in our _init function, however it is possible for the user to change this in the UI.

Our p_render_data parameter gives us access to an object that holds data specific to the frame we're currently rendering. We're currently only interested in our render scene buffers, which provide us access to all the internal buffers used by the rendering engine. Note that we cast this to RenderSceneBuffersRD to expose the full API to this data.

Next we obtain our internal size which is the resolution of our 3D render buffers before they are upscaled (if applicable), upscaling happens after our post processes have run.

From our internal size we calculate our group size, see our local size in our template shader.

We also populate our push constant so our shader knows our size. Godot does not support structs here yet so we use a PackedFloat32Array to store this data into. Note that we have to pad this array with a 16 byte alignment. In other words, the length of our array needs to be a multiple of 4.

Now we loop through our views, this is in case we're using multiview rendering which is applicable for stereo rendering (XR). In most cases we will only have one view.

There is no performance benefit to use multiview for post processing here, handling the views separately like this will still enable the GPU to use parallelism if beneficial.

Next we obtain the color buffer for this view. This is the buffer into which our 3D scene has been rendered.

We then prepare a uniform set so we can communicate the color buffer to our shader.

Note the use of our UniformSetCacheRD cache which ensures we can check for our uniform set each frame. As our color buffer can change from frame to frame and our uniform cache will automatically clean up uniform sets when buffers are freed, this is the safe way to ensure we do not leak memory or use an outdated set.

Finally we build our compute list by binding our pipeline, binding our uniform set, pushing our push constant data, and calling dispatch for our groups.

With our compositor effect completed, we now need to add it to our compositor.

On our compositor we expand the compositor effects property and press Add Element.

Now we can add our compositor effect:

After selecting our PostProcessShader we need to set our user shader code:

With that all done, our output is in grayscale.

For a more advanced example of post effects, check out the Radial blur based sky rays example project created by Bastiaan Olij.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
@tool
extends CompositorEffect
class_name PostProcessShader
```

Example 2 (typescript):
```typescript
const template_shader: String = """
#version 450

// Invocations in the (x, y, z) dimension
layout(local_size_x = 8, local_size_y = 8, local_size_z = 1) in;

layout(rgba16f, set = 0, binding = 0) uniform image2D color_image;

// Our push constant
layout(push_constant, std430) uniform Params {
    vec2 raster_size;
    vec2 reserved;
} params;

// The code we want to execute in each invocation
void main() {
    ivec2 uv = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = ivec2(params.raster_size);

    if (uv.x >= size.x || uv.y >= size.y) {
        return;
    }

    vec4 color = imageLoad(color_image, uv);

    #COMPUTE_CODE

    imageStore(color_image, uv, color);
}
"""
```

Example 3 (swift):
```swift
@export_multiline var shader_code: String = "":
    set(value):
        mutex.lock()
        shader_code = value
        shader_is_dirty = true
        mutex.unlock()

var rd: RenderingDevice
var shader: RID
var pipeline: RID

var mutex: Mutex = Mutex.new()
var shader_is_dirty: bool = true
```

Example 4 (typescript):
```typescript
# Called when this resource is constructed.
func _init():
    effect_callback_type = EFFECT_CALLBACK_TYPE_POST_TRANSPARENT
    rd = RenderingServer.get_rendering_device()
```

---

## Fixing jitter, stutter and input lag — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/rendering/jitter_stutter.html

**Contents:**
- Fixing jitter, stutter and input lag
- What is jitter, stutter and input lag?
- Distinguishing between jitter and stutter
- Jitter
- Stutter
  - Windows
  - Linux
  - macOS
  - Android
  - iOS

Jitter and stutter are two different alterations to visible motion of objects on screen that may affect a game, even when running at full speed. These effects are mostly visible in games where the world moves at a constant speed in a fixed direction, like runners or platformers.

Input lag is unrelated to jitter and stutter, but is sometimes discussed alongside. Input lag refers to visible on-screen delay when performing actions with the mouse, keyboard, controller or touchscreen. It can be related to game code, engine code or external factors (such as hardware). Input lag is most noticeable in games that use the mouse to aim, such as first-person games. Input lag can't be completely eliminated, but it can be reduced in several ways.

A game running at a normal framerate without exhibiting any effect will appear smooth:

A game exhibiting jitter will shake constantly in a very subtle way:

Finally, a game exhibiting stutter will appear smooth, but appear to stop or roll back a frame every few seconds:

There can be many causes of jitter. The most typical one happens when the game physics frequency (usually 60 Hz) runs at a different resolution than the monitor refresh rate. Check whether your monitor refresh rate is different from 60 Hz.

Sometimes, only some objects appear to jitter (character or background). This happens when they are processed in different time sources (one is processed in the physics step while another is processed in the idle step).

This cause of jitter can be alleviated by enabling physics interpolation in the Project Settings. Physics interpolation will smooth out physics updates by interpolating the transforms of physics objects between physics frames. This way, the visual representation of physics objects will always look smooth no matter the framerate and physics tick rate.

Enabling physics interpolation has some caveats you should be aware of. For example, care should be taken when teleporting objects so that they don't visibly interpolate between the old position and new position when it's not intended. See the Physics Interpolation documentation for details.

Enabling physics interpolation will increase input lag for behavior that depends on the physics tick, such as player movement. In most games, this is generally preferable to jitter, but consider this carefully for games that operate on a fixed framerate (like fighting or rhythm games). This increase in input lag can be compensated by increasing the physics tick rate as described in the Input lag section.

Stutter may happen due to several different reasons. One reason is the game not being able to keep full framerate performance due to a CPU or GPU bottleneck. Solving this is game-specific and will require optimization.

Another common reason for stuttering is shader compilation stutter. This occurs when a shader needs to be compiled when a new material or particle effect is spawned for the first time in a game. This kind of stuttering generally only happens on the first playthrough, or after a graphics driver update when the shader cache is invalidated.

Since Godot 4.4, when using the Forward+ or Mobile renderers, the engine tries to avoid shader compilation stutter using an ubershader approach. For this approach to be most effective, care must be taken when designing scenes and resources so that Godot can gather as much information as possible when the scene/resource is loaded, as opposed as to when it's being drawn for the first time. See Reducing stutter from shader (pipeline) compilations for more information.

However, when using the Compatibility renderer, it is not possible to use this ubershader approach due to technical limitations in OpenGL. Therefore, to avoid shader compilation stutter in the Compatibility renderer, you need to spawn every mesh and visual effect in front of the camera for a single frame when the level is loading. This will ensure the shader is compiled when the level is loaded, as opposed to occurring during gameplay. This can be done behind solid 2D UI (such as a fullscreen ColorRect node) so that it's not visible to the player.

On platforms that support disabling V-Sync, stuttering can be made less noticeable by disabling V-Sync in the project settings. This will however cause tearing to appear, especially on monitors with low refresh rates. If your monitor supports it, consider enabling variable refresh rate (G-Sync/FreeSync) while leaving V-Sync enabled. This allows mitigating some forms of stuttering without introducing tearing. However, it will not help with large stutters, such as the ones caused by shader compilation stutter.

Forcing your graphics card to use the maximum performance profile can also help reduce stuttering, at the cost of increased GPU power draw.

Additionally, stutter may be induced by the underlying operating system. Here is some information regarding stutter on different OSes:

Windows is known to cause stutter in windowed games. This mostly depends on the hardware installed, drivers version and processes running in parallel (e.g. having many browser tabs open may cause stutter in a running game). To avoid this, Godot raises the game priority to "Above Normal". This helps considerably, but may not completely eliminate stutter.

Eliminating this completely requires giving your game full privileges to become "Time Critical", which is not advised. Some games may do it, but it is advised to learn to live with this problem, as it is common for Windows games and most users won't play games windowed (games that are played in a window, e.g. puzzle games, will usually not exhibit this problem anyway).

For fullscreen, Windows gives special priority to the game so stutter is no longer visible and very rare. This is how most games are played.

When using a mouse with a polling rate of 1,000 Hz or more, consider using a fully up-to-date Windows 11 installation which comes with fixes related to high CPU utilization with high polling rate mice. These fixes are not available in Windows 10 and older versions.

Games should use the Exclusive Fullscreen window mode, as opposed to Fullscreen which is designed to prevent Windows from automatically treating the window as if it was exclusive fullscreen.

Fullscreen is meant to be used by GUI applications that want to use per-pixel transparency without a risk of having it disabled by the OS. It achieves this by leaving a 1-pixel line at the bottom of the screen. By contrast, Exclusive Fullscreen uses the actual screen size and allows Windows to reduce jitter and input lag for fullscreen games.

Stutter may be visible on desktop Linux, but this is usually associated with different video drivers and compositors. Some compositors may also trigger this problem (e.g. KWin), so it is advised to try using a different one to rule it out as the cause. Some window managers such as KWin and Xfwm allow you to manually disable compositing, which can improve performance (at the cost of tearing).

There is no workaround for driver or compositor stuttering, other than reporting it as an issue to the driver or compositor developers. Stutter may be more present when playing in windowed mode as opposed to fullscreen, even with compositing disabled.

Feral GameMode can be used to automatically apply optimizations (such as forcing the GPU performance profile) when running specific processes.

Generally, macOS is stutter-free, although recently some bugs were reported when running on fullscreen (this is a macOS bug). If you have a machine exhibiting this behavior, please let us know.

Generally, Android is stutter and jitter-free because the running activity gets all the priority. That said, there may be problematic devices (older Kindle Fire is known to be one). If you see this problem on Android, please let us know.

iOS devices are generally stutter-free, but older devices running newer versions of the operating system may exhibit problems. This is generally unavoidable.

On platforms that support disabling V-Sync, input lag can be made less noticeable by disabling V-Sync in the project settings. This will however cause tearing to appear, especially on monitors with low refresh rates. It's suggested to make V-Sync available as an option for players to toggle.

When using the Forward+ or Mobile rendering methods, another way to reduce visual latency when V-Sync is enabled is to use double-buffered V-Sync instead of the default triple-buffered V-Sync. Since Godot 4.3, this can be achieved by reducing the Display > Window > V-Sync > Swapchain Image Count project setting to 2. The downside of using double buffering is that framerate will be less stable if the display refresh rate can't be reached due to a CPU or GPU bottleneck. For instance, on a 60 Hz display, if the framerate would normally drop to 55 FPS during gameplay with triple buffering, it will have to drop down to 30 FPS momentarily with double buffering (and then go back to 60 FPS when possible). As a result, double-buffered V-Sync is only recommended if you can consistently reach the display refresh rate on the target hardware.

Increasing the number of physics iterations per second can also reduce physics-induced input latency. This is especially noticeable when using physics interpolation (which improves smoothness but increases latency). To do so, set Physics > Common > Physics Ticks Per Second to a value higher than the default 60, or set Engine.physics_ticks_per_second at runtime in a script. Values that are a multiple of the monitor refresh rate (typically 60) work best when physics interpolation is disabled, as they will avoid jitter. This means values such as 120, 180 and 240 are good starting points. As a bonus, higher physics FPSes make tunneling and physics instability issues less likely to occur.

The downside of increasing physics FPS is that CPU usage will increase, which can lead to performance bottlenecks in games that have heavy physics simulation code. This can be alleviated by increasing physics FPS only in situations where low latency is critical, or by letting players adjust physics FPS to match their hardware. However, different physics FPS will lead to different outcomes in physics simulation, even when delta is consistently used in your game logic. This can give certain players an advantage over others. Therefore, allowing the player to change the physics FPS themselves should be avoided for competitive multiplayer games.

Lastly, you can disable input buffering on a per-rendered frame basis by calling Input.set_use_accumulated_input(false) in a script. This will make it so the _input() and _unhandled_input() functions in your scripts are called on every input, rather than accumulating inputs and waiting for a frame to be rendered. Disabling input accumulation will increase CPU usage, so it should be done with caution.

On any Godot project, you can use the --disable-vsync command line argument to forcibly disable V-Sync. Since Godot 4.2, --max-fps <fps> can also be used to set an FPS limit (0 is unlimited). These arguments can be used at the same time.

If your monitor supports it, consider enabling variable refresh rate (G-Sync/FreeSync) while leaving V-Sync enabled, then cap the framerate in the project settings to a slightly lower value than your monitor's maximum refresh rate as per this page. For example, on a 144 Hz monitor, you can set the project's framerate cap to 141. This may be counterintuitive at first, but capping the FPS below the maximum refresh rate range ensures that the OS never has to wait for vertical blanking to finish. This leads to similar input lag as V-Sync disabled with the same framerate cap (usually less than 1 ms greater), but without any tearing.

This can be done by changing the Application > Run > Max FPS project setting or assigning Engine.max_fps at runtime in a script.

On some platforms, you can also opt into a low-latency mode in the graphics driver options (such as the NVIDIA Control Panel on Windows). The Ultra setting will give you the lowest possible latency, at the cost of slightly lower average framerates. Forcing the GPU to use the maximum performance profile can also further reduce input lag, at the cost of higher power consumption (and resulting heat/fan noise).

Finally, make sure your monitor is running at its highest possible refresh rate in the OS' display settings.

Also, ensure that your mouse is configured to use its highest polling rate (typically 1,000 Hz for gaming mice, sometimes more). High USB polling rates can however result in high CPU usage, so 500 Hz may be a safer bet on low-end CPUs. If your mouse offers multiple DPI settings, consider also using the highest possible setting and reducing in-game sensitivity to reduce mouse latency.

On Linux when using X11, disabling compositing in window managers that allow it (such as KWin or Xfwm) can reduce input lag significantly.

If you are reporting a stutter or jitter problem (opening an issue) not caused by any of the above reasons, please specify very clearly all the information possible about device, operating system, driver versions, etc. This may help to better troubleshoot it.

If you are reporting input lag problems, please include a capture made with a high speed camera (such as your phone's slow motion video mode). The capture must have both the screen and the input device visible so that the number of frames between an input and the on-screen result can be counted. Also, make sure to mention your monitor's refresh rate and your input device's polling rate (especially for mice).

Also, make sure to use the correct term (jitter, stutter, input lag) based on the exhibited behavior. This will help understand your issue much faster. Provide a project that can be used to reproduce the issue, and if possible, include a screen capture demonstrating the bug.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## XR — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/index.html

**Contents:**
- XR
- Basic Tutorial
- Advanced topics
- Godot XR Tools

This section of the manual covers everything related to XR ( Virtual Reality and Augmented Reality).

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Setting up XR — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html

**Contents:**
- Setting up XR
- Introduction to the XR system in Godot
- Which Renderer to use
- OpenXR
- Setting up the XR scene
- User-contributed notes

Godot provides a modular XR system that abstracts many of the different XR platform specifics away from the user. At the core sits the XRServer which acts as a central interface to the XR system that allows users to discover interfaces and interact with the components of the XR system.

Each supported XR platform is implemented as an XRInterface. A list of supported platforms can be found on the list of features page here. Supported interfaces register themselves with the XRServer and can be queried with the find_interface method on the XRServer. When the desired interface is found it can be initialized by calling initialize on the interface.

A registered interface means nothing more than that the interface is available, if the interface is not supported by the host system, initialization may fail and return false. This can have many reasons and sadly the reasons differ from platform to platform. It can be because the user hasn't installed the required software, or that the user simply hasn't plugged in their headset. You as a developer must thus react properly on an interface failing to initialize.

Due to the special requirements for output in XR, especially for head mounted devices that supply different images to each eye, the XRServer in Godot will override various features in the rendering system. For stand-alone devices this means the final output is handled by the XRInterface and Godot's usual output system is disabled. For desktop XR devices that work as a second screen it is possible to dedicate a separate Viewport to handle the XR output, leaving the main Godot window available for displaying alternative content.

Note that only one interface can be responsible for handling the output to an XR device, this is known as the primary interface and by default will be the first interface that is initialized. Godot currently thus only supports implementations with a single headset. It is possible, but increasingly uncommon, to have a secondary interface, for example to add tracking to an otherwise 3DOF only device.

There are three XR specific node types that you will find in nearly all XR applications:

XROrigin3D represents, for all intents and purposes, the center point of your play space. That is an oversimplified statement but we'll go into more detail later. All objects tracked in physical space by the XR platform are positioned in relation to this point.

XRCamera3D represents the (stereo) camera that is used when rendering output for the XR device. The positioning of this node is controlled by the XR system and updated automatically using the tracking information provided by the XR platform.

XRController3D represents a controller used by the player, commonly there are two, one held in each hand. These nodes give access to various states on these controllers and send out signals when the player presses buttons on them. The positioning of this node is controlled by the XR system and updated automatically using the tracking information provided by the XR platform.

There are other XR related nodes and there is much more to say about these three nodes, but we'll get into that later on.

Godot has 3 renderer options for projects: Compatibility, Mobile, and Forward+. The current recommendation is to use the Mobile renderer for any desktop VR project, and use the Compatibility renderer for any project running on a standalone headset like the Meta Quest 3. XR projects will run with the Forward+ renderer, but it isn't well optimized for XR right now compared to the other two.

OpenXR is a new industry standard that allows different XR platforms to present themselves through a standardised API to XR applications. This standard is an open standard maintained by the Khronos Group and thus aligns very well with Godot's interests.

The Vulkan implementation of OpenXR is closely integrated with Vulkan, taking over part of the Vulkan system. This requires tight integration of certain core graphics features in the Vulkan renderer which are needed before the XR system is setup. This was one of the main deciding factors to include OpenXR as a core interface.

This also means OpenXR needs to be enabled when Godot starts in order to set things up correctly. Check the Enabled setting in your project settings under XR > OpenXR.

You can find several other settings related to OpenXR here as well. These can't be changed while your application is running. The default settings will get us started, but for more information on what's here see OpenXR Settings.

You'll also need to go to XR > Shaders in the project settings and check the Enabled box to enable them. Once you've done that click the Save & Restart button.

Many post process effects have not yet been updated to support stereoscopic rendering. Using these will have adverse effects.

Every XR application needs at least an XROrigin3D and an XRCamera3D node. Most will have two XRController3D, one for the left hand and one for the right. Keep in mind that the camera and controller nodes should be children of the origin node. Add these nodes to a new scene and rename the controller nodes to LeftHand and RightHand, your scene should look something like this:

The warning icons are expected and should go away after you configure the controllers. Select the left hand and set it up as follows:

Right now all these nodes are on the floor, they will be positioned correctly in runtime. To help during development, it can be helpful to move the camera upwards so its y is set to 1.7, and move the controller nodes to -0.5, 1.0, -0.5 and 0.5, 1.0, -0.5 for respectively the left and right hand.

Next we need to add a script to our root node. Add the following code into this script:

This code fragment assumes we are using OpenXR, if you wish to use any of the other interfaces you can change the find_interface call.

As you can see in the code snippet above, we turn off v-sync. When using OpenXR you are outputting the rendering results to an HMD that often requires us to run at 90Hz or higher. If your monitor is a 60hz monitor and v-sync is turned on, you will limit the output to 60 frames per second.

XR interfaces like OpenXR perform their own sync.

Also note that by default the physics engine runs at 60Hz as well and this can result in choppy physics. You should set Engine.physics_ticks_per_second to a higher value.

If you run your project at this point in time, everything will work but you will be in a dark world. So to finish off our starting point add a DirectionalLight3D and a WorldEnvironment node to your scene. You may wish to also add a mesh instance as a child to each controller node just to temporarily visualise them. Make sure you configure a sky in your world environment.

Now run your project, you should be floating somewhere in space and be able to look around.

While traditional level switching can definitely be used with XR applications, where this scene setup is repeated in each level, most find it easier to set this up once and loading levels as a subscene. If you do switch scenes and replicate the XR setup in each one, do make sure you do not run initialize multiple times. The effect can be unpredictable depending on the XR interface used.

For the rest of this basic tutorial series we will create a game that uses a single scene.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node3D

var xr_interface: XRInterface

func _ready():
    xr_interface = XRServer.find_interface("OpenXR")
    if xr_interface and xr_interface.is_initialized():
        print("OpenXR initialized successfully")

        # Turn off v-sync!
        DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)

        # Change our main viewport to output to the HMD
        get_viewport().use_xr = true
    else:
        print("OpenXR not initialized, please check if your headset is connected")
```

Example 2 (swift):
```swift
using Godot;

public partial class MyNode3D : Node3D
{
    private XRInterface _xrInterface;

    public override void _Ready()
    {
        _xrInterface = XRServer.FindInterface("OpenXR");
        if(_xrInterface != null && _xrInterface.IsInitialized())
        {
            GD.Print("OpenXR initialized successfully");

            // Turn off v-sync!
            DisplayServer.WindowSetVsyncMode(DisplayServer.VSyncMode.Disabled);

            // Change our main viewport to output to the HMD
            GetViewport().UseXR = true;
        }
        else
        {
            GD.Print("OpenXR not initialized, please check if your headset is connected");
        }
    }
}
```

---

## Where to go from here — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/xr_next_steps.html

**Contents:**
- Where to go from here
- XR Toolkits
- User-contributed notes

Now that we have the basics covered there are several options to look at for your XR game dev journey:

You can take a look at the Advanced topics section.

You can look at a number of XR demos here.

You can find 3rd party tutorials on our Tutorials and resources page.

There are various XR toolkits available that implement more complex XR logic ready for you to use. We have a small introduction to Godot XR Tools that you can look at, a toolkit developed by core contributors of Godot.

There are more toolkits available for Godot:

Godot XR handtracking toolkit (GDScript)

Godot XR Kit (GDScript)

Godot XR Tools (GDScript)

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## A better XR start script — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/a_better_xr_start_script.html

**Contents:**
- A better XR start script
- Signals for our script
- Variables for our script
- Our updated ready function
- On session begun
- On visible state
- On focussed state
- On stopping state
- On pose recentered
- User-contributed notes

In Setting up XR we introduced a startup script that initialises our setup which we used as our script on our main node. This script performs the minimum steps required for any given interface.

When using OpenXR there are a number of improvements we should do here. For this we've created a more elaborate starting script. You will find these used in our demo projects.

Alternatively, if you are using XR Tools (see Introducing XR tools) it contains a version of this script updated with some features related to XR tools.

Below we will detail out the script used in our demos and explain the parts that are added.

We are introducing 3 signals to our script so that our game can add further logic:

focus_lost is emitted when the player takes off their headset or when the player enters the menu system of the headset.

focus_gained is emitted when the player puts their headset back on or exits the menu system and returns to the game.

pose_recentered is emitted when the headset requests the player's position to be reset.

Our game should react accordingly to these signals.

We introduce a few new variables to our script as well:

maximum_refresh_rate will control the headsets refresh rate if this is supported by the headset.

xr_interface holds a reference to our XR interface, this already existed but we now type it to get full access to our XRInterface API.

xr_is_focussed will be set to true whenever our game has focus.

We add a few things to the ready function.

If we're using the mobile or forward+ renderer we set the viewport's vrs_mode to VRS_XR. On platforms that support this, this will enable foveated rendering.

If we're using the compatibility renderer, we check if the OpenXR foveated rendering settings are configured and if not, we output a warning. See OpenXR Settings for further details.

We hook up a number of signals that will be emitted by the XRInterface. We'll provide more detail about these signals as we implement them.

We also quit our application if we couldn't successfully initialise OpenXR. Now this can be a choice. If you are making a mixed mode game you setup the VR mode of your game on success, and setup the non-VR mode of your game on failure. However, when running a VR only application on a standalone headset, it is nicer to exit on failure than to hang the system.

This signal is emitted by OpenXR when our session is setup. This means the headset has run through setting everything up and is ready to begin receiving content from us. Only at this time various information is properly available.

The main thing we do here is to check our headset's refresh rate. We also check the available refresh rates reported by the XR runtime to determine if we want to set our headset to a higher refresh rate.

Finally we match our physics update rate to our headset update rate. Godot runs at a physics update rate of 60 updates per second by default while headsets run at a minimum of 72, and for modern headsets often up to 144 frames per second. Not matching the physics update rate will cause stuttering as frames are rendered without objects moving.

This signal is emitted by OpenXR when our game becomes visible but is not focused. This is a bit of a weird description in OpenXR but it basically means that our game has just started and we're about to switch to the focused state next, that the user has opened a system menu or the user has just took their headset off.

On receiving this signal we'll update our focused state, we'll change the process mode of our node to disabled which will pause processing on this node and its children, and emit our focus_lost signal.

If you've added this script to your root node, this means your game will automatically pause when required. If you haven't, you can connect a method to the signal that performs additional changes.

While your game is in visible state because the user has opened a system menu, Godot will keep rendering frames and head tracking will remain active so your game will remain visible in the background. However controller and hand tracking will be disabled until the user exits the system menu.

This signal is emitted by OpenXR when our game gets focus. This is done at the completion of our startup, but it can also be emitted when the user exits a system menu, or put their headset back on.

Note also that when your game starts while the user is not wearing their headset, the game stays in 'visible' state until the user puts their headset on.

It is thus important to keep your game paused while in visible mode. If you don't the game will keep on running while your user isn't interacting with your game. Also when the game returns to the focused mode, suddenly all controller and hand tracking is re-enabled and could have game breaking consequences if you do not react to this accordingly. Be sure to test this behavior in your game!

While handling our signal we will update the focuses state, unpause our node and emit our focus_gained signal.

This signal is emitted by OpenXR when we enter our stop state. There are some differences between platforms when this happens. On some platforms this is only emitted when the game is being closed. But on other platforms this will also be emitted every time the player takes off their headset.

For now this method is only a place holder.

This signal is emitted by OpenXR when the user requests their view to be recentered. Basically this communicates to your game that the user is now facing forward and you should re-orient the player so they are facing forward in the virtual world.

As doing so is dependent on your game, your game needs to react accordingly.

All we do here is emit the pose_recentered signal. You can connect to this signal and implement the actual recenter code. Often it is enough to call center_on_hmd().

And that finished our script. It was written so that it can be re-used over multiple projects. Just add it as the script on your main node (and extend it if needed) or add it on a child node specific for this script.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node3D

signal focus_lost
signal focus_gained
signal pose_recentered

...
```

Example 2 (json):
```json
using Godot;

public partial class MyNode3D : Node3D
{
    [Signal]
    public delegate void FocusLostEventHandler();

    [Signal]
    public delegate void FocusGainedEventHandler();

    [Signal]
    public delegate void PoseRecenteredEventHandler();

...
```

Example 3 (swift):
```swift
...

@export var maximum_refresh_rate : int = 90

var xr_interface : OpenXRInterface
var xr_is_focussed = false

...
```

Example 4 (csharp):
```csharp
...

    [Export]
    public int MaximumRefreshRate { get; set; } = 90;

    private OpenXRInterface _xrInterface;

    private bool _xrIsFocused;

...
```

---

## AR / Passthrough — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/ar_passthrough.html

**Contents:**
- AR / Passthrough
- Environment blend modes
- Configuring your background
- OpenXR specific
- Putting it together
- Shadow to opacity
- User-contributed notes

Augmented Reality is supported through various methods depending on the capabilities of the hardware.

Headsets such as the Magic Leap and glasses such as TiltFive show the rendered result on see-through displays allowing the user to see the real world.

Headsets such as the Quest, HTC Elite, and Lynx R1 implement this through a technique called video passthrough, where cameras record the real world and these images are used as the background on top of which our rendered result is used.

Passthrough is implemented very differently across platforms.

In Godot 4.3 we have implemented a unified approach that is explained on this help page so you don't need to worry about these differences, the XRInterface implementation is now responsible for applying the correct platform-dependent method [1].

For headsets such as the Meta Quest and HTC Elite you will need to use the OpenXR vendors plugin v3.0.0 or later to enable video passthrough.

For backwards compatibility the old API for passthrough is still available but it is recommended to follow the new instructions below.

The way we configure VR or AR functionality is through setting the environment blend mode. This mode determines how the (real world) environment is blended with the virtual world.

XR_ENV_BLEND_MODE_OPAQUE

The rendered image is opaque, we do not see the real world. We're in VR mode. This will turn off passthrough if video-passthrough is used.

XR_ENV_BLEND_MODE_ADDITIVE

The rendered image is added to the real world and will look semi transparent. This mode is generally used with see-through devices that are unable to obscure the real world. This will turn on passthrough if video-passthrough is used.

XR_ENV_BLEND_MODE_ALPHA_BLEND

The rendered image is alpha blended with the real world. On see-through devices that support this, the alpha will control the translucency of the optics. On video-passthrough devices alpha blending is applied with the video image. passthrough will also be enabled if applicable.

You can set the environment blend mode for your application through the environment_blend_mode property of the XRInterface instance.

You can query the supported blend modes on the hardware using the get_supported_environment_blend_modes property on the same instance.

When setting the blend mode to XR_ENV_BLEND_MODE_ALPHA_BLEND you must set the transparent_bg property on Viewport to true. When using the XR_ENV_BLEND_MODE_ADDITIVE blend mode you should set your background color to black.

Either solution will result in the background rendering not contributing to lighting. It is thus also recommended you adjust your environment settings accordingly and ensure there is adequate ambient light set to illuminate your scene.

Some AR SDKs do provide ambient lighting information or even provide a full radiance map to allow for real world reflections in your virtual objects. The core Godot XR functionality doesn't currently have support for this, however this functionality can be exposed through plugins.

In OpenXR you can configure the default blend mode you want to use. Godot will select this blend mode at startup if available. If not available Godot will default to the first supported blend mode provided by the XR runtime.

For passthrough devices OpenXR requires additional settings to be configured. These settings are platform-dependent and provided through the OpenXR vendors plugin.

For example, these are the settings required on Meta Quest:

The Passthrough setting defines whether passthrough is supported or even required.

The Boundary Mode allows you to define whether the guardian is needed, disabling this fully requires passthrough to be enabled at all times.

Putting the above together we can use the following code as a base:

Shadow to opacity is a render mode for Godot spatial shaders that was introduced in Godot 3 specifically for AR. It is a special render mode where the more a surface is in shadow, the more opaque the surface becomes. When a surface is fully lit, the surface becomes fully transparent and thus shows the real world.

However the surface is rendered during the opaque state effectively. This has two consequences:

As both the depth buffer and color buffer are written to, we occlude any geometry behind our surface even when fully transparent.

As we are making the surface opaque if in shadow, we can have virtual objects cast shadows on real world objects [2].

Image showing shadow to opacity being used to show the user's desk.

This enabled the following use cases:

You can render a box mesh around a real world table, this ensures the table remains visible even if a virtual object is placed underneath it. The virtual object will be correctly occluded. Placing a virtual object on top of the real world table, will result in a shadow being cast on the table.

You can use a shader with this render mode when render a hand mesh using the hand tracking functionality, and ensure your hands properly occlude virtual objects.

The following shader code is a good base for this functionality:

Restrictions may apply depending on XR interface implementation.

This feature is still being perfected.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
@onready var viewport : Viewport = get_viewport()
@onready var environment : Environment = $WorldEnvironment.environment

func switch_to_ar() -> bool:
    var xr_interface: XRInterface = XRServer.primary_interface
    if xr_interface:
        var modes = xr_interface.get_supported_environment_blend_modes()
        if XRInterface.XR_ENV_BLEND_MODE_ALPHA_BLEND in modes:
            xr_interface.environment_blend_mode = XRInterface.XR_ENV_BLEND_MODE_ALPHA_BLEND
            viewport.transparent_bg = true
        elif XRInterface.XR_ENV_BLEND_MODE_ADDITIVE in modes:
            xr_interface.environment_blend_mode = XRInterface.XR_ENV_BLEND_MODE_ADDITIVE
            viewport.transparent_bg = false
    else:
        return false

    environment.background_mode = Environment.BG_COLOR
    environment.background_color = Color(0.0, 0.0, 0.0, 0.0)
    environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    return true

func switch_to_vr() -> bool:
    var xr_interface: XRInterface = XRServer.primary_interface
    if xr_interface:
        var modes = xr_interface.get_supported_environment_blend_modes()
        if XRInterface.XR_ENV_BLEND_MODE_OPAQUE in modes:
            xr_interface.environment_blend_mode = XRInterface.XR_ENV_BLEND_MODE_OPAQUE
        else:
            return false

    viewport.transparent_bg = false
    environment.background_mode = Environment.BG_SKY
    environment.ambient_light_source = Environment.AMBIENT_SOURCE_BG
    return true
```

Example 2 (cpp):
```cpp
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, shadow_to_opacity;

void fragment() {
    ALBEDO = vec3(0.0, 0.0, 0.0);
}
```

---

## Room scale in XR — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/xr_room_scale.html

**Contents:**
- Room scale in XR
- Origin centric solution
- Step 1
- Step 2
- Step 3
- Character body centric solution
- Step 1
- Step 2
- Step 3
- When the player walks to somewhere they shouldn't

One of the staples of XR projects is the ability to walk around freely in a large space. This space is often constrained by the room the player is physically in with tracking sensors placed within this space. With the advent of inside out tracking however ever larger play spaces are possible.

As a developer this introduces a number of interesting challenges. In this document we will look at a number of the challenges you may face and outline some solutions. We'll discuss the issues and challenges for seated XR games in another document.

Often developers sit behind their desk while building the foundation to their game. In this mode the issues with developing for room scale don't show themselves until it is too late. The advice here is to start testing while standing up and walking around as early as possible. Once you are happy your foundation is solid, you can develop in comfort while remaining seated.

In traditional first person games a player is represented by a CharacterBody3D node. This node is moved by processing traditional controller, mouse or keyboard input. A camera is attached to this node at a location roughly where the player's head will be.

Applying this model to the XR setup, we add an XROrigin3D node as a child of the character body, and add an XRCamera3D as a child of the origin node. At face value this seems to work. However, upon closer examination this model does not take into account that there are two forms of movement in XR. The movement through controller input, and the physical movement of the player in the real world.

As a result, the origin node does not represent the position of the player. It represents the center, or start of, the tracking space in which the player can physically move. As the player moves around their room this movement is represented through the tracking of the player's headset. In game this translates to the camera node's position being updated accordingly. For all intents and purposes, we are tracking a disembodied head. Unless body tracking is available, we have no knowledge of the position or orientation of the player's body.

The first problem this causes is fairly obvious. When the player moves with controller input, we can use the same approach in normal games and move the player in a forward direction. However the player isn't where we think they are and as we move forward we're checking collisions in the wrong location.

The second problem really shows itself when the player walks further away from the center of the tracking space and uses controller input to turn. If we rotate our character body, the player will be moved around the room in a circular fashion.

If we fix the above issues, we will find a third issue. When the path for the player is blocked in the virtual world, the player can still physically move forward.

We will look at solving the first two problem with two separate solutions, and then discuss dealing with the third.

Looking at the first approach for solving this we are going to change our structure. This is the approach currently implemented in XR Tools.

In this setup we mark the character body as top level so it does not move with the origin.

We also have a helper node that tells us where our neck joint is in relation to our camera. We use this to determine where our body center is.

Processing our character movement is now done in three steps.

The Origin centric movement demo contains a more elaborate example of the technique described below.

In the first step we're going to process the physical movement of the player. We determine where the player is right now, and attempt to move our character body there.

Note that we're returning true from our _process_on_physical_movement function when we couldn't move our player all the way.

The second step is to handle rotation of the player as a result of user input.

As the input used can differ based on your needs we are simply calling the function _get_rotational_input. This function should obtain the necessary input and return the rotational speed in radians per second.

For our example we are going to keep this simple and straight forward. We are not going to worry about comfort features such as snap turning and applying a vignette. We highly recommend implementing such comfort features.

We've added the call for processing our rotation to our physics process but we are only executing this if we were able to move our player fully. This means that if the player moves somewhere they shouldn't, we don't process further movement.

The third and final step is moving the player forwards, backwards or sideways as a result of user input.

Just like with the rotation the inputs differ from project to project so we are simply calling the function _get_movement_input. This function should obtain the necessary input and return a directional vector scaled to the required velocity.

Just like with rotation we're keeping it simple. Here too it is advisable to look at adding comfort settings.

In this setup we are going to keep our character body as our root node and as such is easier to combine with traditional game mechanics.

Here we have a standard character body with collision shape, and our XR origin node and camera as normal children. We also have our neck helper node.

Processing our character movement is done in the same three steps but implemented slightly differently.

The Character centric movement demo contains a more elaborate example of the technique described below.

In this approach step 1 is where all the magic happens. Just like with our previous approach we will be applying our physical movement to the character body, but we will counter that movement on the origin node.

This will ensure that the player's location stays in sync with the character body's location.

In essence the code above will move the character body to where the player is, and then move the origin node back in equal amounts. The result is that the player stays centered above the character body.

We start with applying the rotation. The character body should be facing where the player was looking the previous frame. We calculate our camera orientation in the space of the character body. We can now calculate the angle by which the player has rotated their head. We rotate our character body by the same amount so our character body faces the same direction as the player. And then we reverse the rotation on the origin node so the camera ends up aligned with the player again.

For the movement we do much the same. The character body should be where the player was standing the previous frame. We calculate by how much the player has moved from this location. Then we attempt to move the character body to this location.

As the player may hit a collision body and be stopped, we only move the origin point back by the amount we actually moved the character body. The player may thus move away from this location but that will be reflected in the positioning of the player.

As with our previous solution we return true if this is the case.

In this step we again apply the rotation based on controller input. However in this case the code is nearly identical to how one would implement this in a normal first person game.

As the input used can differ based on your needs we are simply calling the function _get_rotational_input. This function should obtain the necessary input and return the rotational speed in radians per second.

For step three we again apply the movement based on controller input. However just like at step 2, we can now implement this as we would in a normal first person game.

Just like with the rotation the inputs differ from project to project so we are simply calling the function _get_movement_input. This function should obtain the necessary input and return a directional vector scaled to the required velocity.

Think of a situation where the player is outside a locked room. You don't want the player to go into that room until the door is unlocked. You also don't want the player to see what is in this room.

The logic for moving the player through controller input nicely prevents this. The player encounters a static body, and the code prevents the player from moving into the room.

However with XR, nothing is preventing the player from taking a real step forward.

With both the approaches worked out up above we will prevent the character body from moving where the player can't go. As the player has physically moved to this location, the camera will now have moved into the room.

The logical solution would be to prevent the movement altogether and adjust the placement of the XR origin point so the player stays outside of the room.

The problem with this approach is that physical movement is now not replicated in the virtual space. This will cause nausea for the player.

What many XR games do instead, is to measure the distance between where the player physically is, and where the player's virtual body has been left behind. As this distance increases, usually to a distance of a few centimeters, the screen slowly blacks out.

Our solutions up above would allow us to add this logic into the code at the end of step 1.

Further improvements to the code presented could be:

allowing controller input as long as this distance is still small,

still applying gravity to the player even when controller input is disabled.

The movement demos in our demo repository contain an example of blacking out the screen when a user walks into restricted areas.

The above provides two good options as starting points for implementing room scale XR games.

A few more things that are worth pointing out that you will likely want to implement:

The height of the camera can be used to detect whether the player is standing up, crouching, jumping or lying down. You can adjust the size and orientation of the collision shape accordingly. Extra bonus points for adding multiple collision shapes so the head and body have their own, more accurately sized, shapes.

When a scene first loads, the player may be far away from the center of the tracking space. This could result in the player spawning into a different room than our origin point. The game will now attempt, and fail, to move the player body from the starting point to where the player is standing. You should implement a reset function that moves the origin point so the player is in the correct starting position.

Both of the above improvements require the player to be ready and standing up straight. There is no guarantee as the player may still be putting their headset on.

Many games, including XR Tools, solve this by introducing an intro screen or loading screen where the player must press a button when they are ready. This starting environment is often a large location where the positioning of the player has little impact on what the player sees. When the player is ready, and presses the button, this is the moment you record the position and height of the camera.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
func _process_on_physical_movement(delta):
  # Remember our current velocity, we'll apply that later
  var current_velocity = $CharacterBody3D.velocity

  # Remember where our player body currently is
  var org_player_body: Vector3 = $CharacterBody3D.global_transform.origin

  # Determine where our player body should be
  var player_body_location: Vector3 = $XRCamera3D.transform * $XRCamera3D/Neck.transform.origin
  player_body_location.y = 0.0
  player_body_location = global_transform * player_body_location

  # Attempt to move our character
  $CharacterBody3D.velocity = (player_body_location - org_player_body) / delta
  $CharacterBody3D.move_and_slide()

  # Set back to our current value
  $CharacterBody3D.velocity = current_velocity

  # Check if we managed to move all the way, ignoring height change
  var movement_left = player_body_location - $CharacterBody3D.global_transform.origin
  movement_left.y = 0.0
  if (movement_left).length() > 0.01:
    # We'll talk more about what we'll do here later on
    return true
  else:
    return false

func _physics_process(delta):
  var is_colliding = _process_on_physical_movement(delta)
```

Example 2 (swift):
```swift
func _get_rotational_input() -> float:
  # Implement this function to return rotation in radians per second.
  return 0.0

func _copy_player_rotation_to_character_body():
  # We only copy our forward direction to our character body, we ignore tilt
  var camera_forward: Vector3 = -$XRCamera3D.global_transform.basis.z
  var body_forward: Vector3 = Vector3(camera_forward.x, 0.0, camera_forward.z)

  $CharacterBody3D.global_transform.basis = Basis.looking_at(body_forward, Vector3.UP)

func _process_rotation_on_input(delta):
  var t1 := Transform3D()
  var t2 := Transform3D()
  var rot := Transform3D()

  # We are going to rotate the origin around the player
  var player_position = $CharacterBody3D.global_transform.origin - global_transform.origin

  t1.origin = -player_position
  t2.origin = player_position
  rot = rot.rotated(Vector3(0.0, 1.0, 0.0), _get_rotational_input() * delta)
  global_transform = (global_transform * t2 * rot * t1).orthonormalized()

  # Now ensure our player body is facing the correct way as well
  _copy_player_rotation_to_character_body()

func _physics_process(delta):
  var is_colliding = _process_on_physical_movement(delta)
  if !is_colliding:
    _process_rotation_on_input(delta)
```

Example 3 (swift):
```swift
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _get_movement_input() -> Vector2:
  # Implement this to return requested directional movement in meters per second.
  return Vector2()

func _process_movement_on_input(delta):
  # Remember where our player body currently is
  var org_player_body: Vector3 = $CharacterBody3D.global_transform.origin

  # We start with applying gravity
  $CharacterBody3D.velocity.y -= gravity * delta

  # Now we add in our movement
  var input: Vector2 = _get_movement_input()
  var movement: Vector3 = ($CharacterBody3D.global_transform.basis * Vector3(input.x, 0, input.y))
  $CharacterBody3D.velocity.x = movement.x
  $CharacterBody3D.velocity.z = movement.z

  # Attempt to move our player
  $CharacterBody3D.move_and_slide()

  # And now apply the actual movement to our origin
  global_transform.origin += $CharacterBody3D.global_transform.origin - org_player_body

func _physics_process(delta):
  var is_colliding = _process_on_physical_movement(delta)
  if !is_colliding:
    _process_rotation_on_input(delta)
    _process_movement_on_input(delta)
```

Example 4 (swift):
```swift
# Helper variables to keep our code readable
@onready var origin_node = $XROrigin3D
@onready var camera_node = $XROrigin3D/XRCamera3D
@onready var neck_position_node = $XROrigin3D/XRCamera3D/Neck

func _process_on_physical_movement(delta) -> bool:
  # Remember our current velocity, we'll apply that later
  var current_velocity = velocity

  # Start by rotating the player to face the same way our real player is
  var camera_basis: Basis = origin_node.transform.basis * camera_node.transform.basis
  var forward: Vector2 = Vector2(camera_basis.z.x, camera_basis.z.z)
  var angle: float = forward.angle_to(Vector2(0.0, 1.0))

  # Rotate our character body
  transform.basis = transform.basis.rotated(Vector3.UP, angle)

  # Reverse this rotation our origin node
  origin_node.transform = Transform3D().rotated(Vector3.UP, -angle) * origin_node.transform

  # Now apply movement, first move our player body to the right location
  var org_player_body: Vector3 = global_transform.origin
  var player_body_location: Vector3 = origin_node.transform * camera_node.transform * neck_position_node.transform.origin
  player_body_location.y = 0.0
  player_body_location = global_transform * player_body_location

  velocity = (player_body_location - org_player_body) / delta
  move_and_slide()

  # Now move our XROrigin back
  var delta_movement = global_transform.origin - org_player_body
  origin_node.global_transform.origin -= delta_movement

  # Return our value
  velocity = current_velocity

  if (player_body_location - global_transform.origin).length() > 0.01:
    # We'll talk more about what we'll do here later on
    return true
  else:
    return false

func _physics_process(delta):
  var is_colliding = _process_on_physical_movement(delta)
```

---

## OpenXR Settings — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/openxr_settings.html

**Contents:**
- OpenXR Settings
- General settings
  - Enabled
  - Default Action Map
  - Form Factor
  - View Configuration
  - Reference Space
    - Local
    - Stage
    - Local Floor

OpenXR has its own set of settings that are applied when OpenXR starts. While it is possible for OpenXR extensions implemented through Godot plugins to add additional settings, we will only discuss the settings in the core of Godot here.

This setting enables the OpenXR module when Godot starts. This is required when the Vulkan backend is used. For other backends you can enable OpenXR at any time by calling initialize on the OpenXRInterface.

This also needs to be enabled to get access to the action map editor.

You can use the --xr-mode on command line switch to force this to on.

This specifies the path of the action map file that OpenXR will load and communicate to the XR Runtime.

This specifies whether your game is designed for:

Head Mounted devices such as a Meta Quest, Valve Index, or Magic Leap,

Handheld devices such as phones.

If the device on which you run your game does not match the selection here, OpenXR will fail to initialise.

This specifies the view configuration your game is designed for:

Mono, your game provides a single image output. E.g. phone based AR;

Stereo, your game provides stereo image output. E.g. head mounted devices.

If the device on which you run your game does not match the selection here, OpenXR will fail to initialise.

OpenXR has additional view configurations for very specific devices that Godot doesn't support yet. For instance, Varjo headsets have a quad view configuration that outputs two sets of stereo images. These may be supported in the near future.

Within XR all elements like the player's head and hands are tracked within a tracking volume. At the base of this tracking volume is our origin point, which maps our virtual space to the real space. There are however different scenarios that place this point in different locations, depending on the XR system used. In OpenXR these scenarios are well defined and selected by setting a reference space.

The local reference space places our origin point at the player's head by default. Some XR runtimes will do this each time your game starts, others will make the position persist over sessions.

This reference space however does not prevent the user from walking away so you will need to detect if the user does so if you wish to prevent the user from leaving the vehicle they are controlling, which could potentially be game breaking.

This reference space is the best option for games like flight simulators or racing simulators where we want to place the XROrigin3D node where the player's head should be.

When the user enacts the recenter option on their headset, the method of which is different per XR runtime, the XR runtime will move the XRCamera3D to the XROrigin3D node. The OpenXRInterface will also emit the pose_recentered signal so your game can react accordingly.

Any other XR tracked elements such as controllers or anchors will also be adjusted accordingly.

You should not call center_on_hmd when using this reference space.

The stage reference space is our default reference space and places our origin point at the center of our play space. For XR runtimes that allow you to draw out a guardian boundary this location and its orientation is often set by the user. Other XR runtimes may decide on the placement of this point by other means. It is however a stationary point in the real world.

This reference space is the best option for room scale games where the user is expected to walk around a larger space, or for games where there is a need to switch between game modes. See Room Scale for more information.

When the user enacts the recenter option on their headset, the method of which is different per XR runtime, the XR runtime will not change the origin point. The OpenXRInterface will emit the pose_recentered signal and it is up to the game to react appropriately. Not doing so will prevent your game from being accepted on various stores.

In Godot you can do this by calling the center_on_hmd function on the XRServer:

Calling XRServer.center_on_hmd(XRServer.RESET_BUT_KEEP_TILT, false) will move the XRCamera3D node to the XROrigin3D node similar to the Local reference space.

Calling XRServer.center_on_hmd(XRServer.RESET_BUT_KEEP_TILT, true) will move the XRCamera3D node above the XROrigin3D node keeping the player's height, similar to the Local Floor reference space.

Any other XR tracked elements such as controllers or anchors will also be adjusted accordingly.

The local floor reference space is similar to the local reference space as it positions the origin point where the player is. In this mode however the height of the player is kept. Same as with the local reference space, some XR runtimes will persist this location over sessions.

It is thus not guaranteed the player will be standing on the origin point, the only guarantee is that they were standing there when the user last recentered. The player is thus also free to walk away.

This reference space is the best option of games where the user is expected to stand in the same location or for AR type games where the user's interface elements are bound to the origin node and are quickly placed at the player's location on recenter.

When the user enacts the recenter option on their headset, the method of which is different per XR runtime, the XR runtime will move the XRCamera3D above the XROrigin3D node but keeping the player's height. The OpenXRInterface will also emit the pose_recentered signal so your game can react accordingly.

Be careful using this mode in combination with virtual movement of the player. The user recentering in this scenario can be unpredictable unless you counter the move when handling the recenter signal. This can even be game breaking as the effect in this scenario would be the player teleporting to whatever abstract location the origin point was placed at during virtual movement, including the ability for players teleporting into locations that should be off limits. It is better to use the Stage mode in this scenario and limit resetting to orientation only when a pose_recentered signal is received.

Any other XR tracked elements such as controllers or anchors will also be adjusted accordingly.

You should not call center_on_hmd when using this reference space.

The environment blend mode defines how our rendered output is blended into "the real world" provided this is supported by the headset.

Opaque means our output obscures the real world, we are in VR mode.

Additive means our output is added to the real world, this is an AR mode where optics do not allow us to fully obscure the real world (e.g. Hololens),

Alpha means our output is blended with the real world using the alpha output (viewport should have transparent background enabled), this is an AR mode where optics can fully obscure the real world (Magic Leap, all pass through devices, etc.).

If a mode is selected that is not supported by the headset, the first available mode will be selected.

Some OpenXR devices have separate systems for enabling/disabling passthrough. From Godot 4.3 onwards selecting the alpha blend mode will also perform these extra steps. This does require the latest vendor plugin to be installed.

Sets the foveation level used when rendering provided this feature is supported by the hardware used. Foveation is a technique where the further away from the center of the viewport we render content, the lower resolution we render at. Most XR runtimes only support fixed foveation, but some will take eye tracking into account and use the focal point for this effect.

The higher the level, the better the performance gains, but also the more reduction in quality there is in the user's peripheral vision.

Compatibility renderer only, for Mobile and Forward+ renderer, set the vrs_mode property on Viewport to VRS_XR.

This feature is disabled if post effects are used such as glow, bloom, or DOF.

When enabled the foveation level will be adjusted automatically depending on current GPU load. It will be adjusted between low and the select foveation level in the previous setting. It is therefore best to combine this setting with foveation level set to high.

Compatibility renderer only

If enabled an OpenXR supplied depth buffer will be used while rendering which is submitted alongside the rendered image. The XR runtime can use this for improved reprojection.

Enabling this feature will disable stencil support during rendering. Not many XR runtimes make use of this, it is advised to leave this setting off unless it provides noticeable benefits for your use case.

If enabled, this will result in an alert message presented to the user if OpenXR fails to start. We don't always receive feedback from the XR system as to why starting fails. If we do, we log this to the console. Common failure reasons are:

No OpenXR runtime is installed on the host system.

Microsoft's WMR OpenXR runtime is currently active, this only supports DirectX and will fail if OpenGL or Vulkan is used.

SteamVR is used but no headset is connected/turned on.

Disable this if you support a fallback mode in your game so it can be played in desktop mode when no VR headset is connected, or if you're handling the failure condition yourself by checking OpenXRInterface.is_initialized().

This subsection allows you to enable to various optional OpenXR extensions. Keep in mind that the extensions will only work if the OpenXR runtime (SteamVR, Oculus, etc) the project is ran with supports them.

Enabling this will log debug messages from the XR runtime.

This allows you to choose which debug messages are logged.

This enables the hand tracking extension when supported by the device used. This is on by default for legacy reasons. The hand tracking extension provides access to data that allows you to visualise the user's hands with correct finger positions. Depending on platform capabilities the hand tracking data can be inferred from controller inputs, come from data gloves, come from optical hand tracking sensors or any other applicable source.

If your game only supports controllers this should be turned off.

See the page on hand tracking for additional details.

Enabling this means hand tracking may use the exact position of fingers, usually what a headset camera sees.

Enabling this means hand tracking may use the controller itself, and infer where fingers are based on controller input or sensors on the controller.

Enabling this extension allows the use of two new hand tracking poses. Pinch pose which is the location between the thumb and index finger pointing forward, and poke pose which is at the tip of the index finger.

This also allows 3 more gesture based inputs. Pinch, when the user pinches their thumb and index finger together. Aim activation, when the index finger is fully extended. And Grasps, when the user makes a fist.

When a hand interaction profile and controller interaction profile are supplied, the runtime will switch between profiles depending on if optical tracking is used or if the user is holding a controller.

If only a hand interaction profile is supplied any runtime should use hand interaction even if a controller is being held.

This enables the eye gaze interaction extension when supported by the device used. When enabled we will get feedback from eye tracking through a pose situated between the user's eyes orientated in the direction the user is looking. This will be a unified orientation.

In order to use this functionality you need to edit your action map and add a new pose action, say eye_pose. Now add a new interaction profile for the eye gaze interaction and map the eye_pose:

Don't forget to save!

Next add a new XRController3D node to your origin node and set its tracker property to /user/eyes_ext and set its pose property to eye_pose.

Now you can add things to this controller node such as a raycast, and control things with your eyes.

This extension is used to query the XR runtime for 3D assets of the hardware being used, usually a controller, as well as the position of that hardware. You can find a detailed guide on how to use it here.

These control whether or not binding modifiers can be used. Binding modifiers are used to apply thresholds or offset values. You can find information on how to use and set them up on the XR action map page here.

Allow analog threshold binding modifiers.

Allow D-pad binding modifiers.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## OpenXR Render Models — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/openxr_render_models.html

**Contents:**
- OpenXR Render Models
- OpenXR Render models node
  - Render model manager example
- Render model node
- Backend access
- User-contributed notes

A cornerstone of OpenXR's API design is being as platform agnostic as possible. A great example of this is OpenXR's action map system where XR runtimes have to support core interaction profiles to fall back on, if no interaction profile exists for the hardware being used. This ensures that OpenXR applications keep functioning even when used on hardware that didn't exist when the application was released, or that the developers of the application did not have access too.

A consequence of this is that the application developer doesn't know with any certainty what hardware is being used, as the XR runtime could be mimicking other hardware. The application developer thus can't show anything in relation to the actual hardware used, the most common use case being showing the controllers the user is currently holding.

Showing the correct controller models and having these models correctly positioned is important to a proper sense of immersion.

This is where OpenXR's render models API comes in. This API allows us to query the XR runtime for 3D assets that are correct for the physical hardware being used. The API also allows us to query the position of this hardware within the tracking volume and the correct positioning of subcomponents of this hardware.

For instance, we can correctly position and animate the trigger or show buttons being pressed.

For those runtimes that support the controller data source for hand tracking , we can also correctly position the user's fingers and hand according to the shape of the controller. Do note that this works in combination with the hand joints motion range extension to prevent clipping of the fingers.

The OpenXRRenderModelManager node can be used to automate most of the render models functionality. This node keeps track of the active render models currently made available by the XR runtime.

It will create child nodes for each active render model resulting in that render model being displayed.

This node must have an XROrigin3D node as an ancestor.

If tracker is set to Any our node will show all render models currently being tracked. In this scenario this node must be a direct child of our XROrigin3D node.

If tracker is set to None set our node will only show render models for which no tracker has been identified. In this scenario this node must also be a direct child of our XROrigin3D node.

If tracker is set to Left Hand or Right Hand our node will only show render models related to our left or right hand respectively. In this scenario, our node can be placed deeper in the scene tree.

For most XR runtimes this means the render model represents a controller that is actually being held by the user but this is not a guarantee. Some XR runtimes will always set the tracker to either the left or right hand even if the controller is not currently held but is being tracked. You should always test this as this will lead to unwanted behavior.

In this scenario we can also specify an action for a pose in the action map by setting the make_local_to_pose property to the pose action. Use this in combination with an XRController3D node that is using the same pose and you can now add a layer that allows you to deviate from the tracked position of both your controller and the related render model (see example below).

Combining the above with hand tracking does introduce the problem that hand tracking is completely independent from the action map system. You will need to combine the hand tracking and controller tracking poses to properly offset the render models.

This falls beyond the scope of this documentation.

You can download our render models demo which implements the setup described below.

In this setup we find an OpenXRRenderModelManager node directly underneath our XROrigin3D node. On this node our target property is set to None set and will handle showing all render models that are currently not related to our left or right hand controllers.

We then see the same setup for our left and right hand so we'll focus on just the left hand.

We have an XRController3D that will track the location of our hand.

We are using the grip pose in this example. The palm pose is arguably more suitable and predictable however it is not supported by all XR runtimes. See the hand tracking demo project for a solution to switching between these poses based on what is supported.

As a child of the node we have an AnimatableBody3D node that follows the tracked location of the hand but will interact with physics objects to stop the player's hand from going through walls etc. This node has a collision shape that encapsulates the hand.

It is important to set the physics priority so that this logic runs after any physics logic that moves the XROrigin3D node or the hand will lag a frame behind.

The script below shows a basic implementation for this that you can build upon.

Finally we see another OpenXRRenderModelManager node, this one with target set to the appropriate hand and make_local_to_pose set to the correct pose. This will ensure that the render models related to this hand are properly shown and offset if our collision handler has altered the location.

The OpenXRRenderModel node implements all the logic to display and position a given render model provided by the render models API.

Instances of this node are added by the render model manager node we used up above but you can interact with these directly if you wish.

Whenever Godot obtains information about a new render model an RID is created to reference that render model.

By assigning that RID to the render_model property on this node, the node will start displaying the render model and manage both the transform that places the render model in the correct place and animates all the sub objects.

The get_top_level_path function will return the top level path associated with this render model. This will point to either the left or right hand. As the top level path can be set or cleared depending on whether the user picks up, or puts down, the controller you can connect to the render_model_top_level_path_changes signal and react to these changes.

Depending on your setup of the OpenXRRenderModelManager nodes, render models will be removed or added as their top level path changes.

The nodes we've detailed out above handle all the display logic for us but it is possible to interact with the data that drives this directly and create your own implementation.

For this you can access the OpenXRRenderModelExtension singleton.

This object also lets you query whether render models are supported and enabled on the device currently being used by calling the is_active function on this object.

The built-in logic implements the interaction render model API that lists all render models related to controllers and similar devices that are present in the action map. It will automatically create and remove render model entities that are exposed through this API.

As other extensions become available these can be implemented in a GDExtension plugin. Such a plugin can call render_model_create and render_model_destroy to create the object that will provide access to that render model through the core render models API.

You should not destroy a render model outside of this logic.

You can connect to the render_model_added and render_model_removed signals to be informed when new render models are added or removed.

The core methods for working with this API are listed below:

Provides an array of RIDs for all render models that are being tracked.

render_model_new_scene_instance

Provides a new scene that contains all meshes needed to display the render model.

render_model_get_subaction_paths

Provides a list of subaction paths from your action map related to this render mode.

render_model_get_top_level_path

Returns the top level path associated with this render model (if any). Use the render_model_top_level_path_changed signal to react to this changing.

render_model_get_confidence

Returns the tracking confidence for the tracking data for this render model.

render_model_get_root_transform

Returns the root transform for this render model within our current reference space. This can be used to place the render model in space.

render_model_get_animatable_node_count

Returns the number of nodes in our render model scene that can be animated

render_model_get_animatable_node_name

Returns the name of the node that we can animate. Note that this node can be any number of levels deep within the scene.

render_model_is_animatable_node_visible

Returns true if this animatable node should be visible

render_model_get_animatable_node_transform

Returns the transform for this animatable node. This is a local transform that can be directly applied.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
class_name CollisionHands3D
extends AnimatableBody3D

func _ready():
    # Make sure these are set correctly.
    top_level = true
    sync_to_physics = false
    process_physics_priority = -90

func _physics_process(_delta):
    # Follow our parent node around.
    var dest_transform = get_parent().global_transform

    # We just apply rotation for this example.
    global_basis = dest_transform.basis

    # Attempt to move to where our tracked hand is.
    move_and_collide(dest_transform.origin - global_position)
```

---

## OpenXR composition layers — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/openxr_composition_layers.html

**Contents:**
- OpenXR composition layers
- Introduction
- Setting up the SubViewport
- Adding a composition layer
- Making the interface work
- Hole punching
- User-contributed notes

In XR games you generally want to create user interactions that happen in 3D space and involve users touching objects as if they are touching them in real life.

Sometimes however creating a more traditional 2D interface is unavoidable. In XR however you can't just add 2D components to your scene. Godot needs depth information to properly position these elements so they appear at a comfortable place for the user. Even with depth information there are headsets with slanted displays that make it impossible for the standard 2D pipeline to correctly render the 2D elements.

The solution then is to render the UI to a SubViewport and display the result of this using a ViewportTexture on a 3D mesh. The QuadMesh is a suitable option for this.

See the GUI in 3D example project for an example of this approach.

The problem with displaying the viewport in this way is that the rendered result is sampled for lens distortion by the XR runtime and the resulting quality loss can make UI text hard to read.

OpenXR offers a solution to this problem through composition layers. With composition layers it is possible for the contents of a viewport to be projected on a surface after lens distortion resulting in a much higher quality end result.

As not all XR runtimes support all composition layer types, Godot implements a fallback solution where we render the viewport as part of the normal scene but with the aforementioned quality limitations.

When the composition layer is supported, it is the XR runtime that presents the subviewport. This means the UI is only visible in the headset, it will not be accessible by Godot and will thus not be shown when you have a spectator view on the desktop.

There are currently 3 nodes that expose this functionality:

OpenXRCompositionLayerCylinder shows the contents of the SubViewport on the inside of a cylinder (or "slice" of a cylinder).

OpenXRCompositionLayerEquirect shows the contents of the SubViewport on the interior of a sphere (or "slice" of a sphere).

OpenXRCompositionLayerQuad shows the contents of the SubViewport on a flat rectangle.

The first step is adding a SubViewport for our 2D UI, this doesn't require any specific steps. For our example we do mark the viewport as transparent.

You can now create the 2D UI by adding child nodes to the SubViewport as you normally would. It is advisable to save the 2D UI in a subscene, this makes it easier to do your layout.

The update mode "When Visible" will not work as Godot can't determine whether the viewport is visible to the user. When assigning our viewport to a composition layer Godot will automatically adjust this.

The second step is adding our composition layer. We can add the correct composition layer node as a child node of our XROrigin3D node. This is very important as the XR runtime positions everything in relation to our origin.

We want to position the composition layer so it is at eye height and roughly 1 to 1.5 meters away from the player.

We now assign the SubViewport to the Layer Viewport property and enable Alpha Blend.

As the player can walk away from the origin point, you will want to reposition the composition layer when the player recenters the view. Using the reference space Local Floor will apply this logic automatically.

So far we're only displaying our UI, to make it work we need to add some code. For this example we're going to keep things simple and make one of the controllers work as a pointer. We'll then simulate mouse actions with this pointer.

This code also requires a MeshInstance3D node called Pointer to be added as a child to our OpenXRCompositionLayerQuad node. We configure a SphereMesh with a radius 0.01 meters. We'll be using this as a helper to visualize where the user is pointing.

The main function that drives this functionality is the intersects_ray function on our composition layer node. This function takes the global position and orientation of our pointer and returns the UV where our ray intersects our viewport. It returns Vector2(-1.0, -1.0) if we're not pointing at our viewport.

We start with setting up some variables, important here are the export variables which identify our controller node with which we point to our screen.

Next we define a helper function that takes the value returned from intersects_ray and gives us the global position for that intersection point. This implementation only works for our OpenXRCompositionLayerQuad node.

We also define a helper function that takes our intersect value and returns our location in the viewport's local coordinate system:

The main logic happens in our _process function. Here we start by hiding our pointer, we then check if we have a valid controller and viewport, and we call intersects_ray with the position and orientation of our controller:

Next we check if we're intersecting with our viewport. If so, we check if our button is pressed and place our pointer at our intersection point.

If we were intersecting in our previous process call and our pointer has moved, we prepare an InputEventMouseMotion object to simulate our mouse moving and send that to our viewport for further processing.

If we've just released our button we also prepare an InputEventMouseButton object to simulate a button release and send that to our viewport for further processing.

Or if we've just pressed our button we prepare an InputEventMouseButton object to simulate a button press and send that to our viewport for further processing.

Next we remember our state for next frame.

Finally, if we aren't intersecting, we clear our state.

As the composition layer is composited on top of the render result, it can be rendered in front of objects that are actually forward of the viewport.

By enabling hole punch you instruct Godot to render a transparent object where our viewport is displayed. It does this in a way that fills the depth buffer and clears the current rendering result. Anything behind our viewport will now be cleared, while anything in front of our viewport will be rendered as usual.

You also need to set Sort Order to a negative value, the XR compositor will now draw the viewport first, and then overlay our rendering result.

Use case showing how the user's hand is incorrectly obscured by a composition layer when hole punching is not used.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends OpenXRCompositionLayerQuad

const NO_INTERSECTION = Vector2(-1.0, -1.0)

@export var controller : XRController3D
@export var button_action : String = "trigger_click"

var was_pressed : bool = false
var was_intersect : Vector2 = NO_INTERSECTION

...
```

Example 2 (swift):
```swift
...

func _intersect_to_global_pos(intersect : Vector2) -> Vector3:
    if intersect != NO_INTERSECTION:
        var local_pos : Vector2 = (intersect - Vector2(0.5, 0.5)) * quad_size
        return global_transform * Vector3(local_pos.x, -local_pos.y, 0.0)
    else:
        return Vector3()

...
```

Example 3 (swift):
```swift
...

func _intersect_to_viewport_pos(intersect : Vector2) -> Vector2i:
    if layer_viewport and intersect != NO_INTERSECTION:
        var pos : Vector2 = intersect * Vector2(layer_viewport.size)
        return Vector2i(pos)
    else:
        return Vector2i(-1, -1)

...
```

Example 4 (gdscript):
```gdscript
...

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
    # Hide our pointer, we'll make it visible if we're interacting with the viewport.
    $Pointer.visible = false

    if controller and layer_viewport:
        var controller_t : Transform3D = controller.global_transform
        var intersect : Vector2 = intersects_ray(controller_t.origin, -controller_t.basis.z)

...
```

---

## Introducing XR tools — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/introducing_xr_tools.html

**Contents:**
- Introducing XR tools
- Installing XR Tools
- Basic hands
- More information
- User-contributed notes

Out of the box Godot gives you all the basic support to setup an XR project. XR specific game mechanics however need to be implemented on top of this foundation. While Godot makes this relatively easy this can still be a daunting task.

For this reason Godot has developed a toolkit called Godot XR Tools that implements many of the basic mechanics found in XR games, from locomotion to object interaction to UI interaction.

This toolkit is designed to work with both OpenXR and WebXR runtimes. We'll be using this as a base for our documentation here. It helps developers hit the ground running but for more specific use cases building your own logic is just as valid. In that case XR tools can help in providing inspiration.

Continuing on from our project we started in Setting up XR we want to add in the Godot XR Tools library. This can be downloaded from the Godot XR Tools releases page. Find the latest release for Godot 4, and under Assets, download the godot-xr-tools.zip file. You can also find it in the asset library with the title "Godot XR Tools for Godot 4".

If you're using the zip file, once it's downloaded unzip it. You will notice the files are held within a godot-xr-tools subfolder. Inside of this folder you will find an addons folder. It is this folder that you want to copy in its entirety to your Godot project folder. Your project should now look something like this:

Now open up your project in Godot, if you haven't already, and give it a minute or so to import all the resources of the plugin. If it asks for a path to Blender to be set you can just click the option to disable blender import and restart the editor.

After the import finishes you may notice that several "failed to load script" messages popped up, that's normal, the plugin just needs to be enabled in the project settings.

Next open the Project menu and select Project Settings... Now go to the Plugins tab and enable the plugin.

After doing that you need to close and re-open your project so everything is properly enabled.

Just to get a feel of things we're going to add a few standard components that dress up our scene starting with hands for our player.

OpenXR supports full hand tracking however there currently are significant differences in capabilities between the different XR Runtimes.

As a reliable alternative Godot XR Tools comes with a number of rigged hand scenes that react on trigger and grip inputs of your controller. These hands come in low and high poly versions, come in a few configurations, a number of animation files to control finger positions and a number of different textures.

In your scene tree select your left hand XRController3D node. Now click on the instantiate Child Scene button to add a child scene. Click the addons toggle so the addons folder can be searched. Then search for left_hand_low.tscn, and select it.

As you can see from the path of this scene, low poly models are in the lowpoly subfolder while high poly models are in the highpoly subfolder. You will want to use the low poly versions if you plan to release your game on mobile devices.

The default hand we chose is just a hand. The other options are:

tac_glove - the hand is wearing a glove with fingers exposed

full_glove - the hand is wearing a glove that covers the entire hand

Finally each hand comes in a physics version. This exposes all the bones. We'll look at how that can be used in another tutorial.

We repeat the same for the right hand.

We'll continue with adding features to our tutorial project using Godot XR tools in the next couple of pages. More detailed information about the toolkit can be found on the toolkits help pages.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## XR full screen effects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/xr_full_screen_effects.html

**Contents:**
- XR full screen effects
- Applying the projection matrix
- Limitations
- User-contributed notes

When adding custom full screen effects to your XR application, one approach is using a full screen quad and applying effects to that quad's shader. Add a MeshInstance3D node to your scene as a child of your XRCamera3D, and set the mesh property to a QuadMesh. Set the width and height of the quad to 2.

You can then add a shader to your quad to make it cover the screen. This is done by setting the vertex shader's POSITION built-in to vec4(VERTEX.xy, 1.0, 1.0). However, when creating an effect that is centered straight ahead in the user's view (such as a vignette effect), the end result may look incorrect in XR.

Below shows captures of the right-eye view with a vignette shader, both from the headset and the render target itself. The left captures are an unmodified shader; the right captures adjust the full screen quad using the projection matrix. While the capture on the left is centered in the render target, it is off-center in the headset view. But, after applying the projection matrix, we see that the effect is centered in the headset itself.

To properly center the effect, the POSITION of the full screen quad needs to take the asymmetric field of view into account. To do this while also ensuring the quad has full coverage of the entire render target, we can subdivide the quad and apply the projection matrix to the inner vertices. Let's increase the subdivide width and depth of the quad.

Then, in the vertex function of our shader, we apply an offset from the projection matrix to the inner vertices. Here's an example of how you might do this with the above simple vignette shader:

For more info on asymmetric FOV and its purpose, see this Meta Asymmetric Field of View FAQ.

This full screen effect method has no performance concerns for per-pixel effects such as the above vignette shader. However, it is not recommended to read from the screen texture when using this technique. Full screen effects that require reading from the screen texture effectively disable all rendering performance optimizations in XR. This is because, when reading from the screen texture, Godot makes a full copy of the render buffer; this drastically increases the workload for the GPU and can create performance concerns.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (julia):
```julia
shader_type spatial;
render_mode depth_test_disabled, skip_vertex_transform, unshaded, cull_disabled;

// Modify VERTEX.xy using the projection matrix to correctly center the effect.
void vertex() {
        vec2 vert_pos = VERTEX.xy;

        if (length(vert_pos) < 0.99) {
                vec4 offset = PROJECTION_MATRIX * vec4(0.0, 0.0, 1.0, 1.0);
                vert_pos += (offset.xy / offset.w);
        }

        POSITION = vec4(vert_pos, 1.0, 1.0);
}

void fragment() {
        ALBEDO = vec3(0.0);
        ALPHA = dot(UV * 2.0 - 1.0, UV * 2.0 - 1.0) * 2.0;
}
```

---

## Basic XR Locomotion — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/basic_xr_locomotion.html

**Contents:**
- Basic XR Locomotion
- Adding our player body
- Adding a floor
- Direct movement
- Teleport
- More advanced movement features
- User-contributed notes

For basic locomotion we're going to continue using our Godot XR Tools library. The library contains both basic movement features as more advanced features.

The first step we need to do is to add a helper node to our XROrigin3D node. Because XR supports roomscale tracking you can't simply add your XR setup to a CharacterBody3D node and expect things to work. You will run into trouble when the user moves around their physical space and is no longer standing in the center of their room. Godot XR Tools embeds the needed logic into a helper node called PlayerBody.

Select your XROrigin3D node and click on the Instantiate Child Scene button to add a child scene. Select addons/godot-xr-tools/player/player_body.tscn and add this node.

This node governs the in game movement of your character and will immediately react to gravity. So to prevent our player from infinitely falling down we'll quickly add a floor to our scene.

We start by adding a StaticBody3D node to our root node and we rename this to Floor. We add a MeshInstance3D node as a child node for our Floor. Then create a new PlaneMesh as its mesh. For now we set the size of the mesh to 100 x 100 meters. Next we add a CollisionShape3D node as a child node for our Floor. Then create a BoxShape as our shape. We set the size of this box shape to 100 x 1 x 100 meters. We also need to move our collision shape down by 0.5 meters so the top of our box is flush with the floor.

To make it easier to see that we're actually moving around our world, a white floor isn't going to do it. Create a texture using Wahooneys excellent free texture generator. Once you've created the texture add it to your project. Then create a new material for the MeshInstance3D node, add your texture as the albedo, and enable Triplaner under UV1 in the material properties.

We're going to start adding some basic direct movement to our setup. This allows the user to move through the virtual world using joystick input.

It is important to note that moving through the virtual world while the player is standing still in the real world, can be nausea inducing especially for players who are new to VR. The default settings on our movement functions are fairly conservative. We advise you to stick to these defaults but offer features in game to enable less comfortable settings for more experienced users who are used to playing VR games.

We want to enable this on the right hand controller. We do this by adding a subscene to the right hand XRController3D node. Select addons/godot-xr-tools/functions/movement_direct.tscn as the scene to add.

This function adds forward and backwards movement to the player by using the joystick on the right hand controller. It has an option to also add left/right strafe but by default this is disabled.

Instead, we are going to add the ability for the player to also turn with this joystick. We will add another subscene to our controller node, select addons/godot-xr-tools/functions/movement_turn.tscn for this.

The turn system by default uses a snap turn approach. This means that turning happens in steps. This may seem jarring however it is a tried and tested method of combating motion sickness. You can easily switch to a mode that offers smooth turning by changing the mode property on the turn node.

If you run your game at this point in time you will find that you can move through the world freely using the right hand joystick.

An alternative to direct movement that some users find more pleasant is the ability to teleport to another location within your game world. Godot XR Tools supports this through the teleport function and we will be adding this to our left hand controller.

Add a new child scene to your left hand XRController3D node by selecting the addons/godot-xr-tools/functions/function_teleport.tscn scene.

With this scene added the player will be able to teleport around the world by pressing the trigger on the left hand controller, pointing where they want to go, and then releasing the trigger. The player can also adjust the orientation by using the left hand controller's joystick.

If you've followed all instructions correctly your scene should now look something like this:

Godot XR Tools adds many more movement features such as gliding, a grapple hook implementation, a jetpack, climbing mechanics, etc.

Most work similarly to the basic movement features we've handled so far, simply add the relevant subscene from the plugin to the controller that implements it.

We'll look at some of these in more detail later on in this tutorial where additional setup is required (such as climbing) but for others please look at Godot XR Tools own help pages for details.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## OpenXR body tracking — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/openxr_body_tracking.html

**Contents:**
- OpenXR body tracking
- HTC Tracker support
- User-contributed notes

Support for full body tracking in OpenXR is only just becoming available for a select few platforms. As support solidifies information will be added to this page.

An option that has been available for some time is doing full body tracking using HTC trackers. These are currently supported through SteamVR and on HTC Elite XR headsets. They are exposed through the action map system.

These trackers are identified by their roles which are assigned to them when configured. Simply add XRController3D nodes as children to the XROrigin3D node and assign one of the following trackers:

/user/vive_tracker_htcx/role/handheld_object

/user/vive_tracker_htcx/role/left_foot

/user/vive_tracker_htcx/role/right_foot

/user/vive_tracker_htcx/role/left_shoulder

/user/vive_tracker_htcx/role/right_shoulder

/user/vive_tracker_htcx/role/left_elbow

/user/vive_tracker_htcx/role/right_elbow

/user/vive_tracker_htcx/role/left_knee

/user/vive_tracker_htcx/role/right_knee

/user/vive_tracker_htcx/role/waist

/user/vive_tracker_htcx/role/chest

/user/vive_tracker_htcx/role/camera

/user/vive_tracker_htcx/role/keyboard

You can now use these as targets for IK modifiers on a full body avatar.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## OpenXR hand tracking — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/xr/openxr_hand_tracking.html

**Contents:**
- OpenXR hand tracking
- Introduction
- Demo project
- The Hand Tracking API
  - Hand tracking node
  - Rigged hand mesh
  - The hand skeleton modifier
- The hand tracking data source
- Handling user input
  - The hand interaction profile

This page focuses specifically on the feature set exposed through OpenXR. Parts of the functionality presented here also applies to WebXR and can by provided by other XR interfaces.

When discussing hand tracking it is important to know that there are differences of opinion as to where lines are drawn. The practical result of this is that there are differences in implementation between the different OpenXR runtimes. You may find yourself in a place where chosen hardware doesn't support a piece of the puzzle or does things differently enough from the other platforms that you need to do extra work.

That said, recent improvements to the OpenXR specification are closing these gaps and as platforms implement these improvements we are getting closer to a future where we have either full portability between platforms or at least a clear way to detect the capabilities of a platform.

When we look at the early days of VR the focus of the major platforms was on tracked controller based input. Here we are tracking a physical device that also has buttons for further input. From the tracking data we can infer the location of the player's hands but no further information is known, traditionally it was left up to the game to implement a mechanism to display the player's hand and animate the fingers based on further input from the controller, be it due to buttons being pressed or through proximity sensors. Often fingers are also placed based on context, what the user is holding, and what action a user is performing.

More recently optical hand tracking has become a popular solution, where cameras track the user's hands and full tracking data for the hand and finger positions becomes available. Many vendors saw this as completely separate from controller tracking and introduced independent APIs to access hand and finger positions and orientation data. When handling input, it was up to the game developer to implement a gesture detection mechanism.

This split also exists in OpenXR, where controller tracking is handled primarily by the action map system, while optical hand tracking is primarily handled by the hand tracking API extension.

However, the world is not that black and white and we're seeing a number of scenarios where we cross the line:

Devices that fit in both categories, such as tracked gloves and controllers such as the Index controller that also perform finger tracking.

XR Runtimes that implement inferred hand tracking from controller data as a means to solve proper finger placement for multiple controllers.

XR applications that wish to seamlessly switch between controller and hand tracking offering the same user experience regardless of approach used.

OpenXR is answering this call by introducing further extensions that lets us query the capabilities of the XR runtime/hardware or that add further functionality across this divide. The problem that currently does remain is that there are gaps in adopting these extensions, with some platforms thus not reporting capabilities to their full extent. As such you may need to test for the features available on specific hardware and adjust your approach accordingly.

The information presented on this page was used to create a demo project that can be found here.

As mentioned in our introduction, the hand tracking API is primarily used with optical hand tracking and on many platforms only works when the user is not holding a controller. Some platforms support controller inferred hand tracking meaning that you will get hand tracking data even if the user is holding a controller. This includes SteamVR, Meta Quest (currently native only but Meta link support is likely coming), and hopefully soon others as well.

The hand tracking implementation in Godot has been standardized around the Godot Humanoid Skeleton and works both in OpenXR and WebXR. The instructions below will thus work in both environments.

In order to use the hand tracking API with OpenXR you first need to enable it. This can be done in the project settings:

For some standalone XR devices you also need to configure the hand tracking extension in export settings, for instance for Meta Quest:

Now you need to add 3 components into your scene for each hand:

A tracked node to position the hand.

A properly skinned hand mesh with skeleton.

A skeleton modifier that applies finger tracking data to the skeleton.

The hand tracking system uses separate hand trackers to track the position of the player's hands within our tracking space.

This information has been separated out for the following use cases:

Tracking happens in the local space of the XROrigin3D node. This node must be a child of the XROrigin3D node in order to be correctly placed.

This node can be used as an IK target when an upper body mesh with arms is used instead of separate hand meshes.

Actual placement of the hands may be loosely bound to the tracking in scenarios such as avatar creation UIs, fake mirrors, or similar situations resulting in the hand mesh and finger tracking being localized elsewhere.

We'll concentrate on the first use case only.

For this you need to add an XRNode3D node to your XROrigin3D node.

On this node the tracker should be set to /user/hand_tracker/left or /user/hand_tracker/right for the left or right hand respectively.

The pose should remain set to default, no other option will work here.

The checkbox Show When Tracked will automatically hide this node if no tracking data is available, or make this node visible if tracking data is available.

In order to display our hand we need a hand mesh that is properly rigged and skinned. For this Godot uses the hand bone structure as defined for the Godot Humanoid but optionally supporting an extra tip bone for each finger.

The OpenXR hand tracking demo contains example glTF files of properly rigged hands.

We will be using those here and add them as a child to our XRNode3D node. We also need to enable editable children to gain access to our Skeleton3D node.

Finally we need to add an XRHandModifier3D node as a child to our Skeleton3D node. This node will obtain the finger tracking data from OpenXR and apply it the hand model.

You need to set the Hand Tracker property to either /user/hand_tracker/left or /user/hand_tracker/right depending on whether we are apply the tracking data of respectively the left or right hand.

You can also set the Bone Update mode on this node.

Full applies the hand tracking data fully. This does mean that the skeleton positioning will potentially reflect the size of the actual hand of the user. This can lead to scrunching effect if meshes aren't weighted properly to account for this. Make sure you test your game with players of all sizes when optical hand tracking is used!

Rotation Only will only apply rotation to the bones of the hands and keep the bone length as is. In this mode the size of the hand mesh doesn't change.

With this added, when we run the project we should see the hand correctly displayed if hand tracking is supported.

This is an OpenXR extension that provides information about the source of the hand tracking data. At this moment only a few runtimes implement it but if it is available, Godot will activate it.

If this extension is not supported and thus unknown is returned, you can make the following assumptions:

If you are using SteamVR (including Steam link), only controller based hand tracking is supported.

For any other runtime, if hand tracking is supported, only optical hand tracking is supported (Note, Meta Link currently fall into this category).

In all other cases, no hand tracking is supported at all.

You can access this information through code:

This example logs the state for the left hand.

If in this example no hand tracker is returned by get_tracker, this means the hand tracking API is not supported on the XR runtime at all.

If there is a tracker but has_tracking_data is false, the user's hand is currently not being tracked. This is likely caused by one of the following reasons:

The player's hand is not visible by any of the tracking cameras on the headset

The player is currently using a controller and the headset only supports optical hand tracking

The controller is turned off and only controller hand tracking is supported.

Reacting to actions performed by the user is handled through The XR action map if controllers are used. In the action map you can map various inputs like the trigger or joystick on the controller to an action. This can then drive logic in your game.

When hand tracking is used we originally had no such inputs, inputs are driven by gestures made by the user such as making a fist to grab or pinching the thumb and index finger together to select something. It was up to the game developer to implement this.

Recognizing that there is an increasing demand for applications that can switch seamlessly between controller and hand tracking and the need some form of basic input capability, a number of extensions were added to the specification that provide some basic gesture recognition and can be used with the action map.

The hand interaction profile extension is a new core extension which supports pinch, grasp, and poke gestures and related poses. There is still limited support for this extension but it should become available in more runtimes in the near future.

The pinch gesture is triggered by pinching your thumb and index finger together. This is often used as a select gesture for menu systems, similar to using your controller to point at an object and press the trigger to select and is thus often mapped as such.

The pinch pose is a pose positioned in the middle between the tip of the thumb and the tip of the index finger and oriented such that a ray cast can be used to identify a target.

The pinch float input is a value between 0.0 (the tip of the thumb and index finger are apart) and 1.0 (the tip of the thumb and index finger are touching).

The pinch ready input is true when the tips of the fingers are (close to) touching.

The grasp gesture is triggered by making a fist and is often used to pick items up, similar to engaging the squeeze input on controllers.

The grasp float input is a value between 0.0 (open hand) and 1.0 (fist).

The grasp ready input is true when the user made a fist.

The poke gesture is triggered by extending your index finger, this one is a bit of an exception as the pose at the tip of your index finger is often used to poke an interactable object. The poke pose is a pose positioned on the tip of the index finger.

Finally the aim activate (ready) input is defined as an input that is 1.0/true when the index finger is extended and pointing at a target that can be activated. How runtimes interpret this, is not clear.

With this setup the normal left_hand and right_hand trackers are used and you can thus seamlessly switch between controller and hand tracking input.

You need to enable the hand interaction profile extension in the OpenXR project settings.

The Microsoft hand interaction profile extension was introduced by Microsoft and loosely mimics the simple controller profile. Meta has also added support for this extension but only on their native OpenXR client, it is currently not available over Meta Link.

Pinch support is exposed through the select input, the value of which is 0.0 when the tip of the thumb and index finger are apart and 1.0 when they are together.

Note that in this profile the aim pose is redefined as a pose between thumb and index finger, oriented so a ray cast can be used to identify a target.

Grasp support is exposed through the squeeze input, the value of which is 0.0 when the hand is open, and 1.0 when a fist is made.

With this setup the normal left_hand and right_hand trackers are used and you can thus seamlessly switch between controller and hand tracking input.

The HTC hand interaction profile extension was introduced by HTC and is defined similarly to the Microsoft extension. It is only supported by HTC for the Focus 3 and Elite XR headsets.

See the Microsoft hand interaction profile for the gesture support.

The defining difference is that this extension introduces two new trackers, /user/hand_htc/left and /user/hand_htc/right. This means that extra logic needs to be implemented to switch between the default trackers and the HTC specific trackers when the user puts down, or picks up, their controller.

The simple controller profile is a standard core profile defined as a fallback profile when a controller is used for which no profile exists.

There are a number of OpenXR runtimes that will mimic controllers through the simple controller profile when hand tracking is used.

Unfortunately there is no sound way to determine whether an unknown controller is used or whether hand tracking is emulating a controller through this profile.

XR runtimes are free to define how the simple controller profile operates, so there is also no certainty to how this profile is mapped to gestures.

The most common mapping seems to be that select click is true when the tip of the thumb and index fingers are touching while the user's palm is facing away from the user. menu click will be true when tip of the thumb and index fingers are touching while the user's palm is facing towards the user.

With this setup the normal left_hand and right_hand trackers are used and you can thus seamlessly switch between controller and hand tracking input.

As some of these interaction profiles have overlap it is important to know that you can add each profile to your action map and the XR runtime will choose the best fitting profile.

For instance, a Meta Quest supports both the Microsoft hand interaction profile and simple controller profile. If both are specified the Microsoft hand interaction profile will take precedence and will be used.

The expectation is that once Meta supports the core hand interaction profile extension, that profile will take precedence over both Microsoft and simple controller profiles.

If the platform doesn't support any interaction profiles when hand tracking is used, or if you're building an application where you need more complicated gesture support you're going to need to build your own gesture recognition system.

You can obtain the full hand tracking data through the XRHandTracker resource for each hand. You can obtain the hand tracker by calling XRServer.get_tracker and using either /user/hand_tracker/left or /user/hand_tracker/left as the tracker. This resource provides access to all the joint information for the given hand.

Detailing out a full gesture recognition algorithm goes beyond the scope of this manual however there are a number of community projects you can look at:

Julian Todd's Auto hands library

Malcolm Nixons Hand Pose Detector

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (yaml):
```yaml
var hand_tracker : XRHandTracker = XRServer.get_tracker('/user/hand_tracker/left')
if hand_tracker:
    if hand_tracker.has_tracking_data:
        if hand_tracker.hand_tracking_source == XRHandTracker.HAND_TRACKING_SOURCE_UNKNOWN:
            print("Hand tracking source unknown")
        elif hand_tracker.hand_tracking_source == XRHandTracker.HAND_TRACKING_SOURCE_UNOBSTRUCTED:
            print("Hand tracking source is optical hand tracking")
        elif hand_tracker.hand_tracking_source == XRHandTracker.HAND_TRACKING_SOURCE_CONTROLLER:
            print("Hand tracking data is inferred from controller data")
        else:
            print("Unknown hand tracking source ", hand_tracker.hand_tracking_source)
    else:
        print("Hand is currently not being tracked")
else:
    print("No hand tracker registered")
```

---

## AimModifier3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_aimmodifier3d.html

**Contents:**
- AimModifier3D
- Description
- Properties
- Methods
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: BoneConstraint3D < SkeletonModifier3D < Node3D < Node < Object

The AimModifier3D rotates a bone to look at a reference bone.

This is a simple version of LookAtModifier3D that only allows bone to the reference without advanced options such as angle limitation or time-based interpolation.

The feature is simplified, but instead it is implemented with smooth tracking without euler, see set_use_euler().

get_forward_axis(index: int) const

get_primary_rotation_axis(index: int) const

is_using_euler(index: int) const

is_using_secondary_rotation(index: int) const

set_forward_axis(index: int, axis: BoneAxis)

set_primary_rotation_axis(index: int, axis: Axis)

set_use_euler(index: int, enabled: bool)

set_use_secondary_rotation(index: int, enabled: bool)

int setting_count = 0 🔗

void set_setting_count(value: int)

int get_setting_count()

The number of settings in the modifier.

BoneAxis get_forward_axis(index: int) const 🔗

Returns the forward axis of the bone.

Axis get_primary_rotation_axis(index: int) const 🔗

Returns the axis of the first rotation. It is enabled only if is_using_euler() is true.

bool is_using_euler(index: int) const 🔗

Returns true if it provides rotation with using euler.

bool is_using_secondary_rotation(index: int) const 🔗

Returns true if it provides rotation by two axes. It is enabled only if is_using_euler() is true.

void set_forward_axis(index: int, axis: BoneAxis) 🔗

Sets the forward axis of the bone.

void set_primary_rotation_axis(index: int, axis: Axis) 🔗

Sets the axis of the first rotation. It is enabled only if is_using_euler() is true.

void set_use_euler(index: int, enabled: bool) 🔗

If sets enabled to true, it provides rotation with using euler.

If sets enabled to false, it provides rotation with using rotation by arc generated from the forward axis vector and the vector toward the reference.

void set_use_secondary_rotation(index: int, enabled: bool) 🔗

If sets enabled to true, it provides rotation by two axes. It is enabled only if is_using_euler() is true.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## AcceptDialog — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_acceptdialog.html

**Contents:**
- AcceptDialog
- Description
- Properties
- Methods
- Theme Properties
- Signals
- Property Descriptions
- Method Descriptions
- Theme Property Descriptions
- User-contributed notes

Inherits: Window < Viewport < Node < Object

Inherited By: ConfirmationDialog

A base dialog used for user notification.

The default use of AcceptDialog is to allow it to only be accepted or closed, with the same result. However, the confirmed and canceled signals allow to make the two actions different, and the add_button() method allows to add custom buttons and actions.

dialog_close_on_escape

true (overrides Window)

true (overrides Window)

true (overrides Window)

true (overrides Window)

"Alert!" (overrides Window)

true (overrides Window)

false (overrides Window)

true (overrides Window)

add_button(text: String, right: bool = false, action: String = "")

add_cancel_button(name: String)

register_text_enter(line_edit: LineEdit)

remove_button(button: Button)

Emitted when the dialog is closed or the button created with add_cancel_button() is pressed.

Emitted when the dialog is accepted, i.e. the OK button is pressed.

custom_action(action: StringName) 🔗

Emitted when a custom button with an action is pressed. See add_button().

bool dialog_autowrap = false 🔗

void set_autowrap(value: bool)

Sets autowrapping for the text in the dialog.

bool dialog_close_on_escape = true 🔗

void set_close_on_escape(value: bool)

bool get_close_on_escape()

If true, the dialog will be hidden when the ui_cancel action is pressed (by default, this action is bound to @GlobalScope.KEY_ESCAPE).

bool dialog_hide_on_ok = true 🔗

void set_hide_on_ok(value: bool)

bool get_hide_on_ok()

If true, the dialog is hidden when the OK button is pressed. You can set it to false if you want to do e.g. input validation when receiving the confirmed signal, and handle hiding the dialog in your own logic.

Note: Some nodes derived from this class can have a different default value, and potentially their own built-in logic overriding this setting. For example FileDialog defaults to false, and has its own input validation code that is called when you press OK, which eventually hides the dialog if the input is valid. As such, this property can't be used in FileDialog to disable hiding the dialog when pressing OK.

String dialog_text = "" 🔗

void set_text(value: String)

The text displayed by the dialog.

String ok_button_text = "" 🔗

void set_ok_button_text(value: String)

String get_ok_button_text()

The text displayed by the OK button (see get_ok_button()). If empty, a default text will be used.

Button add_button(text: String, right: bool = false, action: String = "") 🔗

Adds a button with label text and a custom action to the dialog and returns the created button.

If action is not empty, pressing the button will emit the custom_action signal with the specified action string.

If true, right will place the button to the right of any sibling buttons.

You can use remove_button() method to remove a button created with this method from the dialog.

Button add_cancel_button(name: String) 🔗

Adds a button with label name and a cancel action to the dialog and returns the created button.

You can use remove_button() method to remove a button created with this method from the dialog.

Returns the label used for built-in text.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

Button get_ok_button() 🔗

Returns the OK Button instance.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

void register_text_enter(line_edit: LineEdit) 🔗

Registers a LineEdit in the dialog. When the enter key is pressed, the dialog will be accepted.

void remove_button(button: Button) 🔗

Removes the button from the dialog. Does NOT free the button. The button must be a Button added with add_button() or add_cancel_button() method. After removal, pressing the button will no longer emit this dialog's custom_action or canceled signals.

int buttons_min_height = 0 🔗

The minimum height of each button in the bottom row (such as OK/Cancel) in pixels. This can be increased to make buttons with short texts easier to click/tap.

int buttons_min_width = 0 🔗

The minimum width of each button in the bottom row (such as OK/Cancel) in pixels. This can be increased to make buttons with short texts easier to click/tap.

int buttons_separation = 10 🔗

The size of the vertical space between the dialog's content and the button row.

The panel that fills the background of the window.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Node — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_node.html

**Contents:**
- Node
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Constants
- Property Descriptions
- Method Descriptions

Inherited By: AnimationMixer, AudioStreamPlayer, CanvasItem, CanvasLayer, EditorFileSystem, EditorPlugin, EditorResourcePreview, HTTPRequest, InstancePlaceholder, MissingNode, MultiplayerSpawner, MultiplayerSynchronizer, NavigationAgent2D, NavigationAgent3D, Node3D, ResourcePreloader, ShaderGlobalsOverride, StatusIndicator, Timer, Viewport, WorldEnvironment

Base class for all scene objects.

Nodes are Godot's building blocks. They can be assigned as the child of another node, resulting in a tree arrangement. A given node can contain any number of nodes as children with the requirement that all siblings (direct children of a node) should have unique names.

A tree of nodes is called a scene. Scenes can be saved to the disk and then instantiated into other scenes. This allows for very high flexibility in the architecture and data model of Godot projects.

Scene tree: The SceneTree contains the active tree of nodes. When a node is added to the scene tree, it receives the NOTIFICATION_ENTER_TREE notification and its _enter_tree() callback is triggered. Child nodes are always added after their parent node, i.e. the _enter_tree() callback of a parent node will be triggered before its child's.

Once all nodes have been added in the scene tree, they receive the NOTIFICATION_READY notification and their respective _ready() callbacks are triggered. For groups of nodes, the _ready() callback is called in reverse order, starting with the children and moving up to the parent nodes.

This means that when adding a node to the scene tree, the following order will be used for the callbacks: _enter_tree() of the parent, _enter_tree() of the children, _ready() of the children and finally _ready() of the parent (recursively for the entire scene tree).

Processing: Nodes can override the "process" state, so that they receive a callback on each frame requesting them to process (do something). Normal processing (callback _process(), toggled with set_process()) happens as fast as possible and is dependent on the frame rate, so the processing time delta (in seconds) is passed as an argument. Physics processing (callback _physics_process(), toggled with set_physics_process()) happens a fixed number of times per second (60 by default) and is useful for code related to the physics engine.

Nodes can also process input events. When present, the _input() function will be called for each input that the program receives. In many cases, this can be overkill (unless used for simple projects), and the _unhandled_input() function might be preferred; it is called when the input event was not handled by anyone else (typically, GUI Control nodes), ensuring that the node only receives the events that were meant for it.

To keep track of the scene hierarchy (especially when instantiating scenes into other scenes), an "owner" can be set for the node with the owner property. This keeps track of who instantiated what. This is mostly useful when writing editors and tools, though.

Finally, when a node is freed with Object.free() or queue_free(), it will also free all its children.

Groups: Nodes can be added to as many groups as you want to be easy to manage, you could create groups like "enemies" or "collectables" for example, depending on your game. See add_to_group(), is_in_group() and remove_from_group(). You can then retrieve all nodes in these groups, iterate them and even call methods on groups via the methods on SceneTree.

Networking with nodes: After connecting to a server (or making one, see ENetMultiplayerPeer), it is possible to use the built-in RPC (remote procedure call) system to communicate over the network. By calling rpc() with a method name, it will be called locally and in all connected peers (peers = clients and the server that accepts connections). To identify which node receives the RPC call, Godot will use its NodePath (make sure node names are the same on all peers). Also, take a look at the high-level networking tutorial and corresponding demos.

Note: The script property is part of the Object class, not Node. It isn't exposed like most properties but does have a setter and getter (see Object.set_script() and Object.get_script()).

PhysicsInterpolationMode

physics_interpolation_mode

process_physics_priority

process_thread_group_order

BitField[ProcessThreadMessages]

process_thread_messages

_enter_tree() virtual

_get_accessibility_configuration_warnings() virtual const

_get_configuration_warnings() virtual const

_get_focused_accessibility_element() virtual const

_input(event: InputEvent) virtual

_physics_process(delta: float) virtual

_process(delta: float) virtual

_shortcut_input(event: InputEvent) virtual

_unhandled_input(event: InputEvent) virtual

_unhandled_key_input(event: InputEvent) virtual

add_child(node: Node, force_readable_name: bool = false, internal: InternalMode = 0)

add_sibling(sibling: Node, force_readable_name: bool = false)

add_to_group(group: StringName, persistent: bool = false)

atr(message: String, context: StringName = "") const

atr_n(message: String, plural_message: StringName, n: int, context: StringName = "") const

call_deferred_thread_group(method: StringName, ...) vararg

call_thread_safe(method: StringName, ...) vararg

can_auto_translate() const

duplicate(flags: int = 15) const

find_child(pattern: String, recursive: bool = true, owned: bool = true) const

find_children(pattern: String, type: String = "", recursive: bool = true, owned: bool = true) const

find_parent(pattern: String) const

get_accessibility_element() const

get_child(idx: int, include_internal: bool = false) const

get_child_count(include_internal: bool = false) const

get_children(include_internal: bool = false) const

get_index(include_internal: bool = false) const

get_last_exclusive_window() const

get_multiplayer_authority() const

get_node(path: NodePath) const

get_node_and_resource(path: NodePath)

get_node_or_null(path: NodePath) const

get_node_rpc_config() const

get_orphan_node_ids() static

get_path_to(node: Node, use_unique_path: bool = false) const

get_physics_process_delta_time() const

get_process_delta_time() const

get_scene_instance_load_placeholder() const

get_tree_string_pretty()

has_node(path: NodePath) const

has_node_and_resource(path: NodePath) const

is_ancestor_of(node: Node) const

is_displayed_folded() const

is_editable_instance(node: Node) const

is_greater_than(node: Node) const

is_in_group(group: StringName) const

is_inside_tree() const

is_multiplayer_authority() const

is_node_ready() const

is_part_of_edited_scene() const

is_physics_interpolated() const

is_physics_interpolated_and_enabled() const

is_physics_processing() const

is_physics_processing_internal() const

is_processing() const

is_processing_input() const

is_processing_internal() const

is_processing_shortcut_input() const

is_processing_unhandled_input() const

is_processing_unhandled_key_input() const

move_child(child_node: Node, to_index: int)

notify_deferred_thread_group(what: int)

notify_thread_safe(what: int)

print_orphan_nodes() static

propagate_call(method: StringName, args: Array = [], parent_first: bool = false)

propagate_notification(what: int)

queue_accessibility_update()

remove_child(node: Node)

remove_from_group(group: StringName)

reparent(new_parent: Node, keep_global_transform: bool = true)

replace_by(node: Node, keep_groups: bool = false)

reset_physics_interpolation()

rpc(method: StringName, ...) vararg

rpc_config(method: StringName, config: Variant)

rpc_id(peer_id: int, method: StringName, ...) vararg

set_deferred_thread_group(property: StringName, value: Variant)

set_display_folded(fold: bool)

set_editable_instance(node: Node, is_editable: bool)

set_multiplayer_authority(id: int, recursive: bool = true)

set_physics_process(enable: bool)

set_physics_process_internal(enable: bool)

set_process(enable: bool)

set_process_input(enable: bool)

set_process_internal(enable: bool)

set_process_shortcut_input(enable: bool)

set_process_unhandled_input(enable: bool)

set_process_unhandled_key_input(enable: bool)

set_scene_instance_load_placeholder(load_placeholder: bool)

set_thread_safe(property: StringName, value: Variant)

set_translation_domain_inherited()

update_configuration_warnings()

child_entered_tree(node: Node) 🔗

Emitted when the child node enters the SceneTree, usually because this node entered the tree (see tree_entered), or add_child() has been called.

This signal is emitted after the child node's own NOTIFICATION_ENTER_TREE and tree_entered.

child_exiting_tree(node: Node) 🔗

Emitted when the child node is about to exit the SceneTree, usually because this node is exiting the tree (see tree_exiting), or because the child node is being removed or freed.

When this signal is received, the child node is still accessible inside the tree. This signal is emitted after the child node's own tree_exiting and NOTIFICATION_EXIT_TREE.

child_order_changed() 🔗

Emitted when the list of children is changed. This happens when child nodes are added, moved or removed.

editor_description_changed(node: Node) 🔗

Emitted when the node's editor description field changed.

editor_state_changed() 🔗

Emitted when an attribute of the node that is relevant to the editor is changed. Only emitted in the editor.

Emitted when the node is considered ready, after _ready() is called.

Emitted when the node's name is changed, if the node is inside the tree.

replacing_by(node: Node) 🔗

Emitted when this node is being replaced by the node, see replace_by().

This signal is emitted after node has been added as a child of the original parent node, but before all original child nodes have been reparented to node.

Emitted when the node enters the tree.

This signal is emitted after the related NOTIFICATION_ENTER_TREE notification.

Emitted after the node exits the tree and is no longer active.

This signal is emitted after the related NOTIFICATION_EXIT_TREE notification.

Emitted when the node is just about to exit the tree. The node is still valid. As such, this is the right place for de-initialization (or a "destructor", if you will).

This signal is emitted after the node's _exit_tree(), and before the related NOTIFICATION_EXIT_TREE.

ProcessMode PROCESS_MODE_INHERIT = 0

Inherits process_mode from the node's parent. This is the default for any newly created node.

ProcessMode PROCESS_MODE_PAUSABLE = 1

Stops processing when SceneTree.paused is true. This is the inverse of PROCESS_MODE_WHEN_PAUSED, and the default for the root node.

ProcessMode PROCESS_MODE_WHEN_PAUSED = 2

Process only when SceneTree.paused is true. This is the inverse of PROCESS_MODE_PAUSABLE.

ProcessMode PROCESS_MODE_ALWAYS = 3

Always process. Keeps processing, ignoring SceneTree.paused. This is the inverse of PROCESS_MODE_DISABLED.

ProcessMode PROCESS_MODE_DISABLED = 4

Never process. Completely disables processing, ignoring SceneTree.paused. This is the inverse of PROCESS_MODE_ALWAYS.

enum ProcessThreadGroup: 🔗

ProcessThreadGroup PROCESS_THREAD_GROUP_INHERIT = 0

Process this node based on the thread group mode of the first parent (or grandparent) node that has a thread group mode that is not inherit. See process_thread_group for more information.

ProcessThreadGroup PROCESS_THREAD_GROUP_MAIN_THREAD = 1

Process this node (and child nodes set to inherit) on the main thread. See process_thread_group for more information.

ProcessThreadGroup PROCESS_THREAD_GROUP_SUB_THREAD = 2

Process this node (and child nodes set to inherit) on a sub-thread. See process_thread_group for more information.

flags ProcessThreadMessages: 🔗

ProcessThreadMessages FLAG_PROCESS_THREAD_MESSAGES = 1

Allows this node to process threaded messages created with call_deferred_thread_group() right before _process() is called.

ProcessThreadMessages FLAG_PROCESS_THREAD_MESSAGES_PHYSICS = 2

Allows this node to process threaded messages created with call_deferred_thread_group() right before _physics_process() is called.

ProcessThreadMessages FLAG_PROCESS_THREAD_MESSAGES_ALL = 3

Allows this node to process threaded messages created with call_deferred_thread_group() right before either _process() or _physics_process() are called.

enum PhysicsInterpolationMode: 🔗

PhysicsInterpolationMode PHYSICS_INTERPOLATION_MODE_INHERIT = 0

Inherits physics_interpolation_mode from the node's parent. This is the default for any newly created node.

PhysicsInterpolationMode PHYSICS_INTERPOLATION_MODE_ON = 1

Enables physics interpolation for this node and for children set to PHYSICS_INTERPOLATION_MODE_INHERIT. This is the default for the root node.

PhysicsInterpolationMode PHYSICS_INTERPOLATION_MODE_OFF = 2

Disables physics interpolation for this node and for children set to PHYSICS_INTERPOLATION_MODE_INHERIT.

enum DuplicateFlags: 🔗

DuplicateFlags DUPLICATE_SIGNALS = 1

Duplicate the node's signal connections that are connected with the Object.CONNECT_PERSIST flag.

DuplicateFlags DUPLICATE_GROUPS = 2

Duplicate the node's groups.

DuplicateFlags DUPLICATE_SCRIPTS = 4

Duplicate the node's script (also overriding the duplicated children's scripts, if combined with DUPLICATE_USE_INSTANTIATION).

DuplicateFlags DUPLICATE_USE_INSTANTIATION = 8

Duplicate using PackedScene.instantiate(). If the node comes from a scene saved on disk, reuses PackedScene.instantiate() as the base for the duplicated node and its children.

InternalMode INTERNAL_MODE_DISABLED = 0

The node will not be internal.

InternalMode INTERNAL_MODE_FRONT = 1

The node will be placed at the beginning of the parent's children, before any non-internal sibling.

InternalMode INTERNAL_MODE_BACK = 2

The node will be placed at the end of the parent's children, after any non-internal sibling.

enum AutoTranslateMode: 🔗

AutoTranslateMode AUTO_TRANSLATE_MODE_INHERIT = 0

Inherits auto_translate_mode from the node's parent. This is the default for any newly created node.

AutoTranslateMode AUTO_TRANSLATE_MODE_ALWAYS = 1

Always automatically translate. This is the inverse of AUTO_TRANSLATE_MODE_DISABLED, and the default for the root node.

AutoTranslateMode AUTO_TRANSLATE_MODE_DISABLED = 2

Never automatically translate. This is the inverse of AUTO_TRANSLATE_MODE_ALWAYS.

String parsing for POT generation will be skipped for this node and children that are set to AUTO_TRANSLATE_MODE_INHERIT.

NOTIFICATION_ENTER_TREE = 10 🔗

Notification received when the node enters a SceneTree. See _enter_tree().

This notification is received before the related tree_entered signal.

NOTIFICATION_EXIT_TREE = 11 🔗

Notification received when the node is about to exit a SceneTree. See _exit_tree().

This notification is received after the related tree_exiting signal.

NOTIFICATION_MOVED_IN_PARENT = 12 🔗

Deprecated: This notification is no longer sent by the engine. Use NOTIFICATION_CHILD_ORDER_CHANGED instead.

NOTIFICATION_READY = 13 🔗

Notification received when the node is ready. See _ready().

NOTIFICATION_PAUSED = 14 🔗

Notification received when the node is paused. See process_mode.

NOTIFICATION_UNPAUSED = 15 🔗

Notification received when the node is unpaused. See process_mode.

NOTIFICATION_PHYSICS_PROCESS = 16 🔗

Notification received from the tree every physics frame when is_physics_processing() returns true. See _physics_process().

NOTIFICATION_PROCESS = 17 🔗

Notification received from the tree every rendered frame when is_processing() returns true. See _process().

NOTIFICATION_PARENTED = 18 🔗

Notification received when the node is set as a child of another node (see add_child() and add_sibling()).

Note: This does not mean that the node entered the SceneTree.

NOTIFICATION_UNPARENTED = 19 🔗

Notification received when the parent node calls remove_child() on this node.

Note: This does not mean that the node exited the SceneTree.

NOTIFICATION_SCENE_INSTANTIATED = 20 🔗

Notification received only by the newly instantiated scene root node, when PackedScene.instantiate() is completed.

NOTIFICATION_DRAG_BEGIN = 21 🔗

Notification received when a drag operation begins. All nodes receive this notification, not only the dragged one.

Can be triggered either by dragging a Control that provides drag data (see Control._get_drag_data()) or using Control.force_drag().

Use Viewport.gui_get_drag_data() to get the dragged data.

NOTIFICATION_DRAG_END = 22 🔗

Notification received when a drag operation ends.

Use Viewport.gui_is_drag_successful() to check if the drag succeeded.

NOTIFICATION_PATH_RENAMED = 23 🔗

Notification received when the node's name or one of its ancestors' name is changed. This notification is not received when the node is removed from the SceneTree.

NOTIFICATION_CHILD_ORDER_CHANGED = 24 🔗

Notification received when the list of children is changed. This happens when child nodes are added, moved or removed.

NOTIFICATION_INTERNAL_PROCESS = 25 🔗

Notification received from the tree every rendered frame when is_processing_internal() returns true.

NOTIFICATION_INTERNAL_PHYSICS_PROCESS = 26 🔗

Notification received from the tree every physics frame when is_physics_processing_internal() returns true.

NOTIFICATION_POST_ENTER_TREE = 27 🔗

Notification received when the node enters the tree, just before NOTIFICATION_READY may be received. Unlike the latter, it is sent every time the node enters tree, not just once.

NOTIFICATION_DISABLED = 28 🔗

Notification received when the node is disabled. See PROCESS_MODE_DISABLED.

NOTIFICATION_ENABLED = 29 🔗

Notification received when the node is enabled again after being disabled. See PROCESS_MODE_DISABLED.

NOTIFICATION_RESET_PHYSICS_INTERPOLATION = 2001 🔗

Notification received when reset_physics_interpolation() is called on the node or its ancestors.

NOTIFICATION_EDITOR_PRE_SAVE = 9001 🔗

Notification received right before the scene with the node is saved in the editor. This notification is only sent in the Godot editor and will not occur in exported projects.

NOTIFICATION_EDITOR_POST_SAVE = 9002 🔗

Notification received right after the scene with the node is saved in the editor. This notification is only sent in the Godot editor and will not occur in exported projects.

NOTIFICATION_WM_MOUSE_ENTER = 1002 🔗

Notification received when the mouse enters the window.

Implemented for embedded windows and on desktop and web platforms.

NOTIFICATION_WM_MOUSE_EXIT = 1003 🔗

Notification received when the mouse leaves the window.

Implemented for embedded windows and on desktop and web platforms.

NOTIFICATION_WM_WINDOW_FOCUS_IN = 1004 🔗

Notification received from the OS when the node's Window ancestor is focused. This may be a change of focus between two windows of the same engine instance, or from the OS desktop or a third-party application to a window of the game (in which case NOTIFICATION_APPLICATION_FOCUS_IN is also received).

A Window node receives this notification when it is focused.

NOTIFICATION_WM_WINDOW_FOCUS_OUT = 1005 🔗

Notification received from the OS when the node's Window ancestor is defocused. This may be a change of focus between two windows of the same engine instance, or from a window of the game to the OS desktop or a third-party application (in which case NOTIFICATION_APPLICATION_FOCUS_OUT is also received).

A Window node receives this notification when it is defocused.

NOTIFICATION_WM_CLOSE_REQUEST = 1006 🔗

Notification received from the OS when a close request is sent (e.g. closing the window with a "Close" button or Alt + F4).

Implemented on desktop platforms.

NOTIFICATION_WM_GO_BACK_REQUEST = 1007 🔗

Notification received from the OS when a go back request is sent (e.g. pressing the "Back" button on Android).

Implemented only on Android.

NOTIFICATION_WM_SIZE_CHANGED = 1008 🔗

Notification received when the window is resized.

Note: Only the resized Window node receives this notification, and it's not propagated to the child nodes.

NOTIFICATION_WM_DPI_CHANGE = 1009 🔗

Notification received from the OS when the screen's dots per inch (DPI) scale is changed. Only implemented on macOS.

NOTIFICATION_VP_MOUSE_ENTER = 1010 🔗

Notification received when the mouse cursor enters the Viewport's visible area, that is not occluded behind other Controls or Windows, provided its Viewport.gui_disable_input is false and regardless if it's currently focused or not.

NOTIFICATION_VP_MOUSE_EXIT = 1011 🔗

Notification received when the mouse cursor leaves the Viewport's visible area, that is not occluded behind other Controls or Windows, provided its Viewport.gui_disable_input is false and regardless if it's currently focused or not.

NOTIFICATION_WM_POSITION_CHANGED = 1012 🔗

Notification received when the window is moved.

NOTIFICATION_OS_MEMORY_WARNING = 2009 🔗

Notification received from the OS when the application is exceeding its allocated memory.

Implemented only on iOS.

NOTIFICATION_TRANSLATION_CHANGED = 2010 🔗

Notification received when translations may have changed. Can be triggered by the user changing the locale, changing auto_translate_mode or when the node enters the scene tree. Can be used to respond to language changes, for example to change the UI strings on the fly. Useful when working with the built-in translation support, like Object.tr().

Note: This notification is received alongside NOTIFICATION_ENTER_TREE, so if you are instantiating a scene, the child nodes will not be initialized yet. You can use it to setup translations for this node, child nodes created from script, or if you want to access child nodes added in the editor, make sure the node is ready using is_node_ready().

NOTIFICATION_WM_ABOUT = 2011 🔗

Notification received from the OS when a request for "About" information is sent.

Implemented only on macOS.

NOTIFICATION_CRASH = 2012 🔗

Notification received from Godot's crash handler when the engine is about to crash.

Implemented on desktop platforms, if the crash handler is enabled.

NOTIFICATION_OS_IME_UPDATE = 2013 🔗

Notification received from the OS when an update of the Input Method Engine occurs (e.g. change of IME cursor position or composition string).

Implemented only on macOS.

NOTIFICATION_APPLICATION_RESUMED = 2014 🔗

Notification received from the OS when the application is resumed.

Specific to the Android and iOS platforms.

NOTIFICATION_APPLICATION_PAUSED = 2015 🔗

Notification received from the OS when the application is paused.

Specific to the Android and iOS platforms.

Note: On iOS, you only have approximately 5 seconds to finish a task started by this signal. If you go over this allotment, iOS will kill the app instead of pausing it.

NOTIFICATION_APPLICATION_FOCUS_IN = 2016 🔗

Notification received from the OS when the application is focused, i.e. when changing the focus from the OS desktop or a thirdparty application to any open window of the Godot instance.

Implemented on desktop and mobile platforms.

NOTIFICATION_APPLICATION_FOCUS_OUT = 2017 🔗

Notification received from the OS when the application is defocused, i.e. when changing the focus from any open window of the Godot instance to the OS desktop or a thirdparty application.

Implemented on desktop and mobile platforms.

NOTIFICATION_TEXT_SERVER_CHANGED = 2018 🔗

Notification received when the TextServer is changed.

NOTIFICATION_ACCESSIBILITY_UPDATE = 3000 🔗

Notification received when an accessibility information update is required.

NOTIFICATION_ACCESSIBILITY_INVALIDATE = 3001 🔗

Notification received when accessibility elements are invalidated. All node accessibility elements are automatically deleted after receiving this message, therefore all existing references to such elements should be discarded.

AutoTranslateMode auto_translate_mode = 0 🔗

void set_auto_translate_mode(value: AutoTranslateMode)

AutoTranslateMode get_auto_translate_mode()

Defines if any text should automatically change to its translated version depending on the current locale (for nodes such as Label, RichTextLabel, Window, etc.). Also decides if the node's strings should be parsed for POT generation.

Note: For the root node, auto translate mode can also be set via ProjectSettings.internationalization/rendering/root_node_auto_translate.

String editor_description = "" 🔗

void set_editor_description(value: String)

String get_editor_description()

An optional description to the node. It will be displayed as a tooltip when hovering over the node in the editor's Scene dock.

MultiplayerAPI multiplayer 🔗

MultiplayerAPI get_multiplayer()

The MultiplayerAPI instance associated with this node. See SceneTree.get_multiplayer().

Note: Renaming the node, or moving it in the tree, will not move the MultiplayerAPI to the new path, you will have to update this manually.

void set_name(value: StringName)

StringName get_name()

The name of the node. This name must be unique among the siblings (other child nodes from the same parent). When set to an existing sibling's name, the node is automatically renamed.

Note: When changing the name, the following characters will be replaced with an underscore: (. : @ / " %). In particular, the @ character is reserved for auto-generated names. See also String.validate_node_name().

void set_owner(value: Node)

The owner of this node. The owner must be an ancestor of this node. When packing the owner node in a PackedScene, all the nodes it owns are also saved with it. See also unique_name_in_owner.

Note: In the editor, nodes not owned by the scene root are usually not displayed in the Scene dock, and will not be saved. To prevent this, remember to set the owner after calling add_child().

PhysicsInterpolationMode physics_interpolation_mode = 0 🔗

void set_physics_interpolation_mode(value: PhysicsInterpolationMode)

PhysicsInterpolationMode get_physics_interpolation_mode()

The physics interpolation mode to use for this node. Only effective if ProjectSettings.physics/common/physics_interpolation or SceneTree.physics_interpolation is true.

By default, nodes inherit the physics interpolation mode from their parent. This property can enable or disable physics interpolation individually for each node, regardless of their parents' physics interpolation mode.

Note: Some node types like VehicleWheel3D have physics interpolation disabled by default, as they rely on their own custom solution.

Note: When teleporting a node to a distant position, it's recommended to temporarily disable interpolation with reset_physics_interpolation() after moving the node. This avoids creating a visual streak between the old and new positions.

ProcessMode process_mode = 0 🔗

void set_process_mode(value: ProcessMode)

ProcessMode get_process_mode()

The node's processing behavior. To check if the node can process in its current mode, use can_process().

int process_physics_priority = 0 🔗

void set_physics_process_priority(value: int)

int get_physics_process_priority()

Similar to process_priority but for NOTIFICATION_PHYSICS_PROCESS, _physics_process(), or NOTIFICATION_INTERNAL_PHYSICS_PROCESS.

int process_priority = 0 🔗

void set_process_priority(value: int)

int get_process_priority()

The node's execution order of the process callbacks (_process(), NOTIFICATION_PROCESS, and NOTIFICATION_INTERNAL_PROCESS). Nodes whose priority value is lower call their process callbacks first, regardless of tree order.

ProcessThreadGroup process_thread_group = 0 🔗

void set_process_thread_group(value: ProcessThreadGroup)

ProcessThreadGroup get_process_thread_group()

Set the process thread group for this node (basically, whether it receives NOTIFICATION_PROCESS, NOTIFICATION_PHYSICS_PROCESS, _process() or _physics_process() (and the internal versions) on the main thread or in a sub-thread.

By default, the thread group is PROCESS_THREAD_GROUP_INHERIT, which means that this node belongs to the same thread group as the parent node. The thread groups means that nodes in a specific thread group will process together, separate to other thread groups (depending on process_thread_group_order). If the value is set is PROCESS_THREAD_GROUP_SUB_THREAD, this thread group will occur on a sub thread (not the main thread), otherwise if set to PROCESS_THREAD_GROUP_MAIN_THREAD it will process on the main thread. If there is not a parent or grandparent node set to something other than inherit, the node will belong to the default thread group. This default group will process on the main thread and its group order is 0.

During processing in a sub-thread, accessing most functions in nodes outside the thread group is forbidden (and it will result in an error in debug mode). Use Object.call_deferred(), call_thread_safe(), call_deferred_thread_group() and the likes in order to communicate from the thread groups to the main thread (or to other thread groups).

To better understand process thread groups, the idea is that any node set to any other value than PROCESS_THREAD_GROUP_INHERIT will include any child (and grandchild) nodes set to inherit into its process thread group. This means that the processing of all the nodes in the group will happen together, at the same time as the node including them.

int process_thread_group_order 🔗

void set_process_thread_group_order(value: int)

int get_process_thread_group_order()

Change the process thread group order. Groups with a lesser order will process before groups with a greater order. This is useful when a large amount of nodes process in sub thread and, afterwards, another group wants to collect their result in the main thread, as an example.

BitField[ProcessThreadMessages] process_thread_messages 🔗

void set_process_thread_messages(value: BitField[ProcessThreadMessages])

BitField[ProcessThreadMessages] get_process_thread_messages()

Set whether the current thread group will process messages (calls to call_deferred_thread_group() on threads), and whether it wants to receive them during regular process or physics process callbacks.

String scene_file_path 🔗

void set_scene_file_path(value: String)

String get_scene_file_path()

The original scene's file path, if the node has been instantiated from a PackedScene file. Only scene root nodes contains this.

bool unique_name_in_owner = false 🔗

void set_unique_name_in_owner(value: bool)

bool is_unique_name_in_owner()

If true, the node can be accessed from any node sharing the same owner or from the owner itself, with special %Name syntax in get_node().

Note: If another node with the same owner shares the same name as this node, the other node will no longer be accessible as unique.

void _enter_tree() virtual 🔗

Called when the node enters the SceneTree (e.g. upon instantiating, scene changing, or after calling add_child() in a script). If the node has children, its _enter_tree() callback will be called first, and then that of the children.

Corresponds to the NOTIFICATION_ENTER_TREE notification in Object._notification().

void _exit_tree() virtual 🔗

Called when the node is about to leave the SceneTree (e.g. upon freeing, scene changing, or after calling remove_child() in a script). If the node has children, its _exit_tree() callback will be called last, after all its children have left the tree.

Corresponds to the NOTIFICATION_EXIT_TREE notification in Object._notification() and signal tree_exiting. To get notified when the node has already left the active tree, connect to the tree_exited.

PackedStringArray _get_accessibility_configuration_warnings() virtual const 🔗

The elements in the array returned from this method are displayed as warnings in the Scene dock if the script that overrides it is a tool script, and accessibility warnings are enabled in the editor settings.

Returning an empty array produces no warnings.

PackedStringArray _get_configuration_warnings() virtual const 🔗

The elements in the array returned from this method are displayed as warnings in the Scene dock if the script that overrides it is a tool script.

Returning an empty array produces no warnings.

Call update_configuration_warnings() when the warnings need to be updated for this node.

RID _get_focused_accessibility_element() virtual const 🔗

Called during accessibility information updates to determine the currently focused sub-element, should return a sub-element RID or the value returned by get_accessibility_element().

void _input(event: InputEvent) virtual 🔗

Called when there is an input event. The input event propagates up through the node tree until a node consumes it.

It is only called if input processing is enabled, which is done automatically if this method is overridden, and can be toggled with set_process_input().

To consume the input event and stop it propagating further to other nodes, Viewport.set_input_as_handled() can be called.

For gameplay input, _unhandled_input() and _unhandled_key_input() are usually a better fit as they allow the GUI to intercept the events first.

Note: This method is only called if the node is present in the scene tree (i.e. if it's not an orphan).

void _physics_process(delta: float) virtual 🔗

Called once on each physics tick, and allows Nodes to synchronize their logic with physics ticks. delta is the logical time between physics ticks in seconds and is equal to Engine.time_scale / Engine.physics_ticks_per_second.

It is only called if physics processing is enabled for this Node, which is done automatically if this method is overridden, and can be toggled with set_physics_process().

Processing happens in order of process_physics_priority, lower priority values are called first. Nodes with the same priority are processed in tree order, or top to bottom as seen in the editor (also known as pre-order traversal).

Corresponds to the NOTIFICATION_PHYSICS_PROCESS notification in Object._notification().

Note: This method is only called if the node is present in the scene tree (i.e. if it's not an orphan).

Note: Accumulated delta may diverge from real world seconds.

void _process(delta: float) virtual 🔗

Called on each idle frame, prior to rendering, and after physics ticks have been processed. delta is the time between frames in seconds.

It is only called if processing is enabled for this Node, which is done automatically if this method is overridden, and can be toggled with set_process().

Processing happens in order of process_priority, lower priority values are called first. Nodes with the same priority are processed in tree order, or top to bottom as seen in the editor (also known as pre-order traversal).

Corresponds to the NOTIFICATION_PROCESS notification in Object._notification().

Note: This method is only called if the node is present in the scene tree (i.e. if it's not an orphan).

Note: When the engine is struggling and the frame rate is lowered, delta will increase. When delta is increased, it's capped at a maximum of Engine.time_scale * Engine.max_physics_steps_per_frame / Engine.physics_ticks_per_second. As a result, accumulated delta may not represent real world time.

Note: When --fixed-fps is enabled or the engine is running in Movie Maker mode (see MovieWriter), process delta will always be the same for every frame, regardless of how much time the frame took to render.

Note: Frame delta may be post-processed by OS.delta_smoothing if this is enabled for the project.

void _ready() virtual 🔗

Called when the node is "ready", i.e. when both the node and its children have entered the scene tree. If the node has children, their _ready() callbacks get triggered first, and the parent node will receive the ready notification afterwards.

Corresponds to the NOTIFICATION_READY notification in Object._notification(). See also the @onready annotation for variables.

Usually used for initialization. For even earlier initialization, Object._init() may be used. See also _enter_tree().

Note: This method may be called only once for each node. After removing a node from the scene tree and adding it again, _ready() will not be called a second time. This can be bypassed by requesting another call with request_ready(), which may be called anywhere before adding the node again.

void _shortcut_input(event: InputEvent) virtual 🔗

Called when an InputEventKey, InputEventShortcut, or InputEventJoypadButton hasn't been consumed by _input() or any GUI Control item. It is called before _unhandled_key_input() and _unhandled_input(). The input event propagates up through the node tree until a node consumes it.

It is only called if shortcut processing is enabled, which is done automatically if this method is overridden, and can be toggled with set_process_shortcut_input().

To consume the input event and stop it propagating further to other nodes, Viewport.set_input_as_handled() can be called.

This method can be used to handle shortcuts. For generic GUI events, use _input() instead. Gameplay events should usually be handled with either _unhandled_input() or _unhandled_key_input().

Note: This method is only called if the node is present in the scene tree (i.e. if it's not orphan).

void _unhandled_input(event: InputEvent) virtual 🔗

Called when an InputEvent hasn't been consumed by _input() or any GUI Control item. It is called after _shortcut_input() and after _unhandled_key_input(). The input event propagates up through the node tree until a node consumes it.

It is only called if unhandled input processing is enabled, which is done automatically if this method is overridden, and can be toggled with set_process_unhandled_input().

To consume the input event and stop it propagating further to other nodes, Viewport.set_input_as_handled() can be called.

For gameplay input, this method is usually a better fit than _input(), as GUI events need a higher priority. For keyboard shortcuts, consider using _shortcut_input() instead, as it is called before this method. Finally, to handle keyboard events, consider using _unhandled_key_input() for performance reasons.

Note: This method is only called if the node is present in the scene tree (i.e. if it's not an orphan).

void _unhandled_key_input(event: InputEvent) virtual 🔗

Called when an InputEventKey hasn't been consumed by _input() or any GUI Control item. It is called after _shortcut_input() but before _unhandled_input(). The input event propagates up through the node tree until a node consumes it.

It is only called if unhandled key input processing is enabled, which is done automatically if this method is overridden, and can be toggled with set_process_unhandled_key_input().

To consume the input event and stop it propagating further to other nodes, Viewport.set_input_as_handled() can be called.

This method can be used to handle Unicode character input with Alt, Alt + Ctrl, and Alt + Shift modifiers, after shortcuts were handled.

For gameplay input, this and _unhandled_input() are usually a better fit than _input(), as GUI events should be handled first. This method also performs better than _unhandled_input(), since unrelated events such as InputEventMouseMotion are automatically filtered. For shortcuts, consider using _shortcut_input() instead.

Note: This method is only called if the node is present in the scene tree (i.e. if it's not an orphan).

void add_child(node: Node, force_readable_name: bool = false, internal: InternalMode = 0) 🔗

Adds a child node. Nodes can have any number of children, but every child must have a unique name. Child nodes are automatically deleted when the parent node is deleted, so an entire scene can be removed by deleting its topmost node.

If force_readable_name is true, improves the readability of the added node. If not named, the node is renamed to its type, and if it shares name with a sibling, a number is suffixed more appropriately. This operation is very slow. As such, it is recommended leaving this to false, which assigns a dummy name featuring @ in both situations.

If internal is different than INTERNAL_MODE_DISABLED, the child will be added as internal node. These nodes are ignored by methods like get_children(), unless their parameter include_internal is true. It also prevents these nodes being duplicated with their parent. The intended usage is to hide the internal nodes from the user, so the user won't accidentally delete or modify them. Used by some GUI nodes, e.g. ColorPicker.

Note: If node already has a parent, this method will fail. Use remove_child() first to remove node from its current parent. For example:

If you need the child node to be added below a specific node in the list of children, use add_sibling() instead of this method.

Note: If you want a child to be persisted to a PackedScene, you must set owner in addition to calling add_child(). This is typically relevant for tool scripts and editor plugins. If add_child() is called without setting owner, the newly added Node will not be visible in the scene tree, though it will be visible in the 2D/3D view.

void add_sibling(sibling: Node, force_readable_name: bool = false) 🔗

Adds a sibling node to this node's parent, and moves the added sibling right below this node.

If force_readable_name is true, improves the readability of the added sibling. If not named, the sibling is renamed to its type, and if it shares name with a sibling, a number is suffixed more appropriately. This operation is very slow. As such, it is recommended leaving this to false, which assigns a dummy name featuring @ in both situations.

Use add_child() instead of this method if you don't need the child node to be added below a specific node in the list of children.

Note: If this node is internal, the added sibling will be internal too (see add_child()'s internal parameter).

void add_to_group(group: StringName, persistent: bool = false) 🔗

Adds the node to the group. Groups can be helpful to organize a subset of nodes, for example "enemies" or "collectables". See notes in the description, and the group methods in SceneTree.

If persistent is true, the group will be stored when saved inside a PackedScene. All groups created and displayed in the Node dock are persistent.

Note: To improve performance, the order of group names is not guaranteed and may vary between project runs. Therefore, do not rely on the group order.

Note: SceneTree's group methods will not work on this node if not inside the tree (see is_inside_tree()).

String atr(message: String, context: StringName = "") const 🔗

Translates a message, using the translation catalogs configured in the Project Settings. Further context can be specified to help with the translation. Note that most Control nodes automatically translate their strings, so this method is mostly useful for formatted strings or custom drawn text.

This method works the same as Object.tr(), with the addition of respecting the auto_translate_mode state.

If Object.can_translate_messages() is false, or no translation is available, this method returns the message without changes. See Object.set_message_translation().

For detailed examples, see Internationalizing games.

String atr_n(message: String, plural_message: StringName, n: int, context: StringName = "") const 🔗

Translates a message or plural_message, using the translation catalogs configured in the Project Settings. Further context can be specified to help with the translation.

This method works the same as Object.tr_n(), with the addition of respecting the auto_translate_mode state.

If Object.can_translate_messages() is false, or no translation is available, this method returns message or plural_message, without changes. See Object.set_message_translation().

The n is the number, or amount, of the message's subject. It is used by the translation system to fetch the correct plural form for the current language.

For detailed examples, see Localization using gettext.

Note: Negative and float numbers may not properly apply to some countable subjects. It's recommended to handle these cases with atr().

Variant call_deferred_thread_group(method: StringName, ...) vararg 🔗

This function is similar to Object.call_deferred() except that the call will take place when the node thread group is processed. If the node thread group processes in sub-threads, then the call will be done on that thread, right before NOTIFICATION_PROCESS or NOTIFICATION_PHYSICS_PROCESS, the _process() or _physics_process() or their internal versions are called.

Variant call_thread_safe(method: StringName, ...) vararg 🔗

This function ensures that the calling of this function will succeed, no matter whether it's being done from a thread or not. If called from a thread that is not allowed to call the function, the call will become deferred. Otherwise, the call will go through directly.

bool can_auto_translate() const 🔗

Returns true if this node can automatically translate messages depending on the current locale. See auto_translate_mode, atr(), and atr_n().

bool can_process() const 🔗

Returns true if the node can receive processing notifications and input callbacks (NOTIFICATION_PROCESS, _input(), etc.) from the SceneTree and Viewport. The returned value depends on process_mode:

If set to PROCESS_MODE_PAUSABLE, returns true when the game is processing, i.e. SceneTree.paused is false;

If set to PROCESS_MODE_WHEN_PAUSED, returns true when the game is paused, i.e. SceneTree.paused is true;

If set to PROCESS_MODE_ALWAYS, always returns true;

If set to PROCESS_MODE_DISABLED, always returns false;

If set to PROCESS_MODE_INHERIT, use the parent node's process_mode to determine the result.

If the node is not inside the tree, returns false no matter the value of process_mode.

Tween create_tween() 🔗

Creates a new Tween and binds it to this node.

This is the equivalent of doing:

The Tween will start automatically on the next process frame or physics frame (depending on TweenProcessMode). See Tween.bind_node() for more info on Tweens bound to nodes.

Note: The method can still be used when the node is not inside SceneTree. It can fail in an unlikely case of using a custom MainLoop.

Node duplicate(flags: int = 15) const 🔗

Duplicates the node, returning a new node with all of its properties, signals, groups, and children copied from the original. The behavior can be tweaked through the flags (see DuplicateFlags). Internal nodes are not duplicated.

Note: For nodes with a Script attached, if Object._init() has been defined with required parameters, the duplicated node will not have a Script.

Node find_child(pattern: String, recursive: bool = true, owned: bool = true) const 🔗

Finds the first descendant of this node whose name matches pattern, returning null if no match is found. The matching is done against node names, not their paths, through String.match(). As such, it is case-sensitive, "*" matches zero or more characters, and "?" matches any single character.

If recursive is false, only this node's direct children are checked. Nodes are checked in tree order, so this node's first direct child is checked first, then its own direct children, etc., before moving to the second direct child, and so on. Internal children are also included in the search (see internal parameter in add_child()).

If owned is true, only descendants with a valid owner node are checked.

Note: This method can be very slow. Consider storing a reference to the found node in a variable. Alternatively, use get_node() with unique names (see unique_name_in_owner).

Note: To find all descendant nodes matching a pattern or a class type, see find_children().

Array[Node] find_children(pattern: String, type: String = "", recursive: bool = true, owned: bool = true) const 🔗

Finds all descendants of this node whose names match pattern, returning an empty Array if no match is found. The matching is done against node names, not their paths, through String.match(). As such, it is case-sensitive, "*" matches zero or more characters, and "?" matches any single character.

If type is not empty, only ancestors inheriting from type are included (see Object.is_class()).

If recursive is false, only this node's direct children are checked. Nodes are checked in tree order, so this node's first direct child is checked first, then its own direct children, etc., before moving to the second direct child, and so on. Internal children are also included in the search (see internal parameter in add_child()).

If owned is true, only descendants with a valid owner node are checked.

Note: This method can be very slow. Consider storing references to the found nodes in a variable.

Note: To find a single descendant node matching a pattern, see find_child().

Node find_parent(pattern: String) const 🔗

Finds the first ancestor of this node whose name matches pattern, returning null if no match is found. The matching is done through String.match(). As such, it is case-sensitive, "*" matches zero or more characters, and "?" matches any single character. See also find_child() and find_children().

Note: As this method walks upwards in the scene tree, it can be slow in large, deeply nested nodes. Consider storing a reference to the found node in a variable. Alternatively, use get_node() with unique names (see unique_name_in_owner).

RID get_accessibility_element() const 🔗

Returns main accessibility element RID.

Note: This method should be called only during accessibility information updates (NOTIFICATION_ACCESSIBILITY_UPDATE).

Node get_child(idx: int, include_internal: bool = false) const 🔗

Fetches a child node by its index. Each child node has an index relative to its siblings (see get_index()). The first child is at index 0. Negative values can also be used to start from the end of the list. This method can be used in combination with get_child_count() to iterate over this node's children. If no child exists at the given index, this method returns null and an error is generated.

If include_internal is false, internal children are ignored (see add_child()'s internal parameter).

Note: To fetch a node by NodePath, use get_node().

int get_child_count(include_internal: bool = false) const 🔗

Returns the number of children of this node.

If include_internal is false, internal children are not counted (see add_child()'s internal parameter).

Array[Node] get_children(include_internal: bool = false) const 🔗

Returns all children of this node inside an Array.

If include_internal is false, excludes internal children from the returned array (see add_child()'s internal parameter).

Array[StringName] get_groups() const 🔗

Returns an Array of group names that the node has been added to.

Note: To improve performance, the order of group names is not guaranteed and may vary between project runs. Therefore, do not rely on the group order.

Note: This method may also return some group names starting with an underscore (_). These are internally used by the engine. To avoid conflicts, do not use custom groups starting with underscores. To exclude internal groups, see the following code snippet:

int get_index(include_internal: bool = false) const 🔗

Returns this node's order among its siblings. The first node's index is 0. See also get_child().

If include_internal is false, returns the index ignoring internal children. The first, non-internal child will have an index of 0 (see add_child()'s internal parameter).

Window get_last_exclusive_window() const 🔗

Returns the Window that contains this node, or the last exclusive child in a chain of windows starting with the one that contains this node.

int get_multiplayer_authority() const 🔗

Returns the peer ID of the multiplayer authority for this node. See set_multiplayer_authority().

Node get_node(path: NodePath) const 🔗

Fetches a node. The NodePath can either be a relative path (from this node), or an absolute path (from the SceneTree.root) to a node. If path does not point to a valid node, generates an error and returns null. Attempts to access methods on the return value will result in an "Attempt to call <method> on a null instance." error.

Note: Fetching by absolute path only works when the node is inside the scene tree (see is_inside_tree()).

Example: Assume this method is called from the Character node, inside the following tree:

The following calls will return a valid node:

Array get_node_and_resource(path: NodePath) 🔗

Fetches a node and its most nested resource as specified by the NodePath's subname. Returns an Array of size 3 where:

Element 0 is the Node, or null if not found;

Element 1 is the subname's last nested Resource, or null if not found;

Element 2 is the remaining NodePath, referring to an existing, non-Resource property (see Object.get_indexed()).

Example: Assume that the child's Sprite2D.texture has been assigned an AtlasTexture:

Node get_node_or_null(path: NodePath) const 🔗

Fetches a node by NodePath. Similar to get_node(), but does not generate an error if path does not point to a valid node.

Variant get_node_rpc_config() const 🔗

Returns a Dictionary mapping method names to their RPC configuration defined for this node using rpc_config().

Note: This method only returns the RPC configuration assigned via rpc_config(). See Script.get_rpc_config() to retrieve the RPCs defined by the Script.

Array[int] get_orphan_node_ids() static 🔗

Returns object IDs of all orphan nodes (nodes outside the SceneTree). Used for debugging.

Note: get_orphan_node_ids() only works in debug builds. When called in a project exported in release mode, get_orphan_node_ids() will return an empty array.

Node get_parent() const 🔗

Returns this node's parent node, or null if the node doesn't have a parent.

NodePath get_path() const 🔗

Returns the node's absolute path, relative to the SceneTree.root. If the node is not inside the scene tree, this method fails and returns an empty NodePath.

NodePath get_path_to(node: Node, use_unique_path: bool = false) const 🔗

Returns the relative NodePath from this node to the specified node. Both nodes must be in the same SceneTree or scene hierarchy, otherwise this method fails and returns an empty NodePath.

If use_unique_path is true, returns the shortest path accounting for this node's unique name (see unique_name_in_owner).

Note: If you get a relative path which starts from a unique node, the path may be longer than a normal relative path, due to the addition of the unique node's name.

float get_physics_process_delta_time() const 🔗

Returns the time elapsed (in seconds) since the last physics callback. This value is identical to _physics_process()'s delta parameter, and is often consistent at run-time, unless Engine.physics_ticks_per_second is changed. See also NOTIFICATION_PHYSICS_PROCESS.

Note: The returned value will be larger than expected if running at a framerate lower than Engine.physics_ticks_per_second / Engine.max_physics_steps_per_frame FPS. This is done to avoid "spiral of death" scenarios where performance would plummet due to an ever-increasing number of physics steps per frame. This behavior affects both _process() and _physics_process(). As a result, avoid using delta for time measurements in real-world seconds. Use the Time singleton's methods for this purpose instead, such as Time.get_ticks_usec().

float get_process_delta_time() const 🔗

Returns the time elapsed (in seconds) since the last process callback. This value is identical to _process()'s delta parameter, and may vary from frame to frame. See also NOTIFICATION_PROCESS.

Note: The returned value will be larger than expected if running at a framerate lower than Engine.physics_ticks_per_second / Engine.max_physics_steps_per_frame FPS. This is done to avoid "spiral of death" scenarios where performance would plummet due to an ever-increasing number of physics steps per frame. This behavior affects both _process() and _physics_process(). As a result, avoid using delta for time measurements in real-world seconds. Use the Time singleton's methods for this purpose instead, such as Time.get_ticks_usec().

bool get_scene_instance_load_placeholder() const 🔗

Returns true if this node is an instance load placeholder. See InstancePlaceholder and set_scene_instance_load_placeholder().

SceneTree get_tree() const 🔗

Returns the SceneTree that contains this node. If this node is not inside the tree, generates an error and returns null. See also is_inside_tree().

String get_tree_string() 🔗

Returns the tree as a String. Used mainly for debugging purposes. This version displays the path relative to the current node, and is good for copy/pasting into the get_node() function. It also can be used in game UI/UX.

May print, for example:

String get_tree_string_pretty() 🔗

Similar to get_tree_string(), this returns the tree as a String. This version displays a more graphical representation similar to what is displayed in the Scene Dock. It is useful for inspecting larger trees.

May print, for example:

Viewport get_viewport() const 🔗

Returns the node's closest Viewport ancestor, if the node is inside the tree. Otherwise, returns null.

Window get_window() const 🔗

Returns the Window that contains this node. If the node is in the main window, this is equivalent to getting the root node (get_tree().get_root()).

bool has_node(path: NodePath) const 🔗

Returns true if the path points to a valid node. See also get_node().

bool has_node_and_resource(path: NodePath) const 🔗

Returns true if path points to a valid node and its subnames point to a valid Resource, e.g. Area2D/CollisionShape2D:shape. Properties that are not Resource types (such as nodes or other Variant types) are not considered. See also get_node_and_resource().

bool is_ancestor_of(node: Node) const 🔗

Returns true if the given node is a direct or indirect child of this node.

bool is_displayed_folded() const 🔗

Returns true if the node is folded (collapsed) in the Scene dock. This method is intended to be used in editor plugins and tools. See also set_display_folded().

bool is_editable_instance(node: Node) const 🔗

Returns true if node has editable children enabled relative to this node. This method is intended to be used in editor plugins and tools. See also set_editable_instance().

bool is_greater_than(node: Node) const 🔗

Returns true if the given node occurs later in the scene hierarchy than this node. A node occurring later is usually processed last.

bool is_in_group(group: StringName) const 🔗

Returns true if this node has been added to the given group. See add_to_group() and remove_from_group(). See also notes in the description, and the SceneTree's group methods.

bool is_inside_tree() const 🔗

Returns true if this node is currently inside a SceneTree. See also get_tree().

bool is_multiplayer_authority() const 🔗

Returns true if the local system is the multiplayer authority of this node.

bool is_node_ready() const 🔗

Returns true if the node is ready, i.e. it's inside scene tree and all its children are initialized.

request_ready() resets it back to false.

bool is_part_of_edited_scene() const 🔗

Returns true if the node is part of the scene currently opened in the editor.

bool is_physics_interpolated() const 🔗

Returns true if physics interpolation is enabled for this node (see physics_interpolation_mode).

Note: Interpolation will only be active if both the flag is set and physics interpolation is enabled within the SceneTree. This can be tested using is_physics_interpolated_and_enabled().

bool is_physics_interpolated_and_enabled() const 🔗

Returns true if physics interpolation is enabled (see physics_interpolation_mode) and enabled in the SceneTree.

This is a convenience version of is_physics_interpolated() that also checks whether physics interpolation is enabled globally.

See SceneTree.physics_interpolation and ProjectSettings.physics/common/physics_interpolation.

bool is_physics_processing() const 🔗

Returns true if physics processing is enabled (see set_physics_process()).

bool is_physics_processing_internal() const 🔗

Returns true if internal physics processing is enabled (see set_physics_process_internal()).

bool is_processing() const 🔗

Returns true if processing is enabled (see set_process()).

bool is_processing_input() const 🔗

Returns true if the node is processing input (see set_process_input()).

bool is_processing_internal() const 🔗

Returns true if internal processing is enabled (see set_process_internal()).

bool is_processing_shortcut_input() const 🔗

Returns true if the node is processing shortcuts (see set_process_shortcut_input()).

bool is_processing_unhandled_input() const 🔗

Returns true if the node is processing unhandled input (see set_process_unhandled_input()).

bool is_processing_unhandled_key_input() const 🔗

Returns true if the node is processing unhandled key input (see set_process_unhandled_key_input()).

void move_child(child_node: Node, to_index: int) 🔗

Moves child_node to the given index. A node's index is the order among its siblings. If to_index is negative, the index is counted from the end of the list. See also get_child() and get_index().

Note: The processing order of several engine callbacks (_ready(), _process(), etc.) and notifications sent through propagate_notification() is affected by tree order. CanvasItem nodes are also rendered in tree order. See also process_priority.

void notify_deferred_thread_group(what: int) 🔗

Similar to call_deferred_thread_group(), but for notifications.

void notify_thread_safe(what: int) 🔗

Similar to call_thread_safe(), but for notifications.

void print_orphan_nodes() static 🔗

Prints all orphan nodes (nodes outside the SceneTree). Useful for debugging.

Note: This method only works in debug builds. Does nothing in a project exported in release mode.

Prints the node and its children to the console, recursively. The node does not have to be inside the tree. This method outputs NodePaths relative to this node, and is good for copy/pasting into get_node(). See also print_tree_pretty().

May print, for example:

void print_tree_pretty() 🔗

Prints the node and its children to the console, recursively. The node does not have to be inside the tree. Similar to print_tree(), but the graphical representation looks like what is displayed in the editor's Scene dock. It is useful for inspecting larger trees.

May print, for example:

void propagate_call(method: StringName, args: Array = [], parent_first: bool = false) 🔗

Calls the given method name, passing args as arguments, on this node and all of its children, recursively.

If parent_first is true, the method is called on this node first, then on all of its children. If false, the children's methods are called first.

void propagate_notification(what: int) 🔗

Calls Object.notification() with what on this node and all of its children, recursively.

void queue_accessibility_update() 🔗

Queues an accessibility information update for this node.

Queues this node to be deleted at the end of the current frame. When deleted, all of its children are deleted as well, and all references to the node and its children become invalid.

Unlike with Object.free(), the node is not deleted instantly, and it can still be accessed before deletion. It is also safe to call queue_free() multiple times. Use Object.is_queued_for_deletion() to check if the node will be deleted at the end of the frame.

Note: The node will only be freed after all other deferred calls are finished. Using this method is not always the same as calling Object.free() through Object.call_deferred().

void remove_child(node: Node) 🔗

Removes a child node. The node, along with its children, are not deleted. To delete a node, see queue_free().

Note: When this node is inside the tree, this method sets the owner of the removed node (or its descendants) to null, if their owner is no longer an ancestor (see is_ancestor_of()).

void remove_from_group(group: StringName) 🔗

Removes the node from the given group. Does nothing if the node is not in the group. See also notes in the description, and the SceneTree's group methods.

void reparent(new_parent: Node, keep_global_transform: bool = true) 🔗

Changes the parent of this Node to the new_parent. The node needs to already have a parent. The node's owner is preserved if its owner is still reachable from the new location (i.e., the node is still a descendant of the new parent after the operation).

If keep_global_transform is true, the node's global transform will be preserved if supported. Node2D, Node3D and Control support this argument (but Control keeps only position).

void replace_by(node: Node, keep_groups: bool = false) 🔗

Replaces this node by the given node. All children of this node are moved to node.

If keep_groups is true, the node is added to the same groups that the replaced node is in (see add_to_group()).

Warning: The replaced node is removed from the tree, but it is not deleted. To prevent memory leaks, store a reference to the node in a variable, or use Object.free().

void request_ready() 🔗

Requests _ready() to be called again the next time the node enters the tree. Does not immediately call _ready().

Note: This method only affects the current node. If the node's children also need to request ready, this method needs to be called for each one of them. When the node and its children enter the tree again, the order of _ready() callbacks will be the same as normal.

void reset_physics_interpolation() 🔗

When physics interpolation is active, moving a node to a radically different transform (such as placement within a level) can result in a visible glitch as the object is rendered moving from the old to new position over the physics tick.

That glitch can be prevented by calling this method, which temporarily disables interpolation until the physics tick is complete.

The notification NOTIFICATION_RESET_PHYSICS_INTERPOLATION will be received by the node and all children recursively.

Note: This function should be called after moving the node, rather than before.

Error rpc(method: StringName, ...) vararg 🔗

Sends a remote procedure call request for the given method to peers on the network (and locally), sending additional arguments to the method called by the RPC. The call request will only be received by nodes with the same NodePath, including the exact same name. Behavior depends on the RPC configuration for the given method (see rpc_config() and @GDScript.@rpc). By default, methods are not exposed to RPCs.

May return @GlobalScope.OK if the call is successful, @GlobalScope.ERR_INVALID_PARAMETER if the arguments passed in the method do not match, @GlobalScope.ERR_UNCONFIGURED if the node's multiplayer cannot be fetched (such as when the node is not inside the tree), @GlobalScope.ERR_CONNECTION_ERROR if multiplayer's connection is not available.

Note: You can only safely use RPCs on clients after you received the MultiplayerAPI.connected_to_server signal from the MultiplayerAPI. You also need to keep track of the connection state, either by the MultiplayerAPI signals like MultiplayerAPI.server_disconnected or by checking (get_multiplayer().peer.get_connection_status() == CONNECTION_CONNECTED).

void rpc_config(method: StringName, config: Variant) 🔗

Changes the RPC configuration for the given method. config should either be null to disable the feature (as by default), or a Dictionary containing the following entries:

rpc_mode: see RPCMode;

transfer_mode: see TransferMode;

call_local: if true, the method will also be called locally;

channel: an int representing the channel to send the RPC on.

Note: In GDScript, this method corresponds to the @GDScript.@rpc annotation, with various parameters passed (@rpc(any), @rpc(authority)...). See also the high-level multiplayer tutorial.

Error rpc_id(peer_id: int, method: StringName, ...) vararg 🔗

Sends a rpc() to a specific peer identified by peer_id (see MultiplayerPeer.set_target_peer()).

May return @GlobalScope.OK if the call is successful, @GlobalScope.ERR_INVALID_PARAMETER if the arguments passed in the method do not match, @GlobalScope.ERR_UNCONFIGURED if the node's multiplayer cannot be fetched (such as when the node is not inside the tree), @GlobalScope.ERR_CONNECTION_ERROR if multiplayer's connection is not available.

void set_deferred_thread_group(property: StringName, value: Variant) 🔗

Similar to call_deferred_thread_group(), but for setting properties.

void set_display_folded(fold: bool) 🔗

If set to true, the node appears folded in the Scene dock. As a result, all of its children are hidden. This method is intended to be used in editor plugins and tools, but it also works in release builds. See also is_displayed_folded().

void set_editable_instance(node: Node, is_editable: bool) 🔗

Set to true to allow all nodes owned by node to be available, and editable, in the Scene dock, even if their owner is not the scene root. This method is intended to be used in editor plugins and tools, but it also works in release builds. See also is_editable_instance().

void set_multiplayer_authority(id: int, recursive: bool = true) 🔗

Sets the node's multiplayer authority to the peer with the given peer id. The multiplayer authority is the peer that has authority over the node on the network. Defaults to peer ID 1 (the server). Useful in conjunction with rpc_config() and the MultiplayerAPI.

If recursive is true, the given peer is recursively set as the authority for all children of this node.

Warning: This does not automatically replicate the new authority to other peers. It is the developer's responsibility to do so. You may replicate the new authority's information using MultiplayerSpawner.spawn_function, an RPC, or a MultiplayerSynchronizer. Furthermore, the parent's authority does not propagate to newly added children.

void set_physics_process(enable: bool) 🔗

If set to true, enables physics (fixed framerate) processing. When a node is being processed, it will receive a NOTIFICATION_PHYSICS_PROCESS at a fixed (usually 60 FPS, see Engine.physics_ticks_per_second to change) interval (and the _physics_process() callback will be called if it exists).

Note: If _physics_process() is overridden, this will be automatically enabled before _ready() is called.

void set_physics_process_internal(enable: bool) 🔗

If set to true, enables internal physics for this node. Internal physics processing happens in isolation from the normal _physics_process() calls and is used by some nodes internally to guarantee proper functioning even if the node is paused or physics processing is disabled for scripting (set_physics_process()).

Warning: Built-in nodes rely on internal processing for their internal logic. Disabling it is unsafe and may lead to unexpected behavior. Use this method if you know what you are doing.

void set_process(enable: bool) 🔗

If set to true, enables processing. When a node is being processed, it will receive a NOTIFICATION_PROCESS on every drawn frame (and the _process() callback will be called if it exists).

Note: If _process() is overridden, this will be automatically enabled before _ready() is called.

Note: This method only affects the _process() callback, i.e. it has no effect on other callbacks like _physics_process(). If you want to disable all processing for the node, set process_mode to PROCESS_MODE_DISABLED.

void set_process_input(enable: bool) 🔗

If set to true, enables input processing.

Note: If _input() is overridden, this will be automatically enabled before _ready() is called. Input processing is also already enabled for GUI controls, such as Button and TextEdit.

void set_process_internal(enable: bool) 🔗

If set to true, enables internal processing for this node. Internal processing happens in isolation from the normal _process() calls and is used by some nodes internally to guarantee proper functioning even if the node is paused or processing is disabled for scripting (set_process()).

Warning: Built-in nodes rely on internal processing for their internal logic. Disabling it is unsafe and may lead to unexpected behavior. Use this method if you know what you are doing.

void set_process_shortcut_input(enable: bool) 🔗

If set to true, enables shortcut processing for this node.

Note: If _shortcut_input() is overridden, this will be automatically enabled before _ready() is called.

void set_process_unhandled_input(enable: bool) 🔗

If set to true, enables unhandled input processing. It enables the node to receive all input that was not previously handled (usually by a Control).

Note: If _unhandled_input() is overridden, this will be automatically enabled before _ready() is called. Unhandled input processing is also already enabled for GUI controls, such as Button and TextEdit.

void set_process_unhandled_key_input(enable: bool) 🔗

If set to true, enables unhandled key input processing.

Note: If _unhandled_key_input() is overridden, this will be automatically enabled before _ready() is called.

void set_scene_instance_load_placeholder(load_placeholder: bool) 🔗

If set to true, the node becomes an InstancePlaceholder when packed and instantiated from a PackedScene. See also get_scene_instance_load_placeholder().

void set_thread_safe(property: StringName, value: Variant) 🔗

Similar to call_thread_safe(), but for setting properties.

void set_translation_domain_inherited() 🔗

Makes this node inherit the translation domain from its parent node. If this node has no parent, the main translation domain will be used.

This is the default behavior for all nodes. Calling Object.set_translation_domain() disables this behavior.

void update_configuration_warnings() 🔗

Refreshes the warnings displayed for this node in the Scene dock. Use _get_configuration_warnings() to customize the warning messages to display.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (go):
```go
func _notification(what):
    if what == NOTIFICATION_TRANSLATION_CHANGED:
        if not is_node_ready():
            await ready # Wait until ready signal.
        $Label.text = atr("%d Bananas") % banana_counter
```

Example 2 (gdscript):
```gdscript
@export var energy = 0:
    set(value):
        energy = value
        update_configuration_warnings()

func _get_configuration_warnings():
    if energy < 0:
        return ["Energy must be 0 or greater."]
    else:
        return []
```

Example 3 (gdscript):
```gdscript
var child_node = get_child(0)
if child_node.get_parent():
    child_node.get_parent().remove_child(child_node)
add_child(child_node)
```

Example 4 (json):
```json
Node childNode = GetChild(0);
if (childNode.GetParent() != null)
{
    childNode.GetParent().RemoveChild(childNode);
}
AddChild(childNode);
```

---

## AspectRatioContainer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_aspectratiocontainer.html

**Contents:**
- AspectRatioContainer
- Description
- Tutorials
- Properties
- Enumerations
- Property Descriptions
- User-contributed notes

Inherits: Container < Control < CanvasItem < Node < Object

A container that preserves the proportions of its child controls.

A container type that arranges its child controls in a way that preserves their proportions automatically when the container is resized. Useful when a container has a dynamic size and the child nodes must adjust their sizes accordingly without losing their aspect ratios.

StretchMode STRETCH_WIDTH_CONTROLS_HEIGHT = 0

The height of child controls is automatically adjusted based on the width of the container.

StretchMode STRETCH_HEIGHT_CONTROLS_WIDTH = 1

The width of child controls is automatically adjusted based on the height of the container.

StretchMode STRETCH_FIT = 2

The bounding rectangle of child controls is automatically adjusted to fit inside the container while keeping the aspect ratio.

StretchMode STRETCH_COVER = 3

The width and height of child controls is automatically adjusted to make their bounding rectangle cover the entire area of the container while keeping the aspect ratio.

When the bounding rectangle of child controls exceed the container's size and Control.clip_contents is enabled, this allows to show only the container's area restricted by its own bounding rectangle.

enum AlignmentMode: 🔗

AlignmentMode ALIGNMENT_BEGIN = 0

Aligns child controls with the beginning (left or top) of the container.

AlignmentMode ALIGNMENT_CENTER = 1

Aligns child controls with the center of the container.

AlignmentMode ALIGNMENT_END = 2

Aligns child controls with the end (right or bottom) of the container.

AlignmentMode alignment_horizontal = 1 🔗

void set_alignment_horizontal(value: AlignmentMode)

AlignmentMode get_alignment_horizontal()

Specifies the horizontal relative position of child controls.

AlignmentMode alignment_vertical = 1 🔗

void set_alignment_vertical(value: AlignmentMode)

AlignmentMode get_alignment_vertical()

Specifies the vertical relative position of child controls.

void set_ratio(value: float)

The aspect ratio to enforce on child controls. This is the width divided by the height. The ratio depends on the stretch_mode.

StretchMode stretch_mode = 2 🔗

void set_stretch_mode(value: StretchMode)

StretchMode get_stretch_mode()

The stretch mode used to align child controls.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Bone2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_bone2d.html

**Contents:**
- Bone2D
- Description
- Properties
- Methods
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

A joint used with Skeleton2D to control and animate other nodes.

A hierarchy of Bone2Ds can be bound to a Skeleton2D to control and animate other Node2D nodes.

You can use Bone2D and Skeleton2D nodes to animate 2D meshes created with the Polygon2D UV editor.

Each bone has a rest transform that you can reset to with apply_rest(). These rest poses are relative to the bone's parent.

If in the editor, you can set the rest pose of an entire skeleton using a menu option, from the code, you need to iterate over the bones to set their individual rest poses.

Transform2D(0, 0, 0, 0, 0, 0)

get_autocalculate_length_and_angle() const

get_bone_angle() const

get_index_in_skeleton() const

get_skeleton_rest() const

set_autocalculate_length_and_angle(auto_calculate: bool)

set_bone_angle(angle: float)

set_length(length: float)

Transform2D rest = Transform2D(0, 0, 0, 0, 0, 0) 🔗

void set_rest(value: Transform2D)

Transform2D get_rest()

Rest transform of the bone. You can reset the node's transforms to this value using apply_rest().

Resets the bone to the rest pose. This is equivalent to setting Node2D.transform to rest.

bool get_autocalculate_length_and_angle() const 🔗

Returns whether this Bone2D is going to autocalculate its length and bone angle using its first Bone2D child node, if one exists. If there are no Bone2D children, then it cannot autocalculate these values and will print a warning.

float get_bone_angle() const 🔗

Returns the angle of the bone in the Bone2D.

Note: This is different from the Bone2D's rotation. The bone's angle is the rotation of the bone shown by the gizmo, which is unaffected by the Bone2D's Node2D.transform.

int get_index_in_skeleton() const 🔗

Returns the node's index as part of the entire skeleton. See Skeleton2D.

float get_length() const 🔗

Returns the length of the bone in the Bone2D node.

Transform2D get_skeleton_rest() const 🔗

Returns the node's rest Transform2D if it doesn't have a parent, or its rest pose relative to its parent.

void set_autocalculate_length_and_angle(auto_calculate: bool) 🔗

When set to true, the Bone2D node will attempt to automatically calculate the bone angle and length using the first child Bone2D node, if one exists. If none exist, the Bone2D cannot automatically calculate these values and will print a warning.

void set_bone_angle(angle: float) 🔗

Sets the bone angle for the Bone2D. This is typically set to the rotation from the Bone2D to a child Bone2D node.

Note: This is different from the Bone2D's rotation. The bone's angle is the rotation of the bone shown by the gizmo, which is unaffected by the Bone2D's Node2D.transform.

void set_length(length: float) 🔗

Sets the length of the bone in the Bone2D.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## BackBufferCopy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_backbuffercopy.html

**Contents:**
- BackBufferCopy
- Description
- Tutorials
- Properties
- Enumerations
- Property Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

A node that copies a region of the screen to a buffer for access in shader code.

Node for back-buffering the currently-displayed screen. The region defined in the BackBufferCopy node is buffered with the content of the screen it covers, or the entire screen according to the copy_mode. It can be accessed in shader scripts using the screen texture (i.e. a uniform sampler with hint_screen_texture).

Note: Since this node inherits from Node2D (and not Control), anchors and margins won't apply to child Control-derived nodes. This can be problematic when resizing the window. To avoid this, add Control-derived nodes as siblings to the BackBufferCopy node instead of adding them as children.

Screen-reading shaders

Rect2(-100, -100, 200, 200)

CopyMode COPY_MODE_DISABLED = 0

Disables the buffering mode. This means the BackBufferCopy node will directly use the portion of screen it covers.

CopyMode COPY_MODE_RECT = 1

BackBufferCopy buffers a rectangular region.

CopyMode COPY_MODE_VIEWPORT = 2

BackBufferCopy buffers the entire screen.

CopyMode copy_mode = 1 🔗

void set_copy_mode(value: CopyMode)

CopyMode get_copy_mode()

Rect2 rect = Rect2(-100, -100, 200, 200) 🔗

void set_rect(value: Rect2)

The area covered by the BackBufferCopy. Only used if copy_mode is COPY_MODE_RECT.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## BoneAttachment3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_boneattachment3d.html

**Contents:**
- BoneAttachment3D
- Description
- Properties
- Methods
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

А node that dynamically copies or overrides the 3D transform of a bone in its parent Skeleton3D.

This node selects a bone in a Skeleton3D and attaches to it. This means that the BoneAttachment3D node will either dynamically copy or override the 3D transform of the selected bone.

PhysicsInterpolationMode

physics_interpolation_mode

use_external_skeleton

void set_bone_idx(value: int)

The index of the attached bone.

String bone_name = "" 🔗

void set_bone_name(value: String)

String get_bone_name()

The name of the attached bone.

NodePath external_skeleton 🔗

void set_external_skeleton(value: NodePath)

NodePath get_external_skeleton()

The NodePath to the external Skeleton3D node.

bool override_pose = false 🔗

void set_override_pose(value: bool)

bool get_override_pose()

Whether the BoneAttachment3D node will override the bone pose of the bone it is attached to. When set to true, the BoneAttachment3D node can change the pose of the bone. When set to false, the BoneAttachment3D will always be set to the bone's transform.

Note: This override performs interruptively in the skeleton update process using signals due to the old design. It may cause unintended behavior when used at the same time with SkeletonModifier3D.

bool use_external_skeleton = false 🔗

void set_use_external_skeleton(value: bool)

bool get_use_external_skeleton()

Whether the BoneAttachment3D node will use an external Skeleton3D node rather than attempting to use its parent node as the Skeleton3D. When set to true, the BoneAttachment3D node will use the external Skeleton3D node set in external_skeleton.

Skeleton3D get_skeleton() 🔗

Returns the parent or external Skeleton3D node if it exists, otherwise returns null.

void on_skeleton_update() 🔗

A function that is called automatically when the Skeleton3D is updated. This function is where the BoneAttachment3D node updates its position so it is correctly bound when it is not set to override the bone pose.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## BoneConstraint3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_boneconstraint3d.html

**Contents:**
- BoneConstraint3D
- Description
- Methods
- Method Descriptions
- User-contributed notes

Inherits: SkeletonModifier3D < Node3D < Node < Object

Inherited By: AimModifier3D, ConvertTransformModifier3D, CopyTransformModifier3D

A node that may modify Skeleton3D's bone with associating the two bones.

Base class of SkeletonModifier3D that modifies the bone set in set_apply_bone() based on the transform of the bone retrieved by get_reference_bone().

get_amount(index: int) const

get_apply_bone(index: int) const

get_apply_bone_name(index: int) const

get_reference_bone(index: int) const

get_reference_bone_name(index: int) const

get_setting_count() const

set_amount(index: int, amount: float)

set_apply_bone(index: int, bone: int)

set_apply_bone_name(index: int, bone_name: String)

set_reference_bone(index: int, bone: int)

set_reference_bone_name(index: int, bone_name: String)

set_setting_count(count: int)

void clear_setting() 🔗

float get_amount(index: int) const 🔗

Returns the apply amount of the setting at index.

int get_apply_bone(index: int) const 🔗

Returns the apply bone of the setting at index. This bone will be modified.

String get_apply_bone_name(index: int) const 🔗

Returns the apply bone name of the setting at index. This bone will be modified.

int get_reference_bone(index: int) const 🔗

Returns the reference bone of the setting at index.

This bone will be only referenced and not modified by this modifier.

String get_reference_bone_name(index: int) const 🔗

Returns the reference bone name of the setting at index.

This bone will be only referenced and not modified by this modifier.

int get_setting_count() const 🔗

Returns the number of settings in the modifier.

void set_amount(index: int, amount: float) 🔗

Sets the apply amount of the setting at index to amount.

void set_apply_bone(index: int, bone: int) 🔗

Sets the apply bone of the setting at index to bone. This bone will be modified.

void set_apply_bone_name(index: int, bone_name: String) 🔗

Sets the apply bone of the setting at index to bone_name. This bone will be modified.

void set_reference_bone(index: int, bone: int) 🔗

Sets the reference bone of the setting at index to bone.

This bone will be only referenced and not modified by this modifier.

void set_reference_bone_name(index: int, bone_name: String) 🔗

Sets the reference bone of the setting at index to bone_name.

This bone will be only referenced and not modified by this modifier.

void set_setting_count(count: int) 🔗

Sets the number of settings in the modifier.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## BoxContainer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_boxcontainer.html

**Contents:**
- BoxContainer
- Description
- Tutorials
- Properties
- Methods
- Theme Properties
- Enumerations
- Property Descriptions
- Method Descriptions
- Theme Property Descriptions

Inherits: Container < Control < CanvasItem < Node < Object

Inherited By: HBoxContainer, VBoxContainer

A container that arranges its child controls horizontally or vertically.

A container that arranges its child controls horizontally or vertically, rearranging them automatically when their minimum size changes.

add_spacer(begin: bool)

enum AlignmentMode: 🔗

AlignmentMode ALIGNMENT_BEGIN = 0

The child controls will be arranged at the beginning of the container, i.e. top if orientation is vertical, left if orientation is horizontal (right for RTL layout).

AlignmentMode ALIGNMENT_CENTER = 1

The child controls will be centered in the container.

AlignmentMode ALIGNMENT_END = 2

The child controls will be arranged at the end of the container, i.e. bottom if orientation is vertical, right if orientation is horizontal (left for RTL layout).

AlignmentMode alignment = 0 🔗

void set_alignment(value: AlignmentMode)

AlignmentMode get_alignment()

The alignment of the container's children (must be one of ALIGNMENT_BEGIN, ALIGNMENT_CENTER, or ALIGNMENT_END).

bool vertical = false 🔗

void set_vertical(value: bool)

If true, the BoxContainer will arrange its children vertically, rather than horizontally.

Can't be changed when using HBoxContainer and VBoxContainer.

Control add_spacer(begin: bool) 🔗

Adds a Control node to the box as a spacer. If begin is true, it will insert the Control node in front of all other children.

The space between the BoxContainer's elements, in pixels.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Camera3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_camera3d.html

**Contents:**
- Camera3D
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node3D < Node < Object

Inherited By: XRCamera3D

Camera node, displays from a point of view.

Camera3D is a special node that displays what is visible from its current location. Cameras register themselves in the nearest Viewport node (when ascending the tree). Only one camera can be active per viewport. If no viewport is available ascending the tree, the camera will register in the global viewport. In other words, a camera just provides 3D display capabilities to a Viewport, and, without one, a scene registered in that Viewport (or higher viewports) can't be displayed.

Third Person Shooter (TPS) Demo

clear_current(enable_next: bool = true)

get_camera_projection() const

get_camera_rid() const

get_camera_transform() const

get_cull_mask_value(layer_number: int) const

get_pyramid_shape_rid()

is_position_behind(world_point: Vector3) const

is_position_in_frustum(world_point: Vector3) const

project_local_ray_normal(screen_point: Vector2) const

project_position(screen_point: Vector2, z_depth: float) const

project_ray_normal(screen_point: Vector2) const

project_ray_origin(screen_point: Vector2) const

set_cull_mask_value(layer_number: int, value: bool)

set_frustum(size: float, offset: Vector2, z_near: float, z_far: float)

set_orthogonal(size: float, z_near: float, z_far: float)

set_perspective(fov: float, z_near: float, z_far: float)

unproject_position(world_point: Vector3) const

enum ProjectionType: 🔗

ProjectionType PROJECTION_PERSPECTIVE = 0

Perspective projection. Objects on the screen becomes smaller when they are far away.

ProjectionType PROJECTION_ORTHOGONAL = 1

Orthogonal projection, also known as orthographic projection. Objects remain the same size on the screen no matter how far away they are.

ProjectionType PROJECTION_FRUSTUM = 2

Frustum projection. This mode allows adjusting frustum_offset to create "tilted frustum" effects.

KeepAspect KEEP_WIDTH = 0

Preserves the horizontal aspect ratio; also known as Vert- scaling. This is usually the best option for projects running in portrait mode, as taller aspect ratios will benefit from a wider vertical FOV.

KeepAspect KEEP_HEIGHT = 1

Preserves the vertical aspect ratio; also known as Hor+ scaling. This is usually the best option for projects running in landscape mode, as wider aspect ratios will automatically benefit from a wider horizontal FOV.

enum DopplerTracking: 🔗

DopplerTracking DOPPLER_TRACKING_DISABLED = 0

Disables Doppler effect simulation (default).

DopplerTracking DOPPLER_TRACKING_IDLE_STEP = 1

Simulate Doppler effect by tracking positions of objects that are changed in _process. Changes in the relative velocity of this camera compared to those objects affect how audio is perceived (changing the audio's AudioStreamPlayer3D.pitch_scale).

DopplerTracking DOPPLER_TRACKING_PHYSICS_STEP = 2

Simulate Doppler effect by tracking positions of objects that are changed in _physics_process. Changes in the relative velocity of this camera compared to those objects affect how audio is perceived (changing the audio's AudioStreamPlayer3D.pitch_scale).

CameraAttributes attributes 🔗

void set_attributes(value: CameraAttributes)

CameraAttributes get_attributes()

The CameraAttributes to use for this camera.

Compositor compositor 🔗

void set_compositor(value: Compositor)

Compositor get_compositor()

The Compositor to use for this camera.

int cull_mask = 1048575 🔗

void set_cull_mask(value: int)

The culling mask that describes which VisualInstance3D.layers are rendered by this camera. By default, all 20 user-visible layers are rendered.

Note: Since the cull_mask allows for 32 layers to be stored in total, there are an additional 12 layers that are only used internally by the engine and aren't exposed in the editor. Setting cull_mask using a script allows you to toggle those reserved layers, which can be useful for editor plugins.

To adjust cull_mask more easily using a script, use get_cull_mask_value() and set_cull_mask_value().

Note: VoxelGI, SDFGI and LightmapGI will always take all layers into account to determine what contributes to global illumination. If this is an issue, set GeometryInstance3D.gi_mode to GeometryInstance3D.GI_MODE_DISABLED for meshes and Light3D.light_bake_mode to Light3D.BAKE_DISABLED for lights to exclude them from global illumination.

bool current = false 🔗

void set_current(value: bool)

If true, the ancestor Viewport is currently using this camera.

If multiple cameras are in the scene, one will always be made current. For example, if two Camera3D nodes are present in the scene and only one is current, setting one camera's current to false will cause the other camera to be made current.

DopplerTracking doppler_tracking = 0 🔗

void set_doppler_tracking(value: DopplerTracking)

DopplerTracking get_doppler_tracking()

If not DOPPLER_TRACKING_DISABLED, this camera will simulate the Doppler effect for objects changed in particular _process methods.

Note: The Doppler effect will only be heard on AudioStreamPlayer3Ds if AudioStreamPlayer3D.doppler_tracking is not set to AudioStreamPlayer3D.DOPPLER_TRACKING_DISABLED.

Environment environment 🔗

void set_environment(value: Environment)

Environment get_environment()

The Environment to use for this camera.

void set_far(value: float)

The distance to the far culling boundary for this camera relative to its local Z axis. Higher values allow the camera to see further away, while decreasing far can improve performance if it results in objects being partially or fully culled.

void set_fov(value: float)

The camera's field of view angle (in degrees). Only applicable in perspective mode. Since keep_aspect locks one axis, fov sets the other axis' field of view angle.

For reference, the default vertical field of view value (75.0) is equivalent to a horizontal FOV of:

~91.31 degrees in a 4:3 viewport

~101.67 degrees in a 16:10 viewport

~107.51 degrees in a 16:9 viewport

~121.63 degrees in a 21:9 viewport

Vector2 frustum_offset = Vector2(0, 0) 🔗

void set_frustum_offset(value: Vector2)

Vector2 get_frustum_offset()

The camera's frustum offset. This can be changed from the default to create "tilted frustum" effects such as Y-shearing.

Note: Only effective if projection is PROJECTION_FRUSTUM.

float h_offset = 0.0 🔗

void set_h_offset(value: float)

The horizontal (X) offset of the camera viewport.

KeepAspect keep_aspect = 1 🔗

void set_keep_aspect_mode(value: KeepAspect)

KeepAspect get_keep_aspect_mode()

The axis to lock during fov/size adjustments. Can be either KEEP_WIDTH or KEEP_HEIGHT.

void set_near(value: float)

The distance to the near culling boundary for this camera relative to its local Z axis. Lower values allow the camera to see objects more up close to its origin, at the cost of lower precision across the entire range. Values lower than the default can lead to increased Z-fighting.

ProjectionType projection = 0 🔗

void set_projection(value: ProjectionType)

ProjectionType get_projection()

The camera's projection mode. In PROJECTION_PERSPECTIVE mode, objects' Z distance from the camera's local space scales their perceived size.

void set_size(value: float)

The camera's size in meters measured as the diameter of the width or height, depending on keep_aspect. Only applicable in orthogonal and frustum modes.

float v_offset = 0.0 🔗

void set_v_offset(value: float)

The vertical (Y) offset of the camera viewport.

void clear_current(enable_next: bool = true) 🔗

If this is the current camera, remove it from being current. If enable_next is true, request to make the next camera current, if any.

Projection get_camera_projection() const 🔗

Returns the projection matrix that this camera uses to render to its associated viewport. The camera must be part of the scene tree to function.

RID get_camera_rid() const 🔗

Returns the camera's RID from the RenderingServer.

Transform3D get_camera_transform() const 🔗

Returns the transform of the camera plus the vertical (v_offset) and horizontal (h_offset) offsets; and any other adjustments made to the position and orientation of the camera by subclassed cameras such as XRCamera3D.

bool get_cull_mask_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the cull_mask is enabled, given a layer_number between 1 and 20.

Array[Plane] get_frustum() const 🔗

Returns the camera's frustum planes in world space units as an array of Planes in the following order: near, far, left, top, right, bottom. Not to be confused with frustum_offset.

RID get_pyramid_shape_rid() 🔗

Returns the RID of a pyramid shape encompassing the camera's view frustum, ignoring the camera's near plane. The tip of the pyramid represents the position of the camera.

bool is_position_behind(world_point: Vector3) const 🔗

Returns true if the given position is behind the camera (the blue part of the linked diagram). See this diagram for an overview of position query methods.

Note: A position which returns false may still be outside the camera's field of view.

bool is_position_in_frustum(world_point: Vector3) const 🔗

Returns true if the given position is inside the camera's frustum (the green part of the linked diagram). See this diagram for an overview of position query methods.

void make_current() 🔗

Makes this camera the current camera for the Viewport (see class description). If the camera node is outside the scene tree, it will attempt to become current once it's added.

Vector3 project_local_ray_normal(screen_point: Vector2) const 🔗

Returns a normal vector from the screen point location directed along the camera. Orthogonal cameras are normalized. Perspective cameras account for perspective, screen width/height, etc.

Vector3 project_position(screen_point: Vector2, z_depth: float) const 🔗

Returns the 3D point in world space that maps to the given 2D coordinate in the Viewport rectangle on a plane that is the given z_depth distance into the scene away from the camera.

Vector3 project_ray_normal(screen_point: Vector2) const 🔗

Returns a normal vector in world space, that is the result of projecting a point on the Viewport rectangle by the inverse camera projection. This is useful for casting rays in the form of (origin, normal) for object intersection or picking.

Vector3 project_ray_origin(screen_point: Vector2) const 🔗

Returns a 3D position in world space, that is the result of projecting a point on the Viewport rectangle by the inverse camera projection. This is useful for casting rays in the form of (origin, normal) for object intersection or picking.

void set_cull_mask_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the cull_mask, given a layer_number between 1 and 20.

void set_frustum(size: float, offset: Vector2, z_near: float, z_far: float) 🔗

Sets the camera projection to frustum mode (see PROJECTION_FRUSTUM), by specifying a size, an offset, and the z_near and z_far clip planes in world space units. See also frustum_offset.

void set_orthogonal(size: float, z_near: float, z_far: float) 🔗

Sets the camera projection to orthogonal mode (see PROJECTION_ORTHOGONAL), by specifying a size, and the z_near and z_far clip planes in world space units.

As a hint, 3D games that look 2D often use this projection, with size specified in pixels.

void set_perspective(fov: float, z_near: float, z_far: float) 🔗

Sets the camera projection to perspective mode (see PROJECTION_PERSPECTIVE), by specifying a fov (field of view) angle in degrees, and the z_near and z_far clip planes in world space units.

Vector2 unproject_position(world_point: Vector3) const 🔗

Returns the 2D coordinate in the Viewport rectangle that maps to the given 3D point in world space.

Note: When using this to position GUI elements over a 3D viewport, use is_position_behind() to prevent them from appearing if the 3D point is behind the camera:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
# This code block is part of a script that inherits from Node3D.
# `control` is a reference to a node inheriting from Control.
control.visible = not get_viewport().get_camera_3d().is_position_behind(global_transform.origin)
control.position = get_viewport().get_camera_3d().unproject_position(global_transform.origin)
```

---

## Camera2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_camera2d.html

**Contents:**
- Camera2D
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

Camera node for 2D scenes.

Camera node for 2D scenes. It forces the screen (current layer) to scroll following this node. This makes it easier (and faster) to program scrollable scenes than manually changing the position of CanvasItem-based nodes.

Cameras register themselves in the nearest Viewport node (when ascending the tree). Only one camera can be active per viewport. If no viewport is available ascending the tree, the camera will register in the global viewport.

This node is intended to be a simple helper to get things going quickly, but more functionality may be desired to change how the camera works. To make your own custom camera node, inherit it from Node2D and change the transform of the canvas by setting Viewport.canvas_transform in Viewport (you can obtain the current Viewport by using Node.get_viewport()).

Note that the Camera2D node's Node2D.global_position doesn't represent the actual position of the screen, which may differ due to applied smoothing or limits. You can use get_screen_center_position() to get the real position. Same for the node's Node2D.global_rotation which may be different due to applied rotation smoothing. You can use get_screen_rotation() to get the current rotation of the screen.

drag_horizontal_enabled

drag_horizontal_offset

drag_vertical_enabled

editor_draw_drag_margin

position_smoothing_enabled

position_smoothing_speed

Camera2DProcessCallback

rotation_smoothing_enabled

rotation_smoothing_speed

force_update_scroll()

get_drag_margin(margin: Side) const

get_limit(margin: Side) const

get_screen_center_position() const

get_screen_rotation() const

get_target_position() const

set_drag_margin(margin: Side, drag_margin: float)

set_limit(margin: Side, limit: int)

AnchorMode ANCHOR_MODE_FIXED_TOP_LEFT = 0

The camera's position is fixed so that the top-left corner is always at the origin.

AnchorMode ANCHOR_MODE_DRAG_CENTER = 1

The camera's position takes into account vertical/horizontal offsets and the screen size.

enum Camera2DProcessCallback: 🔗

Camera2DProcessCallback CAMERA2D_PROCESS_PHYSICS = 0

The camera updates during physics frames (see Node.NOTIFICATION_INTERNAL_PHYSICS_PROCESS).

Camera2DProcessCallback CAMERA2D_PROCESS_IDLE = 1

The camera updates during process frames (see Node.NOTIFICATION_INTERNAL_PROCESS).

AnchorMode anchor_mode = 1 🔗

void set_anchor_mode(value: AnchorMode)

AnchorMode get_anchor_mode()

The Camera2D's anchor point.

Node custom_viewport 🔗

void set_custom_viewport(value: Node)

Node get_custom_viewport()

The custom Viewport node attached to the Camera2D. If null or not a Viewport, uses the default viewport instead.

float drag_bottom_margin = 0.2 🔗

void set_drag_margin(margin: Side, drag_margin: float)

float get_drag_margin(margin: Side) const

Bottom margin needed to drag the camera. A value of 1 makes the camera move only when reaching the bottom edge of the screen.

bool drag_horizontal_enabled = false 🔗

void set_drag_horizontal_enabled(value: bool)

bool is_drag_horizontal_enabled()

If true, the camera only moves when reaching the horizontal (left and right) drag margins. If false, the camera moves horizontally regardless of margins.

float drag_horizontal_offset = 0.0 🔗

void set_drag_horizontal_offset(value: float)

float get_drag_horizontal_offset()

The relative horizontal drag offset of the camera between the right (-1) and left (1) drag margins.

Note: Used to set the initial horizontal drag offset; determine the current offset; or force the current offset. It's not automatically updated when drag_horizontal_enabled is true or the drag margins are changed.

float drag_left_margin = 0.2 🔗

void set_drag_margin(margin: Side, drag_margin: float)

float get_drag_margin(margin: Side) const

Left margin needed to drag the camera. A value of 1 makes the camera move only when reaching the left edge of the screen.

float drag_right_margin = 0.2 🔗

void set_drag_margin(margin: Side, drag_margin: float)

float get_drag_margin(margin: Side) const

Right margin needed to drag the camera. A value of 1 makes the camera move only when reaching the right edge of the screen.

float drag_top_margin = 0.2 🔗

void set_drag_margin(margin: Side, drag_margin: float)

float get_drag_margin(margin: Side) const

Top margin needed to drag the camera. A value of 1 makes the camera move only when reaching the top edge of the screen.

bool drag_vertical_enabled = false 🔗

void set_drag_vertical_enabled(value: bool)

bool is_drag_vertical_enabled()

If true, the camera only moves when reaching the vertical (top and bottom) drag margins. If false, the camera moves vertically regardless of the drag margins.

float drag_vertical_offset = 0.0 🔗

void set_drag_vertical_offset(value: float)

float get_drag_vertical_offset()

The relative vertical drag offset of the camera between the bottom (-1) and top (1) drag margins.

Note: Used to set the initial vertical drag offset; determine the current offset; or force the current offset. It's not automatically updated when drag_vertical_enabled is true or the drag margins are changed.

bool editor_draw_drag_margin = false 🔗

void set_margin_drawing_enabled(value: bool)

bool is_margin_drawing_enabled()

If true, draws the camera's drag margin rectangle in the editor.

bool editor_draw_limits = false 🔗

void set_limit_drawing_enabled(value: bool)

bool is_limit_drawing_enabled()

If true, draws the camera's limits rectangle in the editor.

bool editor_draw_screen = true 🔗

void set_screen_drawing_enabled(value: bool)

bool is_screen_drawing_enabled()

If true, draws the camera's screen rectangle in the editor.

bool enabled = true 🔗

void set_enabled(value: bool)

Controls whether the camera can be active or not. If true, the Camera2D will become the main camera when it enters the scene tree and there is no active camera currently (see Viewport.get_camera_2d()).

When the camera is currently active and enabled is set to false, the next enabled Camera2D in the scene tree will become active.

bool ignore_rotation = true 🔗

void set_ignore_rotation(value: bool)

bool is_ignoring_rotation()

If true, the camera's rendered view is not affected by its Node2D.rotation and Node2D.global_rotation.

int limit_bottom = 10000000 🔗

void set_limit(margin: Side, limit: int)

int get_limit(margin: Side) const

Bottom scroll limit in pixels. The camera stops moving when reaching this value, but offset can push the view past the limit.

bool limit_enabled = true 🔗

void set_limit_enabled(value: bool)

bool is_limit_enabled()

If true, the limits will be enabled. Disabling this will allow the camera to focus anywhere, when the four limit_* properties will not work.

int limit_left = -10000000 🔗

void set_limit(margin: Side, limit: int)

int get_limit(margin: Side) const

Left scroll limit in pixels. The camera stops moving when reaching this value, but offset can push the view past the limit.

int limit_right = 10000000 🔗

void set_limit(margin: Side, limit: int)

int get_limit(margin: Side) const

Right scroll limit in pixels. The camera stops moving when reaching this value, but offset can push the view past the limit.

bool limit_smoothed = false 🔗

void set_limit_smoothing_enabled(value: bool)

bool is_limit_smoothing_enabled()

If true, the camera smoothly stops when reaches its limits.

This property has no effect if position_smoothing_enabled is false.

Note: To immediately update the camera's position to be within limits without smoothing, even with this setting enabled, invoke reset_smoothing().

int limit_top = -10000000 🔗

void set_limit(margin: Side, limit: int)

int get_limit(margin: Side) const

Top scroll limit in pixels. The camera stops moving when reaching this value, but offset can push the view past the limit.

Vector2 offset = Vector2(0, 0) 🔗

void set_offset(value: Vector2)

The camera's relative offset. Useful for looking around or camera shake animations. The offsetted camera can go past the limits defined in limit_top, limit_bottom, limit_left and limit_right.

bool position_smoothing_enabled = false 🔗

void set_position_smoothing_enabled(value: bool)

bool is_position_smoothing_enabled()

If true, the camera's view smoothly moves towards its target position at position_smoothing_speed.

float position_smoothing_speed = 5.0 🔗

void set_position_smoothing_speed(value: float)

float get_position_smoothing_speed()

Speed in pixels per second of the camera's smoothing effect when position_smoothing_enabled is true.

Camera2DProcessCallback process_callback = 1 🔗

void set_process_callback(value: Camera2DProcessCallback)

Camera2DProcessCallback get_process_callback()

The camera's process callback.

bool rotation_smoothing_enabled = false 🔗

void set_rotation_smoothing_enabled(value: bool)

bool is_rotation_smoothing_enabled()

If true, the camera's view smoothly rotates, via asymptotic smoothing, to align with its target rotation at rotation_smoothing_speed.

Note: This property has no effect if ignore_rotation is true.

float rotation_smoothing_speed = 5.0 🔗

void set_rotation_smoothing_speed(value: float)

float get_rotation_smoothing_speed()

The angular, asymptotic speed of the camera's rotation smoothing effect when rotation_smoothing_enabled is true.

Vector2 zoom = Vector2(1, 1) 🔗

void set_zoom(value: Vector2)

The camera's zoom. Higher values are more zoomed in. For example, a zoom of Vector2(2.0, 2.0) will be twice as zoomed in on each axis (the view covers an area four times smaller). In contrast, a zoom of Vector2(0.5, 0.5) will be twice as zoomed out on each axis (the view covers an area four times larger). The X and Y components should generally always be set to the same value, unless you wish to stretch the camera view.

Note: FontFile.oversampling does not take Camera2D zoom into account. This means that zooming in/out will cause bitmap fonts and rasterized (non-MSDF) dynamic fonts to appear blurry or pixelated unless the font is part of a CanvasLayer that makes it ignore camera zoom. To ensure text remains crisp regardless of zoom, you can enable MSDF font rendering by enabling ProjectSettings.gui/theme/default_font_multichannel_signed_distance_field (applies to the default project font only), or enabling Multichannel Signed Distance Field in the import options of a DynamicFont for custom fonts. On system fonts, SystemFont.multichannel_signed_distance_field can be enabled in the inspector.

Aligns the camera to the tracked node.

void force_update_scroll() 🔗

Forces the camera to update scroll immediately.

float get_drag_margin(margin: Side) const 🔗

Returns the specified Side's margin. See also drag_bottom_margin, drag_top_margin, drag_left_margin, and drag_right_margin.

int get_limit(margin: Side) const 🔗

Returns the camera limit for the specified Side. See also limit_bottom, limit_top, limit_left, and limit_right.

Vector2 get_screen_center_position() const 🔗

Returns the center of the screen from this camera's point of view, in global coordinates.

Note: The exact targeted position of the camera may be different. See get_target_position().

float get_screen_rotation() const 🔗

Returns the current screen rotation from this camera's point of view.

Note: The screen rotation can be different from Node2D.global_rotation if the camera is rotating smoothly due to rotation_smoothing_enabled.

Vector2 get_target_position() const 🔗

Returns this camera's target position, in global coordinates.

Note: The returned value is not the same as Node2D.global_position, as it is affected by the drag properties. It is also not the same as the current position if position_smoothing_enabled is true (see get_screen_center_position()).

bool is_current() const 🔗

Returns true if this Camera2D is the active camera (see Viewport.get_camera_2d()).

void make_current() 🔗

Forces this Camera2D to become the current active one. enabled must be true.

void reset_smoothing() 🔗

Sets the camera's position immediately to its current smoothing destination.

This method has no effect if position_smoothing_enabled is false.

void set_drag_margin(margin: Side, drag_margin: float) 🔗

Sets the specified Side's margin. See also drag_bottom_margin, drag_top_margin, drag_left_margin, and drag_right_margin.

void set_limit(margin: Side, limit: int) 🔗

Sets the camera limit for the specified Side. See also limit_bottom, limit_top, limit_left, and limit_right.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CheckButton — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_checkbutton.html

**Contents:**
- CheckButton
- Description
- Properties
- Theme Properties
- Theme Property Descriptions
- User-contributed notes

Inherits: Button < BaseButton < Control < CanvasItem < Node < Object

A button that represents a binary choice.

CheckButton is a toggle button displayed as a check field. It's similar to CheckBox in functionality, but it has a different appearance. To follow established UX patterns, it's recommended to use CheckButton when toggling it has an immediate effect on something. For example, it can be used when pressing it shows or hides advanced settings, without asking the user to confirm this action.

See also BaseButton which contains common properties and methods associated with this node.

true (overrides BaseButton)

button_unchecked_color

checked_disabled_mirrored

unchecked_disabled_mirrored

Color button_checked_color = Color(1, 1, 1, 1) 🔗

The color of the checked icon when the checkbox is pressed.

Color button_unchecked_color = Color(1, 1, 1, 1) 🔗

The color of the unchecked icon when the checkbox is not pressed.

int check_v_offset = 0 🔗

The vertical offset used when rendering the toggle icons (in pixels).

The icon to display when the CheckButton is checked (for left-to-right layouts).

Texture2D checked_disabled 🔗

The icon to display when the CheckButton is checked and disabled (for left-to-right layouts).

Texture2D checked_disabled_mirrored 🔗

The icon to display when the CheckButton is checked and disabled (for right-to-left layouts).

Texture2D checked_mirrored 🔗

The icon to display when the CheckButton is checked (for right-to-left layouts).

Texture2D unchecked 🔗

The icon to display when the CheckButton is unchecked (for left-to-right layouts).

Texture2D unchecked_disabled 🔗

The icon to display when the CheckButton is unchecked and disabled (for left-to-right layouts).

Texture2D unchecked_disabled_mirrored 🔗

The icon to display when the CheckButton is unchecked and disabled (for right-to-left layouts).

Texture2D unchecked_mirrored 🔗

The icon to display when the CheckButton is unchecked (for right-to-left layouts).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CenterContainer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_centercontainer.html

**Contents:**
- CenterContainer
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Container < Control < CanvasItem < Node < Object

A container that keeps child controls in its center.

CenterContainer is a container that keeps all of its child controls in its center at their minimum size.

bool use_top_left = false 🔗

void set_use_top_left(value: bool)

bool is_using_top_left()

If true, centers children relative to the CenterContainer's top left corner.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CodeEdit — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_codeedit.html

**Contents:**
- CodeEdit
- Description
- Properties
- Methods
- Theme Properties
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- Theme Property Descriptions

Inherits: TextEdit < Control < CanvasItem < Node < Object

A multiline text editor designed for editing code.

CodeEdit is a specialized TextEdit designed for editing plain text code files. It has many features commonly found in code editors such as line numbers, line folding, code completion, indent management, and string/comment management.

Note: Regardless of locale, CodeEdit will by default always use left-to-right text direction to correctly display source code.

auto_brace_completion_enabled

auto_brace_completion_highlight_matching

auto_brace_completion_pairs

{ "\"": "\"", "'": "'", "(": ")", "[": "]", "{": "}" }

code_completion_enabled

code_completion_prefixes

gutters_draw_bookmarks

gutters_draw_breakpoints_gutter

gutters_draw_executing_lines

gutters_draw_fold_gutter

gutters_draw_line_numbers

gutters_zero_pad_line_numbers

indent_automatic_prefixes

2 (overrides Control)

line_length_guidelines

symbol_lookup_on_click

symbol_tooltip_on_hover

1 (overrides TextEdit)

_confirm_code_completion(replace: bool) virtual

_filter_code_completion_candidates(candidates: Array[Dictionary]) virtual const

_request_code_completion(force: bool) virtual

add_auto_brace_completion_pair(start_key: String, end_key: String)

add_code_completion_option(type: CodeCompletionKind, display_text: String, insert_text: String, text_color: Color = Color(1, 1, 1, 1), icon: Resource = null, value: Variant = null, location: int = 1024)

add_comment_delimiter(start_key: String, end_key: String, line_only: bool = false)

add_string_delimiter(start_key: String, end_key: String, line_only: bool = false)

can_fold_line(line: int) const

cancel_code_completion()

clear_bookmarked_lines()

clear_breakpointed_lines()

clear_comment_delimiters()

clear_executing_lines()

clear_string_delimiters()

confirm_code_completion(replace: bool = false)

convert_indent(from_line: int = -1, to_line: int = -1)

duplicate_selection()

get_auto_brace_completion_close_key(open_key: String) const

get_bookmarked_lines() const

get_breakpointed_lines() const

get_code_completion_option(index: int) const

get_code_completion_options() const

get_code_completion_selected_index() const

get_code_region_end_tag() const

get_code_region_start_tag() const

get_delimiter_end_key(delimiter_index: int) const

get_delimiter_end_position(line: int, column: int) const

get_delimiter_start_key(delimiter_index: int) const

get_delimiter_start_position(line: int, column: int) const

get_executing_lines() const

get_folded_lines() const

get_text_for_code_completion() const

get_text_for_symbol_lookup() const

get_text_with_cursor_char(line: int, column: int) const

has_auto_brace_completion_close_key(close_key: String) const

has_auto_brace_completion_open_key(open_key: String) const

has_comment_delimiter(start_key: String) const

has_string_delimiter(start_key: String) const

is_in_comment(line: int, column: int = -1) const

is_in_string(line: int, column: int = -1) const

is_line_bookmarked(line: int) const

is_line_breakpointed(line: int) const

is_line_code_region_end(line: int) const

is_line_code_region_start(line: int) const

is_line_executing(line: int) const

is_line_folded(line: int) const

remove_comment_delimiter(start_key: String)

remove_string_delimiter(start_key: String)

request_code_completion(force: bool = false)

set_code_completion_selected_index(index: int)

set_code_hint(code_hint: String)

set_code_hint_draw_below(draw_below: bool)

set_code_region_tags(start: String = "region", end: String = "endregion")

set_line_as_bookmarked(line: int, bookmarked: bool)

set_line_as_breakpoint(line: int, breakpointed: bool)

set_line_as_executing(line: int, executing: bool)

set_symbol_lookup_word_as_valid(valid: bool)

toggle_foldable_line(line: int)

toggle_foldable_lines_at_carets()

unfold_line(line: int)

update_code_completion_options(force: bool)

Color(0.5, 0.64, 1, 0.8)

Color(1, 0.2, 0.2, 1)

Color(0.9, 0.29, 0.3, 1)

Color(0.8, 0.8, 0.8, 0.8)

completion_background_color

Color(0.17, 0.16, 0.2, 1)

completion_existing_color

Color(0.87, 0.87, 0.87, 0.13)

completion_scroll_color

completion_scroll_hovered_color

completion_selected_color

Color(0.26, 0.26, 0.27, 1)

Color(0.98, 0.89, 0.27, 1)

folded_code_region_color

Color(0.68, 0.46, 0.77, 0.2)

line_length_guideline_color

Color(0.3, 0.5, 0.8, 0.1)

Color(0.67, 0.67, 0.67, 0.4)

completion_scroll_width

breakpoint_toggled(line: int) 🔗

Emitted when a breakpoint is added or removed from a line. If the line is removed via backspace, a signal is emitted at the old line.

code_completion_requested() 🔗

Emitted when the user requests code completion. This signal will not be sent if _request_code_completion() is overridden or code_completion_enabled is false.

symbol_hovered(symbol: String, line: int, column: int) 🔗

Emitted when the user hovers over a symbol. Unlike Control.mouse_entered, this signal is not emitted immediately, but when the cursor is over the symbol for ProjectSettings.gui/timers/tooltip_delay_sec seconds.

Note: symbol_tooltip_on_hover must be true for this signal to be emitted.

symbol_lookup(symbol: String, line: int, column: int) 🔗

Emitted when the user has clicked on a valid symbol.

symbol_validate(symbol: String) 🔗

Emitted when the user hovers over a symbol. The symbol should be validated and responded to, by calling set_symbol_lookup_word_as_valid().

Note: symbol_lookup_on_click must be true for this signal to be emitted.

enum CodeCompletionKind: 🔗

CodeCompletionKind KIND_CLASS = 0

Marks the option as a class.

CodeCompletionKind KIND_FUNCTION = 1

Marks the option as a function.

CodeCompletionKind KIND_SIGNAL = 2

Marks the option as a Godot signal.

CodeCompletionKind KIND_VARIABLE = 3

Marks the option as a variable.

CodeCompletionKind KIND_MEMBER = 4

Marks the option as a member.

CodeCompletionKind KIND_ENUM = 5

Marks the option as an enum entry.

CodeCompletionKind KIND_CONSTANT = 6

Marks the option as a constant.

CodeCompletionKind KIND_NODE_PATH = 7

Marks the option as a Godot node path.

CodeCompletionKind KIND_FILE_PATH = 8

Marks the option as a file path.

CodeCompletionKind KIND_PLAIN_TEXT = 9

Marks the option as unclassified or plain text.

enum CodeCompletionLocation: 🔗

CodeCompletionLocation LOCATION_LOCAL = 0

The option is local to the location of the code completion query - e.g. a local variable. Subsequent value of location represent options from the outer class, the exact value represent how far they are (in terms of inner classes).

CodeCompletionLocation LOCATION_PARENT_MASK = 256

The option is from the containing class or a parent class, relative to the location of the code completion query. Perform a bitwise OR with the class depth (e.g. 0 for the local class, 1 for the parent, 2 for the grandparent, etc.) to store the depth of an option in the class or a parent class.

CodeCompletionLocation LOCATION_OTHER_USER_CODE = 512

The option is from user code which is not local and not in a derived class (e.g. Autoload Singletons).

CodeCompletionLocation LOCATION_OTHER = 1024

The option is from other engine code, not covered by the other enum constants - e.g. built-in classes.

bool auto_brace_completion_enabled = false 🔗

void set_auto_brace_completion_enabled(value: bool)

bool is_auto_brace_completion_enabled()

If true, uses auto_brace_completion_pairs to automatically insert the closing brace when the opening brace is inserted by typing or autocompletion. Also automatically removes the closing brace when using backspace on the opening brace.

bool auto_brace_completion_highlight_matching = false 🔗

void set_highlight_matching_braces_enabled(value: bool)

bool is_highlight_matching_braces_enabled()

If true, highlights brace pairs when the caret is on either one, using auto_brace_completion_pairs. If matching, the pairs will be underlined. If a brace is unmatched, it is colored with brace_mismatch_color.

Dictionary auto_brace_completion_pairs = { "\"": "\"", "'": "'", "(": ")", "[": "]", "{": "}" } 🔗

void set_auto_brace_completion_pairs(value: Dictionary)

Dictionary get_auto_brace_completion_pairs()

Sets the brace pairs to be autocompleted. For each entry in the dictionary, the key is the opening brace and the value is the closing brace that matches it. A brace is a String made of symbols. See auto_brace_completion_enabled and auto_brace_completion_highlight_matching.

bool code_completion_enabled = false 🔗

void set_code_completion_enabled(value: bool)

bool is_code_completion_enabled()

If true, the ProjectSettings.input/ui_text_completion_query action requests code completion. To handle it, see _request_code_completion() or code_completion_requested.

Array[String] code_completion_prefixes = [] 🔗

void set_code_completion_prefixes(value: Array[String])

Array[String] get_code_completion_prefixes()

Sets prefixes that will trigger code completion.

Array[String] delimiter_comments = [] 🔗

void set_comment_delimiters(value: Array[String])

Array[String] get_comment_delimiters()

Sets the comment delimiters. All existing comment delimiters will be removed.

Array[String] delimiter_strings = ["' '", "\" \""] 🔗

void set_string_delimiters(value: Array[String])

Array[String] get_string_delimiters()

Sets the string delimiters. All existing string delimiters will be removed.

bool gutters_draw_bookmarks = false 🔗

void set_draw_bookmarks_gutter(value: bool)

bool is_drawing_bookmarks_gutter()

If true, bookmarks are drawn in the gutter. This gutter is shared with breakpoints and executing lines. See set_line_as_bookmarked().

bool gutters_draw_breakpoints_gutter = false 🔗

void set_draw_breakpoints_gutter(value: bool)

bool is_drawing_breakpoints_gutter()

If true, breakpoints are drawn in the gutter. This gutter is shared with bookmarks and executing lines. Clicking the gutter will toggle the breakpoint for the line, see set_line_as_breakpoint().

bool gutters_draw_executing_lines = false 🔗

void set_draw_executing_lines_gutter(value: bool)

bool is_drawing_executing_lines_gutter()

If true, executing lines are marked in the gutter. This gutter is shared with breakpoints and bookmarks. See set_line_as_executing().

bool gutters_draw_fold_gutter = false 🔗

void set_draw_fold_gutter(value: bool)

bool is_drawing_fold_gutter()

If true, the fold gutter is drawn. In this gutter, the can_fold_code_region icon is drawn for each foldable line (see can_fold_line()) and the folded_code_region icon is drawn for each folded line (see is_line_folded()). These icons can be clicked to toggle the fold state, see toggle_foldable_line(). line_folding must be true to show icons.

bool gutters_draw_line_numbers = false 🔗

void set_draw_line_numbers(value: bool)

bool is_draw_line_numbers_enabled()

If true, the line number gutter is drawn. Line numbers start at 1 and are incremented for each line of text. Clicking and dragging in the line number gutter will select entire lines of text.

bool gutters_zero_pad_line_numbers = false 🔗

void set_line_numbers_zero_padded(value: bool)

bool is_line_numbers_zero_padded()

If true, line numbers drawn in the gutter are zero padded based on the total line count. Requires gutters_draw_line_numbers to be set to true.

bool indent_automatic = false 🔗

void set_auto_indent_enabled(value: bool)

bool is_auto_indent_enabled()

If true, an extra indent is automatically inserted when a new line is added and a prefix in indent_automatic_prefixes is found. If a brace pair opening key is found, the matching closing brace will be moved to another new line (see auto_brace_completion_pairs).

Array[String] indent_automatic_prefixes = [":", "{", "[", "("] 🔗

void set_auto_indent_prefixes(value: Array[String])

Array[String] get_auto_indent_prefixes()

Prefixes to trigger an automatic indent. Used when indent_automatic is set to true.

int indent_size = 4 🔗

void set_indent_size(value: int)

int get_indent_size()

Size of the tabulation indent (one Tab press) in characters. If indent_use_spaces is enabled the number of spaces to use.

bool indent_use_spaces = false 🔗

void set_indent_using_spaces(value: bool)

bool is_indent_using_spaces()

Use spaces instead of tabs for indentation.

bool line_folding = false 🔗

void set_line_folding_enabled(value: bool)

bool is_line_folding_enabled()

If true, lines can be folded. Otherwise, line folding methods like fold_line() will not work and can_fold_line() will always return false. See gutters_draw_fold_gutter.

Array[int] line_length_guidelines = [] 🔗

void set_line_length_guidelines(value: Array[int])

Array[int] get_line_length_guidelines()

Draws vertical lines at the provided columns. The first entry is considered a main hard guideline and is drawn more prominently.

bool symbol_lookup_on_click = false 🔗

void set_symbol_lookup_on_click_enabled(value: bool)

bool is_symbol_lookup_on_click_enabled()

Set when a validated word from symbol_validate is clicked, the symbol_lookup should be emitted.

bool symbol_tooltip_on_hover = false 🔗

void set_symbol_tooltip_on_hover_enabled(value: bool)

bool is_symbol_tooltip_on_hover_enabled()

If true, the symbol_hovered signal is emitted when hovering over a word.

void _confirm_code_completion(replace: bool) virtual 🔗

Override this method to define how the selected entry should be inserted. If replace is true, any existing text should be replaced.

Array[Dictionary] _filter_code_completion_candidates(candidates: Array[Dictionary]) virtual const 🔗

Override this method to define what items in candidates should be displayed.

Both candidates and the return is an Array of Dictionary, see get_code_completion_option() for Dictionary content.

void _request_code_completion(force: bool) virtual 🔗

Override this method to define what happens when the user requests code completion. If force is true, any checks should be bypassed.

void add_auto_brace_completion_pair(start_key: String, end_key: String) 🔗

Both the start and end keys must be symbols. Only the start key has to be unique.

void add_code_completion_option(type: CodeCompletionKind, display_text: String, insert_text: String, text_color: Color = Color(1, 1, 1, 1), icon: Resource = null, value: Variant = null, location: int = 1024) 🔗

Submits an item to the queue of potential candidates for the autocomplete menu. Call update_code_completion_options() to update the list.

location indicates location of the option relative to the location of the code completion query. See CodeCompletionLocation for how to set this value.

Note: This list will replace all current candidates.

void add_comment_delimiter(start_key: String, end_key: String, line_only: bool = false) 🔗

Adds a comment delimiter from start_key to end_key. Both keys should be symbols, and start_key must not be shared with other delimiters.

If line_only is true or end_key is an empty String, the region does not carry over to the next line.

void add_string_delimiter(start_key: String, end_key: String, line_only: bool = false) 🔗

Defines a string delimiter from start_key to end_key. Both keys should be symbols, and start_key must not be shared with other delimiters.

If line_only is true or end_key is an empty String, the region does not carry over to the next line.

bool can_fold_line(line: int) const 🔗

Returns true if the given line is foldable. A line is foldable if it is the start of a valid code region (see get_code_region_start_tag()), if it is the start of a comment or string block, or if the next non-empty line is more indented (see TextEdit.get_indent_level()).

void cancel_code_completion() 🔗

Cancels the autocomplete menu.

void clear_bookmarked_lines() 🔗

Clears all bookmarked lines.

void clear_breakpointed_lines() 🔗

Clears all breakpointed lines.

void clear_comment_delimiters() 🔗

Removes all comment delimiters.

void clear_executing_lines() 🔗

Clears all executed lines.

void clear_string_delimiters() 🔗

Removes all string delimiters.

void confirm_code_completion(replace: bool = false) 🔗

Inserts the selected entry into the text. If replace is true, any existing text is replaced rather than merged.

void convert_indent(from_line: int = -1, to_line: int = -1) 🔗

Converts the indents of lines between from_line and to_line to tabs or spaces as set by indent_use_spaces.

Values of -1 convert the entire text.

void create_code_region() 🔗

Creates a new code region with the selection. At least one single line comment delimiter have to be defined (see add_comment_delimiter()).

A code region is a part of code that is highlighted when folded and can help organize your script.

Code region start and end tags can be customized (see set_code_region_tags()).

Code regions are delimited using start and end tags (respectively region and endregion by default) preceded by one line comment delimiter. (eg. #region and #endregion)

void delete_lines() 🔗

Deletes all lines that are selected or have a caret on them.

If there is no selection, indentation is inserted at the caret. Otherwise, the selected lines are indented like indent_lines(). Equivalent to the ProjectSettings.input/ui_text_indent action. The indentation characters used depend on indent_use_spaces and indent_size.

void duplicate_lines() 🔗

Duplicates all lines currently selected with any caret. Duplicates the entire line beneath the current one no matter where the caret is within the line.

void duplicate_selection() 🔗

Duplicates all selected text and duplicates all lines with a caret on them.

void fold_all_lines() 🔗

Folds all lines that are possible to be folded (see can_fold_line()).

void fold_line(line: int) 🔗

Folds the given line, if possible (see can_fold_line()).

String get_auto_brace_completion_close_key(open_key: String) const 🔗

Gets the matching auto brace close key for open_key.

PackedInt32Array get_bookmarked_lines() const 🔗

Gets all bookmarked lines.

PackedInt32Array get_breakpointed_lines() const 🔗

Gets all breakpointed lines.

Dictionary get_code_completion_option(index: int) const 🔗

Gets the completion option at index. The return Dictionary has the following key-values:

kind: CodeCompletionKind

display_text: Text that is shown on the autocomplete menu.

insert_text: Text that is to be inserted when this item is selected.

font_color: Color of the text on the autocomplete menu.

icon: Icon to draw on the autocomplete menu.

default_value: Value of the symbol.

Array[Dictionary] get_code_completion_options() const 🔗

Gets all completion options, see get_code_completion_option() for return content.

int get_code_completion_selected_index() const 🔗

Gets the index of the current selected completion option.

String get_code_region_end_tag() const 🔗

Returns the code region end tag (without comment delimiter).

String get_code_region_start_tag() const 🔗

Returns the code region start tag (without comment delimiter).

String get_delimiter_end_key(delimiter_index: int) const 🔗

Gets the end key for a string or comment region index.

Vector2 get_delimiter_end_position(line: int, column: int) const 🔗

If line column is in a string or comment, returns the end position of the region. If not or no end could be found, both Vector2 values will be -1.

String get_delimiter_start_key(delimiter_index: int) const 🔗

Gets the start key for a string or comment region index.

Vector2 get_delimiter_start_position(line: int, column: int) const 🔗

If line column is in a string or comment, returns the start position of the region. If not or no start could be found, both Vector2 values will be -1.

PackedInt32Array get_executing_lines() const 🔗

Gets all executing lines.

Array[int] get_folded_lines() const 🔗

Returns all lines that are currently folded.

String get_text_for_code_completion() const 🔗

Returns the full text with char 0xFFFF at the caret location.

String get_text_for_symbol_lookup() const 🔗

Returns the full text with char 0xFFFF at the cursor location.

String get_text_with_cursor_char(line: int, column: int) const 🔗

Returns the full text with char 0xFFFF at the specified location.

bool has_auto_brace_completion_close_key(close_key: String) const 🔗

Returns true if close key close_key exists.

bool has_auto_brace_completion_open_key(open_key: String) const 🔗

Returns true if open key open_key exists.

bool has_comment_delimiter(start_key: String) const 🔗

Returns true if comment start_key exists.

bool has_string_delimiter(start_key: String) const 🔗

Returns true if string start_key exists.

void indent_lines() 🔗

Indents all lines that are selected or have a caret on them. Uses spaces or a tab depending on indent_use_spaces. See unindent_lines().

int is_in_comment(line: int, column: int = -1) const 🔗

Returns delimiter index if line column is in a comment. If column is not provided, will return delimiter index if the entire line is a comment. Otherwise -1.

int is_in_string(line: int, column: int = -1) const 🔗

Returns the delimiter index if line column is in a string. If column is not provided, will return the delimiter index if the entire line is a string. Otherwise -1.

bool is_line_bookmarked(line: int) const 🔗

Returns true if the given line is bookmarked. See set_line_as_bookmarked().

bool is_line_breakpointed(line: int) const 🔗

Returns true if the given line is breakpointed. See set_line_as_breakpoint().

bool is_line_code_region_end(line: int) const 🔗

Returns true if the given line is a code region end. See set_code_region_tags().

bool is_line_code_region_start(line: int) const 🔗

Returns true if the given line is a code region start. See set_code_region_tags().

bool is_line_executing(line: int) const 🔗

Returns true if the given line is marked as executing. See set_line_as_executing().

bool is_line_folded(line: int) const 🔗

Returns true if the given line is folded. See fold_line().

void move_lines_down() 🔗

Moves all lines down that are selected or have a caret on them.

void move_lines_up() 🔗

Moves all lines up that are selected or have a caret on them.

void remove_comment_delimiter(start_key: String) 🔗

Removes the comment delimiter with start_key.

void remove_string_delimiter(start_key: String) 🔗

Removes the string delimiter with start_key.

void request_code_completion(force: bool = false) 🔗

Emits code_completion_requested, if force is true will bypass all checks. Otherwise will check that the caret is in a word or in front of a prefix. Will ignore the request if all current options are of type file path, node path, or signal.

void set_code_completion_selected_index(index: int) 🔗

Sets the current selected completion option.

void set_code_hint(code_hint: String) 🔗

Sets the code hint text. Pass an empty string to clear.

void set_code_hint_draw_below(draw_below: bool) 🔗

If true, the code hint will draw below the main caret. If false, the code hint will draw above the main caret. See set_code_hint().

void set_code_region_tags(start: String = "region", end: String = "endregion") 🔗

Sets the code region start and end tags (without comment delimiter).

void set_line_as_bookmarked(line: int, bookmarked: bool) 🔗

Sets the given line as bookmarked. If true and gutters_draw_bookmarks is true, draws the bookmark icon in the gutter for this line. See get_bookmarked_lines() and is_line_bookmarked().

void set_line_as_breakpoint(line: int, breakpointed: bool) 🔗

Sets the given line as a breakpoint. If true and gutters_draw_breakpoints_gutter is true, draws the breakpoint icon in the gutter for this line. See get_breakpointed_lines() and is_line_breakpointed().

void set_line_as_executing(line: int, executing: bool) 🔗

Sets the given line as executing. If true and gutters_draw_executing_lines is true, draws the executing_line icon in the gutter for this line. See get_executing_lines() and is_line_executing().

void set_symbol_lookup_word_as_valid(valid: bool) 🔗

Sets the symbol emitted by symbol_validate as a valid lookup.

void toggle_foldable_line(line: int) 🔗

Toggle the folding of the code block at the given line.

void toggle_foldable_lines_at_carets() 🔗

Toggle the folding of the code block on all lines with a caret on them.

void unfold_all_lines() 🔗

Unfolds all lines that are folded.

void unfold_line(line: int) 🔗

Unfolds the given line if it is folded or if it is hidden under a folded line.

void unindent_lines() 🔗

Unindents all lines that are selected or have a caret on them. Uses spaces or a tab depending on indent_use_spaces. Equivalent to the ProjectSettings.input/ui_text_dedent action. See indent_lines().

void update_code_completion_options(force: bool) 🔗

Submits all completion options added with add_code_completion_option(). Will try to force the autocomplete menu to popup, if force is true.

Note: This will replace all current candidates.

Color bookmark_color = Color(0.5, 0.64, 1, 0.8) 🔗

Color of the bookmark icon for bookmarked lines.

Color brace_mismatch_color = Color(1, 0.2, 0.2, 1) 🔗

Color of the text to highlight mismatched braces.

Color breakpoint_color = Color(0.9, 0.29, 0.3, 1) 🔗

Color of the breakpoint icon for bookmarked lines.

Color code_folding_color = Color(0.8, 0.8, 0.8, 0.8) 🔗

Color for all icons related to line folding.

Color completion_background_color = Color(0.17, 0.16, 0.2, 1) 🔗

Sets the background Color for the code completion popup.

Color completion_existing_color = Color(0.87, 0.87, 0.87, 0.13) 🔗

Background highlight Color for matching text in code completion options.

Color completion_scroll_color = Color(1, 1, 1, 0.29) 🔗

Color of the scrollbar in the code completion popup.

Color completion_scroll_hovered_color = Color(1, 1, 1, 0.4) 🔗

Color of the scrollbar in the code completion popup when hovered.

Color completion_selected_color = Color(0.26, 0.26, 0.27, 1) 🔗

Background highlight Color for the current selected option item in the code completion popup.

Color executing_line_color = Color(0.98, 0.89, 0.27, 1) 🔗

Color of the executing icon for executing lines.

Color folded_code_region_color = Color(0.68, 0.46, 0.77, 0.2) 🔗

Color of background line highlight for folded code region.

Color line_length_guideline_color = Color(0.3, 0.5, 0.8, 0.1) 🔗

Color of the main line length guideline, secondary guidelines will have 50% alpha applied.

Color line_number_color = Color(0.67, 0.67, 0.67, 0.4) 🔗

Sets the Color of line numbers.

int completion_lines = 7 🔗

Max number of options to display in the code completion popup at any one time.

int completion_max_width = 50 🔗

Max width of options in the code completion popup. Options longer than this will be cut off.

int completion_scroll_width = 6 🔗

Width of the scrollbar in the code completion popup.

Sets a custom Texture2D to draw in the bookmark gutter for bookmarked lines.

Texture2D breakpoint 🔗

Sets a custom Texture2D to draw in the breakpoint gutter for breakpointed lines.

Sets a custom Texture2D to draw in the line folding gutter when a line can be folded.

Texture2D can_fold_code_region 🔗

Sets a custom Texture2D to draw in the line folding gutter when a code region can be folded.

Texture2D completion_color_bg 🔗

Background panel for the color preview box in autocompletion (visible when the color is translucent).

Texture2D executing_line 🔗

Icon to draw in the executing gutter for executing lines.

Sets a custom Texture2D to draw in the line folding gutter when a line is folded and can be unfolded.

Texture2D folded_code_region 🔗

Sets a custom Texture2D to draw in the line folding gutter when a code region is folded and can be unfolded.

Texture2D folded_eol_icon 🔗

Sets a custom Texture2D to draw at the end of a folded line.

StyleBox completion 🔗

StyleBox for the code completion popup.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CheckBox — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_checkbox.html

**Contents:**
- CheckBox
- Description
- Properties
- Theme Properties
- Theme Property Descriptions
- User-contributed notes

Inherits: Button < BaseButton < Control < CanvasItem < Node < Object

A button that represents a binary choice.

CheckBox allows the user to choose one of only two possible options. It's similar to CheckButton in functionality, but it has a different appearance. To follow established UX patterns, it's recommended to use CheckBox when toggling it has no immediate effect on something. For example, it could be used when toggling it will only do something once a confirmation button is pressed.

See also BaseButton which contains common properties and methods associated with this node.

When BaseButton.button_group specifies a ButtonGroup, CheckBox changes its appearance to that of a radio button and uses the various radio_* theme properties.

true (overrides BaseButton)

checkbox_checked_color

checkbox_unchecked_color

radio_checked_disabled

radio_unchecked_disabled

Color checkbox_checked_color = Color(1, 1, 1, 1) 🔗

The color of the checked icon when the checkbox is pressed.

Color checkbox_unchecked_color = Color(1, 1, 1, 1) 🔗

The color of the unchecked icon when the checkbox is not pressed.

int check_v_offset = 0 🔗

The vertical offset used when rendering the check icons (in pixels).

The check icon to display when the CheckBox is checked.

Texture2D checked_disabled 🔗

The check icon to display when the CheckBox is checked and is disabled.

Texture2D radio_checked 🔗

The check icon to display when the CheckBox is configured as a radio button and is checked.

Texture2D radio_checked_disabled 🔗

The check icon to display when the CheckBox is configured as a radio button, is disabled, and is unchecked.

Texture2D radio_unchecked 🔗

The check icon to display when the CheckBox is configured as a radio button and is unchecked.

Texture2D radio_unchecked_disabled 🔗

The check icon to display when the CheckBox is configured as a radio button, is disabled, and is unchecked.

Texture2D unchecked 🔗

The check icon to display when the CheckBox is unchecked.

Texture2D unchecked_disabled 🔗

The check icon to display when the CheckBox is unchecked and is disabled.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ColorPickerButton — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_colorpickerbutton.html

**Contents:**
- ColorPickerButton
- Description
- Tutorials
- Properties
- Methods
- Theme Properties
- Signals
- Property Descriptions
- Method Descriptions
- Theme Property Descriptions

Inherits: Button < BaseButton < Control < CanvasItem < Node < Object

A button that brings up a ColorPicker when pressed.

Encapsulates a ColorPicker, making it accessible by pressing a button. Pressing the button will toggle the ColorPicker's visibility.

See also BaseButton which contains common properties and methods associated with this node.

Note: By default, the button may not be wide enough for the color preview swatch to be visible. Make sure to set Control.custom_minimum_size to a big enough value to give the button enough space.

GUI Drag And Drop Demo

true (overrides BaseButton)

color_changed(color: Color) 🔗

Emitted when the color changes.

Emitted when the ColorPicker is created (the button is pressed for the first time).

Emitted when the ColorPicker is closed.

Color color = Color(0, 0, 0, 1) 🔗

void set_pick_color(value: Color)

Color get_pick_color()

The currently selected color.

bool edit_alpha = true 🔗

void set_edit_alpha(value: bool)

bool is_editing_alpha()

If true, the alpha channel in the displayed ColorPicker will be visible.

bool edit_intensity = true 🔗

void set_edit_intensity(value: bool)

bool is_editing_intensity()

If true, the intensity slider in the displayed ColorPicker will be visible.

ColorPicker get_picker() 🔗

Returns the ColorPicker that this node toggles.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

PopupPanel get_popup() 🔗

Returns the control's PopupPanel which allows you to connect to popup signals. This allows you to handle events when the ColorPicker is shown or hidden.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their Window.visible property.

The background of the color preview rect on the button.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ColorRect — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_colorrect.html

**Contents:**
- ColorRect
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Control < CanvasItem < Node < Object

A control that displays a solid color rectangle.

Displays a rectangle filled with a solid color. If you need to display the border alone, consider using a Panel instead.

2D Dodge The Creeps Demo

Color color = Color(1, 1, 1, 1) 🔗

void set_color(value: Color)

The fill color of the rectangle.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ConeTwistJoint3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_conetwistjoint3d.html

**Contents:**
- ConeTwistJoint3D
- Description
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Joint3D < Node3D < Node < Object

A physics joint that connects two 3D physics bodies in a way that simulates a ball-and-socket joint.

A physics joint that connects two 3D physics bodies in a way that simulates a ball-and-socket joint. The twist axis is initiated as the X axis of the ConeTwistJoint3D. Once the physics bodies swing, the twist axis is calculated as the middle of the X axes of the joint in the local space of the two physics bodies. Useful for limbs like shoulders and hips, lamps hanging off a ceiling, etc.

get_param(param: Param) const

set_param(param: Param, value: float)

Param PARAM_SWING_SPAN = 0

Swing is rotation from side to side, around the axis perpendicular to the twist axis.

The swing span defines, how much rotation will not get corrected along the swing axis.

Could be defined as looseness in the ConeTwistJoint3D.

If below 0.05, this behavior is locked.

Param PARAM_TWIST_SPAN = 1

Twist is the rotation around the twist axis, this value defined how far the joint can twist.

Twist is locked if below 0.05.

The speed with which the swing or twist will take place.

The higher, the faster.

Param PARAM_SOFTNESS = 3

The ease with which the joint starts to twist. If it's too low, it takes more force to start twisting the joint.

Param PARAM_RELAXATION = 4

Defines, how fast the swing- and twist-speed-difference on both sides gets synced.

Represents the size of the Param enum.

void set_param(param: Param, value: float)

float get_param(param: Param) const

The speed with which the swing or twist will take place.

The higher, the faster.

float relaxation = 1.0 🔗

void set_param(param: Param, value: float)

float get_param(param: Param) const

Defines, how fast the swing- and twist-speed-difference on both sides gets synced.

float softness = 0.8 🔗

void set_param(param: Param, value: float)

float get_param(param: Param) const

The ease with which the joint starts to twist. If it's too low, it takes more force to start twisting the joint.

float swing_span = 0.7853982 🔗

void set_param(param: Param, value: float)

float get_param(param: Param) const

Swing is rotation from side to side, around the axis perpendicular to the twist axis.

The swing span defines, how much rotation will not get corrected along the swing axis.

Could be defined as looseness in the ConeTwistJoint3D.

If below 0.05, this behavior is locked.

float twist_span = 3.1415927 🔗

void set_param(param: Param, value: float)

float get_param(param: Param) const

Twist is the rotation around the twist axis, this value defined how far the joint can twist.

Twist is locked if below 0.05.

float get_param(param: Param) const 🔗

Returns the value of the specified parameter.

void set_param(param: Param, value: float) 🔗

Sets the value of the specified parameter.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ColorPicker — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_colorpicker.html

**Contents:**
- ColorPicker
- Description
- Tutorials
- Properties
- Methods
- Theme Properties
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions

Inherits: VBoxContainer < BoxContainer < Container < Control < CanvasItem < Node < Object

A widget that provides an interface for selecting or modifying a color.

A widget that provides an interface for selecting or modifying a color. It can optionally provide functionalities like a color sampler (eyedropper), color modes, and presets.

Note: This control is the color picker widget itself. You can use a ColorPickerButton instead if you need a button that brings up a ColorPicker in a popup.

Tween Interpolation Demo

add_preset(color: Color)

add_recent_preset(color: Color)

erase_preset(color: Color)

erase_recent_preset(color: Color)

get_recent_presets() const

focused_not_editing_cursor_color

Color(1, 1, 1, 0.275)

center_slider_grabbers

picker_focus_rectangle

color_changed(color: Color) 🔗

Emitted when the color is changed.

preset_added(color: Color) 🔗

Emitted when a preset is added.

preset_removed(color: Color) 🔗

Emitted when a preset is removed.

enum ColorModeType: 🔗

ColorModeType MODE_RGB = 0

Allows editing the color with Red/Green/Blue sliders in sRGB color space.

ColorModeType MODE_HSV = 1

Allows editing the color with Hue/Saturation/Value sliders.

ColorModeType MODE_RAW = 2

Deprecated: This is replaced by MODE_LINEAR.

ColorModeType MODE_LINEAR = 2

Allows editing the color with Red/Green/Blue sliders in linear color space.

ColorModeType MODE_OKHSL = 3

Allows editing the color with Hue/Saturation/Lightness sliders.

OKHSL is a new color space similar to HSL but that better match perception by leveraging the Oklab color space which is designed to be simple to use, while doing a good job at predicting perceived lightness, chroma and hue.

Okhsv and Okhsl color spaces

enum PickerShapeType: 🔗

PickerShapeType SHAPE_HSV_RECTANGLE = 0

HSV Color Model rectangle color space.

PickerShapeType SHAPE_HSV_WHEEL = 1

HSV Color Model rectangle color space with a wheel.

PickerShapeType SHAPE_VHS_CIRCLE = 2

HSV Color Model circle color space. Use Saturation as a radius.

PickerShapeType SHAPE_OKHSL_CIRCLE = 3

HSL OK Color Model circle color space.

PickerShapeType SHAPE_NONE = 4

The color space shape and the shape select button are hidden. Can't be selected from the shapes popup.

PickerShapeType SHAPE_OK_HS_RECTANGLE = 5

OKHSL Color Model rectangle with constant lightness.

PickerShapeType SHAPE_OK_HL_RECTANGLE = 6

OKHSL Color Model rectangle with constant saturation.

bool can_add_swatches = true 🔗

void set_can_add_swatches(value: bool)

bool are_swatches_enabled()

If true, it's possible to add presets under Swatches. If false, the button to add presets is disabled.

Color color = Color(1, 1, 1, 1) 🔗

void set_pick_color(value: Color)

Color get_pick_color()

The currently selected color.

ColorModeType color_mode = 0 🔗

void set_color_mode(value: ColorModeType)

ColorModeType get_color_mode()

The currently selected color mode.

bool color_modes_visible = true 🔗

void set_modes_visible(value: bool)

bool are_modes_visible()

If true, the color mode buttons are visible.

bool deferred_mode = false 🔗

void set_deferred_mode(value: bool)

bool is_deferred_mode()

If true, the color will apply only after the user releases the mouse button, otherwise it will apply immediately even in mouse motion event (which can cause performance issues).

bool edit_alpha = true 🔗

void set_edit_alpha(value: bool)

bool is_editing_alpha()

If true, shows an alpha channel slider (opacity).

bool edit_intensity = true 🔗

void set_edit_intensity(value: bool)

bool is_editing_intensity()

If true, shows an intensity slider. The intensity is applied as follows: multiply the color by 2 ** intensity in linear RGB space, and then convert it back to sRGB.

bool hex_visible = true 🔗

void set_hex_visible(value: bool)

bool is_hex_visible()

If true, the hex color code input field is visible.

PickerShapeType picker_shape = 0 🔗

void set_picker_shape(value: PickerShapeType)

PickerShapeType get_picker_shape()

The shape of the color space view.

bool presets_visible = true 🔗

void set_presets_visible(value: bool)

bool are_presets_visible()

If true, the Swatches and Recent Colors presets are visible.

bool sampler_visible = true 🔗

void set_sampler_visible(value: bool)

bool is_sampler_visible()

If true, the color sampler and color preview are visible.

bool sliders_visible = true 🔗

void set_sliders_visible(value: bool)

bool are_sliders_visible()

If true, the color sliders are visible.

void add_preset(color: Color) 🔗

Adds the given color to a list of color presets. The presets are displayed in the color picker and the user will be able to select them.

Note: The presets list is only for this color picker.

void add_recent_preset(color: Color) 🔗

Adds the given color to a list of color recent presets so that it can be picked later. Recent presets are the colors that were picked recently, a new preset is automatically created and added to recent presets when you pick a new color.

Note: The recent presets list is only for this color picker.

void erase_preset(color: Color) 🔗

Removes the given color from the list of color presets of this color picker.

void erase_recent_preset(color: Color) 🔗

Removes the given color from the list of color recent presets of this color picker.

PackedColorArray get_presets() const 🔗

Returns the list of colors in the presets of the color picker.

PackedColorArray get_recent_presets() const 🔗

Returns the list of colors in the recent presets of the color picker.

Color focused_not_editing_cursor_color = Color(1, 1, 1, 0.275) 🔗

Color of rectangle or circle drawn when a picker shape part is focused but not editable via keyboard or joypad. Displayed over the picker shape, so a partially transparent color should be used to ensure the picker shape remains visible.

int center_slider_grabbers = 1 🔗

Overrides the Slider.center_grabber theme property of the sliders.

The width of the hue selection slider.

int label_width = 10 🔗

The minimum width of the color labels next to sliders.

The margin around the ColorPicker.

int sv_height = 256 🔗

The height of the saturation-value selection box.

The width of the saturation-value selection box.

Texture2D add_preset 🔗

The icon for the "Add Preset" button.

Texture2D bar_arrow 🔗

The texture for the arrow grabber.

Texture2D color_hue 🔗

Custom texture for the hue selection slider on the right.

Texture2D color_script 🔗

The icon for the button that switches color text to hexadecimal.

Texture2D expanded_arrow 🔗

The icon for color preset drop down menu when expanded.

Texture2D folded_arrow 🔗

The icon for color preset drop down menu when folded.

Texture2D menu_option 🔗

The icon for color preset option menu.

Texture2D overbright_indicator 🔗

The indicator used to signalize that the color value is outside the 0-1 range.

Texture2D picker_cursor 🔗

The image displayed over the color box/circle (depending on the picker_shape), marking the currently selected color.

Texture2D picker_cursor_bg 🔗

The fill image displayed behind the picker cursor.

Texture2D sample_bg 🔗

Background panel for the color preview box (visible when the color is translucent).

Texture2D sample_revert 🔗

The icon for the revert button (visible on the middle of the "old" color when it differs from the currently selected color). This icon is modulated with a dark color if the "old" color is bright enough, so the icon should be bright to ensure visibility in both scenarios.

Texture2D screen_picker 🔗

The icon for the screen color picker button.

Texture2D shape_circle 🔗

The icon for circular picker shapes.

Texture2D shape_rect 🔗

The icon for rectangular picker shapes.

Texture2D shape_rect_wheel 🔗

The icon for rectangular wheel picker shapes.

StyleBox picker_focus_circle 🔗

The StyleBox used when the circle-shaped part of the picker is focused. Displayed over the picker shape, so a partially transparent StyleBox should be used to ensure the picker shape remains visible. A StyleBox that represents an outline or an underline works well for this purpose. To disable the focus visual effect, assign a StyleBoxEmpty resource. Note that disabling the focus visual effect will harm keyboard/controller navigation usability, so this is not recommended for accessibility reasons.

StyleBox picker_focus_rectangle 🔗

The StyleBox used when the rectangle-shaped part of the picker is focused. Displayed over the picker shape, so a partially transparent StyleBox should be used to ensure the picker shape remains visible. A StyleBox that represents an outline or an underline works well for this purpose. To disable the focus visual effect, assign a StyleBoxEmpty resource. Note that disabling the focus visual effect will harm keyboard/controller navigation usability, so this is not recommended for accessibility reasons.

StyleBox sample_focus 🔗

The StyleBox used for the old color sample part when it is focused. Displayed over the sample, so a partially transparent StyleBox should be used to ensure the picker shape remains visible. A StyleBox that represents an outline or an underline works well for this purpose. To disable the focus visual effect, assign a StyleBoxEmpty resource. Note that disabling the focus visual effect will harm keyboard/controller navigation usability, so this is not recommended for accessibility reasons.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ConvertTransformModifier3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_converttransformmodifier3d.html

**Contents:**
- ConvertTransformModifier3D
- Description
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: BoneConstraint3D < SkeletonModifier3D < Node3D < Node < Object

A SkeletonModifier3D that apply transform to the bone which converted from reference.

Apply the copied transform of the bone set by BoneConstraint3D.set_reference_bone() to the bone set by BoneConstraint3D.set_apply_bone() about the specific axis with remapping it with some options.

There are 4 ways to apply the transform, depending on the combination of set_relative() and set_additive().

Extract reference pose relative to the rest and add it to the apply bone's pose.

Relative + Not Additive:

Extract reference pose relative to the rest and add it to the apply bone's rest.

Not Relative + Additive:

Extract reference pose absolutely and add it to the apply bone's pose.

Not Relative + Not Additive:

Extract reference pose absolutely and the apply bone's pose is replaced with it.

get_apply_axis(index: int) const

get_apply_range_max(index: int) const

get_apply_range_min(index: int) const

get_apply_transform_mode(index: int) const

get_reference_axis(index: int) const

get_reference_range_max(index: int) const

get_reference_range_min(index: int) const

get_reference_transform_mode(index: int) const

is_additive(index: int) const

is_relative(index: int) const

set_additive(index: int, enabled: bool)

set_apply_axis(index: int, axis: Axis)

set_apply_range_max(index: int, range_max: float)

set_apply_range_min(index: int, range_min: float)

set_apply_transform_mode(index: int, transform_mode: TransformMode)

set_reference_axis(index: int, axis: Axis)

set_reference_range_max(index: int, range_max: float)

set_reference_range_min(index: int, range_min: float)

set_reference_transform_mode(index: int, transform_mode: TransformMode)

set_relative(index: int, enabled: bool)

enum TransformMode: 🔗

TransformMode TRANSFORM_MODE_POSITION = 0

Convert with position. Transfer the difference.

TransformMode TRANSFORM_MODE_ROTATION = 1

Convert with rotation. The angle is the roll for the specified axis.

TransformMode TRANSFORM_MODE_SCALE = 2

Convert with scale. Transfers the ratio, not the difference.

int setting_count = 0 🔗

void set_setting_count(value: int)

int get_setting_count()

The number of settings in the modifier.

Axis get_apply_axis(index: int) const 🔗

Returns the axis of the remapping destination transform.

float get_apply_range_max(index: int) const 🔗

Returns the maximum value of the remapping destination range.

float get_apply_range_min(index: int) const 🔗

Returns the minimum value of the remapping destination range.

TransformMode get_apply_transform_mode(index: int) const 🔗

Returns the operation of the remapping destination transform.

Axis get_reference_axis(index: int) const 🔗

Returns the axis of the remapping source transform.

float get_reference_range_max(index: int) const 🔗

Returns the maximum value of the remapping source range.

float get_reference_range_min(index: int) const 🔗

Returns the minimum value of the remapping source range.

TransformMode get_reference_transform_mode(index: int) const 🔗

Returns the operation of the remapping source transform.

bool is_additive(index: int) const 🔗

Returns true if the additive option is enabled in the setting at index.

bool is_relative(index: int) const 🔗

Returns true if the relative option is enabled in the setting at index.

void set_additive(index: int, enabled: bool) 🔗

Sets additive option in the setting at index to enabled. This mainly affects the process of applying transform to the BoneConstraint3D.set_apply_bone().

If sets enabled to true, the processed transform is added to the pose of the current apply bone.

If sets enabled to false, the pose of the current apply bone is replaced with the processed transform. However, if set set_relative() to true, the transform is relative to rest.

void set_apply_axis(index: int, axis: Axis) 🔗

Sets the axis of the remapping destination transform.

void set_apply_range_max(index: int, range_max: float) 🔗

Sets the maximum value of the remapping destination range.

void set_apply_range_min(index: int, range_min: float) 🔗

Sets the minimum value of the remapping destination range.

void set_apply_transform_mode(index: int, transform_mode: TransformMode) 🔗

Sets the operation of the remapping destination transform.

void set_reference_axis(index: int, axis: Axis) 🔗

Sets the axis of the remapping source transform.

void set_reference_range_max(index: int, range_max: float) 🔗

Sets the maximum value of the remapping source range.

void set_reference_range_min(index: int, range_min: float) 🔗

Sets the minimum value of the remapping source range.

void set_reference_transform_mode(index: int, transform_mode: TransformMode) 🔗

Sets the operation of the remapping source transform.

void set_relative(index: int, enabled: bool) 🔗

Sets relative option in the setting at index to enabled.

If sets enabled to true, the extracted and applying transform is relative to the rest.

If sets enabled to false, the extracted transform is absolute.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CPUParticles2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html

**Contents:**
- CPUParticles2D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node2D < CanvasItem < Node < Object

A CPU-based 2D particle emitter.

CPU-based 2D particle node used to create a variety of particle systems and effects.

See also GPUParticles2D, which provides the same functionality with hardware acceleration, but may not run on older devices.

Particle systems (2D)

angular_velocity_curve

emission_rect_extents

emission_sphere_radius

particle_flag_align_y

PhysicsInterpolationMode

physics_interpolation_mode

tangential_accel_curve

convert_from_particles(particles: Node)

get_param_curve(param: Parameter) const

get_param_max(param: Parameter) const

get_param_min(param: Parameter) const

get_particle_flag(particle_flag: ParticleFlags) const

request_particles_process(process_time: float)

restart(keep_seed: bool = false)

set_param_curve(param: Parameter, curve: Curve)

set_param_max(param: Parameter, value: float)

set_param_min(param: Parameter, value: float)

set_particle_flag(particle_flag: ParticleFlags, enable: bool)

Emitted when all active particles have finished processing. When one_shot is disabled, particles will process continuously, so this is never emitted.

DrawOrder DRAW_ORDER_INDEX = 0

Particles are drawn in the order emitted.

DrawOrder DRAW_ORDER_LIFETIME = 1

Particles are drawn in order of remaining lifetime. In other words, the particle with the highest lifetime is drawn at the front.

Parameter PARAM_INITIAL_LINEAR_VELOCITY = 0

Use with set_param_min(), set_param_max(), and set_param_curve() to set initial velocity properties.

Parameter PARAM_ANGULAR_VELOCITY = 1

Use with set_param_min(), set_param_max(), and set_param_curve() to set angular velocity properties.

Parameter PARAM_ORBIT_VELOCITY = 2

Use with set_param_min(), set_param_max(), and set_param_curve() to set orbital velocity properties.

Parameter PARAM_LINEAR_ACCEL = 3

Use with set_param_min(), set_param_max(), and set_param_curve() to set linear acceleration properties.

Parameter PARAM_RADIAL_ACCEL = 4

Use with set_param_min(), set_param_max(), and set_param_curve() to set radial acceleration properties.

Parameter PARAM_TANGENTIAL_ACCEL = 5

Use with set_param_min(), set_param_max(), and set_param_curve() to set tangential acceleration properties.

Parameter PARAM_DAMPING = 6

Use with set_param_min(), set_param_max(), and set_param_curve() to set damping properties.

Parameter PARAM_ANGLE = 7

Use with set_param_min(), set_param_max(), and set_param_curve() to set angle properties.

Parameter PARAM_SCALE = 8

Use with set_param_min(), set_param_max(), and set_param_curve() to set scale properties.

Parameter PARAM_HUE_VARIATION = 9

Use with set_param_min(), set_param_max(), and set_param_curve() to set hue variation properties.

Parameter PARAM_ANIM_SPEED = 10

Use with set_param_min(), set_param_max(), and set_param_curve() to set animation speed properties.

Parameter PARAM_ANIM_OFFSET = 11

Use with set_param_min(), set_param_max(), and set_param_curve() to set animation offset properties.

Parameter PARAM_MAX = 12

Represents the size of the Parameter enum.

enum ParticleFlags: 🔗

ParticleFlags PARTICLE_FLAG_ALIGN_Y_TO_VELOCITY = 0

Use with set_particle_flag() to set particle_flag_align_y.

ParticleFlags PARTICLE_FLAG_ROTATE_Y = 1

Present for consistency with 3D particle nodes, not used in 2D.

ParticleFlags PARTICLE_FLAG_DISABLE_Z = 2

Present for consistency with 3D particle nodes, not used in 2D.

ParticleFlags PARTICLE_FLAG_MAX = 3

Represents the size of the ParticleFlags enum.

enum EmissionShape: 🔗

EmissionShape EMISSION_SHAPE_POINT = 0

All particles will be emitted from a single point.

EmissionShape EMISSION_SHAPE_SPHERE = 1

Particles will be emitted in the volume of a sphere flattened to two dimensions.

EmissionShape EMISSION_SHAPE_SPHERE_SURFACE = 2

Particles will be emitted on the surface of a sphere flattened to two dimensions.

EmissionShape EMISSION_SHAPE_RECTANGLE = 3

Particles will be emitted in the area of a rectangle.

EmissionShape EMISSION_SHAPE_POINTS = 4

Particles will be emitted at a position chosen randomly among emission_points. Particle color will be modulated by emission_colors.

EmissionShape EMISSION_SHAPE_DIRECTED_POINTS = 5

Particles will be emitted at a position chosen randomly among emission_points. Particle velocity and rotation will be set based on emission_normals. Particle color will be modulated by emission_colors.

EmissionShape EMISSION_SHAPE_MAX = 6

Represents the size of the EmissionShape enum.

void set_amount(value: int)

Number of particles emitted in one emission cycle.

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's rotation will be animated along this Curve. Should be a unit Curve.

float angle_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial rotation applied to each particle, in degrees.

float angle_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of angle_max.

Curve angular_velocity_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's angular velocity will vary along this Curve. Should be a unit Curve.

float angular_velocity_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial angular velocity (rotation speed) applied to each particle in degrees per second.

float angular_velocity_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of angular_velocity_max.

Curve anim_offset_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's animation offset will vary along this Curve. Should be a unit Curve.

float anim_offset_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum animation offset that corresponds to frame index in the texture. 0 is the first frame, 1 is the last one. See CanvasItemMaterial.particles_animation.

float anim_offset_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of anim_offset_max.

Curve anim_speed_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's animation speed will vary along this Curve. Should be a unit Curve.

float anim_speed_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum particle animation speed. Animation speed of 1 means that the particles will make full 0 to 1 offset cycle during lifetime, 2 means 2 cycles etc.

With animation speed greater than 1, remember to enable CanvasItemMaterial.particles_anim_loop property if you want the animation to repeat.

float anim_speed_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of anim_speed_max.

Color color = Color(1, 1, 1, 1) 🔗

void set_color(value: Color)

Each particle's initial color. If texture is defined, it will be multiplied by this color.

Gradient color_initial_ramp 🔗

void set_color_initial_ramp(value: Gradient)

Gradient get_color_initial_ramp()

Each particle's initial color will vary along this Gradient (multiplied with color).

Gradient color_ramp 🔗

void set_color_ramp(value: Gradient)

Gradient get_color_ramp()

Each particle's color will vary along this Gradient over its lifetime (multiplied with color).

Curve damping_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Damping will vary along this Curve. Should be a unit Curve.

float damping_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

The maximum rate at which particles lose velocity. For example value of 100 means that the particle will go from 100 velocity to 0 in 1 second.

float damping_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of damping_max.

Vector2 direction = Vector2(1, 0) 🔗

void set_direction(value: Vector2)

Vector2 get_direction()

Unit vector specifying the particles' emission direction.

DrawOrder draw_order = 0 🔗

void set_draw_order(value: DrawOrder)

DrawOrder get_draw_order()

PackedColorArray emission_colors 🔗

void set_emission_colors(value: PackedColorArray)

PackedColorArray get_emission_colors()

Sets the Colors to modulate particles by when using EMISSION_SHAPE_POINTS or EMISSION_SHAPE_DIRECTED_POINTS.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedColorArray for more details.

PackedVector2Array emission_normals 🔗

void set_emission_normals(value: PackedVector2Array)

PackedVector2Array get_emission_normals()

Sets the direction the particles will be emitted in when using EMISSION_SHAPE_DIRECTED_POINTS.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector2Array for more details.

PackedVector2Array emission_points 🔗

void set_emission_points(value: PackedVector2Array)

PackedVector2Array get_emission_points()

Sets the initial positions to spawn particles when using EMISSION_SHAPE_POINTS or EMISSION_SHAPE_DIRECTED_POINTS.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector2Array for more details.

Vector2 emission_rect_extents 🔗

void set_emission_rect_extents(value: Vector2)

Vector2 get_emission_rect_extents()

The rectangle's extents if emission_shape is set to EMISSION_SHAPE_RECTANGLE.

EmissionShape emission_shape = 0 🔗

void set_emission_shape(value: EmissionShape)

EmissionShape get_emission_shape()

Particles will be emitted inside this region.

float emission_sphere_radius 🔗

void set_emission_sphere_radius(value: float)

float get_emission_sphere_radius()

The sphere's radius if emission_shape is set to EMISSION_SHAPE_SPHERE.

bool emitting = true 🔗

void set_emitting(value: bool)

If true, particles are being emitted. emitting can be used to start and stop particles from emitting. However, if one_shot is true setting emitting to true will not restart the emission cycle until after all active particles finish processing. You can use the finished signal to be notified once all active particles finish processing.

float explosiveness = 0.0 🔗

void set_explosiveness_ratio(value: float)

float get_explosiveness_ratio()

How rapidly particles in an emission cycle are emitted. If greater than 0, there will be a gap in emissions before the next cycle begins.

void set_fixed_fps(value: int)

The particle system's frame rate is fixed to a value. For example, changing the value to 2 will make the particles render at 2 frames per second. Note this does not slow down the simulation of the particle system itself.

bool fract_delta = true 🔗

void set_fractional_delta(value: bool)

bool get_fractional_delta()

If true, results in fractional delta calculation which has a smoother particles display effect.

Vector2 gravity = Vector2(0, 980) 🔗

void set_gravity(value: Vector2)

Vector2 get_gravity()

Gravity applied to every particle.

Curve hue_variation_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's hue will vary along this Curve. Should be a unit Curve.

float hue_variation_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial hue variation applied to each particle. It will shift the particle color's hue.

float hue_variation_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of hue_variation_max.

float initial_velocity_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial velocity magnitude for each particle. Direction comes from direction and spread.

float initial_velocity_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of initial_velocity_max.

float lifetime = 1.0 🔗

void set_lifetime(value: float)

Amount of time each particle will exist.

float lifetime_randomness = 0.0 🔗

void set_lifetime_randomness(value: float)

float get_lifetime_randomness()

Particle lifetime randomness ratio.

Curve linear_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's linear acceleration will vary along this Curve. Should be a unit Curve.

float linear_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum linear acceleration applied to each particle in the direction of motion.

float linear_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of linear_accel_max.

bool local_coords = false 🔗

void set_use_local_coordinates(value: bool)

bool get_use_local_coordinates()

If true, particles use the parent node's coordinate space (known as local coordinates). This will cause particles to move and rotate along the CPUParticles2D node (and its parents) when it is moved or rotated. If false, particles use global coordinates; they will not move or rotate along the CPUParticles2D node (and its parents) when it is moved or rotated.

bool one_shot = false 🔗

void set_one_shot(value: bool)

If true, only one emission cycle occurs. If set true during a cycle, emission will stop at the cycle's end.

Curve orbit_velocity_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's orbital velocity will vary along this Curve. Should be a unit Curve.

float orbit_velocity_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum orbital velocity applied to each particle. Makes the particles circle around origin. Specified in number of full rotations around origin per second.

float orbit_velocity_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of orbit_velocity_max.

bool particle_flag_align_y = false 🔗

void set_particle_flag(particle_flag: ParticleFlags, enable: bool)

bool get_particle_flag(particle_flag: ParticleFlags) const

Align Y axis of particle with the direction of its velocity.

float preprocess = 0.0 🔗

void set_pre_process_time(value: float)

float get_pre_process_time()

Particle system starts as if it had already run for this many seconds.

Curve radial_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's radial acceleration will vary along this Curve. Should be a unit Curve.

float radial_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum radial acceleration applied to each particle. Makes particle accelerate away from the origin or towards it if negative.

float radial_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of radial_accel_max.

float randomness = 0.0 🔗

void set_randomness_ratio(value: float)

float get_randomness_ratio()

Emission lifetime randomness ratio.

Curve scale_amount_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's scale will vary along this Curve. Should be a unit Curve.

float scale_amount_max = 1.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial scale applied to each particle.

float scale_amount_min = 1.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of scale_amount_max.

Curve scale_curve_x 🔗

void set_scale_curve_x(value: Curve)

Curve get_scale_curve_x()

Each particle's horizontal scale will vary along this Curve. Should be a unit Curve.

split_scale must be enabled.

Curve scale_curve_y 🔗

void set_scale_curve_y(value: Curve)

Curve get_scale_curve_y()

Each particle's vertical scale will vary along this Curve. Should be a unit Curve.

split_scale must be enabled.

void set_seed(value: int)

Sets the random seed used by the particle system. Only effective if use_fixed_seed is true.

float speed_scale = 1.0 🔗

void set_speed_scale(value: float)

float get_speed_scale()

Particle system's running speed scaling ratio. A value of 0 can be used to pause the particles.

bool split_scale = false 🔗

void set_split_scale(value: bool)

bool get_split_scale()

If true, the scale curve will be split into x and y components. See scale_curve_x and scale_curve_y.

float spread = 45.0 🔗

void set_spread(value: float)

Each particle's initial direction range from +spread to -spread degrees.

Curve tangential_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's tangential acceleration will vary along this Curve. Should be a unit Curve.

float tangential_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum tangential acceleration applied to each particle. Tangential acceleration is perpendicular to the particle's velocity giving the particles a swirling motion.

float tangential_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum equivalent of tangential_accel_max.

void set_texture(value: Texture2D)

Texture2D get_texture()

Particle texture. If null, particles will be squares.

bool use_fixed_seed = false 🔗

void set_use_fixed_seed(value: bool)

bool get_use_fixed_seed()

If true, particles will use the same seed for every simulation using the seed defined in seed. This is useful for situations where the visual outcome should be consistent across replays, for example when using Movie Maker mode.

void convert_from_particles(particles: Node) 🔗

Sets this node's properties to match a given GPUParticles2D node with an assigned ParticleProcessMaterial.

Curve get_param_curve(param: Parameter) const 🔗

Returns the Curve of the parameter specified by Parameter.

float get_param_max(param: Parameter) const 🔗

Returns the maximum value range for the given parameter.

float get_param_min(param: Parameter) const 🔗

Returns the minimum value range for the given parameter.

bool get_particle_flag(particle_flag: ParticleFlags) const 🔗

Returns the enabled state of the given particle flag.

void request_particles_process(process_time: float) 🔗

Requests the particles to process for extra process time during a single frame.

Useful for particle playback, if used in combination with use_fixed_seed or by calling restart() with parameter keep_seed set to true.

void restart(keep_seed: bool = false) 🔗

Restarts the particle emitter.

If keep_seed is true, the current random seed will be preserved. Useful for seeking and playback.

void set_param_curve(param: Parameter, curve: Curve) 🔗

Sets the Curve of the parameter specified by Parameter. Should be a unit Curve.

void set_param_max(param: Parameter, value: float) 🔗

Sets the maximum value for the given parameter.

void set_param_min(param: Parameter, value: float) 🔗

Sets the minimum value for the given parameter.

void set_particle_flag(particle_flag: ParticleFlags, enable: bool) 🔗

Enables or disables the given particle flag.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CPUParticles3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_cpuparticles3d.html

**Contents:**
- CPUParticles3D
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

A CPU-based 3D particle emitter.

CPU-based 3D particle node used to create a variety of particle systems and effects.

See also GPUParticles3D, which provides the same functionality with hardware acceleration, but may not run on older devices.

Particle systems (3D)

angular_velocity_curve

emission_ring_cone_angle

emission_ring_inner_radius

emission_sphere_radius

particle_flag_align_y

particle_flag_disable_z

particle_flag_rotate_y

tangential_accel_curve

AABB(0, 0, 0, 0, 0, 0)

convert_from_particles(particles: Node)

get_param_curve(param: Parameter) const

get_param_max(param: Parameter) const

get_param_min(param: Parameter) const

get_particle_flag(particle_flag: ParticleFlags) const

request_particles_process(process_time: float)

restart(keep_seed: bool = false)

set_param_curve(param: Parameter, curve: Curve)

set_param_max(param: Parameter, value: float)

set_param_min(param: Parameter, value: float)

set_particle_flag(particle_flag: ParticleFlags, enable: bool)

Emitted when all active particles have finished processing. When one_shot is disabled, particles will process continuously, so this is never emitted.

DrawOrder DRAW_ORDER_INDEX = 0

Particles are drawn in the order emitted.

DrawOrder DRAW_ORDER_LIFETIME = 1

Particles are drawn in order of remaining lifetime. In other words, the particle with the highest lifetime is drawn at the front.

DrawOrder DRAW_ORDER_VIEW_DEPTH = 2

Particles are drawn in order of depth.

Parameter PARAM_INITIAL_LINEAR_VELOCITY = 0

Use with set_param_min(), set_param_max(), and set_param_curve() to set initial velocity properties.

Parameter PARAM_ANGULAR_VELOCITY = 1

Use with set_param_min(), set_param_max(), and set_param_curve() to set angular velocity properties.

Parameter PARAM_ORBIT_VELOCITY = 2

Use with set_param_min(), set_param_max(), and set_param_curve() to set orbital velocity properties.

Parameter PARAM_LINEAR_ACCEL = 3

Use with set_param_min(), set_param_max(), and set_param_curve() to set linear acceleration properties.

Parameter PARAM_RADIAL_ACCEL = 4

Use with set_param_min(), set_param_max(), and set_param_curve() to set radial acceleration properties.

Parameter PARAM_TANGENTIAL_ACCEL = 5

Use with set_param_min(), set_param_max(), and set_param_curve() to set tangential acceleration properties.

Parameter PARAM_DAMPING = 6

Use with set_param_min(), set_param_max(), and set_param_curve() to set damping properties.

Parameter PARAM_ANGLE = 7

Use with set_param_min(), set_param_max(), and set_param_curve() to set angle properties.

Parameter PARAM_SCALE = 8

Use with set_param_min(), set_param_max(), and set_param_curve() to set scale properties.

Parameter PARAM_HUE_VARIATION = 9

Use with set_param_min(), set_param_max(), and set_param_curve() to set hue variation properties.

Parameter PARAM_ANIM_SPEED = 10

Use with set_param_min(), set_param_max(), and set_param_curve() to set animation speed properties.

Parameter PARAM_ANIM_OFFSET = 11

Use with set_param_min(), set_param_max(), and set_param_curve() to set animation offset properties.

Parameter PARAM_MAX = 12

Represents the size of the Parameter enum.

enum ParticleFlags: 🔗

ParticleFlags PARTICLE_FLAG_ALIGN_Y_TO_VELOCITY = 0

Use with set_particle_flag() to set particle_flag_align_y.

ParticleFlags PARTICLE_FLAG_ROTATE_Y = 1

Use with set_particle_flag() to set particle_flag_rotate_y.

ParticleFlags PARTICLE_FLAG_DISABLE_Z = 2

Use with set_particle_flag() to set particle_flag_disable_z.

ParticleFlags PARTICLE_FLAG_MAX = 3

Represents the size of the ParticleFlags enum.

enum EmissionShape: 🔗

EmissionShape EMISSION_SHAPE_POINT = 0

All particles will be emitted from a single point.

EmissionShape EMISSION_SHAPE_SPHERE = 1

Particles will be emitted in the volume of a sphere.

EmissionShape EMISSION_SHAPE_SPHERE_SURFACE = 2

Particles will be emitted on the surface of a sphere.

EmissionShape EMISSION_SHAPE_BOX = 3

Particles will be emitted in the volume of a box.

EmissionShape EMISSION_SHAPE_POINTS = 4

Particles will be emitted at a position chosen randomly among emission_points. Particle color will be modulated by emission_colors.

EmissionShape EMISSION_SHAPE_DIRECTED_POINTS = 5

Particles will be emitted at a position chosen randomly among emission_points. Particle velocity and rotation will be set based on emission_normals. Particle color will be modulated by emission_colors.

EmissionShape EMISSION_SHAPE_RING = 6

Particles will be emitted in a ring or cylinder.

EmissionShape EMISSION_SHAPE_MAX = 7

Represents the size of the EmissionShape enum.

void set_amount(value: int)

Number of particles emitted in one emission cycle.

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's rotation will be animated along this Curve. Should be a unit Curve.

float angle_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

float angle_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Curve angular_velocity_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's angular velocity (rotation speed) will vary along this Curve over its lifetime. Should be a unit Curve.

float angular_velocity_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum initial angular velocity (rotation speed) applied to each particle in degrees per second.

float angular_velocity_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum initial angular velocity (rotation speed) applied to each particle in degrees per second.

Curve anim_offset_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's animation offset will vary along this Curve. Should be a unit Curve.

float anim_offset_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum animation offset.

float anim_offset_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum animation offset.

Curve anim_speed_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's animation speed will vary along this Curve. Should be a unit Curve.

float anim_speed_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum particle animation speed.

float anim_speed_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum particle animation speed.

Color color = Color(1, 1, 1, 1) 🔗

void set_color(value: Color)

Each particle's initial color.

Note: color multiplies the particle mesh's vertex colors. To have a visible effect on a BaseMaterial3D, BaseMaterial3D.vertex_color_use_as_albedo must be true. For a ShaderMaterial, ALBEDO *= COLOR.rgb; must be inserted in the shader's fragment() function. Otherwise, color will have no visible effect.

Gradient color_initial_ramp 🔗

void set_color_initial_ramp(value: Gradient)

Gradient get_color_initial_ramp()

Each particle's initial color will vary along this Gradient (multiplied with color).

Note: color_initial_ramp multiplies the particle mesh's vertex colors. To have a visible effect on a BaseMaterial3D, BaseMaterial3D.vertex_color_use_as_albedo must be true. For a ShaderMaterial, ALBEDO *= COLOR.rgb; must be inserted in the shader's fragment() function. Otherwise, color_initial_ramp will have no visible effect.

Gradient color_ramp 🔗

void set_color_ramp(value: Gradient)

Gradient get_color_ramp()

Each particle's color will vary along this Gradient over its lifetime (multiplied with color).

Note: color_ramp multiplies the particle mesh's vertex colors. To have a visible effect on a BaseMaterial3D, BaseMaterial3D.vertex_color_use_as_albedo must be true. For a ShaderMaterial, ALBEDO *= COLOR.rgb; must be inserted in the shader's fragment() function. Otherwise, color_ramp will have no visible effect.

Curve damping_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Damping will vary along this Curve. Should be a unit Curve.

float damping_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

float damping_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Vector3 direction = Vector3(1, 0, 0) 🔗

void set_direction(value: Vector3)

Vector3 get_direction()

Unit vector specifying the particles' emission direction.

DrawOrder draw_order = 0 🔗

void set_draw_order(value: DrawOrder)

DrawOrder get_draw_order()

Vector3 emission_box_extents 🔗

void set_emission_box_extents(value: Vector3)

Vector3 get_emission_box_extents()

The rectangle's extents if emission_shape is set to EMISSION_SHAPE_BOX.

PackedColorArray emission_colors = PackedColorArray() 🔗

void set_emission_colors(value: PackedColorArray)

PackedColorArray get_emission_colors()

Sets the Colors to modulate particles by when using EMISSION_SHAPE_POINTS or EMISSION_SHAPE_DIRECTED_POINTS.

Note: emission_colors multiplies the particle mesh's vertex colors. To have a visible effect on a BaseMaterial3D, BaseMaterial3D.vertex_color_use_as_albedo must be true. For a ShaderMaterial, ALBEDO *= COLOR.rgb; must be inserted in the shader's fragment() function. Otherwise, emission_colors will have no visible effect.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedColorArray for more details.

PackedVector3Array emission_normals 🔗

void set_emission_normals(value: PackedVector3Array)

PackedVector3Array get_emission_normals()

Sets the direction the particles will be emitted in when using EMISSION_SHAPE_DIRECTED_POINTS.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector3Array for more details.

PackedVector3Array emission_points 🔗

void set_emission_points(value: PackedVector3Array)

PackedVector3Array get_emission_points()

Sets the initial positions to spawn particles when using EMISSION_SHAPE_POINTS or EMISSION_SHAPE_DIRECTED_POINTS.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector3Array for more details.

Vector3 emission_ring_axis 🔗

void set_emission_ring_axis(value: Vector3)

Vector3 get_emission_ring_axis()

The axis of the ring when using the emitter EMISSION_SHAPE_RING.

float emission_ring_cone_angle 🔗

void set_emission_ring_cone_angle(value: float)

float get_emission_ring_cone_angle()

The angle of the cone when using the emitter EMISSION_SHAPE_RING. The default angle of 90 degrees results in a ring, while an angle of 0 degrees results in a cone. Intermediate values will result in a ring where one end is larger than the other.

Note: Depending on emission_ring_height, the angle may be clamped if the ring's end is reached to form a perfect cone.

float emission_ring_height 🔗

void set_emission_ring_height(value: float)

float get_emission_ring_height()

The height of the ring when using the emitter EMISSION_SHAPE_RING.

float emission_ring_inner_radius 🔗

void set_emission_ring_inner_radius(value: float)

float get_emission_ring_inner_radius()

The inner radius of the ring when using the emitter EMISSION_SHAPE_RING.

float emission_ring_radius 🔗

void set_emission_ring_radius(value: float)

float get_emission_ring_radius()

The radius of the ring when using the emitter EMISSION_SHAPE_RING.

EmissionShape emission_shape = 0 🔗

void set_emission_shape(value: EmissionShape)

EmissionShape get_emission_shape()

Particles will be emitted inside this region.

float emission_sphere_radius 🔗

void set_emission_sphere_radius(value: float)

float get_emission_sphere_radius()

The sphere's radius if EmissionShape is set to EMISSION_SHAPE_SPHERE.

bool emitting = true 🔗

void set_emitting(value: bool)

If true, particles are being emitted. emitting can be used to start and stop particles from emitting. However, if one_shot is true setting emitting to true will not restart the emission cycle until after all active particles finish processing. You can use the finished signal to be notified once all active particles finish processing.

float explosiveness = 0.0 🔗

void set_explosiveness_ratio(value: float)

float get_explosiveness_ratio()

How rapidly particles in an emission cycle are emitted. If greater than 0, there will be a gap in emissions before the next cycle begins.

void set_fixed_fps(value: int)

The particle system's frame rate is fixed to a value. For example, changing the value to 2 will make the particles render at 2 frames per second. Note this does not slow down the particle system itself.

float flatness = 0.0 🔗

void set_flatness(value: float)

Amount of spread in Y/Z plane. A value of 1 restricts particles to X/Z plane.

bool fract_delta = true 🔗

void set_fractional_delta(value: bool)

bool get_fractional_delta()

If true, results in fractional delta calculation which has a smoother particles display effect.

Vector3 gravity = Vector3(0, -9.8, 0) 🔗

void set_gravity(value: Vector3)

Vector3 get_gravity()

Gravity applied to every particle.

Curve hue_variation_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's hue will vary along this Curve. Should be a unit Curve.

float hue_variation_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum hue variation.

float hue_variation_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum hue variation.

float initial_velocity_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum value of the initial velocity.

float initial_velocity_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum value of the initial velocity.

float lifetime = 1.0 🔗

void set_lifetime(value: float)

Amount of time each particle will exist.

float lifetime_randomness = 0.0 🔗

void set_lifetime_randomness(value: float)

float get_lifetime_randomness()

Particle lifetime randomness ratio.

Curve linear_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's linear acceleration will vary along this Curve. Should be a unit Curve.

float linear_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum linear acceleration.

float linear_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum linear acceleration.

bool local_coords = false 🔗

void set_use_local_coordinates(value: bool)

bool get_use_local_coordinates()

If true, particles use the parent node's coordinate space (known as local coordinates). This will cause particles to move and rotate along the CPUParticles3D node (and its parents) when it is moved or rotated. If false, particles use global coordinates; they will not move or rotate along the CPUParticles3D node (and its parents) when it is moved or rotated.

void set_mesh(value: Mesh)

The Mesh used for each particle. If null, particles will be spheres.

bool one_shot = false 🔗

void set_one_shot(value: bool)

If true, only one emission cycle occurs. If set true during a cycle, emission will stop at the cycle's end.

Curve orbit_velocity_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's orbital velocity will vary along this Curve. Should be a unit Curve.

float orbit_velocity_max 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum orbit velocity.

float orbit_velocity_min 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum orbit velocity.

bool particle_flag_align_y = false 🔗

void set_particle_flag(particle_flag: ParticleFlags, enable: bool)

bool get_particle_flag(particle_flag: ParticleFlags) const

Align Y axis of particle with the direction of its velocity.

bool particle_flag_disable_z = false 🔗

void set_particle_flag(particle_flag: ParticleFlags, enable: bool)

bool get_particle_flag(particle_flag: ParticleFlags) const

If true, particles will not move on the Z axis.

bool particle_flag_rotate_y = false 🔗

void set_particle_flag(particle_flag: ParticleFlags, enable: bool)

bool get_particle_flag(particle_flag: ParticleFlags) const

If true, particles rotate around Y axis by angle_min.

float preprocess = 0.0 🔗

void set_pre_process_time(value: float)

float get_pre_process_time()

Particle system starts as if it had already run for this many seconds.

Curve radial_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's radial acceleration will vary along this Curve. Should be a unit Curve.

float radial_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum radial acceleration.

float radial_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum radial acceleration.

float randomness = 0.0 🔗

void set_randomness_ratio(value: float)

float get_randomness_ratio()

Emission lifetime randomness ratio.

Curve scale_amount_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's scale will vary along this Curve. Should be a unit Curve.

float scale_amount_max = 1.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

float scale_amount_min = 1.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Curve scale_curve_x 🔗

void set_scale_curve_x(value: Curve)

Curve get_scale_curve_x()

Curve for the scale over life, along the x axis.

Curve scale_curve_y 🔗

void set_scale_curve_y(value: Curve)

Curve get_scale_curve_y()

Curve for the scale over life, along the y axis.

Curve scale_curve_z 🔗

void set_scale_curve_z(value: Curve)

Curve get_scale_curve_z()

Curve for the scale over life, along the z axis.

void set_seed(value: int)

Sets the random seed used by the particle system. Only effective if use_fixed_seed is true.

float speed_scale = 1.0 🔗

void set_speed_scale(value: float)

float get_speed_scale()

Particle system's running speed scaling ratio. A value of 0 can be used to pause the particles.

bool split_scale = false 🔗

void set_split_scale(value: bool)

bool get_split_scale()

If set to true, three different scale curves can be specified, one per scale axis.

float spread = 45.0 🔗

void set_spread(value: float)

Each particle's initial direction range from +spread to -spread degrees. Applied to X/Z plane and Y/Z planes.

Curve tangential_accel_curve 🔗

void set_param_curve(param: Parameter, curve: Curve)

Curve get_param_curve(param: Parameter) const

Each particle's tangential acceleration will vary along this Curve. Should be a unit Curve.

float tangential_accel_max = 0.0 🔗

void set_param_max(param: Parameter, value: float)

float get_param_max(param: Parameter) const

Maximum tangent acceleration.

float tangential_accel_min = 0.0 🔗

void set_param_min(param: Parameter, value: float)

float get_param_min(param: Parameter) const

Minimum tangent acceleration.

bool use_fixed_seed = false 🔗

void set_use_fixed_seed(value: bool)

bool get_use_fixed_seed()

If true, particles will use the same seed for every simulation using the seed defined in seed. This is useful for situations where the visual outcome should be consistent across replays, for example when using Movie Maker mode.

AABB visibility_aabb = AABB(0, 0, 0, 0, 0, 0) 🔗

void set_visibility_aabb(value: AABB)

AABB get_visibility_aabb()

The AABB that determines the node's region which needs to be visible on screen for the particle system to be active.

Grow the box if particles suddenly appear/disappear when the node enters/exits the screen. The AABB can be grown via code or with the Particles → Generate AABB editor tool.

AABB capture_aabb() const 🔗

Returns the axis-aligned bounding box that contains all the particles that are active in the current frame.

void convert_from_particles(particles: Node) 🔗

Sets this node's properties to match a given GPUParticles3D node with an assigned ParticleProcessMaterial.

Curve get_param_curve(param: Parameter) const 🔗

Returns the Curve of the parameter specified by Parameter.

float get_param_max(param: Parameter) const 🔗

Returns the maximum value range for the given parameter.

float get_param_min(param: Parameter) const 🔗

Returns the minimum value range for the given parameter.

bool get_particle_flag(particle_flag: ParticleFlags) const 🔗

Returns the enabled state of the given particle flag.

void request_particles_process(process_time: float) 🔗

Requests the particles to process for extra process time during a single frame.

Useful for particle playback, if used in combination with use_fixed_seed or by calling restart() with parameter keep_seed set to true.

void restart(keep_seed: bool = false) 🔗

Restarts the particle emitter.

If keep_seed is true, the current random seed will be preserved. Useful for seeking and playback.

void set_param_curve(param: Parameter, curve: Curve) 🔗

Sets the Curve of the parameter specified by Parameter. Should be a unit Curve.

void set_param_max(param: Parameter, value: float) 🔗

Sets the maximum value for the given parameter.

void set_param_min(param: Parameter, value: float) 🔗

Sets the minimum value for the given parameter.

void set_particle_flag(particle_flag: ParticleFlags, enable: bool) 🔗

Enables or disables the given particle flag.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## ConfirmationDialog — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_confirmationdialog.html

**Contents:**
- ConfirmationDialog
- Description
- Properties
- Methods
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: AcceptDialog < Window < Viewport < Node < Object

Inherited By: EditorCommandPalette, EditorFileDialog, FileDialog, ScriptCreateDialog

A dialog used for confirmation of actions.

A dialog used for confirmation of actions. This window is similar to AcceptDialog, but pressing its Cancel button can have a different outcome from pressing the OK button. The order of the two buttons varies depending on the host OS.

To get cancel action, you can use:

Vector2i(200, 70) (overrides Window)

Vector2i(200, 100) (overrides Window)

"Please Confirm..." (overrides Window)

String cancel_button_text = "Cancel" 🔗

void set_cancel_button_text(value: String)

String get_cancel_button_text()

The text displayed by the cancel button (see get_cancel_button()).

Button get_cancel_button() 🔗

Returns the cancel button.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
get_cancel_button().pressed.connect(_on_canceled)
```

Example 2 (unknown):
```unknown
GetCancelButton().Pressed += OnCanceled;
```

---

## CopyTransformModifier3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_copytransformmodifier3d.html

**Contents:**
- CopyTransformModifier3D
- Description
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: BoneConstraint3D < SkeletonModifier3D < Node3D < Node < Object

A SkeletonModifier3D that apply transform to the bone which copied from reference.

Apply the copied transform of the bone set by BoneConstraint3D.set_reference_bone() to the bone set by BoneConstraint3D.set_apply_bone() with processing it with some masks and options.

There are 4 ways to apply the transform, depending on the combination of set_relative() and set_additive().

Extract reference pose relative to the rest and add it to the apply bone's pose.

Relative + Not Additive:

Extract reference pose relative to the rest and add it to the apply bone's rest.

Not Relative + Additive:

Extract reference pose absolutely and add it to the apply bone's pose.

Not Relative + Not Additive:

Extract reference pose absolutely and the apply bone's pose is replaced with it.

get_axis_flags(index: int) const

BitField[TransformFlag]

get_copy_flags(index: int) const

get_invert_flags(index: int) const

is_additive(index: int) const

is_axis_x_enabled(index: int) const

is_axis_x_inverted(index: int) const

is_axis_y_enabled(index: int) const

is_axis_y_inverted(index: int) const

is_axis_z_enabled(index: int) const

is_axis_z_inverted(index: int) const

is_position_copying(index: int) const

is_relative(index: int) const

is_rotation_copying(index: int) const

is_scale_copying(index: int) const

set_additive(index: int, enabled: bool)

set_axis_flags(index: int, axis_flags: BitField[AxisFlag])

set_axis_x_enabled(index: int, enabled: bool)

set_axis_x_inverted(index: int, enabled: bool)

set_axis_y_enabled(index: int, enabled: bool)

set_axis_y_inverted(index: int, enabled: bool)

set_axis_z_enabled(index: int, enabled: bool)

set_axis_z_inverted(index: int, enabled: bool)

set_copy_flags(index: int, copy_flags: BitField[TransformFlag])

set_copy_position(index: int, enabled: bool)

set_copy_rotation(index: int, enabled: bool)

set_copy_scale(index: int, enabled: bool)

set_invert_flags(index: int, axis_flags: BitField[AxisFlag])

set_relative(index: int, enabled: bool)

flags TransformFlag: 🔗

TransformFlag TRANSFORM_FLAG_POSITION = 1

If set, allows to copy the position.

TransformFlag TRANSFORM_FLAG_ROTATION = 2

If set, allows to copy the rotation.

TransformFlag TRANSFORM_FLAG_SCALE = 4

If set, allows to copy the scale.

TransformFlag TRANSFORM_FLAG_ALL = 7

If set, allows to copy the position/rotation/scale.

AxisFlag AXIS_FLAG_X = 1

If set, allows to process the X-axis.

AxisFlag AXIS_FLAG_Y = 2

If set, allows to process the Y-axis.

AxisFlag AXIS_FLAG_Z = 4

If set, allows to process the Z-axis.

AxisFlag AXIS_FLAG_ALL = 7

If set, allows to process the all axes.

int setting_count = 0 🔗

void set_setting_count(value: int)

int get_setting_count()

The number of settings in the modifier.

BitField[AxisFlag] get_axis_flags(index: int) const 🔗

Returns the axis flags of the setting at index.

BitField[TransformFlag] get_copy_flags(index: int) const 🔗

Returns the copy flags of the setting at index.

BitField[AxisFlag] get_invert_flags(index: int) const 🔗

Returns the invert flags of the setting at index.

bool is_additive(index: int) const 🔗

Returns true if the additive option is enabled in the setting at index.

bool is_axis_x_enabled(index: int) const 🔗

Returns true if the enable flags has the flag for the X-axis in the setting at index. See also set_axis_flags().

bool is_axis_x_inverted(index: int) const 🔗

Returns true if the invert flags has the flag for the X-axis in the setting at index. See also set_invert_flags().

bool is_axis_y_enabled(index: int) const 🔗

Returns true if the enable flags has the flag for the Y-axis in the setting at index. See also set_axis_flags().

bool is_axis_y_inverted(index: int) const 🔗

Returns true if the invert flags has the flag for the Y-axis in the setting at index. See also set_invert_flags().

bool is_axis_z_enabled(index: int) const 🔗

Returns true if the enable flags has the flag for the Z-axis in the setting at index. See also set_axis_flags().

bool is_axis_z_inverted(index: int) const 🔗

Returns true if the invert flags has the flag for the Z-axis in the setting at index. See also set_invert_flags().

bool is_position_copying(index: int) const 🔗

Returns true if the copy flags has the flag for the position in the setting at index. See also set_copy_flags().

bool is_relative(index: int) const 🔗

Returns true if the relative option is enabled in the setting at index.

bool is_rotation_copying(index: int) const 🔗

Returns true if the copy flags has the flag for the rotation in the setting at index. See also set_copy_flags().

bool is_scale_copying(index: int) const 🔗

Returns true if the copy flags has the flag for the scale in the setting at index. See also set_copy_flags().

void set_additive(index: int, enabled: bool) 🔗

Sets additive option in the setting at index to enabled. This mainly affects the process of applying transform to the BoneConstraint3D.set_apply_bone().

If sets enabled to true, the processed transform is added to the pose of the current apply bone.

If sets enabled to false, the pose of the current apply bone is replaced with the processed transform. However, if set set_relative() to true, the transform is relative to rest.

void set_axis_flags(index: int, axis_flags: BitField[AxisFlag]) 🔗

Sets the flags to copy axes. If the flag is valid, the axis is copied.

void set_axis_x_enabled(index: int, enabled: bool) 🔗

If sets enabled to true, the X-axis will be copied.

void set_axis_x_inverted(index: int, enabled: bool) 🔗

If sets enabled to true, the X-axis will be inverted.

void set_axis_y_enabled(index: int, enabled: bool) 🔗

If sets enabled to true, the Y-axis will be copied.

void set_axis_y_inverted(index: int, enabled: bool) 🔗

If sets enabled to true, the Y-axis will be inverted.

void set_axis_z_enabled(index: int, enabled: bool) 🔗

If sets enabled to true, the Z-axis will be copied.

void set_axis_z_inverted(index: int, enabled: bool) 🔗

If sets enabled to true, the Z-axis will be inverted.

void set_copy_flags(index: int, copy_flags: BitField[TransformFlag]) 🔗

Sets the flags to process the transform operations. If the flag is valid, the transform operation is processed.

Note: If the rotation is valid for only one axis, it respects the roll of the valid axis. If the rotation is valid for two axes, it discards the roll of the invalid axis.

void set_copy_position(index: int, enabled: bool) 🔗

If sets enabled to true, the position will be copied.

void set_copy_rotation(index: int, enabled: bool) 🔗

If sets enabled to true, the rotation will be copied.

void set_copy_scale(index: int, enabled: bool) 🔗

If sets enabled to true, the scale will be copied.

void set_invert_flags(index: int, axis_flags: BitField[AxisFlag]) 🔗

Sets the flags to inverte axes. If the flag is valid, the axis is copied.

Note: An inverted scale means an inverse number, not a negative scale. For example, inverting 2.0 means 0.5.

Note: An inverted rotation flips the elements of the quaternion. For example, a two-axis inversion will flip the roll of each axis, and a three-axis inversion will flip the final orientation. However, be aware that flipping only one axis may cause unintended rotation by the unflipped axes, due to the characteristics of the quaternion.

void set_relative(index: int, enabled: bool) 🔗

Sets relative option in the setting at index to enabled.

If sets enabled to true, the extracted and applying transform is relative to the rest.

If sets enabled to false, the extracted transform is absolute.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGBox3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgbox3d.html

**Contents:**
- CSGBox3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: CSGPrimitive3D < CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

This node allows you to create a box for use with the CSG system.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

void set_material(value: Material)

Material get_material()

The material used to render the box.

Vector3 size = Vector3(1, 1, 1) 🔗

void set_size(value: Vector3)

The box's width, height and depth.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGShape3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgshape3d.html

**Contents:**
- CSGShape3D
- Description
- Tutorials
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

Inherited By: CSGCombiner3D, CSGPrimitive3D

This is the CSG base class that provides CSG operation support to the various CSG nodes in Godot.

Performance: CSG nodes are only intended for prototyping as they have a significant CPU performance cost. Consider baking final CSG operation results into static geometry that replaces the CSG nodes.

Individual CSG root node results can be baked to nodes with static resources with the editor menu that appears when a CSG root node is selected.

Individual CSG root nodes can also be baked to static resources with scripts by calling bake_static_mesh() for the visual mesh or bake_collision_shape() for the physics collision.

Entire scenes of CSG nodes can be baked to static geometry and exported with the editor glTF scene exporter: Scene > Export As... > glTF 2.0 Scene...

Prototyping levels with CSG

ConcavePolygonShape3D

bake_collision_shape()

get_collision_layer_value(layer_number: int) const

get_collision_mask_value(layer_number: int) const

is_root_shape() const

set_collision_layer_value(layer_number: int, value: bool)

set_collision_mask_value(layer_number: int, value: bool)

Operation OPERATION_UNION = 0

Geometry of both primitives is merged, intersecting geometry is removed.

Operation OPERATION_INTERSECTION = 1

Only intersecting geometry remains, the rest is removed.

Operation OPERATION_SUBTRACTION = 2

The second shape is subtracted from the first, leaving a dent with its shape.

bool calculate_tangents = true 🔗

void set_calculate_tangents(value: bool)

bool is_calculating_tangents()

Calculate tangents for the CSG shape which allows the use of normal and height maps. This is only applied on the root shape, this setting is ignored on any child. Setting this to false can speed up shape generation slightly.

int collision_layer = 1 🔗

void set_collision_layer(value: int)

int get_collision_layer()

The physics layers this area is in.

Collidable objects can exist in any of 32 different layers. These layers work like a tagging system, and are not visual. A collidable can use these layers to select with which objects it can collide, using the collision_mask property.

A contact is detected if object A is in any of the layers that object B scans, or object B is in any layer scanned by object A. See Collision layers and masks in the documentation for more information.

int collision_mask = 1 🔗

void set_collision_mask(value: int)

int get_collision_mask()

The physics layers this CSG shape scans for collisions. Only effective if use_collision is true. See Collision layers and masks in the documentation for more information.

float collision_priority = 1.0 🔗

void set_collision_priority(value: float)

float get_collision_priority()

The priority used to solve colliding when occurring penetration. Only effective if use_collision is true. The higher the priority is, the lower the penetration into the object will be. This can for example be used to prevent the player from breaking through the boundaries of a level.

Operation operation = 0 🔗

void set_operation(value: Operation)

Operation get_operation()

The operation that is performed on this shape. This is ignored for the first CSG child node as the operation is between this node and the previous child of this nodes parent.

void set_snap(value: float)

Deprecated: The CSG library no longer uses snapping.

This property does nothing.

bool use_collision = false 🔗

void set_use_collision(value: bool)

bool is_using_collision()

Adds a collision shape to the physics engine for our CSG shape. This will always act like a static body. Note that the collision shape is still active even if the CSG shape itself is hidden. See also collision_mask and collision_priority.

ConcavePolygonShape3D bake_collision_shape() 🔗

Returns a baked physics ConcavePolygonShape3D of this node's CSG operation result. Returns an empty shape if the node is not a CSG root node or has no valid geometry.

Performance: If the CSG operation results in a very detailed geometry with many faces physics performance will be very slow. Concave shapes should in general only be used for static level geometry and not with dynamic objects that are moving.

Note: CSG mesh data updates are deferred, which means they are updated with a delay of one rendered frame. To avoid getting an empty shape or outdated mesh data, make sure to call await get_tree().process_frame before using bake_collision_shape() in Node._ready() or after changing properties on the CSGShape3D.

ArrayMesh bake_static_mesh() 🔗

Returns a baked static ArrayMesh of this node's CSG operation result. Materials from involved CSG nodes are added as extra mesh surfaces. Returns an empty mesh if the node is not a CSG root node or has no valid geometry.

Note: CSG mesh data updates are deferred, which means they are updated with a delay of one rendered frame. To avoid getting an empty mesh or outdated mesh data, make sure to call await get_tree().process_frame before using bake_static_mesh() in Node._ready() or after changing properties on the CSGShape3D.

bool get_collision_layer_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_layer is enabled, given a layer_number between 1 and 32.

bool get_collision_mask_value(layer_number: int) const 🔗

Returns whether or not the specified layer of the collision_mask is enabled, given a layer_number between 1 and 32.

Array get_meshes() const 🔗

Returns an Array with two elements, the first is the Transform3D of this node and the second is the root Mesh of this node. Only works when this node is the root shape.

Note: CSG mesh data updates are deferred, which means they are updated with a delay of one rendered frame. To avoid getting an empty shape or outdated mesh data, make sure to call await get_tree().process_frame before using get_meshes() in Node._ready() or after changing properties on the CSGShape3D.

bool is_root_shape() const 🔗

Returns true if this is a root shape and is thus the object that is rendered.

void set_collision_layer_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_layer, given a layer_number between 1 and 32.

void set_collision_mask_value(layer_number: int, value: bool) 🔗

Based on value, enables or disables the specified layer in the collision_mask, given a layer_number between 1 and 32.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGCylinder3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgcylinder3d.html

**Contents:**
- CSGCylinder3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: CSGPrimitive3D < CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

A CSG Cylinder shape.

This node allows you to create a cylinder (or cone) for use with the CSG system.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

void set_cone(value: bool)

If true a cone is created, the radius will only apply to one side.

void set_height(value: float)

The height of the cylinder.

void set_material(value: Material)

Material get_material()

The material used to render the cylinder.

void set_radius(value: float)

The radius of the cylinder.

void set_sides(value: int)

The number of sides of the cylinder, the higher this number the more detail there will be in the cylinder.

bool smooth_faces = true 🔗

void set_smooth_faces(value: bool)

bool get_smooth_faces()

If true the normals of the cylinder are set to give a smooth effect making the cylinder seem rounded. If false the cylinder will have a flat shaded look.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGPolygon3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgpolygon3d.html

**Contents:**
- CSGPolygon3D
- Description
- Tutorials
- Properties
- Enumerations
- Property Descriptions
- User-contributed notes

Inherits: CSGPrimitive3D < CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

Extrudes a 2D polygon shape to create a 3D mesh.

An array of 2D points is extruded to quickly and easily create a variety of 3D meshes. See also CSGMesh3D for using 3D meshes as CSG nodes.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

path_rotation_accurate

PackedVector2Array(0, 0, 0, 1, 1, 1, 1, 0)

The polygon shape is extruded along the negative Z axis.

The polygon shape is extruded by rotating it around the Y axis.

The polygon shape is extruded along the Path3D specified in path_node.

PathRotation PATH_ROTATION_POLYGON = 0

The polygon shape is not rotated.

Note: Requires the path Z coordinates to continually decrease to ensure viable shapes.

PathRotation PATH_ROTATION_PATH = 1

The polygon shape is rotated along the path, but it is not rotated around the path axis.

Note: Requires the path Z coordinates to continually decrease to ensure viable shapes.

PathRotation PATH_ROTATION_PATH_FOLLOW = 2

The polygon shape follows the path and its rotations around the path axis.

enum PathIntervalType: 🔗

PathIntervalType PATH_INTERVAL_DISTANCE = 0

When mode is set to MODE_PATH, path_interval will determine the distance, in meters, each interval of the path will extrude.

PathIntervalType PATH_INTERVAL_SUBDIVIDE = 1

When mode is set to MODE_PATH, path_interval will subdivide the polygons along the path.

void set_depth(value: float)

When mode is MODE_DEPTH, the depth of the extrusion.

void set_material(value: Material)

Material get_material()

Material to use for the resulting mesh. The UV maps the top half of the material to the extruded shape (U along the length of the extrusions and V around the outline of the polygon), the bottom-left quarter to the front end face, and the bottom-right quarter to the back end face.

void set_mode(value: Mode)

The mode used to extrude the polygon.

bool path_continuous_u 🔗

void set_path_continuous_u(value: bool)

bool is_path_continuous_u()

When mode is MODE_PATH, by default, the top half of the material is stretched along the entire length of the extruded shape. If false the top half of the material is repeated every step of the extrusion.

float path_interval 🔗

void set_path_interval(value: float)

float get_path_interval()

When mode is MODE_PATH, the path interval or ratio of path points to extrusions.

PathIntervalType path_interval_type 🔗

void set_path_interval_type(value: PathIntervalType)

PathIntervalType get_path_interval_type()

When mode is MODE_PATH, this will determine if the interval should be by distance (PATH_INTERVAL_DISTANCE) or subdivision fractions (PATH_INTERVAL_SUBDIVIDE).

void set_path_joined(value: bool)

bool is_path_joined()

When mode is MODE_PATH, if true the ends of the path are joined, by adding an extrusion between the last and first points of the path.

void set_path_local(value: bool)

When mode is MODE_PATH, if true the Transform3D of the CSGPolygon3D is used as the starting point for the extrusions, not the Transform3D of the path_node.

void set_path_node(value: NodePath)

NodePath get_path_node()

When mode is MODE_PATH, the location of the Path3D object used to extrude the polygon.

PathRotation path_rotation 🔗

void set_path_rotation(value: PathRotation)

PathRotation get_path_rotation()

When mode is MODE_PATH, the path rotation method used to rotate the polygon as it is extruded.

bool path_rotation_accurate 🔗

void set_path_rotation_accurate(value: bool)

bool get_path_rotation_accurate()

When mode is MODE_PATH, if true the polygon will be rotated according to the proper tangent of the path at the sampled points. If false an approximation is used, which decreases in accuracy as the number of subdivisions decreases.

float path_simplify_angle 🔗

void set_path_simplify_angle(value: float)

float get_path_simplify_angle()

When mode is MODE_PATH, extrusions that are less than this angle, will be merged together to reduce polygon count.

float path_u_distance 🔗

void set_path_u_distance(value: float)

float get_path_u_distance()

When mode is MODE_PATH, this is the distance along the path, in meters, the texture coordinates will tile. When set to 0, texture coordinates will match geometry exactly with no tiling.

PackedVector2Array polygon = PackedVector2Array(0, 0, 0, 1, 1, 1, 1, 0) 🔗

void set_polygon(value: PackedVector2Array)

PackedVector2Array get_polygon()

The point array that defines the 2D polygon that is extruded. This can be a convex or concave polygon with 3 or more points. The polygon must not have any intersecting edges. Otherwise, triangulation will fail and no mesh will be generated.

Note: If only 1 or 2 points are defined in polygon, no mesh will be generated.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedVector2Array for more details.

bool smooth_faces = false 🔗

void set_smooth_faces(value: bool)

bool get_smooth_faces()

If true, applies smooth shading to the extrusions.

void set_spin_degrees(value: float)

float get_spin_degrees()

When mode is MODE_SPIN, the total number of degrees the polygon is rotated when extruding.

void set_spin_sides(value: int)

When mode is MODE_SPIN, the number of extrusions made.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGCombiner3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgcombiner3d.html

**Contents:**
- CSGCombiner3D
- Description
- Tutorials
- User-contributed notes

Inherits: CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

A CSG node that allows you to combine other CSG modifiers.

For complex arrangements of shapes, it is sometimes needed to add structure to your CSG nodes. The CSGCombiner3D node allows you to create this structure. The node encapsulates the result of the CSG operations of its children. In this way, it is possible to do operations on one set of shapes that are children of one CSGCombiner3D node, and a set of separate operations on a second set of shapes that are children of a second CSGCombiner3D node, and then do an operation that takes the two end results as its input to create the final shape.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGPrimitive3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgprimitive3d.html

**Contents:**
- CSGPrimitive3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

Inherited By: CSGBox3D, CSGCylinder3D, CSGMesh3D, CSGPolygon3D, CSGSphere3D, CSGTorus3D

Base class for CSG primitives.

Parent class for various CSG primitives. It contains code and functionality that is common between them. It cannot be used directly. Instead use one of the various classes that inherit from it.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

bool flip_faces = false 🔗

void set_flip_faces(value: bool)

bool get_flip_faces()

If set, the order of the vertices in each triangle are reversed resulting in the backside of the mesh being drawn.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGTorus3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgtorus3d.html

**Contents:**
- CSGTorus3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: CSGPrimitive3D < CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

This node allows you to create a torus for use with the CSG system.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

float inner_radius = 0.5 🔗

void set_inner_radius(value: float)

float get_inner_radius()

The inner radius of the torus.

void set_material(value: Material)

Material get_material()

The material used to render the torus.

float outer_radius = 1.0 🔗

void set_outer_radius(value: float)

float get_outer_radius()

The outer radius of the torus.

void set_ring_sides(value: int)

The number of edges each ring of the torus is constructed of.

void set_sides(value: int)

The number of slices the torus is constructed of.

bool smooth_faces = true 🔗

void set_smooth_faces(value: bool)

bool get_smooth_faces()

If true the normals of the torus are set to give a smooth effect making the torus seem rounded. If false the torus will have a flat shaded look.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## CSGSphere3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_csgsphere3d.html

**Contents:**
- CSGSphere3D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: CSGPrimitive3D < CSGShape3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

This node allows you to create a sphere for use with the CSG system.

Note: CSG nodes are intended to be used for level prototyping. Creating CSG nodes has a significant CPU cost compared to creating a MeshInstance3D with a PrimitiveMesh. Moving a CSG node within another CSG node also has a significant CPU cost, so it should be avoided during gameplay.

Prototyping levels with CSG

void set_material(value: Material)

Material get_material()

The material used to render the sphere.

int radial_segments = 12 🔗

void set_radial_segments(value: int)

int get_radial_segments()

Number of vertical slices for the sphere.

void set_radius(value: float)

Radius of the sphere.

void set_rings(value: int)

Number of horizontal slices for the sphere.

bool smooth_faces = true 🔗

void set_smooth_faces(value: bool)

bool get_smooth_faces()

If true the normals of the sphere are set to give a smooth effect making the sphere seem rounded. If false the sphere will have a flat shaded look.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## DampedSpringJoint2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_dampedspringjoint2d.html

**Contents:**
- DampedSpringJoint2D
- Description
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Joint2D < Node2D < CanvasItem < Node < Object

A physics joint that connects two 2D physics bodies with a spring-like force.

A physics joint that connects two 2D physics bodies with a spring-like force. This behaves like a spring that always wants to stretch to a given length.

float damping = 1.0 🔗

void set_damping(value: float)

The spring joint's damping ratio. A value between 0 and 1. When the two bodies move into different directions the system tries to align them to the spring axis again. A high damping value forces the attached bodies to align faster.

float length = 50.0 🔗

void set_length(value: float)

The spring joint's maximum length. The two attached bodies cannot stretch it past this value.

float rest_length = 0.0 🔗

void set_rest_length(value: float)

float get_rest_length()

When the bodies attached to the spring joint move they stretch or squash it. The joint always tries to resize towards this length.

float stiffness = 20.0 🔗

void set_stiffness(value: float)

float get_stiffness()

The higher the value, the less the bodies attached to the joint will deform it. The joint applies an opposing force to the bodies, the product of the stiffness multiplied by the size difference from its resting length.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Decal — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_decal.html

**Contents:**
- Decal
- Description
- Properties
- Methods
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: VisualInstance3D < Node3D < Node < Object

Node that projects a texture onto a MeshInstance3D.

Decals are used to project a texture onto a Mesh in the scene. Use Decals to add detail to a scene without affecting the underlying Mesh. They are often used to add weathering to building, add dirt or mud to the ground, or add variety to props. Decals can be moved at any time, making them suitable for things like blob shadows or laser sight dots.

They are made of an AABB and a group of Texture2Ds specifying Color, normal, ORM (ambient occlusion, roughness, metallic), and emission. Decals are projected within their AABB so altering the orientation of the Decal affects the direction in which they are projected. By default, Decals are projected down (i.e. from positive Y to negative Y).

The Texture2Ds associated with the Decal are automatically stored in a texture atlas which is used for drawing the decals so all decals can be drawn at once. Godot uses clustered decals, meaning they are stored in cluster data and drawn when the mesh is drawn, they are not drawn as a post-processing effect after.

Note: Decals cannot affect an underlying material's transparency, regardless of its transparency mode (alpha blend, alpha scissor, alpha hash, opaque pre-pass). This means translucent or transparent areas of a material will remain translucent or transparent even if an opaque decal is applied on them.

Note: Decals are only supported in the Forward+ and Mobile rendering methods, not Compatibility. When using the Mobile rendering method, only 8 decals can be displayed on each mesh resource. Attempting to display more than 8 decals on a single mesh resource will result in decals flickering in and out as the camera moves.

Note: When using the Mobile rendering method, decals will only correctly affect meshes whose visibility AABB intersects with the decal's AABB. If using a shader to deform the mesh in a way that makes it go outside its AABB, GeometryInstance3D.extra_cull_margin must be increased on the mesh. Otherwise, the decal may not be visible on the mesh.

distance_fade_enabled

get_texture(type: DecalTexture) const

set_texture(type: DecalTexture, texture: Texture2D)

DecalTexture TEXTURE_ALBEDO = 0

Texture2D corresponding to texture_albedo.

DecalTexture TEXTURE_NORMAL = 1

Texture2D corresponding to texture_normal.

DecalTexture TEXTURE_ORM = 2

Texture2D corresponding to texture_orm.

DecalTexture TEXTURE_EMISSION = 3

Texture2D corresponding to texture_emission.

DecalTexture TEXTURE_MAX = 4

Max size of DecalTexture enum.

float albedo_mix = 1.0 🔗

void set_albedo_mix(value: float)

float get_albedo_mix()

Blends the albedo Color of the decal with albedo Color of the underlying mesh. This can be set to 0.0 to create a decal that only affects normal or ORM. In this case, an albedo texture is still required as its alpha channel will determine where the normal and ORM will be overridden. See also modulate.

int cull_mask = 1048575 🔗

void set_cull_mask(value: int)

Specifies which VisualInstance3D.layers this decal will project on. By default, Decals affect all layers. This is used so you can specify which types of objects receive the Decal and which do not. This is especially useful so you can ensure that dynamic objects don't accidentally receive a Decal intended for the terrain under them.

float distance_fade_begin = 40.0 🔗

void set_distance_fade_begin(value: float)

float get_distance_fade_begin()

The distance from the camera at which the Decal begins to fade away (in 3D units).

bool distance_fade_enabled = false 🔗

void set_enable_distance_fade(value: bool)

bool is_distance_fade_enabled()

If true, decals will smoothly fade away when far from the active Camera3D starting at distance_fade_begin. The Decal will fade out over distance_fade_begin + distance_fade_length, after which it will be culled and not sent to the shader at all. Use this to reduce the number of active Decals in a scene and thus improve performance.

float distance_fade_length = 10.0 🔗

void set_distance_fade_length(value: float)

float get_distance_fade_length()

The distance over which the Decal fades (in 3D units). The Decal becomes slowly more transparent over this distance and is completely invisible at the end. Higher values result in a smoother fade-out transition, which is more suited when the camera moves fast.

float emission_energy = 1.0 🔗

void set_emission_energy(value: float)

float get_emission_energy()

Energy multiplier for the emission texture. This will make the decal emit light at a higher or lower intensity, independently of the albedo color. See also modulate.

float lower_fade = 0.3 🔗

void set_lower_fade(value: float)

float get_lower_fade()

Sets the curve over which the decal will fade as the surface gets further from the center of the AABB. Only positive values are valid (negative values will be clamped to 0.0). See also upper_fade.

Color modulate = Color(1, 1, 1, 1) 🔗

void set_modulate(value: Color)

Changes the Color of the Decal by multiplying the albedo and emission colors with this value. The alpha component is only taken into account when multiplying the albedo color, not the emission color. See also emission_energy and albedo_mix to change the emission and albedo intensity independently of each other.

float normal_fade = 0.0 🔗

void set_normal_fade(value: float)

float get_normal_fade()

Fades the Decal if the angle between the Decal's AABB and the target surface becomes too large. A value of 0 projects the Decal regardless of angle, a value of 1 limits the Decal to surfaces that are nearly perpendicular.

Note: Setting normal_fade to a value greater than 0.0 has a small performance cost due to the added normal angle computations.

Vector3 size = Vector3(2, 2, 2) 🔗

void set_size(value: Vector3)

Sets the size of the AABB used by the decal. All dimensions must be set to a value greater than zero (they will be clamped to 0.001 if this is not the case). The AABB goes from -size/2 to size/2.

Note: To improve culling efficiency of "hard surface" decals, set their upper_fade and lower_fade to 0.0 and set the Y component of the size as low as possible. This will reduce the decals' AABB size without affecting their appearance.

Texture2D texture_albedo 🔗

void set_texture(type: DecalTexture, texture: Texture2D)

Texture2D get_texture(type: DecalTexture) const

Texture2D with the base Color of the Decal. Either this or the texture_emission must be set for the Decal to be visible. Use the alpha channel like a mask to smoothly blend the edges of the decal with the underlying object.

Note: Unlike BaseMaterial3D whose filter mode can be adjusted on a per-material basis, the filter mode for Decal textures is set globally with ProjectSettings.rendering/textures/decals/filter.

Texture2D texture_emission 🔗

void set_texture(type: DecalTexture, texture: Texture2D)

Texture2D get_texture(type: DecalTexture) const

Texture2D with the emission Color of the Decal. Either this or the texture_albedo must be set for the Decal to be visible. Use the alpha channel like a mask to smoothly blend the edges of the decal with the underlying object.

Note: Unlike BaseMaterial3D whose filter mode can be adjusted on a per-material basis, the filter mode for Decal textures is set globally with ProjectSettings.rendering/textures/decals/filter.

Texture2D texture_normal 🔗

void set_texture(type: DecalTexture, texture: Texture2D)

Texture2D get_texture(type: DecalTexture) const

Texture2D with the per-pixel normal map for the decal. Use this to add extra detail to decals.

Note: Unlike BaseMaterial3D whose filter mode can be adjusted on a per-material basis, the filter mode for Decal textures is set globally with ProjectSettings.rendering/textures/decals/filter.

Note: Setting this texture alone will not result in a visible decal, as texture_albedo must also be set. To create a normal-only decal, load an albedo texture into texture_albedo and set albedo_mix to 0.0. The albedo texture's alpha channel will be used to determine where the underlying surface's normal map should be overridden (and its intensity).

Texture2D texture_orm 🔗

void set_texture(type: DecalTexture, texture: Texture2D)

Texture2D get_texture(type: DecalTexture) const

Texture2D storing ambient occlusion, roughness, and metallic for the decal. Use this to add extra detail to decals.

Note: Unlike BaseMaterial3D whose filter mode can be adjusted on a per-material basis, the filter mode for Decal textures is set globally with ProjectSettings.rendering/textures/decals/filter.

Note: Setting this texture alone will not result in a visible decal, as texture_albedo must also be set. To create an ORM-only decal, load an albedo texture into texture_albedo and set albedo_mix to 0.0. The albedo texture's alpha channel will be used to determine where the underlying surface's ORM map should be overridden (and its intensity).

float upper_fade = 0.3 🔗

void set_upper_fade(value: float)

float get_upper_fade()

Sets the curve over which the decal will fade as the surface gets further from the center of the AABB. Only positive values are valid (negative values will be clamped to 0.0). See also lower_fade.

Texture2D get_texture(type: DecalTexture) const 🔗

Returns the Texture2D associated with the specified DecalTexture. This is a convenience method, in most cases you should access the texture directly.

For example, instead of albedo_tex = $Decal.get_texture(Decal.TEXTURE_ALBEDO), use albedo_tex = $Decal.texture_albedo.

One case where this is better than accessing the texture directly is when you want to copy one Decal's textures to another. For example:

void set_texture(type: DecalTexture, texture: Texture2D) 🔗

Sets the Texture2D associated with the specified DecalTexture. This is a convenience method, in most cases you should access the texture directly.

For example, instead of $Decal.set_texture(Decal.TEXTURE_ALBEDO, albedo_tex), use $Decal.texture_albedo = albedo_tex.

One case where this is better than accessing the texture directly is when you want to copy one Decal's textures to another. For example:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (bash):
```bash
for i in Decal.TEXTURE_MAX:
    $NewDecal.set_texture(i, $OldDecal.get_texture(i))
```

Example 2 (json):
```json
for (int i = 0; i < (int)Decal.DecalTexture.Max; i++)
{
    GetNode<Decal>("NewDecal").SetTexture(i, GetNode<Decal>("OldDecal").GetTexture(i));
}
```

Example 3 (bash):
```bash
for i in Decal.TEXTURE_MAX:
    $NewDecal.set_texture(i, $OldDecal.get_texture(i))
```

Example 4 (json):
```json
for (int i = 0; i < (int)Decal.DecalTexture.Max; i++)
{
    GetNode<Decal>("NewDecal").SetTexture(i, GetNode<Decal>("OldDecal").GetTexture(i));
}
```

---

## DirectionalLight3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_directionallight3d.html

**Contents:**
- DirectionalLight3D
- Description
- Tutorials
- Properties
- Enumerations
- Property Descriptions
- User-contributed notes

Inherits: Light3D < VisualInstance3D < Node3D < Node < Object

Directional light from a distance, as from the Sun.

A directional light is a type of Light3D node that models an infinite number of parallel rays covering the entire scene. It is used for lights with strong intensity that are located far away from the scene to model sunlight or moonlight.

Light is emitted in the -Z direction of the node's global basis. For an unrotated light, this means that the light is emitted forwards, illuminating the front side of a 3D model (see Vector3.FORWARD and Vector3.MODEL_FRONT). The position of the node is ignored; only the basis is used to determine light direction.

3D lights and shadows

Faking global illumination

directional_shadow_blend_splits

directional_shadow_fade_start

directional_shadow_max_distance

directional_shadow_mode

directional_shadow_pancake_size

directional_shadow_split_1

directional_shadow_split_2

directional_shadow_split_3

ShadowMode SHADOW_ORTHOGONAL = 0

Renders the entire scene's shadow map from an orthogonal point of view. This is the fastest directional shadow mode. May result in blurrier shadows on close objects.

ShadowMode SHADOW_PARALLEL_2_SPLITS = 1

Splits the view frustum in 2 areas, each with its own shadow map. This shadow mode is a compromise between SHADOW_ORTHOGONAL and SHADOW_PARALLEL_4_SPLITS in terms of performance.

ShadowMode SHADOW_PARALLEL_4_SPLITS = 2

Splits the view frustum in 4 areas, each with its own shadow map. This is the slowest directional shadow mode.

SkyMode SKY_MODE_LIGHT_AND_SKY = 0

Makes the light visible in both scene lighting and sky rendering.

SkyMode SKY_MODE_LIGHT_ONLY = 1

Makes the light visible in scene lighting only (including direct lighting and global illumination). When using this mode, the light will not be visible from sky shaders.

SkyMode SKY_MODE_SKY_ONLY = 2

Makes the light visible to sky shaders only. When using this mode the light will not cast light into the scene (either through direct lighting or through global illumination), but can be accessed through sky shaders. This can be useful, for example, when you want to control sky effects without illuminating the scene (during a night cycle, for example).

bool directional_shadow_blend_splits = false 🔗

void set_blend_splits(value: bool)

bool is_blend_splits_enabled()

If true, shadow detail is sacrificed in exchange for smoother transitions between splits. Enabling shadow blend splitting also has a moderate performance cost. This is ignored when directional_shadow_mode is SHADOW_ORTHOGONAL.

float directional_shadow_fade_start = 0.8 🔗

void set_param(value: float)

Proportion of directional_shadow_max_distance at which point the shadow starts to fade. At directional_shadow_max_distance, the shadow will disappear. The default value is a balance between smooth fading and distant shadow visibility. If the camera moves fast and the directional_shadow_max_distance is low, consider lowering directional_shadow_fade_start below 0.8 to make shadow transitions less noticeable. On the other hand, if you tuned directional_shadow_max_distance to cover the entire scene, you can set directional_shadow_fade_start to 1.0 to prevent the shadow from fading in the distance (it will suddenly cut off instead).

float directional_shadow_max_distance = 100.0 🔗

void set_param(value: float)

The maximum distance for shadow splits. Increasing this value will make directional shadows visible from further away, at the cost of lower overall shadow detail and performance (since more objects need to be included in the directional shadow rendering).

ShadowMode directional_shadow_mode = 2 🔗

void set_shadow_mode(value: ShadowMode)

ShadowMode get_shadow_mode()

The light's shadow rendering algorithm.

float directional_shadow_pancake_size = 20.0 🔗

void set_param(value: float)

Sets the size of the directional shadow pancake. The pancake offsets the start of the shadow's camera frustum to provide a higher effective depth resolution for the shadow. However, a high pancake size can cause artifacts in the shadows of large objects that are close to the edge of the frustum. Reducing the pancake size can help. Setting the size to 0 turns off the pancaking effect.

float directional_shadow_split_1 = 0.1 🔗

void set_param(value: float)

The distance from camera to shadow split 1. Relative to directional_shadow_max_distance. Only used when directional_shadow_mode is SHADOW_PARALLEL_2_SPLITS or SHADOW_PARALLEL_4_SPLITS.

float directional_shadow_split_2 = 0.2 🔗

void set_param(value: float)

The distance from shadow split 1 to split 2. Relative to directional_shadow_max_distance. Only used when directional_shadow_mode is SHADOW_PARALLEL_4_SPLITS.

float directional_shadow_split_3 = 0.5 🔗

void set_param(value: float)

The distance from shadow split 2 to split 3. Relative to directional_shadow_max_distance. Only used when directional_shadow_mode is SHADOW_PARALLEL_4_SPLITS.

SkyMode sky_mode = 0 🔗

void set_sky_mode(value: SkyMode)

SkyMode get_sky_mode()

Whether this DirectionalLight3D is visible in the sky, in the scene, or both in the sky and in the scene.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## EditorFileSystem — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_editorfilesystem.html

**Contents:**
- EditorFileSystem
- Description
- Methods
- Signals
- Method Descriptions
- User-contributed notes

Inherits: Node < Object

Resource filesystem, as the editor sees it.

This object holds information of all resources in the filesystem, their types, etc.

Note: This class shouldn't be instantiated directly. Instead, access the singleton using EditorInterface.get_resource_filesystem().

get_file_type(path: String) const

EditorFileSystemDirectory

EditorFileSystemDirectory

get_filesystem_path(path: String)

get_scanning_progress() const

reimport_files(files: PackedStringArray)

update_file(path: String)

filesystem_changed() 🔗

Emitted if the filesystem changed.

resources_reimported(resources: PackedStringArray) 🔗

Emitted if a resource is reimported.

resources_reimporting(resources: PackedStringArray) 🔗

Emitted before a resource is reimported.

resources_reload(resources: PackedStringArray) 🔗

Emitted if at least one resource is reloaded when the filesystem is scanned.

script_classes_updated() 🔗

Emitted when the list of global script classes gets updated.

sources_changed(exist: bool) 🔗

Emitted if the source of any imported file changed.

String get_file_type(path: String) const 🔗

Returns the resource type of the file, given the full path. This returns a string such as "Resource" or "GDScript", not a file extension such as ".gd".

EditorFileSystemDirectory get_filesystem() 🔗

Gets the root directory object.

EditorFileSystemDirectory get_filesystem_path(path: String) 🔗

Returns a view into the filesystem at path.

float get_scanning_progress() const 🔗

Returns the scan progress for 0 to 1 if the FS is being scanned.

bool is_scanning() const 🔗

Returns true if the filesystem is being scanned.

void reimport_files(files: PackedStringArray) 🔗

Reimports a set of files. Call this if these files or their .import files were directly edited by script or an external program.

If the file type changed or the file was newly created, use update_file() or scan().

Note: This function blocks until the import is finished. However, the main loop iteration, including timers and Node._process(), will occur during the import process due to progress bar updates. Avoid calls to reimport_files() or scan() while an import is in progress.

Scan the filesystem for changes.

void scan_sources() 🔗

Check if the source of any imported resource changed.

void update_file(path: String) 🔗

Add a file in an existing directory, or schedule file information to be updated on editor restart. Can be used to update text files saved by an external program.

This will not import the file. To reimport, call reimport_files() or scan() methods.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## EditorInspector — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_editorinspector.html

**Contents:**
- EditorInspector
- Description
- Properties
- Methods
- Signals
- Method Descriptions
- User-contributed notes

Inherits: ScrollContainer < Container < Control < CanvasItem < Node < Object

A control used to edit properties of an object.

This is the control that implements property editing in the editor's Settings dialogs, the Inspector dock, etc. To get the EditorInspector used in the editor's Inspector dock, use EditorInterface.get_inspector().

EditorInspector will show properties in the same order as the array returned by Object.get_property_list().

If a property's name is path-like (i.e. if it contains forward slashes), EditorInspector will create nested sections for "directories" along the path. For example, if a property is named highlighting/gdscript/node_path_color, it will be shown as "Node Path Color" inside the "GDScript" section nested inside the "Highlighting" section.

If a property has @GlobalScope.PROPERTY_USAGE_GROUP usage, it will group subsequent properties whose name starts with the property's hint string. The group ends when a property does not start with that hint string or when a new group starts. An empty group name effectively ends the current group. EditorInspector will create a top-level section for each group. For example, if a property with group usage is named Collide With and its hint string is collide_with_, a subsequent collide_with_area property will be shown as "Area" inside the "Collide With" section. There is also a special case: when the hint string contains the name of a property, that property is grouped too. This is mainly to help grouping properties like font, font_color and font_size (using the hint string font_).

If a property has @GlobalScope.PROPERTY_USAGE_SUBGROUP usage, a subgroup will be created in the same way as a group, and a second-level section will be created for each subgroup.

Note: Unlike sections created from path-like property names, EditorInspector won't capitalize the name for sections created from groups. So properties with group usage usually use capitalized names instead of snake_cased names.

true (overrides ScrollContainer)

2 (overrides Control)

true (overrides ScrollContainer)

horizontal_scroll_mode

0 (overrides ScrollContainer)

get_selected_path() const

instantiate_property_editor(object: Object, type: Variant.Type, path: String, hint: PropertyHint, hint_text: String, usage: int, wide: bool = false) static

edited_object_changed() 🔗

Emitted when the object being edited by the inspector has changed.

object_id_selected(id: int) 🔗

Emitted when the Edit button of an Object has been pressed in the inspector. This is mainly used in the remote scene tree Inspector.

property_deleted(property: String) 🔗

Emitted when a property is removed from the inspector.

property_edited(property: String) 🔗

Emitted when a property is edited in the inspector.

property_keyed(property: String, value: Variant, advance: bool) 🔗

Emitted when a property is keyed in the inspector. Properties can be keyed by clicking the "key" icon next to a property when the Animation panel is toggled.

property_selected(property: String) 🔗

Emitted when a property is selected in the inspector.

property_toggled(property: String, checked: bool) 🔗

Emitted when a boolean property is toggled in the inspector.

Note: This signal is never emitted if the internal autoclear property enabled. Since this property is always enabled in the editor inspector, this signal is never emitted by the editor itself.

resource_selected(resource: Resource, path: String) 🔗

Emitted when a resource is selected in the inspector.

restart_requested() 🔗

Emitted when a property that requires a restart to be applied is edited in the inspector. This is only used in the Project Settings and Editor Settings.

void edit(object: Object) 🔗

Shows the properties of the given object in this inspector for editing. To clear the inspector, call this method with null.

Note: If you want to edit an object in the editor's main inspector, use the edit_* methods in EditorInterface instead.

Object get_edited_object() 🔗

Returns the object currently selected in this inspector.

String get_selected_path() const 🔗

Gets the path of the currently selected property.

EditorProperty instantiate_property_editor(object: Object, type: Variant.Type, path: String, hint: PropertyHint, hint_text: String, usage: int, wide: bool = false) static 🔗

Creates a property editor that can be used by plugin UI to edit the specified property of an object.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## DirectionalLight2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_directionallight2d.html

**Contents:**
- DirectionalLight2D
- Description
- Tutorials
- Properties
- Property Descriptions
- User-contributed notes

Inherits: Light2D < Node2D < CanvasItem < Node < Object

Directional 2D light from a distance.

A directional light is a type of Light2D node that models an infinite number of parallel rays covering the entire scene. It is used for lights with strong intensity that are located far away from the scene (for example: to model sunlight or moonlight).

Light is emitted in the +Y direction of the node's global basis. For an unrotated light, this means that the light is emitted downwards. The position of the node is ignored; only the basis is used to determine light direction.

Note: DirectionalLight2D does not support light cull masks (but it supports shadow cull masks). It will always light up 2D nodes, regardless of the 2D node's CanvasItem.light_mask.

2D lights and shadows

void set_height(value: float)

The height of the light. Used with 2D normal mapping. Ranges from 0 (parallel to the plane) to 1 (perpendicular to the plane).

float max_distance = 10000.0 🔗

void set_max_distance(value: float)

float get_max_distance()

The maximum distance from the camera center objects can be before their shadows are culled (in pixels). Decreasing this value can prevent objects located outside the camera from casting shadows (while also improving performance). Camera2D.zoom is not taken into account by max_distance, which means that at higher zoom values, shadows will appear to fade out sooner when zooming onto a given point.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## EditorFileDialog — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_editorfiledialog.html

**Contents:**
- EditorFileDialog
- Description
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: ConfirmationDialog < AcceptDialog < Window < Viewport < Node < Object

A modified version of FileDialog used by the editor.

EditorFileDialog is an enhanced version of FileDialog available only to editor plugins. Additional features include list of favorited/recent files and the ability to see files as thumbnails grid instead of list.

Unlike FileDialog, EditorFileDialog does not have a property for using native dialogs. Instead, native dialogs can be enabled globally via the EditorSettings.interface/editor/use_native_file_dialogs editor setting. They are also enabled automatically when running in sandbox (e.g. on macOS).

false (overrides AcceptDialog)

disable_overwrite_warning

"Save a File" (overrides Window)

add_filter(filter: String, description: String = "")

add_option(name: String, values: PackedStringArray, default_value_index: int)

add_side_menu(menu: Control, title: String = "")

clear_filename_filter()

get_filename_filter() const

get_option_default(option: int) const

get_option_name(option: int) const

get_option_values(option: int) const

get_selected_options() const

set_filename_filter(filter: String)

set_option_default(option: int, default_value_index: int)

set_option_name(option: int, name: String)

set_option_values(option: int, values: PackedStringArray)

dir_selected(dir: String) 🔗

Emitted when a directory is selected.

file_selected(path: String) 🔗

Emitted when a file is selected.

filename_filter_changed(filter: String) 🔗

Emitted when the filter for file names changes.

files_selected(paths: PackedStringArray) 🔗

Emitted when multiple files are selected.

FileMode FILE_MODE_OPEN_FILE = 0

The EditorFileDialog can select only one file. Accepting the window will open the file.

FileMode FILE_MODE_OPEN_FILES = 1

The EditorFileDialog can select multiple files. Accepting the window will open all files.

FileMode FILE_MODE_OPEN_DIR = 2

The EditorFileDialog can select only one directory. Accepting the window will open the directory.

FileMode FILE_MODE_OPEN_ANY = 3

The EditorFileDialog can select a file or directory. Accepting the window will open it.

FileMode FILE_MODE_SAVE_FILE = 4

The EditorFileDialog can select only one file. Accepting the window will save the file.

Access ACCESS_RESOURCES = 0

The EditorFileDialog can only view res:// directory contents.

Access ACCESS_USERDATA = 1

The EditorFileDialog can only view user:// directory contents.

Access ACCESS_FILESYSTEM = 2

The EditorFileDialog can view the entire local file system.

DisplayMode DISPLAY_THUMBNAILS = 0

The EditorFileDialog displays resources as thumbnails.

DisplayMode DISPLAY_LIST = 1

The EditorFileDialog displays resources as a list of filenames.

void set_access(value: Access)

The location from which the user may select a file, including res://, user://, and the local file system.

void set_current_dir(value: String)

String get_current_dir()

The currently occupied directory.

String current_file 🔗

void set_current_file(value: String)

String get_current_file()

The currently selected file.

String current_path 🔗

void set_current_path(value: String)

String get_current_path()

The file system path in the address bar.

bool disable_overwrite_warning = false 🔗

void set_disable_overwrite_warning(value: bool)

bool is_overwrite_warning_disabled()

If true, the EditorFileDialog will not warn the user before overwriting files.

DisplayMode display_mode = 0 🔗

void set_display_mode(value: DisplayMode)

DisplayMode get_display_mode()

The view format in which the EditorFileDialog displays resources to the user.

FileMode file_mode = 4 🔗

void set_file_mode(value: FileMode)

FileMode get_file_mode()

The dialog's open or save mode, which affects the selection behavior.

PackedStringArray filters = PackedStringArray() 🔗

void set_filters(value: PackedStringArray)

PackedStringArray get_filters()

The available file type filters. For example, this shows only .png and .gd files: set_filters(PackedStringArray(["*.png ; PNG Images","*.gd ; GDScript Files"])). Multiple file types can also be specified in a single filter. "*.png, *.jpg, *.jpeg ; Supported Images" will show both PNG and JPEG files when selected.

Note: The returned array is copied and any changes to it will not update the original property value. See PackedStringArray for more details.

int option_count = 0 🔗

void set_option_count(value: int)

int get_option_count()

The number of additional OptionButtons and CheckBoxes in the dialog.

bool show_hidden_files = false 🔗

void set_show_hidden_files(value: bool)

bool is_showing_hidden_files()

If true, hidden files and directories will be visible in the EditorFileDialog. This property is synchronized with EditorSettings.filesystem/file_dialog/show_hidden_files.

void add_filter(filter: String, description: String = "") 🔗

Adds a comma-separated file name filter option to the EditorFileDialog with an optional description, which restricts what files can be picked.

A filter should be of the form "filename.extension", where filename and extension can be * to match any string. Filters starting with . (i.e. empty filenames) are not allowed.

For example, a filter of "*.tscn, *.scn" and a description of "Scenes" results in filter text "Scenes (*.tscn, *.scn)".

void add_option(name: String, values: PackedStringArray, default_value_index: int) 🔗

Adds an additional OptionButton to the file dialog. If values is empty, a CheckBox is added instead.

default_value_index should be an index of the value in the values. If values is empty it should be either 1 (checked), or 0 (unchecked).

void add_side_menu(menu: Control, title: String = "") 🔗

Adds the given menu to the side of the file dialog with the given title text on top. Only one side menu is allowed.

void clear_filename_filter() 🔗

Clear the filter for file names.

void clear_filters() 🔗

Removes all filters except for "All Files (*.*)".

String get_filename_filter() const 🔗

Returns the value of the filter for file names.

LineEdit get_line_edit() 🔗

Returns the LineEdit for the selected file.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

int get_option_default(option: int) const 🔗

Returns the default value index of the OptionButton or CheckBox with index option.

String get_option_name(option: int) const 🔗

Returns the name of the OptionButton or CheckBox with index option.

PackedStringArray get_option_values(option: int) const 🔗

Returns an array of values of the OptionButton with index option.

Dictionary get_selected_options() const 🔗

Returns a Dictionary with the selected values of the additional OptionButtons and/or CheckBoxes. Dictionary keys are names and values are selected value indices.

VBoxContainer get_vbox() 🔗

Returns the VBoxContainer used to display the file system.

Warning: This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their CanvasItem.visible property.

Notify the EditorFileDialog that its view of the data is no longer accurate. Updates the view contents on next view update.

void popup_file_dialog() 🔗

Shows the EditorFileDialog at the default size and position for file dialogs in the editor, and selects the file name if there is a current file.

void set_filename_filter(filter: String) 🔗

Sets the value of the filter for file names.

void set_option_default(option: int, default_value_index: int) 🔗

Sets the default value index of the OptionButton or CheckBox with index option.

void set_option_name(option: int, name: String) 🔗

Sets the name of the OptionButton or CheckBox with index option.

void set_option_values(option: int, values: PackedStringArray) 🔗

Sets the option values of the OptionButton with index option.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
