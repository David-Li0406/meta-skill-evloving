# Sound Classes

## Contents
- [Sound](#sound)
- [SoundGroup](#soundgroup)
- [SoundEffect](#soundeffect)
- [DistortionSoundEffect](#distortionsoundeffect)
- [ReverbSoundEffect](#reverbsoundeffect)

---

## Sound

An object that emits sound. This object can be placed within a
`Class.BasePart` or `Class.Attachment` to emit a sound from a particular
position within a place or world, or it can be attached elsewhere to play the
sound at a constant volume throughout the entire place.

**Properties:**
- `Sound.AudioContent`: Content
- `Sound.ChannelCount`: int
- `Sound.EmitterSize`: float - The minimum distance, in studs, at which a 3D `Class.Sound` (direct child
- `Sound.IsLoaded`: boolean - This property is `true` when the `Class.Sound` has loaded from Roblox
- `Sound.IsMutedForCapture`: boolean
- `Sound.IsPaused`: boolean - Read-only property which returns `true` when the `Class.Sound` is not
- `Sound.IsPlaying`: boolean - Read-only property which returns `true` when the `Class.Sound` is playing.
- `Sound.isPlaying`: boolean
- `Sound.Looped`: boolean - Sets whether or not the `Class.Sound` repeats once it has finished
- `Sound.LoopRegion`: NumberRange - A range denoting a desired loop start and loop end within the
- ...and 17 more

**Methods:**
- `Sound:Pause` - Pauses playback of the `Class.Sound` if it is playing.
- `Sound:pause`
- `Sound:Play` - Plays the `Class.Sound`.
- `Sound:play`
- `Sound:Resume` - Resumes the `Class.Sound`.
- `Sound:Stop` - Stops the `Class.Sound`.
- `Sound:stop`

**Events:**
- `Sound.DidLoop` - Fires whenever the `Class.Sound` loops.
- `Sound.Ended` - Fires when the `Class.Sound` has completed playback and stopped.
- `Sound.Loaded` - Fires when the `Class.Sound` is loaded.
- `Sound.Paused` - Fires whenever the `Class.Sound` is paused using
- `Sound.Played` - Fires whenever the `Class.Sound` is played using

---

## SoundGroup

A `Class.SoundGroup` is used to manage the volume and sound effects on
multiple `Class.Sound|Sounds` at once. `Class.Sound|Sounds` in the SoundGroup
will have their volume and effects adjusted by the SoundGroup.

**Properties:**
- `SoundGroup.Volume`: float - The volume multiplier applied to `Class.Sound|Sounds` that are in the

---

## SoundEffect

SoundEffect is the base class that all other sound effects derive from. A
SoundEffect can be applied to either a `Class.Sound` or `Class.SoundGroup` by
being parented to either.

**Properties:**
- `SoundEffect.Enabled`: boolean - Toggles the effect on and off.
- `SoundEffect.Priority`: int - Determines the order the effect will be applied in relation to other

---

## DistortionSoundEffect

Distorts audio, making it sound fuzzier and overdriven.

**Properties:**
- `DistortionSoundEffect.Level`: float - The intensity of the effect.

---

## ReverbSoundEffect

Reverberates audio, simulating the effect of bouncing off walls in a room.

**Properties:**
- `ReverbSoundEffect.DecayTime`: float - Sets how long it takes for the reverberating echoes to fade out
- `ReverbSoundEffect.Density`: float - Controls how many reflections are generated.
- `ReverbSoundEffect.Diffusion`: float - Controls how smooth and reflective the simulated surfaces are.
- `ReverbSoundEffect.DryLevel`: float - The output volume of the original sound.
- `ReverbSoundEffect.WetLevel`: float - The output volume of the echoed effect.

---

