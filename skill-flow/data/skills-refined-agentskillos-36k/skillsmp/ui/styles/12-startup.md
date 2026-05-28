---
name: 新創風格
description: Startup - 活力現代的科技新創風格
---

# 12. 新創風 Startup

## 概述
活力、現代、創新的科技新創設計風格。

## 特徵
- 漸層色彩
- 活力動效
- 清晰 CTA
- 產品導向

## 配色
```css
:root {
  --start-primary: #6366f1;
  --start-secondary: #8b5cf6;
  --start-accent: #06b6d4;
  --start-dark: #0f172a;
  --start-light: #f8fafc;
}
```

## 元件

### Hero
```css
.startup-hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, var(--start-primary), var(--start-secondary));
  color: white;
}

.startup-hero h1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
}
```

### 特色卡片
```css
.feature-card {
  padding: 32px;
  border-radius: 16px;
  background: white;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--start-primary), var(--start-secondary));
}
```

### CTA 按鈕
```css
.cta-button {
  background: linear-gradient(135deg, var(--start-primary), var(--start-secondary));
  color: white;
  padding: 16px 40px;
  border-radius: 100px;
  font-weight: 600;
  font-size: 1.125rem;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}
```

## 適用場景
- 科技新創
- SaaS 產品
- App 官網
- 創投公司
