# Code Locations Reference

## Apps Structure

### raamattu-nyt (Main App)

```
apps/raamattu-nyt/src/
├── App.tsx                 # Routes, providers
├── main.tsx                # Entry point
├── index.css               # Global styles
├── pages/
│   ├── Index.tsx           # Home page
│   ├── ReaderPage.tsx      # Bible reader
│   ├── SearchPage.tsx      # Search
│   ├── TopicPage.tsx       # Single topic
│   ├── TopicsBrowsePage.tsx # Topic browser
│   ├── VideoPage.tsx       # Video player
│   ├── SettingsPage.tsx    # User settings
│   ├── Admin*.tsx          # Admin pages (9 total)
│   └── TopicEditorPage.tsx # Topic editing
├── components/
│   ├── AppSidebar.tsx      # Main navigation
│   ├── BibleReader*.tsx    # Reader components
│   ├── Audio*.tsx          # Audio player
│   ├── Search*.tsx         # Search UI
│   ├── Topic*.tsx          # Topic display
│   ├── admin/              # Admin components
│   └── ui/                 # Local UI overrides
├── hooks/
│   ├── useAIQuota.ts       # AI quota management
│   ├── usePlanInfo.ts      # Subscription plans
│   ├── useChapterBundle.tsx # Chapter loading
│   ├── useFeedback.ts      # User feedback
│   ├── useNotifications.ts # Notifications
│   ├── useActiveSummary.ts # Summary state
│   ├── useSwipe.tsx        # Touch gestures
│   ├── use-toast.ts        # Toast notifications
│   └── use-mobile.tsx      # Mobile detection
├── lib/
│   ├── bibleService.ts     # Bible API
│   ├── searchService.ts    # Search logic
│   ├── audioService.ts     # Audio management
│   ├── aiSummaryService.ts # AI summaries
│   ├── verseParser.ts      # OSIS parsing
│   ├── bookNameMapping.ts  # Book name utils
│   ├── activityLogger.ts   # Activity tracking
│   ├── topicEditorUtils.ts # Topic editing
│   ├── config.ts           # App configuration
│   └── reader/             # Reader utilities
│       └── outlook.ts      # Responsive layout
└── integrations/
    └── supabase/
        ├── client.ts       # Supabase client
        └── types.ts        # Generated types
```

### idea-machina (AI App)

```
apps/idea-machina/src/
├── App.tsx
├── main.tsx
└── components/
```

## Packages Structure

### packages/ui (Shared Components)

```
packages/ui/src/
├── button.tsx
├── card.tsx
├── dialog.tsx
├── input.tsx
├── select.tsx
├── tabs.tsx
├── table.tsx
├── form.tsx
└── ... (all shadcn components)
```

### packages/shared-auth

```
packages/shared-auth/
├── hooks/
│   └── useUserRole.ts      # Role checking
└── lib/
    └── session.ts          # Session management
```

### packages/shared-voice

```
packages/shared-voice/
└── hooks/
    └── useVoicePreferences.ts
```

## Supabase Structure

### Edge Functions

```
supabase/functions/
├── _shared/                # Shared modules
│   ├── ai-quota.ts         # Quota helpers
│   ├── cors.ts             # CORS config
│   └── supabase.ts         # Client init
├── ai-orchestrator/        # Main AI endpoint
├── embed/                  # Embeddings
├── generate-audio/         # TTS generation
├── topic-translations/     # Topic translation
├── translate-search-term/  # Term translation
├── send-notifications/     # Email via Resend
└── get-elevenlabs-usage/   # Usage stats
```

### Migrations

```
supabase/migrations/
├── 2024*                   # Older migrations
├── 20260107*               # AI quota system
└── 20260108*               # Recent updates
```

## Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Root workspace config |
| `apps/*/package.json` | App dependencies |
| `packages/*/package.json` | Package dependencies |
| `tsconfig.json` | TypeScript config |
| `vite.config.ts` | Vite build config |
| `tailwind.config.ts` | Tailwind CSS |
| `supabase/config.toml` | Supabase settings |
| `.env` / `.env.local` | Environment variables |

## Import Aliases

| Alias | Path |
|-------|------|
| `@/` | `apps/raamattu-nyt/src/` |
| `@ui/` | `packages/ui/src/` |
| `@shared-auth/` | `packages/shared-auth/` |
| `@shared-voice/` | `packages/shared-voice/` |
| `@shared-content/` | `packages/shared-content/` |
| `@shared-history/` | `packages/shared-history/` |
