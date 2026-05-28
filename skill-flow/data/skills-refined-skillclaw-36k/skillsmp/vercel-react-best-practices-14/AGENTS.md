# React 最佳實踐

**版本 1.0.0**  
Vercel Engineering  
2026 年 1 月

> **注意：**  
> 本文件主要供 AI 代理和大型語言模型在維護、生成或重構 Vercel 的 React 和 Next.js 程式碼庫時遵循。人類開發者也可能會覺得有用，但此處的指引已針對自動化和 AI 輔助工作流程的一致性進行最佳化。

---

## 摘要

針對 React 和 Next.js 應用程式設計的全面效能最佳化指南，專為 AI 代理和大型語言模型打造。包含 8 個類別中的 40 多條規則，按影響程度從關鍵（消除瀑布流、減少打包體積）到漸進式（進階模式）進行優先排序。每條規則都包含詳細說明、比較錯誤與正確實作的真實範例，以及具體的影響指標，以指導自動化重構和程式碼生成。

---

## 目錄

1. [消除瀑布流](#1-消除瀑布流) — **關鍵**
   - 1.1 [延遲 Await 直到需要時](#11-延遲-await-直到需要時)
   - 1.2 [基於依賴關係的平行化](#12-基於依賴關係的平行化)
   - 1.3 [防止 API 路由中的瀑布流鏈](#13-防止-api-路由中的瀑布流鏈)
   - 1.4 [對獨立操作使用 Promise.all()](#14-對獨立操作使用-promiseall)
   - 1.5 [策略性 Suspense 邊界](#15-策略性-suspense-邊界)
2. [打包體積最佳化](#2-打包體積最佳化) — **關鍵**
   - 2.1 [避免桶檔案匯入](#21-避免桶檔案匯入)
   - 2.2 [條件式模組載入](#22-條件式模組載入)
   - 2.3 [延遲非關鍵第三方函式庫](#23-延遲非關鍵第三方函式庫)
   - 2.4 [對大型元件使用動態匯入](#24-對大型元件使用動態匯入)
   - 2.5 [基於使用者意圖的預載](#25-基於使用者意圖的預載)
3. [伺服器端效能](#3-伺服器端效能) — **高**
   - 3.1 [跨請求 LRU 快取](#31-跨請求-lru-快取)
   - 3.2 [在 RSC 邊界最小化序列化](#32-在-rsc-邊界最小化序列化)
   - 3.3 [透過元件組合實現平行資料擷取](#33-透過元件組合實現平行資料擷取)
   - 3.4 [使用 React.cache() 進行每個請求的去重](#34-使用-reactcache-進行每個請求的去重)
   - 3.5 [使用 after() 處理非阻塞操作](#35-使用-after-處理非阻塞操作)
4. [客戶端資料擷取](#4-客戶端資料擷取) — **中高**
   - 4.1 [去重全域事件監聽器](#41-去重全域事件監聽器)
   - 4.2 [使用被動事件監聽器改善滾動效能](#42-使用被動事件監聽器改善滾動效能)
   - 4.3 [使用 SWR 進行自動去重](#43-使用-swr-進行自動去重)
   - 4.4 [版本化並最小化 localStorage 資料](#44-版本化並最小化-localstorage-資料)
5. [重新渲染最佳化](#5-重新渲染最佳化) — **中**
   - 5.1 [延遲狀態讀取到使用點](#51-延遲狀態讀取到使用點)
   - 5.2 [提取到記憶化元件](#52-提取到記憶化元件)
   - 5.3 [縮小 Effect 依賴項](#53-縮小-effect-依賴項)
   - 5.4 [訂閱衍生狀態](#54-訂閱衍生狀態)
   - 5.5 [使用函式式 setState 更新](#55-使用函式式-setstate-更新)
   - 5.6 [使用延遲狀態初始化](#56-使用延遲狀態初始化)
   - 5.7 [對非緊急更新使用 Transitions](#57-對非緊急更新使用-transitions)
6. [渲染效能](#6-渲染效能) — **中**
   - 6.1 [動畫 SVG 包裝器而不是 SVG 元素](#61-動畫-svg-包裝器而不是-svg-元素)
   - 6.2 [對長列表使用 CSS content-visibility](#62-對長列表使用-css-content-visibility)
   - 6.3 [提升靜態 JSX 元素](#63-提升靜態-jsx-元素)
   - 6.4 [最佳化 SVG 精度](#64-最佳化-svg-精度)
   - 6.5 [防止 Hydration 不匹配且不閃爍](#65-防止-hydration-不匹配且不閃爍)
   - 6.6 [使用 Activity 元件進行顯示/隱藏](#66-使用-activity-元件進行顯示隱藏)
   - 6.7 [使用明確的條件渲染](#67-使用明確的條件渲染)
7. [JavaScript 效能](#7-javascript-效能) — **低中**
   - 7.1 [批次處理 DOM CSS 變更](#71-批次處理-dom-css-變更)
   - 7.2 [為重複查詢建立索引 Map](#72-為重複查詢建立索引-map)
   - 7.3 [在迴圈中快取屬性存取](#73-在迴圈中快取屬性存取)
   - 7.4 [快取重複的函式呼叫](#74-快取重複的函式呼叫)
   - 7.5 [快取 Storage API 呼叫](#75-快取-storage-api-呼叫)
   - 7.6 [合併多個陣列迭代](#76-合併多個陣列迭代)
   - 7.7 [在陣列比較前提前檢查長度](#77-在陣列比較前提前檢查長度)
   - 7.8 [從函式提前返回](#78-從函式提前返回)
   - 7.9 [提升 RegExp 建立](#79-提升-regexp-建立)
   - 7.10 [使用迴圈而非排序來查找最小/最大值](#710-使用迴圈而非排序來查找最小最大值)
   - 7.11 [使用 Set/Map 進行 O(1) 查詢](#711-使用-setmap-進行-o1-查詢)
   - 7.12 [使用 toSorted() 而非 sort() 以保持不可變性](#712-使用-tosorted-而非-sort-以保持不可變性)
8. [進階模式](#8-進階模式) — **低**
   - 8.1 [在 Refs 中儲存事件處理器](#81-在-refs-中儲存事件處理器)
   - 8.2 [使用 useLatest 建立穩定的回呼 Refs](#82-使用-uselatest-建立穩定的回呼-refs)

---

## 1. 消除瀑布流

**影響：關鍵**

瀑布流是效能殺手第一名。每個連續的 await 都會增加完整的網路延遲。消除它們可以獲得最大的收益。

### 1.1 延遲 Await 直到需要時

**影響：高（避免阻塞未使用的程式碼路徑）**

將 `await` 操作移到實際使用它們的分支中，以避免阻塞不需要它們的程式碼路徑。

**錯誤：阻塞兩個分支**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId);

  if (skipProcessing) {
    // 立即返回但仍然等待了 userData
    return { skipped: true };
  }

  // 只有這個分支使用 userData
  return processUserData(userData);
}
```

**正確：只在需要時阻塞**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    // 立即返回而不等待
    return { skipped: true };
  }

  // 只在需要時擷取
  const userData = await fetchUserData(userId);
  return processUserData(userData);
}
```

**另一個範例：提前返回最佳化**

```typescript
// 錯誤：總是擷取權限
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId);
  const resource = await getResource(resourceId);

  if (!resource) {
    return { error: "Not found" };
  }

  if (!permissions.canEdit) {
    return { error: "Forbidden" };
  }

  return await updateResourceData(resource, permissions);
}

// 正確：只在需要時擷取
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId);

  if (!resource) {
    return { error: "Not found" };
  }

  const permissions = await fetchPermissions(userId);

  if (!permissions.canEdit) {
    return { error: "Forbidden" };
  }

  return await updateResourceData(resource, permissions);
}
```

當跳過的分支經常被採用，或當延遲的操作成本高昂時，這種最佳化特別有價值。

### 1.2 基於依賴關係的平行化

**影響：關鍵（2-10 倍改善）**

對於具有部分依賴關係的操作，使用 `better-all` 來最大化平行性。它會在最早可能的時刻自動啟動每個任務。

**錯誤：profile 不必要地等待 config**

```typescript
const [user, config] = await Promise.all([fetchUser(), fetchConfig()]);
const profile = await fetchProfile(user.id);
```

**正確：config 和 profile 平行執行**

```typescript
import { all } from "better-all";

const { user, config, profile } = await all({
  async user() {
    return fetchUser();
  },
  async config() {
    return fetchConfig();
  },
  async profile() {
    return fetchProfile((await this.$.user).id);
  },
});
```

參考：[https://github.com/shuding/better-all](https://github.com/shuding/better-all)

### 1.3 防止 API 路由中的瀑布流鏈

**影響：關鍵（2-10 倍改善）**

在 API 路由和 Server Actions 中，立即啟動獨立操作，即使您還沒有 await 它們。

**錯誤：config 等待 auth，data 等待兩者**

```typescript
export async function GET(request: Request) {
  const session = await auth();
  const config = await fetchConfig();
  const data = await fetchData(session.user.id);
  return Response.json({ data, config });
}
```

**正確：auth 和 config 立即啟動**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth();
  const configPromise = fetchConfig();
  const session = await sessionPromise;
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id),
  ]);
  return Response.json({ data, config });
}
```

對於具有更複雜依賴鏈的操作，使用 `better-all` 自動最大化平行性（參見基於依賴關係的平行化）。

### 1.4 對獨立操作使用 Promise.all()

**影響：關鍵（2-10 倍改善）**

當非同步操作沒有相互依賴時，使用 `Promise.all()` 同時執行它們。

**錯誤：連續執行，3 次往返**

```typescript
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();
```

**正確：平行執行，1 次往返**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
```

### 1.5 策略性 Suspense 邊界

**影響：高（更快的初始繪製）**

不要在非同步元件中在返回 JSX 之前 await 資料，而是使用 Suspense 邊界在資料載入時更快地顯示包裝器 UI。

**錯誤：包裝器被資料擷取阻塞**

```tsx
async function Page() {
  const data = await fetchData(); // 阻塞整個頁面

  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  );
}
```

即使只有中間部分需要資料，整個佈局也會等待資料。

**正確：包裝器立即顯示，資料串流進入**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  );
}

async function DataDisplay() {
  const data = await fetchData(); // 只阻塞這個元件
  return <div>{data.content}</div>;
}
```

Sidebar、Header 和 Footer 立即渲染。只有 DataDisplay 等待資料。

**替代方案：在元件之間共享 promise**

```tsx
function Page() {
  // 立即開始擷取，但不要 await
  const dataPromise = fetchData();

  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  );
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise); // 解包 promise
  return <div>{data.content}</div>;
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise); // 重用相同的 promise
  return <div>{data.summary}</div>;
}
```

兩個元件共享相同的 promise，所以只發生一次擷取。佈局立即渲染，而兩個元件一起等待。

**何時不使用此模式：**

- 佈局決策所需的關鍵資料（影響定位）

- SEO 關鍵的首屏內容

- 小型、快速的查詢，其中 suspense 開銷不值得

- 當您想避免佈局偏移時（載入 → 內容跳躍）

**權衡：** 更快的初始繪製 vs 潛在的佈局偏移。根據您的 UX 優先順序選擇。

---

## 2. 打包體積最佳化

**影響：關鍵**

減少初始打包體積可改善互動時間（Time to Interactive）和最大內容繪製（Largest Contentful Paint）。

### 2.1 避免桶檔案匯入

**影響：關鍵（200-800ms 匯入成本，建置緩慢）**

直接從來源檔案匯入而不是從桶檔案匯入，以避免載入數千個未使用的模組。**桶檔案**是重新匯出多個模組的入口點（例如，執行 `export * from './module'` 的 `index.js`）。

流行的圖示和元件函式庫在其入口檔案中可能有**多達 10,000 個重新匯出**。對於許多 React 套件，**僅匯入它們就需要 200-800ms**，影響開發速度和生產環境的冷啟動。

**為什麼 tree-shaking 沒有幫助：** 當函式庫被標記為外部（未打包）時，打包器無法最佳化它。如果您打包它以啟用 tree-shaking，建置會變得非常慢，需要分析整個模組圖。

**錯誤：匯入整個函式庫**

```tsx
import { Check, X, Menu } from "lucide-react";
// 載入 1,583 個模組，在開發環境中額外耗時約 2.8 秒
// 執行時成本：每次冷啟動 200-800ms

import { Button, TextField } from "@mui/material";
// 載入 2,225 個模組，在開發環境中額外耗時約 4.2 秒
```

**正確：只匯入您需要的**

```tsx
import Check from "lucide-react/dist/esm/icons/check";
import X from "lucide-react/dist/esm/icons/x";
import Menu from "lucide-react/dist/esm/icons/menu";
// 只載入 3 個模組（約 2KB vs 約 1MB）

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
// 只載入您使用的
```

**替代方案：Next.js 13.5+**

```js
// next.config.js - 使用 optimizePackageImports
module.exports = {
  experimental: {
    optimizePackageImports: ["lucide-react", "@mui/material"],
  },
};

// 然後您可以保留符合人體工學的桶檔案匯入：
import { Check, X, Menu } from "lucide-react";
// 在建置時自動轉換為直接匯入
```

直接匯入提供 15-70% 更快的開發啟動、28% 更快的建置、40% 更快的冷啟動，以及顯著更快的 HMR。

常受影響的函式庫：`lucide-react`、`@mui/material`、`@mui/icons-material`、`@tabler/icons-react`、`react-icons`、`@headlessui/react`、`@radix-ui/react-*`、`lodash`、`ramda`、`date-fns`、`rxjs`、`react-use`。

參考：[https://vercel.com/blog/how-we-optimized-package-imports-in-next-js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)

### 2.2 條件式模組載入

**影響：高（只在需要時載入大型資料）**

只在功能啟動時載入大型資料或模組。

**範例：延遲載入動畫幀**

```tsx
function AnimationPlayer({
  enabled,
  setEnabled,
}: {
  enabled: boolean;
  setEnabled: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const [frames, setFrames] = useState<Frame[] | null>(null);

  useEffect(() => {
    if (enabled && !frames && typeof window !== "undefined") {
      import("./animation-frames.js")
        .then((mod) => setFrames(mod.frames))
        .catch(() => setEnabled(false));
    }
  }, [enabled, frames, setEnabled]);

  if (!frames) return <Skeleton />;
  return <Canvas frames={frames} />;
}
```

`typeof window !== 'undefined'` 檢查防止為 SSR 打包此模組，最佳化伺服器打包體積和建置速度。

### 2.3 延遲非關鍵第三方函式庫

**影響：中（在 hydration 後載入）**

分析、日誌記錄和錯誤追蹤不會阻塞使用者互動。在 hydration 後載入它們。

**錯誤：阻塞初始打包**

```tsx
import { Analytics } from "@vercel/analytics/react";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

**正確：在 hydration 後載入**

```tsx
import dynamic from "next/dynamic";

const Analytics = dynamic(
  () => import("@vercel/analytics/react").then((m) => m.Analytics),
  { ssr: false },
);

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 2.4 對大型元件使用動態匯入

**影響：關鍵（直接影響 TTI 和 LCP）**

使用 `next/dynamic` 延遲載入初始渲染時不需要的大型元件。

**錯誤：Monaco 與主區塊一起打包 約 300KB**

```tsx
import { MonacoEditor } from "./monaco-editor";

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />;
}
```

**正確：Monaco 按需載入**

```tsx
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(
  () => import("./monaco-editor").then((m) => m.MonacoEditor),
  { ssr: false },
);

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />;
}
```

### 2.5 基於使用者意圖的預載

**影響：中（減少感知延遲）**

在需要之前預載大型打包檔案以減少感知延遲。

**範例：在懸停/聚焦時預載**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== "undefined") {
      void import("./monaco-editor");
    }
  };

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  );
}
```

**範例：當功能旗標啟用時預載**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== "undefined") {
      void import("./monaco-editor").then((mod) => mod.init());
    }
  }, [flags.editorEnabled]);

  return (
    <FlagsContext.Provider value={flags}>{children}</FlagsContext.Provider>
  );
}
```

`typeof window !== 'undefined'` 檢查防止為 SSR 打包預載的模組，最佳化伺服器打包體積和建置速度。

---

## 3. 伺服器端效能

**影響：高**

最佳化伺服器端渲染和資料擷取可消除伺服器端瀑布流並減少回應時間。

### 3.1 跨請求 LRU 快取

**影響：高（跨請求快取）**

`React.cache()` 只在一個請求內有效。對於在連續請求之間共享的資料（使用者點擊按鈕 A 然後按鈕 B），使用 LRU 快取。

**實作：**

```typescript
import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000, // 5 分鐘
});

export async function getUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;

  const user = await db.user.findUnique({ where: { id } });
  cache.set(id, user);
  return user;
}

// 請求 1：資料庫查詢，結果被快取
// 請求 2：快取命中，無資料庫查詢
```

當連續的使用者操作在幾秒鐘內命中需要相同資料的多個端點時使用。

**使用 Vercel 的 [Fluid Compute](https://vercel.com/docs/fluid-compute)：** LRU 快取特別有效，因為多個並發請求可以共享相同的函式實例和快取。這意味著快取在請求之間持續存在，無需外部儲存如 Redis。

**在傳統 serverless 中：** 每次呼叫都在隔離中執行，因此考慮使用 Redis 進行跨處理程序快取。

參考：[https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

### 3.2 在 RSC 邊界最小化序列化

**影響：高（減少資料傳輸大小）**

React Server/Client 邊界會將所有物件屬性序列化為字串，並將它們嵌入 HTML 回應和後續的 RSC 請求中。這些序列化的資料直接影響頁面權重和載入時間，所以**大小很重要**。只傳遞客戶端實際使用的欄位。

**錯誤：序列化所有 50 個欄位**

```tsx
async function Page() {
  const user = await fetchUser(); // 50 個欄位
  return <Profile user={user} />;
}

("use client");
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>; // 使用 1 個欄位
}
```

**正確：只序列化 1 個欄位**

```tsx
async function Page() {
  const user = await fetchUser();
  return <Profile name={user.name} />;
}

("use client");
function Profile({ name }: { name: string }) {
  return <div>{name}</div>;
}
```

### 3.3 透過元件組合實現平行資料擷取

**影響：關鍵（消除伺服器端瀑布流）**

React Server Components 在樹中按順序執行。使用組合重構以平行化資料擷取。

**錯誤：Sidebar 等待 Page 的擷取完成**

```tsx
export default async function Page() {
  const header = await fetchHeader();
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  );
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}
```

**正確：兩者同時擷取**

```tsx
async function Header() {
  const data = await fetchHeader();
  return <div>{data}</div>;
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
```

**使用 children prop 的替代方案：**

```tsx
async function Header() {
  const data = await fetchHeader();
  return <div>{data}</div>;
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}

function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Header />
      {children}
    </div>
  );
}

export default function Page() {
  return (
    <Layout>
      <Sidebar />
    </Layout>
  );
}
```

### 3.4 使用 React.cache() 進行每個請求的去重

**影響：中（在請求內去重）**

使用 `React.cache()` 進行伺服器端請求去重。身份驗證和資料庫查詢最受益。

**用法：**

```typescript
import { cache } from "react";

export const getCurrentUser = cache(async () => {
  const session = await auth();
  if (!session?.user?.id) return null;
  return await db.user.findUnique({
    where: { id: session.user.id },
  });
});
```

在單個請求中，多次呼叫 `getCurrentUser()` 只執行一次查詢。

**避免將內聯物件作為引數：**

`React.cache()` 使用淺相等（`Object.is`）來確定快取命中。內聯物件在每次呼叫時建立新引用，防止快取命中。

**錯誤：總是快取未命中**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } });
});

// 每次呼叫建立新物件，永遠不會命中快取
getUser({ uid: 1 });
getUser({ uid: 1 }); // 快取未命中，再次執行查詢
```

**正確：快取命中**

```typescript
const params = { uid: 1 };
getUser(params); // 查詢執行
getUser(params); // 快取命中（相同引用）
```

如果您必須傳遞物件，請傳遞相同的引用：

**Next.js 特定注意事項：**

在 Next.js 中，`fetch` API 會自動擴展請求記憶化。在單個請求中，具有相同 URL 和選項的請求會自動去重，因此您不需要為 `fetch` 呼叫使用 `React.cache()`。但是，`React.cache()` 對於其他非同步任務仍然是必要的：

- 資料庫查詢（Prisma、Drizzle 等）

- 繁重的計算

- 身份驗證檢查

- 檔案系統操作

- 任何非 fetch 的非同步工作

使用 `React.cache()` 在元件樹中去重這些操作。

參考：[https://react.dev/reference/react/cache](https://react.dev/reference/react/cache)

### 3.5 使用 after() 處理非阻塞操作

**影響：中（更快的回應時間）**

使用 Next.js 的 `after()` 來排程應在回應發送後執行的工作。這可以防止日誌記錄、分析和其他副作用阻塞回應。

**錯誤：阻塞回應**

```tsx
import { logUserAction } from "@/app/utils";

export async function POST(request: Request) {
  // 執行變更
  await updateDatabase(request);

  // 日誌記錄阻塞回應
  const userAgent = request.headers.get("user-agent") || "unknown";
  await logUserAction({ userAgent });

  return new Response(JSON.stringify({ status: "success" }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
```

**正確：非阻塞**

```tsx
import { after } from "next/server";
import { headers, cookies } from "next/headers";
import { logUserAction } from "@/app/utils";

export async function POST(request: Request) {
  // 執行變更
  await updateDatabase(request);

  // 在回應發送後記錄
  after(async () => {
    const userAgent = (await headers()).get("user-agent") || "unknown";
    const sessionCookie =
      (await cookies()).get("session-id")?.value || "anonymous";

    logUserAction({ sessionCookie, userAgent });
  });

  return new Response(JSON.stringify({ status: "success" }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
```

回應立即發送，而日誌記錄在後台發生。

**常見用例：**

- 分析追蹤

- 稽核日誌記錄

- 發送通知

- 快取失效

- 清理任務

**重要注意事項：**

- 即使回應失敗或重新導向，`after()` 也會執行

- 可在 Server Actions、Route Handlers 和 Server Components 中使用

參考：[https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)

---

## 4. 客戶端資料擷取

**影響：中高**

自動去重和高效的資料擷取模式可減少冗餘的網路請求。

### 4.1 去重全域事件監聽器

**影響：低（N 個元件使用單一監聽器）**

使用 `useSWRSubscription()` 在元件實例之間共享全域事件監聽器。

**錯誤：N 個實例 = N 個監聽器**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [key, callback]);
}
```

當多次使用 `useKeyboardShortcut` hook 時，每個實例都會註冊一個新監聽器。

**正確：N 個實例 = 1 個監聽器**

```tsx
import useSWRSubscription from "swr/subscription";

// 模組層級的 Map 來追蹤每個按鍵的回呼
const keyCallbacks = new Map<string, Set<() => void>>();

function useKeyboardShortcut(key: string, callback: () => void) {
  // 在 Map 中註冊此回呼
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set());
    }
    keyCallbacks.get(key)!.add(callback);

    return () => {
      const set = keyCallbacks.get(key);
      if (set) {
        set.delete(callback);
        if (set.size === 0) {
          keyCallbacks.delete(key);
        }
      }
    };
  }, [key, callback]);

  useSWRSubscription("global-keydown", () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach((cb) => cb());
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  });
}

function Profile() {
  // 多個快捷鍵將共享相同的監聽器
  useKeyboardShortcut("p", () => {
    /* ... */
  });
  useKeyboardShortcut("k", () => {
    /* ... */
  });
  // ...
}
```

### 4.2 使用被動事件監聽器改善滾動效能

**影響：中（消除事件監聽器造成的滾動延遲）**

為觸控和滾輪事件監聽器添加 `{ passive: true }` 以啟用即時滾動。瀏覽器通常會等待監聽器完成以檢查是否呼叫了 `preventDefault()`，這會導致滾動延遲。

**錯誤：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener("touchstart", handleTouch);
  document.addEventListener("wheel", handleWheel);

  return () => {
    document.removeEventListener("touchstart", handleTouch);
    document.removeEventListener("wheel", handleWheel);
  };
}, []);
```

**正確：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener("touchstart", handleTouch, { passive: true });
  document.addEventListener("wheel", handleWheel, { passive: true });

  return () => {
    document.removeEventListener("touchstart", handleTouch);
    document.removeEventListener("wheel", handleWheel);
  };
}, []);
```

**何時使用 passive：** 追蹤/分析、日誌記錄、任何不呼叫 `preventDefault()` 的監聽器。

**何時不使用 passive：** 實作自訂滑動手勢、自訂縮放控制項，或任何需要 `preventDefault()` 的監聽器。

### 4.3 使用 SWR 進行自動去重

**影響：中高（自動去重）**

SWR 可在元件實例之間實現請求去重、快取和重新驗證。

**錯誤：沒有去重，每個實例都擷取**

```tsx
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch("/api/users")
      .then((r) => r.json())
      .then(setUsers);
  }, []);
}
```

**正確：多個實例共享一個請求**

```tsx
import useSWR from "swr";

function UserList() {
  const { data: users } = useSWR("/api/users", fetcher);
}
```

**對於不可變資料：**

```tsx
import { useImmutableSWR } from "@/lib/swr";

function StaticContent() {
  const { data } = useImmutableSWR("/api/config", fetcher);
}
```

**對於變更：**

```tsx
import { useSWRMutation } from "swr/mutation";

function UpdateButton() {
  const { trigger } = useSWRMutation("/api/user", updateUser);
  return <button onClick={() => trigger()}>Update</button>;
}
```

參考：[https://swr.vercel.app](https://swr.vercel.app)

### 4.4 版本化並最小化 localStorage 資料

**影響：中（防止架構衝突，減少儲存大小）**

為鍵添加版本前綴並只儲存需要的欄位。防止架構衝突和意外儲存敏感資料。

**錯誤：**

```typescript
// 沒有版本，儲存所有內容，沒有錯誤處理
localStorage.setItem("userConfig", JSON.stringify(fullUserObject));
const data = localStorage.getItem("userConfig");
```

**正確：**

```typescript
const VERSION = "v2";

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config));
  } catch {
    // 在無痕/私密瀏覽、配額超出或停用時拋出
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

// 從 v1 遷移到 v2
function migrate() {
  try {
    const v1 = localStorage.getItem("userConfig:v1");
    if (v1) {
      const old = JSON.parse(v1);
      saveConfig({
        theme: old.darkMode ? "dark" : "light",
        language: old.lang,
      });
      localStorage.removeItem("userConfig:v1");
    }
  } catch {}
}
```

**從伺服器回應儲存最少欄位：**

```typescript
// User 物件有 20 多個欄位，只儲存 UI 需要的
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem(
      "prefs:v1",
      JSON.stringify({
        theme: user.preferences.theme,
        notifications: user.preferences.notifications,
      }),
    );
  } catch {}
}
```

**始終包裝在 try-catch 中：** `getItem()` 和 `setItem()` 在無痕/私密瀏覽（Safari、Firefox）、配額超出或停用時會拋出錯誤。

**優點：** 透過版本控制實現架構演進、減少儲存大小、防止儲存令牌/PII/內部旗標。

---

## 5. 重新渲染最佳化

**影響：中**

減少不必要的重新渲染可最小化浪費的計算並改善 UI 回應性。

### 5.1 延遲狀態讀取到使用點

**影響：中（避免不必要的訂閱）**

如果您只在回呼中讀取動態狀態（searchParams、localStorage），請不要訂閱它。

**錯誤：訂閱所有 searchParams 變更**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams();

  const handleShare = () => {
    const ref = searchParams.get("ref");
    shareChat(chatId, { ref });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

**正確：按需讀取，無訂閱**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get("ref");
    shareChat(chatId, { ref });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

### 5.2 提取到記憶化元件

**影響：中（啟用提前返回）**

將昂貴的工作提取到記憶化元件中，以在計算之前啟用提前返回。

**錯誤：即使在載入時也計算 avatar**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user);
    return <Avatar id={id} />;
  }, [user]);

  if (loading) return <Skeleton />;
  return <div>{avatar}</div>;
}
```

**正確：載入時跳過計算**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user]);
  return <Avatar id={id} />;
});

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />;
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  );
}
```

**注意：** 如果您的專案啟用了 [React Compiler](https://react.dev/learn/react-compiler)，則不需要使用 `memo()` 和 `useMemo()` 進行手動記憶化。編譯器會自動最佳化重新渲染。

### 5.3 縮小 Effect 依賴項

**影響：低（最小化 effect 重新執行）**

指定原始依賴項而不是物件，以最小化 effect 重新執行。

**錯誤：在任何 user 欄位變更時重新執行**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user]);
```

**正確：只在 id 變更時重新執行**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user.id]);
```

**對於衍生狀態，在 effect 外部計算：**

```tsx
// 錯誤：在 width=767、766、765... 時執行
useEffect(() => {
  if (width < 768) {
    enableMobileMode();
  }
}, [width]);

// 正確：只在布林值轉換時執行
const isMobile = width < 768;
useEffect(() => {
  if (isMobile) {
    enableMobileMode();
  }
}, [isMobile]);
```

### 5.4 訂閱衍生狀態

**影響：中（降低重新渲染頻率）**

訂閱衍生的布林狀態而不是連續值，以降低重新渲染頻率。

**錯誤：每個像素變更時重新渲染**

```tsx
function Sidebar() {
  const width = useWindowWidth(); // 持續更新
  const isMobile = width < 768;
  return <nav className={isMobile ? "mobile" : "desktop"} />;
}
```

**正確：只在布林值變更時重新渲染**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery("(max-width: 767px)");
  return <nav className={isMobile ? "mobile" : "desktop"} />;
}
```

### 5.5 使用函式式 setState 更新

**影響：中（防止過時閉包和不必要的回呼重建）**

當基於當前狀態值更新狀態時，使用 setState 的函式更新形式而不是直接引用狀態變數。這可以防止過時閉包、消除不必要的依賴項，並建立穩定的回呼引用。

**錯誤：需要狀態作為依賴項**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  // 回呼必須依賴 items，在每次 items 變更時重建
  const addItems = useCallback(
    (newItems: Item[]) => {
      setItems([...items, ...newItems]);
    },
    [items],
  ); // ❌ items 依賴項導致重建

  // 如果忘記依賴項，則有過時閉包的風險
  const removeItem = useCallback((id: string) => {
    setItems(items.filter((item) => item.id !== id));
  }, []); // ❌ 缺少 items 依賴項 - 將使用過時的 items！

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

第一個回呼在每次 `items` 變更時重建，這可能導致子元件不必要地重新渲染。第二個回呼有過時閉包錯誤——它總是引用初始的 `items` 值。

**正確：穩定的回呼，沒有過時閉包**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  // 穩定的回呼，永不重建
  const addItems = useCallback((newItems: Item[]) => {
    setItems((curr) => [...curr, ...newItems]);
  }, []); // ✅ 不需要依賴項

  // 總是使用最新狀態，沒有過時閉包風險
  const removeItem = useCallback((id: string) => {
    setItems((curr) => curr.filter((item) => item.id !== id));
  }, []); // ✅ 安全且穩定

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

**優點：**

1. **穩定的回呼引用** - 當狀態變更時不需要重建回呼

2. **沒有過時閉包** - 總是操作最新的狀態值

3. **更少的依賴項** - 簡化依賴項陣列並減少記憶體洩漏

4. **防止錯誤** - 消除 React 閉包錯誤的最常見來源

**何時使用函式式更新：**

- 任何依賴當前狀態值的 setState

- 在需要狀態時在 useCallback/useMemo 內部

- 引用狀態的事件處理器

- 更新狀態的非同步操作

**何時直接更新是可以的：**

- 將狀態設定為靜態值：`setCount(0)`

- 僅從 props/引數設定狀態：`setName(newName)`

- 狀態不依賴先前的值

**注意：** 如果您的專案啟用了 [React Compiler](https://react.dev/learn/react-compiler)，編譯器可以自動最佳化某些情況，但仍建議使用函式式更新以確保正確性並防止過時閉包錯誤。

### 5.6 使用延遲狀態初始化

**影響：中（每次渲染時浪費的計算）**

為昂貴的初始值傳遞函式給 `useState`。沒有函式形式，初始化器會在每次渲染時執行，即使該值只使用一次。

**錯誤：在每次渲染時執行**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 在每次渲染時執行，即使在初始化之後
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items));
  const [query, setQuery] = useState("");

  // 當 query 變更時，buildSearchIndex 再次不必要地執行
  return <SearchResults index={searchIndex} query={query} />;
}

function UserProfile() {
  // JSON.parse 在每次渲染時執行
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem("settings") || "{}"),
  );

  return <SettingsForm settings={settings} onChange={setSettings} />;
}
```

**正確：只執行一次**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 只在初始渲染時執行
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items));
  const [query, setQuery] = useState("");

  return <SearchResults index={searchIndex} query={query} />;
}

function UserProfile() {
  // JSON.parse 只在初始渲染時執行
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem("settings");
    return stored ? JSON.parse(stored) : {};
  });

  return <SettingsForm settings={settings} onChange={setSettings} />;
}
```

當從 localStorage/sessionStorage 計算初始值、建立資料結構（索引、maps）、從 DOM 讀取或執行繁重轉換時，使用延遲初始化。

對於簡單的原始值（`useState(0)`）、直接引用（`useState(props.value)`）或便宜的字面值（`useState({})`），函式形式是不必要的。

### 5.7 對非緊急更新使用 Transitions

**影響：中（保持 UI 回應性）**

將頻繁的非緊急狀態更新標記為 transitions 以保持 UI 回應性。

**錯誤：每次滾動時阻塞 UI**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);
}
```

**正確：非阻塞更新**

```tsx
import { startTransition } from "react";

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY));
    };
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);
}
```

---

## 6. 渲染效能

**影響：中**

最佳化渲染過程可減少瀏覽器需要執行的工作。

### 6.1 動畫 SVG 包裝器而不是 SVG 元素

**影響：低（啟用硬體加速）**

許多瀏覽器沒有針對 SVG 元素的 CSS3 動畫硬體加速。將 SVG 包裝在 `<div>` 中並對包裝器進行動畫處理。

**錯誤：直接對 SVG 進行動畫 - 沒有硬體加速**

```tsx
function LoadingSpinner() {
  return (
    <svg className="animate-spin" width="24" height="24" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  );
}
```

**正確：對包裝器 div 進行動畫 - 硬體加速**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  );
}
```

