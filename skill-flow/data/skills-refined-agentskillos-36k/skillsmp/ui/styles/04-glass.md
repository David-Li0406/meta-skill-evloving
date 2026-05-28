---
name: 玻璃擬態
description: Glassmorphism - 毛玻璃透明效果
---

# 04. 玻璃擬態 Glassmorphism

## 概述

使用毛玻璃效果創造半透明、有層次感的介面。

### 核心特徵
- 毛玻璃效果 (backdrop-filter: blur)
- 半透明背景
- 微妙白色邊框
- 搭配漸層背景

---

## 配色

```css
:root {
  --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --glass-bg: rgba(255, 255, 255, 0.15);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}
```

---

## 核心效果

```css
.glass {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}
```

---

## 元件

### 卡片

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
}
```

### 按鈕

```css
.btn-glass {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 0.875rem 2rem;
  color: #fff;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.3);
}
```

### 導航

```css
.nav-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
```

### 輸入框

```css
.input-glass {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #fff;
}

.input-glass::placeholder {
  color: rgba(255, 255, 255, 0.5);
}
```

---

## 適用場景

- 科技/軟體
- 應用程式
- 金融科技
- 音樂/娛樂

---

## 瀏覽器支援

```css
@supports (backdrop-filter: blur(10px)) {
  .glass {
    backdrop-filter: blur(10px);
  }
}
```

- ✅ Chrome 76+
- ✅ Safari 9+
- ✅ Firefox 103+
