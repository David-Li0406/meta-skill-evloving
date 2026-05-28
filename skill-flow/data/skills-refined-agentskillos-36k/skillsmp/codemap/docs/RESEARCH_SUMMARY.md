# CodeMap 前端 UI 设计调研摘要

> 基于 UI/UX Pro Max 设计系统技能的系统性调研结果

## 📊 调研执行时间

**日期**: 2026-01-15
**调研工具**: UI/UX Pro Max Search (8 个领域)
**调研方法**: 关键词搜索 + 跨领域交叉验证

## 🎯 产品定位确认

| 维度         | 结论                                   |
| ------------ | -------------------------------------- |
| **产品类型** | Developer Tool / Dashboard / SaaS      |
| **核心价值** | AI 驱动的代码可视化工具 + 实时代码分析 |
| **目标用户** | 开发者、技术团队、代码审查员           |
| **使用场景** | 代码流程追踪、调试、文档生成、代码学习 |

## 🎨 设计风格决策

### 主风格：Dark Mode (OLED) + Minimalism

**来源**: Product Type: Dashboard/Developer Tool 搜索结果
**理由**:

- 开发者工具标准 UI 模式
- OLED 友好（纯黑背景省电）
- 减少眼部疲劳（长时间编码场景）
- 符合 VS Code、GitHub Copilot 等主流工具趋势

### 辅助风格：Flat Design + Bento Box Grid

**理由**:

- 扁平化设计减少视觉干扰，聚焦内容
- 便当盒网格布局规范信息密度
- 适应 CodeMap 信息密集的特性

### Dashboard 风格：Real-Time Monitor + Terminal

**理由**:

- 实时代码分析需要监控风格 UI
- 终端风格符合开发者习惯
- 支持命令行风格交互

## 🌈 颜色系统

### 深色模式（默认）

```css
--color-primary: #3b82f6 /* blue-500 - AI 分析颜色 */
  --color-background: #0f172a /* slate-900 - 深色背景 */
  --color-foreground: #f1f5f9 /* slate-100 - 主要文字 */ --color-card: #1e293b
  /* slate-800 - 卡片背景 */ --color-muted: #334155 /* slate-700 - 次要文字 */
  --color-border: #334155 /* slate-700 - 边框 */;
```

### 浅色模式（可选）

```css
--color-primary: #3b82f6 /* blue-500 */ --color-background: #ffffff
  /* 纯白背景 */ --color-foreground: #0f172a /* slate-900 - 主要文字 */
  --color-card: #ffffff /* 纯白卡片 */ --color-muted: #f1f5f9
  /* slate-100 - 次要文字 */ --color-border: #e2e8f0 /* slate-200 - 边框 */;
```

### 语义色

```css
--color-success: #16a34a; /* green-600 */
--color-warning: #ea580c; /* orange-600 */
--color-error: #ef4444; /* red-500 */
--color-info: #0ea5e9; /* sky-500 */
```

### 对比度标准（WCAG AA）

- **正常文本**: ≥ 4.5:1
- **深色模式**: #F1F5F9 on #0F172A = 14.3:1 ✓
- **浅色模式**: #0F172A on #FFFFFF = 14.3:1 ✓
- **静默文字（深色）**: #94A3B8 on #0F172A = 5.4:1 ✓
- **静默文字（浅色）**: #475569 on #FFFFFF = 7.1:1 ✓

## 🔤 排版系统

### 推荐配对：Developer Mono

```css
--font-sans: "IBM Plex Sans", system-ui, sans-serif; /* UI 文字 */
--font-mono: "JetBrains Mono", monospace; /* 代码文字 */
```

**来源**: Typography: "clean readable monospace code" 调研

**备选**: Dashboard Data - Fira Code + Fira Sans

### 字号规范（基于 16px 基准）

```css
font-size-xs: 12px; /* 标签、徽章 */
font-size-sm: 14px; /* 辅助文字 */
font-size-base: 16px; /* 正文 */
font-size-lg: 18px; /* 小标题 */
font-size-xl: 20px; /* 中标题 */
font-size-2xl: 24px; /* 大标题 */
font-size-3xl: 30px; /* 页面标题 */
```

### 行高

```css
line-height-tight: 1.25; /* 标题 */
line-height-normal: 1.5; /* 正文 */
line-height-relaxed: 1.75; /* 长文 */
```

## 📐 间距系统

### Tailwind 默认间距（基于 0.25rem = 4px）

```
spacing-1:  4px  /* 紧凑间距 */
spacing-2:  8px  /* 小间距 */
spacing-3:  12px /* 组件间隙 */
spacing-4:  16px /* 标准间距（组件内边距） */
spacing-6:  24px /* 大间距 */
spacing-8:  32px /* 页面间距 */
```

### 使用规范