這適用於所有 CSS 轉換和過渡（`transform`、`opacity`、`translate`、`scale`、`rotate`）。包裝器 div 允許瀏覽器使用 GPU 加速以獲得更流暢的動畫。

### 6.2 對長列表使用 CSS content-visibility

**影響：高（更快的初始渲染）**

應用 `content-visibility: auto` 以延遲螢幕外渲染。

**CSS：**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**範例：**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map((msg) => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  );
}
```

對於 1000 則訊息，瀏覽器跳過約 990 個螢幕外項目的佈局/繪製（初始渲染快 10 倍）。

### 6.3 提升靜態 JSX 元素

**影響：低（避免重新建立）**

將靜態 JSX 提取到元件外部以避免重新建立。

**錯誤：每次渲染時重新建立元素**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />;
}

function Container() {
  return <div>{loading && <LoadingSkeleton />}</div>;
}
```

**正確：重用相同元素**

```tsx
const loadingSkeleton = <div className="animate-pulse h-20 bg-gray-200" />;

function Container() {
  return <div>{loading && loadingSkeleton}</div>;
}
```

這對於大型和靜態的 SVG 節點特別有用，它們在每次渲染時重新建立的成本可能很高。

**注意：** 如果您的專案啟用了 [React Compiler](https://react.dev/learn/react-compiler)，編譯器會自動提升靜態 JSX 元素並最佳化元件重新渲染，使手動提升變得不必要。

### 6.4 最佳化 SVG 精度

**影響：低（減少檔案大小）**

減少 SVG 座標精度以減小檔案大小。最佳精度取決於 viewBox 大小，但一般來說應該考慮降低精度。

**錯誤：過度的精度**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**正確：1 位小數**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**使用 SVGO 自動化：**

```bash
npx svgo --precision=1 --multipass icon.svg
```

### 6.5 防止 Hydration 不匹配且不閃爍

**影響：中（避免視覺閃爍和 hydration 錯誤）**

當渲染依賴客戶端儲存（localStorage、cookies）的內容時，透過注入同步腳本在 React hydrate 之前更新 DOM，以避免 SSR 中斷和 hydration 後閃爍。

**錯誤：破壞 SSR**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage 在伺服器上不可用 - 拋出錯誤
  const theme = localStorage.getItem("theme") || "light";

  return <div className={theme}>{children}</div>;
}
```

伺服器端渲染將失敗，因為 `localStorage` 未定義。

**錯誤：視覺閃爍**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    // 在 hydration 後執行 - 造成可見閃爍
    const stored = localStorage.getItem("theme");
    if (stored) {
      setTheme(stored);
    }
  }, []);

  return <div className={theme}>{children}</div>;
}
```

