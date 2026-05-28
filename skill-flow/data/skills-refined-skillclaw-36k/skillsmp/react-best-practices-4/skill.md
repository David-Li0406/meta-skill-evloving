---
name: react-best-practices
description: Vercel React/Next.jsパフォーマンス最適化 - 45ルール8カテゴリ、ウォーターフォール排除からバンドル最適化まで
requires-guidelines:
  - nextjs-react
---

# React Best Practices (Vercel Engineering)

> **Version**: 0.1.0 | **Source**: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

## 使用タイミング

- **React/Next.jsコンポーネント実装時**
- **パフォーマンス最適化・レビュー時**
- **バンドルサイズ削減時**
- **データフェッチ設計時**

## ルールカテゴリ（優先度順）

| 優先度 | カテゴリ | 影響度 | プレフィックス |
|--------|----------|--------|----------------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## クイックリファレンス

### 1. Eliminating Waterfalls（CRITICAL）

- `async-defer-await` - awaitを必要なブランチに移動
- `async-parallel` - 独立操作にPromise.all()
- `async-dependencies` - 部分依存にbetter-all
- `async-api-routes` - APIルートで早期Promise開始
- `async-suspense-boundaries` - Suspenseでストリーミング

### 2. Bundle Size Optimization（CRITICAL）

- `bundle-barrel-imports` - barrel fileを避け直接import
- `bundle-dynamic-imports` - 重いコンポーネントにnext/dynamic
- `bundle-defer-third-party` - hydration後にanalytics読み込み
- `bundle-conditional` - 機能有効化時のみモジュール読み込み
- `bundle-preload` - hover/focusでpreload

### 3. Server-Side Performance（HIGH）

- `server-cache-react` - リクエスト単位でReact.cache()
- `server-cache-lru` - リクエスト横断でLRUキャッシュ
- `server-serialization` - Client Componentへの最小限データ
- `server-parallel-fetching` - コンポーネント構成でフェッチ並列化
- `server-after-nonblocking` - after()で非ブロッキング処理

### 4. Client-Side Data Fetching（MEDIUM-HIGH）

- `client-swr-dedup` - SWRで自動重複排除
- `client-event-listeners` - グローバルイベントリスナー重複排除

### 5. Re-render Optimization（MEDIUM）

- `rerender-defer-reads` - コールバックのみで使う状態を購読しない
- `rerender-memo` - 高コスト処理をmemo化コンポーネントに抽出
- `rerender-dependencies` - effect依存はプリミティブに
- `rerender-derived-state` - 生値でなく派生booleanを購読
- `rerender-functional-setstate` - 関数式setStateで安定callback
- `rerender-lazy-state-init` - 高コスト初期値は関数でuseState
- `rerender-transitions` - startTransitionで非緊急更新

### 6. Rendering Performance（MEDIUM）

- `rendering-animate-svg-wrapper` - SVG要素でなくdivラッパーをアニメーション
- `rendering-content-visibility` - 長いリストにcontent-visibility
- `rendering-hoist-jsx` - 静的JSXをコンポーネント外に抽出
- `rendering-svg-precision` - SVG座標精度を削減
- `rendering-hydration-no-flicker` - インラインスクリプトでちらつき防止
- `rendering-activity` - show/hideにActivityコンポーネント
- `rendering-conditional-render` - &&でなく三項演算子で条件レンダリング

### 7. JavaScript Performance（LOW-MEDIUM）

- `js-batch-dom-css` - CSSをclassまたはcssTextでまとめて変更
- `js-index-maps` - 繰り返し検索にMap構築
- `js-cache-property-access` - ループ内でプロパティアクセスをキャッシュ
- `js-cache-function-results` - 関数結果をモジュールレベルMapでキャッシュ
- `js-cache-storage` - localStorage/sessionStorage読み取りをキャッシュ
- `js-combine-iterations` - 複数filter/mapを1ループに統合
- `js-length-check-first` - 高コスト比較前に配列長チェック
- `js-early-exit` - 関数から早期return
- `js-hoist-regexp` - RegExp生成をループ外に巻き上げ
- `js-min-max-loop` - min/maxにsortでなくループ使用
- `js-set-map-lookups` - O(1)検索にSet/Map使用
- `js-tosorted-immutable` - イミュータビリティにtoSorted()

### 8. Advanced Patterns（LOW）

- `advanced-event-handler-refs` - イベントハンドラをrefに格納
- `advanced-use-latest` - 安定callbackにuseLatest

## 代表的なルール詳細

### async-defer-await（CRITICAL）

awaitを必要なブランチにのみ配置。不要なパスをブロックしない。

```typescript
// ❌ 両ブランチをブロック
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)

  if (skipProcessing) {
    return { skipped: true }  // userDataは不要だったが待った
  }

  return processUserData(userData)
}

// ✅ 必要な時だけ待機
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    return { skipped: true }  // 即座に返す
  }

  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

### bundle-barrel-imports（CRITICAL）

barrel file（index.ts）からのimportを避け、直接ファイルを指定。

```typescript
// ❌ barrel経由：未使用コードもバンドルに含まれる
import { Button } from '@/components'

// ✅ 直接import：必要なコードのみ
import { Button } from '@/components/Button'
```

### rerender-memo（MEDIUM）

高コストな子コンポーネントをmemo化。親の再レンダリングから分離。

```tsx
// ❌ 親が再レンダリングするたびにExpensiveChartも再描画
function Dashboard() {
  const [filter, setFilter] = useState('all')
  return (
    <div>
      <FilterDropdown value={filter} onChange={setFilter} />
      <ExpensiveChart data={staticData} />
    </div>
  )
}

// ✅ memo化で不要な再描画を防止
const MemoizedChart = memo(ExpensiveChart)

function Dashboard() {
  const [filter, setFilter] = useState('all')
  return (
    <div>
      <FilterDropdown value={filter} onChange={setFilter} />
      <MemoizedChart data={staticData} />
    </div>
  )
}
```

## 完全なルール一覧

全45ルールの詳細は `agents.md` を参照。

## 出力形式

🔴 **CRITICAL**: `ファイル:行` - ルールID - 問題と修正案
🟠 **HIGH**: `ファイル:行` - ルールID - 問題と修正案
🟡 **MEDIUM**: `ファイル:行` - ルールID - 問題と修正案
📊 **Summary**: Critical X件 / High Y件 / Medium Z件

## 関連ガイドライン

- `~/.claude/guidelines/languages/nextjs-react.md`
