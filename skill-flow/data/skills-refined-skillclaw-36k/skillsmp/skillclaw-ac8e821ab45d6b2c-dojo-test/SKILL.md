---
name: dojo-test
description: Use this skill when you need to write tests for Dojo models and systems, ensuring game logic correctness and state verification.
---

# Dojo Test Generation

Write comprehensive tests for your Dojo models and systems using Cairo's test framework and Dojo's test utilities.

## When to Use This Skill

- "Write tests for the move system"
- "Test the Position model"
- "Add unit tests for combat logic"
- "Create integration tests"

## What This Skill Does

Generates test files with:
- `spawn_test_world()` setup
- Model and system registration
- Test functions with assertions
- Cheat code usage for manipulating execution context
- State verification

## Quick Start

**Interactive mode:**
```
"Write tests for the spawn system"
```
I'll ask about:
- What to test (models, systems, or both)
- Test scenarios (happy path, edge cases)
- State assertions needed

**Direct mode:**
```
"Test that the move system correctly updates Position"
```

## Running Tests

```bash
# Run all tests
sozo test

# Run specific test
sozo test test_spawn
```

## Test Structure

### Basic Test Pattern

```cairo
#[cfg(test)]
mod tests {
    use dojo::model::{ModelStorage, ModelValueStorage};
    use dojo::world::WorldStorageTrait;
    use dojo_cairo_test::{spawn_test_world, NamespaceDef, TestResource};
    use super::{Position, IActionsDispatcher, IActionsDispatcherTrait};

    #[test]
    fn test_spawn() {
        // 1. Set up test world
        let ndef = NamespaceDef {
            namespace: "dojo",
            resources: [
                TestResource::Model(m_Position::TEST_CLASS_HASH),
                TestResource::Contract(actions::TEST_CLASS_HASH),
            ].span()
        };
        let mut world = spawn_test_world([ndef].span());

        // 2. Deploy system
        let actions_address = world.deploy_contract("actions", actions::TEST_CLASS_HASH);
        let actions = IActionsDispatcher { contract_address: actions_address };

        // 3. Execute action
        actions.spawn();

        // 4. Verify results
        let player = starknet::get_caller_address();
        let position: Position = world.read_model(player);
        assert(position.x == 0, 'wrong x');
        assert(position.y == 0, 'wrong y');
    }
}
```

### Unit Tests

Test individual functions:
```cairo
#[test]
fn test_model_creation() {
    let position = Position { player: 0x123.try_into().unwrap(), x: 5, y: 10 };
    assert(position.x == 5, 'x should be 5');
}
```

### Integration Tests

Create a `tests` directory for system integration tests:
```cairo
// tests/test_move.cairo

#[cfg(test)]
mod tests {
    use dojo::model::{ModelStorage, ModelValueStorage, ModelStorageTest};
    use dojo::world::WorldStorageTrait;
    use dojo_cairo_test::{spawn_test_world, NamespaceDef, TestResource, ContractDefTrait};

    use dojo_starter::systems::actions::{actions, IActionsDispatcher, IActionsDispatcherTrait};
    use dojo_starter::models::{Position, m_Position, Moves, m_Moves, Direction};

    // Add your integration tests here
}
```