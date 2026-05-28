---
name: Bootstrap 指南
description: Bootstrap 5 開發最佳實踐
---

# 🅱️ Bootstrap 指南

## 安裝

```html
<!-- CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

```bash
# npm
npm install bootstrap
```

---

## 網格系統

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">欄位 1</div>
    <div class="col-12 col-md-6 col-lg-4">欄位 2</div>
    <div class="col-12 col-md-12 col-lg-4">欄位 3</div>
  </div>
</div>
```

### 斷點

| 斷點 | 縮寫 | 寬度 |
|-----|-----|------|
| Extra small | - | <576px |
| Small | sm | ≥576px |
| Medium | md | ≥768px |
| Large | lg | ≥992px |
| Extra large | xl | ≥1200px |
| XXL | xxl | ≥1400px |

---

## 常用元件

### 按鈕
```html
<button class="btn btn-primary">主要</button>
<button class="btn btn-secondary">次要</button>
<button class="btn btn-outline-primary">外框</button>
<button class="btn btn-lg">大按鈕</button>
<button class="btn btn-sm">小按鈕</button>
```

### 卡片
```html
<div class="card">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">標題</h5>
    <p class="card-text">內容</p>
    <a href="#" class="btn btn-primary">按鈕</a>
  </div>
</div>
```

### 導航
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container">
    <a class="navbar-brand" href="#">Logo</a>
    <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#nav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="#">連結</a></li>
      </ul>
    </div>
  </div>
</nav>
```

---

## 工具類別

```html
<!-- 間距 -->
<div class="p-4 m-2">padding 和 margin</div>
<div class="mt-3 mb-4">margin-top 和 bottom</div>

<!-- Flexbox -->
<div class="d-flex justify-content-between align-items-center">
  <span>左</span>
  <span>右</span>
</div>

<!-- 文字 -->
<p class="text-center text-primary fw-bold fs-4">樣式文字</p>

<!-- 顯示 -->
<div class="d-none d-md-block">平板以上顯示</div>
```

---

## 客製化

```scss
// 覆蓋變數
$primary: #6366f1;
$border-radius: 0.75rem;

@import "bootstrap/scss/bootstrap";
```
