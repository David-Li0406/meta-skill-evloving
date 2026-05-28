---
name: component-docs-batcher
description: 批量生成和维护Monorepo前端组件库文档。通过Git时间对比智能识别需更新的组件，自动生成任务清单并批量生成规范文档。支持：定期批量更新、单个组件维护、新组件初始化。自动识别主要组件文件（button/button.tsx），跳过index.ts/store/hooks等辅助文件，文档路径为组件目录下的index.zh-CN.md。
---

# Component Docs Batcher

批量生成和维护前端组件库文档的自动化工具。

## 核心功能

- **智能组件识别**: 识别主要组件文件（如button/button.tsx），跳过index.ts、store、hooks等辅助文件
- **Git时间对比**: 使用`git log`对比组件和文档的最后提交时间（比文件系统时间更准确）
- **任务清单生成**: 自动生成结构化的todos.md
- **批量文档生成**: 按规范批量生成完整组件文档（index.zh-CN.md）

## 工作流程

### 1. 扫描组件

```bash
# 扫描组件库
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/components

# 输出JSON格式
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/components --json
```

**识别规则**: 扫描一级子目录，识别同名.tsx/.jsx文件，跳过index.ts/*.store.ts/use*.ts等辅助文件和styles/__tests__等目录

**扫描结果**:
- ❌ 文档缺失：组件目录下没有index.zh-CN.md
- ⚠️ 文档过时：组件文件的git时间晚于文档
- ✅ 文档最新：不输出

### 2. 生成任务清单

```bash
npx ts-node .claude/skills/component-docs-batcher/scripts/generate-todos.ts /path/to/components /output/todos.md
```

生成包含统计信息、任务列表、使用说明、文档规范引用的todos.md

### 3. 分析组件结构

```bash
npx ts-node .claude/skills/component-docs-batcher/scripts/analyze-component.ts /path/to/Component.tsx --json
```

分析内容：组件类型、Props接口、TypeScript类型定义、导入依赖、代码示例

### 4. 批量生成文档

1. 读取组件源码（使用Read工具）
2. 理解组件逻辑（不依赖代码注释，独立理解）
3. 提取关键信息：Props接口、TypeScript类型、使用场景、第三方组件API
4. **确定导出名称**：⚠️ 必须检查`/packages/atom-ui-mobile/src/index.ts`确认实际导出名称
   - 例：`qr-code` → `QrCode`（不是`QRCode`）
   - 例：`message` → 小写`message`
   - 例：`time-select` → `TimeSelect`（无`default as`）
5. 按照[文档格式规范](references/docs-format.md)生成完整文档
6. 质量验证

**重要规则**:
- 文档路径：组件目录下的`index.zh-CN.md`
- 独立理解组件，不复制代码注释
- 完整列出所有API（特别是继承的第三方组件API）
- 提供真实可用的代码示例
- 导出名称必须与`src/index.ts`完全一致
- 引用示例：`import { Button } from '@evanfang/atom-ui-mobile';`

### 5. 更新任务状态

在todos.md中标记任务完成，完成后删除todos.md

## 使用场景

### 定期批量更新

```bash
# 1. 扫描组件库
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/components

# 2. 生成任务清单
npx ts-node .claude/skills/component-docs-batcher/scripts/generate-todos.ts /path/to/components

# 3. 按todos.md批量处理，完成后删除todos.md
```

### 单个组件维护

```bash
# 1. 分析组件
npx ts-node .claude/skills/component-docs-batcher/scripts/analyze-component.ts /path/to/Component.tsx

# 2. 生成/更新文档（位置：组件目录/index.zh-CN.md）
```

### 新组件文档初始化

```bash
# 扫描组件库，新组件会在"文档缺失"列表中显示
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/components
```

## 文档规范

详见[文档格式规范](references/docs-format.md)

**关键要求**: 完整的API表格（属性名、类型、说明、默认值）、TypeScript类型定义表格、真实可用的代码示例、主题变量列表或"无"的明确说明

## 资源

**scripts/**
- scan-components.ts: 扫描组件文件，对比修改时间，输出需更新/新增的组件列表（支持JSON）
- generate-todos.ts: 生成todos.md任务清单（含统计、步骤、规范引用）
- analyze-component.ts: 分析组件结构，提取Props、类型、依赖等

**references/**
- docs-format.md: 标准文档模板、编写规则、质量检查清单
