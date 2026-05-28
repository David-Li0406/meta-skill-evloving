---
name: procedural-generation
description: Implements procedural generation systems including noise functions, terrain generation, dungeon generation, city generation, and object placement. Use when building roguelikes, open worlds, or any content that needs to be generated algorithmically.
---

# Procedural Generation Techniques

When implementing procedural content, use these patterns for varied and interesting generated worlds.

## Noise Functions

### Multi-Octave Perlin Noise
```lua
local function octaveNoise(x, y, octaves, persistence, scale, lacunarity)
    octaves = octaves or 4
    persistence = persistence or 0.5
    scale = scale or 1
    lacunarity = lacunarity or 2

    local total = 0
    local frequency = scale
    local amplitude = 1
    local maxValue = 0

    for i = 1, octaves do
        total = total + math.noise(x * frequency, y * frequency) * amplitude
        maxValue = maxValue + amplitude
        amplitude = amplitude * persistence
        frequency = frequency * lacunarity
    end

    return total / maxValue  -- Normalize to [-1, 1]
end
```

### Domain Warping
```lua
local function warpedNoise(x, y, scale, warpStrength)
    local warpX = math.noise(x * scale, y * scale, 0) * warpStrength
    local warpY = math.noise(x * scale, y * scale, 100) * warpStrength

    return math.noise((x + warpX) * scale, (y + warpY) * scale)
end
```

### Ridged Noise (Mountains)
```lua
local function ridgedNoise(x, y, octaves, scale)
    local total = 0
    local frequency = scale
    local amplitude = 1
    local weight = 1

    for i = 1, octaves do
        local noise = math.noise(x * frequency, y * frequency)
        noise = 1 - math.abs(noise)  -- Create ridges
        noise = noise * noise        -- Sharpen ridges
        noise = noise * weight
        weight = math.clamp(noise * 2, 0, 1)

        total = total + noise * amplitude
        amplitude = amplitude * 0.5
        frequency = frequency * 2
    end

    return total
end
```

## Terrain Generation

### Heightmap-Based Terrain
```lua
local TerrainGenerator = {}

function TerrainGenerator.generateChunk(chunkX, chunkZ, chunkSize, resolution)
    local terrain = workspace.Terrain
    local heightMap = {}

    for x = 0, resolution do
        heightMap[x] = {}
        for z = 0, resolution do
            local worldX = chunkX * chunkSize + (x / resolution) * chunkSize
            local worldZ = chunkZ * chunkSize + (z / resolution) * chunkSize

            local height = getTerrainHeight(worldX, worldZ)
            heightMap[x][z] = height
        end
    end

    local cellSize = chunkSize / resolution
    for x = 0, resolution - 1 do
        for z = 0, resolution - 1 do
            local worldX = chunkX * chunkSize + x * cellSize
            local worldZ = chunkZ * chunkSize + z * cellSize

            local h1 = heightMap[x][z]
            local h2 = heightMap[x + 1][z]
            local h3 = heightMap[x][z + 1]
            local h4 = heightMap[x + 1][z + 1]

            local minH = math.min(h1, h2, h3, h4)
            local maxH = math.max(h1, h2, h3, h4)

            local material = TerrainGenerator.getMaterial(maxH, maxH - minH)

            terrain:FillBlock(
                CFrame.new(worldX + cellSize/2, (minH + maxH)/2, worldZ + cellSize/2),
                Vector3.new(cellSize, maxH - minH + 1, cellSize),
                material
            )
        end
    end
end
```

## Dungeon Generation

