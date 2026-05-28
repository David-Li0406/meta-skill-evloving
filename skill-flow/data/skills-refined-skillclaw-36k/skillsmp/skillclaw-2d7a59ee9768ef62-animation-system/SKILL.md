---
name: animation-system
description: Use this skill when creating character animations, custom rigs, or procedural movement in Roblox, implementing features like custom animators, animation blending, and procedural animation.
---

# Skill body

## Animation Basics

### Loading and Playing Animations
```lua
local function setupAnimations(character)
    local humanoid = character:WaitForChild("Humanoid")
    local animator = humanoid:WaitForChild("Animator")

    -- Create animation instance
    local walkAnim = Instance.new("Animation")
    walkAnim.AnimationId = "rbxassetid://123456789"

    -- Load animation track
    local walkTrack = animator:LoadAnimation(walkAnim)

    -- Configure track
    walkTrack.Priority = Enum.AnimationPriority.Movement
    walkTrack.Looped = true

    -- Play with parameters
    walkTrack:Play(
        0.1,  -- Fade in time
        1,    -- Weight (0-1)
        1     -- Speed multiplier
    )

    return walkTrack
end
```

### Animation Priorities
```lua
-- Priority order (lowest to highest):
-- Core < Idle < Movement < Action < Action2 < Action3 < Action4

local function setAnimationPriority(track, priority)
    track.Priority = priority
end

-- Example priority usage
idleTrack.Priority = Enum.AnimationPriority.Idle
walkTrack.Priority = Enum.AnimationPriority.Movement
attackTrack.Priority = Enum.AnimationPriority.Action
-- Action always overrides Movement, Movement overrides Idle
```

### Animation Events (Keyframe Markers)
```lua
-- Add markers in Animation Editor, then listen:
local function setupAnimationEvents(track)
    -- Listen for specific marker
    track:GetMarkerReachedSignal("Footstep"):Connect(function(paramValue)
        playFootstepSound()
    end)

    track:GetMarkerReachedSignal("DamageFrame"):Connect(function()
        applyDamage()
    end)

    track:GetMarkerReachedSignal("SpawnVFX"):Connect(function(vfxName)
        spawnEffect(vfxName)
    end)
end

-- Animation completion
track.Stopped:Connect(function()
    print("Animation stopped or completed")
end)

-- Check if playing
if track.IsPlaying then
    -- Animation is active
end
```

## Animation Controller

### State-Based Animation Controller
```lua
local AnimationController = {}
AnimationController.__index = AnimationController

function AnimationController.new(character)
    local self = setmetatable({}, AnimationController)
    -- Initialize controller properties here
    return self
end
```