元件首先使用預設值（`light`）渲染，然後在 hydration 後更新，造成錯誤內容的可見閃爍。

**正確：無閃爍，無 hydration 不匹配**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">{children}</div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  );
}
```

內聯腳本在顯示元素之前同步執行，確保 DOM 已經具有正確的值。無閃爍，無 hydration 不匹配。

此模式特別適用於主題切換、使用者偏好設定、身份驗證狀態，以及任何應立即渲染而不閃爍預設值的僅客戶端資料。

### 6.6 使用 Activity 元件進行顯示/隱藏

**影響：中（保留狀態/DOM）**

使用 React 的 `<Activity>` 為頻繁切換可見性的昂貴元件保留狀態/DOM。

**用法：**

```tsx
import { Activity } from "react";

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? "visible" : "hidden"}>
      <ExpensiveMenu />
    </Activity>
  );
}
```

避免昂貴的重新渲染和狀態丟失。

### 6.7 使用明確的條件渲染

**影響：低（防止渲染 0 或 NaN）**

當條件可能是 `0`、`NaN` 或其他會渲染的假值時，使用明確的三元運算子（`? :`）而不是 `&&` 進行條件渲染。

**錯誤：當 count 為 0 時渲染 "0"**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count && <span className="badge">{count}</span>}</div>;
}

// 當 count = 0 時，渲染：<div>0</div>
// 當 count = 5 時，渲染：<div><span class="badge">5</span></div>
```

