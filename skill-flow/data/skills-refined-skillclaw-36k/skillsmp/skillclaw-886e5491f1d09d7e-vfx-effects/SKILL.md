---
name: vfx-effects
description: Use this skill when implementing visual effects such as particle systems, camera effects, lighting, mesh effects, and UI animations for combat, environmental effects, feedback systems, or any visual polish.
---

# Skill body

## Roblox Visual Effects (VFX)

When implementing VFX, use these patterns for impactful and performant effects.

### Particle Effects

#### Anime Hit VFX
```lua
local function createHitEffect(position, direction, intensity)
    intensity = intensity or 1

    -- Impact flash
    local flash = Instance.new("Part")
    flash.Shape = Enum.PartType.Ball
    flash.Size = Vector3.new(0.1, 0.1, 0.1)
    flash.Position = position
    flash.Anchored = true
    flash.CanCollide = false
    flash.Material = Enum.Material.Neon
    flash.Color = Color3.new(1, 1, 1)
    flash.Parent = workspace.Effects

    -- Scale up and fade
    local tweenInfo = TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    TweenService:Create(flash, tweenInfo, {
        Size = Vector3.new(3, 3, 3) * intensity,
        Transparency = 1
    }):Play()

    -- Radial lines (speedlines)
    local numLines = 8
    for i = 1, numLines do
        local angle = (i / numLines) * math.pi * 2
        local lineDir = Vector3.new(math.cos(angle), 0, math.sin(angle))

        local line = Instance.new("Part")
        line.Size = Vector3.new(0.1, 0.1, 2)
        line.CFrame = CFrame.lookAt(position, position + lineDir) * CFrame.new(0, 0, -1)
        line.Anchored = true
        line.CanCollide = false
        line.Material = Enum.Material.Neon
        line.Color = Color3.new(1, 0.9, 0.8)
        line.Parent = workspace.Effects

        TweenService:Create(line, TweenInfo.new(0.2), {
            Size = Vector3.new(0.05, 0.05, 5) * intensity,
            CFrame = line.CFrame * CFrame.new(0, 0, -3),
            Transparency = 1
        }):Play()

        Debris:AddItem(line, 0.3)
    end

    -- Screen shake
    shakeCamera(0.3, intensity * 5)

    Debris:AddItem(flash, 0.2)
end
```

#### Slash Trail
```lua
local function createSlashTrail(weapon, duration)
    local attachment0 = weapon:FindFirstChild("TrailAttachment0")
    local attachment1 = weapon:FindFirstChild("TrailAttachment1")

    if not attachment0 or not attachment1 then
        -- Create attachments at blade ends
        attachment0 = Instance.new("Attachment")
        attachment0.Name = "TrailAttachment0"
        attachment0.Position = Vector3.new(0, 0, 0) -- Adjust position as needed
        attachment0.Parent = weapon

        attachment1 = Instance.new("Attachment")
        attachment1.Name = "TrailAttachment1"
        attachment1.Position = Vector3.new(0, 0, 0) -- Adjust position as needed
        attachment1.Parent = weapon
    end

    -- Create the trail effect here
    -- (Implementation details would go here)
end
```