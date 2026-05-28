---
name: building-construction
description: Provides patterns for building detailed structures programmatically using Parts and CSG. Use when creating buildings, towers, vehicles, or any brick-by-brick constructions in code.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Building & Construction Patterns

When building detailed structures programmatically in Roblox, use the brick-by-brick approach with simple primitives.

## Core Principle: Brick-by-Brick Construction

Build complex structures by stacking simple Parts. Don't try to be clever - use many simple pieces rather than few complex ones.

### Helper Function for Stud-Style Parts
```lua
local function createStudPart(size, position, color, name, parent)
    local part = Instance.new("Part")
    part.Size = size
    part.Position = position
    part.Anchored = true
    part.BrickColor = color
    part.Material = Enum.Material.Plastic
    part.TopSurface = Enum.SurfaceType.Studs
    part.BottomSurface = Enum.SurfaceType.Inlet
    part.FrontSurface = Enum.SurfaceType.Studs
    part.BackSurface = Enum.SurfaceType.Studs
    part.LeftSurface = Enum.SurfaceType.Studs
    part.RightSurface = Enum.SurfaceType.Studs
    part.Name = name or "Part"
    part.Parent = parent
    return part
end
```

## Mental Models for Common Structures

### Castle
Components: Foundation → Walls (with gate opening) → Crenellations → Corner Towers → Main Keep → Roofs → Details (windows, flags, doors)

```lua
-- Castle structure breakdown:
-- 1. Foundation (wide, flat)
createStudPart(Vector3.new(40, 2, 40), Vector3.new(0, 1, 0), BrickColor.new("Dark stone grey"), "Foundation", castle)

-- 2. Walls (4 sides, front has gate opening)
createStudPart(Vector3.new(wallLength, wallHeight, wallThickness), wallPosition, BrickColor.new("Medium stone grey"), "Wall", castle)

-- 3. Crenellations (small blocks on top of walls)
for i = -n, n do
    createStudPart(Vector3.new(1.5, 2, 1.5), Vector3.new(i * spacing, wallTop + 1, wallZ), BrickColor.new("Medium stone grey"), "Crenel", castle)
end

-- 4. Corner towers (taller than walls)
createStudPart(Vector3.new(towerSize, towerHeight, towerSize), cornerPos, BrickColor.new("Medium stone grey"), "Tower", castle)

-- 5. Tower roofs (stacked, tapering)
createStudPart(Vector3.new(4, 1, 4), roofPos, BrickColor.new("Bright red"), "Roof1", castle)
createStudPart(Vector3.new(3, 1, 3), roofPos + Vector3.new(0, 1, 0), BrickColor.new("Bright red"), "Roof2", castle)
createStudPart(Vector3.new(2, 1, 2), roofPos + Vector3.new(0, 2, 0), BrickColor.new("Bright red"), "Roof3", castle)

-- 6. Main keep (central, tallest)
createStudPart(Vector3.new(keepSize, keepHeight, keepSize), keepPos, BrickColor.new("Medium stone grey"), "Keep", castle)

-- 7. Details
createStudPart(Vector3.new(4, 5, 0.5), gatePos, BrickColor.new("Reddish brown"), "Door", castle)  -- Door
createStudPart(Vector3.new(1, 1.5, 0.3), windowPos, BrickColor.new("Really black"), "Window", castle)  -- Windows
createStudPart(Vector3.new(0.3, 4, 0.3), flagPolePos, BrickColor.new("Reddish brown"), "FlagPole", castle)  -- Flag
```

### Tower (Gun/Sniper/etc)
Components: Platform → Tiered Base (2-3 layers, decreasing size) → Body → Top with Crenellations → Special Features (barrel, crystal, coils)

```lua
-- Tower structure breakdown:
-- 1. Platform (widest)
createStudPart(Vector3.new(7, 1, 7), Vector3.new(x, 0.5, z), BrickColor.new("Medium stone grey"), "Platform", tower)

-- 2. Tiered base (each layer smaller)
createStudPart(Vector3.new(6, 1, 6), Vector3.new(x, 1.5, z), BrickColor.new("Brick yellow"), "Base1", tower)
createStudPart(Vector3.new(5, 1, 5), Vector3.new(x, 2.5, z), BrickColor.new("Brick yellow"), "Base2", tower)

-- 3. Main body
createStudPart(Vector3.new(4, 3, 4), Vector3.new(x, 4.5, z), BrickColor.new("Bright blue"), "Body", tower)

-- 4. Top section
createStudPart(Vector3.new(3, 2, 3), Vector3.new(x, 7, z), BrickColor.new("Bright blue"), "Top", tower)

-- 5. Crenellations (4 corners)
for dx = -1, 1, 2 do
    for dz = -1, 1, 2 do
        createStudPart(Vector3.new(1, 1.5, 1), Vector3.new(x + dx * 1.5, 8.75, z + dz * 1.5), BrickColor.new("Bright blue"), "Crenel", tower)
    end
end

-- 6. Special features (barrel, crystal, etc)
createStudPart(Vector3.new(1, 1, 4), Vector3.new(x, 5, z - 3.5), BrickColor.new("Dark stone grey"), "Barrel", tower)
```

