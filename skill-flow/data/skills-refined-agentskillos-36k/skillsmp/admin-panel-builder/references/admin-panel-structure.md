# Admin Panel Structure Reference

Complete mapping of admin pages, their tabs, sections, and manager components.

## Pages Overview

| Page | Route | File | Tabs | Description |
|------|-------|------|------|-------------|
| Dashboard | `/admin` | `AdminDashboardPage.tsx` | - | Overview cards, stats, alerts |
| AI | `/admin/ai` | `AdminAIPage.tsx` | 6 | AI features, prompts, usage, pricing |
| Audio | `/admin/audio` | `AdminAudioPage.tsx` | 2 | TTS generation, voice config |
| Auth Tokens | `/admin/auth-tokens` | `AdminAuthTokensPage.tsx` | - | API keys, collapsible sections |
| Cinema | `/admin/cinema` | `AdminCinemaPage.tsx` | 2 | Background visuals, music |
| Reading Plans | `/admin/reading-plans` | `AdminReadingPlansPage.tsx` | - | Bible reading plans |
| Subscriptions | `/admin/subscriptions` | `AdminSubscriptionsPage.tsx` | - | Plans, limits |
| Testing | `/admin/testing` | `AdminTestingPage.tsx` | - | Component demos |
| Topics | `/admin/topics` | `AdminTopicsPage.tsx` | - | Suggestions, QA, translations |
| Translations | `/admin/translations` | `AdminTranslationsPage.tsx` | - | FI-EN term cache |
| Users | `/admin/users` | `AdminUsersPage.tsx` | 3 | Users, history, emails |
| Video | `/admin/video` | `AdminVideoPage.tsx` | - | Series, clips |
| Widget Analytics | `/admin/widget-analytics` | `AdminWidgetAnalyticsPage.tsx` | - | Embed usage stats |

---

## Detailed Page Structures

### AdminDashboardPage (`/admin`)

**Layout**: No sidebar initially (uses `SidebarProvider defaultOpen={false}`)

**Sections**:
- Token deadline alerts (critical/warning)
- Overview stats widget (users, summaries, highlights, searches, widget, topics)
- Grid of admin cards linking to all pages

**Stats shown**:
- User count
- Summaries count
- Highlights count
- Search count
- Widget requests today
- Pending topic suggestions

---

### AdminAIPage (`/admin/ai`)

**Tabs** (6):
| Tab | Value | Icon | Component |
|-----|-------|------|-----------|
| Käyttö (Usage) | `usage` | BarChart3 | Inline stats, tables |
| Palautteet (Feedback) | `feedback` | MessageSquare | `FeedbackAdminList`, `AISummaryFeedbackManager` |
| Ominaisuudet (Features) | `features` | Settings | `AIFeaturesManager` |
| Promptit (Prompts) | `prompts` | FileText | `AIPromptsManager` |
| Hinnoittelu (Pricing) | `pricing` | Coins | `AIPricingManager` |
| Testaus (Test) | `test` | FlaskConical | `AITestTool` |

**Usage tab contents**:
- Time filter toggle (all/today/week/month)
- Stats cards: requests, cost, tokens, avg cost
- Model stats table
- Usage logs table

---

### AdminAudioPage (`/admin/audio`)

**Tabs** (2):
| Tab | Value | Icon | Component |
|-----|-------|------|-----------|
| Generointi | `generation` | Play | Inline generation UI |
| Äänikonfiguraatio | `config` | Settings | `AudioVoicesManager`, `VersionAudioConfigManager` |

**Generation tab contents**:
- ElevenLabs credits card
- Summary stats (audio count, cues, books)
- Generation form (version, book, chapter, voice)
- Book coverage grid with progress
- Audio assets by book (collapsible)
- Audio cues detail

---

### AdminAuthTokensPage (`/admin/auth-tokens`)

**Layout**: Collapsible sections (all start closed)

**Sections** (using `TokenCategorySection`):
1. Authentication Tokens
2. OAuth Provider Tokens
3. Integration & API Tokens
4. CI/CD Secrets (GitHub Actions)

Each section shows token cards with:
- Name, status badges
- Environment variable
- Location, deadline, notes
- Used in tags
- Admin/dashboard links
- Regenerate info

**Bottom section**: "When to Regenerate" guidance card

---

### AdminCinemaPage (`/admin/cinema`)

**Tabs** (2):
| Tab | Value | Icon | Component |
|-----|-------|------|-----------|
| Taustakuvat | `visuals` | Image | `CinemaVisualsManager` |
| Taustamusiikit | `tracks` | Music | `CinemaTracksManager` |

