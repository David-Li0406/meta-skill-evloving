---
name: dojo-system
description: Use this skill to create Dojo systems that implement game logic, modify model state, and handle player actions, such as player commands or automated logic.
---

# Dojo System Generation

Create Dojo systems (smart contracts) that implement your game's logic and modify model state.

## When to Use This Skill

- "Create a spawn system"
- "Add a move system that updates position"
- "Implement combat logic"
- "Generate a system for [game action]"

## What This Skill Does

Generates Cairo system contracts with:
- `#[dojo::contract]` attribute
- Interface definition with `#[starknet::interface]`
- System implementation
- World access (`world.read_model()`, `world.write_model()`)
- Event emissions with `#[dojo::event]`
- Optional: Authorization checks
- Optional: System tests

## Quick Start

**Interactive mode:**
```
"Create a system for player movement"
```

I'll ask about:
- System name
- Functions and their parameters
- Models used
- Authorization requirements

**Direct mode:**
```
"Create a move system that updates Position based on Direction"
```

## System Structure

A Dojo contract consists of an interface trait and a contract module:

```cairo
use dojo_starter::models::{Direction, Position};

// Define the interface
#[starknet::interface]
trait IActions<T> {
    fn spawn(ref self: T);
    fn move(ref self: T, direction: Direction);
}

// Dojo contract
#[dojo::contract]
pub mod actions {
    use super::{IActions, Direction, Position};
    use starknet::{ContractAddress, get_caller_address};
    use dojo_starter::models::{Vec2};

    use dojo::model::{ModelStorage, ModelValueStorage};
    use dojo::event::EventStorage;

    // Define a custom event
    #[derive(Copy, Drop, Serde)]
    #[dojo::event]
    pub struct Moved {
        #[key]
        pub player: ContractAddress,
        pub direction: Direction,
    }

    #[abi(embed_v0)]
    impl ActionsImpl of IActions<ContractState> {
        fn spawn(ref self: ContractState) {
            let mut world = self.world_default();
            let player = get_caller_address();

            // Read current position (defaults to zero if not set)
            let position: Position = world.read_model(player);

            // Set initial position
            let new_position = Position {
                player,
                vec: Vec2 { x: position.vec.x + 10, y: position.vec.y + 10 }
            };
            world.write_model(@new_position);
        }

        fn move(ref self: ContractState, direction: Direction) {
            let mut world = self.world_default();
            let player = get_caller_address();

            // Read current state
            let mut position: Position = world.read_model(player);

            // Modify state
            match direction {
                Direction::Up => position.vec.y += 1,
                Direction::Down => position.vec.y -= 1,
                Direction::Left => position.vec.x -= 1,
                Direction::Right => position.vec.x += 1,
            }

            // Write updated state
            world.write_model(@position);
            // Emit event
            world.emit_event(Moved { player, direction });
        }
    }
}
```