### Coil/Spiral (Tesla Tower)
Build with stacked cylinders, each slightly smaller than the last:

```lua
for i = 1, 6 do
    local coilSize = 6 - i * 0.6  -- Tapering
    local coil = Instance.new("Part")
    coil.Shape = Enum.PartType.Cylinder
    coil.Size = Vector3.new(0.8, coilSize, coilSize)
    coil.CFrame = CFrame.new(x, baseY + i * 1.3, z) * CFrame.Angles(0, 0, math.rad(90))
    coil.Anchored = true
    coil.BrickColor = BrickColor.new("Deep orange")
    coil.Material = Enum.Material.Metal
    coil.Parent = tower
end
```

### Pyramid/Cone Roof
Stack decreasing-size parts:

```lua
local roofSizes = {4, 3, 2, 1}
for i, size in ipairs(roofSizes) do
    createStudPart(
        Vector3.new(size, 1, size),
        Vector3.new(x, baseY + i, z),
        BrickColor.new("Bright red"),
        "Roof" .. i, building
    )
end
```

## Detail Techniques

### Windows
Small black parts slightly in front of walls:
```lua
createStudPart(Vector3.new(1, 1.5, 0.3), Vector3.new(x, y, wallZ - 0.2), BrickColor.new("Really black"), "Window", building)
```

### Doors
Brown part in wall opening:
```lua
createStudPart(Vector3.new(4, 5, 0.5), gatePosition, BrickColor.new("Reddish brown"), "Door", building)
```

### Flags
Thin pole + flat flag:
```lua
createStudPart(Vector3.new(0.3, 4, 0.3), polePos, BrickColor.new("Reddish brown"), "FlagPole", building)
createStudPart(Vector3.new(0.2, 2, 3), flagPos, BrickColor.new("Bright blue"), "Flag", building)
```

### Glowing Effects
Add PointLight to parts:
```lua
local glow = Instance.new("PointLight")
glow.Color = Color3.fromRGB(255, 200, 100)
glow.Brightness = 2
glow.Range = 15
glow.Parent = part
```

### Angled Parts
Use CFrame rotation:
```lua
local barrel = createStudPart(Vector3.new(1.5, 1.5, 5), pos, color, "Barrel", tower)
barrel.CFrame = barrel.CFrame * CFrame.Angles(math.rad(-35), 0, 0)  -- Tilt up 35 degrees
```

## Color Palettes

### Castle/Stone
- Foundation: `BrickColor.new("Dark stone grey")`
- Walls: `BrickColor.new("Medium stone grey")`
- Roofs: `BrickColor.new("Bright red")`
- Doors: `BrickColor.new("Reddish brown")`
- Windows: `BrickColor.new("Really black")`

### Military
- Base: `BrickColor.new("Dark stone grey")`
- Body: `BrickColor.new("Earth green")`
- Metal: `BrickColor.new("Dark stone grey")`

### Ice/Freeze
- Base: `BrickColor.new("White")`, `BrickColor.new("Institutional white")`
- Body: `BrickColor.new("Bright blue")`, `BrickColor.new("Medium blue")`
- Crystal: `BrickColor.new("Cyan")` with `Material = Enum.Material.Ice`

### Gold/Treasure
- Base: `BrickColor.new("Reddish brown")`, `BrickColor.new("Bright orange")`
- Gold: `BrickColor.new("Bright yellow")` with `Reflectance = 0.4`

### Electric/Tesla
- Base: `BrickColor.new("Dark blue")`, `BrickColor.new("Navy blue")`
- Coils: `BrickColor.new("Deep orange")`, `BrickColor.new("Neon orange")`
- Ball: `BrickColor.new("Medium stone grey")` with `Reflectance = 0.5`

## Guidelines for Quality Builds

1. **Start with the silhouette** - What's the overall shape? Wide base, narrow top? Tall and thin?

2. **Layer from bottom to top** - Foundation → Base → Body → Top → Details

3. **Use tiered bases** - 2-3 layers of decreasing size creates visual interest

4. **Add crenellations** - Small blocks on top of walls/towers add detail cheaply

5. **Include special features** - What makes this unique? (barrel, crystal, coils, ears)

6. **Color hierarchy** - Darker at bottom (grounded), lighter/accent at top

7. **Details last** - Windows, doors, flags, lights come after structure is complete

8. **Consistent scale** - Keep brick sizes consistent (1-stud increments)

## When to Use CSG Operations

For shapes that can't be made with simple Parts:

```lua
-- Union (combine parts)
local union = part1:UnionAsync({part2, part3})

-- Negate (subtract/cut holes)
local negatedPart = Instance.new("Part")
negatedPart.Size = Vector3.new(2, 10, 2)  -- Hole shape
local result = mainPart:SubtractAsync({negatedPart})
```

