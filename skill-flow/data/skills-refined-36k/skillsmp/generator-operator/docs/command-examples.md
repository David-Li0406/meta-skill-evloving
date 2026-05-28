# コマンド例集

npm run generateの実行コマンド例。

## UI層

### Route

```bash
npm run generate -- \
  --category ui \
  --ui-type route \
  --service blog \
  --section posts \
  --name index
```

**生成**: `app/routes/blog.posts.index.tsx`

### Component

```bash
npm run generate -- \
  --category ui \
  --ui-type component \
  --service blog \
  --section posts \
  --name ProgressSummary
```

**生成**: `app/components/blog/posts/ProgressSummary.tsx`

## lib層

```bash
npm run generate -- \
  --category lib \
  --service blog \
  --section posts \
  --name progressCalculator
```

**生成**: `app/lib/blog/posts/progressCalculator.ts`

## data-io層

```bash
npm run generate -- \
  --category data-io \
  --service blog \
  --section posts \
  --name postLoader
```

**生成**: `app/data-io/blog/posts/postLoader.server.ts`

## documents層

### Spec

```bash
npm run generate -- \
  --category documents \
  --document-type spec \
  --service blog \
  --section posts \
  --name posts-spec
```

**生成**: `app/specs/blog/posts-spec.yaml`

### Requirements

```bash
npm run generate -- \
  --category documents \
  --document-type requirements \
  --service blog \
  --section posts \
  --name requirements
```

**生成**: `develop/blog/posts/requirements.md`
