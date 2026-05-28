# Data Model Migration to CodeMap v2

## Status

Accepted

## Context

当前CodeMap项目存在两个版本的数据模型定义：

- `codemap.rs`: 旧版数据结构（Traces架构）
- `codemap_v2.rs`: 新版数据结构（Nodes + Edges架构）

并存导致：

1. 代码混淆：analyzer、storage、commands使用旧版
2. 类型不一致：前端TypeScript使用新版
3. 维护困难：新旧结构需要同步更新
4. 测试障碍：无法统一测试策略

## Decision

**统一使用 `codemap_v2.rs` 作为唯一数据模型**

### 迁移步骤

1. 更新 `storage.rs` - 适配v2的索引结构
2. 更新 `analyzer.rs` - 生成v2的CodeMap
3. 更新 `commands.rs` - 使用v2类型
4. 更新 `main.rs` - 移除旧module声明
5. 删除 `codemap.rs` - 仅保留v2版本
6. 验证前后端类型一致性

## Consequences

### 优点

- 统一数据模型，消除混淆
- 使用Windsurf Codemaps标准，提高兼容性
- 简化维护和测试
- 前后端类型自动同步（通过ts-rs可自动生成）

### 缺点

- 需要迁移现有数据（index.json）
- 分析器需要重写以生成Nodes/Edges
- 需要更新所有相关导入

### 迁移影响范围

- Rust后端：storage, analyzer, commands
- 前端：无需改动（已使用v2类型）
- 数据格式：需要迁移存储的codemaps

## Migration Notes

### 旧结构 (codemap.rs)

```rust
pub struct CodeMap {
    pub schema_version: u32,
    pub metadata: CodeMapMetadata,
    pub title: String,
    pub description: String,
    pub mermaid_diagram: String,
    pub traces: Vec<Trace>,
}
pub struct Trace {
    pub id: String,
    pub title: String,
    pub locations: Vec<Location>,
    pub trace_text_diagram: String,
    pub trace_guide: String,
}
```

### 新结构 (codemap_v2.rs)

```rust
pub struct CodeMap {
    pub schema_version: String,
    pub codemap_id: String,
    pub title: String,
    pub prompt: String,
    pub nodes: Vec<Node>,
    pub edges: Vec<Edge>,
    pub created_at: DateTime<Utc>,
    pub repo: RepoInfo,
    pub generation: GenerationConfig,
}
pub struct Node {
    pub node_id: String,
    pub title: String,
    pub summary: String,
    pub children: Vec<String>,
    pub code_refs: Vec<CodeRef>,
    pub trace_guide: TraceGuide,
}
```

### 映射关系

- `Trace` → `Node` (每个trace作为一个节点)
- `Location` → `CodeRef` (code_refs数组)
- `trace_text_diagram` → `Node.summary` + `Node.children`
- `trace_guide` → `TraceGuide.short/long`
- `mermaid_diagram` → `edges` (自动生成调用边)

## Date

2026-01-14
