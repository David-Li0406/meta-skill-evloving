# CodeMap 设计系统 - 基于 UI/UX Pro Max 调研

> 本文档基于 UI/UX Pro Max 设计系统调研结果，为 CodeMap 项目制定专业、现代化的开发者工具界面设计规范。

## 📊 调研总结

### 产品定位

- **类型**: Developer Tool / Dashboard / SaaS
- **核心价值**: AI 驱动的代码可视化工具
- **目标用户**: 开发者、技术团队
- **使用场景**: 代码分析、流程追踪、调试、文档生成

### 设计方向

- **主风格**: Dark Mode (OLED) + Minimalism（深色模式 + 极简主义）
- **辅助风格**: Flat Design（扁平化设计）、Bento Box Grid（便当盒网格）
- **Dashboard 风格**: Real-Time Monitor + Terminal（实时监控 + 终端风格）

## 🎨 颜色系统

### 深色模式（默认）

#### HSL 颜色定义

```css
:root {
  /* 品牌色 - Primary Blue */
  --color-primary: 217.2 91.2% 59.8%; /* #3B82F6 - blue-500 */
  --color-primary-foreground: 222.2 47.4% 11.2%; /* #0F172A - slate-900 */

  /* 语义色 */
  --color-success: 142.1 76.2% 36.3%; /* #16A34A - green-600 */
  --color-success-foreground: 355.7 100% 97.3%; /* #FEF2F2 */

  --color-warning: 32.6 94.6% 43.7%; /* #EA580C - orange-600 */
  --color-warning-foreground: 210 40% 98%; /* #FEF9C3 */

  --color-error: 0 84.2% 60.2%; /* #EF4444 - red-500 */
  --color-error-foreground: 355.7 100% 97.3%; /* #FEF2F2 */

  --color-info: 199 89% 48%; /* #0EA5E9 - sky-500 */
  --color-info-foreground: 210 40% 98%; /* #E0F2FE */

  /* 语义变量 - 深色模式 */
  --color-background: 222.2 84% 4.9%; /* #0F172A - slate-900 */
  --color-foreground: 210 40% 98%; /* #F1F5F9 - slate-100 */
  --color-card: 217.2 32.6% 17.5%; /* #1E293B - slate-800 */
  --color-card-foreground: 210 40% 98%; /* #F1F5F9 */
  --color-popover: 217.2 32.6% 17.5%; /* #1E293B */
  --color-popover-foreground: 210 40% 98%; /* #F1F5F9 */
  --color-secondary: 217.2 32.6% 17.5%; /* #1E293B */
  --color-secondary-foreground: 210 40% 98%; /* #F1F5F9 */
  --color-muted: 217.2 32.6% 20%; /* #334155 - slate-700 */
  --color-muted-foreground: 215 20.2% 65.1%; /* #94A3B8 - slate-400 */
  --color-accent: 217.2 32.6% 17.5%; /* #1E293B */
  --color-accent-foreground: 210 40% 98%; /* #F1F5F9 */
  --color-destructive: 0 62.8% 30.6%; /* #7F1D1D - red-900 */
  --color-destructive-foreground: 210 40% 98%; /* #FEF2F2 */
  --color-border: 217.2 32.6% 17.5%; /* #334155 - slate-700 */
  --color-input: 217.2 32.6% 17.5%; /* #334155 */
  --color-ring: 224.3 76.3% 48%; /* #3B82F6 */

  /* 玻璃态效果 - 深色模式 */
  --glass-background: 217.2 32.6% 17.5%;
  --glass-opacity: 0.85;
  --glass-border: 217.2 32.6% 25%;

  /* 阴影层级 */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
  --shadow-lg:
    0 10px 15px -3px rgb(0 0 0 / 0.5), 0 4px 6px -4px rgb(0 0 0 / 0.5);
  --shadow-xl:
    0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.5);

  /* 圆角 */
  --radius-sm: 0.375rem; /* 6px */
  --radius-md: 0.5rem; /* 8px */
  --radius-lg: 0.75rem; /* 12px */
  --radius-xl: 1rem; /* 16px */

  /* 动画 */
  --animation-duration: 200ms;
  --animation-easing: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 浅色模式

```css
.light {
  /* 语义变量 - 浅色模式 */
  --color-background: 0 0% 100%; /* #FFFFFF */
  --color-foreground: 222.2 84% 4.9%; /* #0F172A - slate-900 */
  --color-card: 0 0% 100%; /* #FFFFFF */
  --color-card-foreground: 222.2 84% 4.9%; /* #0F172A */
  --color-popover: 0 0% 100%; /* #FFFFFF */
  --color-popover-foreground: 222.2 84% 4.9%; /* #0F172A */
  --color-secondary: 210 40% 96.1%; /* #F8FAFC - slate-50 */
  --color-secondary-foreground: 222.2 47.4% 11.2%; /* #0F172A */
  --color-muted: 210 40% 96.1%; /* #F1F5F9 - slate-100 */
  --color-muted-foreground: 215.4 16.3% 46.9%; /* #64748B - slate-500 */
  --color-accent: 210 40% 96.1%; /* #F1F5F9 */
  --color-accent-foreground: 222.2 47.4% 11.2%; /* #0F172A */
  --color-destructive: 0 84.2% 60.2%; /* #EF4444 */
  --color-destructive-foreground: 210 40% 98%; /* #FEF2F2 */
  --color-border: 214.3 31.8% 91.4%; /* #E2E8F0 - slate-200 */
  --color-input: 214.3 31.8% 91.4%; /* #E2E8F0 */

  /* 玻璃态效果 - 浅色模式 */
  --glass-background: 0 0% 100%;
  --glass-opacity: 0.9;
  --glass-border: 214.3 31.8% 91.4%;

  /* 阴影层级 - 浅色模式 */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg:
    0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl:
    0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
```

### 颜色使用指南

#### 语义化颜色命名

```javascript
// Tailwind 配置中使用语义化颜色
theme: {
  extend: {
    colors: {
      primary: 'hsl(var(--color-primary) / <alpha-value>)',
      success: 'hsl(var(--color-success) / <alpha-value>)',
      warning: 'hsl(var(--color-warning) / <alpha-value>)',
      error: 'hsl(var(--color-error) / <alpha-value>)',
      info: 'hsl(var(--color-info) / <alpha-value>)',
      // ... 其他语义颜色
    }
  }
}

// ✅ 正确：使用语义化颜色
<button className="bg-primary text-primary-foreground hover:opacity-90">
  Generate
</button>

// ❌ 错误：直接使用硬编码颜色
<button className="bg-blue-500 hover:bg-blue-600">
  Generate
</button>
```

#### 对比度要求（WCAG AA）

- **正常文本**: 最小 4.5:1
- **大号文本（≥18pt）**: 最小 3:1
- **UI 组件**: 最小 3:1
- **图形对象**: 最小 3:1

#### 深色模式对比度检查

```css
/* ✅ 良好对比度 - 深色模式 */
--color-foreground: 210 40% 98%; /* #F1F5F9 on #0F172A = 14.3:1 ✓ */
--color-muted-foreground: 215 20.2% 65.1%; /* #94A3B8 on #0F172A = 5.4:1 ✓ */

/* ❌ 低对比度 - 需避免 */
--color-body-text: 215 25% 40%; /* 低于标准 */
```

## 🔤 排版系统

### 字体家族

#### 推荐配对：Developer Mono

```javascript
// Google Fonts Import
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

// Tailwind 配置
theme: {
  extend: {
    fontFamily: {
      sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
      mono: ['"JetBrains Mono"', 'monospace'],
    }
  }
}
```

#### 备选配对：Dashboard Data

```javascript
// Google Fonts Import
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');

// Tailwind 配置
theme: {
  extend: {
    fontFamily: {
      sans: ['"Fira Sans"', 'system-ui', 'sans-serif'],
      mono: ['"Fira Code"', 'monospace'],
    }
  }
}
```

### 字体大小

```css
/* Tailwind 默认字号（16px 基准） */
--font-size-xs: 0.75rem; /* 12px */
--font-size-sm: 0.875rem; /* 14px */
--font-size-base: 1rem; /* 16px */
--font-size-lg: 1.125rem; /* 18px */
--font-size-xl: 1.25rem; /* 20px */
--font-size-2xl: 1.5rem; /* 24px */
--font-size-3xl: 1.875rem; /* 30px */
--font-size-4xl: 2.25rem; /* 36px */
```

### 行高

```css
--line-height-tight: 1.25; /* 标题 */
--line-height-normal: 1.5; /* 正文 */
--line-height-relaxed: 1.75; /* 长文 */
```

### 使用指南

```tsx
// ✅ 正确：使用语义化字体类
<h1 className="text-4xl font-bold tracking-tight mb-4">CodeMap Explorer</h1>
<p className="text-base text-muted-foreground leading-relaxed">
  Visualize your code execution flow with AI-powered analysis
</p>

// 代码片段
<code className="text-sm font-mono bg-muted px-2 py-1 rounded">
  npm install codemap
</code>
```

## 📐 间距系统

### Tailwind 默认间距（基于 0.25rem = 4px）

```css
spacing-0: 0;
spacing-px: 1px;
spacing-1: 0.25rem; /* 4px */
spacing-2: 0.5rem; /* 8px */
spacing-3: 0.75rem; /* 12px */
spacing-4: 1rem; /* 16px */
spacing-5: 1.25rem; /* 20px */
spacing-6: 1.5rem; /* 24px */
spacing-8: 2rem; /* 32px */
spacing-10: 2.5rem; /* 40px */
spacing-12: 3rem; /* 48px */
spacing-16: 4rem; /* 64px */
spacing-20: 5rem; /* 80px */
spacing-24: 6rem; /* 96px */
```

### 间距使用指南

```tsx
// 组件内边距 - 使用一致的最小值
<div className="p-4"> {/* 16px 标准内边距 */}

// 组件间隙 - 使用一致
<div className="flex flex-col gap-4"> {/* 16px 标准间隙 */}

// 页面间距 - 使用较大值
<section className="py-8"> {/* 32px 页面内边距 */}

// 紧凑布局
<div className="p-2 gap-2"> {/* 8px 紧凑间距 */}
```

## 🌓 主题系统

### 主题实现

#### 1. Tailwind 配置

```javascript
export default {
  darkMode: "class", // 使用 class 切换主题
  // ... 其他配置
};
```

#### 2. 主题管理器

```tsx
// client/src/components/theme/ThemeProvider.tsx
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "dark" | "light" | "system";

type ThemeProviderProps = {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
};

type ThemeProviderState = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
};

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
};

