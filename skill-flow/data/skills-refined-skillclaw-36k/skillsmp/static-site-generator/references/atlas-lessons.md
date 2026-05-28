# Lessons from Atlas & Official Site Build

Building the Atlas official site taught us several critical lessons for Gravito-based SSG.

## 1. The StaticLink Protocol

Gravito SSG 專案中，導航必須是「雙模式」：
- **Dev Mode**: Inertia AJAX（SPA 體驗）
- **Static Mode**: 標準瀏覽器導航（原生體驗）

使用官方套件的 `StaticLink`：
- React: `import { StaticLink } from '@gravito/freeze-react'`
- Vue: `import { StaticLink } from '@gravito/freeze-vue'`

沒有 StaticLink，在 GitHub Pages 上刷新子頁面會導致 404。

## 2. Naming Collision Avoidance
We discovered that having a view `src/views/Features.vue` and a component `src/components/Features.vue` causes Vite/Rollup to occasionally fail during tree-shaking, resulting in an empty page.
- **Fix**: Use the `View` suffix for all entry-point pages.

## 3. SPA Recovery Logic
Our `404.html` generator injects a script that:
1. Catches the current path on a 404 hit.
2. Checks if an `index.html` exists for that path.
3. If not, it falls back to the main SPA bundle to handle the route client-side.
This ensures that deep-links work even on "dumb" static servers.

## 4. Build-Time Data Fetching

在 `build-static.ts` 中直接獲取資料：

```typescript
// templates/static-site/build-static.ts
const routes = discoverRoutes(core)
for (const route of routes) {
  // 可在這裡根據 route 獲取對應資料
  const res = await core.adapter.fetch(new Request(`http://localhost${route}`))
  // ...
}
```

或定義自訂 hook 模式（需在 build script 中調用）：

```typescript
// src/hooks/index.ts
core.hooks.addFilter('ssg:data', async (data) => {
  if (data.pageName === 'Blog') {
    data.posts = await Post.all()
  }
  return data
})
```
