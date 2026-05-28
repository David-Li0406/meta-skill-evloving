---
name: procedural-generation
description: Implements procedural generation techniques including noise-based terrain, dungeon generation, wave function collapse, and random world building. Use when creating procedurally generated content.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Procedural Generation

When implementing procedural content, use these patterns for varied and interesting generated worlds.

## Noise-Based Generation

### Using FastNoiseLite
```gdscript
extends Node2D

var noise := FastNoiseLite.new()

func _ready() -> void:
    # Configure noise
    noise.noise_type = FastNoiseLite.TYPE_PERLIN
    noise.seed = randi()
    noise.frequency = 0.02

    # Optional fractal settings for more detail
    noise.fractal_type = FastNoiseLite.FRACTAL_FBM
    noise.fractal_octaves = 4
    noise.fractal_lacunarity = 2.0
    noise.fractal_gain = 0.5

func get_height_at(x: float, y: float) -> float:
    # Returns value between -1 and 1
    return noise.get_noise_2d(x, y)

func get_normalized_height(x: float, y: float) -> float:
    # Returns value between 0 and 1
    return (noise.get_noise_2d(x, y) + 1.0) / 2.0
```

### Terrain Generation with Multiple Noise Layers
```gdscript
extends Node3D

var base_noise := FastNoiseLite.new()
var detail_noise := FastNoiseLite.new()
var moisture_noise := FastNoiseLite.new()

@export var terrain_size := Vector2i(100, 100)
@export var height_scale := 20.0

func _ready() -> void:
    setup_noise()
    generate_terrain()

func setup_noise() -> void:
    var seed_value := randi()

    base_noise.seed = seed_value
    base_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    base_noise.frequency = 0.005
    base_noise.fractal_type = FastNoiseLite.FRACTAL_FBM
    base_noise.fractal_octaves = 5

    detail_noise.seed = seed_value + 1
    detail_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    detail_noise.frequency = 0.05
    detail_noise.fractal_octaves = 3

    moisture_noise.seed = seed_value + 2
    moisture_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    moisture_noise.frequency = 0.01

func get_terrain_height(x: float, z: float) -> float:
    var base := base_noise.get_noise_2d(x, z)
    var detail := detail_noise.get_noise_2d(x, z) * 0.3

    return (base + detail) * height_scale

func get_biome(x: float, z: float) -> String:
    var height := get_terrain_height(x, z) / height_scale
    var moisture := moisture_noise.get_noise_2d(x, z)

    if height < -0.2:
        return "water"
    elif height < 0.0:
        return "beach"
    elif height > 0.6:
        return "mountain"
    elif moisture > 0.3:
        return "forest"
    elif moisture < -0.3:
        return "desert"
    else:
        return "plains"

func generate_terrain() -> void:
    var surface_tool := SurfaceTool.new()
    surface_tool.begin(Mesh.PRIMITIVE_TRIANGLES)

    for x in range(terrain_size.x):
        for z in range(terrain_size.y):
            var height := get_terrain_height(x, z)
            add_terrain_quad(surface_tool, x, z, height)

    surface_tool.generate_normals()
    var mesh := surface_tool.commit()

    var mesh_instance := MeshInstance3D.new()
    mesh_instance.mesh = mesh
    add_child(mesh_instance)
```

### Chunk-Based Infinite Terrain
```gdscript
extends Node3D

const CHUNK_SIZE := 32
const RENDER_DISTANCE := 3

var chunks: Dictionary = {}  # Vector2i -> MeshInstance3D
var player_chunk := Vector2i.ZERO

func _process(_delta: float) -> void:
    update_player_chunk()
    load_nearby_chunks()
    unload_distant_chunks()

func update_player_chunk() -> void:
    var player_pos: Vector3 = $Player.global_position
    player_chunk = Vector2i(
        floor(player_pos.x / CHUNK_SIZE),
        floor(player_pos.z / CHUNK_SIZE)
    )

func load_nearby_chunks() -> void:
    for x in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for z in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            var chunk_pos := player_chunk + Vector2i(x, z)
            if not chunks.has(chunk_pos):
                generate_chunk(chunk_pos)

func unload_distant_chunks() -> void:
    var to_remove: Array[Vector2i] = []

    for chunk_pos in chunks.keys():
        var distance := (chunk_pos - player_chunk).length()
        if distance > RENDER_DISTANCE + 1:
            to_remove.append(chunk_pos)

    for chunk_pos in to_remove:
        chunks[chunk_pos].queue_free()
        chunks.erase(chunk_pos)

func generate_chunk(chunk_pos: Vector2i) -> void:
    var mesh := create_chunk_mesh(chunk_pos)
    var instance := MeshInstance3D.new()
    instance.mesh = mesh
    instance.position = Vector3(
        chunk_pos.x * CHUNK_SIZE,
        0,
        chunk_pos.y * CHUNK_SIZE
    )
    add_child(instance)
    chunks[chunk_pos] = instance
```

