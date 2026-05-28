# Parts Classes

## Contents
- [Part](#part)
- [MeshPart](#meshpart)
- [UnionOperation](#unionoperation)
- [Model](#model)
- [Folder](#folder)
- [SpawnLocation](#spawnlocation)
- [Seat](#seat)
- [VehicleSeat](#vehicleseat)
- [TrussPart](#trusspart)
- [WedgePart](#wedgepart)
- [CornerWedgePart](#cornerwedgepart)
- [Terrain](#terrain)

---

## Part

A common type of `Class.BasePart` that comes in different primitive shapes.

**Properties:**
- `Part.Shape`: PartType - Sets the overall shape of the object.

---

## MeshPart

A form of `Class.BasePart` that includes a physically simulated custom mesh.

**Properties:**
- `MeshPart.DoubleSided`: boolean - Determines whether to render both faces of polygons in the mesh.
- `MeshPart.HasJointOffset`: boolean
- `MeshPart.HasSkinnedMesh`: boolean
- `MeshPart.JointOffset`: Vector3
- `MeshPart.MeshContent`: Content - The mesh that is displayed on the `Class.MeshPart`. Supports
- `MeshPart.MeshId`: ContentId - The [asset URIs](../../../projects/assets/index.md#asset-uris) of the mesh
- `MeshPart.RenderFidelity`: RenderFidelity - The level of detail used to render the `Class.MeshPart`.
- `MeshPart.TextureContent`: Content - The texture applied to the `Class.MeshPart`. Supports
- `MeshPart.TextureID`: ContentId - The texture applied to the `Class.MeshPart`. Reads and writes to

**Methods:**
- `MeshPart:ApplyMesh` - Overwrites the `Class.MeshPart.MeshContent|MeshContent`,

---

## UnionOperation

Result of parts that have been joined together into a single solid model.

---

## Model

Models are container objects, meaning they group objects together. They are
best used to hold collections of `Class.BasePart|BaseParts` and have a number
of functions that extend their functionality.

**Properties:**
- `Model.LevelOfDetail`: ModelLevelOfDetail - Sets the level of detail on the model for experiences with instance
- `Model.ModelStreamingMode`: ModelStreamingMode - Controls the model streaming behavior on `Class.Model|Models` when
- `Model.PrimaryPart`: BasePart - The primary part of the `Class.Model`, or `nil` if not explicitly set.
- `Model.Scale`: float - Editor-only property used to scale the model around its pivot. Setting
- `Model.WorldPivot`: CFrame - Determines where the pivot of a `Class.Model` which does **not** have a

**Methods:**
- `Model:AddPersistentPlayer` - Sets this model to be persistent for the specified player.
- `Model:BreakJoints` - Breaks connections between `BaseParts`, including surface connections with
- `Model:breakJoints`
- `Model:GetBoundingBox` - Returns a description of a volume that contains all parts of a Model.
- `Model:GetExtentsSize` - Returns the size of the smallest bounding box that contains all of the
- `Model:GetModelCFrame` - This value historically returned the CFrame of a central position in the
- `Model:GetModelSize` - Returns the Vector3 size of the Model.
- `Model:GetPersistentPlayers` - Returns all the `Class.Player` objects that this model object is
- `Model:GetPrimaryPartCFrame` - Returns the `Datatype.CFrame` of the model's `Class.Model.PrimaryPart`.
- `Model:GetScale` - Returns the canonical scale of the model, which defaults to 1 for newly
- ...and 11 more

---

## Folder

A simple container used to hold and organize Roblox instances.

---

## SpawnLocation

`Class.SpawnLocation|SpawnLocations`, or "spawns" determine where a
`Class.Player` respawns when they die. They can be configured to allow only
certain players to use each spawn, using `Class.Team|Teams`. They also control
how `Class.ForceField|ForceFields` are set up for newly-spawned players.

**Properties:**
- `SpawnLocation.AllowTeamChangeOnTouch`: boolean - Allows a `Class.Player` to join the team by touching the
- `SpawnLocation.Duration`: int - The length of time, in seconds, that a `Class.ForceField` will be applied
- `SpawnLocation.Enabled`: boolean - Sets whether or not the `Class.SpawnLocation` is enabled. When disabled
- `SpawnLocation.Neutral`: boolean - Whether or not a `Class.SpawnLocation` is affiliated with a specific team.
- `SpawnLocation.TeamColor`: BrickColor - Sets what team the `Class.SpawnLocation` is affiliated to. If

---

## Seat

A type of `Class.BasePart` that characters can 'sit' in. When a character
touches an enabled Seat object, it will be attached to the part by a
`Class.Weld` and the default character scripts will play a sitting animation.

**Properties:**
- `Seat.Disabled`: boolean - Whether or not the seat is usable. If set to true, the seat will act as a
- `Seat.Occupant`: Humanoid - The humanoid that is sitting in the seat.

**Methods:**
- `Seat:Sit` - Forces the character with the specified `Class.Humanoid` to sit in the

---

## VehicleSeat

A seat object that can be used to control a vehicle.

**Properties:**
- `VehicleSeat.AreHingesDetected`: int - Displays how many hinges are detected by the VehicleSeat. Useful for
- `VehicleSeat.Disabled`: boolean - Toggles whether the `Class.VehicleSeat` is active or not.
- `VehicleSeat.HeadsUpDisplay`: boolean - If true, a fancy speed bar will be displayed speed on screen that tells
- `VehicleSeat.MaxSpeed`: float - The maximum speed that can be attained.
- `VehicleSeat.Occupant`: Humanoid - The humanoid that is sitting in the seat.
- `VehicleSeat.Steer`: int - The direction of movement, tied to the keys A and D. Must be one of 1
- `VehicleSeat.SteerFloat`: float - Functions identically to `Class.VehicleSeat.Steer`, but the value is not
- `VehicleSeat.Throttle`: int - The direction of movement, tied to the keys W and S. Must be an integer 1
- `VehicleSeat.ThrottleFloat`: float - Functions identically to `Class.VehicleSeat.Throttle`, but the value is
- `VehicleSeat.Torque`: float - How fast the vehicles will be able to attain `Class.VehicleSeat.MaxSpeed`.
- ...and 1 more

**Methods:**
- `VehicleSeat:Sit` - Forces the character with the specified `Class.Humanoid` to sit in the

---

## TrussPart

Similar to a `Class.Part` but with a different visual
`Class.TrussPart.Style|Style` and the important distinction that default
characters are able to climb it.

**Properties:**
- `TrussPart.Style`: Style - Sets what the truss looks like.

---

## WedgePart

A type of `Class.BasePart` that has a wedge shape.

---

## CornerWedgePart

---

## Terrain

Terrain lets you to create dynamically morphable environments.

**Properties:**
- `Terrain.Decoration`: boolean - Enables or disables terrain decoration.
- `Terrain.GrassLength`: float - Specifies the length of animated grass.
- `Terrain.IsSmooth`: boolean - Returns true if the current game is using the smooth terrain system.
- `Terrain.MaterialColors`: BinaryString - MaterialColors represents the editor for the Material Color feature, and
- `Terrain.MaxExtents`: Region3int16 - Displays the boundaries of the largest possible editable region.
- `Terrain.WaterColor`: Color3 - The tint of the Terrain water.
- `Terrain.WaterReflectance`: float - Controls how opaque the Terrain's water reflections are.
- `Terrain.WaterTransparency`: float - The transparency of the Terrain water.
- `Terrain.WaterWaveSize`: float - Sets the maximum height of the Terrain water waves in studs.
- `Terrain.WaterWaveSpeed`: float - Sets how many times the Terrain water waves will move up and down per

**Methods:**
- `Terrain:AutowedgeCell` - _(OBSOLETE)_ No longer does anything.
- `Terrain:AutowedgeCells` - _(OBSOLETE)_ No longer does anything.
- `Terrain:CellCenterToWorld` - Returns the world position of the center of the terrain cell (x, y, z).
- `Terrain:CellCornerToWorld` - Returns the position of the lower-left-forward corner of the grid cell (x,
- `Terrain:Clear` - Clears the terrain.
- `Terrain:ClearVoxelsAsync_beta`
- `Terrain:ConvertToSmooth` - Transforms the legacy terrain engine into the new terrain engine.
- `Terrain:CopyRegion` - Stores a chunk of terrain into a `Class.TerrainRegion` object so it can be
- `Terrain:CountCells` - Returns the number of non-empty cells in the Terrain.
- `Terrain:FillBall` - Fills a ball of smooth terrain in a given space.
- ...and 24 more

---

