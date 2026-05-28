# Bevy ECS Patterns

## Basic App

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, (movement, collision))
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2dBundle::default());
}
```

## Components

```rust
#[derive(Component)]
struct Player {
    speed: f32,
}

#[derive(Component)]
struct Health(f32);

#[derive(Component)]
struct Velocity(Vec2);

// Bundle for related components
#[derive(Bundle)]
struct PlayerBundle {
    player: Player,
    health: Health,
    velocity: Velocity,
    sprite: SpriteBundle,
}
```

## Spawning Entities

```rust
fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    // Simple entity
    commands.spawn((
        Player { speed: 200.0 },
        Health(100.0),
        Velocity(Vec2::ZERO),
        SpriteBundle {
            texture: asset_server.load("player.png"),
            transform: Transform::from_xyz(0.0, 0.0, 0.0),
            ..default()
        },
    ));

    // With bundle
    commands.spawn(PlayerBundle {
        player: Player { speed: 200.0 },
        health: Health(100.0),
        velocity: Velocity(Vec2::ZERO),
        sprite: SpriteBundle::default(),
    });

    // With children
    commands.spawn(SpriteBundle::default())
        .with_children(|parent| {
            parent.spawn(SpriteBundle::default());
        });
}
```

## Systems

```rust
// Query for entities with components
fn movement(
    time: Res<Time>,
    input: Res<ButtonInput<KeyCode>>,
    mut query: Query<(&Player, &mut Transform)>,
) {
    for (player, mut transform) in &mut query {
        let mut direction = Vec2::ZERO;
        
        if input.pressed(KeyCode::KeyW) { direction.y += 1.0; }
        if input.pressed(KeyCode::KeyS) { direction.y -= 1.0; }
        if input.pressed(KeyCode::KeyA) { direction.x -= 1.0; }
        if input.pressed(KeyCode::KeyD) { direction.x += 1.0; }
        
        if direction != Vec2::ZERO {
            direction = direction.normalize();
            transform.translation.x += direction.x * player.speed * time.delta_seconds();
            transform.translation.y += direction.y * player.speed * time.delta_seconds();
        }
    }
}

// Query filters
fn update_enemies(
    query: Query<&mut Health, (With<Enemy>, Without<Player>)>,
) {
    // Only entities with Enemy, without Player
}
```

## Resources

```rust
#[derive(Resource)]
struct GameState {
    score: u32,
    level: u32,
}

#[derive(Resource, Default)]
struct GameTimer(Timer);

fn setup(mut commands: Commands) {
    commands.insert_resource(GameState { score: 0, level: 1 });
    commands.insert_resource(GameTimer(Timer::from_seconds(1.0, TimerMode::Repeating)));
}

fn update_score(
    mut game: ResMut<GameState>,
    time: Res<Time>,
    mut timer: ResMut<GameTimer>,
) {
    if timer.0.tick(time.delta()).just_finished() {
        game.score += 10;
    }
}
```

## Events

```rust
#[derive(Event)]
struct CollisionEvent {
    entity_a: Entity,
    entity_b: Entity,
}

fn detect_collisions(
    query: Query<(Entity, &Transform), With<Collider>>,
    mut events: EventWriter<CollisionEvent>,
) {
    // Check collisions
    events.send(CollisionEvent {
        entity_a: e1,
        entity_b: e2,
    });
}

fn handle_collisions(
    mut events: EventReader<CollisionEvent>,
    mut commands: Commands,
) {
    for event in events.read() {
        commands.entity(event.entity_b).despawn();
    }
}

// Register event
App::new()
    .add_event::<CollisionEvent>()
    .add_systems(Update, (detect_collisions, handle_collisions).chain())
```

## States

```rust
#[derive(States, Debug, Clone, PartialEq, Eq, Hash, Default)]
enum GameState {
    #[default]
    Menu,
    Playing,
    Paused,
    GameOver,
}

fn main() {
    App::new()
        .init_state::<GameState>()
        .add_systems(OnEnter(GameState::Playing), setup_game)
        .add_systems(OnExit(GameState::Playing), cleanup_game)
        .add_systems(Update, game_logic.run_if(in_state(GameState::Playing)))
        .run();
}

fn pause_game(
    input: Res<ButtonInput<KeyCode>>,
    state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if input.just_pressed(KeyCode::Escape) {
        match state.get() {
            GameState::Playing => next_state.set(GameState::Paused),
            GameState::Paused => next_state.set(GameState::Playing),
            _ => {}
        }
    }
}
```

## Asset Loading

```rust
#[derive(Resource)]
struct GameAssets {
    player: Handle<Image>,
    enemy: Handle<Image>,
    font: Handle<Font>,
}

fn load_assets(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.insert_resource(GameAssets {
        player: asset_server.load("player.png"),
        enemy: asset_server.load("enemy.png"),
        font: asset_server.load("fonts/main.ttf"),
    });
}
```