**正確：當 count 為 0 時不渲染任何內容**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count > 0 ? <span className="badge">{count}</span> : null}</div>;
}

// 當 count = 0 時，渲染：<div></div>
// 當 count = 5 時，渲染：<div><span class="badge">5</span></div>
```

---

## 7. JavaScript 效能

**影響：低中**

熱路徑的微最佳化可以累積成有意義的改進。

### 7.1 批次處理 DOM CSS 變更

**影響：中（減少重排/重繪）**

避免一次變更一個屬性的樣式。透過類別或 `cssText` 將多個 CSS 變更組合在一起，以最小化瀏覽器重排。

**錯誤：多次重排**

```typescript
function updateElementStyles(element: HTMLElement) {
  // 每行觸發一次重排
  element.style.width = "100px";
  element.style.height = "200px";
  element.style.backgroundColor = "blue";
  element.style.border = "1px solid black";
}
```

**正確：添加類別 - 單次重排**

```typescript
// CSS 檔案
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}

// JavaScript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
}
```

**正確：變更 cssText - 單次重排**

```typescript
function updateElementStyles(element: HTMLElement) {
  element.style.cssText = `
    width: 100px;
    height: 200px;
    background-color: blue;
    border: 1px solid black;
  `;
}
```

**React 範例：**

```tsx
// 錯誤：逐一變更樣式
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = "100px";
      ref.current.style.height = "200px";
      ref.current.style.backgroundColor = "blue";
    }
  }, [isHighlighted]);

  return <div ref={ref}>Content</div>;
}

