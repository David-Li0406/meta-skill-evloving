---
name: audio-system
description: Implements audio systems using AudioStreamPlayer, audio buses, spatial audio, and dynamic music. Use when adding sound effects, music, and ambient audio.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Audio System

When implementing audio, follow these patterns for immersive and performant sound design.

## Audio Basics

### Playing Sounds
```gdscript
extends Node2D

@onready var sfx_player: AudioStreamPlayer2D = $SFXPlayer

func play_sound(stream: AudioStream, volume_db: float = 0.0) -> void:
    sfx_player.stream = stream
    sfx_player.volume_db = volume_db
    sfx_player.play()

func play_sound_pitched(stream: AudioStream, pitch_range: float = 0.1) -> void:
    sfx_player.stream = stream
    sfx_player.pitch_scale = 1.0 + randf_range(-pitch_range, pitch_range)
    sfx_player.play()

# One-shot sound (auto-cleanup)
func play_oneshot(stream: AudioStream, position: Vector2) -> void:
    var player := AudioStreamPlayer2D.new()
    player.stream = stream
    player.position = position
    player.bus = "SFX"
    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)
```

### Audio Pool
```gdscript
class_name AudioPool
extends Node

var pool: Array[AudioStreamPlayer] = []
var pool_size := 10

func _ready() -> void:
    for i in range(pool_size):
        var player := AudioStreamPlayer.new()
        player.bus = "SFX"
        add_child(player)
        pool.append(player)

func get_player() -> AudioStreamPlayer:
    for player in pool:
        if not player.playing:
            return player

    # All players busy, return first (will cut off)
    return pool[0]

func play(stream: AudioStream, volume: float = 0.0, pitch: float = 1.0) -> void:
    var player := get_player()
    player.stream = stream
    player.volume_db = volume
    player.pitch_scale = pitch
    player.play()

# 2D version
class_name AudioPool2D
extends Node

var pool: Array[AudioStreamPlayer2D] = []

func play_at(stream: AudioStream, position: Vector2) -> void:
    var player := get_available_player()
    player.stream = stream
    player.global_position = position
    player.play()
```

## Audio Bus System

### Bus Configuration
```gdscript
extends Node

func _ready() -> void:
    setup_audio_buses()

func setup_audio_buses() -> void:
    # Buses are typically set up in Project Settings
    # But can be modified at runtime

    # Get bus indices
    var master_idx := AudioServer.get_bus_index("Master")
    var music_idx := AudioServer.get_bus_index("Music")
    var sfx_idx := AudioServer.get_bus_index("SFX")

    # Set volumes (in dB)
    AudioServer.set_bus_volume_db(music_idx, linear_to_db(0.8))
    AudioServer.set_bus_volume_db(sfx_idx, linear_to_db(1.0))

func set_master_volume(linear: float) -> void:
    var idx := AudioServer.get_bus_index("Master")
    AudioServer.set_bus_volume_db(idx, linear_to_db(linear))

func set_music_volume(linear: float) -> void:
    var idx := AudioServer.get_bus_index("Music")
    AudioServer.set_bus_volume_db(idx, linear_to_db(linear))

func set_sfx_volume(linear: float) -> void:
    var idx := AudioServer.get_bus_index("SFX")
    AudioServer.set_bus_volume_db(idx, linear_to_db(linear))

func mute_bus(bus_name: String, mute: bool) -> void:
    var idx := AudioServer.get_bus_index(bus_name)
    AudioServer.set_bus_mute(idx, mute)
```

### Audio Effects
```gdscript
extends Node

func add_reverb_to_bus(bus_name: String) -> void:
    var idx := AudioServer.get_bus_index(bus_name)

    var reverb := AudioEffectReverb.new()
    reverb.room_size = 0.8
    reverb.damping = 0.5
    reverb.wet = 0.3

    AudioServer.add_bus_effect(idx, reverb)

func add_lowpass_filter(bus_name: String, cutoff_hz: float = 1000.0) -> void:
    var idx := AudioServer.get_bus_index(bus_name)

    var filter := AudioEffectLowPassFilter.new()
    filter.cutoff_hz = cutoff_hz
    filter.resonance = 0.5

    AudioServer.add_bus_effect(idx, filter)

func add_compressor(bus_name: String) -> void:
    var idx := AudioServer.get_bus_index(bus_name)

    var compressor := AudioEffectCompressor.new()
    compressor.threshold = -20
    compressor.ratio = 4
    compressor.attack_us = 20
    compressor.release_ms = 250

    AudioServer.add_bus_effect(idx, compressor)

func set_effect_enabled(bus_name: String, effect_idx: int, enabled: bool) -> void:
    var bus_idx := AudioServer.get_bus_index(bus_name)
    AudioServer.set_bus_effect_enabled(bus_idx, effect_idx, enabled)
```

## Music System

