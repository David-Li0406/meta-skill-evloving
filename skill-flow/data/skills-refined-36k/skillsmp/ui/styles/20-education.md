---
name: 教育風格
description: Education - 友善清晰的教育學習風格
---

# 20. 教育風 Education

## 概述
友善、清晰、引導式的教育平台設計。

## 特徵
- 清晰導航
- 進度追蹤
- 友善互動
- 知識結構

## 配色
```css
:root {
  --edu-primary: #4f46e5;
  --edu-secondary: #06b6d4;
  --edu-success: #22c55e;
  --edu-warning: #f59e0b;
  --edu-bg: #f8fafc;
  --edu-text: #1e293b;
}
```

## 元件

### 課程卡片
```css
.course-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.course-image {
  aspect-ratio: 16/9;
  object-fit: cover;
}

.course-body {
  padding: 20px;
}

.course-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(79, 70, 229, 0.1);
  color: var(--edu-primary);
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
}
```

### 進度條
```css
.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 100px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--edu-primary), var(--edu-secondary));
  border-radius: 100px;
  transition: width 0.3s ease;
}
```

### 成就徽章
```css
.achievement {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border-radius: 12px;
}

.achievement-icon {
  width: 48px;
  height: 48px;
  background: var(--edu-warning);
  border-radius: 50%;
}
```

## 適用場景
- 線上課程
- 教育機構
- 學習平台
- 培訓系統
