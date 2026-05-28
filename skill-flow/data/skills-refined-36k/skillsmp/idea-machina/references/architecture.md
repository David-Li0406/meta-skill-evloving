# IdeaMachina Architecture

## Component Hierarchy

```
App.tsx (Router)
├── /ideas → IdeasPage
│   ├── AppHeader (navigation)
│   ├── IdeaFilters (search, status, tags, AI pickup)
│   ├── IdeaCard[] (list display)
│   │   ├── TagChips
│   │   ├── RatingStars
│   │   └── AIPickupToggle
│   ├── Dialog: IdeaForm (create/edit)
│   ├── Dialog: Delete confirmation
│   └── ContinueDialog
│       ├── Action selector (project/goal/workflow/prompt)
│       └── Action-specific forms
│
└── /ideas/:id → IdeaDetailPage
    ├── AppHeader
    ├── Status badge + AI pickup badge
    ├── Description section
    ├── AI guidance section
    ├── TagChips (read-only)
    ├── RatingStars (interactive)
    ├── Metadata (created/updated)
    ├── "Continue to..." button
    ├── Dialog: IdeaForm (edit)
    ├── Dialog: Delete confirmation
    └── ContinueDialog
```

## Data Flow

```
User Action → React Query Mutation → Supabase Client → Database
                    ↓
              Invalidate queries
                    ↓
              React Query refetch → UI Update
```

### Query Keys

| Key | Data |
|-----|------|
| `["ideas", filters]` | Filtered ideas list |
| `["idea", id]` | Single idea with details |
| `["idea-tags"]` | All available tags |
| `["pm-projects"]` | Projects for "Continue to..." |

## State Management

### Local State (useState)

- Dialog open/close states
- Filter values (search, status, tags, AI pickup)
- Form input values in dialogs

### Server State (React Query)

- Ideas list and single idea
- Tags and projects
- Mutations for CRUD operations

## File Responsibilities

| File | Responsibility |
|------|----------------|
| `lib/ideas.ts` | All Supabase operations |
| `types/ideas.ts` | TypeScript interfaces |
| `IdeasPage.tsx` | List view, filters, dialogs |
| `IdeaDetailPage.tsx` | Detail view, edit, delete |
| `IdeaCard.tsx` | Card display, quick actions |
| `IdeaForm.tsx` | Create/edit form fields |
| `IdeaFilters.tsx` | Search and filter controls |
| `ContinueDialog.tsx` | "Continue to..." wizard |
| `TagSelector.tsx` | Tag multi-select + chips |
| `RatingStars.tsx` | Star rating input |
| `AIPickupToggle.tsx` | AI pickup toggle + priority |

## UI Components from packages/ui

- Button, Badge
- Dialog, DialogContent, DialogHeader, DialogTitle
- Input, Textarea, Label
- Select, SelectItem (custom styled)
- Slider (for priority)

## Integration Points

### Supabase Client

Located at `src/integrations/supabase/client.ts` - shared across app.

### Navigation

AppHeader contains nav links:
- Prompts (Index.tsx)
- Ideas (IdeasPage.tsx)

### "Continue to..." Targets

| Target | Table | Notes |
|--------|-------|-------|
| Project | `pm_projects` | Sets idea status='converted' |
| Goal | `pm_goals` | Requires project_id |
| Workflow | `workflows` | Optional project_id |
| Prompt | `prompts` + `prompt_versions` | Creates both records |
