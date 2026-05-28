# Development Environment Troubleshooting

從 Official Site 開發經驗總結的故障排除指南。

## 症狀識別

當 `bun run dev` 後網站無法正常瀏覽時，檢查：
- 前端資源（`/app.tsx`、`/@vite/client`、`/styles.css`）是否返回 404
- Console 是否有 MIME type 錯誤
- 端口是否被佔用

---

## 關鍵問題

### 1. Bootstrap 執行順序

**問題**：`setupViteProxy` 在路由註冊之後調用，導致 proxy middleware 無法攔截請求。

**正確順序**：
```typescript
// src/bootstrap.ts

// 1. Setup Vite Proxy（必須在路由之前）
if (process.env.NODE_ENV !== 'production') {
  setupViteProxy(core)
}

// 2. Register Routes（在 proxy 之後）
registerRoutes(core)
```

### 2. Middleware 使用方式

**錯誤**：使用 `app.all()` 而非 `app.use()`

```typescript
// ❌ 錯誤 - app.all() 是路由處理器
app.all('*', async (c, next) => { ... })

// ✅ 正確 - app.use() 註冊為 middleware
app.use('*', async (c, next) => { ... })
```

### 3. CSS Content-Type 問題

**症狀**：
```
Failed to load module script: Expected a JavaScript-or-Wasm module script
but the server responded with a MIME type of "text/css".
```

**原因**：Vite 在開發模式下將 CSS import 轉換為 JS 模組（用於 HMR），不應強制覆蓋 Content-Type。

**修復**：保留 Vite 的原始 Content-Type
```typescript
// ❌ 錯誤
if (isCSS) {
  responseHeaders.set('Content-Type', 'text/css')
}

// ✅ 正確 - 保留 Vite 設置
if (isCSS) {
  const originalContentType = response.headers.get('content-type')
  // 只在 Vite 沒有提供有效類型時才 fallback
}
```

### 4. 端口衝突

**問題**：舊進程佔用端口（3000、5174）。

**解決方案**：使用 `predev` hook 自動清理
```json
{
  "scripts": {
    "predev": "bun run clean:ports",
    "dev": "bun run dev:vite & bun run dev:server",
    "clean:ports": "bun scripts/clean-port.ts 5174; bun scripts/clean-port.ts 3000"
  }
}
```

### 5. next() 函數檢查

在 middleware 中始終檢查 `next` 是否存在：
```typescript
if (next) {
  return await next()
}
return undefined
```

---

## 檢查清單

設置開發環境時確認：

- [ ] `setupViteProxy` 在 `registerRoutes` **之前**調用
- [ ] 使用 `app.use('*', ...)` 而非 `app.all('*', ...)`
- [ ] CSS Content-Type 保留 Vite 原始設置
- [ ] `predev` hook 清理端口
- [ ] Middleware 中有 `if (next)` 檢查
- [ ] Vite 配置 `strictPort: true`

---

## 最佳實踐

1. **執行順序**：Middleware → Proxy → Routes
2. **理解 Vite 行為**：開發模式下 CSS → JS 模組轉換
3. **自動化端口管理**：使用 `predev` hook
4. **在關鍵位置添加註釋**：說明執行順序和原因

---

## 相關檔案

- `src/bootstrap.ts` - 應用程式啟動邏輯
- `src/utils/vite.ts` - Vite proxy 設置
- `packages/core/src/engine/Gravito.ts` - Gravito Engine 核心
- `packages/core/src/engine/AOTRouter.ts` - 路由與 middleware 管理
