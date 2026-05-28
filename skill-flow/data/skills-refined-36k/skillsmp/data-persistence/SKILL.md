---
name: data-persistence
description: Implements save/load systems using Resources, JSON, ConfigFile, and file encryption. Use when persisting game data, settings, and player progress.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Data Persistence

When implementing save systems, use these patterns for reliable and secure data storage.

## Resource-Based Saving

### Custom Resource for Save Data
```gdscript
# save_data.gd
class_name SaveData
extends Resource

@export var player_name := "Player"
@export var level := 1
@export var experience := 0
@export var health := 100
@export var position := Vector3.ZERO
@export var inventory: Array[Dictionary] = []
@export var unlocked_abilities: Array[String] = []
@export var play_time := 0.0
@export var save_timestamp := 0

func _init() -> void:
    save_timestamp = int(Time.get_unix_time_from_system())
```

### Resource Save/Load
```gdscript
extends Node

const SAVE_PATH := "user://saves/"

func save_game(slot: int, data: SaveData) -> bool:
    # Ensure directory exists
    DirAccess.make_dir_recursive_absolute(SAVE_PATH)

    var path := SAVE_PATH + "save_%d.tres" % slot
    var error := ResourceSaver.save(data, path)

    if error != OK:
        push_error("Failed to save: %s" % error)
        return false

    return true

func load_game(slot: int) -> SaveData:
    var path := SAVE_PATH + "save_%d.tres" % slot

    if not FileAccess.file_exists(path):
        return null

    var data := ResourceLoader.load(path) as SaveData
    return data

func delete_save(slot: int) -> void:
    var path := SAVE_PATH + "save_%d.tres" % slot
    DirAccess.remove_absolute(path)

func get_save_slots() -> Array[Dictionary]:
    var slots: Array[Dictionary] = []

    for i in range(10):  # 10 save slots
        var path := SAVE_PATH + "save_%d.tres" % i
        if FileAccess.file_exists(path):
            var data := ResourceLoader.load(path) as SaveData
            slots.append({
                "slot": i,
                "name": data.player_name,
                "level": data.level,
                "timestamp": data.save_timestamp
            })
        else:
            slots.append({"slot": i, "empty": true})

    return slots
```

## JSON Save System

### JSON Serialization
```gdscript
extends Node

const SAVE_FILE := "user://save_data.json"

func save_to_json(data: Dictionary) -> bool:
    var json_string := JSON.stringify(data, "\t")

    var file := FileAccess.open(SAVE_FILE, FileAccess.WRITE)
    if not file:
        push_error("Failed to open save file: %s" % FileAccess.get_open_error())
        return false

    file.store_string(json_string)
    file.close()
    return true

func load_from_json() -> Dictionary:
    if not FileAccess.file_exists(SAVE_FILE):
        return {}

    var file := FileAccess.open(SAVE_FILE, FileAccess.READ)
    if not file:
        return {}

    var json_string := file.get_as_text()
    file.close()

    var json := JSON.new()
    var error := json.parse(json_string)

    if error != OK:
        push_error("JSON parse error: %s" % json.get_error_message())
        return {}

    return json.data

# Usage
func save_player_data() -> void:
    var data := {
        "version": 1,
        "player": {
            "name": player_name,
            "level": level,
            "position": {"x": position.x, "y": position.y, "z": position.z}
        },
        "inventory": inventory,
        "timestamp": Time.get_unix_time_from_system()
    }
    save_to_json(data)

func load_player_data() -> void:
    var data := load_from_json()
    if data.is_empty():
        return

    player_name = data.player.name
    level = data.player.level
    position = Vector3(
        data.player.position.x,
        data.player.position.y,
        data.player.position.z
    )
```

### Type-Safe Serialization
```gdscript
class_name Serializer
extends RefCounted

static func serialize_vector2(v: Vector2) -> Dictionary:
    return {"x": v.x, "y": v.y}

static func deserialize_vector2(d: Dictionary) -> Vector2:
    return Vector2(d.get("x", 0), d.get("y", 0))

static func serialize_vector3(v: Vector3) -> Dictionary:
    return {"x": v.x, "y": v.y, "z": v.z}

static func deserialize_vector3(d: Dictionary) -> Vector3:
    return Vector3(d.get("x", 0), d.get("y", 0), d.get("z", 0))

static func serialize_color(c: Color) -> Dictionary:
    return {"r": c.r, "g": c.g, "b": c.b, "a": c.a}

static func deserialize_color(d: Dictionary) -> Color:
    return Color(d.get("r", 1), d.get("g", 1), d.get("b", 1), d.get("a", 1))

static func serialize_transform2d(t: Transform2D) -> Dictionary:
    return {
        "x": serialize_vector2(t.x),
        "y": serialize_vector2(t.y),
        "origin": serialize_vector2(t.origin)
    }

static func deserialize_transform2d(d: Dictionary) -> Transform2D:
    return Transform2D(
        deserialize_vector2(d.get("x", {})),
        deserialize_vector2(d.get("y", {})),
        deserialize_vector2(d.get("origin", {}))
    )
```

