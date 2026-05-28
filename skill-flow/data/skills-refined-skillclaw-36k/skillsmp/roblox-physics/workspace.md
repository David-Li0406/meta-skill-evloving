# Workspace Reference

## Contents
- [Customize the camera](#customize-the-camera)
- [CFrames](#cframes)
- [Collisions](#collisions)
- [3D workspace](#3d-workspace)
- [Raycasting](#raycasting)
- [Instance streaming](#instance-streaming)

---

## Customize the camera

Roblox's built-in camera powers a default **third person** mode and an optional **first person** mode, so you don't need to build your own following camera. For more customized scenarios, you can adjust the default properties in `Class.Camera` or replace it entirely like for over-the-shoulder, isometric, and weapon scoping views.

## Basic settings

You can configure common camera settings directly within Studio's `Class.StarterPlayer` object. These settings include [zoom distance](#zoom-distance) and various [camera](#camera-mode), [occlusion](#occlusion-mode), and [movement](#movement-mode) modes.

1. In the **Explorer** window, select the **StarterPlayer** object.

   <img src="../assets/studio/explorer/StarterPlayer.png" width="320" alt="StarterPlayer in Explorer" />

1. In the **Properties** window, scroll down to locate the **Camera** section. You can configure the following properties directly or through a script.

   <img src="../assets/studio/properties/StarterPlayer-Camera-Group.png" width="320" alt="Camera properties on StarterPlayer in Properties Window" />

### Zoom distance

Together, `Class.StarterPlayer.CameraMaxZoomDistance|CameraMaxZoomDistance` and `Class.StarterPlayer.CameraMinZoomDistance|CameraMinZoomDistance` set the range in which players can zoom the camera in respect to their player character. Setting a very high maximum such as 500 allows players to zoom the camera far out in space. If you want to lock the camera to a specific distance away from the character and prevent zooming, set both of these properties to the same value.

```lua title="LocalScript - Camera Zoom Range" highlight="5,6"
local Players = game:GetService("Players")

local player = Players.LocalPlayer

player.CameraMaxZoomDistance = 25
player.CameraMinZoomDistance = 50
```

### Camera mode

The `Class.StarterPlayer.CameraMode|CameraMode` property sets the overall behavior of the camera between two options:

<table>
<thead>
  <tr>
    <th>Setting</th>
    <th>Description</th

[Content truncated - see full docs]

---

## CFrames

A `Datatype.CFrame`, short for **Coordinate Frame**, is a data type used to rotate and position 3D objects. As either an object property or a standalone unit, a `Datatype.CFrame` contains global x-, y-, and z-coordinates as well as rotation data for each axis. In addition, `Datatype.CFrame|CFrames` contain helpful functions for working with objects in the 3D space.

Some examples of `Datatype.CFrame` applications in a game might be:

- Finding a far-off target point for a projectile, like the position of an enemy targeted by a player's laser blaster.
- Moving the camera so that it focuses on specific NPCs as a player interacts with them.
- Placing a status indicator directly above a player's head to show if they are paralyzed, boosted, poisoned, etc.

## CFrame basics

### Position a CFrame

You can create an empty `Datatype.CFrame` at the default position of (0, 0, 0) by using `Datatype.CFrame.new()`. To position a `Datatype.CFrame` at a specific point, provide x-, y-, and z-coordinates as arguments to `Datatype.CFrame.new()`. In the following example, the `redBlock` part's `Datatype.CFrame` property changes to `newCFrame`, repositioning it to (-2, 2, 4).

```lua highlight="4,7"
local Workspace = game:GetService("Workspace")

local redBlock = Workspace.RedBlock

-- Create new CFrame
local newCFrame = CFrame.new(-2, 2, 4)

-- Overwrite redBlock's current CFrame with new CFrame
redBlock.CFrame = newCFrame
```

<GridContainer numColumns="2">
  <figure>
    <img src="../assets/modeling/cframes/CFrame-Strict-Position-A.png" />
    <figcaption>Before</figcaption>
  </figure>
  <figure>
    <img src="../assets/modeling/cframes/CFrame-Strict-Position-B.png" />
    <figcaption>After</figcaption>
  </figure>
</GridContainer>

Alternatively, you can provide a new `Datatype.Vector3` position to `Datatype.CFrame.new()` and achieve the same result:

```lua highlight="5-6,8"
local Workspace = game:GetService("Workspace")

local redBlock = Workspace.RedBlock

-- Create new CFrame


[Content truncated - see full docs]

---

## Collisions

A collision occurs when two 3D objects come into contact within the 3D world. For customized collision handling, `Class.BasePart` has a set of [collision events](#collision-events) and [collision filtering](#collision-filtering) techniques, so you can control which physical assemblies collide with others.

## Collision events

Collision **events** occur when two `Class.BasePart|BaseParts` touch or stop touching in the 3D world. You can detect these collisions through the `Class.BasePart.Touched|Touched` and `Class.BasePart.TouchEnded|TouchEnded` events which occur regardless of either part's `Class.BasePart.CanCollide|CanCollide` property value. When considering collision handling on parts, note the following:

- A part's `Class.BasePart.CanTouch|CanTouch` property determines whether it triggers collision events. If set to `false`, neither `Class.BasePart.Touched|Touched` nor `Class.BasePart.TouchEnded|TouchEnded` will fire.
- A part's `Class.BasePart.CanCollide|CanCollide` property affects whether it will **physically** collide with other parts and cause forces to act upon them. Even if `Class.BasePart.CanCollide|CanCollide` is disabled for a part, you can detect touch and non‑touch through `Class.BasePart.Touched|Touched` and `Class.BasePart.TouchEnded|TouchEnded` events.
- The `Class.BasePart.Touched|Touched` and `Class.BasePart.TouchEnded|TouchEnded` events only fire as a result of **physical** movement, not from a `Class.BasePart.Position|Position` or `Class.BasePart.CFrame|CFrame` changes that cause a part to intersect or stop intersecting another part.
- The top-level `Class.Terrain` class inherits from `Class.BasePart`, so you can assign a [collision group](#collision-groups) to `Class.Terrain` to determine whether other `Class.BasePart|BaseParts` collide with [Terrain](../parts/terrain.md) voxels.

<Alert severity="info">
For performance optimization, set `Class.BasePart.CanTouch|CanTouch` to `false` for objects that don't require collisions.
</Alert>

### 

[Content truncated - see full docs]

---

## 3D workspace

`Class.Workspace` is a container service that holds objects that you want the
Roblox Engine to render in the 3D world. You typically will add these objects to
the workspace:

- `Class.BasePart` objects, which includes both `Class.Part` and `Class.MeshPart` objects.
- `Class.Attachment` objects, which you can attach to special effect generators like a `Class.ParticleEmitter`, UI objects like a `Class.BillboardGui`, physical `Class.Constraint|Constraints`, and more.
- `Class.Model` objects that organize geometric groupings.
- `Class.Script` objects that are parented by other objects in the workspace.
  Scripts aren't rendered but can affect another object's rendering.

## Parts

`Class.Part` objects represent the primitive building blocks in Roblox. By default, all parts have their physics simulated and are rendered if they appear in the 3D workspace. Parts can take the shape of blocks, spheres, cylinders, wedges, or corner wedges. In addition, `Class.TrussPart` acts as a truss beam that characters can climb like a ladder.

<Grid container spacing={1}>
<Grid item XSmall={4} XLarge={2}>
	<figure>
	<img src="../assets/modeling/parts/Basic-Part-Block.png" alt="A single Block part." />
	<figcaption><center>Block</center></figcaption>
	</figure>
</Grid>
<Grid item XSmall={4} XLarge={2}>
	<figure>
	<img src="../assets/modeling/parts/Basic-Part-Sphere.png" alt="A single Sphere part." />
	<figcaption><center>Sphere</center></figcaption>
	</figure>
</Grid>
<Grid item XSmall={4} XLarge={2}>
	<figure>
	<img src="../assets/modeling/parts/Basic-Part-Cylinder.png" alt="A single Cylinder part." />
	<figcaption><center>Cylinder</center></figcaption>
	</figure>
</Grid>
<Grid item XSmall={4} XLarge={2}>
	<figure>
	<img src="../assets/modeling/parts/Basic-Part-Wedge.png" alt="A single Wedge part." />
	<figcaption><center>Wedge</center></figcaption>
	</figure>
</Grid>
<Grid item XSmall={4} XLarge={2}>
	<figure>
	<img src="../assets/modeling/parts/Basic-Part-Corner-Wedge.png" alt="A singl

[Content truncated - see full docs]

---

## Raycasting

At its most basic level, **raycasting** is the act of sending out an invisible ray from a `Datatype.Vector3` point in a specific direction with a defined length. Once cast, you can detect if the ray hits a `Class.BasePart` or `Class.Terrain` cell.

<figure>
  <video controls src="../assets/workspace/raycasting/Laser-Maze.mp4" width="100%"></video>
  <figcaption>Lasers are fired by floating orbs, and raycasting determines whether a laser hits a platform. Platforms touched by the lasers are temporarily destroyed.</figcaption>
</figure>

You can cast a ray with the `Class.WorldRoot:Raycast()` method (`Class.Workspace:Raycast()`) from a `Datatype.Vector3` origin in a `Datatype.Vector3` direction.

```lua title="Basic Raycast" highlight="4"
local Workspace = game:GetService("Workspace")

local rayOrigin = Vector3.new(0, 0, 0)
local rayDirection = Vector3.new(0, -100, 0)

local raycastResult = Workspace:Raycast(rayOrigin, rayDirection)
```

<Alert severity="warning">
When casting a ray, the direction parameter should encompass the desired length of the ray. For instance, if the magnitude of the direction is 10, the resulting ray will also be of length 10. The maximum length is 15,000 studs.
</Alert>

When applicable, you can calculate an unknown directional vector (`rayDirection`) using a known **origin** and **destination**. This is useful when casting a ray between two points that can change, such as from one player character to another.

1. The origin plus a directional vector indicate the ray's destination:

   $\text{rayOrigin} + \text{rayDirection} = \text{rayDestination}$

2. Subtract $\text{rayOrigin}$ from both sides of the equation:

   $\text{rayOrigin} + \text{rayDirection} - \text{rayOrigin} = \text{rayDestination} - \text{rayOrigin}$

3. The ray's direction equals the destination minus the origin:

   $\text{rayDirection} = \text{rayDestination} - \text{rayOrigin}$

```lua highlight="4"
local Workspace = game:GetService("Workspace")

local rayOrigin = Worksp

[Content truncated - see full docs]

---

## Instance streaming

import BetaAlert from '../includes/beta-features/beta-alert.md'

In-experience **instance streaming** allows the Roblox Engine to dynamically load and unload 3D content and related instances in regions of the world. This can improve the overall player experience in several ways, for example:

- **Faster join times** &mdash; Players can start playing in one part of the world while more of the world loads in the background.
- **Memory efficiency** &mdash; Experiences can be played on devices with less memory since content is dynamically streamed in and out. More immersive and detailed worlds can be played on a wider range of devices.
- **Improved performance** &mdash; Better frame rates and performance, as the server can spend less time and bandwidth synchronizing changes between the world and players in it. Clients spend less time updating instances that aren't currently relevant to the player.
- **Level of detail** &mdash; Distant models and terrain remain visible even when they're not streamed to clients, keeping the experience optimized without entirely sacrificing background visuals.

## Enable streaming

Instance streaming is enabled through the **StreamingEnabled** property of the **Workspace** object in Studio. This property cannot be set in a script. Streaming is enabled by default for new places created in Studio.

<img src="../assets/studio/properties/Workspace-StreamingEnabled.png" width="320" alt="The Properties window with the StreamingEnabled property enabled." />

Once enabled, it's recommended that you adhere to the following practices:

- Because clients will not typically have the entire `Class.Workspace` available locally, use the appropriate tool/API to ensure that instances exist before attempting to access them in a `Class.LocalScript`. For example, utilize [per‑model streaming controls](#per-model-streaming-controls), [detect instance streaming](#detect-instance-streaming), or use `Class.Instance:WaitForChild()|WaitForChild()` on objects that m

[Content truncated - see full docs]

---

