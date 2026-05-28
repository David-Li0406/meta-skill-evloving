---
name: sage-system-design
description: Use this skill when implementing advanced system features such as state recovery, fault tolerance, and adaptive learning mechanisms.
---

# Sage 系统设计指南

## 概述

Sage 的系统设计模块结合了检查点系统、恢复模式和学习系统，提供以下功能：

- **状态快照与恢复**: 保存和恢复系统状态，支持事务性操作。
- **容错机制**: 通过熔断器、限流器和重试策略确保系统的稳定性。
- **用户偏好学习**: 识别用户行为模式并根据反馈调整系统行为。

## 检查点系统

### 概述

Sage 的 `checkpoints/` 模块提供：

- **状态快照**: 保存完整执行状态。
- **文件追踪**: 追踪所有文件变更。
- **回滚恢复**: 安全回滚到任意检查点。

### 检查点管理

#### 创建检查点

```rust
let checkpoint = manager.create_checkpoint(
    CheckpointType::Manual,
    Some("Before refactoring".to_string()),
).await?;
```

#### 恢复检查点

```rust
let result = manager.restore(&checkpoint_id, options).await?;
```

## 恢复模式

### 概述

Sage 的 `recovery/` 模块提供生产级容错能力：

- **熔断器 (Circuit Breaker)**: 防止级联故障。
- **限流器 (Rate Limiter)**: 控制 API 调用频率。
- **重试策略 (Retry Policy)**: 智能重试失败操作。

### 熔断器配置

```rust
let config = CircuitBreakerConfig {
    failure_threshold: 5,
    recovery_timeout: Duration::from_secs(30),
    success_rate_threshold: 0.5,
    window_size: 10,
};
```

### 限流器使用

```rust
let limiter = SlidingWindowRateLimiter::new(100, Duration::from_secs(60));
limiter.acquire().await?;
```

## 学习系统

### 概述

Sage 的 `learning/` 模块提供：

- **模式检测**: 识别用户行为模式。
- **偏好学习**: 学习用户代码风格和偏好。
- **纠正记录**: 记录和学习用户纠正。

### 学习引擎初始化

```rust
let config = LearningConfig {
    pattern_threshold: 3,
    confidence_decay: 0.1,
    storage_path: PathBuf::from("~/.config/sage/learning"),
    max_patterns: 1000,
};
let engine = LearningEngine::new(config).await?;
```

### 记录事件

```rust
engine.record_event(LearningEvent {
    event_type: LearningEventType::Correction,
    data: CorrectionData {
        original: "function getName()".to_string(),
        corrected: "fn get_name()".to_string(),
        context: "rust_code".to_string(),
    },
    timestamp: Utc::now(),
}).await?;
```

## 最佳实践

### 1. 渐进式学习

```rust
if pattern.confidence < CONFIDENCE_THRESHOLD {
    continue; // 不立即应用低置信度模式
}
```

### 2. 衰减机制

```rust
for pattern in &mut self.patterns {
    if days_unused > 7 {
        pattern.confidence *= 0.9; // 每周衰减 10%
    }
}
```

### 3. 用户反馈优先

```rust
if let Some(explicit) = user_preferences.get(key) {
    return explicit.clone();
}
```

## 配置建议

```rust
LearningConfig {
    pattern_threshold: 3,
    auto_apply_threshold: 0.8,
    min_confidence: 0.1,
    weekly_decay_rate: 0.1,
    max_patterns: 1000,
    storage_path: PathBuf::from("~/.config/sage/learning"),
}
```