### Music Manager
```gdscript
# music_manager.gd (Autoload)
extends Node

@onready var music_player: AudioStreamPlayer = $MusicPlayer
@onready var crossfade_player: AudioStreamPlayer = $CrossfadePlayer

var current_track: AudioStream
var is_crossfading := false

func play_music(track: AudioStream, fade_duration: float = 1.0) -> void:
    if track == current_track:
        return

    current_track = track

    if music_player.playing and fade_duration > 0:
        crossfade(track, fade_duration)
    else:
        music_player.stream = track
        music_player.play()

func crossfade(new_track: AudioStream, duration: float) -> void:
    is_crossfading = true

    # Set up crossfade player
    crossfade_player.stream = new_track
    crossfade_player.volume_db = -80
    crossfade_player.play()

    # Tween volumes
    var tween := create_tween()
    tween.set_parallel(true)
    tween.tween_property(music_player, "volume_db", -80, duration)
    tween.tween_property(crossfade_player, "volume_db", 0, duration)

    await tween.finished

    # Swap players
    music_player.stop()
    music_player.stream = new_track
    music_player.volume_db = 0
    music_player.play()
    music_player.seek(crossfade_player.get_playback_position())
    crossfade_player.stop()

    is_crossfading = false

func stop_music(fade_duration: float = 1.0) -> void:
    if fade_duration > 0:
        var tween := create_tween()
        tween.tween_property(music_player, "volume_db", -80, fade_duration)
        await tween.finished

    music_player.stop()
    music_player.volume_db = 0
    current_track = null
```

### Adaptive Music
```gdscript
extends Node

enum MusicState { EXPLORE, COMBAT, BOSS, VICTORY }

var music_tracks := {
    MusicState.EXPLORE: preload("res://audio/music/explore.ogg"),
    MusicState.COMBAT: preload("res://audio/music/combat.ogg"),
    MusicState.BOSS: preload("res://audio/music/boss.ogg"),
    MusicState.VICTORY: preload("res://audio/music/victory.ogg")
}

var current_state: MusicState = MusicState.EXPLORE

func set_music_state(state: MusicState) -> void:
    if state == current_state:
        return

    current_state = state
    MusicManager.play_music(music_tracks[state])

# Layered adaptive music
class_name AdaptiveMusicPlayer
extends Node

var layers: Array[AudioStreamPlayer] = []
var layer_volumes: Array[float] = []

func setup_layers(streams: Array[AudioStream]) -> void:
    for stream in streams:
        var player := AudioStreamPlayer.new()
        player.stream = stream
        player.bus = "Music"
        player.volume_db = -80
        add_child(player)
        layers.append(player)
        layer_volumes.append(0.0)

func play_all() -> void:
    for player in layers:
        player.play()

func set_layer_volume(layer_idx: int, volume: float, fade_time: float = 0.5) -> void:
    if layer_idx >= layers.size():
        return

    layer_volumes[layer_idx] = volume
    var target_db := linear_to_db(volume) if volume > 0 else -80

    var tween := create_tween()
    tween.tween_property(layers[layer_idx], "volume_db", target_db, fade_time)

func set_intensity(intensity: float) -> void:
    # intensity 0-1 controls which layers are active
    for i in range(layers.size()):
        var threshold := float(i) / layers.size()
        var target_volume := 1.0 if intensity > threshold else 0.0
        set_layer_volume(i, target_volume)
```

### Beat Synchronization
```gdscript
extends Node

signal beat
signal bar

@export var bpm := 120.0
@export var beats_per_bar := 4

var beat_duration: float
var time_since_last_beat := 0.0
var current_beat := 0

func _ready() -> void:
    beat_duration = 60.0 / bpm

func _process(delta: float) -> void:
    time_since_last_beat += delta

    if time_since_last_beat >= beat_duration:
        time_since_last_beat -= beat_duration
        current_beat += 1
        beat.emit()

        if current_beat % beats_per_bar == 0:
            bar.emit()

func get_beat_progress() -> float:
    return time_since_last_beat / beat_duration

func sync_to_music(music_position: float) -> void:
    current_beat = int(music_position / beat_duration)
    time_since_last_beat = fmod(music_position, beat_duration)
```

## Spatial Audio

### 2D Positional Audio
```gdscript
extends AudioStreamPlayer2D

@export var max_distance := 500.0
@export var attenuation := 1.0

func _ready() -> void:
    # Configure 2D audio
    max_distance = max_distance
    attenuation = attenuation

    # Optional: Panning
    panning_strength = 1.0

# Doppler effect simulation
extends AudioStreamPlayer2D

var last_position: Vector2
var velocity: Vector2

func _physics_process(delta: float) -> void:
    velocity = (global_position - last_position) / delta
    last_position = global_position

    # Adjust pitch based on relative velocity to listener
    var listener_pos := get_viewport().get_camera_2d().global_position
    var to_listener := (listener_pos - global_position).normalized()
    var relative_velocity := velocity.dot(to_listener)

    var speed_of_sound := 343.0 * 10  # Scaled for game units
    var doppler_shift := speed_of_sound / (speed_of_sound + relative_velocity)

    pitch_scale = clamp(doppler_shift, 0.5, 2.0)
```

