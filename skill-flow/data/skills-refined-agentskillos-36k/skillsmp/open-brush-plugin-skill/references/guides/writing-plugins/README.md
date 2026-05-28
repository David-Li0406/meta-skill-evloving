# Writing Plugins

Plugins are written in the scripting language [Lua](https://www.lua.org) which is designed to be simple to learn and easy to understand. There's plenty of tutorials online and Lua is widely used in games and applications such as [Factorio](https://wiki.factorio.com/Tutorial:Scripting), [Garry's Mod](https://wiki.facepunch.com/gmod/Beginner_Tutorial_Intro)_,_ [Roblox](https://create.roblox.com/docs/tutorials/scripting/basic-scripting/intro-to-scripting), [LÖVR](https://lovr.org/) and many others.

If you've written scripts in any other language then you'll find it easy to pick up.&#x20;

If you've never programmed at all then Lua is a great place to start. Copy an example script to your Open Brush folder (there's a button next to each Plugin type that does this for you), open it up in a text editor and try changing things.

As soon as you save your changes, Open Brush will load the new version. If you've made a mistake then the console on the back of your brush hand will tell you what line the error is on.

## Libraries

In addition to the [API commands](https://icosa.gitbook.io/open-brush-plugin-scripting-docs) you can use most of the [Lua Standard Library](https://www.moonsharp.org/MoonSharpStdLib.pdf). Another included library is [Lume](https://github.com/rxi/lume) which you can use via `require "lume"`

### Built-in functions and properties

The following realtime values from the sketch are examples of values that are available to use in your scripts. There are many more. Here is a [full list of methods and properties for each type.](https://icosa.gitbook.io/open-brush-plugin-scripting-docs)

* **Brush.position:** \
  The current position of the brush pointer relative to the canvas
* **Brush.rotation:** \
  The current orientation of the brush pointer relative to the canvas
* **Brush.colorRgb:** \
  The current brush color
* **Brush.colorHsv:** \
  The current brush colour converted to HSV
* **Brush.size:** \
  The current brush size
* **Brush.pressure:** \
  The current pressure of the brush pointer (how hard the trigger is being pressed)
* **Brush.type:** \
  The current brush name
* **App.time:** \
  The time in seconds since Open Brush was launched
* **App.currentScale:** \
  The current scale of the canvas
* **Sketch.strokes**\
  A list of strokes in the current sketch

### Script Parameters

Scripts can specify parameters that appear as UI widgets such as sliders. These appear in a popup when you click the "3 dots" button on the right of each row.  For example you might want a script to have sliders to control "speed" or "wigglyness".

You define the widgets for each parameter in your script. Here's an example:

```lua
Parameters = {
    speed={label="Speed", type="float", min=0.01, max=32, default=16},
    radius={label="Radius", type="float", min=0.01, max=5, default=1},
}

function Main()
    angle = App.time * speed
    r = Brush.pressure * radius;
    pos = Vector3:New(Math.Sin(angle) * r, Math:Cos(angle) * r, 0)
    return Transform:New(pos)
end
```

Here we have defined two widgets. Both are floats (rather than integers) and we have defined a minimum, a maximum and a default value. You can set the ltext abel that appears when you hover over each slider.

The name of each widget (here "speed" and "radius") are then available to the script as variables.

### Coordinate Spaces

By default each script type works relative to an origin and has a rotation that makes sense for each of the three types. Pointer and Tool Scripts are relative to the user's brush hand and Symmetry Scripts are relative to the Symmetry Widget.

You can override this. For example, here's a PointerScript that is relative to the canvas. We can then position the pointer so it is always at y=0 (the floor) but still tracks the pointer in the x and z directions:

```lua
Settings = {space="canvas"}

function Main()
    return Transform:New(
        Vector3:New(Brush.position.x, 0, Brush.position.z)
    )
end
```

Note that we have to manually specific pointer.position.x and pointer.position.y. If we were using space="pointer" (the default) then we wouldn't need to as coordinates are automatically relative to pointer.position

Valid spaces are currently "pointer" or "canvas".

