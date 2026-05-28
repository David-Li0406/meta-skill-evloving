---
name: 法律風格
description: Legal - 傳統權威的法律服務設計
---

# 22. 法律風 Legal

## 概述
傳達專業、權威、信任的法律服務設計。

## 特徵
- 傳統穩重
- 權威感
- 深色調
- 嚴謹專業

## 配色
```css
:root {
  --legal-navy: #1e3a5f;
  --legal-dark: #0f172a;
  --legal-gold: #b8860b;
  --legal-light: #f8fafc;
  --legal-gray: #64748b;
}
```

## 字型
```css
h1, h2, h3 {
  font-family: 'Playfair Display', 'Noto Serif TC', serif;
}

body {
  font-family: 'Inter', 'Noto Sans TC', sans-serif;
}
```

## 元件

### 服務卡片
```css
.legal-card {
  background: white;
  border-left: 4px solid var(--legal-gold);
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
```

### 律師簡介
```css
.attorney-card {
  text-align: center;
}

.attorney-photo {
  width: 160px;
  height: 200px;
  object-fit: cover;
  filter: grayscale(30%);
}

.attorney-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  color: var(--legal-navy);
}

.attorney-title {
  color: var(--legal-gold);
  font-size: 14px;
}
```

### 按鈕
```css
.legal-button {
  background: var(--legal-navy);
  color: white;
  padding: 14px 32px;
  font-weight: 500;
}

.legal-button-gold {
  background: var(--legal-gold);
  color: white;
}
```

## 適用場景
- 律師事務所
- 法律顧問
- 公證服務
- 專業諮詢
