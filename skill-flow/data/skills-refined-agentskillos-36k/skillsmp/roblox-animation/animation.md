# Animation Reference

## Contents
- [Animation capture](#animation-capture)
- [Curve Editor](#curve-editor)
- [Animation Editor](#animation-editor)
- [Animation events](#animation-events)
- [Animation in Roblox](#animation-in-roblox)
- [Inverse Kinematics](#inverse-kinematics)
- [Use animations](#use-animations)

---

## Animation capture

import BetaAlert from '../includes/beta-features/beta-alert.md'

You can record or upload video content to the [Animation Editor](../animation/editor.md) to quickly capture movement and expressions as animation keyframes. These tools can create unique and realistic animations within minutes while providing access to the animation keyframes for additional adjustments.

The animation capture tools allow you to:

- [Record your face](#face) with a webcam to puppeteer characters with [animation compatible heads](../art/characters/facial-animation/index.md).
- [Upload full-body video content](#body) to generate high quality realistic animations for an entire character.

## Face

**Animation Capture - Face** allows you to use your webcam to puppeteer rigs with [animation compatible heads](../art/characters/facial-animation/index.md) and generate corresponding keyframes to your movement. With the ability to record up to 60‑second animations, you can quickly provide both your playable and nonplayable characters the means to realistically grin, raise their eyebrows, drop their jaw, or any other expression necessary for your experience.

<BetaAlert betaName="Face Capture" leadIn="To ensure that you're able to utilize your camera to record and create facial animations, you must first enable the beta feature through " leadOut="." components={props.components} />

Before you begin to record your face, ensure that you're in a well lit room close enough to your camera so that your face is in the center of your camera's recording frame. This increases your camera's ability to distinguish you from your surroundings so that you can accurately puppeteer your avatar and create high-quality animations.

1. From the toolbar's **Avatar** tab, click **Animation**. The [Animation Editor](../animation/editor.md) window displays.
2. In the 3D viewport or the [Explorer](../studio/explorer.md) hierarchy, select the rig you want your video to animate. Enter a new animation name in the dialog win

[Content truncated - see full docs]

---

## Curve Editor

The **Curve Editor** is a curve-based animation editing interface within the [Animation Editor](../animation/editor.md) that allows you to see and modify how a rig's position and orientation changes between keyframes through color‑coded curve graphs. It allows you to define independent tracks for the **X**, **Y** and **Z** angles, providing additional levels of control to make your animations more fluid and realistic.

<GridContainer numColumns="2">
  <figure>
    <img src="../assets/animation/curve-editor/Dope-Sheet-Editor.png" />
    <figcaption>Dope Sheet Editor</figcaption>
  </figure>
  <figure>
    <img src="../assets/animation/curve-editor/Curve-Editor-Example.png" />
    <figcaption>Curve Editor</figcaption>
  </figure>
</GridContainer>

Instead of using the default dope sheet editor's method of manually moving the scrubber from one frame to another to see how a rig's position and orientation change over time, the Curve Editor lets you quickly reference position and orientation values of your selected tracks through the **position ruler** on the left side of the timeline and the **rotation ruler** on the right side of the timeline.

<img
  alt="Curve Editor Overview"
  src="../assets/animation/curve-editor/UI-Overview.png"
  width="780" />

## Open the Curve Editor

You can switch the editor's timeline between the dope sheet editor and the Curve Editor at any time.

1. Open the [Animation Editor](./editor.md) from Studio's **Avatar** tab or the **Window**&nbsp;⟩ **Avatar** menu.

   <img src="../assets/studio/general/Toolbar-Animation.png" width="800" alt="Animation Editor indicated in Studio's toolbar" />

2. <Chip label="IMPORTANT" size="small" variant="outlined" color="warning" /> Studio automatically converts [quaternions](https://en.wikipedia.org/wiki/Quaternion) to [Euler angles](https://en.wikipedia.org/wiki/Euler_angles) when you open the Curve Editor, so it's important that you verify your rotation type **before** you switch to the Curve Editor. Onc

[Content truncated - see full docs]

---

## Animation Editor

The **Animation Editor**, accessible from Studio's **Avatar** tab or **Window**&nbsp;⟩ **Avatar** menu, allows you to design and publish custom animations on rigs. A rig is an object with individual sections connected by joints. You can move these joints to [create poses](#create-poses) and then smoothly animate the rig from pose to pose.

<img src="../assets/studio/general/Toolbar-Animation.png" width="800" alt="Animation Editor indicated in Studio's toolbar" />

## Interface

<img src="../assets/animation/animation-editor/Editor-Sections-Labeled.png"
   width="80%" />

### Media and playback controls

<table>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-Animation-Name.png"
   width="100%" /></td>
    <td>The name of the animation.</td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-File-Menu.png"
   width="100%" /></td>
    <td>
      Opens a contextual menu with the following menu items:
      <ul>
        <li>**Load**</li>
        <li>**Save**</li>
        <li>**Save As**</li>
        <li>**Import**</li>
        <li>**Export**</li>
        <li>**Create New**</li>
        <li>**Set Animation Priority**</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-First-Key.png"
   width="100%" /></td>
    <td>Moves the scrubber to the first key.</td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-Previous-Key.png"
   width="100%" /></td>
    <td>Moves the scrubber to the previous key.</td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-Preview-Reverse.png"
   width="100%" /></td>
    <td>Previews the animation in reverse.</td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-Pause.png"
   width="100%" /></td>
    <td>Pauses the animation.</td>
  </tr>
  <tr>
    <td><img src="../assets/animation/animation-editor/Controls-Preview.png"
   width="100%" /></td>
    <td>Previ

[Content truncated - see full docs]

---

## Animation events

You can define animation **event markers** across the timeline span and use
`Class.AnimationTrack:GetMarkerReachedSignal()|GetMarkerReachedSignal()`
to detect those markers as the animation runs.

## Show events

By default, the event track isn't visible. To show the event track:

1. Navigate to the right of the **timeline**, then click the **Gear** icon.
   A pop-up menu displays.

   <img
   src="../assets/animation/animation-editor/Timeline-Options-Menu.png"
   width="330" />

2. Select **Show Animation Events**. This opens the **Animation Events** bar directly below the media and
   playback controls.

   <img
   src="../assets/animation/animation-editor/Animation-Events-Bar.png"
   width="600" />

You can now [create](#create-events), [detect](#detect-events), and
[duplicate](#duplicate-events) events.

## Create events

Event markers are visual indicators of where an animation event begins. After you create an event
marker, you can move it to any frame position on the timeline.

To create a new event marker:

1. Navigate to the **timeline**, then click-and-drag the **scrubber** to the
   frame position where the event should occur.
2. Navigate to the **event track**, then click the **Edit Animation Events**
   button. The **Edit Animation Events** dialog displays.

   <img
   src="../assets/animation/animation-editor/Animation-Events-Edit-Button.png"
   width="600" />

3. In the **Edit Animation Events** dialog, click **+ Add Event**, then enter an
   event name.

   <img
   src="../assets/animation/animation-editor/Animation-Events-Add-Event.png"
   width="507" />

4. **(Optional)** In the **Parameter** field, enter a parameter string for the event.
5. Click the **Save** button. In the events bar within the timeline, a new
   marker symbol displays at the frame position.

   <img
   src="../assets/animation/animation-editor/Animation-Events-Marker-In-Timeline.png"
   width="700" />

## Detect events

To detect animation events in a `Class.LocalScript`,
connec

[Content truncated - see full docs]

---

## Animation in Roblox

**Animation** is the process of applying motion to your characters, objects, and environments to create an engaging and dynamic experience. While there are many ways to make objects move and interact, animation in Roblox typically refers to customizing an expressive movement of a specific character, or group of parts, using the **Animation Editor** or **animation-related APIs**.

Animation can apply to any Roblox part or group of parts. Different types of objects can utilize various animation features. The following are the general categories of animatable objects:

- **Simple objects**, such as a basic part, can only animate changes across the part's single position or rotation property.
- **Rigs**, or parts connected by joints like `Class.Bone` or `Class.Motor6D`, can articulate positional and rotational movement between their joints, like elbows and wrists. Rigged models can take advantage of animation features like [inverse kinematics](#inverse-kinematics) to quickly and programmatically apply movement in response to environments and events.
- **R15 rigs**, rigs that incorporate the standardized [avatar character model](../characters/index.md#avatar-character-components), can use animations from Roblox's character animation library and other movement features, even if it's a player or non-player character model.

## Animation Editor

The [Animation Editor](../animation/editor.md) allows you to design and publish custom animations on rigs. You can move the joints that connect individual sections of a rig to create poses, and the **Animation Editor** smoothly animates the rig from pose-to-pose. As long as all moving parts are connected with `Class.Motor6D` objects, you can use the editor for both human and non-human rigs.

<video src="../assets/animation/inverse-kinematics/IK-Body-Part.mp4" controls width="80%"></video>

When creating animations, Studio provides the following features to animate effectively:

- Instantly create face and body animations through the

[Content truncated - see full docs]

---

## Inverse Kinematics

[Inverse Kinematics](https://en.wikipedia.org/wiki/Inverse_kinematics) (IK) is a common technique in computer animation to efficiently make characters move and interact realistically with their environment. The process of creating a realistic movement for a character often requires many iterations and minor adjustments of the various joints. With IK, you can pose and animate multiple character parts by posing or adjusting a single object.

This animation technique can provide solutions to the following examples:

<GridContainer numColumns="3">
	<figure>
		<video controls src="../assets/animation/inverse-kinematics/IK-Place-Hand.mp4" width="90%"></video>
		<figcaption>Grab and pose a character's hand while automatically adjusting the related limbs, such as the wrist, elbow, and shoulder.</figcaption>
	</figure>
	<figure>
		<video controls src="../assets/animation/inverse-kinematics/IK-Uneven-Surfaces.mp4" width="90%"></video>
		<figcaption>Make a character's feet interact realistically on different surfaces and slopes.</figcaption>
	</figure>
   <figure>
		<video controls src="../assets/animation/inverse-kinematics/IK-Drag-Accessory.mp4" width="90%"></video>
		<figcaption>Grab and move a single target object to quickly create realistic interactions with your character and props.</figcaption>
	</figure>
</GridContainer>

## IKControl

You can use an `Class.IKControl` to procedurally add IK to your character rigs outside of the **Animation Editor**. Studio allows you to programmatically apply IK to all characters, such as R15, Rthro, and custom imported skinned characters, to create realistic movement and interactions in your experience.

When adding an `Class.IKControl`, set the [required properties](#required-properties) correctly to avoid unexpected and unnatural animation results. As with all animation, [test your IKControls](#test-ikcontrols) to ensure that you achieve the desired behavior.

### Required properties

When adding a `Class.IKControl` to your characte

[Content truncated - see full docs]

---

## Use animations

Once you have [created an animation](../animation/editor.md), you need to use scripts to include them in your experience. You can either [play animations manually](#play-animations-from-scripts) from scripts or [replace default animations](#replace-default-animations) for player characters.

## Play animations from scripts

In some cases, you'll need to play an animation directly from inside a script, such as when a user presses a certain key or picks up a special item.

### Humanoids

To play an animation on a rig containing a `Class.Humanoid`
object, such as typical playable characters, follow this basic pattern:

1. Ensure that the local player's `Class.Humanoid` contains an `Class.Animator` object.
2. Create a new `Class.Animation` instance with the proper `Class.Animation.AnimationId|AnimationId`.
3. Load the animation via `Class.Animator:LoadAnimation()` to create an `Class.AnimationTrack`.
4. Play the track with `Class.AnimationTrack:Play()`.

For example, the following `Class.LocalScript`, when placed in
`Class.StarterPlayerScripts`, loads a "kick" animation onto the player's character and plays it. The script also utilizes the `Class.AnimationTrack:GetMarkerReachedSignal()|GetMarkerReachedSignal()` method to detect when a specific [animation event](../animation/events.md) occurs.

```lua title="LocalScript - Play Custom Animation on Player Character"
local Players = game:GetService("Players")

local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()

-- Ensure that the character's humanoid contains an "Animator" object
local humanoid = character:WaitForChild("Humanoid")
local animator = humanoid:WaitForChild("Animator")

-- Create a new "Animation" instance and assign an animation asset ID
local kickAnimation = Instance.new("Animation")
kickAnimation.AnimationId = "rbxassetid://2515090838"

-- Load the animation onto the animator
local kickAnimationTrack = animator:LoadAnimation(kickAnimation)

-- If a named even

[Content truncated - see full docs]

---