// 正確：切換類別
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return <div className={isHighlighted ? "highlighted-box" : ""}>Content</div>;
}
```

盡可能優先使用 CSS 類別而不是內聯樣式。類別會被瀏覽器快取，並提供更好的關注點分離。

### 7.2 為重複查詢建立索引 Map

**影響：低中（從 1M 次操作減少到 2K 次操作）**

透過相同鍵進行的多個 `.find()` 呼叫應使用 Map。

**錯誤（每次查詢 O(n)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map((order) => ({
    ...order,
    user: users.find((u) => u.id === order.userId),
  }));
}
```

**正確（每次查詢 O(1)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map((u) => [u.id, u]));

  return orders.map((order) => ({
    ...order,
    user: userById.get(order.userId),
  }));
}
```

建立 map 一次（O(n)），然後所有查詢都是 O(1)。

對於 1000 個訂單 × 1000 個使用者：1M 次操作 → 2K 次操作。

### 7.3 在迴圈中快取屬性存取

**影響：低中（減少查詢）**

在熱路徑中快取物件屬性查詢。

**錯誤：3 次查詢 × N 次迭代**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value);
}
```

**正確：總共 1 次查詢**

```typescript
const value = obj.config.settings.value;
const len = arr.length;
for (let i = 0; i < len; i++) {
  process(value);
}
```

