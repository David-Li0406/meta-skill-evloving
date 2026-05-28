# Characters Classes

## Contents
- [Humanoid](#humanoid)
- [HumanoidDescription](#humanoiddescription)
- [Accessory](#accessory)
- [Shirt](#shirt)
- [Pants](#pants)
- [CharacterMesh](#charactermesh)

---

## Humanoid

A special object that gives models the functionality of a character.

**Properties:**
- `Humanoid.AutoJumpEnabled`: boolean - Sets whether the character will automatically jump when they hit an
- `Humanoid.AutomaticScalingEnabled`: boolean - When Enabled, AutomaticScalingEnabled causes the size of the character to
- `Humanoid.AutoRotate`: boolean - AutoRotate sets whether or not the Humanoid will automatically rotate to
- `Humanoid.BreakJointsOnDeath`: boolean - Determines whether the humanoid's joints break when in the
- `Humanoid.CameraOffset`: Vector3 - An offset applied to the Camera's subject position when its CameraSubject
- `Humanoid.CollisionType`: HumanoidCollisionType - Selects the `Enum.HumanoidCollisionType` for R15 and Rthro non-player
- `Humanoid.DisplayDistanceType`: HumanoidDisplayDistanceType - Controls the distance behavior of the humanoid's name and health display.
- `Humanoid.DisplayName`: string - Sets the text of a Humanoid, displayed above their head.
- `Humanoid.EvaluateStateMachine`: boolean - Used to disable the internal physics and state machine of the Humanoid.
- `Humanoid.FloorMaterial`: Material - Describes the `Enum.Material` that the `Class.Humanoid` is currently
- ...and 27 more

**Methods:**
- `Humanoid:AddAccessory` - Attaches the specified `Class.Accessory` to the humanoid's parent.
- `Humanoid:AddCustomStatus` - Adds a custom status to the Humanoid.
- `Humanoid:AddStatus` - Adds a BoolValue to the Humanoid's _Status_ object.
- `Humanoid:ApplyDescriptionAsync` - Makes the character's look match that of the passed in
- `Humanoid:ApplyDescription` - Makes the character's look match that of the passed in
- `Humanoid:ApplyDescriptionResetAsync` - Makes the character's look match that of the passed in
- `Humanoid:ApplyDescriptionReset` - Makes the character's look match that of the passed in
- `Humanoid:BuildRigFromAttachments` - Assembles a tree of `Class.Motor6D` joints by attaching together
- `Humanoid:ChangeState` - Sets the `Class.Humanoid` to enter the given `Enum.HumanoidStateType`.
- `Humanoid:EquipTool` - Makes the `Class.Humanoid` equip the given `Class.Tool`.
- ...and 25 more

**Events:**
- `Humanoid.AnimationPlayed` - Fires when an `Class.AnimationTrack` begins playing on the
- `Humanoid.ApplyDescriptionFinished`
- `Humanoid.Climbing` - Fires when the speed at which a `Class.Humanoid` is climbing changes.
- `Humanoid.CustomStatusAdded` - Fired when a status is added to the Humanoid.
- `Humanoid.CustomStatusRemoved` - Fired when a status is removed from the Humanoid.

---

## HumanoidDescription

Describes the appearance of a Humanoid character including body parts,
accessories, colors, scales, animations, and emotes.

**Properties:**
- `HumanoidDescription.AccessoryBlob`: string - A JSON formatted array of Layered clothing where each table in the entry
- `HumanoidDescription.BackAccessory`: string - A comma-separated list of asset IDs that will be added as
- `HumanoidDescription.BodyTypeScale`: float - Determines the factor by which the shape of a `Class.Humanoid` is
- `HumanoidDescription.ClimbAnimation`: int64 - When this description is `Class.Humanoid:ApplyDescription()|applied` to a
- `HumanoidDescription.DepthScale`: float - Determines by what factor the depth (back-to-front distance) of a
- `HumanoidDescription.Face`: int64 - Determines the asset ID of the Face to be applied to the `Class.Humanoid`.
- `HumanoidDescription.FaceAccessory`: string - A comma-separated list of asset IDs that will be added as
- `HumanoidDescription.FallAnimation`: int64 - When this description is `Class.Humanoid:ApplyDescription()|applied` to a
- `HumanoidDescription.FrontAccessory`: string - A comma-separated list of asset IDs that will be added as
- `HumanoidDescription.GraphicTShirt`: int64 - Determines the `Class.ShirtGraphic.Graphic|Graphic` used by a
- ...and 29 more

**Methods:**
- `HumanoidDescription:AddEmote` - Adds the emote to the description given a name and its asset ID.
- `HumanoidDescription:GetAccessories` - Returns a table of an avatar's current accessories.
- `HumanoidDescription:GetEmotes` - Returns a dictionary of emotes that have been
- `HumanoidDescription:GetEquippedEmotes` - Returns an array of tables describing the equipped emotes that have been
- `HumanoidDescription:RemoveEmote` - Removes any emotes that have been added under the given name.
- `HumanoidDescription:SetAccessories` - Accepts a table that sets the accessories and related properties for an
- `HumanoidDescription:SetEmotes` - Sets all of the emotes on this description.
- `HumanoidDescription:SetEquippedEmotes` - Sets the currently equipped emotes given an array of emote names.

**Events:**
- `HumanoidDescription.EmotesChanged` - Fires when emotes are added, removed or set on this description.
- `HumanoidDescription.EquippedEmotesChanged` - Fires when the equipped emotes are

---

## Accessory

An item that a Character can wear.

**Properties:**
- `Accessory.AccessoryType`: AccessoryType - Specifies the AccessoryType of the Accessory (eg. Hat, Tshirt, Waist).

---

## Shirt

Displays a shirt texture on a `Class.Humanoid` rig.

**Properties:**
- `Shirt.ShirtTemplate`: ContentId - Determines the texture of the `Class.Shirt`.

---

## Pants

Displays a Pants texture from the Roblox website to display on a
`Class.Humanoid` rig.

**Properties:**
- `Pants.PantsTemplate`: ContentId - Determines the texture of the `Class.Pants`.

---

## CharacterMesh

Modifies the appearance of an R6 body part.

**Properties:**
- `CharacterMesh.BaseTextureId`: int64 - The texture of a CharacterMesh. It can be overridden by Shirts, Pants,
- `CharacterMesh.BodyPart`: BodyPart - The part of the Character's body that is affected.
- `CharacterMesh.MeshId`: int64 - Used to load a mesh file, and apply it to the given BodyPart.
- `CharacterMesh.OverlayTextureId`: int64 - The assetId of the overlay texture. The overlay covers Shirts, Pants,

---