### BSP (Binary Space Partitioning)
```lua
local DungeonGenerator = {}

local function splitRoom(room, minSize)
    local rooms = {}

    local canSplitH = room.width >= minSize * 2
    local canSplitV = room.height >= minSize * 2

    if not canSplitH and not canSplitV then
        return {room}
    end

    local splitHorizontal
    if canSplitH and canSplitV then
        splitHorizontal = math.random() > 0.5
    else
        splitHorizontal = canSplitH
    end

    if splitHorizontal then
        local splitX = room.x + math.random(minSize, room.width - minSize)
        local room1 = {x = room.x, y = room.y, width = splitX - room.x, height = room.height}
        local room2 = {x = splitX, y = room.y, width = room.x + room.width - splitX, height = room.height}

        for _, r in ipairs(splitRoom(room1, minSize)) do
            table.insert(rooms, r)
        end
        for _, r in ipairs(splitRoom(room2, minSize)) do
            table.insert(rooms, r)
        end
    else
        local splitY = room.y + math.random(minSize, room.height - minSize)
        local room1 = {x = room.x, y = room.y, width = room.width, height = splitY - room.y}
        local room2 = {x = room.x, y = splitY, width = room.width, height = room.y + room.height - splitY}

        for _, r in ipairs(splitRoom(room1, minSize)) do
            table.insert(rooms, r)
        end
        for _, r in ipairs(splitRoom(room2, minSize)) do
            table.insert(rooms, r)
        end
    end

    return rooms
end

function DungeonGenerator.generate(width, height, minRoomSize)
    local initialRoom = {x = 0, y = 0, width = width, height = height}
    local partitions = splitRoom(initialRoom, minRoomSize)

    local rooms = {}
    for _, partition in ipairs(partitions) do
        local padding = 2
        local room = {
            x = partition.x + padding,
            y = partition.y + padding,
            width = partition.width - padding * 2,
            height = partition.height - padding * 2
        }
        if room.width > 0 and room.height > 0 then
            table.insert(rooms, room)
        end
    end

    return rooms
end
```

## Object Placement

### Poisson Disc Sampling
```lua
local function poissonDiscSampling(width, height, minDistance, maxAttempts)
    maxAttempts = maxAttempts or 30
    local cellSize = minDistance / math.sqrt(2)
    local gridWidth = math.ceil(width / cellSize)
    local gridHeight = math.ceil(height / cellSize)

    local grid = {}
    for i = 1, gridWidth do
        grid[i] = {}
    end

    local points = {}
    local activeList = {}

    local startX = math.random() * width
    local startY = math.random() * height
    table.insert(points, {x = startX, y = startY})
    table.insert(activeList, 1)

    local gx = math.floor(startX / cellSize) + 1
    local gy = math.floor(startY / cellSize) + 1
    grid[gx][gy] = 1

    while #activeList > 0 do
        local activeIndex = math.random(#activeList)
        local currentPoint = points[activeList[activeIndex]]
        local found = false

        for _ = 1, maxAttempts do
            local angle = math.random() * math.pi * 2
            local distance = minDistance + math.random() * minDistance

            local newX = currentPoint.x + math.cos(angle) * distance
            local newY = currentPoint.y + math.sin(angle) * distance

            if newX >= 0 and newX < width and newY >= 0 and newY < height then
                local gx = math.floor(newX / cellSize) + 1
                local gy = math.floor(newY / cellSize) + 1

                local valid = true

                for dx = -2, 2 do
                    for dy = -2, 2 do
                        local checkX = gx + dx
                        local checkY = gy + dy

                        if checkX >= 1 and checkX <= gridWidth and
                           checkY >= 1 and checkY <= gridHeight and
                           grid[checkX][checkY] then

                            local otherPoint = points[grid[checkX][checkY]]
                            local dist = math.sqrt((newX - otherPoint.x)^2 + (newY - otherPoint.y)^2)

                            if dist < minDistance then
                                valid = false
                                break
                            end
                        end
                    end
                    if not valid then break end
                end

                if valid then
                    local newIndex = #points + 1
                    table.insert(points, {x = newX, y = newY})
                    table.insert(activeList, newIndex)
                    grid[gx][gy] = newIndex
                    found = true
                    break
                end
            end
        end

        if not found then
            table.remove(activeList, activeIndex)
        end
    end

    return points
end
```