## Dungeon Generation

### Binary Space Partitioning (BSP)
```gdscript
class_name BSPDungeon
extends Node

class BSPNode:
    var rect: Rect2i
    var left: BSPNode
    var right: BSPNode
    var room: Rect2i

    func _init(r: Rect2i) -> void:
        rect = r

    func is_leaf() -> bool:
        return left == null and right == null

var min_room_size := 6
var split_chance := 0.8
var rooms: Array[Rect2i] = []

func generate(width: int, height: int) -> Array:
    var root := BSPNode.new(Rect2i(0, 0, width, height))
    split_node(root)
    create_rooms(root)
    var corridors := connect_rooms(root)

    return [rooms, corridors]

func split_node(node: BSPNode) -> void:
    if randf() > split_chance:
        return

    var can_split_h := node.rect.size.y >= min_room_size * 2
    var can_split_v := node.rect.size.x >= min_room_size * 2

    if not can_split_h and not can_split_v:
        return

    var split_horizontal: bool
    if can_split_h and can_split_v:
        split_horizontal = randf() > 0.5
    else:
        split_horizontal = can_split_h

    if split_horizontal:
        var split_y := randi_range(min_room_size, node.rect.size.y - min_room_size)
        node.left = BSPNode.new(Rect2i(
            node.rect.position,
            Vector2i(node.rect.size.x, split_y)
        ))
        node.right = BSPNode.new(Rect2i(
            node.rect.position + Vector2i(0, split_y),
            Vector2i(node.rect.size.x, node.rect.size.y - split_y)
        ))
    else:
        var split_x := randi_range(min_room_size, node.rect.size.x - min_room_size)
        node.left = BSPNode.new(Rect2i(
            node.rect.position,
            Vector2i(split_x, node.rect.size.y)
        ))
        node.right = BSPNode.new(Rect2i(
            node.rect.position + Vector2i(split_x, 0),
            Vector2i(node.rect.size.x - split_x, node.rect.size.y)
        ))

    split_node(node.left)
    split_node(node.right)

func create_rooms(node: BSPNode) -> void:
    if node.is_leaf():
        # Create room smaller than partition
        var padding := 2
        var room_w := randi_range(min_room_size, node.rect.size.x - padding * 2)
        var room_h := randi_range(min_room_size, node.rect.size.y - padding * 2)
        var room_x := node.rect.position.x + randi_range(padding, node.rect.size.x - room_w - padding)
        var room_y := node.rect.position.y + randi_range(padding, node.rect.size.y - room_h - padding)

        node.room = Rect2i(room_x, room_y, room_w, room_h)
        rooms.append(node.room)
    else:
        if node.left:
            create_rooms(node.left)
        if node.right:
            create_rooms(node.right)

func connect_rooms(node: BSPNode) -> Array[Rect2i]:
    var corridors: Array[Rect2i] = []

    if not node.is_leaf():
        var room1 := get_room(node.left)
        var room2 := get_room(node.right)

        if room1 and room2:
            corridors.append_array(create_corridor(room1, room2))

        corridors.append_array(connect_rooms(node.left))
        corridors.append_array(connect_rooms(node.right))

    return corridors

func get_room(node: BSPNode) -> Rect2i:
    if node.room != Rect2i():
        return node.room
    if node.left:
        return get_room(node.left)
    if node.right:
        return get_room(node.right)
    return Rect2i()

func create_corridor(room1: Rect2i, room2: Rect2i) -> Array[Rect2i]:
    var corridors: Array[Rect2i] = []
    var center1 := room1.get_center()
    var center2 := room2.get_center()

    # L-shaped corridor
    if randf() > 0.5:
        corridors.append(Rect2i(center1.x, center1.y, center2.x - center1.x + 1, 2))
        corridors.append(Rect2i(center2.x, min(center1.y, center2.y), 2, abs(center2.y - center1.y) + 1))
    else:
        corridors.append(Rect2i(center1.x, center1.y, 2, center2.y - center1.y + 1))
        corridors.append(Rect2i(min(center1.x, center2.x), center2.y, abs(center2.x - center1.x) + 1, 2))

    return corridors
```

