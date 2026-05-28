---
name: static-site-generator
description: Framework-exclusive skill for Gravito SSG (Freeze Protocol). Operates directly on PlanetCore and Orbit systems. Use when user asks to: (1) Create static site with gravito create --template static-site, (2) Configure Freeze/SSG settings, (3) Fix StaticLink navigation issues, (4) Generate sitemap via OrbitConstellation, (5) Deploy to GitHub Pages/Vercel, (6) Debug deployment issues (404, empty pages, asset loading failures, MIME type errors), (7) Troubleshoot dev environment (Vite proxy, middleware order, port conflicts).
---

# Gravito Static Site Generator (Freeze Engine)

Gravito 框架專用的靜態網站生成器。NOT a general-purpose SSG tool.

## Core Packages

| 套件 | 用途 |
|------|------|
| `@gravito/freeze` | SSG 核心模組 |
| `@gravito/freeze-react` | React StaticLink + useFreeze hook |
| `@gravito/freeze-vue` | Vue StaticLink + useFreeze composable |
| `@gravito/prism` | 視圖引擎 + StaticSiteGenerator (packages/prism/src/SSG.ts) |
| `@gravito/constellation` | Sitemap 生成 + 重定向管理 |

## Framework Integration

### PlanetCore Liftoff
Generator boots headless PlanetCore instance，確保每個頁面經過：
- **Middlewares**: CSP, Security Headers
- **Orbits**: OrbitIon (Inertia), OrbitPrism (Templates)
- **Hooks**: 專案 hooks 目錄中的 Filters/Actions

### Freeze Protocol
Static Generation = **Freezing**。透過 `core.adapter.fetch` 進行內部請求分派。

## Workflow

```bash
# 1. Scaffold
gravito create my-site --template static-site --framework react  # or vue

# 2. Develop
bun run dev

# 3. Freeze (Build)
bun run build:static

# 4. Preview
bun run preview:static
```

## StaticLink (Official)

NEVER use `<Link>` from Inertia for static routes. Use official packages：

```tsx
// React - from @gravito/freeze-react
import { StaticLink, useFreeze } from '@gravito/freeze-react'
<StaticLink href="/about">About</StaticLink>

// Vue - from @gravito/freeze-vue
import { StaticLink, useFreeze } from '@gravito/freeze-vue'
<StaticLink href="/about">About</StaticLink>
```

Features:
- 自動偵測靜態環境 (github.io, vercel.app, port 4173)
- i18n 路徑本地化 (`getLocalizedPath`)
- `skipLocalization` prop 可跳過

## Custom Hooks（建議模式）

可在 `src/hooks/index.ts` 定義，generate.ts 會自動調用：

```typescript
// HTML 後處理（generate.ts 自動調用）
core.hooks.addFilter('ssg:rendered', async (html: string) => {
  return minify(html)
})
```

詳見 `references/configuration.md`

## Development Environment

開發環境常見問題：

| 症狀 | 可能原因 |
|------|---------|
| 前端資源 404 | Vite proxy 未正確設置，或 bootstrap 順序錯誤 |
| CSS MIME type 錯誤 | 強制覆蓋了 Vite 的 Content-Type |
| 端口衝突 | 舊進程佔用端口 |

**關鍵原則**：
- `setupViteProxy` 必須在 `registerRoutes` **之前**調用
- 使用 `app.use('*', ...)` 而非 `app.all('*', ...)`
- 保留 Vite 原始 Content-Type，勿強制覆蓋

詳見 `references/dev-troubleshooting.md`

## Best Practices

- **Suffix Views**: Entry-point components use `*View.vue` / `*View.tsx` to avoid naming collisions
- **SPA Recovery**: SSG 自動生成 `404.html` with recovery script for deep-links
- **Build Verification**: 部署前執行 `bun run preview:static` 確認：
  - Assets 從 `/static/build/` 載入
  - `404.html` 存在於 root
  - CNAME 檔案已生成（若適用）
- **Dev Environment**: 確保 bootstrap 順序正確（Middleware → Proxy → Routes）

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate.ts` | 完整 SSG 生成腳本（可複製到專案使用） |
| `scripts/verify.ts` | 驗證構建輸出是否符合預期 |

### generate.ts

功能完整的 SSG 腳本，包含：
- Vite client build
- Route rendering via `core.adapter.fetch`
- Sitemap 生成
- 404.html with SPA recovery
- Static asset 複製
- CNAME + .nojekyll 生成

使用方式：
1. 複製到專案根目錄
2. 修改 `BOOTSTRAP_PATH` 和 `KNOWN_ROUTES`
3. `bun run generate.ts`

或直接使用官方 `bun run build:static`

### verify.ts

需要配置檔（預設 `ssg.verify.json`）：
```json
{
  "outDir": "dist-static",
  "checks": [
    { "file": "index.html", "contains": ["<!DOCTYPE html>"] },
    { "file": "404.html", "contains": ["SPA routing"] }
  ]
}
```

## References

- **references/configuration.md**: 環境變數、bootstrap 配置、hooks 說明
- **references/atlas-lessons.md**: StaticLink 問題排查、命名衝突、SPA recovery 經驗
- **references/dev-troubleshooting.md**: 開發環境故障排除（Vite proxy、middleware 順序、端口衝突）