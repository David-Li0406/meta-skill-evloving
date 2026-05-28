# Audio Reference

## Contents
- [Audio assets](#audio-assets)
- [Audio effects](#audio-effects)
- [Audio](#audio)
- [Audio objects](#audio-objects)

---

## Audio assets

You can [find](#find-audio) a wide variety of free‑to‑use audio assets in the Creator Store, or you can [import](#import-audio) audio assets that you're certain you have permission to use, such as audio that you make yourself. The [asset privacy](../projects/assets/privacy.md) system automatically ensures that the IDs of your imported audio can't be accessed by users without proper permissions.

## Find audio

The [Creator Store](../production/creator-store.md) tab of the [Toolbox](../projects/assets/toolbox.md) contains a wide variety of free-to-use audio assets made by Roblox and the Roblox community for creators to use within their experiences, including more than 100,000 professionally-produced sound effects and music tracks from top audio and music partners.

To find audio assets on the Creator Store:

1. In the **Toolbox**, navigate to the **Creator Store** tab, then use the category selector dropdown to select **Audio**.

   <img src="../assets/studio/toolbox/Creator-Store-Audio.png" width="360" alt="Audio section of Creator Store in Studio's Toolbox" />

2. Use the keyword search, quick filter options, and/or advanced filters to narrow down the results.

   <img src="../assets/studio/toolbox/Creator-Store-Audio-Discovery.png" width="580" alt="Audio discovery options in Studio's Toolbox" />

3. Right-click any audio asset, then select **Copy Asset ID** to copy the asset ID to your clipboard. You can now paste this asset ID into a `Class.AudioPlayer` object to [play the audio](../audio/objects.md).

<Alert severity="warning">
  If you click any audio asset, Studio inserts it as a new `Class.Sound` instance into the **Explorer** window. However, `Class.Sound` objects don't have the same dynamic functionality as `Class.AudioPlayer` objects.
</Alert>

## Import audio

You can import custom audio through the [Asset Manager](../projects/assets/manager.md), Creator Dashboard, and Open Cloud API as long as your audio meets the following requirements:

- You have the 

[Content truncated - see full docs]

---

## Audio effects

Audio effects non-destructively modify or enhance audio streams. You can apply these effects to make your audio more immersive within your experience, such as using an `Class.AudioEqualizer` object to make rain sound muffled, `Class.AudioCompressor` object to control a sound's maximum volume, or `Class.AudioReverb` to add more realistic reflections of sound in interior spaces.

## Apply audio effects

You can apply audio effects to your audio streams by wiring up the effect within your 2D audio or 3D audio setup before it reaches the player's ears. For example, to review the setup instructions in [Audio objects](../audio/objects.md#2d-audio), 2D audio requires an audio player to produce the stream, a physical hardware device like a speaker or headphones, and a wire to carry the audio stream from the audio player to the output device.

<img src="../assets/audio/audio-objects/2D-Audio-Diagram.png" width="100%" />

If you keep this setup the way it is, the audio stream from the asset ID plays as it was originally recorded. However, if you want to apply an audio effect to this audio stream, you must introduce the audio effect in the middle of the configuration so that the audio stream transmits through the effect before it transmits to the output device.

<img src="../assets/audio/effects/AudioEffect-Single.png" width="100%" />

Roblox's modular audio objects also allow you to wire multiple audio players through an audio effect, meaning that you don't have to have multiple audio effect objects with the same settings. This provides a lot of flexibility in how you customize multiple audio sources at once.

<img src="../assets/audio/effects/AudioEffect-Multiple.png" width="100%" />

In addition, you can apply multiple audio effects to the same audio stream to further customize your audio. As the audio stream transmits from the audio player to the device output, it's important to note that the order of the audio effects impacts the custom sound. For example, if you were to 

[Content truncated - see full docs]

---

## Audio

Adding audio to your experiences is crucial for elevating your experiences to new heights. By strategically using positional and non-positional audio, you can immerse players into your worlds, provide them useful feedback for their actions, and direct their attention to what they need to do to be successful in their objectives.

## Audio assets

You can import [audio assets](../audio/assets.md) that you're certain you have permission to use, such as audio that you make yourself. However, Roblox's [Creator Store](../production/creator-store.md) provides you a wide variety of free-to-use audio assets, including more than 100,000 professionally-produced sound effects and music tracks from top audio and music partners.

## Audio objects

Roblox offers many different types of [audio objects](../audio/objects.md) that you can use to play and modify your audio until it meets your experience's design requirements:

- The `Class.AudioPlayer` object loads and plays the **audio file** using a set [audio asset ID](../audio/assets.md).
- The `Class.AudioEmitter` object is a **virtual speaker** that emits audio into the 3D environment.
- The `Class.AudioListener` object is a **virtual microphone** that picks up audio from the 3D environment.
- The `Class.AudioDeviceOutput` object is a **physical hardware device** within the real world, such as a speaker or headphones.
- The `Class.AudioDeviceInput` object is a **physical microphone** within the real world.
- The `Class.AudioTextToSpeech` object converts **text to audio** using an artificial voice.
- The `Class.AudioSpeechToText` object converts **audio to text**.
- `Class.Wire|Wires` carry audio streams from one object to another.

Using these objects, you can either set audio to play automatically at runtime, or trigger it to play from scripts. For practical applications of these audio objects, see the [Add 2D audio](../tutorials/use-case-tutorials/audio/add-2D-audio.md), [Add 3D audio](../tutorials/use-case-tutorials/audio/add-

[Content truncated - see full docs]

---

## Audio objects

Roblox's modular audio objects allow you to have dynamic control over sound and voice chat in your experiences. Almost every audio object corresponds to a real-world audio device, and they all function together to capture and play audio like their physical counterparts.

For example, every audio object conceptually falls into the following categories:

- Objects that **produce** audio streams, such as audio players.
- Objects that **consume** audio streams, such as audio emitters.
- Objects that **modify** audio streams, such as audio effects.
- Objects that **carry** audio streams from one audio object to another, such as wires.

As you read through this guide and learn about how all of these audio objects work together to emit sound, you will learn how to accurately capture and feed music, sound effects, and the human voice from the experience to the player and vice-versa.

<Alert severity = 'info'>
`Class.Sound`, `Class.SoundGroup`, and `Class.SoundEffect` objects are now discouraged in favor of the more robust functionality of audio objects.
</Alert>

## Play audio

To play audio within your experience, it's important to understand the role of each available audio object:

- An `Class.AudioPlayer` loads and plays the **audio file** using a set audio asset ID.
- An `Class.AudioEmitter` is a **virtual speaker** that emits audio into the 3D environment.
- An `Class.AudioListener` is a **virtual microphone** that picks up audio from the 3D environment.
- An `Class.AudioDeviceOutput` is a **physical hardware device** within the real world, such as a speaker or headphones.
- An `Class.AudioDeviceInput` is a **physical microphone** within the real world.
- The `Class.AudioTextToSpeech` object converts **text to audio** using an artificial human voice.
- The `Class.AudioSpeechToText` object converts **spoken audio to text**.
- A `Class.Wire` **carries audio streams** from one audio object to another.

How you pair these audio objects together depends on if you want to e

[Content truncated - see full docs]

---