### Cellular Automata Cave Generation
```gdscript
class_name CaveGenerator
extends Node

var width := 80
var height := 50
var fill_probability := 0.45
var smoothing_iterations := 5
var birth_limit := 4
var death_limit := 3

var grid: Array[Array] = []

func generate() -> Array[Array]:
    initialize_grid()

    for i in range(smoothing_iterations):
        smooth_grid()

    return grid

func initialize_grid() -> void:
    grid.clear()
    for x in range(width):
        var column: Array[bool] = []
        for y in range(height):
            # True = wall, False = floor
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                column.append(true)  # Border walls
            else:
                column.append(randf() < fill_probability)
        grid.append(column)

func smooth_grid() -> void:
    var new_grid: Array[Array] = []

    for x in range(width):
        var column: Array[bool] = []
        for y in range(height):
            var neighbors := count_neighbors(x, y)

            if grid[x][y]:
                # Wall
                column.append(neighbors >= death_limit)
            else:
                # Floor
                column.append(neighbors > birth_limit)
        new_grid.append(column)

    grid = new_grid

func count_neighbors(x: int, y: int) -> int:
    var count := 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            var nx := x + dx
            var ny := y + dy

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                count += 1  # Out of bounds counts as wall
            elif grid[nx][ny]:
                count += 1

    return count
```

### Room-Based Dungeon with Prefabs
```gdscript
class_name PrefabDungeon
extends Node2D

@export var room_prefabs: Array[PackedScene]
@export var start_room: PackedScene
@export var boss_room: PackedScene
@export var dungeon_size := 10

var placed_rooms: Array[Node2D] = []
var open_doors: Array[Dictionary] = []  # {room, door_position, direction}

func generate() -> void:
    # Place start room
    var start := start_room.instantiate() as Node2D
    add_child(start)
    placed_rooms.append(start)
    register_doors(start)

    # Generate main dungeon
    for i in range(dungeon_size - 2):
        if open_doors.is_empty():
            break
        place_random_room()

    # Place boss room
    if not open_doors.is_empty():
        place_specific_room(boss_room)

func register_doors(room: Node2D) -> void:
    for door in room.get_node("Doors").get_children():
        open_doors.append({
            "room": room,
            "position": door.global_position,
            "direction": door.rotation
        })

func place_random_room() -> void:
    var prefab: PackedScene = room_prefabs.pick_random()
    place_specific_room(prefab)

func place_specific_room(prefab: PackedScene) -> void:
    var door_data: Dictionary = open_doors.pick_random()
    open_doors.erase(door_data)

    var new_room := prefab.instantiate() as Node2D
    var entry_door := find_compatible_door(new_room, door_data["direction"])

    if entry_door:
        # Position room so doors align
        var offset: Vector2 = entry_door.position
        new_room.global_position = door_data["position"] - offset.rotated(new_room.rotation)

        # Check for overlaps
        if not check_overlap(new_room):
            add_child(new_room)
            placed_rooms.append(new_room)
            register_doors(new_room)
            return

    new_room.queue_free()
    # Try again with different door
    open_doors.append(door_data)

func find_compatible_door(room: Node2D, target_direction: float) -> Node2D:
    var opposite := target_direction + PI
    for door in room.get_node("Doors").get_children():
        if abs(angle_difference(door.rotation, opposite)) < 0.1:
            return door
    return null
```

## Wave Function Collapse

### Simple WFC Implementation
```gdscript
class_name WaveFunctionCollapse
extends Node

class Tile:
    var id: int
    var constraints: Dictionary  # direction -> Array of allowed neighbor IDs

var tiles: Array[Tile] = []
var grid: Array[Array] = []  # 2D array of possible tile IDs (superposition)
var width: int
var height: int

func setup(w: int, h: int, tile_data: Array[Tile]) -> void:
    width = w
    height = h
    tiles = tile_data

    # Initialize grid with all possibilities
    grid.clear()
    for x in range(width):
        var column: Array = []
        for y in range(height):
            var possibilities: Array[int] = []
            for tile in tiles:
                possibilities.append(tile.id)
            column.append(possibilities)
        grid.append(column)

func collapse() -> bool:
    while not is_collapsed():
        var cell := find_lowest_entropy()
        if cell == Vector2i(-1, -1):
            return false  # Contradiction

        if not collapse_cell(cell):
            return false

        if not propagate(cell):
            return false

    return true

func is_collapsed() -> bool:
    for x in range(width):
        for y in range(height):
            if grid[x][y].size() != 1:
                return false
    return true

func find_lowest_entropy() -> Vector2i:
    var min_entropy := 999
    var candidates: Array[Vector2i] = []

    for x in range(width):
        for y in range(height):
            var entropy: int = grid[x][y].size()
            if entropy <= 1:
                continue

            if entropy < min_entropy:
                min_entropy = entropy
                candidates.clear()
                candidates.append(Vector2i(x, y))
            elif entropy == min_entropy:
                candidates.append(Vector2i(x, y))

    if candidates.is_empty():
        return Vector2i(-1, -1)

    return candidates.pick_random()

func collapse_cell(cell: Vector2i) -> bool:
    var possibilities: Array = grid[cell.x][cell.y]
    if possibilities.is_empty():
        return false

    # Choose random possibility (can add weights)
    var chosen: int = possibilities.pick_random()
    grid[cell.x][cell.y] = [chosen]
    return true

func propagate(start: Vector2i) -> bool:
    var stack: Array[Vector2i] = [start]

    while not stack.is_empty():
        var current := stack.pop_back()
        var current_possibilities: Array = grid[current.x][current.y]

        for dir in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
            var neighbor := current + dir
            if not is_valid(neighbor):
                continue

            var allowed := get_allowed_neighbors(current_possibilities, dir)
            var neighbor_possibilities: Array = grid[neighbor.x][neighbor.y]
            var new_possibilities: Array = []

            for p in neighbor_possibilities:
                if p in allowed:
                    new_possibilities.append(p)

            if new_possibilities.size() < neighbor_possibilities.size():
                if new_possibilities.is_empty():
                    return false  # Contradiction

                grid[neighbor.x][neighbor.y] = new_possibilities
                stack.append(neighbor)

    return true

func get_allowed_neighbors(possibilities: Array, direction: Vector2i) -> Array:
    var allowed: Array = []
    for tile_id in possibilities:
        var tile := tiles[tile_id]
        var dir_name := direction_to_string(direction)
        if tile.constraints.has(dir_name):
            for allowed_id in tile.constraints[dir_name]:
                if allowed_id not in allowed:
                    allowed.append(allowed_id)
    return allowed

func direction_to_string(dir: Vector2i) -> String:
    match dir:
        Vector2i.UP: return "up"
        Vector2i.DOWN: return "down"
        Vector2i.LEFT: return "left"
        Vector2i.RIGHT: return "right"
    return ""

func is_valid(pos: Vector2i) -> bool:
    return pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height
```

