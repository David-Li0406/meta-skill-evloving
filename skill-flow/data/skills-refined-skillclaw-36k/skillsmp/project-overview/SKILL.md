---
name: Project Overview
description: Dataforge 项目结构、核心模块及测试流程概览
---

# Dataforge 项目概览

Dataforge 是一个功能类似于 `freezed` + `json_serializable` 的数据类生成库。

## 核心模块结构

*   **[dataforge_base](../../../dataforge_base)**
    包含核心的代码生成逻辑 (Model, Parser, Writer)。这是 `cli` 和 `generator` 的共同基础。

*   **[cli](../../../cli)**
    命令行工具，用于独立生成代码。
    *   入口: `bin/dataforge.dart`
    *   依赖 `dataforge_base`

*   **[generator](../../../generator)**
    基于 `build_runner` 的生成器实现。
    *   用于 `flutter pub run build_runner build`
    *   依赖 `dataforge_base`

> **架构说明**: `generator` 和 `cli` 均依赖并共享 `dataforge_base` 的逻辑，确保生成行为一致。

## 开发与测试流程

### Generator 测试
主要基于 `build_test` 和 source_gen 的 `@ShouldGenerate` 注解进行测试。
*   **位置**: `generator/test/`
*   **方法**: 验证输入源代码 (source) 是否生成了预期的输出代码 (generated)。

### CLI 测试
采用集成测试 (Integration Testing) 流程，模拟真实使用场景：
1.  **编写 Case**: 在 `cli/test/models/` 等目录编写包含 `@DataForge` 注解的 Dart 文件。
2.  **生成代码**: 通过 `bin/dataforge.dart` 运行生成命令，处理这些 Case 文件。
3.  **验证逻辑**: 运行 `test` 目录下的测试脚本，直接引用并测试生成的代码逻辑（如 `toJson`, `fromJson` 等）。
