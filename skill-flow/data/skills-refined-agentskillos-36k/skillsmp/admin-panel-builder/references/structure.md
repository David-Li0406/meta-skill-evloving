# Admin Panel Structure Reference

## Directory Layout

```
apps/raamattu-nyt/src/
├── pages/
│   ├── AdminDashboardPage.tsx    # Main dashboard with cards
│   ├── AdminAIPage.tsx           # AI management (prompts, pricing, quotas)
│   ├── AdminAudioPage.tsx        # Audio/TTS management
│   ├── AdminAuthTokensPage.tsx   # API tokens management
│   ├── AdminTopicsPage.tsx       # Topic management
│   ├── AdminTranslationsPage.tsx # Translation cache
│   ├── AdminUsersPage.tsx        # Users and roles
│   ├── AdminVideoPage.tsx        # Video series/clips
│   ├── AdminWidgetAnalyticsPage.tsx # Widget stats
│   └── TopicEditorPage.tsx       # Topic detail editor
├── components/admin/
│   ├── AdminHeader.tsx           # Shared header component
│   ├── AI*Manager.tsx            # AI feature managers
│   ├── Audio*Manager.tsx         # Audio managers
│   ├── Topic*Manager.tsx         # Topic managers
│   ├── UserHistoryManager.tsx    # User activity
│   ├── EmailTemplatesManager.tsx # Email templates
│   └── tokens/                   # Token management components
└── App.tsx                       # Route definitions
```

## Route Configuration

In `App.tsx`:
```tsx
<Route path="/admin" element={<AdminDashboardPage />} />
<Route path="/admin/audio" element={<AdminAudioPage />} />
<Route path="/admin/video" element={<AdminVideoPage />} />
<Route path="/admin/widget-analytics" element={<AdminWidgetAnalyticsPage />} />
<Route path="/admin/users" element={<AdminUsersPage />} />
<Route path="/admin/topics" element={<AdminTopicsPage />} />
<Route path="/admin/topics/:topicId/edit" element={<TopicEditorPage />} />
<Route path="/admin/ai" element={<AdminAIPage />} />
<Route path="/admin/translations" element={<AdminTranslationsPage />} />
<Route path="/admin/auth-tokens" element={<AdminAuthTokensPage />} />
```

## Dashboard Card Structure

Each admin section appears as a card on the dashboard with:
- Icon
- Title
- Description
- Stats (optional)
- Path to navigate

```tsx
const adminSections = [
  {
    title: "AI Management",
    description: "AI prompts, pricing, quotas",
    icon: Sparkles,
    path: "/admin/ai",
    stats: [{ label: "features", value: 9 }]
  },
  // ... more sections
];
```

## Standard Page Layout

All admin pages follow this structure:

```tsx
<SidebarProvider>
  <div className="min-h-screen flex w-full bg-background">
    <AppSidebar onNavigateToContinueAudio={() => {}} onNavigateToContinueText={() => {}} />
    <main className="flex-1 overflow-auto">
      <AdminHeader
        title="Page Title"
        icon={<IconName className="h-6 w-6 text-primary" />}
        showBackButton={true}
      />
      <div className="p-6">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Page content */}
        </div>
      </div>
    </main>
  </div>
</SidebarProvider>
```

## AdminHeader Props

```tsx
interface AdminHeaderProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  showBackButton?: boolean;      // Default: true
  showSidebarTrigger?: boolean;  // Default: true
}
```

## Tab-Based Pages

Most admin pages use tabs for organization:

```tsx
<Tabs defaultValue="tab1" className="space-y-4">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">
    <Card>
      <CardHeader><CardTitle>Section 1</CardTitle></CardHeader>
      <CardContent><Manager1 /></CardContent>
    </Card>
  </TabsContent>
  <TabsContent value="tab2">
    <Card>
      <CardHeader><CardTitle>Section 2</CardTitle></CardHeader>
      <CardContent><Manager2 /></CardContent>
    </Card>
  </TabsContent>
</Tabs>
```

## Existing Manager Components

| Component | Purpose | Used In |
|-----------|---------|---------|
| `AIFeaturesManager` | AI feature config | AdminAIPage |
| `AIPricingManager` | Model pricing | AdminAIPage |
| `AIPromptsManager` | Prompt templates | AdminAIPage |
| `AIQuotasManager` | Plan quotas | AdminAIPage |
| `AITestTool` | AI testing | AdminAIPage |
| `AISummaryFeedbackManager` | AI feedback | AdminAIPage |
| `AudioVoicesManager` | TTS voices | AdminAudioPage |
| `VersionAudioConfigManager` | Version audio | AdminAudioPage |
| `TopicSuggestionsManager` | Topic suggestions | AdminTopicsPage |
| `TopicQAIssuesManager` | QA issues | AdminTopicsPage |
| `TopicContentSuggestionsManager` | Content suggestions | AdminTopicsPage |
| `UserHistoryManager` | User activity | AdminUsersPage |
| `EmailTemplatesManager` | Email templates | AdminUsersPage |
| `TokenEditDialog` | Token editing | AdminAuthTokensPage |
