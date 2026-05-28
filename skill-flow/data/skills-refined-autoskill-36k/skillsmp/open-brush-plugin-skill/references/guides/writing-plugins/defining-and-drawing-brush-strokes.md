# Defining and Drawing Brush Strokes



When you paint freehand in Open Brush, the application is constantly recording your hand's position and orientation. Therefore internally a stroke is defined as a list of transforms. Scale isn't used but the position and rotation are key in defining the shape of the resulting stroke.

There are several situations when you might need to define a stroke when writing a plugin:

1. The most common use-case is with Tool Plugins. The value you return from the Main() function in a Tool Plugin is drawn as a brush stroke
2. You can paths explicitly using Path:Draw(), PathList:Draw() or the draw methods provided by classes such as SVG

In both these cases you must define the path as a list of transforms. Both the position and rotation are used to define the shape of the stroke. It matches what happens when you draw a stroke by hand - at each point in time you control both the position of the brush and it's orientation. Orientation doesn't matter for all brushes (a tube brush looks much the same whatever the rotation of the brush controller at each point is) but other brushes such as flat stroke brushes do make use of the rotation values you provide.

In the simple case where you are returning a value from the Main function of a Tool Plugin, you can return a normal lua array (or "table" as they are also called) containing two or more Transform instances:

```lua
origin = Transform:New(Vector3:New(0, 0, 0), Rotation.forwards)
return {origin, origin:TranslateBy(2, 2, 0)}
```

It's simple to use a lua list like this: {} but there is also a class specifically for definition a list of transforms and it's called [`Path`](https://icosa.gitbook.io/open-brush-plugin-scripting-docs/readme/path). The advantage of using this class is that also has many useful methods for modifying paths.

```lua
origin = Transform:New(Vector3:New(0, 0, 0), Rotation.forwards)
path = Path:New({origin, origin:TranslateBy(2, 2, 0)})
path:RotateBy(0, 45, 0)
return path
```

(The various `Draw()` methods insist that you use a Path object - so you can't use a simple lua array when you use those.)

Open Brush usually assumes a brush stroke is drawn by hand. Some simplification is done depending on your settings but a stroke is still usually made up of a lot of points forming a smooth curve as the app samples your controller position and orientation many times a second.

When you draw paths via code in a plugin script, you often send only the exact points you want. For example if you were drawing a square then you'd simply define the four points that make up the corners of the square (although you usually repeat the first point at the end if you want a closed shape)

The problem is that by default Open Brush tries to smooth the path you give it so your nice precise square becomes a rounded squiggle. The end result actually varies depending on the brush you use - different brushes use different rules for how to smooth the input points.

But generally speaking - if you want to draw a precise geometric shape then you need to add extra points - and the Path object has some useful methods to do this.
