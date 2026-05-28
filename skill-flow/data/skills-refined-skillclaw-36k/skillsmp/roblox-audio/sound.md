# Sound Reference

## Contents
- [Dynamic effects](#dynamic-effects)
- [Sound groups](#sound-groups)
- [Sound](#sound)
- [Sound objects](#sound-objects)

---

## Dynamic effects

<Alert severity = 'warning'>
There is a newer set of audio effects that offer more control and address robust use cases. For more information, see [Audio effects](../audio/effects.md).
</Alert>

Dynamic effects modify or enhance the audio of individual `Class.Sound` objects or an entire `Class.SoundGroup`. You can apply these effects to make your audio more immersive within your experience, such as using `Class.ReverbSoundEffect` in large rooms to make them feel massive.

## Apply dynamic effects

Each dynamic effect you apply has additional properties you can adjust until you achieve the type of sound you desire. For more information on these properties, see each dynamic effect's API page.

To apply a dynamic effect:

1. In the **Explorer** window, insert a new dynamic effect into a `Class.Sound` or `Class.SoundGroup` object.

   1. Hover over the object and click the ⊕ button. A contextual menu displays.
   2. From the menu, insert a **dynamic effect**.

      <img src="../assets/studio/explorer/SoundService-SoundGroup-ReverbSoundEffect.png" width="320" />

2. **(Optional)** In the **Properties** window, select the new dynamic effect and adjust its properties.

   <img src="../assets/audio/sound-groups/Dynamic-Effect-Properties.png" width="320" />

## Types

### Equalizer

The `Class.EqualizerSoundEffect` allows for control of the volume of various frequency ranges. This dynamic effect is useful to highlight or minimize particular elements of audio, such as muffling all audio in your experience when a user goes underwater.

<table>
<tbody>
  <tr>
    <td><audio controls>
<source src="../assets/audio/dynamic-effects/no-effect.mp3" type="audio/mpeg"></source>
</audio></td>
    <td><audio controls>
<source src="../assets/audio/dynamic-effects/equalizer.mp3" type="audio/mpeg"></source>
</audio></td>
  </tr>
  <tr>
    <td>Audio without effect</td>
    <td>Audio with equalizer</td>
  </tr>
</tbody>
</table>

### Compressor

The `Class.CompressorSoundEffect` reduces the

[Content truncated - see full docs]

---

## Sound groups

<Alert severity = 'warning'>
`Class.SoundGroup` objects are now discouraged in favor of the more robust functionality of audio objects. For more information, see [Audio objects](../audio/objects.md).
</Alert>

A `Class.SoundGroup` is an **audio mixer** that groups multiple audio objects, such as `Class.Sound` objects or additional `Class.SoundGroup|SoundGroups`, allowing you to control the volume and dynamic effects properties of multiple audio signals at once. Useful applications include:

- [Assigning audio](#assign-audio-objects-to-sound-groups) to **SoundEffects** and **BackgroundMusic** sound groups so that you can adjust each group's master volume for optimal audio balancing.
- [Nesting sound groups](#nest-sound-groups) into meaningful categories under a mix tree.
- Grouping all sounds that need a specific [dynamic effect](../sound/dynamic-effects.md). For example, you can group all sounds inside a cave to a **Cave** sound group, then apply a `Class.ReverbSoundEffect` to simulate the sounds reflecting off of the cave's environment.

When creating `Class.SoundGroup|SoundGroups`, it's best to keep them all in a single location for organizational purposes as you continue to add and edit audio within your experience. The following example stores the new `Class.SoundGroup` under `Class.SoundService`, as this service determines how `Class.Sound` objects play in experiences.

## Create sound groups

To create a `Class.SoundGroup`:

1. In the **Explorer** window, hover over `Class.SoundService` and click the ⊕ button. A contextual menu displays.
2. From the menu, insert a `Class.SoundGroup`.

   <img src="../assets/studio/explorer/SoundService-SoundGroup.png" width="320" />

3. Triple-click the new sound group and rename it according to its purpose, such as **SoundEffects** or **BackgroundMusic**.

## Assign audio objects to sound groups

`Class.SoundGroup|SoundGroups` don't have the typical parent-child behavior of other forms of object grouping like `Class.Model|Mod

[Content truncated - see full docs]

---

## Sound

<Alert severity = 'warning'>
There is a newer set of [audio objects](../audio/objects.md) and [effects](../audio/effects.md) that offer more control and address robust use cases. For more information, see [Audio](../audio/index.md).
</Alert>

Sound effects and music enhance your experiences and make them more immersive. You can import your own [audio assets](../audio/assets.md) or search for free-to-use audio in the [Creator Store](../production/creator-store.md), play audio through `Class.Sound` or objects, and enhance audio playback through [dynamic effects](#dynamic-effects).

## Sound objects

A [sound object](../sound/objects.md) emits audio within an experience. Roblox assigns each [audio asset](../audio/assets.md) a unique ID that you can assign to `Class.Sound` objects to play a specific sound effect or music track. You can either set this audio to play automatically at runtime, or trigger it to play from scripts.

The location of where you place a `Class.Sound` object in the [Explorer](../studio/explorer.md) hierarchy affects how users hear audio. If you want users to only hear audio near a specific position, you must parent the `Class.Sound` object to a 3D object or `Class.Attachment` to behave as positional audio. If you want users to hear audio regardless of their position, you must insert the `Class.Sound` object directly into `Class.Workspace` or `Class.SoundService` to behave as background audio.

## Sound groups

A [sound group](../sound/groups.md) acts as an audio mixer for multiple audio objects, such as `Class.Sound` objects or additional `Class.SoundGroup|SoundGroups`, allowing you to control the volume and dynamic effects properties of multiple audio signals at once.

## Dynamic effects

[Dynamic effects](../sound/dynamic-effects.md) modify or enhance the audio of individual `Class.Sound` objects or an entire `Class.SoundGroup`. You can apply these effects to make audio more immersive within the experience, such as using `Class.EqualizerSoundEff

[Content truncated - see full docs]

---

## Sound objects

<Alert severity = 'warning'>
There is a newer set of [audio objects](../audio/objects.md) that offer more control and address robust use cases. For more information, see [Audio](../audio/index.md).
</Alert>

Audio playback occurs through `Class.Sound` objects which emit audio within an experience. Roblox assigns each [audio asset](../audio/assets.md) a unique ID that you can assign to `Class.Sound` objects to play a specific sound effect or music track. You can either set this audio to play automatically at runtime, or trigger it to [play from scripts](#script-sound-objects).

To modify playback of multiple `Class.Sound` objects, you can assign them to a [sound group](../sound/groups.md) and control the entire group's volume, as well as apply [dynamic effects](../sound/dynamic-effects.md).

## Create sound objects

There are three locations you can create a `Class.Sound` object, and each location determines how audio emits and volume changes in relation to the user's position within the experience.

<table>
<thead>
  <tr>
    <th>Location</th>
    <th>How audio emits</th>
    <th>How volume changes</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Child of a block, sphere, or cylinder `Class.BasePart`.</td>
    <td>Audio emits outward from the entire surface of the part.</td>
    <td>Volume changes depending on the distance between the user's sound listener and the position of the part, as well as its size.</td>
  </tr>
  <tr>
    <td>Child of an `Class.Attachment`, `Class.MeshPart`, `Class.TrussPart`, `Class.WedgePart`, or `Class.CornerWedgePart`.</td>
    <td>Audio emits outward from the single attachment point or part center.</td>
    <td>Volume changes depending on the distance between the user's sound listener and the attachment/part position.</td>
  </tr>
  <tr>
    <td>Within `Class.SoundService` or `Class.Workspace`.</td>
    <td>Audio emits throughout the experience.</td>
    <td>Volume and pan position remain the same regardless of the user's sound listener pos

[Content truncated - see full docs]

---

