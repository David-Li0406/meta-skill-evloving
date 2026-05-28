# Writing a Pointer Plugin

Pointer Plugins can modify the pointer position and/or rotation every frame. You can get the current position and rotation so you can simply add an offset to those - or you could create an entirely new position or rotation based on any of the other context variables that are available to the script.

Name a Pointer Script with the prefix "PointerScript". For example: _PointerScript.MyPlugin.lua_&#x20;

Assuming your script is valid (i.e. it has no syntax errors) then giving it a valid prefix is all you need for it to appear in the Scripts Panel.

By default a Pointer Script returns a [Transform](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/transform) which represents how the pointer moves relative to it's normal position (which in this case is wherever the user moves their brush hand)

The simplest possible pointer plugin would be something like this:

```lua
function Main()
    return Transform.identity
end
```

This does nothing at all. It returns a transform called "identity" which means "no change at all". There are several other ways to express the same thing:

```lua
-- Explicitly returns zero for position, rotation and scale.
return Transform:New(Vector3.zero, Rotation.zero, 0)

-- If you miss out rotation and/or scale they are assumed to be zero
return Transform:New(Vector3.zero)

-- Vector3.zero is itself shorthand for this:
return Transform:New(Vector3:New(0,0,0))

-- You can create a transform with only a position in a slightly shorter way:
return Transform:Position(0,0,0)
```

There's no difference between these - it's just sometimes more convenient or clearer to write things in different ways.

So - a plugin script that does nothing isn't much fun. Let's change it so it does _something._

```lua
function Main()
    return Transform:New(0,1,0)
end

-- or

function Main()
    return Transform:Vector3.up
end
```

Vector3.up is another shorthand - this time it's shorthand for Vector3:New(0, 1, 0)\
this is a vector with:

**x is 0** (no change in the left/right direction)\
**y is 1** (a shift of 1 in the up direction)\
**z is 0** (meaning "no change in the forward/back direction")

So - this plugin tells Open Brush "the user's pointer should be moved up by 1 unit from whereever they are painting".  If you try it you should see your pointer is about 10cm above wherever you move your brush hand.

So this is not very useful - but we at least we can see we are changing _something_ now.

Let's try something slightly more interesting.

```lua
function Main()
    return Transform:Position(0, App.time, 0)
end
```

App.time is a property of the [App](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/app) class where you can access various properties of Open Brush app itself. As you might have guessed App.time measures time - specifically the number of seconds since you launched Open Brush.

This plugin script will result in your strokes being painted somewhere way higher than the user's brush hand. How high depends on how long since they opened the app! Let's rein things in a bit.

```lua
function Main()
    return Transform:Position(0, Waveform:Triangle(App.time, 1), 0)
end
```

That single return line is getting a bit complicated. Let's split things over two lines to make it easier to read:

```lua
function Main()
    y = Waveform:Triangle(App.time, 1)
    return Transform:Position(0, y, 0)
end
```

If you've done any programming or scripting before, you should recognise what we've done here. "y" is a variable. We chose "y" as the variable name but we could call it anything we want.&#x20;

We've assigned a value to "y" which is the result of calculating a [waveform shaped like a triangle](https://en.wikipedia.org/wiki/Triangle_wave)&#x20;

The output of the Waveform:Triangle method takes two parameters as input time and frequency. It returns a value that varies between -1 and +1. If you've configured your editor as explained in [Getting Started](getting-started.md) then you should have seen a hint pop up when you typed the first open bracket:

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

So we now have a plugin that moves the pointer up and down over time. You can change the second parameter to control the speed.&#x20;

Let's go one step further - allow the user the control the speed without needing to edit the plugin script:

```lua
Parameters = {
    frequency={label="Frequency", type="float", min=0.01, max=10, default=2}
}

function Main()
    y = Waveform:Triangle(App.time, Parameters.frequency)
    return Transform:Position(0, y, 0)
end
```

We've now told Open Brush that this plugin should show a slider in it's [Parameters popup](../#plugin-parameters) which changes the frequency that the pointer moves.
