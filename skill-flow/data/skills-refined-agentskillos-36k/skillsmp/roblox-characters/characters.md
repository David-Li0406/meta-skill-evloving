# Characters Reference

## Contents
- [Adaptive Animation](#adaptive-animation)
- [Character appearance](#character-appearance)
- [Emotes](#emotes)
- [Characters](#characters)
- [Character name/health display](#character-name-health-display)
- [Character pathfinding](#character-pathfinding)
- [R6 to R15 Adapter](#r6-to-r15-adapter)

---

## Adaptive Animation

<Alert severity = 'info'>
Adaptive Animation is currently in beta. Enable the beta by navigating to **File** > **Beta Features** and enable **Adaptive Animation**.
</Alert>

Roblox's **Adaptive Animation** system allows animations to play seamlessly between custom characters with unique body types, rigs, and proportions. This feature utilizes a `Class.HumanoidRigDescription` object within your character model that enables you to customize, modify, and map the internal joints of your custom character to enable universal animation support.

After importing an adaptive animation rig, you can access several Studio tools to help you remap your joints and set a baseline t-pose reference to better support animations. After configuring your rig, your custom character can playback any R15 animation, or any animation that has been published from a character with a `Class.HumanoidRigDescription`.

<GridContainer numColumns="2">
  <figure>
  <img src="../assets/avatar/adaptive-animation/Import-Custom-Humanoid.png" />
  <figcaption>Seamlessly import custom characters into Studio as a `Custom Humanoid` rig type.</figcaption>
  </figure>
  <figure>
  <img src="../assets/avatar/adaptive-animation/Assign-Joints-A.png" />
  <figcaption>Modify and adjust the generated `Class.HumanoidRigDescription` to ensure compatibility with universal animations.</figcaption>
  </figure>
</GridContainer>

## Modify custom character rig

The following instructions cover the process to [import](#import-model), [assign joints](#assign-joints), and [pose](#create-t-pose) a custom character using a non-standard Roblox rig. When importing a rig as a `Custom Humanoid`, Studio attempts to automatically configure the model's `Class.HumanoidRigDescription`. Use the joint assignment and t-pose tools to fine-tune or adjust the automated changes.

You can follow along this process with your own custom character, or the same [reference character](../assets/art/reference-files/Snow.fbx) used in this guide.

<Alert

[Content truncated - see full docs]

---

## Character appearance

Most experiences let players use their own Roblox avatar, although some implement an in-experience customization system like the [UGC Homestore](/resources/templates.md#ugc-homestore) template. Other experiences make limited [modifications](../characters/appearance.md) to player avatars such as helmets, wings, or accessories that match the genre.

To create a unique experience that alters the appearance of your users, you can customize the default character properties through [avatar settings](#global-avatar-settings) or a [manually modify appearance](#manually-modify-appearance).

## Global avatar settings

Studio's **File**&nbsp;⟩ **Avatar Settings** allows you to quickly set several global player character properties in your experience. These settings apply globally to all player character models joining your experience. To modify specific characters, such as non-player character models, see [manually modify appearance](#manually-modify-appearance).

In this window, you can set various presets for clothing, accessories, body parts, collision behavior, animations and more. When editing these settings, a preview of the applied settings displays in the workspace.

For more information, see [Avatar Settings](../studio/avatar-settings.md).

## Manually modify appearance

Character models contain a `Class.Humanoid` object that gives the model special characteristics, such as walking, jumping, equipping items, and interacting with the environment.

You can programmatically modify a `Class.Humanoid` by updating `Class.HumanoidDescription`. This includes player character models or non-player character models in your experience.

You can adjust the following character properties in your experience using `Class.HumanoidDescription`:

<table>
<thead>
  <tr>
    <th>Character property</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Scale</td>
    <td>Number values for physical traits `Class.HumanoidDescription.HeightScale|height`, `Class.HumanoidDescript

[Content truncated - see full docs]

---

## Emotes

Emotes are expressive character [animations](../animation/index.md) that are accessible by using chat commands ("/e cheer") or by accessing the **emotes menu** on the top right of any experience. All users have access to default emotes, such as **dance**, **point**, and **cheer**. Additional avatar emotes can be purchased and equipped from the [Marketplace](https://www.roblox.com/catalog).

<video src="../assets/avatar/avatar-emotes/Avatar-Emotes.mp4" controls width="100%"></video>

In your experience, you can perform the following emote customizations:

- [Open and close](#open-and-close) a user's emotes menu programmatically.
- [Add or remove](#add-and-remove-emotes) emotes options from a user's menu.
- [Disable](#disable) access to the menu.
- [Play](#play-emotes) an emote, targeting a specific user character.

## Emotes menu

You can open and close a user's emote menu manually, customize the menu to display specific emotes, or disable the menu completely.

### Open and close

To manually open or close a player's emote menu, call `Class.GuiService:SetEmotesMenuOpen()` with a boolean value of true or false.

The following code sample will open the emotes menu for the user:

```lua
-- Open the emote Menu
local GuiService = game:GetService("GuiService")
GuiService:SetEmotesMenuOpen(true)
```

If you need to detect whether the emotes menu is open, call `Class.GuiService:GetEmotesMenuOpen()`. This returns a boolean indicating the menu's current state.

### Add and remove emotes

Customize the emote menu by setting emotes from the catalog and then equipping emotes to a `Class.Humanoid`. Set emotes with the `Class.HumanoidDescription:SetEmotes()` method and equip up to 8 emotes to the emotes menu using `Class.HumanoidDescription:SetEquippedEmotes()`.

Use the following code sample in a `Class.LocalScript` within the `Class.StarterCharacterScripts` folder to set and equip emotes in your experience:

```lua
local Players = game:GetService("Players")
local humanoid = Playe

[Content truncated - see full docs]

---

## Characters

**Characters** typically refer to any `Class.Model` objects that interact with the world or other users. While a character can be as simple as a glowing sphere that communicates and interacts with users, characters are often human-like models with additional means of expression to encourage immersion and realism.

Characters can range between **basic** characters, such as a simple non-player character (NPC), or **avatar** characters, which are user-controlled models that include advanced features for movement, animation, and cosmetics.

All Roblox users are associated with an account-based avatar character. Along with this avatar character, Roblox represents users as **players** in the data model, giving developers access to additional character customization properties, social features, and relevant gameplay and account information. For more information on account specific player features, see [Players](../players/index.md).

## Basic characters

Basic characters are often used as NPCs and typically perform one or two simple tasks. A common component of basic characters include a display name, health, and basic movement.

You can use the following components within your `Class.Model` object to enable these basic features:

- A group of parts, or [assembly](../physics/assemblies.md), that includes the following:
  - A collection with the name `HumanoidRootPart` to indicate the root part of the assembly.
  - A part with the name `Head` to display a display name over.
  - Additional parts that make up the cosmetic individual body parts, which commonly include the 6 (R6) or 15 (R15) body parts used for human-like models.
  - Joints, such as `Class.Bone` or `Class.Motor6D`, that connects each body part as an assembly.
- A `Class.Humanoid` instance to quickly add common character properties to a model.

<GridContainer numColumns="2">
  <figure>
    <img src="../assets/avatar/character-customization/R6-Example.jpg" />
    <figcaption>Basic Character Example (R6)</figcapti

[Content truncated - see full docs]

---

## Character name/health display

The `Class.Humanoid` instance is used to create character models, both for user avatars and NPCs. When a `Class.Humanoid` is present inside a `Class.Model` that contains a part named **Head**, Roblox displays a name and/or health bar above that part.

<img src="../assets/avatar/name-health-display/Display-Indicated.jpg" width="800" alt="Character display information above an in-experience avatar" />

Through various `Class.Humanoid` properties, you can modify the following:

- The [distance](#display-distance-type) from which users can see the name/health of other humanoids in relation to their own character's humanoid.
- The [display name](#override-display-names) which shows over a humanoid.
- Whether a humanoid's [health bar](#health-display-type) always appears, never appears, or only appears when the humanoid is damaged.
- Whether names and health bars are [occluded](#occlusion) (hidden) when line-of-sight between the camera and another humanoid is blocked.

<Alert severity="warning">
As noted in the introduction, character name/health display requires that the `Class.Humanoid` instance is inside a `Class.Model` and that the model contains a `Class.BasePart` named **Head**. Both objects must also be at the same level in the model's hierarchy.
</Alert>

## Display properties

### Display distance type

The `Class.Humanoid.DisplayDistanceType` property sets how users see the name/health of other characters in relation to their own character.

#### Viewer

When a humanoid's `Class.Humanoid.DisplayDistanceType|DisplayDistanceType` is set to `Enum.HumanoidDisplayDistanceType|HumanoidDisplayDistanceType.Viewer`, it sees the name/health of other humanoids within range of its own `Class.Humanoid.NameDisplayDistance|NameDisplayDistance` and `Class.Humanoid.HealthDisplayDistance|HealthDisplayDistance`. You can consider this the lowest priority since it is not taken into account for other humanoids configured as [subject](#subject) or [none](#none).

In the following scen

[Content truncated - see full docs]

---

## Character pathfinding

**Pathfinding** is the process of moving a character along a logical path to reach a destination, avoiding obstacles and (optionally) hazardous materials or defined regions.

<video controls src="../assets/avatar/pathfinding/Showcase.mp4" width="100%" alt="Video showcase of character pathfinding across a series of bridges"></video>

## Navigation visualization

To assist with pathfinding layout and debugging, Studio can render a navigation mesh and [modifier](#pathfinding-modifiers) labels. To enable them, toggle on **Navigation&nbsp;mesh** and **Pathfinding&nbsp;modifiers** from the [Visualization&nbsp;Options](../studio/ui-overview.md#visualization-options) widget in the upper‑right corner of the 3D viewport.

<img src="../assets/studio/general/Visualization-Options.png" width="780" alt="A close up view of the 3D viewport with the Visualization Options button indicated in the upper-right corner." />

With **Navigation mesh** enabled, colored areas show where a character might walk or swim, while non-colored areas are blocked. The small arrows indicate areas that a character will attempt to reach by jumping, assuming you set `AgentCanJump` to `true` when [creating the path](#create-paths).

<img src="../assets/avatar/pathfinding/Navigation-Mesh.jpg" width="800" alt="Navigation mesh showing in Studio" />

With **Pathfinding modifiers** enabled, text labels indicate specific materials and regions that are taken into consideration when using [pathfinding modifiers](#pathfinding-modifiers).

<img src="../assets/avatar/pathfinding/Navigation-Labels.jpg" width="800" alt="Navigation labels showing on navigation mesh" />

## Known limitations

Pathfinding features specific limitations to ensure efficient processing and optimal performance.

### Vertical placement limit

Pathfinding calculations consider only parts within certain vertical boundaries:

- Lower Boundary &mdash; Parts with a bottom **Y** coordinate less than -65,536 studs are ignored.
- Upper Boundary &mdash; 

[Content truncated - see full docs]

---

## R6 to R15 Adapter

<Alert severity = 'warning'>
This feature is only applicable to developers who manage an active experience with **R6** avatar characters enabled.
</Alert>

The **R6 to R15 Adapter** allows R15 avatars to join your R6 experience. All avatars in the experience will still use the R6-like scale and movement systems. The adapter allows your experience to take advantage of modern R15 components, such as layered clothing and animatable heads, with minimal performance or gameplay impact to your experience.

It's important to understand how the adapter uses [adapter parts](#adapter-parts) and review the feature's [known limitations](#known-limitations) before [enabling](#enable-the-r6-to-r15-adapter) and testing the adapter for your experience.

## Adapter parts

The R6 to R15 Adapter implements a Luau script injection when an avatar spawns that creates adapter parts.

These are invisible `Class.MeshPart|MeshParts` that have the exact same name as R6 body parts and are welded to their corresponding R15 body parts. The scripts allow adapter parts to accept R6-based script interactions and forward them to the appropriate R15 parts.

The adapter parts perform the following:

- Emulates R6 physics using extra invisible collideable parts with the positions and dimensions of R6 hitboxes.
- Sets the visible R15 body parts as non-collideable.
- Scales and positions the visible R15 parts to match the R6 size and joint positions.
- Acts as a shim between R6 and R15 body parts. Property changes applied to the invisible R6 parts are passed along to their corresponding visible R15 parts.
  - For example, a color change in R6 `LeftArm` is passed to the R15 `LeftUpperArm`, `LeftLowerArm` and `LeftHand` parts.

## Enable the R6 to R15 Adapter

You can enable the R6 to R15 Adapter by setting the `Class.Workspace.AvatarUnificationMode|AvatarUnificationMode` property in `Class.Workspace`. You can only access this property if **Avatar Type** is set to `R6` in Studio's **File**&nbsp;⟩ **Game Set

[Content truncated - see full docs]

---