### 3D Positional Audio
```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # Distance model
    attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE

    # Distance settings
    unit_size = 10.0  # Distance at which volume is 0 dB
    max_distance = 100.0

    # Doppler
    doppler_tracking = AudioStreamPlayer3D.DOPPLER_TRACKING_PHYSICS_STEP

    # Directional
    emission_angle_enabled = true
    emission_angle_degrees = 45.0
    emission_angle_filter_attenuation_db = -12.0
```

### Audio Occlusion
```gdscript
extends AudioStreamPlayer3D

@export var occlusion_bus := "Occluded"
@export var normal_bus := "SFX"

var listener: Node3D

func _physics_process(_delta: float) -> void:
    if not listener:
        listener = get_viewport().get_camera_3d()

    if not listener:
        return

    check_occlusion()

func check_occlusion() -> void:
    var space := get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(
        global_position,
        listener.global_position
    )
    query.collision_mask = 1  # Walls layer

    var result := space.intersect_ray(query)

    if result.is_empty():
        # No occlusion
        bus = normal_bus
    else:
        # Occluded - use muffled bus
        bus = occlusion_bus
```

## Sound Design Patterns

### Footstep System
```gdscript
extends CharacterBody2D

var surface_sounds := {
    "grass": [
        preload("res://audio/sfx/footstep_grass_1.ogg"),
        preload("res://audio/sfx/footstep_grass_2.ogg")
    ],
    "stone": [
        preload("res://audio/sfx/footstep_stone_1.ogg"),
        preload("res://audio/sfx/footstep_stone_2.ogg")
    ],
    "wood": [
        preload("res://audio/sfx/footstep_wood_1.ogg"),
        preload("res://audio/sfx/footstep_wood_2.ogg")
    ]
}

var step_timer := 0.0
var step_interval := 0.4

func _physics_process(delta: float) -> void:
    if is_on_floor() and velocity.length() > 10:
        step_timer += delta
        if step_timer >= step_interval:
            step_timer = 0
            play_footstep()

func play_footstep() -> void:
    var surface := detect_surface()
    var sounds: Array = surface_sounds.get(surface, surface_sounds["stone"])
    var sound: AudioStream = sounds.pick_random()

    $FootstepPlayer.stream = sound
    $FootstepPlayer.pitch_scale = randf_range(0.9, 1.1)
    $FootstepPlayer.play()

func detect_surface() -> String:
    # Raycast down to detect surface
    var ray_result := get_world_2d().direct_space_state.intersect_ray(
        PhysicsRayQueryParameters2D.create(global_position, global_position + Vector2(0, 20))
    )

    if ray_result.is_empty():
        return "stone"

    var collider := ray_result.collider
    if collider.has_meta("surface_type"):
        return collider.get_meta("surface_type")

    return "stone"
```

### Impact Sounds
```gdscript
extends RigidBody2D

@export var impact_threshold := 100.0  # Minimum impact velocity

var impact_sounds: Array[AudioStream] = [
    preload("res://audio/sfx/impact_1.ogg"),
    preload("res://audio/sfx/impact_2.ogg")
]

var last_velocity: Vector2

func _physics_process(_delta: float) -> void:
    last_velocity = linear_velocity

func _on_body_entered(body: Node) -> void:
    var impact_speed := last_velocity.length()

    if impact_speed > impact_threshold:
        play_impact(impact_speed)

func play_impact(speed: float) -> void:
    var player := AudioStreamPlayer2D.new()
    player.stream = impact_sounds.pick_random()

    # Volume based on impact force
    var volume_ratio := clamp((speed - impact_threshold) / 500.0, 0, 1)
    player.volume_db = linear_to_db(volume_ratio)

    # Pitch variation
    player.pitch_scale = randf_range(0.8, 1.2)

    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)
```

### Ambient Audio
```gdscript
extends Node2D

@export var ambient_sounds: Array[AudioStream]
@export var min_interval := 5.0
@export var max_interval := 15.0
@export var volume_range := Vector2(-10, 0)
@export var spawn_radius := 200.0

var timer: Timer

func _ready() -> void:
    timer = Timer.new()
    timer.one_shot = true
    timer.timeout.connect(play_random_ambient)
    add_child(timer)
    schedule_next()

func schedule_next() -> void:
    timer.start(randf_range(min_interval, max_interval))

func play_random_ambient() -> void:
    var sound: AudioStream = ambient_sounds.pick_random()

    var player := AudioStreamPlayer2D.new()
    player.stream = sound
    player.volume_db = randf_range(volume_range.x, volume_range.y)

    # Random position around listener
    var offset := Vector2.from_angle(randf() * TAU) * randf_range(50, spawn_radius)
    player.global_position = global_position + offset

    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)

    schedule_next()
```