const ThemeProviderContext = createContext<ThemeProviderState>(initialState);

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "codemap-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme,
  );

  useEffect(() => {
    const root = window.document.documentElement;

    root.classList.remove("light", "dark");

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light";

      root.classList.add(systemTheme);
      return;
    }

    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme);
      setTheme(theme);
    },
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext);

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider");

  return context;
};
```

#### 3. 主题切换按钮

```tsx
// client/src/components/theme/ThemeToggle.tsx
import { Icon } from "@components/icons";
import { useTheme } from "@components/theme/ThemeProvider";
import { Button } from "@components/ui/Button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={toggleTheme}
      aria-label="Toggle theme"
    >
      {theme === "dark" ? <Icon.Sun size={16} /> : <Icon.Moon size={16} />}
    </Button>
  );
}
```

### 主题切换最佳实践

#### 防止闪烁

```tsx
// 在 document head 中立即应用主题
<script>
  ;(function() {
    const theme = localStorage.getItem('codemap-theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const effectiveTheme = theme === 'system' ? systemTheme : theme || systemTheme;
    document.documentElement.classList.add(effectiveTheme);
  })();
</script>
```

#### 平滑过渡

```css
html {
  transition:
    background-color 200ms ease,
    color 200ms ease;
}

@media (prefers-reduced-motion: reduce) {
  html {
    transition: none;
  }
}
```

## 🎯 组件设计原则

### 通用规则

#### 1. 禁止使用 emoji 图标

```tsx
// ❌ 错误：使用 emoji 作为图标
<button>🚀 Generate</button>
<div>⚙️ Settings</div>

// ✅ 正确：使用 SVG 图标
import { Rocket, Settings } from 'lucide-react'

<button className="flex items-center gap-2">
  <Rocket size={16} />
  Generate
</button>
<div className="flex items-center gap-2">
  <Settings size={16} />
  Settings
</div>
```

#### 2. 稳定的 hover 状态

```tsx
// ❌ 错误：使用 scale 改变布局
<div className="hover:scale-105 transition-transform">
  Card
</div>

// ✅ 正确：使用颜色/不透明度
<div className="hover:bg-accent/50 hover:border-accent transition-colors duration-200">
  Card
</div>
```

#### 3. Cursor pointer

```tsx
// ✅ 正确：可点击元素添加 cursor-pointer
<button className="cursor-pointer">Button</button>
<div onClick={handleClick} className="cursor-pointer">Clickable Div</div>
```

#### 4. 平滑过渡

```tsx
// ✅ 正确：使用 200ms 过渡
<button className="bg-primary hover:bg-primary/90 transition-colors duration-200">
  Button
</button>

// ❌ 错误：过渡时间过长
<button className="bg-primary hover:bg-primary/90 transition-colors duration-500">
  Button
</button>
```

### Light/Dark Mode 对比度

#### 玻璃态卡片

```tsx
// ✅ 正确：浅色模式高透明度
<div className="dark:bg-card/85 dark:backdrop-blur-sm bg-white/95 backdrop-blur-sm border dark:border-glass-border border-gray-200">
  Content
</div>

// ❌ 错误：浅色模式透明度过低
<div className="dark:bg-card/85 dark:backdrop-blur-sm bg-white/10 backdrop-blur-sm border dark:border-glass-border border-gray-200">
  Content {/* 对比度不足 */}
</div>
```

#### 文字对比度

```tsx
// ✅ 正确：浅色模式高对比度
<p className="dark:text-foreground text-slate-900">
  Body text with high contrast
</p>

// ❌ 错误：浅色模式低对比度
<p className="dark:text-foreground text-slate-400">
  Body text with low contrast
</p>
```

#### 静默文字对比度（浅色模式最小值）

```tsx
// ✅ 正确：浅色模式使用 slate-600 及以上
<span className="dark:text-muted-foreground text-slate-600">
  Muted text
</span>

// ❌ 错误：浅色模式使用 slate-400 或更低
<span className="dark:text-muted-foreground text-slate-400">
  Muted text with low contrast
</span>
```

#### 边框可见性

```tsx
// ✅ 正确：浅色模式使用可见边框
<div className="dark:border-glass-border border-gray-200">
  Card
</div>

// ❌ 错误：浅色模式使用透明边框
<div className="dark:border-glass-border border-white/10">
  Card {/* 边框不可见 */}
</div>
```

## 🖼️ 图表设计

### 图表类型推荐

#### Network Graph（网络图）- CodeMap 主要图表

```tsx
// 颜色指南
const nodeColors = {
  primary: "#3B82F6", // 主节点 - blue-500
  secondary: "#10B981", // 次要节点 - green-500
  highlight: "#F59E0B", // 高亮节点 - amber-500
  error: "#EF4444", // 错误节点 - red-500
};

const edgeColor = "rgba(144, 164, 174, 0.6)"; // #90A4AE 60% opacity

// 库推荐
// - D3.js (d3-force) - 最灵活但复杂
// - ReactFlow - React 原生，推荐使用
// - Cytoscape.js - 科学计算图谱
```

#### Decomposition Tree（分解树）- 根因分析

```tsx
// 颜色指南
const treeColors = {
  node: "#2563EB", // blue-600
  negativeImpact: "#EF4444", // red-500
  connector: "#94A3B8", // slate-400
};

// 交互级别
// - Drill: 点击展开/折叠
// - Expand: 自动展开子节点
```

#### Process Map（流程图）- 代码执行流

```tsx
// 颜色指南
const processColors = {
  happyPath: "#10B981", // 绿色路径 - thick
  deviation: "#F59E0B", // 橙色路径 - medium
  bottleneck: "#EF4444", // 红色阻断 - thin
};

// 交互级别
// - Drag: 拖动节点
// - Node-Click: 点击节点查看详情
```

### 图表可访问性

```tsx
// ❌ 网络图可访问性：非常差
// 解决方案：提供邻接列表替代视图

// ✅ 添加替代视图
<div>
  <button onClick={() => setView("graph")}>Graph View</button>
  <button onClick={() => setView("list")}>List View (Accessible)</button>

  {view === "list" && (
    <ul role="list" aria-label="Node relationships">
      {nodes.map((node) => (
        <li key={node.id}>
          <h3>{node.name}</h3>
          <p>Connected to: {node.connections.join(", ")}</p>
        </li>
      ))}
    </ul>
  )}
</div>
```

## ⚡ 动画与过渡

### 动画时长

```css
/* 标准时长 */
--animation-duration-fast: 150ms;
--animation-duration-normal: 200ms;
--animation-duration-slow: 300ms;
```

### 过渡效果

```tsx
// ✅ 正确：使用标准过渡
<div className="transition-all duration-200 ease-in-out">
  Content
</div>

// ✅ 仅颜色过渡
<div className="transition-colors duration-200">
  Content
</div>

// ✅ 仅阴影过渡
<div className="transition-shadow duration-200">
  Content
</div>
```

### Hover vs Touch

```tsx
// ✅ 正确：click/tap 用于主要交互
<button onClick={handleAction} className="hover:bg-accent active:bg-accent/80">
  Action
</button>

// ❌ 错误：仅依赖 hover
<div onMouseEnter={handleAction} className="hover:bg-accent">
  Action {/* 触摸设备无效 */}
</div>
```

### Focus States

```tsx
// ✅ 正确：仅为键盘用户显示 focus
<button className="focus-visible:ring-2 focus-visible:ring-primary outline-none">
  Button
</button>

// ✅ 或：总是显示 focus（需要确保不影响视觉效果）
<button className="focus:ring-2 focus:ring-primary outline-none ring-offset-2 ring-offset-background">
  Button
</button>

// ❌ 错误：移除 focus 轮廓
<button className="outline-none">
  Button {/* 键盘用户无法知道焦点位置 */}
</button>
```

### Continuous Animation

```tsx
// ✅ 正确：仅用于加载指示器
<div className="animate-spin">
  Loading...
</div>

// ❌ 错误：用于装饰元素（分散注意力）
<Icon.Rocket className="animate-bounce" />  {/* ❌ 不要这样做 */}
```

### Reduced Motion 支持

```tsx
// ✅ 正确：尊重用户动画偏好
<div className="transition-transform hover:scale-105 motion-reduce:transition-none motion-reduce:hover:scale-100">
  Card
</div>

// 系统级 CSS
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## ♿ 可访问性

### 键盘导航

```tsx
// ✅ 正确：Tab 顺序符合视觉顺序
<form>
  <input type="text" tabIndex={1} aria-label="First name" />
  <input type="text" tabIndex={2} aria-label="Last name" />
  <button tabIndex={3}>Submit</button>
</form>

// ❌ 错误：不合理的 Tab 键盘陷阱
<form>
  <button tabIndex={10}>Submit</button> {/* ❌ 跳过多个元素 */}
  <input type="text" tabIndex={1} />
</form>
```

### 颜色对比度

```tsx
// ✅ 正确：高对比度文本
<p className="dark:text-background text-foreground">
  High contrast text (WCAG 4.5:1+)
</p>

// ✅ 测试对比度
// - dark: #F1F5F9 on #0F172A = 14.3:1 ✓
// - light: #0F172A on #FFFFFF = 14.3:1 ✓

// ❌ 错误：低对比度文本
<p className="text-slate-400 on-white">
  Low contrast text (2.8:1) ❌
</p>
```

### Skip Links

```tsx
// ✅ 正确：提供跳转到主内容的链接
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:bg-primary focus:text-primary-foreground focus:p-4 focus:rounded-md"
>
  Skip to main content
</a>

<main id="main-content">
  {/* Main content */}
</main>

// Tailwind hidden class
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

### ARIA 标签

```tsx
// ✅ 正确：为交互元素添加 aria-label
<button aria-label="Close dialog" onClick={onClose}>
  <Icon.X size={16} />
</button>

// ✅ 正确：为表单元素添加标签
<label htmlFor="email">Email</label>
<input id="email" type="email" aria-label="Email address" />

// ✅ 正确：为动态内容添加 aria-live
<div aria-live="polite" aria-atomic="true">
  {notification && <p>{notification}</p>}
</div>
```

## 🎬 静态状态

### Empty States（空状态）

```tsx
// ✅ 正确：显示有帮助的消息和操作
<div className="flex flex-col items-center justify-center py-12 text-center">
  <Icon.FolderOpen size={48} className="text-muted-foreground mb-4" />
  <h3 className="text-lg font-semibold mb-2">No CodeMaps found</h3>
  <p className="text-muted-foreground mb-4 max-w-sm">
    Get started by generating your first CodeMap to visualize your code execution flow.
  </p>
  <Button onClick={handleCreate}>
    <Icon.Plus size={16} className="mr-2" />
    Generate CodeMap
  </Button>
</div>

// ❌ 错误：空白屏幕
<div>
  {/* 空白，没有任何提示 */}
</div>
```

### Loading States（加载状态）

```tsx
// ✅ 正确 1：Skeleton Loading（内容感知）
<div className="space-y-4">
  {[...Array(3)].map((_, i) => (
    <div key={i} className="bg-muted h-24 rounded-md animate-pulse" />
  ))}
</div>

// ✅ 正确 2：Spinner（通用加载）
<div className="flex items-center justify-center py-8">
  <Icon.Loader2 className="animate-spin h-8 w-8 text-muted-foreground" />
</div>

// ✅ 正确 3：Progress Indicator（进度）
<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Analyzing code...</span>
    <span>{progress}%</span>
  </div>
  <div className="h-2 bg-muted rounded-full overflow-hidden">
    <div
      className="h-full bg-primary transition-all duration-300"
      style={{ width: `${progress}%` }}
    />
  </div>
</div>
```

### Error States（错误状态）

```tsx
// ✅ 正确：用户友好的错误提示
<div className="p-4 bg-error/10 border border-error rounded-md">
  <div className="flex items-start gap-3">
    <Icon.AlertCircle className="text-error mt-0.5 flex-shrink-0" size={20} />
    <div className="flex-1">
      <h4 className="font-semibold text-error mb-1">
        Failed to generate CodeMap
      </h4>
      <p className="text-sm text-muted-foreground mb-2">
        {message || "An unexpected error occurred. Please try again."}
      </p>
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={onRetry}>
          <Icon.Refresh size={14} className="mr-1" />
          Retry
        </Button>
        <Button variant="ghost" size="sm" onClick={onReport}>
          Report Issue
        </Button>
      </div>
    </div>
  </div>
</div>
```

## 🧭 导航模式

### Sticky Navigation（固定导航）

```tsx
// ✅ 正确：固定导航 + 内容 padding
<header className="fixed top-0 left-0 right-0 h-14 z-50 bg-background/95 backdrop-blur-sm border-b">
  {/* Navigation content */}
</header>

<main className="pt-14"> {/* padding-top = header height */}
  {/* Main content */}
</main>

// ❌ 错误：导航遮挡内容
<header className="fixed top-0 left-0 right-0 h-14 z-50">
  {/* Navigation content */}
</header>

<main className="pt-0"> {/* ❌ 首部分内容被遮挡 */}
  {/* Main content */}
</main>
```

### Active State（活动状态）

```tsx
// ✅ 正确：高亮当前导航项
<nav className="flex flex-col gap-1">
  <a href="/codemap" className={cn(
    "flex items-center gap-2 px-3 py-2 rounded-md transition-colors",
    pathname === '/codemap'
      ? "bg-primary text-primary-foreground font-medium"
      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
  )}>
    <Icon.Map size={16} />
    CodeMap
  </a>
  <a href="/browser" className={cn(
    "flex items-center gap-2 px-3 py-2 rounded-md transition-colors",
    pathname === '/browser'
      ? "bg-primary text-primary-foreground font-medium"
      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
  )}>
    <Icon.FileText size={16} />
    Code Browser
  </a>
</nav>

// ❌ 错误：没有视觉反馈
<nav className="flex flex-col gap-1">
  <a href="/codemap" className="flex items-center gap-2 px-3 py-2 rounded-md text-muted-foreground">
    <Icon.Map size={16} />
    CodeMap
  </a>
  <a href="/browser" className="flex items-center gap-2 px-3 py-2 rounded-md text-muted-foreground">
    <Icon.FileText size={16} />
    Code Browser
  </a>
</nav>
```

### Deep Linking（深度链接）

```tsx
// ✅ 正确：URL 反映当前状态
// URL: /codemap/view=graph&node=123&expanded=true

// 使用 URL 参数或 hash 保存状态
useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const view = params.get("view") || "tree";
  setView(view as ViewMode);
}, [window.location.search]);