## ConfigFile for Settings

### Settings Manager
```gdscript
# settings_manager.gd (Autoload)
extends Node

const SETTINGS_PATH := "user://settings.cfg"

var config := ConfigFile.new()

# Default settings
var defaults := {
    "audio": {
        "master_volume": 1.0,
        "music_volume": 0.8,
        "sfx_volume": 1.0,
        "voice_volume": 1.0
    },
    "video": {
        "fullscreen": false,
        "vsync": true,
        "resolution": "1920x1080",
        "quality": "high"
    },
    "controls": {
        "mouse_sensitivity": 1.0,
        "invert_y": false
    }
}

func _ready() -> void:
    load_settings()

func load_settings() -> void:
    var error := config.load(SETTINGS_PATH)

    if error != OK:
        # Create default settings
        apply_defaults()
        save_settings()

func save_settings() -> void:
    config.save(SETTINGS_PATH)

func apply_defaults() -> void:
    for section in defaults:
        for key in defaults[section]:
            config.set_value(section, key, defaults[section][key])

func get_setting(section: String, key: String) -> Variant:
    return config.get_value(section, key, defaults.get(section, {}).get(key))

func set_setting(section: String, key: String, value: Variant) -> void:
    config.set_value(section, key, value)
    save_settings()

# Convenience methods
func get_master_volume() -> float:
    return get_setting("audio", "master_volume")

func set_master_volume(value: float) -> void:
    set_setting("audio", "master_volume", value)
    apply_audio_settings()

func apply_audio_settings() -> void:
    AudioServer.set_bus_volume_db(
        AudioServer.get_bus_index("Master"),
        linear_to_db(get_master_volume())
    )
```

## Encrypted Save Data

### Basic Encryption
```gdscript
extends Node

const ENCRYPTION_KEY := "your-secret-key-here"
const SAVE_PATH := "user://encrypted_save.dat"

func save_encrypted(data: Dictionary) -> bool:
    var json_string := JSON.stringify(data)

    var file := FileAccess.open_encrypted_with_pass(
        SAVE_PATH,
        FileAccess.WRITE,
        ENCRYPTION_KEY
    )

    if not file:
        push_error("Failed to open encrypted file")
        return false

    file.store_string(json_string)
    file.close()
    return true

func load_encrypted() -> Dictionary:
    if not FileAccess.file_exists(SAVE_PATH):
        return {}

    var file := FileAccess.open_encrypted_with_pass(
        SAVE_PATH,
        FileAccess.READ,
        ENCRYPTION_KEY
    )

    if not file:
        push_error("Failed to open encrypted file")
        return {}

    var json_string := file.get_as_text()
    file.close()

    var json := JSON.new()
    if json.parse(json_string) != OK:
        return {}

    return json.data
```

### Save File Validation
```gdscript
extends Node

func save_with_checksum(data: Dictionary) -> bool:
    # Add checksum
    var json_string := JSON.stringify(data)
    var checksum := json_string.md5_text()

    var save_data := {
        "data": data,
        "checksum": checksum,
        "version": 1
    }

    return save_to_file(save_data)

func load_with_validation() -> Dictionary:
    var save_data := load_from_file()

    if save_data.is_empty():
        return {}

    # Validate checksum
    var json_string := JSON.stringify(save_data.get("data", {}))
    var expected_checksum := json_string.md5_text()

    if save_data.get("checksum") != expected_checksum:
        push_error("Save file corrupted!")
        return {}

    return save_data.get("data", {})
```

## Auto-Save System

