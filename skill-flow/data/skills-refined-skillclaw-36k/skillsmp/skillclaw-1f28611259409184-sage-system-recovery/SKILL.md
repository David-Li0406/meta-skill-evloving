---
name: sage-system-recovery
description: Use this skill when you need to implement state recovery, fault tolerance, or adaptive learning mechanisms in your system.
---

# Skill body

## Overview

The `sage-system-recovery` module provides unique capabilities for state recovery, fault tolerance, and adaptive learning. It includes features for managing checkpoints, implementing recovery patterns, and learning user preferences.

## Checkpoint Management

### Overview

The checkpoint system allows you to save the complete execution state, track file changes, and safely roll back to any checkpoint.

### Module Structure

```
checkpoints/
├── mod.rs              # Public interface
├── manager.rs          # Checkpoint manager
├── storage/            # Storage implementations
│   ├── mod.rs
│   ├── file.rs         # File storage
│   └── memory.rs       # In-memory storage (for testing)
├── snapshot.rs         # Snapshot types
├── diff.rs             # Difference calculation
└── restore.rs          # Restore logic
```

### Creating Checkpoints

```rust
let checkpoint = manager.create_checkpoint(
    CheckpointType::Manual,
    Some("Before refactoring".to_string()),
).await?;
```

### Restoring Checkpoints

```rust
let preview = manager.preview_restore(&checkpoint_id).await?;
```

## Recovery Patterns

### Overview

The recovery patterns module provides production-grade fault tolerance capabilities, including circuit breakers, rate limiters, and retry strategies.

### Circuit Breaker Configuration

```rust
let config = CircuitBreakerConfig {
    failure_threshold: 5,
    recovery_timeout: Duration::from_secs(30),
    half_open_max_calls: 3,
    success_rate_threshold: 0.5,
    window_size: 10,
};

let breaker = CircuitBreaker::new("llm-api", config);
```

### Using the Circuit Breaker

```rust
let result = breaker.call(|| async {
    llm_client.chat(request).await
}).await;
```

## Learning System

### Overview

The learning system module allows for pattern recognition, user preference learning, and adaptive behavior adjustments based on user feedback.

### Learning Engine Initialization

```rust
let config = LearningConfig {
    pattern_threshold: 3,
    confidence_decay: 0.1,
    storage_path: PathBuf::from("~/.config/sage/learning"),
    max_patterns: 1000,
};

let engine = LearningEngine::new(config).await?;
```

### Recording Learning Events

```rust
engine.record_event(LearningEvent {
    event_type: LearningEventType::Correction,
    data: CorrectionData {
        original: "function getName()".to_string(),
        corrected: "fn get_name()".to_string(),
        context: "rust_code".to_string(),
    },
}).await?;
```