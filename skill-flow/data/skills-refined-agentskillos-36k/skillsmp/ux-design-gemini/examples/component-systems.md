# Component Systems and Design System Examples

Examples for creating design systems, component libraries, style guides, and pattern libraries using Gemini.

---

## Example 1: Design System Documentation

Create comprehensive design system documentation.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: design-system-doc
backend: gemini
workdir: /path/to/design-system
---CONTENT---
为移动端App创建设计系统文档：

包含以下部分：
1. 设计原则 (3-5条核心原则)
2. 色彩系统 (主色、辅助色、语义色、中性色)
3. 字体系统 (字阶、字重、行高)
4. 间距系统 (基于4px或8px grid)
5. 圆角和阴影规范
6. 图标规范

输出Markdown格式文档，包含使用示例。
---END---
EOF
```

### Expected Output

```markdown
# 移动端App设计系统

## 设计原则

1. **简洁优先** - 去除不必要的视觉元素，聚焦核心功能
2. **一致性** - 统一的组件、颜色、间距，减少用户学习成本
3. **可访问性** - 符合WCAG 2.1 Level AA标准
4. **响应式** - 适配不同屏幕尺寸和方向
5. **性能优先** - 轻量级设计，减少资源占用

---

## 色彩系统

### 主色 (Primary)

```css
--primary-50:  #E3F2FD;  /* 最浅 */
--primary-100: #BBDEFB;
--primary-200: #90CAF9;
--primary-300: #64B5F6;
--primary-400: #42A5F5;
--primary-500: #2196F3;  /* 主色 */
--primary-600: #1E88E5;
--primary-700: #1976D2;
--primary-800: #1565C0;
--primary-900: #0D47A1;  /* 最深 */
```

**使用场景:**
- Primary-500: 主按钮、链接、选中状态
- Primary-100: 浅色背景（如Tag、Badge）
- Primary-700: 深色模式主色

### 语义色 (Semantic)

| 颜色 | HEX | 用途 |
|------|-----|------|
| **Success** | `#4CAF50` | 成功提示、完成状态 |
| **Warning** | `#FF9800` | 警告提示、待处理 |
| **Error** | `#F44336` | 错误提示、删除操作 |
| **Info** | `#2196F3` | 信息提示、提醒 |

### 中性色 (Neutral)

```css
--gray-50:  #FAFAFA;  /* 背景色 */
--gray-100: #F5F5F5;  /* 卡片背景 */
--gray-200: #EEEEEE;  /* 分隔线 */
--gray-300: #E0E0E0;  /* 边框 */
--gray-400: #BDBDBD;  /* 禁用状态 */
--gray-500: #9E9E9E;  /* 图标 */
--gray-600: #757575;  /* 次要文本 */
--gray-700: #616161;
--gray-800: #424242;
--gray-900: #212121;  /* 主要文本 */
```

---

## 字体系统

### 字阶 (Type Scale)

基于1.25比例（Major Third）

| 名称 | 大小 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| **Display** | 40px | 48px | 700 | 营销页大标题 |
| **H1** | 32px | 40px | 700 | 页面标题 |
| **H2** | 24px | 32px | 600 | 区块标题 |
| **H3** | 20px | 28px | 600 | 小标题 |
| **Body Large** | 18px | 28px | 400 | 重要正文 |
| **Body** | 16px | 24px | 400 | 正文、输入框 |
| **Body Small** | 14px | 20px | 400 | 次要文本 |
| **Caption** | 12px | 16px | 400 | 辅助说明 |

### 字重 (Font Weight)

```css
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

**使用规则:**
- 标题使用600或700
- 正文使用400
- 强调文本使用500或600
- 避免使用300以下（移动端可读性差）

---

## 间距系统

### 8px Grid System

所有间距必须是8的倍数。

**间距值:**
```css
--space-0: 0px;
--space-1: 4px;   /* 特殊情况：图标与文字 */
--space-2: 8px;   /* 最小间距 */
--space-3: 12px;  /* 小间距 */
--space-4: 16px;  /* 常规间距 */
--space-5: 20px;
--space-6: 24px;  /* 中等间距 */
--space-8: 32px;  /* 大间距 */
--space-10: 40px;
--space-12: 48px; /* 区块间距 */
--space-16: 64px; /* 超大间距 */
```

**使用指南:**

| 场景 | 间距 | 示例 |
|------|------|------|
| 组件内元素 | 8-12px | 图标与文字 |
| 相关组件 | 16px | 表单字段间距 |
| 区块间距 | 24-32px | 卡片与卡片 |
| 页面边距 | 16px (移动), 24px (桌面) | Container padding |

---

## 圆角系统

```css
--radius-none: 0px;
--radius-sm: 4px;   /* 小组件：Tag, Badge */
--radius-md: 8px;   /* 按钮、输入框 */
--radius-lg: 12px;  /* 卡片 */
--radius-xl: 16px;  /* 大卡片、弹窗 */
--radius-full: 9999px; /* 圆形：头像、Pill按钮 */
```

---

## 阴影系统

```css
/* 小阴影：悬浮元素 */
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12),
             0 1px 2px rgba(0, 0, 0, 0.06);

