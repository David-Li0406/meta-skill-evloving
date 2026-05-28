# [FEATURE_NAME] Feature Specification

## 1. Overview

### Objective
[What this feature accomplishes]

### Summary
[Brief description of the feature]

### Tech Stack
- **Frontend**: Next.js 16, TypeScript, TailwindCSS, Shadcn UI
- **Backend**: Go, Fiber, Clean Architecture
- **Database**: Supabase (PostgreSQL)

---

## 2. Context and Motivation

### Why this feature?
[Business justification]

### User stories
- As a [user type], I want to [action] so that [benefit]

### Success criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## 3. Functional Specifications

### Core behavior
[Detailed description of how the feature works]

### Business rules
1. [Rule 1]
2. [Rule 2]

### Edge cases
| Case | Expected behavior |
|------|-------------------|
| [Case 1] | [Behavior] |
| [Case 2] | [Behavior] |

### Error handling
| Error | Message | Action |
|-------|---------|--------|
| [Error 1] | "[Message]" | [Action] |

---

## 4. Technical Architecture

### Existing files to modify
| File | Changes |
|------|---------|
| `path/to/file.go` | [Description] |

### New files to create
| File | Purpose |
|------|---------|
| `path/to/new/file.go` | [Purpose] |

---

## 5. Configuration

### app.yaml additions
```yaml
# New configuration for [feature]
feature_name:
  enabled: true
  max_items: 100
  threshold: 0.8
  # Add all thresholds, limits, feature flags here
```

### Environment variables (.env)
```bash
# Only for secrets - API keys, credentials
# FEATURE_API_KEY=xxx
```

**Rule:** NO hardcoded values in code. All parameters must come from config.

---

## 6. Database

### Migrations

```sql
-- Migration: [name]
-- Description: [what it does]

CREATE TABLE IF NOT EXISTS [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- columns
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS policies
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

CREATE POLICY "[policy_name]" ON [table_name]
  FOR SELECT
  USING (auth.uid() = user_id);
```

---

## 7. Backend Implementation

### Phase 1: Domain
- [ ] Entity: `internal/domain/entities/[entity].go`
- [ ] Repository interface: `internal/domain/repositories/[repo].go`

### Phase 2: Infrastructure
- [ ] Repository impl: `internal/infrastructure/repositories/[repo]_repository.go`

### Phase 3: Application
- [ ] UseCase: `internal/application/usecases/[feature]/[usecase].go`
- [ ] DTO: `internal/application/dtos/[feature]_dto.go`

### Phase 4: Presentation
- [ ] Handler: `internal/presentation/handlers/[feature]_handler.go`
- [ ] Routes: Update `internal/presentation/routes/routes.go`

---

## 8. Frontend Implementation

### Phase 5: Types & API
- [ ] Types: `src/types/[feature].ts`
- [ ] API: `src/lib/api/[feature].ts`

### Phase 6: Hooks
- [ ] Query hook: `src/hooks/use-[feature].ts`
- [ ] Mutation hooks

### Phase 7: Components
- [ ] Component: `src/components/[feature]/[Component].tsx`

### Phase 8: Pages
- [ ] Page: `src/app/[locale]/(protected)/[route]/page.tsx`

---

## 9. Execution Plan

### Backend
- [ ] Phase 1: Domain layer
- [ ] Phase 2: Infrastructure layer
- [ ] Phase 3: Application layer
- [ ] Phase 4: Presentation layer

### Frontend
- [ ] Phase 5: Types & API
- [ ] Phase 6: Hooks
- [ ] Phase 7: Components
- [ ] Phase 8: Pages

### Verification
- [ ] Backend builds: `go build ./...`
- [ ] Frontend builds: `npm run build`
- [ ] Database advisors: `mcp__supabase-dev__get_advisors`

---

## 10. Important Notes

### Compatibility
- [Any compatibility concerns]

### Performance
- [Performance considerations]

### Security
- [Security considerations]

---

## Usage

```bash
# Execute phase by phase
/dev spec=docs/plan-features/[NAME]_FEATURE.md phase=1
/dev spec=docs/plan-features/[NAME]_FEATURE.md phase=2
# ... etc
```
