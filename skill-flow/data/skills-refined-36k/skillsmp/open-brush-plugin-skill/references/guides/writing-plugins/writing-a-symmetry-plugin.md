# Writing a Symmetry Plugin

Symmetry Plugins are similar to Pointer plugins with a few differences:

1. They can return a list of transforms that represent multiple pointers.
2. They can modify the color, size and brush type for each of the strokes separately.
3. They have access to the Symmetry Widget which can be used as a point of origin for each pointer. If you've used the Mirror or [MultiMirror](../../../alternate-and-experimental-builds/old-or-completed-feature-builds/multi-mirror.md) features in Open Brush then the Symmetry Widget is like the Mirror Widget that controls the reflection plane and center for those mirrors.

Bear in mind - the number of pointers you generate cannot change once a brush stroke has begun, but can change between each brush stroke.

Make sure you name your symmetry plugin scripts with the prefix "SymmetryScript". For example **SymmetryScript.MyMirror.lua**

Let's start with the simplest possible Symmetry Plugin:

```lua
function Main()
    return {Transform.identity}
end
```

In lua you can define a list of items by enclosing them in curly braces. This example is almost identical to the simplest possible Pointer plugin except that we wrap the transform in curly braces.&#x20;

You might expect that it behaves the same - i.e. nothing changes and you paint as normal. However if you try it, you'll find that's not the case. In fact - you can't paint at all - your pointer remains stubbornly stuck to the center of the Symmetry Widget.

Why is this? By default Pointer Plugins and Symmetry Plugins use a different [coordinate space](./#coordinate-spaces). This is how we describe how where the origin is and how translations and rotations are interpreted. Pointer plugins default to using the current brush controller position as the origin so all coordinates are relative to that. Symmetry plugins on the other hand default to using the Symmetry Widget as the origin. So returning a transform that does nothing means that the pointer is stuck at the widget's center.

You can change the default coordinate space by adding a value to the script settings:

```lua
Settings = {space="pointer"}

function Main()
    return {Transform.identity}
end
```

This plugin will now behave the same as the "do nothing" pointer plugin example. Using `space="pointer"` in a Symmetry Plugin is useful if you want to ignore the widget and have all the pointers move relative to the brush controller.

Let's do something more interesting in our Symmetry Plugin:

```lua
function Main()
    origin = Transform.identity
    brushOffset = Transform:New(Symmetry.brushOffset)
    return {
        Transform:Lerp(origin, brushOffset, 0.2),
        Transform:Lerp(origin, brushOffset, 0.4),
        Transform:Lerp(origin, brushOffset, 0.6),
        Transform:Lerp(origin, brushOffset, 0.8)
    }
end
```

Here we are returning a list of 4 transforms so we will have four separate pointers all creating a stroke at the same time.

`Transform.Lerp` is a method that takes two transforms as input and blends them by an amount given by the third number. So `Transform.Lerp(a, b, 0.5)` will return a transform that is exactly half-way between a and b. It's position will be at the midpoint of a and b and will have a rotation and scale exactly halfway between those of a and b.

What are we passing into Transform.Lerp? `origin` is set to `Transform.identity` which is our do-nothing transform. As mentioned before - in this case it will be the center point of the symmetry widget.

`brushOffset` is a [Transform](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/transform) with it's position set to the value of`Symmetry.brushOffset`. This is a [Vector3](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/vector3) which represents the position of the user's brush controller relative to the symmetry widget. It is a special value that only makes sense in the context of a Symmetry plugin and you won't use it in other types of plugin script.

Usually the value of the user's brush controller is given by`Brush.position`. This is because by default, symmetry scripts use coordinates centered on the symmetry widget and you'd have to do a some complicated calculations to get from there to the current brush position. If you use `symmetry.brushOffset` this is done for you.

So this script will create 4 pointers that are spaced evenly between the symmetry widget and the user's brush controller as they paint. Give it a try!

Finally - let's look at one last symmetry script.

```lua
function Main()
    copies = 10
    pointers = Path:New()
    angleStep = 360 / copies 
    for i = 1, copies do
        angle = i * angleStep
        pointer = Transform:New(Symmetry.brushOffset, Rotation:New(0, angle, 0))
        pointers:Insert(pointer)
    end
    return pointers
end
```

Some things to note here:

1. Instead of creating a list of transforms using curly braces we are creating a `Path`object and then using `Insert` to add pointers to it one at a time. Path is just a class that stores a list of transforms. It has some useful methods for transforming and modifying itself so is often more useful than just a simple list.
2. We are using a loop: **`for i = 1, copies do`** \
   You should have come across similar constructs in other scripting languages. Any lua tutorial will explain some small differences with lua loops but in general they should behave as you would expect.
3. `angleStep`is always 36 in this case but if you wanted to,`copies` could be a slider that the user sets so we calculate how many degrees to add to the angle for each copy of the pointer.
4. You don't have to calculate the position of each pointer around the circle. This is done automatically for you. The final position is calculated based on the symmetry widget's transform and the rotation value you return for each pointer. This saves you from having to do some pretty gnarly maths yourself in symmetry plugins.