### 7.4 快取重複的函式呼叫

**影響：中（避免冗餘計算）**

當在渲染期間使用相同輸入重複呼叫相同函式時，使用模組層級的 Map 來快取函式結果。

**錯誤：冗餘計算**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() 對相同的專案名稱呼叫 100 多次
        const slug = slugify(project.name)

        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**正確：快取結果**

```typescript
// 模組層級快取
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // 每個唯一專案名稱只計算一次
        const slug = cachedSlugify(project.name)

        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**單值函式的更簡單模式：**

```typescript
let isLoggedInCache: boolean | null = null;

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache;
  }

  isLoggedInCache = document.cookie.includes("auth=");
  return isLoggedInCache;
}

// 當身份驗證變更時清除快取
function onAuthChange() {
  isLoggedInCache = null;
}
```

使用 Map（而不是 hook），這樣它可以在任何地方工作：工具程式、事件處理器，而不僅僅是 React 元件。

參考：[https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

### 7.5 快取 Storage API 呼叫

**影響：低中（減少昂貴的 I/O）**

`localStorage`、`sessionStorage` 和 `document.cookie` 是同步且昂貴的。在記憶體中快取讀取。

**錯誤：每次呼叫時讀取儲存**

```typescript
function getTheme() {
  return localStorage.getItem("theme") ?? "light";
}
// 呼叫 10 次 = 10 次儲存讀取
```

**正確：Map 快取**

```typescript
const storageCache = new Map<string, string | null>();

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value);
  storageCache.set(key, value); // 保持快取同步
}
```

使用 Map（而不是 hook），這樣它可以在任何地方工作：工具程式、事件處理器，而不僅僅是 React 元件。

**Cookie 快取：**

```typescript
let cookieCache: Record<string, string> | null = null;

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split("; ").map((c) => c.split("=")),
    );
  }
  return cookieCache[name];
}
```

**重要：在外部變更時使快取失效**

```typescript
window.addEventListener("storage", (e) => {
  if (e.key) storageCache.delete(e.key);
});

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    storageCache.clear();
  }
});
```

如果儲存可以在外部變更（另一個分頁、伺服器設定的 cookies），請使快取失效：

### 7.6 合併多個陣列迭代

**影響：低中（減少迭代）**

多個 `.filter()` 或 `.map()` 呼叫會多次迭代陣列。合併為一個迴圈。

**錯誤：3 次迭代**

```typescript
const admins = users.filter((u) => u.isAdmin);
const testers = users.filter((u) => u.isTester);
const inactive = users.filter((u) => !u.isActive);
```

**正確：1 次迭代**

```typescript
const admins: User[] = [];
const testers: User[] = [];
const inactive: User[] = [];