/* 中阴影：卡片 */
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07),
             0 2px 4px rgba(0, 0, 0, 0.05);

/* 大阴影：弹窗 */
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1),
             0 4px 6px rgba(0, 0, 0, 0.05);

/* 超大阴影：模态框 */
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15),
             0 10px 10px rgba(0, 0, 0, 0.04);
```

**使用场景:**
- shadow-sm: 按钮悬停
- shadow-md: 卡片默认
- shadow-lg: 下拉菜单、Tooltip
- shadow-xl: Modal、Drawer

---

## 图标规范

### 图标尺寸

```css
--icon-xs: 16px;  /* 小图标：Tag内、表单提示 */
--icon-sm: 20px;  /* 常规图标：按钮 */
--icon-md: 24px;  /* 默认图标：导航 */
--icon-lg: 32px;  /* 大图标：功能入口 */
--icon-xl: 48px;  /* 超大图标：Empty State */
```

### 图标库

使用统一图标库（推荐 Material Icons 或 Heroicons）

**样式:**
- 线性图标优先（2px描边）
- 填充图标用于激活状态
- 保持视觉重量一致

---

## 使用示例

### 按钮组件

```css
.btn-primary {
  padding: var(--space-3) var(--space-6);    /* 12px 24px */
  background: var(--primary-500);
  color: white;
  border-radius: var(--radius-md);           /* 8px */
  font-size: 16px;
  font-weight: var(--font-semibold);         /* 600 */
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background: var(--primary-600);
  box-shadow: var(--shadow-md);
}
```

### 卡片组件

```css
.card {
  background: white;
  border-radius: var(--radius-lg);           /* 12px */
  padding: var(--space-6);                   /* 24px */
  box-shadow: var(--shadow-md);
  margin-bottom: var(--space-6);             /* 24px */
}

.card-title {
  font-size: 20px;
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--space-4);             /* 16px */
}
```

» 写入 design-system-doc.md
✓ design-system-doc 13.5s
```

---

## Example 2: Component Library Specification

Document reusable UI components.

### Command

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: component-library
backend: gemini
workdir: /path/to/components
---CONTENT---
创建组件库文档，包含10个常用组件：

组件：
1. Button (主按钮、次要按钮、文字按钮)
2. Input (文本输入、密码、搜索)
3. Select (下拉选择)
4. Checkbox & Radio
5. Switch (开关)
6. Card (卡片)
7. Modal (模态框)
8. Toast (轻提示)
9. Tag (标签)
10. Avatar (头像)

对每个组件，描述：
- 变体 (Variants)
- 状态 (States)
- 属性 (Props)
- 使用场景
- 代码示例（伪代码）
---END---
EOF
```

---

## Example 3: Style Guide Creation

Create comprehensive brand style guide.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: style-guide
backend: gemini
workdir: /path/to/styleguide
---CONTENT---
为品牌创建视觉风格指南：

内容：
1. Logo使用规范（标准版、简化版、单色版）
2. 品牌色彩（主色、辅助色、禁用色）
3. 字体系统（标题字体、正文字体）
4. 摄影风格（照片类型、色调、构图）
5. 插画风格（线条、色彩、元素）
6. 语气和用词（品牌声音）
7. Do's and Don'ts（正确和错误示例）

输出Markdown文档，包含视觉示例描述。
---END---
EOF
```

---

## Example 4: Pattern Library

Document interaction patterns and best practices.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: pattern-library
backend: gemini
workdir: /path/to/patterns
---CONTENT---
创建交互模式库，包含常见设计模式：

模式：
1. 表单验证（实时验证 vs 提交后验证）
2. 搜索（即时搜索 vs 手动触发）
3. 加载反馈（骨架屏 vs Spinner vs 进度条）
4. 空状态（无数据、无搜索结果、首次使用）
5. 错误处理（行内错误 vs Toast vs Banner）
6. 确认操作（二次确认 vs 撤销操作）
7. 翻页（无限滚动 vs 分页 vs 加载更多）
8. 导航（Tab vs Drawer vs Bottom Sheet）

对每个模式，描述：
- 使用场景
- 优缺点
- 最佳实践
- 示例应用
---END---
EOF
```

---

## Tips for Component Systems

1. **Design System**
   - Start with foundations (colors, typography, spacing)
   - Use design tokens (CSS variables, JSON)
   - Version control system updates
   - Provide migration guides

2. **Component Library**
   - Document all states (default, hover, active, disabled, error)
   - Provide accessibility guidelines
   - Include code examples
   - Keep components atomic (single responsibility)

3. **Style Guide**
   - Show don'ts, not just dos
   - Include real examples from products
   - Make it searchable
   - Update quarterly

4. **Pattern Library**
   - Base on actual user research
   - Provide decision trees (when to use X vs Y)
   - Include performance considerations
   - Link to code implementations

---

## Related Resources

- [references/design-principles.md](../references/design-principles.md) - Design principles foundation
- [references/design-workflow.md](../references/design-workflow.md) - Design system in workflow
- [examples/wireframes-mockups.md](./wireframes-mockups.md) - Using design system in mockups
- [SKILL.md](../SKILL.md) - Gemini basic usage
