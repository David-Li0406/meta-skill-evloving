# Writing a Tool Plugin

Tool Plugins can do many different things but they are often used for drawing a lot of brush strokes all in one go. For example you could draw an entire spiral shape whenever the user clicks the trigger. Or you could use the positions: where they first pressed the trigger in and where their brush controller was when they released the trigger - to get the size of a region and create a shape that filled that space.

To create a Tool Plugin name your script with the prefix "ToolScript". For example: _ToolScript.Circle.lua_

Tool Scripts should usually return a list of transforms. If they do then this defines an entire brush stroke that is then created for you.

We previously started by showing the simplest possible plugin script - one that does nothing. Because a tool plugin does nothing by default that would be an empty file! But let's put a bit of scaffolding in so you have a starting point for a plugin that actually does _something._

```lua
function Main()
    if Brush.triggerPressedThisFrame then
        return {}
    end
end
```

It checks to see if the user pressed the trigger and if so it returns an empty list. So this plugin does nothing and it does it every time the user presses the trigger. Great, huh?

Let's make it do something:

```lua
function Main()
    if Brush.triggerPressedThisFrame then
        return {
            Transform:Position(-1, -1, 0),
            Transform:Position(1, -1, 0),
            Transform:Position(1, 1, 0),
            Transform:Position(-1, 1, 0),
            Transform:Position(-1, -1, 0)
        }
    end
end
```

This returns a path with 5 points forming a square. A square has 4 corners so why 5 points? The last point is the same as the first so that the square closes on itself.

If you try this, you'll notice the square isn't very square. This is because Open Brush tries to smooth brush strokes. It expects you to be hand-drawing smooth curvy lines in space - not carefully placing precise geometric paths.

We can fix this by adding extra points:

```lua
function Main()
    if Brush.triggerPressedThisFrame then
        myPath = Path:New({
            Transform:Position(-1, -1, 0),
            Transform:Position(1, -1, 0),
            Transform:Position(1, 1, 0),
            Transform:Position(-1, 1, 0),
            Transform:Position(-1, -1, 0)
        })
        return myPath:SubdivideSegments(5)
    end
end
```

This time we create a `Path` object instead of just using a list of transforms. This allows us to use any of the handy methods that are provided by `Path` - in this case it's the [`SubdivideSegments`](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/path#path-subdividesegments-parts) method. This modifies the path by inserting as many new points as we ask for in each path segment. In this case we ask for 5 new points so the square that previously had 5 points (and thus 4 segments) will now have 4 x 5 = 20 points. (I'll let you work out how many segments!)

Next let's draw a circle:

```lua
function Main()
    if Brush.triggerReleasedThisFrame then
        points = Path:New()
        for angle = 0, 360, 10 do
            position2d = Vector2:PointOnCircle(angle)
            points:Insert(Transform:Position(position2d:OnZ()))
        end
        return points
    end
end
```

There's a few new things here:

1. a loop that begins `for...do`, this is a standard lua construct and works similarly to loops in other languages.
2. we first calculate a 2d vector using `Vector2:PointOnCircle(angle)`. A Vector2 is very similar to the `Vector3` that we used previously for specifying a position. The difference is that it only has two coordinates: x and y.
3. We convert the `Vector2` into a `Vector3` on the next line by using the `OnZ()` method. This creates a `Vector3` where x and y are taken from the `Vector2` the z value is set to 0. Therefore it lies on the plane perpendicular to the z axis (it could probably have been named on `OnXY()` but this sounded better to me)
4. We are using `triggerReleasedThisFrame` instead of `triggerPressedThisFrame`. In this example we wait for the user to release the trigger before we do anything. This means we know both the start point (where they pressed the trigger) and the end point (where they released it). These two points are used to determine how the path we return is scaled and rotated. You don't need to do this scaling and rotating yourself - it happens automatically if you return a value representing a brush stroke.&#x20;
