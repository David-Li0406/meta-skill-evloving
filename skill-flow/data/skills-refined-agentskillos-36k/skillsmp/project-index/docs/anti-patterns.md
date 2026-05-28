# ⚠️ 禁止的错误模式

测试修复和代码生成时，**严禁**以下反模式。

## 1. 为测试通过而修改实现代码

```
❌ 错误：测试期望 event 名为 "tool:failed"，实现是 "tool.failed"
         → 修改实现代码把 "tool.failed" 改成 "tool:failed"

✅ 正确：检查项目约定，修改测试断言匹配实际行为
         或者确认是 bug 后单独提 fix commit
```

**原则**：测试验证现有行为，不驱动实现变更（除非是 TDD 新功能）。

## 2. 创建 Shim/桥接文件

```
❌ 错误：测试 import 路径 "runtime/compression/xxx.js" 不存在
         → 创建 shim 文件 re-export 真实模块

✅ 正确：修正测试的 import 路径指向实际模块位置
```

**原则**：一个模块只有一个入口点，不创建重导出 shim。

## 3. 事件名/API 破坏性变更

```
❌ 错误：统一事件名格式 "domain:action" → "domain.action"
         混在测试修复 commit 中

✅ 正确：破坏性变更需要：
         1. 独立 commit/PR
         2. 更新所有订阅者
         3. 更新文档
         4. 明确标注 BREAKING CHANGE
```

## 4. 为兼容添加 Polyfill/Wrapper

```
❌ 错误：测试期望 manager.getAllSkillMetadata() 方法
         → 在 index.js 中动态添加 prototype 方法

✅ 正确：检查是否测试了不存在的 API
         如需新 API，在实现模块中正式添加
```

## 5. 重复 Emit 事件

```
❌ 错误：为兼容新旧格式，同时 emit 两种事件名
         emit("design:phase.transition", ...)
         emit("design.phase.transition", ...)

✅ 正确：选择一种格式，统一使用
```

## 检查清单

修复测试前，问自己：

- [ ] 是修改测试还是修改实现？（优先修改测试）
- [ ] 是否创建了新的 re-export 文件？（不应该）
- [ ] 是否改变了公开 API/事件名？（需要独立处理）
- [ ] 修改是否只影响测试文件？（理想情况）

## 发现问题时的处理

如果发现实现确实有 bug：

1. **分离 commit** — 测试修复和 bug 修复分开提交
2. **明确标注** — bug 修复 commit 说明问题和影响
3. **更新文档** — 如涉及 API 变更，同步更新 CLAUDE.md

## 真实案例

### 案例 1: Shim 泛滥

问题：测试使用路径 `runtime/compression/cicada-compressor.js`，但实际模块在 `plugins/compression/impl/cicada-compressor.js`。

错误做法：创建 `runtime/compression/` 目录，添加 shim 文件 re-export 实际模块。

正确做法：修改测试的 import 路径。

### 案例 2: 事件名混乱

问题：代码中事件名混用 `:` 和 `.` 分隔符。

错误做法：在测试修复中顺便统一格式。

正确做法：
1. 先完成测试修复（匹配现有行为）
2. 如需统一格式，单独 PR 处理
3. 更新所有订阅者和文档

### 案例 3: 动态添加方法

问题：测试调用 `manager.getCatalogPrompt()`，但 SkillsManager 没有这个方法。

错误做法：
```javascript
if (!SkillsManager.prototype.getCatalogPrompt) {
  SkillsManager.prototype.getCatalogPrompt = function() { ... };
}
```

正确做法：检查测试是否正确，如确需此方法则在 manager.js 中正式实现。
