# IdeaMachina Database Schema

All tables in `ai_prompt` schema.

## Tables

### pm_ideas

Main ideas table.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK, auto-generated |
| title | text | Required |
| description | text | Optional |
| ai_guidance_prompt | text | Instructions for AI |
| is_ai_pickup | boolean | Default false |
| ai_pickup_priority | integer | 1-100, default 50 |
| status | text | new/nurturing/ready/converted/archived |
| priority | integer | 1-100, default 50 |
| avg_rating | numeric | Computed average |
| rating_count | integer | Number of ratings |
| created_by | uuid | FK to auth.users |
| created_at | timestamptz | Auto |
| updated_at | timestamptz | Auto, trigger |
| deleted_at | timestamptz | Soft delete |

**Indexes:**
- `status` WHERE `deleted_at IS NULL`
- `is_ai_pickup, ai_pickup_priority` WHERE `is_ai_pickup = true AND deleted_at IS NULL`
- `created_by`

### pm_idea_tags

Tag definitions.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| slug | text | Unique, URL-safe |
| label | text | Display name (called `name` in UI) |
| description | text | Optional |
| color | text | Hex color, default #6366f1 |
| created_at | timestamptz | Auto |

**Seeded tags:**
- ready-for-ai (#22c55e)
- needs-research (#eab308)
- quick-win (#3b82f6)
- blocked (#ef4444)

### pm_idea_tag_links

Many-to-many: ideas ↔ tags.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| idea_id | uuid | FK to pm_ideas, CASCADE |
| tag_id | uuid | FK to pm_idea_tags, CASCADE |
| created_at | timestamptz | Auto |

**Constraint:** UNIQUE(idea_id, tag_id)

### pm_idea_ratings

Per-user ratings.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| idea_id | uuid | FK to pm_ideas, CASCADE |
| user_id | uuid | Default auth.uid() |
| rating | integer | 1-5 |
| note | text | Optional |
| created_at | timestamptz | Auto |
| updated_at | timestamptz | Auto, trigger |

**Constraint:** UNIQUE(idea_id, user_id)

## Related Tables

### pm_projects

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| slug | text | Unique |
| name | text | Required |
| repo_path | text | Optional |
| idea_id | uuid | FK to pm_ideas, SET NULL |
| created_by | uuid | FK to auth.users |

### pm_goals

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| project_id | uuid | FK to pm_projects |
| title | text | Required |
| success_criteria | text | Optional |
| status | text | draft/active/completed/archived |
| idea_id | uuid | FK to pm_ideas, SET NULL |

### workflows

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| name | text | Required |
| description | text | Optional |
| scope | text | global/user/team |
| owner_user_id | uuid | FK to auth.users |
| project_id | uuid | FK to pm_projects, SET NULL |

### prompts + prompt_versions

For "Continue to Prompt" action:

**prompts:**
- name, description, scope, owner_user_id
- prompt_type (enum: code, research, etc.)
- tags (text array)

**prompt_versions:**
- prompt_id (FK)
- version_number
- content
- format (plain/markdown/xml/json)

## RLS Policies

### pm_ideas

| Operation | Policy |
|-----------|--------|
| SELECT | Authenticated, deleted_at IS NULL |
| INSERT | Authenticated, created_by = auth.uid() |
| UPDATE | Owner only (created_by = auth.uid()) |
| DELETE | Owner only |

### pm_idea_tags

| Operation | Policy |
|-----------|--------|
| SELECT | Authenticated (all can read) |
| INSERT/UPDATE/DELETE | Service role only |

### pm_idea_tag_links

| Operation | Policy |
|-----------|--------|
| SELECT | Authenticated |
| INSERT | Owner of linked idea |
| DELETE | Owner of linked idea |

### pm_idea_ratings

| Operation | Policy |
|-----------|--------|
| SELECT | Authenticated |
| INSERT | user_id = auth.uid() |
| UPDATE | user_id = auth.uid() |

## Type Gotcha

**DB column:** `pm_idea_tags.label`
**UI property:** `IdeaTag.name`

Transform with:
```typescript
function transformTag(dbTag: PmIdeaTag): IdeaTag {
  return { ...dbTag, name: dbTag.label };
}
```
