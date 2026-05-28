---
name: ui-design-core
description: 核心设计能力，提供配色、布局、组件样式生成及反模式检查。
---

# Core Design Skills

## 🌟 技能核心：拒绝平庸
本技能旨在生成**具有独特审美、生产级质量**的前端界面。
**核心原则**：拒绝千篇一律的 "AI 廉价感" (AI Slop)。我们追求**大胆**、**独特**且**细节丰富**的设计。

## 🧠 Design Thinking (设计思维)
在编写任何代码之前，必须先确立设计方向：

### 1. 确立审美基调 (Bold Direction)
不要做"干净但无聊"的设计。选择一个明确的风格方向：
- **Brutalism (野兽派)**: 粗边框、高对比度、单色底、巨大字体。
- **Glassmorphism (玻璃拟态)**: 深度模糊、半透明层、微妙的光影。
- **Neo-Brutalism**: 鲜艳高饱和色、复古黑边、几何图形。
- **Editorial (杂志风)**: 精致的衬线体、大留白、不对称布局。
- **Cyberpunk (赛博朋克)**: 霓虹光晕、深色背景、Glitch 效果。

### 2. 细节至上 (Refined Details)
- **Typography**: 拒绝 Arial/Roboto。混合搭配 Display 字体（标题）和高可读性 Sans 字体（正文）。
- **Motion**: 每一个交互都应有物理反馈。使用 `cubic-bezier` 而不是线性的 `ease`。
- **Depth**: 避免扁平化。使用阴影、纹理、噪点 (Noise) 来增加质感。

## 🚫 反模式 (Anti-Patterns)
**绝对禁止**以下 "AI 默认审美"：
- ❌ 泛滥的紫色/蓝色线性渐变背景。
- ❌ 毫无个性的 `box-shadow: 0 4px 6px rgba(0,0,0,0.1)`。
- ❌ 默认的圆角 (如 `border-radius: 4px`) —— 要么完全直角，要么夸张的大圆角。
- ❌ 枯燥的 "Header-Hero-Features" 三段式布局。

## 🎨 常用指令与 Prompt 策略

### 1. 布局生成 (Layout)
不要只说 "生成一个着陆页"，尝试更具体的风格描述：
```bash
# ❌ 错误示范
/ui-design 生成一个科技感着陆页

# ✅ 正确示范
/ui-design 生成一个 Neo-Brutalism 风格的着陆页。使用高饱和度的橙色和黑色，厚重的边框，巨大的无衬线标题，并且布局要打破常规网格。
```

### 2. 组件样式 (Component)
```bash
# 生成具有杂志质感的卡片
/ui-design 设计一个 Article Card。使用衬线字体 (Playfair Display)，大留白，图片带有视差滚动效果，鼠标悬停时卡片轻微上浮并投射长阴影。
```

### 3. 即时重构 (Refactor)
```bash
# 拯救平庸设计
/ui-design 重新设计这个 Hero Section。现在的太普通了。把它改成极简主义风格，使用巨大的文字排版作为主视觉，去掉所有多余的装饰，只保留黑白两色和极细的分割线。
```

## �️ 技术栈推荐
- **CSS Framework**: Tailwind CSS (推荐), CSS Modules.
- **Animation**: Framer Motion (React), GSAP, 或原生 CSS Transitions.
- **Icons**: Lucide React, Remix Icon (避免 FontAwesome).
