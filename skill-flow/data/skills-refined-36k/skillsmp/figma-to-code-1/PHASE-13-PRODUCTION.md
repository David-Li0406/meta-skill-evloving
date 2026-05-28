# Phase 13: Production Audit

## Step 1: Migrate Figma Images to CDN

**CRITICAL:** Before production deployment, all Figma MCP URLs must be migrated to permanent CDN storage.

Figma MCP URLs (`https://www.figma.com/api/mcp/asset/...`) are temporary and will eventually expire.

### Run Image Migration

1. **Get CMS auth token** via login mutation
2. **Run migration script** from Phase 4:
   ```bash
   CMS_AUTH_TOKEN='your-token' npx tsx scripts/migrate-figma-images.ts
   ```
3. **Verify** all images now use `pub-*.r2.dev` or your CDN domain
4. **Test** the site to ensure images load correctly

See [PHASE-4-ASSETS.md](PHASE-4-ASSETS.md) for the full migration script.

## Step 2: Build Verification

```bash
npm run build
npm run lint
npx tsc --noEmit
```

All must pass without errors.

## Step 3: Verification Checklist

### Images
- [ ] **Image migration complete** - no Figma MCP URLs remain
- [ ] All images use `next/image`
- [ ] All images reference CDN URLs (pub-*.r2.dev or your domain)
- [ ] No local image paths in components

### Content
- [ ] All content from CMS
- [ ] No hardcoded strings (re-verify)
- [ ] CMS errors handled gracefully

### Data Attributes
- [ ] All editable elements have `data-cms-*` attributes
- [ ] Field paths are correct
- [ ] CMS data structure is flat (no `data.data` nesting)

### Accessibility
- [ ] All images have alt text (from CMS)
- [ ] Semantic HTML used
- [ ] Focus states work
- [ ] Color contrast acceptable

### Performance
- [ ] No render blocking
- [ ] Images optimized
- [ ] Fonts preloaded

## Step 3: Error Handling

Verify graceful degradation:
- [ ] CMS unavailable → error boundary works
- [ ] Missing content → fallbacks render
- [ ] Image load failure → handled

## Step 4: Environment Variables

Update README with required variables:

```markdown
## Environment Variables

Required in production:
- `NEXT_PUBLIC_CMS_GRAPHQL_URL` - CMS GraphQL endpoint
- `CMS_ORGANIZATION_ID` - Organization ID
- `CDN_BUCKET_URL` - CDN base URL
```

## Step 5: Security Check

- [ ] No credentials in code
- [ ] `.env.local` in `.gitignore`
- [ ] No API keys exposed

## Git Commit

```bash
git commit -m "chore: production audit complete"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 13: Production audit complete" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-14-DEPLOY.md](PHASE-14-DEPLOY.md) (if deployment enabled)
