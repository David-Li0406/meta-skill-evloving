# VueUse Integration

**Check if installed:** Look for `@vueuse/core` or `@vueuse/nuxt` in package.json before using.

## Overview

VueUse is a collection of essential Vue Composition Utilities. It provides ready-made composables for common tasks, eliminating the need to write custom implementations.

## Installation Detection

Prefer VueUse over custom implementations when it's installed. Check package.json first.

## Common Composables

### State Management

**useLocalStorage / useSessionStorage**

```typescript
// Syncs ref with localStorage
const token = useLocalStorage("auth-token", "")
const user = useLocalStorage<User | null>("user", null)

// Automatically saves to localStorage when updated
token.value = "new-token"
```

**useToggle**

```typescript
const [isOpen, toggle] = useToggle()
// toggle() switches between true/false
// toggle(true) sets to true
// toggle(false) sets to false
```

**useCounter**

```typescript
const { count, inc, dec, set, reset } = useCounter(0, { min: 0, max: 10 })
```

### Browser APIs

**useMouse**

```typescript
const { x, y, sourceType } = useMouse()
// Reactive mouse position
```

**useWindowSize**

```typescript
const { width, height } = useWindowSize()
// Reactive window dimensions
```

**useScroll**

```typescript
const { x, y, isScrolling, arrivedState, directions } = useScroll(elementRef)
// Track scroll position and state
```

**useClipboard**

```typescript
const { text, copy, copied, isSupported } = useClipboard()

async function copyToClipboard() {
  await copy("Hello World")
  // copied.value is true for 1.5s
}
```

**useMediaQuery**

```typescript
const isMobile = useMediaQuery("(max-width: 768px)")
const isDark = useMediaQuery("(prefers-color-scheme: dark)")
```

### Element Interaction

**useIntersectionObserver**

```typescript
const target = ref<HTMLElement | null>(null)
const isVisible = ref(false)

useIntersectionObserver(target, ([{ isIntersecting }]) => {
  isVisible.value = isIntersecting
})
```

**useElementVisibility**

```typescript
const target = ref<HTMLElement | null>(null)
const isVisible = useElementVisibility(target)
```

**useFocus**

```typescript
const input = ref<HTMLInputElement | null>(null)
const { focused } = useFocus(input)

// Auto-focus on mount
useFocus(input, { initialValue: true })
```

### Network

**useFetch** (VueUse version, different from Nuxt's useFetch)

```typescript
const { data, error, isFetching } = useFetch("https://api.example.com/users")
  .get()
  .json()
```

Note: In Nuxt, prefer Nuxt's built-in `useFetch` for API calls. Use VueUse's `useFetch` only for external APIs or when you need different behavior.

### Utilities

**refDebounced / useDebounceFn**

```typescript
// Debounce a ref value
const input = ref("")
const debounced = refDebounced(input, 500)

// Debounce a function
const debouncedFn = useDebounceFn(() => {
  console.log("Debounced!")
}, 500)
```

**refThrottled / useThrottleFn**

```typescript
// Throttle a ref value
const scrollY = ref(0)
const throttled = refThrottled(scrollY, 200)

// Throttle a function
const throttledFn = useThrottleFn(() => {
  console.log("Throttled!")
}, 200)
```

**useInterval / useTimeout**

```typescript
const counter = ref(0)
const { pause, resume } = useInterval(1000, {
  callback: () => counter.value++,
})
```

**useEventListener**

```typescript
useEventListener(window, "resize", () => {
  console.log("Window resized")
})

// On element
const button = ref<HTMLButtonElement | null>(null)
useEventListener(button, "click", () => {
  console.log("Clicked")
})
```

## Nuxt Auto-Import

When using `@vueuse/nuxt`, composables are auto-imported. No need to import them manually.

```typescript
// ✅ With @vueuse/nuxt
const { width } = useWindowSize()

// ❌ Without @vueuse/nuxt (need manual import)
import { useWindowSize } from "@vueuse/core"
const { width } = useWindowSize()
```

## Common Patterns

### Dark Mode Toggle

```typescript
const isDark = useDark()
const toggleDark = useToggle(isDark)
```

### Infinite Scroll

```typescript
const el = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(el)

watch(
  () => arrivedState.bottom,
  async (isBottom) => {
    if (isBottom) {
      await loadMore()
    }
  },
)
```

### Form Field Debouncing

```typescript
const searchQuery = ref("")
const debouncedQuery = refDebounced(searchQuery, 300)

watch(debouncedQuery, async (query) => {
  // API call with debounced value
  await searchProducts(query)
})
```

### Responsive Breakpoints

```typescript
const breakpoints = useBreakpoints({
  mobile: 640,
  tablet: 768,
  laptop: 1024,
  desktop: 1280,
})

const isMobile = breakpoints.smaller("tablet")
const isDesktop = breakpoints.greaterOrEqual("laptop")
```

## Resources

- [VueUse Documentation](https://vueuse.org/)
- [Function Reference](https://vueuse.org/functions.html)