## Object Placement

### Poisson Disc Sampling
```gdscript
class_name PoissonDiscSampling
extends RefCounted

static func generate(width: float, height: float, min_distance: float, attempts: int = 30) -> Array[Vector2]:
    var cell_size := min_distance / sqrt(2)
    var grid_width := int(ceil(width / cell_size))
    var grid_height := int(ceil(height / cell_size))

    var grid: Array = []
    grid.resize(grid_width * grid_height)
    grid.fill(-1)

    var points: Array[Vector2] = []
    var active: Array[int] = []

    # Start with random point
    var initial := Vector2(randf() * width, randf() * height)
    points.append(initial)
    active.append(0)
    grid[grid_index(initial, cell_size, grid_width)] = 0

    while not active.is_empty():
        var idx := randi() % active.size()
        var point := points[active[idx]]
        var found := false

        for _attempt in range(attempts):
            var angle := randf() * TAU
            var distance := min_distance + randf() * min_distance
            var candidate := point + Vector2(cos(angle), sin(angle)) * distance

            if is_valid_point(candidate, width, height, min_distance, points, grid, cell_size, grid_width, grid_height):
                points.append(candidate)
                active.append(points.size() - 1)
                grid[grid_index(candidate, cell_size, grid_width)] = points.size() - 1
                found = true
                break

        if not found:
            active.remove_at(idx)

    return points

static func grid_index(point: Vector2, cell_size: float, grid_width: int) -> int:
    var x := int(point.x / cell_size)
    var y := int(point.y / cell_size)
    return y * grid_width + x

static func is_valid_point(candidate: Vector2, width: float, height: float, min_dist: float,
                          points: Array[Vector2], grid: Array, cell_size: float,
                          grid_width: int, grid_height: int) -> bool:
    if candidate.x < 0 or candidate.x >= width or candidate.y < 0 or candidate.y >= height:
        return false

    var cell_x := int(candidate.x / cell_size)
    var cell_y := int(candidate.y / cell_size)

    # Check neighboring cells
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            var nx := cell_x + dx
            var ny := cell_y + dy

            if nx >= 0 and nx < grid_width and ny >= 0 and ny < grid_height:
                var idx: int = grid[ny * grid_width + nx]
                if idx != -1:
                    if candidate.distance_to(points[idx]) < min_dist:
                        return false

    return true
```

### Weighted Random Placement
```gdscript
func place_objects_weighted(positions: Array[Vector2], weights: Dictionary) -> void:
    # weights = {"tree": 0.5, "rock": 0.3, "bush": 0.2}

    var total_weight := 0.0
    for w in weights.values():
        total_weight += w

    for pos in positions:
        var roll := randf() * total_weight
        var cumulative := 0.0

        for object_type in weights:
            cumulative += weights[object_type]
            if roll <= cumulative:
                spawn_object(object_type, pos)
                break

func spawn_object(type: String, position: Vector2) -> void:
    var prefab: PackedScene = load("res://objects/%s.tscn" % type)
    var instance := prefab.instantiate()
    instance.position = position
    add_child(instance)
```