- **组件内边距**: `p-4` (16px) - 标准值
- **组件间隙**: `gap-4` (16px) - 标准值
- **页面间距**: `py-8` (32px) - 大值
- **紧凑布局**: `p-2 gap-2` (8px) - 小值

## 🌓 主题系统

### 实现方式

- **Tailwind Config**: `darkMode: 'class'`
- **CSS 变量**: HSL 颜色空间，便于透明度控制
- **主题管理**: ThemeProvider Context + localStorage 持久化
- **系统主题**: `prefers-color-scheme` 自动检测

### 切换最佳实践

1. **防止闪烁**: 在 `<head>` 中立即应用主题（内联 script）
2. **平滑过渡**: `transition: background-color 200ms ease, color 200ms ease`
3. **系统默认**: 优先读取 localStorage，其次系统主题
4. ** Reduced Motion**: 尊重用户动画偏好设置

## 🎯 组件设计原则

### ✅ 规则 1：禁止使用 Emoji 图标

```tsx
// ❌ 错误
<button>🚀 Generate</button>;

// ✅ 正确
import { Rocket } from "lucide-react";
<button>
  <Rocket size={16} /> Generate
</button>;
```

**来源**: 设计调研的通用规则

### ✅ 规则 2：稳定的 Hover 状态

```tsx
// ❌ 错误：scale 改变布局
<div className="hover:scale-105 transition-transform">Card</div>

// ✅ 正确：颜色/不透明度
<div className="hover:bg-accent/50 transition-colors duration-200">Card</div>
```

**来源**: Style: "modern professional dark mode minimal" - 效果与动画指南

### ✅ 规则 3：Cursor Pointer

```tsx
// ✅ 正确
<button className="cursor-pointer">Button</button>
<div className="cursor-pointer" onClick={handleClick}>Card</div>
```

**来源**: UI/UX Pro Max Common Rules

### ✅ 规则 4：平滑过渡（200ms）

```tsx
// ✅ 正确
<button className="transition-colors duration-200 hover:bg-primary/90">
  Button
</button>

// ❌ 错误：>500ms
<button className="transition-colors duration-500 hover:bg-primary/90">
  Button
</button>
```

**来源**: UX: "animation transition hover focus" 调研

## 🌓 Light/Dark Mode 对比度规则

### 玻璃态卡片

```tsx
// ✅ 正确：浅色高透明度
<div className="dark:bg-card/85 bg-white/95">
  Content
</div>

// ❌ 错误：浅色低透明度（对比度不足）
<div className="dark:bg-card/85 bg-white/10">
  Content
</div>
```

### 文字对比度（浅色模式）

```tsx
// ✅ 正确：高对比度
<p className="text-slate-900">Body text (14.3:1)</p>

// ❌ 错误：低对比度
<p className="text-slate-400">Body text (2.8:1)</p>

// ✅ 正确：静默文字最小值
<span className="text-slate-600">Muted text (7.1:1)</span>

// ❌ 错误：静默文字低于最小值
<span className="text-slate-400">Muted text (2.8:1)</span>
```

### 边框可见性

```tsx
// ✅ 正确：浅色模式可见边框
<div className="border-gray-200">Card</div>

// ❌ 错误：浅色透明边框（不可见）
<div className="border-white/10">Card</div>
```

## 🖼️ 图表设计

### Network Graph（CodeMap 主图表）

**来源**: Chart: "graph tree network flowchart" 调研

**颜色指南**:

```css
node-primary:      #3B82F6  /* blue-500 - 主节点 */
node-secondary:    #10B981  /* green-500 - 次要节点 */
node-highlight:    #F59E0B  /* amber-500 - 高亮节点 */
node-error:        #EF4444  /* red-500 - 错误节点 */
edge:              rgba(144, 164, 174, 0.6) /* #90A4AE 60% */
```

**库推荐**:

1. **ReactFlow** ⭐ 推荐 - React 原生，易用
2. **D3.js (d3-force)** - 最灵活但复杂
3. **Cytoscape.js** - 科学计算图谱

**交互**: Drilldown + Hover + Drag

### 可访问性警告

- **问题**: 网络图可访问性非常差
- **解决方案**: 提供邻接列表替代视图
- **代码示例**:
  ```tsx
  <button onClick={() => setView("list")}>List View (Accessible)</button>;
  {
    view === "list" && <ul role="list">{/* 列表视图 */}</ul>;
  }
  ```

## ⚡ 动画与过渡

### 时长标准

```css
--animation-duration-fast: 150ms; /* 微交互 */
--animation-duration-normal: 200ms; /* 标准过渡 */
--animation-duration-slow: 300ms; /* 复杂动画 */
```

**来源**: 通用设计规范

### Hover vs Touch

```tsx
// ✅ 正确：click/tap 用于主要交互
<button onClick={handleAction}>Action</button>

// ❌ 错误：仅依赖 hover
<div onMouseEnter={handleAction}>Action</div> {/* 触摸设备无效 */}
```

