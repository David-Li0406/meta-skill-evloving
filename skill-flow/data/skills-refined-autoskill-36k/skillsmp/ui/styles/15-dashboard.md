---
name: 儀表板風格
description: Dashboard - 數據視覺化的管理介面風格
---

# 15. 儀表板 Dashboard

## 概述
資料密集型管理介面的設計風格。

## 特徵
- 側邊欄導航
- 統計卡片
- 圖表區塊
- 表格資料

## 配色
```css
:root {
  --dash-bg: #f1f5f9;
  --dash-sidebar: #1e293b;
  --dash-card: #ffffff;
  --dash-primary: #3b82f6;
  --dash-success: #22c55e;
  --dash-warning: #f59e0b;
  --dash-danger: #ef4444;
  --dash-text: #334155;
}
```

## 佈局
```css
.dashboard {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: var(--dash-sidebar);
  color: white;
  padding: 24px;
}

.main {
  background: var(--dash-bg);
  padding: 24px;
}
```

## 統計卡片
```css
.stat-card {
  background: var(--dash-card);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--dash-text);
}

.stat-label {
  color: #64748b;
  font-size: 14px;
}

.stat-change {
  font-size: 14px;
  color: var(--dash-success);
}

.stat-change.negative {
  color: var(--dash-danger);
}
```

## 表格
```css
.data-table {
  width: 100%;
  background: var(--dash-card);
  border-radius: 12px;
  overflow: hidden;
}

.data-table th {
  background: #f8fafc;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

.data-table td {
  padding: 16px;
  border-top: 1px solid #e2e8f0;
}
```

## 適用場景
- 管理後台
- 數據平台
- CRM 系統
- 分析工具
