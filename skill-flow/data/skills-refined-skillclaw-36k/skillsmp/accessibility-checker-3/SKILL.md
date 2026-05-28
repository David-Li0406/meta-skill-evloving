---
name: accessibility-checker
description: 检查 UI 组件的可访问性（a11y）。用于审查和改进网页可访问性，确保符合 WCAG 标准。
allowed-tools: Read, Grep, Glob
---

# 可访问性检查器

## WCAG 2.1 核心原则

### 1. 可感知 (Perceivable)
内容必须以用户能感知的方式呈现

### 2. 可操作 (Operable)
用户界面组件和导航必须可操作

### 3. 可理解 (Understandable)
信息和用户界面操作必须可理解

### 4. 健壮 (Robust)
内容必须足够健壮，能被各种用户代理解释

## 检查清单

### 语义化 HTML
- [ ] 使用正确的 HTML5 语义标签（header, nav, main, article, aside, footer）
- [ ] 标题层级正确（h1-h6）
- [ ] 列表使用 ul/ol/li
- [ ] 表单使用 label 关联 input

```html
<!-- ✅ 正确 -->
<label htmlFor="email">邮箱</label>
<input id="email" type="email" />

<!-- ❌ 错误 -->
<div>邮箱</div>
<input type="email" />
```

### ARIA 属性
- [ ] 交互元素有 aria-label 或 aria-labelledby
- [ ] 动态内容使用 aria-live
- [ ] 展开/折叠使用 aria-expanded
- [ ] 模态框使用 role="dialog" 和 aria-modal

```jsx
<button
  aria-label="关闭对话框"
  aria-expanded={isOpen}
  onClick={handleClose}
>
  <CloseIcon />
</button>
```

### 键盘导航
- [ ] 所有交互元素可通过 Tab 键访问
- [ ] 焦点顺序符合逻辑
- [ ] 焦点可见（outline 或自定义样式）
- [ ] 支持 Enter/Space 触发操作
- [ ] 支持 Esc 关闭模态框

```css
/* 保持焦点可见 */
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

### 颜色和对比度
- [ ] 文本对比度至少 4.5:1（正常文本）
- [ ] 大文本对比度至少 3:1
- [ ] 不仅依赖颜色传达信息
- [ ] 链接有下划线或其他视觉区分

### 图片和媒体
- [ ] 图片有 alt 属性
- [ ] 装饰性图片 alt=""
- [ ] 视频有字幕
- [ ] 音频有文字稿

```jsx
{/* 内容图片 */}
<img src="chart.png" alt="2024年销售趋势图" />

{/* 装饰图片 */}
<img src="decoration.png" alt="" aria-hidden="true" />
```

### 表单可访问性
- [ ] 每个输入框有关联的 label
- [ ] 错误提示与输入框关联（aria-describedby）
- [ ] 必填字段标记（aria-required）
- [ ] 表单验证提供清晰反馈

```jsx
<div>
  <label htmlFor="username">用户名 *</label>
  <input
    id="username"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? "username-error" : undefined}
  />
  {hasError && (
    <span id="username-error" role="alert">
      用户名必须至少 3 个字符
    </span>
  )}
</div>
```

### 响应式和缩放
- [ ] 支持 200% 文本缩放
- [ ] 移动端触摸目标至少 44x44px
- [ ] 横向和纵向都可用

### 屏幕阅读器
- [ ] 跳过导航链接
- [ ] 页面标题描述性强
- [ ] 地标区域（landmarks）清晰
- [ ] 动态内容更新通知用户

```jsx
{/* 跳过导航 */}
<a href="#main-content" className="skip-link">
  跳到主内容
</a>

{/* 主内容区域 */}
<main id="main-content">
  {/* 内容 */}
</main>
```

## 测试工具

### 自动化工具
- axe DevTools（浏览器扩展）
- Lighthouse（Chrome DevTools）
- WAVE（Web Accessibility Evaluation Tool）
- eslint-plugin-jsx-a11y

### 手动测试
- 仅使用键盘导航
- 使用屏幕阅读器（NVDA, JAWS, VoiceOver）
- 测试颜色对比度
- 缩放到 200% 测试

## 常见问题修复

### 问题：按钮没有可访问名称
```jsx
// ❌ 错误
<button><Icon /></button>

// ✅ 正确
<button aria-label="删除">
  <Icon />
</button>
```

### 问题：div 作为按钮
```jsx
// ❌ 错误
<div onClick={handleClick}>点击</div>

// ✅ 正确
<button onClick={handleClick}>点击</button>
```

### 问题：模态框焦点管理
```jsx
// ✅ 正确
useEffect(() => {
  if (isOpen) {
    const previousFocus = document.activeElement;
    modalRef.current?.focus();

    return () => {
      previousFocus?.focus();
    };
  }
}, [isOpen]);
```

## 审查流程

1. 使用自动化工具扫描
2. 键盘导航测试
3. 屏幕阅读器测试
4. 颜色对比度检查
5. 缩放测试
6. 移动端测试