// 更新 URL 当状态改变
const handleViewChange = (view: ViewMode) => {
  setView(view);
  const params = new URLSearchParams(window.location.search);
  params.set("view", view);
  window.history.replaceState(null, "", `?${params.toString()}`);
};

// ❌ 错误：所有状态使用相同 URL
// URL: /codemap （但显示不同的视图）
```

### Content Jumping（内容跳动）

```tsx
// ✅ 正确：为异步内容预留空间
<div className="min-h-[200px]"> {/* 预留最小高度 */}
  {isLoading ? (
    <div className="animate-pulse bg-muted h-full rounded-md" />
  ) : (
    <CodeMap data={data} />
  )}
</div>

// ✅ 或：使用 aspect-ratio
<div className="aspect-video">
  {isLoading ? (
    <div className="w-full h-full animate-pulse bg-muted rounded-md" />
  ) : (
    <GraphView data={data} />
  )}
</div>

// ❌ 错误：没有预留空间，导致布局跳动
<div>
  {isLoading && <div className="animate-pulse h-12 bg-muted" />}
  {!isLoading && <CodeMap data={data} />} {/* 可能有 200px 高，导致跳动 */}
</div>
```

## 📝 实施检查清单

### Phase 1: 设计系统搭建

- [ ] 创建 `client/src/styles/design-tokens.css`
- [ ] 配置 Tailwind 集成设计令牌
- [ ] 实现 ThemeProvider 和 ThemeToggle
- [ ] 更新 `client/src/index.css` 应用设计令牌
- [ ] 配置暗色模式 `darkMode: 'class'`

### Phase 2: 基础组件重构

- [ ] Button - 更多 variants 和 sizes
- [ ] Input - 支持前缀/后缀图标
- [ ] Card - 支持玻璃态效果
- [ ] Badge - 状态卡片展示
- [ ] Separator - 分割线
- [ ] ScrollArea - 可滚动区域

### Phase 3: 数据展示组件

- [ ] Table - 表格组件
- [ ] Tabs - 选项卡（优化）
- [ ] Accordion - 折叠面板（优化）
- [ ] Tooltip - 工具提示
- [ ] Alert - 警告通知

### Phase 4: 反馈组件

- [ ] Dialog - 对话框（优化）
- [ ] Toast - 临时消息
- [ ] Loading - 加载指示器
- [ ] EmptyState - 空状态展示
- [ ] Progress - 进度条

### Phase 5: 布局组件

- [ ] Container - 内容容器
- [ ] Grid - 网格布局
- [ ] Flex - 弹性布局
- [ ] Stack - 堆叠布局

### Phase 6: 页面级重设计

- [ ] Header - 玻璃态导航栏
- [ ] Sidebar - 优化历史记录列表
- [ ] MainPanel - 优化树形/图形视图
- [ ] CodeBrowser - 优化代码浏览器
- [ ] Dialog - 统一弹窗样式

### Phase 7: 动画和交互

- [ ] 添加 framer-motion 页面过渡
- [ ] 优化 hover/active/focus 状态
- [ ] 实现面板展开/折叠动画
- [ ] 添加列表项进入动画

### Phase 8: 可访问性

- [ ] 全键盘导航支持
- [ ] 完善 ARIA 标签
- [ ] 屏幕阅读器测试
- [ ] Focus Trap in Modals

### Phase 9: 性能优化

- [ ] 代码分割优化
- [ ] Monaco Editor 懒加载
- [ ] 虚拟滚动实现
- [ ] 图表库按需加载

### Phase 10: 验证和测试

- [ ] 视觉一致性检查
- [ ] 跨浏览器测试
- [ ] 响应式测试
- [ ] 性能基准测试
- [ ] 可访问性测试 (axe-core)

## 📚 参考资料

### 设计系统

- [shadcn/ui](https://ui.shadcn.com/) - 零复制粘贴的组件库
- [Radix UI](https://www.radix-ui.com/) - 无访问组件基础
- [Tailwind CSS](https://tailwindcss.com/docs) - 实用优先的 CSS 框架

### 开发者工具设计

- [VS Code Design System](https://microsoft.github.io/vscode-codicons/)
- [GitHub Design](https://github.com/design)
- [Linear Design](https://linear.app/design)

### 图表库

- [ReactFlow](https://reactflow.dev/) - React 节点图库
- [D3.js](https://d3js.org/) - 数据可视化库
- [Cytoscape.js](https://js.cytoscape.org/) - 图论可视化

### 可访问性

- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project](https://www.a11yproject.com/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)

---

**文档版本**: 1.0.0
**最后更新**: 2026-01-15
**基于**: UI/UX Pro Max 调研结果