**Footer**: Help section about media storage (Supabase/CDN)

---

### AdminTopicsPage (`/admin/topics`)

**Layout**: No tabs, stacked sections

**Sections**:
1. `TopicSuggestionsManager` - User suggestions
2. `TopicContentSuggestionsManager` - Content suggestions
3. `TopicQAIssuesManager` - QA issues
4. Stats cards (total, translated, untranslated, core)
5. Search/filter card with CSV import
6. Topics table with pagination

**Filters**: all, translated, untranslated, core

---

### AdminUsersPage (`/admin/users`)

**Tabs** (3):
| Tab | Value | Icon | Component |
|-----|-------|------|-----------|
| Käyttäjät | `users` | Users | Inline user management |
| Historia | `history` | History | `UserHistoryManager` |
| Sähköpostit | `emails` | Mail | `EmailTemplatesManager` |

**Users tab contents**:
- Add role card
- Users table with plan, tokens, roles, actions
- Edit user dialog

---

## Manager Components

| Component | Location | Used In |
|-----------|----------|---------|
| `AdminHeader` | `components/admin/AdminHeader.tsx` | All admin pages |
| `AIFeaturesManager` | `components/admin/AIFeaturesManager.tsx` | AI page |
| `AIPricingManager` | `components/admin/AIPricingManager.tsx` | AI page |
| `AIPromptsManager` | `components/admin/AIPromptsManager.tsx` | AI page |
| `AISummaryFeedbackManager` | `components/admin/AISummaryFeedbackManager.tsx` | AI page |
| `AITestTool` | `components/admin/AITestTool.tsx` | AI page |
| `AudioVoicesManager` | `components/admin/AudioVoicesManager.tsx` | Audio page |
| `CinemaTracksManager` | `components/admin/CinemaTracksManager.tsx` | Cinema page |
| `CinemaVisualsManager` | `components/admin/CinemaVisualsManager.tsx` | Cinema page |
| `EmailTemplatesManager` | `components/admin/EmailTemplatesManager.tsx` | Users page |
| `TopicContentSuggestionsManager` | `components/admin/TopicContentSuggestionsManager.tsx` | Topics page |
| `TopicQAIssuesManager` | `components/admin/TopicQAIssuesManager.tsx` | Topics page |
| `TopicSuggestionsManager` | `components/admin/TopicSuggestionsManager.tsx` | Topics page |
| `UserHistoryManager` | `components/admin/UserHistoryManager.tsx` | Users page |
| `VersionAudioConfigManager` | `components/admin/VersionAudioConfigManager.tsx` | Audio page |

### Token Components (`components/admin/tokens/`)

| Component | Purpose |
|-----------|---------|
| `TokenCategorySection` | Collapsible section wrapper with badge |
| `TokenDeadlineIndicator` | Deadline status badge |
| `TokenEditDialog` | Edit token dialog |
| `useApiTokens` | Hook for token CRUD + deadline utilities |

---

## Page Layout Patterns

### With Sidebar (standard)
```tsx
<SidebarProvider>
  <div className="min-h-screen flex w-full bg-background">
    <AppSidebar ... />
    <main className="flex-1 overflow-auto">
      <AdminHeader ... />
      <div className="p-6">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Content */}
        </div>
      </div>
    </main>
  </div>
</SidebarProvider>
```

### Sidebar closed by default
```tsx
<SidebarProvider defaultOpen={false}>
```

### Without Sidebar (simpler pages)
```tsx
<div className="min-h-screen bg-background">
  <AdminHeader ... showSidebarTrigger={false} />
  <div className="container mx-auto p-4 max-w-6xl">
    {/* Content */}
  </div>
</div>
```

---

## Common UI Patterns

### Tab Structure
```tsx
<Tabs defaultValue="first" className="space-y-6">
  <TabsList className="grid w-full grid-cols-2">
    <TabsTrigger value="first">Tab 1</TabsTrigger>
    <TabsTrigger value="second">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="first">
    <ManagerComponent />
  </TabsContent>
</Tabs>
```

### Stats Card Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-4 gap-4">
  <Card>
    <CardHeader className="pb-2">
      <CardTitle className="text-sm font-medium text-muted-foreground">
        Label
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
    </CardContent>
  </Card>
</div>
```

### Collapsible Section
```tsx
<Accordion type="single" collapsible defaultValue={open ? "section" : undefined}>
  <AccordionItem value="section">
    <AccordionTrigger>Section Title</AccordionTrigger>
    <AccordionContent>
      {/* Content */}
    </AccordionContent>
  </AccordionItem>
</Accordion>
```