for (const user of users) {
  if (user.isAdmin) admins.push(user);
  if (user.isTester) testers.push(user);
  if (!user.isActive) inactive.push(user);
}
```

### 7.7 在陣列比較前提前檢查長度

**影響：中高（當長度不同時避免昂貴的操作）**

當使用昂貴的操作（排序、深度相等、序列化）比較陣列時，首先檢查長度。如果長度不同，陣列不可能相等。

在實際應用中，當比較在熱路徑（事件處理器、渲染迴圈）中執行時，此最佳化特別有價值。

**錯誤：總是執行昂貴的比較**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 總是排序和連接，即使長度不同
  return current.sort().join() !== original.sort().join();
}
```

即使 `current.length` 是 5 而 `original.length` 是 100，也會執行兩次 O(n log n) 排序。還有連接陣列和比較字串的開銷。

**正確（首先進行 O(1) 長度檢查）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 如果長度不同，提前返回
  if (current.length !== original.length) {
    return true;
  }
  // 只在長度匹配時排序/連接
  const currentSorted = current.toSorted();
  const originalSorted = original.toSorted();
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true;
    }
  }
  return false;
}
```

這個新方法更有效率，因為：

- 當長度不同時避免排序和連接陣列的開銷

- 避免為連接的字串消耗記憶體（對於大型陣列特別重要）

- 避免變更原始陣列

- 找到差異時提前返回

### 7.8 從函式提前返回

**影響：低中（避免不必要的計算）**

當結果確定時提前返回以跳過不必要的處理。

**錯誤：即使找到答案後仍處理所有項目**

```typescript
function validateUsers(users: User[]) {
  let hasError = false;
  let errorMessage = "";

  for (const user of users) {
    if (!user.email) {
      hasError = true;
      errorMessage = "Email required";
    }
    if (!user.name) {
      hasError = true;
      errorMessage = "Name required";
    }
    // 即使找到錯誤後仍繼續檢查所有使用者
  }

  return hasError ? { valid: false, error: errorMessage } : { valid: true };
}
```

**正確：在第一個錯誤時立即返回**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: "Email required" };
    }
    if (!user.name) {
      return { valid: false, error: "Name required" };
    }
  }

  return { valid: true };
}
```