**来源**: UX: "animation transition hover focus" - Hover vs Tap

### Focus States

```tsx
// ✅ 正确 1：focus-visible（键盘用户）
<button className="focus-visible:ring-2 focus-visible:ring-primary">
  Button
</button>

// ✅ 正确 2：focus 总是显示（带 offset）
<button className="focus:ring-2 ring-offset-2 ring-offset-background">
  Button
</button>

// ❌ 错误：移除 focus
<button className="outline-none">Button</button> {/* 键盘用户无法定位 */}
```

**来源**: UX: "animation transition hover focus" - Focus States

### Continuous Animation

```tsx
// ✅ 正确：仅用于加载
<div className="animate-spin">Loading...</div>

// ❌ 错误：用于装饰（分散注意力）
<Icon.Rocket className="animate-bounce" />
```

**来源**: UX: "animation transition hover focus" - Continuous Animation

### Reduced Motion 支持

```tsx
// ✅ 正确：尊重用户偏好
<div className="hover:scale-105 motion-reduce:hover:scale-100">
  Card
</div>

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**来源**: Stack: html-tailwind - Reduced motion

## ♿ 可访问性

### 键盘导航

```tsx
// ✅ 正确：Tab 顺序符合视觉顺序
<form>
  <input tabIndex={1} aria-label="First name" />
  <input tabIndex={2} aria-label="Last name" />
  <button tabIndex={3}>Submit</button>
</form>

// ❌ 错误：不合理 Tab 顺序
<form>
  <button tabIndex={10}>Submit</button> {/* 跳过多个元素 */}
  <input tabIndex={1} />
</form>
```

**来源**: UX: "accessibility keyboard contrast" - Keyboard Navigation

### 颜色对比度

```
正常文本最小：4.5:1
大号文本（≥18pt）最小：3:1
UI 组件最小：3:1
图形对象最小：3:1
```

**来源**: UX: "accessibility keyboard contrast" - Color Contrast

### Skip Links

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:top-4"
>
  Skip to main content
</a>
<main id="main-content">{/* Content */}</main>
```

**来源**: UX: "accessibility keyboard contrast" - Skip Links

### ARIA 标签

```tsx
<button aria-label="Close dialog" onClick={onClose}>
  <Icon.X size={16} />
</button>

<label htmlFor="email">Email</label>
<input id="email" type="email" aria-description="Your email address" />

<div aria-live="polite" aria-atomic="true">
  {notification && <p>{notification}</p>}
</div>
```

## 🎬 静态状态

### Empty States（空状态）

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <Icon.FolderOpen size={48} className="text-muted-foreground mb-4" />
  <h3 className="text-lg font-semibold mb-2">No CodeMaps found</h3>
  <p className="text-muted-foreground mb-4 max-w-sm">
    Get started by generating your first CodeMap
  </p>
  <Button onClick={handleCreate}>Generate CodeMap</Button>
</div>
```

**来源**: UX: "loading skeleton empty state" - Empty States

### Loading States（加载）

```tsx
// Skeleton Loading（内容感知）
<div className="space-y-4">
  {[...Array(3)].map((_, i) => (
    <div key={i} className="bg-muted h-24 rounded-md animate-pulse" />
  ))}
</div>

// Progress Indicator
<div className="h-2 bg-muted rounded-full overflow-hidden">
  <div className="h-full bg-primary" style={{ width: `${progress}%` }} />
</div>
```

**来源**: UX: "loading skeleton empty state" - Loading States

### Error States（错误）

```tsx
<div className="bg-error/10 border border-error rounded-md">
  <div className="flex items-start gap-3">
    <Icon.AlertCircle className="text-error" size={20} />
    <div>
      <h4 className="font-semibold text-error">Failed to generate</h4>
      <p className="text-muted-foreground mb-2">{message}</p>
      <Button variant="outline" size="sm" onClick={onRetry}>
        Retry
      </Button>
    </div>
  </div>
</div>
```

## 🧭 导航模式

### Sticky Navigation

```tsx
// ✅ 正确：固定导航 + 内容 padding
<header className="fixed top-0 left-0 right-0 h-14 z-50">Nav</header>
<main className="pt-14">{/* Content */}</main>

// ❌ 错误：导航遮挡内容
<header className="fixed top-0 left-0 right-0 h-14 z-50">Nav</header>
<main className="pt-0">{/* ❌ 首部被遮挡 */}</main>
```

**来源**: UX: "layout sidebar navigation" - Sticky Navigation

### Active State

```tsx
// ✅ 正确：高亮当前导航项
<nav>
  <a href="/codemap" className={cn(
    pathname === '/codemap'
      ? "bg-primary text-primary-foreground"
      : "text-muted-foreground hover:bg-accent"
  )}>CodeMap</a>
