# 组件文档格式规范

本文档定义了所有组件文档必须遵循的标准格式。

## ⚠️ 重要：确定正确的导出名称

在编写文档前，**必须**先检查 `/packages/atom-ui-mobile/src/index.ts` 文件，确认组件的实际导出名称。导出名称可能与组件目录名不同！

**常见导出名称示例**:
- `qr-code` 目录 → 导出为 `QrCode`（不是 `QRCode`）
- `message` 目录 → 导出为小写 `message`
- `time-select` 目录 → 导出为 `TimeSelect`
- `result-page` → `ResultPage`
- `search-bar` → `SearchBar`

**引用方式必须使用实际导出名称**:
```typescript
// ✅ 正确 - 使用 index.ts 中定义的导出名称
import { QrCode, message, TimeSelect } from '@evanfang/atom-ui-mobile';

// ❌ 错误 - 不要猜测组件名称
import { QRCode, Message, TimeSelectPanel } from '@evanfang/atom-ui-mobile';
```

## 文档命名规则

- **位置**: 组件目录下
- **命名**: `index.zh-CN.md`
- **示例**: `components/button/index.zh-CN.md`

## 标准文档模板

```markdown
# 技术文档

## 引用方式
**注意：组件名称必须与 src/index.ts 中的导出名称一致**

import { ComponentName } from '@evanfang/atom-ui-mobile';

## 功能类型
[工具/组件]

## 功能名称
[组件/工具名称]

## 功能描述
[组件/工具功能描述，包含适用场景和核心特性]

## 何时使用
[说明组件/工具在什么情况下使用]

## 使用示例
[给出组件/工具的使用示例代码]

## API
[仅包含组件/工具 API，包含属性名、类型、说明、默认值，详细列出继承的第三方组件的所有属性。若存在多个组件/功能，需分开列出各组件/功能的 API]
| 属性名 | 类型 | 说明 | 默认值 |
|-------|------|-----|-------|
| {prop1} | {type1} | {description1} | {default1} |
| {prop2} | {type2} | {description2} | {default2} |

## 类型描述
[仅包含组件/工具类型描述，包含类型名、类型详情、必填、默认值、说明，不要重复列出类型内部的字段]
| 类型名 | 类型详情 | 必填 | 默认值 | 说明 |
|-------|------|-----|-------|------|
| {type1} | {typeDetail1} | {required1} | {default1} | {description1} |
| {type2} | {typeDetail2} | {required2} | {default2} | {description2} |

## 主题变量(可选)
若代码中无需要暴露的自定义主题变量，需在此说明。
| Token 名称       | 描述     | 类型             | 默认值 |
| ---------------- | -------- | ---------------- | ------ |
| {name1} | {description1} | (type1) | {default1}    |
| {name2} | {description2} | (type2) | {default2}    |
```

## 编写规则

1. **独立理解组件**: 不要直接复制代码注释，需独立分析组件实现逻辑
2. **完整的API文档**: 必须列出所有Props属性及其类型、说明、默认值
3. **继承的API**: 如果组件继承自第三方组件库（如Ant Design），必须完整列出所有继承的API，不能简化
4. **类型定义**: 清晰描述所有自定义TypeScript类型
5. **主题变量**: 如果组件支持主题定制，列出所有CSS变量；如果没有，明确说明"无"
6. **实用示例**: 提供真实可用的代码示例，展示主要使用场景

## 不同组件类型的特殊要求

### React组件
- 重点描述Props接口
- 列出所有事件处理器（onXxx）
- 说明组件的状态管理（如有）
- 提供完整的交互示例

### Hooks
- 说明Hook的用途和返回值
- 详细描述参数类型和含义
- 提供使用场景示例
- 注意副作用和依赖项

### 工具函数
- 说明函数的输入输出
- 列出所有参数及其类型
- 提供使用示例和边界情况处理
- 说明算法复杂度（如相关）

### 类型定义
- 描述类型的用途
- 列出所有属性和可选性
- 提供类型使用示例

## 质量检查清单

- [ ] 文档路径与组件路径一致
- [ ] 引用方式正确
- [ ] 功能描述清晰完整
- [ ] API列表完整无遗漏
- [ ] 类型定义准确
- [ ] 使用示例可运行
- [ ] 主题变量明确（存在或说明无）
- [ ] 格式符合Markdown规范
