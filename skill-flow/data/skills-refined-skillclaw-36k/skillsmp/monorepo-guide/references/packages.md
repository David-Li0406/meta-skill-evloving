# Package Reference

## Table of Contents
- [shared-auth](#shared-auth)
- [shared-content](#shared-content)
- [shared-history](#shared-history)
- [shared-voice](#shared-voice)
- [ai](#ai)
- [ui](#ui)

## shared-auth

Authentication and user management.

**Location:** `packages/shared-auth/`
**Alias:** `@shared-auth`

### Exports
```typescript
// hooks/useAuth.ts
export function useAuth(): {
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

// hooks/useUserRole.ts
export function useUserRole(): {
  isAdmin: boolean;
  isModerator: boolean;
  role: 'admin' | 'moderator' | 'user' | null;
  isLoading: boolean;
}
```

### Usage
```typescript
import { useAuth } from "@shared-auth/hooks/useAuth";
import { useUserRole } from "@shared-auth/hooks/useUserRole";

function MyComponent() {
  const { user, signOut } = useAuth();
  const { isAdmin } = useUserRole();
}
```

## shared-content

Bible content, search, and topic management.

**Location:** `packages/shared-content/`
**Alias:** `@shared-content`

### Exports
```typescript
// hooks/useTopicSuggestions.ts
export function useTopicSuggestions(query: string): {
  suggestions: Topic[];
  isLoading: boolean;
}

// hooks/useComprehensiveTopicSuggestions.ts
export function useComprehensiveTopicSuggestions(query: string): {
  topics: Topic[];
  verses: Verse[];
  isLoading: boolean;
}

// hooks/useTopicContentSuggestions.ts
export function useTopicContentSuggestions(topicId: string): {
  content: TopicContent;
  isLoading: boolean;
}
```

### Usage
```typescript
import { useTopicSuggestions } from "@shared-content/hooks/useTopicSuggestions";

function SearchComponent() {
  const { suggestions } = useTopicSuggestions(searchTerm);
}
```

## shared-history

Reading history, bookmarks, and user activity tracking.

**Location:** `packages/shared-history/`
**Alias:** `@shared-history`

### Exports
```typescript
// hooks/useReadingHistory.ts
export function useReadingHistory(): {
  history: ReadingEntry[];
  addEntry: (entry: ReadingEntry) => void;
  clearHistory: () => void;
}

// hooks/useBookmarks.ts
export function useBookmarks(): {
  bookmarks: Bookmark[];
  addBookmark: (verseId: string) => void;
  removeBookmark: (id: string) => void;
}
```

## shared-voice

Audio Bible and text-to-speech features.

**Location:** `packages/shared-voice/`
**Alias:** `@shared-voice`

### Exports
```typescript
// hooks/useAudioPlayer.ts
export function useAudioPlayer(): {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  play: (url: string) => void;
  pause: () => void;
  seek: (time: number) => void;
}

// hooks/useVoicePreferences.ts
export function useVoicePreferences(): {
  speed: number;
  voice: string;
  setSpeed: (speed: number) => void;
  setVoice: (voice: string) => void;
}
```

## ai

AI integration, prompts, and usage tracking.

**Location:** `packages/ai/`
**Alias:** `@ai`

### Exports
```typescript
// Integration with AI orchestrator Edge Function
// Prompt management utilities
// Usage logging helpers
```

### Usage
AI features primarily accessed via Edge Functions, not directly from this package.

## ui

Shared shadcn/ui components.

**Location:** `packages/ui/`
**Alias:** `@ui`

### Available Components
All shadcn/ui components are available:

```typescript
import { Button } from "@ui/button";
import { Card, CardHeader, CardContent } from "@ui/card";
import { Dialog, DialogContent, DialogTrigger } from "@ui/dialog";
import { Input } from "@ui/input";
import { Label } from "@ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";
import { Toast, ToastProvider } from "@ui/toast";
// ... and all other shadcn components
```

### Usage Pattern
```typescript
import { Button } from "@ui/button";
import { Card, CardContent } from "@ui/card";

function MyComponent() {
  return (
    <Card>
      <CardContent>
        <Button variant="outline">Click me</Button>
      </CardContent>
    </Card>
  );
}
```

## Adding New Exports to Packages

### 1. Create the Module
```typescript
// packages/shared-auth/src/hooks/useNewHook.ts
export function useNewHook() {
  // implementation
}
```

### 2. Export from Index
```typescript
// packages/shared-auth/src/index.ts
export * from './hooks/useAuth';
export * from './hooks/useUserRole';
export * from './hooks/useNewHook';  // Add this
```

### 3. Use in App
```typescript
import { useNewHook } from "@shared-auth/hooks/useNewHook";
// or
import { useNewHook } from "@shared-auth";
```