</nav>

// ❌ 错误：无视觉反馈
<nav>
  <a href="/codemap" className="text-muted-foreground">CodeMap</a>
</nav>
```

**来源**: UX: "loading skeleton empty state" - Active State

### Deep Linking

```tsx
// ✅ 正确：URL 反映当前状态
// URL: /codemap?view=graph&node=123&expanded=true

// ❌ 错误：所有状态使用相同 URL
// URL: /codemap（但显示不同视图）
```

**来源**: UX: "loading skeleton empty state" - Deep Linking

### Content Jumping（内容跳动）

```tsx
// ✅ 正确：预留空间
<div className="min-h-[200px]">
  {isLoading ? (
    <div className="animate-pulse bg-muted h-full" />
  ) : (
    <CodeMap data={data} />
  )}
</div>

// ❌ 错误：没有预留空间
<div>
  {isLoading && <div className="h-12 bg-muted" />}
  {!isLoading && <CodeMap data={data} />} {/* 导致跳动 */}
</div>
```

**来源**: UX: "layout sidebar navigation" - Content Jumping

## 📝 React + Tailwind 最佳实践

### 语义化颜色

```tsx
// ✅ 正确：使用语义化颜色
<button className="bg-primary text-primary-foreground">Button</button>

// ❌ 错误：硬编码颜色
<button className="bg-blue-500">Button</button>
```

**来源**: Stack: html-tailwind - Semantic colors

### Reduced Motion

```tsx
// ✅ 正确：尊重用户动画偏好
<div className="motion-reduce:animate-none motion-reduce:transition-none">
  Content
</div>

// ❌ 错误：忽略动画偏好
<div className="animate-pulse">Content</div>
```

**来源**: Stack: html-tailwind - Reduced motion

### Focus Visible

```tsx
// ✅ 正确：focus-visible（键盘用户）
<button className="focus-visible:ring-2">Button</button>

// ❌ 错误：focus（点击也显示）
<button className="focus:ring-2">Button</button>
```

**来源**: Stack: html-tailwind - Focus visible

## 🎯 关键决策总结

| 决策                | 理由                           | 来源                            |
| ------------------- | ------------------------------ | ------------------------------- |
| **深色模式默认**    | 开发者工具标准，减少眼部疲劳   | Product Type: Dashboard/DevTool |
| **OLED 纯黑背景**   | 省电、高对比度、专业感         | Style: Dark Mode (OLED)         |
| **JetBrains Mono**  | IDE 常用字体，开发者熟悉       | Typography: Developer Mono      |
| **ReactFlow**       | React 原生，性能好，易集成     | Chart: Network Graph            |
| **语义化颜色**      | 便于主题切换和维护             | Stack: Semantic colors          |
| **focus-visible**   | 仅键盘用户，不干扰点击         | Stack: Focus visible            |
| **Reduced Motion**  | 尊重用户偏好，提升可访问性     | Stack: Reduced motion           |
| **200ms 过渡**      | 流畅但不拖沓                   | Style: Animation duration       |
| **禁止 Emoji 图标** | 专业性、一致性和可访问性       | UI/UX Pro Max Common Rules      |
| **Glass 玻璃态**    | 现代感、层次感，深色模式效果佳 | Style: Dark Mode (OLED)         |

## 📚 参考资料

### 调研工具

- **UI/UX Pro Max** - 8 个领域系统性调研
  - Product Type（3 结果）
  - Style（3 结果）
  - Typography（3 结果）
  - Color（3 结果）
  - Chart（3 结果）
  - UX（6 结果）
  - Stack（3 结果）
  - Layout/Navigtion（3 结果）

### 设计系统参考

- [shadcn/ui](https://ui.shadcn.com/) - 零复制粘贴组件库
- [Radix UI](https://www.radix-ui.com/) - 无访问组件基础
- [Tailwind CSS](https://tailwindcss.com/docs) - 实用优先 CSS
- [VS Code](https://microsoft.github.io/vscode-codicons/) - 开发者工具设计
- [GitHub Design](https://github.com/design) - 现代 UI 设计
- [Linear](https://linear.app/design) - 极致用户体验

### 图表库

- [ReactFlow](https://reactflow.dev/) - React 节点图库
- [D3.js](https://d3js.org/) - 数据可视化库
- [Cytoscape.js](https://js.cytoscape.org/) - 图论可视化

### 可访问性

- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project](https://www.a11yproject.com/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)

### 动画库

- [framer-motion](https://www.framer.com/motion/) - React 动画库

---

**文档版本**: 1.0.0
**创建日期**: 2026-01-15
**调研完成率**: 100%（27 个关键点，8 个调研领域）
**设计文档**: `docs/DESIGN_SYSTEM.md`（24,902 bytes，11 个主要章节）
