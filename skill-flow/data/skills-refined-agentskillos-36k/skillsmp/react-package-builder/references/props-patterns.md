# Props Patterns for Reusable React Packages

## 1. Controlled vs Uncontrolled

Support both patterns for stateful props:

```typescript
interface Props {
  // Controlled mode
  currentIndex?: number;

  // Uncontrolled mode (initial value)
  defaultIndex?: number;

  // Change callback (works with both)
  onIndexChange?: (index: number, meta: { source: string }) => void;
}
```

Implementation:

```typescript
function Component({ currentIndex, defaultIndex = 0, onIndexChange }: Props) {
  const [internalIndex, setInternalIndex] = useState(defaultIndex);
  const isControlled = currentIndex !== undefined;
  const index = isControlled ? currentIndex : internalIndex;

  const handleChange = (newIndex: number, source: string) => {
    if (!isControlled) setInternalIndex(newIndex);
    onIndexChange?.(newIndex, { source });
  };
}
```

## 2. Event Callbacks (Signals Only)

Package emits intent, parent handles side effects:

```typescript
interface Props {
  // Toggle signals
  verseAudioEnabled?: boolean;
  onToggleVerseAudio?: (enabled: boolean) => void;

  // Volume signals
  onVoiceVolumeChange?: (volume: number) => void;

  // Lifecycle
  onExit?: () => void;
}
```

**Rule**: Never pass refs, audio elements, or external state objects. Use callbacks.

## 3. Engine Abstraction

Decouple animation/logic implementation from component:

```typescript
// Engine contract
export type Engine = {
  mount(opts: MountOptions): { destroy(): void };
  step(dir: 1 | -1): void;
  seek(index: number): void;
  setPlaying(playing: boolean): void;
};

// Multiple implementations
const gsapEngine: Engine = { ... };
const framerEngine: Engine = { ... };
```

Component selects engine via prop:

```typescript
interface Props {
  animationPreset?: "loopCarouselV" | "loopCarouselH";
}
```

## 4. Content Props

Simple data structures, no app-specific types:

```typescript
// Good: Generic structure
interface Verse {
  id: string;
  number: string | number;
  text: string;
}

// Bad: App-specific structure
interface BundleVerse {
  verse_id: number;
  book_id: number;
  // ... Supabase-specific fields
}
```

## 5. Behavior Props

Flags and settings that affect rendering:

```typescript
interface Props {
  // Animation
  orientation?: "vertical" | "horizontal";
  speed?: number;
  reducedMotion?: boolean;

  // Playback
  playing?: boolean;
  onPlayingChange?: (playing: boolean) => void;
}
```

## 6. Props Organization

Group related props in interface:

```typescript
interface ComponentProps {
  // ---- Content ----
  title: string;
  subtitle?: string;
  items: Item[];

  // ---- Index Control ----
  currentIndex?: number;
  defaultIndex?: number;
  onIndexChange?: (index: number) => void;

  // ---- Playback ----
  playing?: boolean;
  onPlayingChange?: (playing: boolean) => void;

  // ---- Animation ----
  orientation?: "vertical" | "horizontal";
  speed?: number;

  // ---- Lifecycle ----
  onExit?: () => void;
}
```
