# Ui Reference

## Contents
- [2D paths](#2d-paths)
- [3D drag detectors](#3d-drag-detectors)
- [UI 9-slice design](#ui-9-slice-design)
- [UI animation/tweens](#ui-animation-tweens)
- [UI appearance modifiers](#ui-appearance-modifiers)
- [Text & image buttons](#text-image-buttons)
- [Frames](#frames)
- [Grid and table layouts](#grid-and-table-layouts)
- [In-experience UI containers](#in-experience-ui-containers)
- [User interface](#user-interface)
- [Text & image labels](#text-image-labels)
- [List and flex layouts](#list-and-flex-layouts)
- [On-screen UI containers](#on-screen-ui-containers)
- [Page layouts](#page-layouts)
- [Position and size UI objects](#position-and-size-ui-objects)
- [Proximity prompts](#proximity-prompts)
- [Rich text markup](#rich-text-markup)
- [Scrolling frames](#scrolling-frames)
- [Size modifiers and constraints](#size-modifiers-and-constraints)
- [UI styling compatibility](#ui-styling-compatibility)
- [CSS Comparisons](#css-comparisons)
- [Style Editor](#style-editor)
- [UI styling](#ui-styling)
- [Text filtering](#text-filtering)
- [Text input fields](#text-input-fields)
- [UI drag detectors](#ui-drag-detectors)
- [Video frames](#video-frames)
- [Viewport frames](#viewport-frames)

---

## 2D paths

The `Class.Path2D` instance, along with its API methods and properties, lets you implement 2D splines and 2D curved lines, useful for UI effects like path‑based animations and graph editors.

<video src="../assets/ui/2D-paths/Path2D.mp4" controls width="90%" alt="Video showing a UI object animating back and forth across a complex path."></video>

## Create a 2D path

To add a `Class.Path2D` to the screen or an in-experience object:

1. In the [Explorer](../studio/explorer.md) window, insert a `Class.Path2D` instance under a visible `Class.ScreenGui` or `Class.SurfaceGui` (it does not need to be a direct child).

   <img src="../assets/studio/explorer/StarterGui-ScreenGui-Path2D.png" width="320" alt="Path2D instance parented to a ScreenGui in the Explorer hierarchy." />

2. Select the new `Class.Path2D` to reveal the in-viewport tooling widget. By default, the **Add&nbsp;Point** tool is selected.

   <img src="../assets/ui/2D-paths/Widget-Add-Point.png" width="600" alt="Add Point tool indicated in the 2D path editor widget." />

3. Begin clicking on the screen to add a series of **control points** to form a path. The initial path will likely be imprecise but you can [fine‑tune](#move-points) the position of any control point later.

   <img src="../assets/ui/2D-paths/Path-Example-Create-Basic.png" width="600" alt="Diagram illustrating an example path created using the Add Point tool to connect a series of points." />

   <Alert severity="info">
   If you drag the mouse after clicking, [tangents](#control-point-tangents) will be created on that point. Tangents can also be procedurally [added](#add-tangents) to any control point.
	 </Alert>

4. When finished, click the widget's **Done** button or press <kbd>Enter</kbd>.

## Modify control points

With a `Class.Path2D` selected in the [Explorer](../studio/explorer.md) hierarchy, you can modify its individual control points as well as their [tangents](#control-point-tangents).

### Move points

To move an individual cont

[Content truncated - see full docs]

---

## 3D drag detectors

The `Class.DragDetector` instance facilitates and encourages interaction with 3D objects in an experience, such as opening doors and drawers, sliding a part around, grabbing and tossing a bowling ball, pulling back and firing a slingshot, and much more. Key features include:

- Place a `Class.DragDetector` under any `Class.BasePart` or `Class.Model` to [make it draggable](#make-objects-draggable) via all inputs (mouse, touch, gamepad, and VR), all without a single line of code.

- Choose from several [drag styles](#drag-style), define how the object [responds to motion](#response-to-motion), and optionally apply [axis or movement limits](#axis--movement-limits).

- Scripts can [respond to manipulation of dragged objects](#script-responses-to-clicking-and-dragging) to drive UI or make logical decisions, such as adjusting the light level in a room based on a sliding wall switch dimmer.

- Players can manipulate anchored parts or models and they'll stay exactly where you put them upon release.

- `Class.DragDetector|DragDetectors` work in Studio as long as you're **not** using the **Select**, **Move**, **Scale**, or **Rotate** tools, making it easier to test and adjust draggable objects while editing.

<video src="../assets/ui/3D-drag-detectors/Showcase.mp4" controls width="100%" alt="Drag detectors used in a variety of implementations in the 3D world"></video>

## Make objects draggable

To make any part or model draggable, simply add a `Class.DragDetector` as a direct descendant.

1. In the [Explorer](../studio/explorer.md) window, hover over the `Class.Part`, `Class.MeshPart`, or `Class.Model` and click the &CirclePlus; button. A contextual menu displays.
1. From the menu, insert a **DragDetector**.

   <img src="../assets/studio/explorer/Model-DragDetector.png" width="320" />

1. By default, the object will now be draggable in the ground plane, but you can customize its `Class.DragDetector.DragStyle|DragStyle`, define how it [responds to motion](#response-to-motion

[Content truncated - see full docs]

---

## UI 9-slice design

When creating UI with custom borders and corners, you'll often need to render elements at different aspect ratios and visually surround [localized text](../production/localization/index.md) or other contents of unknown dimensions.
This lets you create UI elements of varying sizes without distorting the borders or corners.

<GridContainer numColumns="2">
  <figure>
    <img src="../assets/ui/9-slice/9-Slice-Comparison-Without.png" />
    <figcaption>Without 9-Slice</figcaption>
  </figure>
  <figure>
    <img src="../assets/ui/9-slice/9-Slice-Comparison-With.png" />
    <figcaption>With 9-Slice</figcaption>
  </figure>
</GridContainer>

Under the **9-slice** approach, one image (a single Roblox image asset) is
internally divided into nine sub-images, each with different scaling rules.
<img src="../assets/ui/9-slice/9-Slice-Concept-Diagram.png" width="412" />

<table>
    <thead>
        <tr>
            <th>Sub-image</th>
            <th>Scaling</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>1</strong> <strong>3</strong> <strong>7</strong> <strong>9</strong> (corners)</td>
            <td>none</td>
        </tr>
        <tr>
            <td><strong>2</strong> <strong>8</strong> (top/bottom edges)</td>
            <td>horizontal</td>
        </tr>
        <tr>
            <td><strong>4</strong> <strong>6</strong> (left/right edges)</td>
            <td>vertical</td>
        </tr>
        <tr>
            <td><strong>5</strong> (center)</td>
            <td>horizontal + vertical</td>
        </tr>
    </tbody>
</table>

## Studio editor

Slice configuration is possible by directly setting the `Enum.ScaleType` and slice properties on an image label or button, but Studio's built-in **9-Slice Editor** is more intuitive.

### Opening the editor

To open the visual **9-Slice Editor** in Studio:

1. Select an `Class.ImageLabel` or `Class.ImageButton` with a valid asset ID entered into its **Image** field.

  <img src="../assets/ui/9-slice/9-

[Content truncated - see full docs]

---

## UI animation/tweens

In animation, **tweening** is the process of generating intermediate frames between two key points in a sequence. When designing a user interface, you can use tweening to transition a `Class.GuiObject` smoothly from one state to another, such as:

- Smoothly increasing the size of a button when a user selects it.
- Sliding UI menus in and out from the screen edges.
- Gradually animating a health bar between two widths when a user receives a health boost.

## Single-property tweens

### Position

To tween the **position** of a `Class.GuiObject`:

1. Set the `Class.GuiObject.AnchorPoint|AnchorPoint` for the object.
1. Determine `Datatype.UDim2` coordinates for the object's target position, using the **scale** parameters of `Datatype.UDim2` instead of exact pixel values so that the object tweens to the exact center of the screen.
1. Pass a `Datatype.TweenInfo` and the target position to `Class.TweenService:Create()`.
1. Play the tween with `Class.Tween:Play()`.

The following code snippet moves an `Class.ImageLabel` within a `Class.ScreenGui` to the exact center of the screen:

```lua title="UI Tween - Position" highlight="8,10,12,13,15"
local TweenService = game:GetService("TweenService")
local Players = game:GetService("Players")

local PlayerGui = Players.LocalPlayer:WaitForChild("PlayerGui")
local ScreenGui = PlayerGui:WaitForChild("ScreenGui")
local object = ScreenGui:WaitForChild("ImageLabel")

object.AnchorPoint = Vector2.new(0.5, 0.5)

local targetPosition = UDim2.new(0.5, 0, 0.5, 0)

local tweenInfo = TweenInfo.new(2)
local tween = TweenService:Create(object, tweenInfo, {Position = targetPosition})

tween:Play()
```

### Size

To tween the **size** of a `Class.GuiObject`:

1. Determine `Datatype.UDim2` coordinates for the object's target size, using the **scale** parameters of `Datatype.UDim2` instead of exact pixel values so that the object tweens to a relative percentage of the screen size.
1. Attach a `Class.UIAspectRatioConstraint` to the object to maintai

[Content truncated - see full docs]

---

## UI appearance modifiers

import BetaAlert from '../includes/beta-features/beta-alert.md'

By utilizing **appearance modifiers**, you can further customize the appearance of your `Class.GuiObject|GuiObjects`.

- Apply a [gradient](#gradient) to the background of an object.
- Apply a [stroke](#stroke) to text or a border.
- Set [rounded corners](#corners) for an object.
- Increase [padding](#padding) between the borders of an object.

## Gradient

The `Class.UIGradient` object applies a color and transparency gradient to its parent `Class.GuiObject`.

<Grid container spacing={3}>
  <Grid item>
		<img src="../assets/ui/ui-objects/UIGradient-Example.png" width="480" />
	</Grid>
	<Grid item>
		<img src="../assets/studio/explorer/UIGradient.png" width="320" />
	</Grid>
</Grid>

You can configure the gradient by:

- Setting its [colors](#color-sequence) through a `Datatype.ColorSequence` in the gradient's `Class.UIGradient.Color|Color` property.
- Setting its [transparency](#transparency) through a `Datatype.NumberSequence` in the gradient's `Class.UIGradient.Transparency|Transparency` property.
- Choosing the gradient's starting point (inside or outside the parent's bounds) through the `Class.UIGradient.Offset|Offset` property.
- Choosing the gradient's angle through the `Class.UIGradient.Rotation|Rotation` property.

### Color sequence

To set a gradient's color sequence:

1. In the [Explorer](../studio/explorer.md) window, select the `Class.UIGradient`.
1. In the [Properties](../studio/properties.md) window, click inside the `Class.UIGradient.Color|Color` property field, then click the **&ctdot;** button to the right of the input box. A color sequence pop-up displays.

   <img src="../assets/studio/properties/UIGradient-Open-ColorSequence-Window.png"
   width="320" />

   Each triangle on the bottom axis of the color sequence is a **keypoint** that determines the color value at that point.

   <img src="../assets/studio/general/ColorSequence-White.png" width="640" alt="Color sequence popup from

[Content truncated - see full docs]

---

## Text & image buttons

**Buttons** are `Class.GuiObject|GuiObjects` that allow users to perform an action. You can customize buttons to provide context and feedback, such as changing the visual appearance or [scripting](#script-buttons) audible feedback when a user clicks a button.

There are two types of buttons which you can place [on‑screen](../ui/on-screen-containers.md) or [in‑experience](../ui/in-experience-containers.md):

- A `Class.TextButton` is a rectangle with text that triggers the `Class.GuiButton.Activated|Activated` event on click/tap.

- An `Class.ImageButton` is a rectangle with an image that triggers the `Class.GuiButton.Activated|Activated` event on click/tap. It features additional states for swapping the image on user hover or press.

## Create buttons on the screen

Buttons on a screen are useful to quickly guide users to various menus or pages.

To add a button to the screen:

1. In the **Explorer** window, select **StarterGui** and add a **ScreenGui**.

   1. Hover over **StarterGui** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **ScreenGui**.

2. Select the new **ScreenGui** and add a button.

   1. Hover over **ScreenGui** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert either a **TextButton** or **ImageButton**.

   <img src="../assets/ui/button-text-input/ImageButton-Screen-New.jpg" width="800" />

## Create buttons on part faces

Buttons on a part are useful for allowing users to interact with parts. For
example, you can let users step on a button to complete an action.

To add a button to the face of a part:

1. In the **Explorer** window, select the **part** and add a **SurfaceGui**.

   1. Hover over the **part** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **SurfaceGui**.

2. Select the new **SurfaceGui** and add any type of button or input.

   1. Hover over **SurfaceGui** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert either a *

[Content truncated - see full docs]

---

## Frames

Basic `Class.Frame|Frames` act as containers for other `Class.GuiObject|GuiObjects` such as [labels](../ui/labels.md) and [buttons](../ui/buttons.md). You can apply frames to display on a user's [screen](../ui/on-screen-containers.md) or on a [surface](../ui/in-experience-containers.md) within the experience.

<img src="../assets/ui/ui-objects/Frame-Example.jpg" width="840" alt="Example Frame on the screen containing a TextLabel, TextBox, and ImageButton." />

Frames are ideal containers for responsive layouts such as [list and flex layouts](../ui/list-flex-layouts.md), allowing you to change the size of the frame and dynamically adjust how layout items fit within it. `Class.Frame|Frames` are also core `Class.GuiObject|GuiObjects`, so you can customize properties such as `Class.GuiObject.BackgroundColor3|BackgroundColor3`, `Class.GuiObject.Transparency|Transparency`, apply a [background gradient](../ui/appearance-modifiers.md#gradient) or [border](../ui/appearance-modifiers.md#stroke), and more.

Aside from their common use as containers, you can also use `Class.Frame|Frames` for UI design. For example, as a visual separator between other UI elements, you can scale a frame to be thin and long until it becomes a line.

<Alert severity="success">
See also [scrolling frames](../ui/scrolling-frames.md), [viewport frames](../ui/viewport-frames.md), and [video frames](../ui/video-frames.md) as specialty frame types with unique built‑in capabilities.
</Alert>

## Clipping

By default, `Class.Frame` containers **clip** their content (child `Class.GuiObject|GuiObjects`) through the `Class.Frame.ClipsDescendants|ClipsDescendants` boolean. If you want children to appear outside of a frame's bounds, simply set `Class.Frame.ClipsDescendants|ClipsDescendants` to `false`.

Importantly, note that `Class.Frame.ClipsDescendants|ClipsDescendants` does **not** apply if the frame or any of its ancestors have a non‑zero `Class.Frame.Rotation|Rotation`; in such cases, descendants will ren

[Content truncated - see full docs]

---

## Grid and table layouts

In comparison to `Class.UIListLayout`, `Class.UIGridLayout` and `Class.UITableLayout` allow for more structured and organized layouts. These are most appropriate for interfaces like a shop inventory where each item can be presented in a grid of equally‑sized tiles, or items can be sorted into related rows/columns.

<GridContainer numColumns="2">
	<figure>
  	<img src="../assets/ui/ui-objects/UIGridLayout-Example.jpg" />
		<figcaption>`Class.UIGridLayout`</figcaption>
	</figure>
	<figure>
  	<img src="../assets/ui/ui-objects/UITableLayout-Example.jpg" />
		<figcaption>`Class.UITableLayout`</figcaption>
	</figure>
</GridContainer>

## Grid layout

`Class.UIGridLayout` positions sibling `Class.GuiObject|GuiObjects` in a grid of uniform cells of the same size within their parent container. Cells are added by row or column based on the layout's `Class.UIGridLayout.FillDirection|FillDirection` until the next cell doesn't fit, then a new row or column begins. For further control, you can use the `Class.UIGridLayout.FillDirectionMaxCells|FillDirectionMaxCells` property to set the maximum number of cells per row or column.

<Grid container spacing={2}>
  <Grid item>
		<img src="../assets/ui/ui-objects/UIGridLayout-Example.jpg" width="500" />
	</Grid>
	<Grid item>
		<img src="../assets/studio/explorer/UIGridLayout.png" width="320" />
	</Grid>
</Grid>

By default, `Class.UIGridLayout` positions sibling `Class.GuiObject|GuiObjects` in order of their `Class.GuiObject.LayoutOrder|LayoutOrder` where lower values go before higher values, and equal values sort depending on the order in which you added them. If you change the layout's `Class.UIGridStyleLayout.SortOrder|SortOrder` to `Enum.SortOrder.Name`, siblings sort in alphabetical order.

<Alert severity="warning">
Once you insert a `Class.UIGridLayout`, it either overrides or influences the `Class.GuiObject.Position|Position` and/or `Class.GuiObject.Size|Size` of all sibling UI objects, so changes to those properties within the 

[Content truncated - see full docs]

---

## In-experience UI containers

In-experience UI containers hold `Class.GuiObject|GuiObjects` that you want to display within your experience's 3D world.

- A `Class.SurfaceGui` allows for the rendering of UI objects onto a part's surface in the 3D world while also allowing for basic user interaction to occur.
- A `Class.BillboardGui` is a container for UI objects to appear in the 3D space but always face the camera.

<video src="../assets/ui/in-experience/Showcase.mp4" controls width="100%"></video>

## Surface UI

Similar to `Class.Decal|Decals` and `Class.Texture|Textures`, UI objects such as `Class.TextLabel|TextLabels` and `Class.ImageLabel|ImageLabels` parented to a `Class.SurfaceGui` face the same direction as the surface they're on, editable through the `Class.SurfaceGui.Face` property.

<img src="../assets/ui/in-experience/SurfaceGui-Diagram.jpg" width="800" alt="SurfaceGui on a 3D part in the place with an ImageLabel child to depict a screen console." />

To apply a `Class.SurfaceGui` to an in-experience `Class.BasePart`, simply parent it to that part and set the `Class.SurfaceGui.Face` property. Child UI objects then appear on that face of the parent part.

<Grid container spacing={2} alignItems="top">
	<Grid item>
		<img src="../assets/studio/explorer/Part-SurfaceGui-ImageLabel.png" width="320" />
	</Grid>
	<Grid item>
		<img src="../assets/studio/properties/SurfaceGui-Face-Top.png" width="320" />
	</Grid>
</Grid>

Alternatively, you can place the `Class.SurfaceGui` inside a container like `Class.StarterGui` and then set its `Class.SurfaceGui.Adornee|Adornee` property to any `Class.BasePart`, as well as the target `Class.SurfaceGui.Face|Face`. Setting `Class.SurfaceGui.Adornee|Adornee` overrides direct parent association, allowing for more flexibility in placement since it can be set from a script during runtime.

<Grid container spacing={2} alignItems="top">
	<Grid item>
		<img src="../assets/studio/explorer/StarterGui-SurfaceGui.png" width="320" />
	</Grid>
	<Grid item>
		<img src=".

[Content truncated - see full docs]

---

## User interface

You can quickly create high-quality graphical user interfaces with minimal scripting requirements using built-in [UI objects](#ui-objects). Depending on where you create it, UI renders either [on-screen](#on-screen-ui) or [within an experience's 3D world](#in-experience-ui).

## On-screen UI

[On-screen containers](../ui/on-screen-containers.md) hold UI objects that you want to display on a player's screen, including [frames](../ui/frames.md), [labels](../ui/labels.md), [buttons](../ui/buttons.md), and more. All on-screen UI objects and code are stored and changed on the client.

<figure>
<img src="../assets/ui/ui-objects/ScreenGui-Example.jpg" width="840" alt="Example ScreenGui with various GuiObject children, including a Frame, TextLabel, TextBox, and ImageButton." />
</figure>

## In-experience UI

[In-experience containers](../ui/in-experience-containers.md) such as `Class.SurfaceGui|SurfaceGuis` and `Class.BillboardGui|BillboardGuis` hold UI objects that you want to display within your experience's 3D world.

<video src="../assets/ui/in-experience/Showcase.mp4" controls width="100%"></video>

## UI objects

Most UI elements are `Class.GuiObject|GuiObjects`, 2D graphical user interface objects that you can parent to containers. The four most common are [frames](../ui/frames.md), [labels](../ui/labels.md), [buttons](../ui/buttons.md), and [text input](../ui/text-input.md) objects.

<img src="../assets/ui/ui-objects/ScreenGui-Example.jpg" width="840" />

<table>
<thead>
  <tr>
    <th>Object</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>[Frame](../ui/frames.md)</td>
    <td>`Class.Frame|Frames` act as containers for other UI objects. When you manipulate frames, you also manipulate the objects they contain.</td>
  </tr>
	<tr>
    <td>[Label](../ui/labels.md)</td>
    <td>`Class.TextLabel` and `Class.ImageLabel` objects allow you to display customizable text and images.</td>
  </tr>
	<tr>
    <td>[Button](../ui/buttons.md)</td>
    <td>`Class

[Content truncated - see full docs]

---

## Text & image labels

import TextFiltering from '../includes/text-filtering/text-filtering.md'

**Labels** are `Class.GuiObject|GuiObjects` that let you display customizable text and images [on‑screen](../ui/on-screen-containers.md) or [in‑experience](../ui/in-experience-containers.md). There are two types of labels:

- A `Class.TextLabel` is a rectangle with text that you can style through customizable properties. This is the primary way to display text in an experience.

- An `Class.ImageLabel` is a rectangle with an image [asset](../projects/assets/index.md) that you can style through customizable properties. Alongside [textures and decals](../parts/textures-decals.md), this lets you display images in an experience.

## Create labels on the screen

Labels on a screen are useful for things like displaying images of characters
with dialog.

To add a label to a screen:

1. In the **Explorer** window, select **StarterGui** and add a **ScreenGui**.

   1. Hover over StarterGui and click the &CirclePlus; button. A contextual menu displays.

   1. From the menu, insert a **ScreenGui**.

2. Select the new **ScreenGui** and add a label.

   1. Hover over **ScreenGui** and click the &CirclePlus; button. A contextual menu displays.

   1. From the menu, insert a **TextLabel** or **ImageLabel**.

   <img src="../assets/ui/button-text-input/ImageButton-Screen-New.jpg" width="80%" />

## Create labels on part faces

Labels on a part are useful for things like creating billboards, posters, and
wallpaper.

To add a label to the face of a part:

1. In the **Explorer** window, insert a **SurfaceGui** onto the part.

   1. Hover over the part instance and click the &CirclePlus; button. A contextual menu displays.

   1. From the menu, insert a **SurfaceGui**.

2. Select the new **SurfaceGui** and add a label.

   1. Hover over the **SurfaceGui** and click the &CirclePlus; button. A contextual menu displays.

   1. From the menu, insert a **TextLabel** or **ImageLabel**.

   <img src="../assets/ui/button

[Content truncated - see full docs]

---

## List and flex layouts

The `Class.UIListLayout` positions sibling `Class.GuiObject|GuiObjects` into horizontal rows or vertical columns within their parent container. Whenever you add or remove a sibling object, the layout adjusts accordingly.

<img src="../assets/ui/ui-objects/UIListLayout-Example.png" width="840" />

<Alert severity="warning">
Once you insert a `Class.UIListLayout`, it either overrides or influences the `Class.GuiObject.Position|Position`, `Class.GuiObject.Rotation|Rotation`, and/or `Class.GuiObject.Size|Size` of all sibling UI objects, so changes to those properties within the [Properties](../studio/properties.md) window or within a script will not have the normal effect.
</Alert>

## Fill direction

The `Class.UIListLayout.FillDirection|FillDirection` property determines the direction in which the list layout's siblings will render.

<img src="../assets/engine-api/classes/UIListLayout/FillDirection.png" width="720" alt="UIListLayouts illustrating FillDirection of either horizontal or vertical." />

Ordering is determined by the layout's `Class.UIListLayout.SortOrder|SortOrder` property which can be either **ascending numeric**, based on each item's `Class.GuiObject.LayoutOrder|LayoutOrder` integer value, or **alphanumeric** based on the item's `Class.Instance.Name|Name`.

<img src="../assets/engine-api/classes/UIListLayout/SortOrder.png" width="720" alt="List layout examples illustrating numerical LayoutOrder sorting or alphanumerical Name sorting." />

<Alert severity="info">
To reverse elements, such as right-to-left ordering in a horizontal list, you'll need to reverse the sorting. For example, if four items are ordered by `Class.GuiObject.LayoutOrder|LayoutOrder` of `0`, `1`, `2`, `3` respectively, negate each value to form an order of `0`, `-1`, `-2`, `-3`.
</Alert>

## Alignment

The `Class.UIListLayout.HorizontalAlignment|HorizontalAlignment` and `Class.UIListLayout.VerticalAlignment|VerticalAlignment` properties determine the respective **X** and **Y** alignme

[Content truncated - see full docs]

---

## On-screen UI containers

import DefaultUI from '../includes/ui/default-ui.md'
import ScreenInsets from '../includes/ui/screen-insets.md'

The `Class.ScreenGui` container holds `Class.GuiObject|GuiObjects` to display on a player's screen, including [frames](../ui/frames.md), [labels](../ui/labels.md), [buttons](../ui/buttons.md), and more. All on‑screen UI objects and code are stored and changed on the client.

<figure>
<img src="../assets/ui/ui-objects/ScreenGui-Example.jpg" width="840" alt="Example ScreenGui with various GuiObject children, including a Frame, TextLabel, TextBox, and ImageButton." />
<Alert severity="info">
For UI containers that hold `Class.GuiObject|GuiObjects` that you want to display **within** the 3D world, such as on the face of a part, see [In-Experience UI Containers](../ui/in-experience-containers.md).
</Alert>
</figure>

To display a `Class.ScreenGui` and its child `Class.GuiObject|GuiObjects` to every player who joins the experience, place it inside the `Class.StarterGui` container. When a player joins an experience and their character first spawns, the `Class.ScreenGui` and its contents clone into the `Class.PlayerGui` container for that player, located within the `Class.Players` container.

<img src="../assets/ui/ui-objects/StarterGui-To-PlayerGui.png" width="840" alt="Diagram of how a ScreenGui clones from StarterGui to a player's PlayerGui" />

<Alert severity="success">
By default, `Class.GuiObject|GuiObjects` inside a `Class.ScreenGui` within `Class.StarterGui` appear as an overlay of the [3D&nbsp;viewport](../studio/ui-overview.md#3d-viewport), simulating their appearance and position in a running experience. To hide all such screen overlays, toggle off **GUI&nbsp;overlay** from the [Visualization&nbsp;Options](../studio/ui-overview.md#visualization-options) widget in the upper‑right corner of the 3D viewport.
</Alert>

<Alert severity="info">
If `Class.Players.CharacterAutoLoads` is disabled, the contents of `Class.StarterGui` will not be cloned until `Cl

[Content truncated - see full docs]

---

## Page layouts

When you parent a `Class.UIPageLayout` to a UI container, every sibling `Class.GuiObject` becomes a unique page that you can transition to through scripting. This layout is useful when you want to create user interfaces such as tabbed modals, tutorials, or character customization screens.

<img src="../assets/studio/explorer/UIPageLayout.png" width="320" />

After you create multiple pages within the `Class.UIPageLayout`, you need to use scripting to transition from page to page. For example, the following code, pasted into a client‑side sibling `Class.Script` of the layout, transitions forward and then backward between the pages every two seconds.

```lua
local frame = script.Parent

local pageLayout = frame:FindFirstChildWhichIsA("UIPageLayout")

task.wait(2)
pageLayout:Next()

task.wait(2)
pageLayout:Next()

task.wait(2)
pageLayout:Previous()

task.wait(2)
pageLayout:Previous()
```

If you want to view pages while editing in Studio, you can use the [Command Bar](../studio/ui-overview.md#command-bar) to navigate from one page to another, letting you review where you need to make changes without having to play your experience each time.

1. In the [Explorer](../studio/explorer.md) window hierarchy, select the `Class.UIPageLayout` object.

   <img src="../assets/studio/explorer/UIPageLayout.png" width="320" />

2. Open the [Command Bar](../studio/ui-overview.md#command-bar).
3. Input any of the following commands and press <kbd>Enter</kbd>.

   <table>
	<thead>
     <tr>
       <td>Action</td>
       <td>Command</td>
     </tr>
   </thead>
   <tbody>
     <tr>
       <td>**Next Page**</td>
       <td>`game:GetService("Selection"):Get()[1]:Next()`</td>
     </tr>
     <tr>
       <td>**Previous Page**</td>
       <td>`game:GetService("Selection"):Get()[1]:Previous()`</td>
     </tr>
     <tr>
       <td>**First Page**</td>
       <td>`game:GetService("Selection"):Get()[1]:JumpToIndex(0)`</td>
     </tr>
   </tbody>
   </table>

---

## Position and size UI objects

Unless UI objects are under control of a [layout structure](#layout-structures) or a [size modifier/constraint](../ui/size-modifiers.md), you have complete control over their [position](#position) and [size](#size). You can also set the Z‑index [layering](#zindex) order in which objects overlap.

## Core properties

All `Class.GuiObject|GuiObjects` share a core set of properties to [position](#position), [size](#size), [anchor](#anchorpoint), and [layer](#zindex) them within an on‑screen or in‑experience container.

### Position

The `Class.GuiObject.Position|Position` property is a `Datatype.UDim2` coordinate set that positions the object along the **X** and **Y** axes. A `Datatype.UDim2` is represented by both `Datatype.UDim.Scale|Scale` and `Datatype.UDim.Offset|Offset` values for each axis:

- `Datatype.UDim.Scale|Scale` values represent a **percentage** of the container's size along the corresponding axis, additive of any `Datatype.UDim.Offset|Offset` values.
- `Datatype.UDim.Offset|Offset` values represent how many **pixels** to shift the object on the corresponding axis, additive of any `Datatype.UDim.Scale|Scale` values.

<figure>
<img src="../assets/ui/misc/UDim2-Components.png" width="334" />
</figure>

To edit the position of a selected `Class.GuiObject`, click the **Position** field in the [Properties](../studio/properties.md) window and enter a new `Datatype.UDim2` coordinate set.

<img src="../assets/studio/properties/GuiObject-Position.png" width="320" />

<img src="../assets/ui/misc/Scale-Offset-Positioning.png" width="840" />

<Alert severity="success">
Brackets and spaces are **optional** when entering a `Datatype.UDim2` in Studio&nbsp;&mdash; you can simply enter the four values separated by commas, for instance `0.25,40,0.1,20`, and Studio will infer the intended value set.

Studio also infers the intended value set when a single number is entered. For example, entering simply `0.5` will be converted to <Typography noWrap>`{0.5, 0},{0.5, 0}`</Typ

[Content truncated - see full docs]

---

## Proximity prompts

`Class.ProximityPrompt` objects
encourage user interaction to trigger an action when they approach in-experience
objects such as doors, light switches, and buttons. Using this object, you can:

- Indicate what objects a user can interact with in the experience.
- Display the action a user can take on the object, then trigger the action through user input such as pressing or holding a key.
- Display the correct input for all input types, such a keyboard, gamepad, and touchscreen keys.

<video src="../assets/ui/proximity-prompt/Showcase.mp4" controls width="100%" alt="User interacting with proximity prompts to perform actions in the experience"></video>

<Alert severity="info">
See the [Dungeon Delve](https://www.roblox.com/games/6074153281/Dungeon-Delve) sample place for the fully working proximity prompt examples shown in the video above.
</Alert>

## Create proximity prompts

You must parent proximity prompts to the part, model, or attachment that you want a user to interact with. To add a proximity prompt to a `Class.BasePart`, `Class.Model`, or `Class.Attachment` object:

1. In the [Explorer](../studio/explorer.md) window, hover over the `Class.BasePart`, `Class.Model`, or `Class.Attachment` and click the &CirclePlus; button. A contextual menu displays.
1. From the menu, insert a **ProximityPrompt**.

   <img src="../assets/ui/proximity-prompt/ProximityPrompt-New.png" width="320" alt="Explorer hierarchy showing a ProximityPrompt parented to an Attachment" />

## Customize proximity prompts

You can customize a proximity prompt based on how you want it to [appear](#appearance), when you want it to be [visible](#visibility), and what you want a user to do to [trigger the action](#interactivity).

### Appearance

Proximity prompts need to communicate three things:

- The **object** that a user can interact with.
- The **action** that triggers when they interact with the proximity
  prompt.
- The **key** that a user must press or hold.

You can specify these through 

[Content truncated - see full docs]

---

## Rich text markup

UI **rich text** utilizes simple markup tags to style sections of a string in bold, italics, underline, fill color, stroke variations, and more. You can apply styling tags to `Class.TextLabel`, `Class.TextButton`, and `Class.TextBox` objects.

## Enable rich text

You must enable rich text on a per-object basis through its **RichText** property in the [Properties](../studio/properties.md) window, or by setting the property to `true` in a `Class.LocalScript`.

<img src="../assets/ui/rich-text/Enable-Rich-Text.png"
   width="320" />

```lua highlight="2"
local title = Instance.new("TextLabel")
title.RichText = true

title.Text = "Use a <b>bold title</b>"
```

<Alert severity="info">
When editing an object's **Text** property in Studio, toggling the **RichText** checkbox in the [Properties](../studio/properties.md) window displays the text string as a final render. This is useful for identifying and correcting mistakes in any [supported tags](#supported-tags).
</Alert>

<Alert severity="warning">
<a href="../production/localization/index.md">Localizing</a> a game to support other languages removes rich text formatting tags. To ensure formatting appears in other languages, re-apply the tags manually to your localized strings.
</Alert>

## Supported tags

Rich text tags are similar to XML/HTML tags and you must include both an opening and closing tag around the formatted text.

`<b>Formatted text</b>`

You can also nest tags inside each other as long as you close them in the reverse order of how you opened them.

`<b><i><u>Formatted text</u></i></b>`

### Font color

`<font color=""> </font>`

<blockquote>
`I want the <font color="#FF7800">orange</font> candy.`<br />
`I want the <font color="rgb(255,125,0)">orange</font> candy.`
<img src="../assets/ui/rich-text/Example-Color.png" width="600" />
</blockquote>

### Font size

`<font size=""> </font>`

<blockquote>
`<font size="40">This is big.</font> <font size="20">This is small.</font>`
<img src="../assets/ui/rich-text/E

[Content truncated - see full docs]

---

## Scrolling frames

A `Class.ScrollingFrame` consists of a customizable **canvas** and **scroll bars** with built‑in scrolling interactivity and different ways to customize how the scrolling works. `Class.ScrollingFrame` is ideal for displaying a lot of information in a confined space and it works well with [list](../ui/list-flex-layouts.md) and [grid](../ui/grid-table-layouts.md) layouts.

<img src="../assets/ui/ui-objects/ScrollingFrame-Example.jpg" width="840" alt="Example ScrollingFrame on the screen containing a tabbed category bar and a list of magical items for the player to consider purchasing." />

## Canvas

The **canvas** is the primary area of a `Class.ScrollingFrame` that can contain other `Class.GuiObject|GuiObjects`. Scrolling behavior automatically adapts in the following scenarios:

<table>
  <thead>
    <tr>
      <th>Frame Setup</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>The frame's `Class.ScrollingFrame.CanvasSize|CanvasSize` is taller than its overall height; specifically the total `Class.ScrollingFrame.CanvasSize|CanvasSize.Y` exceeds the total `Class.ScrollingFrame.Size|Size.Y`.</td>
      <td>Vertical scrolling is enabled and a vertical scroll bar appears.</td>
    </tr>
    <tr>
      <td>The frame's `Class.ScrollingFrame.CanvasSize|CanvasSize` is wider than its overall width; specifically the total `Class.ScrollingFrame.CanvasSize|CanvasSize.X` exceeds the total `Class.ScrollingFrame.Size|Size.X`.</td>
      <td>Horizontal scrolling is enabled and a horizontal scroll bar appears.</td>
    </tr>
    <tr>
      <td>The frame's `Class.ScrollingFrame.AutomaticCanvasSize|AutomaticCanvasSize` is set to `Enum.AutomaticSize|Y` or `Enum.AutomaticSize|XY` and the total height of its contents (child `Class.GuiObject|GuiObjects`) exceed its total `Class.ScrollingFrame.Size|Size.Y`.</td>
      <td>Vertical scrolling is enabled and a vertical scroll bar appears.</td>
    </tr>
    <tr>
      <td>The frame's `Class.ScrollingFrame.AutomaticCa

[Content truncated - see full docs]

---

## Size modifiers and constraints

Alongside basic [sizing](../ui/position-and-size.md) of UI objects, you can utilize size modifiers to [scale](#scale) an object proportionally or [automatically resize](#automatic-sizing) it. You can also insert [size constraints](#constraints) to control **aspect ratio**, or set a minimum and maximum **size** or **text size**.

## Scale

A `Class.UIScale` object stores a numerical value that multiplies the `Class.GuiBase2d.AbsoluteSize|AbsoluteSize` property of the parent `Class.GuiObject`. For example, if you want an object to be twice as large as it currently is, you can insert a `Class.UIScale` object with a `Class.UIScale.Scale|Scale` property of `2`.

This modifier is useful for "zooming in" while designing a detailed user interface in Studio, since it proportionally scales the object and all of its children, including any applied [appearance modifiers](../ui/appearance-modifiers.md) like `Class.UIStroke` or `Class.UICorner`. It's also useful to [tween](../ui/animation.md) the size of an object, for example to slightly increase the size of a button when a player hovers their mouse over it.

<img src="../assets/ui/ui-objects/UIScale-Example.png" width="800" />

## Automatic sizing

The `Class.GuiObject.AutomaticSize|AutomaticSize` property automatically resizes a parent `Class.GuiObject` to the size of its descendants. You can use this property in a variety of cases, including:

- Expanding a `Class.GuiObject` to fit text that has been [localized](../production/localization/index.md) in many languages.
- Allowing users to [input text](../ui/text-input.md) within a `Class.TextBox`, automatically adjusting its size based on the amount of text entered.
- Automatically adjusting the size of text objects using [rich text markup](../ui/rich-text.md), including font type and size.

<video controls width="90%" src="../assets/ui/automatic-sizing/Intro-Frame.mp4"></video>

You can enable the `Class.GuiObject.AutomaticSize|AutomaticSize` property for any `Class.GuiObject`

[Content truncated - see full docs]

---

## UI styling compatibility

import BetaAlert from '../../includes/beta-features/beta-alert.md'

<BetaAlert betaName="UI Styling" leadIn="UI styling and related workflows are currently in beta and must be enabled through " leadOut="." components={props.components} />

The following tables outline all of the classes and associated properties which can be styled. Additional support may be added over time, so please bookmark this page for reference.

## UI objects

### GuiObject

`Class.GuiObject` is an abstract class from which most UI classes inherit, including [frames](../frames.md), [labels](../labels.md), [buttons](../buttons.md), and more.

<table size="small">
<thead>
  <tr>
    <th>Property</th>
    <th width="40%">Type</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>`Class.GuiObject.Active`</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.AnchorPoint`</td>
    <td>`Datatype.Vector2`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.AutomaticSize`</td>
    <td>`Enum.AutomaticSize`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BackgroundColor`</td>
    <td>`Datatype.BrickColor`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BackgroundColor3`</td>
    <td>`Datatype.Color3`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BackgroundTransparency`</td>
    <td>float</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BorderColor3`</td>
    <td>`Datatype.Color3`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BorderMode`</td>
    <td>`Enum.BorderMode`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.BorderSizePixel`</td>
    <td>integer</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.ClipsDescendants`</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.Interactable`</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.LayoutOrder`</td>
    <td>integer</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.Position`</td>
    <td>`Datatype.UDim2`</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.Rotation`</td>
    <td>float</td>
  </tr>
  <tr>
    <td>`Class.GuiObject.Selectable`</td>
    <td>boolean

[Content truncated - see full docs]

---

## CSS Comparisons

import BetaAlert from '../../includes/beta-features/beta-alert.md'

<BetaAlert betaName="UI Styling" leadIn="UI styling and related workflows are currently in beta and must be enabled through " leadOut="." components={props.components} />

Most CSS concepts map to Roblox styling concepts. The following examples show how CSS and HTML align with Luau and Roblox classes/properties.

To test each of the following Luau script examples:

1. In the [Explorer](../../studio/explorer.md), create the following:

   <img src="../../assets/studio/explorer/CSS-Test-Setup.png" width="320" style={{float: "right;", marginLeft: "20px;"}} />

	 1. `Class.StyleSheet` instance named `CoreSheet` inside `Class.ReplicatedStorage`.
	 2. Empty `Class.StyleRule` instance as a child of `CoreSheet`.
	 3. `Class.ScreenGui` container in `Class.StarterGui`.
	 4. `Class.LocalScript` instance inside the `Class.ScreenGui`.
	 5. `Class.StyleLink` object inside the `Class.ScreenGui` whose `Class.StyleLink.StyleSheet|StyleSheet` property is linked to `CoreSheet`.

2. In the `Class.LocalScript`, paste the following supporting code:

		```lua title="LocalScript"
		local CollectionService = game:GetService("CollectionService")
		local ReplicatedStorage = game:GetService("ReplicatedStorage")

		local coreSheet = ReplicatedStorage:FindFirstChild("CoreSheet")
		local rule = coreSheet:FindFirstChildWhichIsA("StyleRule")
		local screenGui = script.Parent
		```

3. For each example below, paste the **Luau** code lines following the supporting lines 1–6.

## Selectors

The `Class.StyleRule.Selector|Selector` property of a `Class.StyleRule` specifies which instances the rule should affect. The following selector types map from CSS to Luau and can be used with combinators.

### Element

Equivalent to CSS element selectors are Roblox **class selectors** which select all instances of a given `Class.GuiObject` class, for example `Class.Frame`, `Class.ImageLabel`, `Class.TextButton`, etc.

<Card>
<CardContent style={{p

[Content truncated - see full docs]

---

## Style Editor

import BetaAlert from '../../includes/beta-features/beta-alert.md'

<BetaAlert betaName="UI Styling" leadIn="UI styling and related workflows are currently in beta and must be enabled through " leadOut="." components={props.components} />

The built-in **Style Editor** is a comprehensive tool that allows you to create, manage, and apply UI styles for Roblox experiences through a combination of [tokens](#style-tokens), [design sheets](#design-sheets), [style rules](#style-rules), and [themes](#style-themes).

<figure>
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/_k1ea0OIKaU?si=A9mdnnG95qdaZbB_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</figure>

Access the **Style Editor** via the **UI** tab.

<img src="../../assets/studio/general/Toolbar-Style-Editor.png" width="800" alt="Style Editor tool indicated in UI tab of Studio toolbar" />

Once open, click the **Create Design** button to generate a base style set.

<img src="../../assets/ui/ui-styling/SE-Create-Design-Entry.png" width="350" alt="Create Design button in opening dialog of Style Editor." />

<Alert severity="warning">
Creating a design style set through the Style Editor generates a **BaseStyleSheet** inside a **Design** folder within `Class.ReplicatedStorage`. This base sheet syncs specific engine‑level defaults like the `Datatype.Color3` default of <Typography noWrap>`[163, 162, 165]`</Typography> with defaults that come from insertion workflows in Studio. It's highly recommended that you do **not** delete or attempt to modify the base style sheet&nbsp;— instead, build tokens and style rules around a design sheet to match your UI goals.

Additionally, a **StyleSheet** sheet is generated in the **Design** folder which contains a `Class.StyleDerive` to the base style sheet. If you choose to remov

[Content truncated - see full docs]

---

## UI styling

import BetaAlert from '../../includes/beta-features/beta-alert.md'

<BetaAlert betaName="UI Styling" leadIn="UI styling and related workflows are currently in beta and must be enabled through " leadOut="." components={props.components} />

UI styling is a Roblox solution to stylesheets, [similar to CSS](css-comparisons.md), that lets you declare and globally apply overrides to UI instance properties. This engine‑level support is the foundation for the [Style&nbsp;Editor](./editor.md) and the end‑to‑end token pipeline.

## Concepts

Style **rules** (part of a `Class.StyleSheet`) apply to every instance that matches the rule's `Class.StyleRule.Selector|Selector` definition to match characteristics such as class name, instance name, and hierarchy relationships. See the `Class.StyleRule.Selector|Selector` documentation for details.

Style **tokens**, defined through [attributes](../../studio/properties.md#instance-attributes) of a token `Class.StyleSheet`, represent UI property variables that can be used across styles and components, for example a common color for a `Class.Frame.BackgroundColor3`, `Class.TextLabel.TextColor3`, and `Class.UIStroke.Color`. Tokens are comparable to CSS [variables](css-comparisons.md#variables).

Style **themes**, configured through [attributes](../../studio/properties.md#instance-attributes) of a theme `Class.StyleSheet`, consist of sets of specific tokens that can be swapped, for example color tokens that define a "light" and "dark" theme. Related themes must have the same set of tokens to work correctly.

<figure>
<img src="../../assets/studio/explorer/Styling-Hierarchy.png" width="414" />
</figure>

## Rule propagation

A `Class.StyleLink` instance links a `Class.StyleSheet` and its associated rules to a parent `Class.ScreenGui` and all of the `Class.GuiObject|GuiObjects` within it. Only one `Class.StyleSheet` can apply to a given tree.

<img src="../../assets/studio/explorer/StyleLink-Propagation.png" width="320" />

## Selector defini

[Content truncated - see full docs]

---

## Text filtering

Applied to various sources and inputs, **text filtering** prevents users from seeing inappropriate language and personally identifiable information such as phone numbers. Roblox automatically filters common text outputs such as messages that have passed through [in-experience text chat](../chat/in-experience-text-chat.md), but **you are responsible for filtering any displayed text that you don't have explicit control over**.

<Alert severity="error">
Because filtering is crucial for a safe environment, Roblox actively moderates the content of experiences to make sure they meet [community standards](https://en.help.roblox.com/hc/en-us/articles/203313410-Roblox-Community-Standards). If Roblox receives reports or automatically detects that your experience doesn't apply text filtering, then the system removes the experience until you add filtering.
</Alert>

## Filter scenarios

Text can be gathered and/or displayed to users in a variety of scenarios, including:

- An experience that gathers users' [text input](../ui/text-input.md) through `Class.TextBox` entries, a custom GUI with buttons such as a keyboard/keypad interface, or an interactive keyboard model in the 3D space.

- An experience that generates words from random characters and displays them to users, as there's a chance it will create inappropriate words.

- An experience that connects to an external web server to fetch content that is displayed in-experience. Often you will not have control over the content of the external site and a third party can edit the information.

- An experience that stores text such as users' pet names using [data stores](../cloud-services/data-stores), where the stored text might include inappropriate words that should be filtered when retrieving them.

## Filtering process

`Class.TextService:FilterStringAsync()` filters in-experience text by taking a string of text and the `Class.Player.UserId|UserId` of the user who created the text as input. It returns a `Class.TextFilterResu

[Content truncated - see full docs]

---

## Text input fields

import TextFiltering from '../includes/text-filtering/text-filtering.md'

A `Class.TextBox` is a rectangle that allows a user to provide text input while it's in focus. When you [script](#script-text-inputs) a `Class.TextBox`, you can use it as a search bar or an input field on a form. To help users know what type of text they should input, you can also provide a prompt through the `Class.TextBox.PlaceholderText|PlaceholderText` property.

<img src="../assets/ui/ui-objects/TextBox-Example.jpg" width="840" />

Because these objects are `Class.GuiObject|GuiObjects`, you can customize
properties such as `Class.GuiObject.BackgroundColor3|BackgroundColor3`,
`Class.GuiObject.BorderMode|BorderMode`,
`Class.GuiObject.Transparency|Transparency`, and
`Class.GuiObject.Rotation|Rotation` to fit the aesthetics of your experience.

## Create text inputs on the screen

A `Class.TextBox` on a screen is useful for
things like an input field for a form.

To add a `Class.TextBox` to a screen:

1. In the **Explorer** window, select **StarterGui** and add a **ScreenGui**.

   1. Hover over StarterGui and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **ScreenGui**.

2. Select the new **ScreenGui** and add a **TextBox**.

   1. Hover over **ScreenGui** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **TextBox**.

## Create text inputs on part faces

To add a `Class.TextBox` to the face of a part:

1. In the **Explorer** window, select **StarterGui** and add a **SurfaceGui**.

   1. Hover over StarterGui and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **ScreenGui**.

2. Select the new **SurfaceGui** and add a **TextBox**.

   1. Hover over **SurfaceGui** and click the &CirclePlus; button. A contextual menu displays.

   1. Insert a **TextBox**.

3. Adorn the **SurfaceGui** to the **part** on which you want to display the **TextBox**.

   1. In the **Properties** window, select the **Adornee** propert

[Content truncated - see full docs]

---

## UI drag detectors

import BetaAlert from '../includes/beta-features/beta-alert.md'

<BetaAlert betaName="UIDragDetectors" leadIn="This feature is currently in beta. Enable it through " leadOut="." components={props.components} />

The `Class.UIDragDetector` instance facilitates and encourages interaction with 2D user interface elements in an experience, such as sliders, spinners, and more. Key features include:

- Place a `Class.UIDragDetector` under any `Class.GuiObject` instance to make it draggable via all user inputs without a single line of code.

- Choose from several `Class.UIDragDetector.DragStyle|DragStyle` options, define how the object responds to motion via `Class.UIDragDetector.ResponseStyle|ResponseStyle`, and optionally apply axis, movement limits, or drag boundaries.

- Scripts can respond to manipulation of dragged objects to drive logic responses, such as adjusting settings.

- `Class.UIDragDetector|UIDragDetectors` work in Studio's edit and play mode as long as you're **not** using the **Select**, **Move**, **Scale**, or **Rotate** tools, nor certain plugins or Studio's **UI** editor tools.

<video src="../assets/ui/ui-drag-detectors/Showcase.mp4" controls width="100%" alt="How to add UI Drag Detectors and Drag in Edit Mode"></video>

<Alert severity="info">
For drag detectors that manipulate 3D objects in an experience, such as opening doors and drawers or sliding a part around, see [3D Drag Detectors](../ui/3D-drag-detectors.md).
</Alert>

## Make UI elements draggable

To make any `Class.GuiObject` instances draggable, simply add a `Class.UIDragDetector` as a direct descendant.

1. In the [Explorer](../studio/explorer.md) window, hover over the `Class.GuiObject` instance and click the &CirclePlus; button. A contextual menu displays.
1. From the menu, insert a **UIDragDetector**.

   <img src="../assets/studio/explorer/StarterGui-UIDragDetector.png" width="320" />

1. By default, the object will now be draggable in the `Class.LayerCollector|LayerCollector` interfa

[Content truncated - see full docs]

---

## Video frames

import BetaAlert from '../includes/beta-features/beta-alert.md'

Video assets used in `Class.VideoFrame` instances allow for video playback in experiences. You can [upload](#upload-videos) videos that you're certain you have permission to use, such as videos you make yourself, and the [asset privacy](../projects/assets/privacy.md) system automatically ensures that the IDs of your uploaded videos can't be accessed by users without the proper permissions.

## Upload videos

<BetaAlert betaName="Video Uploads" leadIn="To upload video assets, enable the beta feature through " leadOut="." components={props.components} />

If you're a 13+ [ID verified](https://en.help.roblox.com/hc/en-us/articles/4407282410644-Age-ID-Verification) user, you can upload videos through the [Asset Manager](../projects/assets/manager.md), the [Creator Dashboard](https://create.roblox.com/dashboard/creations?activeTab=Video), or the [Open Cloud API](../cloud/guides/usage-assets.md). You can upload a video as long as it meets the following requirements:

- You have the legal rights to use the video asset.
- It adheres to the [Roblox Community Standards](https://en.help.roblox.com/hc/en-us/articles/203313410) and [Terms of Use](https://en.help.roblox.com/hc/en-us/articles/115004647846).
- It's 5 minutes or less in either `.mp4` or `.mov` format.
- Its resolution is less than or equal to 4096&times;2160.
- It's less than 3.75 GB.
- It includes only English, Spanish, Portuguese, Indonesian, Chinese (simplified and traditional), Japanese, and/or Korean audio and text.

Videos that don't meet these requirements are rejected. Alpha channels are not supported and will be ignored. When uploading videos, consider the following:

- Each video upload costs 2,000 Robux.
- You can upload a maximum of 20 videos a day.

## Play videos

A `Class.VideoFrame` must be parented to a `Class.ScreenGui`, `Class.SurfaceGui`, or `Class.BillboardGui` in order to be playable. Currently, a maximum of two videos can play si

[Content truncated - see full docs]

---

## Viewport frames

A `Class.ViewportFrame` uses a camera to render 3D objects into a 2D viewport. Ideal use cases include:

- A minimap of your experience directly in the corner of a user's screen.
- 3D models of items in an inventory menu.
- Rotating objects that a character has equipped.

## Viewport configurations

3D objects that users view through a `Class.ViewportFrame` can either move with their camera, remain static, or rotate within the `Class.ViewportFrame`. This object can also include a `Class.Sky` child as a cubemap for reflections.

<Tabs>
<TabItem label="With Camera">

If you want a 3D object to move with the camera:

1. Position your camera view within the experience so that the object you want to see within the frame is visible.
2. Add a new `Class.ViewportFrame` to the [screen](../ui/on-screen-containers.md) and then make sure it's selected in the **Explorer**.
3. In the **Properties** window, assign the `Class.ViewportFrame.CurrentCamera|CurrentCamera` property to the camera:

	 1. Select the `Class.ViewportFrame.CurrentCamera|CurrentCamera` property. Your cursor changes.
	 2. In the **Explorer** window, click on the top-level `Class.Camera` object.

4. Parent the desired 3D object to the new `Class.ViewportFrame`. Note that if you still want to see the object within your experience, you must duplicate it in the `Class.Workspace` and then parent the **duplicate** object to the `Class.ViewportFrame`.

When you move your camera, the object will also move within the `Class.ViewportFrame`.

<Alert severity="warning">
When you want to update the view of your `Class.ViewportFrame`, be sure to update the camera, **not** the objects within the view.
</Alert>

</TabItem>
<TabItem label="Static">

If you want the 3D object to remain static:

1. Position your camera view within the experience so that the object you want to see is in the exact position you want to see it within the frame.
2. In the **Explorer** window, duplicate the top-level `Class.Camera` object, then rename 

[Content truncated - see full docs]

---

