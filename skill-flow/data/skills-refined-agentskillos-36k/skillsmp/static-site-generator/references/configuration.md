# Gravito SSG Configuration

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STATIC_SITE_BASE_URL` | 靜態網站基礎 URL（用於 sitemap、CNAME） | `https://yourdomain.com` |
| `STATIC_SITE_DOMAINS` | 額外靜態域名（逗號分隔，傳給 Vite） | `''` |

## Bootstrap Configuration

在 `src/bootstrap.ts` 中配置：

```typescript
const config = defineConfig({
  config: {
    PORT: 3000,
    VIEW_DIR: 'src/views',  // 視圖目錄
  },
  orbits: [OrbitCache, OrbitPrism, OrbitIon],
})
```

## Output Directory

官方模板固定輸出到 `dist-static/`，定義在 `build-static.ts:65`：

```typescript
const outputDir = join(process.cwd(), 'dist-static')
```

## Built-in Hooks

框架提供的標準 hooks：

| Hook | Type | Description |
|------|------|-------------|
| `app:liftoff` | Action | 應用啟動時觸發 |
| `api:response` | Filter | API 回應過濾 |
| `view:helpers:register` | Action | 視圖 helper 註冊 |

## Custom SSG Hooks（建議模式）

可在 `src/hooks/index.ts` 中定義，並在 build script 中調用：

```typescript
// HTML 後處理
core.hooks.addFilter('ssg:rendered', async (html: string) => {
  return minify(html)
})
```

generate.ts 會自動調用 `ssg:rendered` filter（如已註冊）。