### Auto-Save Manager
```gdscript
extends Node

signal auto_save_started
signal auto_save_completed

@export var auto_save_interval := 300.0  # 5 minutes
@export var max_auto_saves := 3

var auto_save_timer: Timer
var auto_save_enabled := true

func _ready() -> void:
    auto_save_timer = Timer.new()
    auto_save_timer.wait_time = auto_save_interval
    auto_save_timer.timeout.connect(_on_auto_save_timer)
    add_child(auto_save_timer)

    if auto_save_enabled:
        auto_save_timer.start()

func _on_auto_save_timer() -> void:
    perform_auto_save()

func perform_auto_save() -> void:
    auto_save_started.emit()

    # Rotate auto-saves
    rotate_auto_saves()

    # Save to newest slot
    var data := gather_save_data()
    save_game("autosave_0", data)

    auto_save_completed.emit()

func rotate_auto_saves() -> void:
    # Delete oldest
    var oldest := "user://autosave_%d.save" % (max_auto_saves - 1)
    if FileAccess.file_exists(oldest):
        DirAccess.remove_absolute(oldest)

    # Rename existing
    for i in range(max_auto_saves - 2, -1, -1):
        var current := "user://autosave_%d.save" % i
        var next := "user://autosave_%d.save" % (i + 1)
        if FileAccess.file_exists(current):
            DirAccess.rename_absolute(current, next)

func enable_auto_save(enabled: bool) -> void:
    auto_save_enabled = enabled
    if enabled:
        auto_save_timer.start()
    else:
        auto_save_timer.stop()
```

## Scene State Persistence

### Saveable Node Interface
```gdscript
# saveable.gd
class_name Saveable
extends Node

func get_save_data() -> Dictionary:
    # Override in child classes
    return {}

func load_save_data(data: Dictionary) -> void:
    # Override in child classes
    pass

# Example implementation
class_name SaveableChest
extends Saveable

var is_open := false
var contents: Array = []

func get_save_data() -> Dictionary:
    return {
        "node_path": get_path(),
        "is_open": is_open,
        "contents": contents.duplicate()
    }

func load_save_data(data: Dictionary) -> void:
    is_open = data.get("is_open", false)
    contents = data.get("contents", [])
    update_visual()
```

### World State Manager
```gdscript
extends Node

func save_world_state() -> Dictionary:
    var state := {
        "saveables": [],
        "destroyed": []
    }

    # Save all saveable nodes
    for node in get_tree().get_nodes_in_group("saveable"):
        if node is Saveable:
            state.saveables.append(node.get_save_data())

    # Track destroyed objects
    state.destroyed = destroyed_objects.duplicate()

    return state

func load_world_state(state: Dictionary) -> void:
    # Restore saveable nodes
    for save_data in state.get("saveables", []):
        var node_path: String = save_data.get("node_path", "")
        var node := get_node_or_null(node_path)

        if node is Saveable:
            node.load_save_data(save_data)

    # Remove destroyed objects
    for object_id in state.get("destroyed", []):
        var node := get_node_or_null(object_id)
        if node:
            node.queue_free()

var destroyed_objects: Array[String] = []

func mark_destroyed(node: Node) -> void:
    destroyed_objects.append(str(node.get_path()))
```

## Cloud Save Integration

### Abstract Cloud Save Interface
```gdscript
class_name CloudSaveProvider
extends RefCounted

signal save_completed(success: bool)
signal load_completed(success: bool, data: Dictionary)

func save_data(data: Dictionary) -> void:
    # Override in provider implementations
    pass

func load_data() -> void:
    # Override in provider implementations
    pass

func is_available() -> bool:
    return false

# Example Steam Cloud implementation stub
class_name SteamCloudProvider
extends CloudSaveProvider

func is_available() -> bool:
    # Check if Steam is running
    return false  # Implement Steam check

func save_data(data: Dictionary) -> void:
    # Steam cloud save implementation
    pass

func load_data() -> void:
    # Steam cloud load implementation
    pass
```

### Save Sync Manager
```gdscript
extends Node

var local_save_time := 0
var cloud_save_time := 0
var cloud_provider: CloudSaveProvider

func sync_saves() -> void:
    if not cloud_provider or not cloud_provider.is_available():
        return

    cloud_provider.load_data()
    await cloud_provider.load_completed

    # Compare timestamps
    if cloud_save_time > local_save_time:
        # Cloud is newer, download
        apply_cloud_save()
    elif local_save_time > cloud_save_time:
        # Local is newer, upload
        upload_local_save()
    # If equal, no action needed

func handle_save_conflict() -> int:
    # Return: 0 = use local, 1 = use cloud, 2 = cancel
    # Show UI for user to decide
    return 0
```