### 7.9 提升 RegExp 建立

**影響：低中（避免重新建立）**

不要在渲染內部建立 RegExp。提升到模組範圍或使用 `useMemo()` 記憶化。

**錯誤：每次渲染時都建立新的 RegExp**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**正確：記憶化或提升**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**警告：全域 regex 具有可變狀態**

```typescript
const regex = /foo/g;
regex.test("foo"); // true, lastIndex = 3
regex.test("foo"); // false, lastIndex = 0
```

全域 regex（`/g`）具有可變的 `lastIndex` 狀態：

### 7.10 使用迴圈而非排序來查找最小/最大值

**影響：低（O(n) 而不是 O(n log n)）**

找到最小或最大元素只需要單次遍歷陣列。排序是浪費且較慢的。

**錯誤（O(n log n) - 排序以查找最新）：**

```typescript
interface Project {
  id: string;
  name: string;
  updatedAt: number;
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt);
  return sorted[0];
}
```

只是為了找到最大值而排序整個陣列。

**錯誤（O(n log n) - 排序以查找最舊和最新）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt);
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] };
}
```

當只需要最小值/最大值時仍然不必要地排序。

**正確（O(n) - 單次迴圈）：**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null;

  let latest = projects[0];

  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i];
    }
  }

  return latest;
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null };

  let oldest = projects[0];
  let newest = projects[0];

  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i];
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i];
  }

  return { oldest, newest };
}
```

單次遍歷陣列，無複製，無排序。

**替代方案：對小型陣列使用 Math.min/Math.max**

```typescript
const numbers = [5, 2, 8, 1, 9];
const min = Math.min(...numbers);
const max = Math.max(...numbers);
```

這對小型陣列有效，但由於展開運算子的限制，對於非常大的陣列可能較慢。為了可靠性，使用迴圈方法。

### 7.11 使用 Set/Map 進行 O(1) 查詢

**影響：低中（從 O(n) 到 O(1)）**

將陣列轉換為 Set/Map 以進行重複的成員檢查。

**錯誤（每次檢查 O(n)）：**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**正確（每次檢查 O(1)）：**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```

### 7.12 使用 toSorted() 而非 sort() 以保持不可變性

**影響：中高（防止 React 狀態中的變更錯誤）**

`.sort()` 會就地變更陣列，這可能導致 React 狀態和 props 的錯誤。使用 `.toSorted()` 來建立新的排序陣列而不變更。

**錯誤：變更原始陣列**

```typescript
function UserList({ users }: { users: User[] }) {
  // 變更 users prop 陣列！
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正確：建立新陣列**

```typescript
function UserList({ users }: { users: User[] }) {
  // 建立新的排序陣列，原始未變更
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**為什麼這在 React 中很重要：**

1. Props/狀態變更破壞 React 的不可變性模型 - React 期望 props 和狀態被視為唯讀

2. 導致過時閉包錯誤 - 在閉包（回呼、effects）內部變更陣列可能導致意外行為

**瀏覽器支援：較舊瀏覽器的回退**

```typescript
// 較舊瀏覽器的回退
const sorted = [...items].sort((a, b) => a.value - b.value);
```

`.toSorted()` 在所有現代瀏覽器中可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。對於較舊的環境，使用展開運算子：

**其他不可變陣列方法：**

- `.toSorted()` - 不可變排序

- `.toReversed()` - 不可變反轉

- `.toSpliced()` - 不可變拼接

- `.with()` - 不可變元素替換

---

## 8. 進階模式

**影響：低**

需要仔細實作的特定情況的進階模式。

### 8.1 在 Refs 中儲存事件處理器

**影響：低（穩定的訂閱）**

當在不應在回呼變更時重新訂閱的 effects 中使用回呼時，將回呼儲存在 refs 中。

**錯誤：每次渲染時重新訂閱**

```tsx
function useWindowEvent(event: string, handler: () => void) {
  useEffect(() => {
    window.addEventListener(event, handler);
    return () => window.removeEventListener(event, handler);
  }, [event, handler]);
}
```

**正確：穩定的訂閱**

```tsx
import { useEffectEvent } from "react";

function useWindowEvent(event: string, handler: () => void) {
  const onEvent = useEffectEvent(handler);

  useEffect(() => {
    window.addEventListener(event, onEvent);
    return () => window.removeEventListener(event, onEvent);
  }, [event]);
}
```

**替代方案：如果您使用最新的 React，請使用 `useEffectEvent`：**

`useEffectEvent` 為相同模式提供更清晰的 API：它建立一個穩定的函式引用，總是呼叫最新版本的處理器。

### 8.2 使用 useLatest 建立穩定的回呼 Refs

**影響：低（防止 effect 重新執行）**

在回呼中存取最新值而不將它們添加到依賴項陣列中。防止 effect 重新執行，同時避免過時閉包。

**實作：**

```typescript
function useLatest<T>(value: T) {
  const ref = useRef(value);
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref;
}
```

**錯誤：effect 在每次回呼變更時重新執行**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300);
    return () => clearTimeout(timeout);
  }, [query, onSearch]);
}
```

**正確：穩定的 effect，新鮮的回呼**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");
  const onSearchRef = useLatest(onSearch);

  useEffect(() => {
    const timeout = setTimeout(() => onSearchRef.current(query), 300);
    return () => clearTimeout(timeout);
  }, [query]);
}
```

---

## 參考資料

1. [https://react.dev](https://react.dev)
2. [https://nextjs.org](https://nextjs.org)
3. [https://swr.vercel.app](https://swr.vercel.app)
4. [https://github.com/shuding/better-all](https://github.com/shuding/better-all)
5. [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)
6. [https://vercel.com/blog/how-we-optimized-package-imports-in-next-js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
7. [https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
