# Writing a Background Plugin

Background Plugins run all the time when activated. They are useful for animating layers or continually generating new shapes. You can still check for user actions such as pressing the trigger and change the action accordingly. They are very versatile but because they run continuously in they background, they can affect performance (especially if you run several at the same time).

Always use one of the other script types in preference if it is more suitable.&#x20;

Unlike other plugin types, Background Plugins don't expect you to return a value and they don't do anything with any values you do return.

In contrast other plugin types use return values as follows:

1. Pointer Plugins use the returned value to change the pointer position, rotation or scale.
2. Symmetry Plugins use the returned values to create multiple new pointers.
3. Tool Plugins can use the returned value as the path of a new brush stroke which is drawn immediately.

You can of course draw in a Background Plugin but it's left to you to do so explicitly:

```lua
function Main()
    if Brush.triggerPressedThisFrame then
        myPath = Path:New()
        position = getRandomPosition()
        myPath:Insert(Transform:New(position))
        myPath:Insert(Transform:New(position))
        myPath:Draw()
    end
end

function getRandomPosition()
    return Brush.position + Random.insideUnitSphere
end
```

There are some potentially new details to be aware of here:

1. We are defining our own function to generate a random position around the current brush position
2. We are using the `Random` class to generate a point that is never more than a certain distance away from the origin. We then add that to the current brush position
3. We are manually drawing the path with `myPath:Draw()`
