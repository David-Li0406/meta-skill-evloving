# Documentation Quality Checklist

## TL;DR Quality

- [ ] **Starts with TL;DR block** at top of document
- [ ] **One sentence summary** (not a paragraph)
- [ ] **3-5 key points** with specific values/numbers
- [ ] **Quick links** to main sections
- [ ] **No jargon** in summary (understandable to new reader)

## Content Quality

### Structure
- [ ] Clear heading hierarchy (H1 > H2 > H3)
- [ ] Tables for structured data
- [ ] Code blocks with language tags
- [ ] Consistent formatting throughout

### Accuracy
- [ ] All table names match database
- [ ] All RPC signatures match code
- [ ] All Edge Function endpoints tested
- [ ] Version numbers current

### Completeness
- [ ] Request/response examples for APIs
- [ ] Error codes documented
- [ ] TypeScript usage examples
- [ ] Admin operations explained

## Cross-Reference Check

For each change, verify these docs are in sync:

| Change Type | Primary Doc | Also Update |
|-------------|-------------|-------------|
| New table | `03-API.md` | `02-DESIGN.md`, `CLAUDE.MD` |
| New RPC | `03-API.md` | `05-DEV.md` |
| New Edge Fn | `03-API.md` | `02-DESIGN.md`, `06-AI-ARCHITECTURE.md` |
| Admin feature | `07-ADMIN-GUIDE.md` | `CLAUDE.MD` |
| User feature | `README.md` | `01-PRD.md` (if significant) |
| AI change | `06-AI-ARCHITECTURE.md` | `CLAUDE.MD` |

## Staleness Detection

### Signs of Outdated Docs

- Migration date newer than doc modified date
- Table in DB not in docs
- RPC in code not in docs
- Edge Function deployed but undocumented
- UI screenshot doesn't match current UI

### Automated Checks

```bash
# Check for undocumented tables
supabase db dump --schema public | grep "CREATE TABLE" | \
  while read line; do
    table=$(echo "$line" | grep -oP '(?<=TABLE )\w+')
    grep -q "$table" Docs/03-API.md || echo "Missing: $table"
  done

# Check for undocumented Edge Functions
ls supabase/functions/ | while read fn; do
  grep -q "$fn" Docs/02-DESIGN.md || echo "Missing: $fn"
done
```

## Pre-Commit Checklist

Before committing doc changes:

- [ ] Spell check passed
- [ ] Links work (no broken anchors)
- [ ] Code blocks render correctly
- [ ] Tables aligned properly
- [ ] No placeholder text remaining
- [ ] Date/version updated if applicable

## Release Checklist

Before release:

- [ ] All new features documented
- [ ] CHANGELOG.md updated
- [ ] README.md reflects current state
- [ ] API docs match deployed code
- [ ] Admin guide covers new UI
- [ ] No TODO/FIXME in docs
