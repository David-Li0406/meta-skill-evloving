# Animation Classes

## Contents
- [Animation](#animation)
- [AnimationController](#animationcontroller)
- [Animator](#animator)
- [AnimationTrack](#animationtrack)
- [Keyframe](#keyframe)

---

## Animation

References an animation asset which can be loaded by an
`Class.AnimationController`.

**Properties:**
- `Animation.AnimationId`: ContentId - Asset ID of the animation an `Class.Animation` object is referencing.

---

## AnimationController

Allows animations to be loaded and applied to a character or model in place of
a `Class.Humanoid`.

**Methods:**
- `AnimationController:GetPlayingAnimationTracks` - Returns an array of all `Class.AnimationTrack|AnimationTracks` that are
- `AnimationController:LoadAnimation` - Loads an `Class.Animation` onto an `Class.AnimationController`, returning

**Events:**
- `AnimationController.AnimationPlayed` - Fires whenever the `Class.AnimationController` begins playing an

---

## Animator

Responsible for the playback and replication of `Class.Animation|Animations`.

**Properties:**
- `Animator.EvaluationThrottled`: boolean
- `Animator.PreferLodEnabled`: boolean
- `Animator.RootMotion`: CFrame
- `Animator.RootMotionWeight`: float

**Methods:**
- `Animator:ApplyJointVelocities` - Computes relative velocities between parts and apply them to
- `Animator:GetPlayingAnimationTracks` - Returns the list of currently playing
- `Animator:LoadAnimation` - Loads an `Class.Animation` onto an `Class.Animator`, returning an
- `Animator:RegisterEvaluationParallelCallback`
- `Animator:StepAnimations` - Increments the `Class.AnimationTrack.TimePosition` of all playing

**Events:**
- `Animator.AnimationPlayed` - Fires when the Animator starts playing an AnimationTrack.

---

## AnimationTrack

Controls the playback of an animation on an `Class.Animator`.

**Properties:**
- `AnimationTrack.Animation`: Animation - The `Class.Animation` object that was used to create this
- `AnimationTrack.IsPlaying`: boolean - A read-only property that returns true when the `Class.AnimationTrack` is
- `AnimationTrack.Length`: float - A read-only property that returns the length (in seconds) of an
- `AnimationTrack.Looped`: boolean - Sets whether the animation will repeat after finishing. If it is changed
- `AnimationTrack.Priority`: AnimationPriority - Sets the priority of an `Class.AnimationTrack`. Depending on what this is
- `AnimationTrack.Speed`: float - Read-only property that gives the current playback speed of the
- `AnimationTrack.TimePosition`: float - Returns the position in time in seconds that an `Class.AnimationTrack` is
- `AnimationTrack.WeightCurrent`: float - Read-only property that gives the current weight of the
- `AnimationTrack.WeightTarget`: float - Read-only property that gives the current weight of the

**Methods:**
- `AnimationTrack:AdjustSpeed` - Changes the `Class.AnimationTrack.Speed` of an animation. A positive value
- `AnimationTrack:AdjustWeight` - Changes the weight of an animation, with the optional `fadeTime` parameter
- `AnimationTrack:GetMarkerReachedSignal` - Returns an `Datatype.RBXScriptSignal` (event) that fires when a specified
- `AnimationTrack:GetParameter`
- `AnimationTrack:GetParameterDefaults`
- `AnimationTrack:GetTargetInstance`
- `AnimationTrack:GetTargetNames`
- `AnimationTrack:GetTimeOfKeyframe` - Returns the time position of the first `Class.Keyframe` of the given name
- `AnimationTrack:Play` - Plays the `Class.AnimationTrack`. Once called an `Class.AnimationTrack`
- `AnimationTrack:SetParameter`
- ...and 2 more

**Events:**
- `AnimationTrack.DidLoop` - Fires when an `Class.AnimationTrack` loops on the next update following
- `AnimationTrack.Ended` - Fires when the `Class.AnimationTrack` is completely done moving anything
- `AnimationTrack.KeyframeReached` - Fires every time playback of an `Class.AnimationTrack` reaches a
- `AnimationTrack.Stopped` - Fires when the `Class.AnimationTrack` finishes playing. The AnimationTrack

---

## Keyframe

A Keyframe holds the `Class.Pose|Poses` applied to joints in a `Class.Model`
at a given point of time in an animation. `Class.Keyframe|Keyframes` are
interpolated between during animation playback.

**Properties:**
- `Keyframe.Time`: float - The `Class.Keyframe` time position (in seconds) in an animation. This

**Methods:**
- `Keyframe:AddMarker` - Adds a `Class.KeyframeMarker` to the `Class.Keyframe` by parenting it to
- `Keyframe:AddPose` - Adds a `Class.Pose` to the `Class.Keyframe` by parenting it to the
- `Keyframe:GetMarkers` - Returns an array containing all `KeyframeMarkers` that have been added to
- `Keyframe:GetPoses` - Returns an array containing all `Class.Pose|Poses` that have been added to
- `Keyframe:RemoveMarker` - Removes a `Class.KeyframeMarker` from the `Class.Keyframe` by settings its
- `Keyframe:RemovePose` - Removes a `Class.Pose` from the `Class.Keyframe` by setting its

---

