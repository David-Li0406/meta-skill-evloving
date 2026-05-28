# Mobile-Native Patterns

## Table of Contents
- [Breakpoints](#breakpoints)
- [Touch Interactions](#touch-interactions)
- [Bottom Navigation](#bottom-navigation)
- [Mobile Sheets](#mobile-sheets)
- [Safe Areas](#safe-areas)
- [Responsive Hooks](#responsive-hooks)
- [Gestures](#gestures)
- [Native-Like Animations](#native-like-animations)

## Breakpoints

```tsx
// Tailwind breakpoints
// Default (no prefix) = mobile-first
// md: = 768px+ (tablet/desktop)
// lg: = 1024px+
// xl: = 1280px+

// Mobile-first pattern
<div className="px-4 md:px-8">        {/* 16px mobile, 32px desktop */}
<div className="flex-col md:flex-row"> {/* Stack mobile, row desktop */}
<div className="hidden md:block">      {/* Desktop only */}
<div className="md:hidden">            {/* Mobile only */}
```

## Touch Interactions

### Touch Target Sizes
```tsx
// Minimum 44px touch targets (Apple HIG)
<Button className="h-11 min-w-[44px]">Tap Me</Button>

// Icon button with proper size
<Button variant="ghost" size="icon" className="h-11 w-11">
  <Menu className="h-5 w-5" />
</Button>

// List item touch target
<button className="w-full h-12 flex items-center px-4 active:bg-accent">
  <span>Menu Item</span>
</button>
```

### Touch Feedback
```tsx
// Scale on press
<button className="active:scale-95 transition-transform">
  Tap Me
</button>

// Background change on press
<button className="active:bg-accent/80 transition-colors">
  Tap Me
</button>

// Combined feedback
<Button className="active:scale-[0.98] active:opacity-90 transition-all">
  Native Feel
</Button>
```

### Preventing Accidental Taps
```tsx
// Disable double-tap zoom on interactive elements
<button className="touch-manipulation">
  No Zoom
</button>

// Prevent text selection during interaction
<div className="select-none">
  Interactive Area
</div>
```

## Bottom Navigation

### Standard Pattern
```tsx
const BottomNav = () => (
  <nav className="fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-t border-border md:hidden safe-area-bottom">
    <div className="flex items-center justify-around h-16 px-2">
      {navItems.map((item) => (
        <button
          key={item.label}
          onClick={item.action}
          className={cn(
            "flex flex-col items-center justify-center flex-1 h-full gap-1",
            "transition-colors active:scale-95",
            item.isActive
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          <item.icon className={cn("h-5 w-5", item.isActive && "scale-110")} />
          <span className={cn(
            "text-[10px] font-medium",
            item.isActive && "font-semibold"
          )}>
            {item.label}
          </span>
        </button>
      ))}
    </div>
  </nav>
);
```

### With Badge
```tsx
<button className="relative flex flex-col items-center">
  <div className="relative">
    <Bell className="h-5 w-5" />
    <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-destructive text-[10px] text-white flex items-center justify-center">
      3
    </span>
  </div>
  <span className="text-[10px]">Alerts</span>
</button>
```

## Mobile Sheets

### Bottom Sheet
```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button>Open</Button>
  </SheetTrigger>
  <SheetContent
    side="bottom"
    className="h-[85vh] rounded-t-[20px] px-0"
  >
    {/* Drag handle */}
    <div className="flex justify-center py-3">
      <div className="w-12 h-1.5 rounded-full bg-muted" />
    </div>

    <SheetHeader className="px-4">
      <SheetTitle>Sheet Title</SheetTitle>
    </SheetHeader>

    <ScrollArea className="h-full px-4 pb-safe">
      {/* Content */}
    </ScrollArea>
  </SheetContent>
</Sheet>
```

### Full Screen Modal (Mobile)
```tsx
const isMobile = useIsMobile();

{isMobile ? (
  <Sheet>
    <SheetContent side="bottom" className="h-full rounded-none">
      {/* Full screen content */}
    </SheetContent>
  </Sheet>
) : (
  <Dialog>
    <DialogContent className="max-w-lg">
      {/* Desktop modal */}
    </DialogContent>
  </Dialog>
)}
```

## Safe Areas

### CSS Classes
```css
/* In global CSS */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.safe-area-top {
  padding-top: env(safe-area-inset-top, 0px);
}

.pb-safe {
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}
```

### Usage
```tsx
// Bottom navigation with safe area
<nav className="fixed bottom-0 safe-area-bottom">
  {/* Nav content */}
</nav>

// Content area avoiding bottom nav
<main className="pb-20 md:pb-0">
  {/* Main content - 80px padding on mobile for nav */}
</main>

// Full height with safe areas
<div className="min-h-[100dvh] safe-area-top safe-area-bottom">
  {/* Content */}
</div>
```

## Responsive Hooks

### useIsMobile
```tsx
import { useIsMobile } from "@/hooks/use-mobile";

function Component() {
  const isMobile = useIsMobile();

  return (
    <div>
      {isMobile ? <MobileView /> : <DesktopView />}
    </div>
  );
}
```

### Custom Breakpoint Hook
```tsx
function useBreakpoint() {
  const [breakpoint, setBreakpoint] = useState({
    isPhone: false,
    isTablet: false,
    isDesktop: true,
  });

  useEffect(() => {
    const checkBreakpoint = () => {
      const width = window.innerWidth;
      setBreakpoint({
        isPhone: width < 768,
        isTablet: width >= 768 && width < 1280,
        isDesktop: width >= 1280,
      });
    };

    checkBreakpoint();
    window.addEventListener('resize', checkBreakpoint);
    return () => window.removeEventListener('resize', checkBreakpoint);
  }, []);

  return breakpoint;
}
```

### Touch Device Detection
```tsx
function useTouchDevice() {
  const [isTouch, setIsTouch] = useState(false);

  useEffect(() => {
    setIsTouch(
      'ontouchstart' in window ||
      navigator.maxTouchPoints > 0
    );
  }, []);

  return isTouch;
}
```

## Gestures

### Swipe Detection
```tsx
function useSwipe(onSwipeLeft?: () => void, onSwipeRight?: () => void) {
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) onSwipeLeft?.();
    if (isRightSwipe) onSwipeRight?.();
  };

  return { onTouchStart, onTouchMove, onTouchEnd };
}
```

### Pull to Refresh Pattern
```tsx
function PullToRefresh({ onRefresh, children }) {
  const [pulling, setPulling] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  // Implement pull detection logic...

  return (
    <div className="relative overflow-hidden">
      {refreshing && (
        <div className="absolute top-0 left-0 right-0 flex justify-center py-4">
          <Loader2 className="h-6 w-6 animate-spin" />
        </div>
      )}
      <div className={cn(refreshing && "translate-y-12 transition-transform")}>
        {children}
      </div>
    </div>
  );
}
```

## Native-Like Animations

### Bounce Animation
```css
@keyframes bounce-once {
  0%, 100% { transform: scale(1); }
  25% { transform: scale(0.85); }
  50% { transform: scale(1.15); }
  75% { transform: scale(1.05); }
}

.animate-bounce-once {
  animation: bounce-once 0.3s ease-out;
}
```

### Slide Transitions
```tsx
// Page transition
<div className="animate-in slide-in-from-right-4 duration-200">
  <NewPage />
</div>

// Modal entrance
<div className="animate-in fade-in-0 zoom-in-95 duration-200">
  <ModalContent />
</div>
```

### Spring Animation (CSS)
```css
.spring-bounce {
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.spring-bounce:active {
  transform: scale(0.95);
}
```

## Mobile-Specific UI Patterns

### Floating Action Button
```tsx
<Button
  size="icon"
  className="fixed bottom-20 right-4 h-14 w-14 rounded-full shadow-lg z-40 md:hidden"
>
  <Plus className="h-6 w-6" />
</Button>
```

### Pull-Down Header
```tsx
<header className="sticky top-0 z-40 bg-background/95 backdrop-blur-md border-b">
  <div className="flex items-center h-14 px-4">
    <Button variant="ghost" size="icon" onClick={goBack}>
      <ChevronLeft className="h-5 w-5" />
    </Button>
    <h1 className="flex-1 text-center font-semibold truncate">
      Page Title
    </h1>
    <Button variant="ghost" size="icon">
      <MoreVertical className="h-5 w-5" />
    </Button>
  </div>
</header>
```

### Inline Actions (Swipe-to-Reveal Alternative)
```tsx
<div className="flex items-center gap-2 p-3 border-b">
  <div className="flex-1">
    <p className="font-medium">Item Title</p>
    <p className="text-sm text-muted-foreground">Subtitle</p>
  </div>
  <Button variant="ghost" size="icon" className="h-9 w-9">
    <Edit className="h-4 w-4" />
  </Button>
  <Button variant="ghost" size="icon" className="h-9 w-9 text-destructive">
    <Trash className="h-4 w-4" />
  </Button>
</div>
```