**Prefer simple Parts over CSG when possible** - CSG operations are slower and can cause mesh issues.

## Checklist for Detailed Builds

- [ ] Clear mental model of structure components
- [ ] Foundation/platform layer
- [ ] Tiered base (2-3 layers)
- [ ] Main body with appropriate height
- [ ] Top section with crenellations or detail
- [ ] Special features (what makes it unique)
- [ ] Color palette appropriate to theme
- [ ] Details (windows, doors, decorations)
- [ ] Lighting effects where appropriate
- [ ] All surfaces have studs (classic Roblox style)

## How Claude Should Handle Build Requests

Users often give vague prompts like "make a tower" or "build a castle." Claude should NOT build primitively - instead, **automatically expand the request** into a detailed component breakdown before coding.

### The Expansion Approach

When receiving ANY 3D build request, Claude should:

1. **Identify the structure type** and recall its standard components
2. **Assume detailed LEGO/brick style** unless told otherwise
3. **Break down into components** before writing any code
4. **Plan the build order** (foundation → base → body → top → details)
5. **Include special features** that make it interesting

### Example: Expanding a Vague Request

**User says:** "Make a tower"

**Claude should think:**
```
Tower type: Defensive/gun tower (default)
Components needed:
- Platform (gray, widest layer)
- Tiered base (2-3 yellow layers, decreasing size)
- Main body (colored, 3-4 studs tall)
- Top section with crenellations (4 corner blocks)
- Special feature: barrel or weapon
- Style: Classic Roblox studs on all surfaces

Build order:
1. Platform (7x1x7)
2. Base layer 1 (6x1x6)
3. Base layer 2 (5x1x5)
4. Body (4x3x4)
5. Top (3x2x3)
6. Crenellations (4 x 1x1.5x1 corners)
7. Barrel (1x1x4)
```

**Then build it with full detail** - don't wait for user to ask for more.

### Expansion Templates

**"Build a castle"** → Expand to:
- Foundation (dark stone, wide)
- 4 walls with front gate opening
- Crenellations on all walls
- 4 corner towers (taller than walls)
- Tower roofs (red, stacked/tapered)
- Main keep (central, tallest)
- Keep roof with spire
- Details: door, windows, flag

**"Make a freeze tower"** → Expand to:
- White tiered base (2-3 layers)
- Blue body with stepped top
- Castle crenellations (blue)
- Ice crystals on top (3 crystals, different angles)
- Frost mist effect (cylinder, transparent, neon)
- Icy color palette (white, bright blue, cyan)

**"Build a Tesla tower"** → Expand to:
- Dark blue/navy base platform
- Central support pole
- Copper coil rings (6, tapering upward)
- White insulator rings (3)
- Large silver ball on top
- Electric PointLight glow

**"Make a house"** → Expand to:
- Foundation (stone gray)
- Walls (4 sides, with door and window openings)
- Door (brown)
- Windows (black inset)
- Roof (red/brown, angled or stacked)
- Chimney
- Optional: fence, path, mailbox

### Default Assumptions

When user doesn't specify, assume:
- **Style:** Classic Roblox/LEGO brick with studs on all surfaces
- **Detail level:** Detailed (20+ parts)
- **Colors:** Appropriate to structure type (see Color Palettes section)
- **Features:** Include what makes it recognizable (castle needs crenellations, tower needs tiered base)

### Code Pattern

```lua
-- ALWAYS start with component breakdown comment
--[[
Building: [Structure Name]
Components:
1. Foundation - [size, color]
2. Base layers - [sizes, color]
3. Body - [size, color]
4. Top - [size, color, crenellations]
5. Special features - [what makes it unique]
6. Details - [windows, doors, lights]
]]

local function build[StructureName](position, parent)
    local model = Instance.new("Model")
    model.Name = "[StructureName]"

    local x, z = position.X, position.Z

    -- 1. Foundation
    createStudPart(...)

    -- 2. Base layers
    createStudPart(...)
    createStudPart(...)

    -- 3. Body
    local body = createStudPart(...)

    -- 4. Top with crenellations
    createStudPart(...)
    for dx = -1, 1, 2 do
        for dz = -1, 1, 2 do
            createStudPart(...) -- crenels
        end
    end

    -- 5. Special features
    createStudPart(...) -- barrel/crystal/etc

    -- 6. Details
    createStudPart(...) -- windows
    createStudPart(...) -- door

    -- 7. Lighting
    local light = Instance.new("PointLight")
    light.Parent = body

    model.PrimaryPart = body
    model.Parent = parent
    return model
end
```

### Key Rule

**Never build primitively.** A "tower" is never just a single rectangular part. Always expand to the full component list and build with detail.

If unsure about style/detail level, **default to MORE detail** - it's easier for users to ask for simplification than to ask for "make it better."
