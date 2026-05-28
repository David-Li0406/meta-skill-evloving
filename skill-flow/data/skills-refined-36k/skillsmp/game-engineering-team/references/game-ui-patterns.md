# Game UI Patterns Reference

## Base Game Components

```typescript
// Animated number display
function AnimatedNumber({ value }: { value: number }) {
  const spring = useSpring(value, { stiffness: 100, damping: 30 });
  const display = useTransform(spring, (v) => Math.floor(v).toLocaleString());
  return <motion.span>{display}</motion.span>;
}

// Progress bar with juice
function ProgressBar({ value, max = 100 }: { value: number; max?: number }) {
  const percentage = Math.min((value / max) * 100, 100);
  return (
    <div className="progress-track">
      <motion.div 
        className="progress-fill"
        animate={{ width: `${percentage}%` }}
        transition={{ type: 'spring', stiffness: 100 }}
      />
    </div>
  );
}

// Game button with haptics
function GameButton({ onClick, children }: { onClick: () => void; children: React.ReactNode }) {
  const handleClick = () => {
    if ('vibrate' in navigator) navigator.vibrate(10);
    onClick();
  };
  return (
    <motion.button onClick={handleClick} whileTap={{ scale: 0.95 }}>
      {children}
    </motion.button>
  );
}
```

## Modal System

```typescript
function GameModal({ open, children, pauseGame = true }: GameModalProps) {
  const { pause, resume } = useGameLoop();
  
  useEffect(() => {
    if (pauseGame) open ? pause() : resume();
  }, [open, pauseGame]);
  
  return (
    <AnimatePresence>
      {open && (
        <motion.div className="modal-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <motion.div className="modal-content" initial={{ scale: 0.9 }} animate={{ scale: 1 }}>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## Toast Notifications

```typescript
function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);
  
  const showToast = (toast: Omit<Toast, 'id'>) => {
    const id = crypto.randomUUID();
    setToasts(prev => [...prev, { ...toast, id }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
  };
  
  return {
    toasts,
    success: (message: string) => showToast({ type: 'success', message }),
    error: (message: string) => showToast({ type: 'error', message }),
    achievement: (message: string) => showToast({ type: 'achievement', message }),
  };
}
```

## Touch/Gesture Handling

```typescript
function useSwipe(onSwipe: (dir: 'left' | 'right' | 'up' | 'down') => void) {
  const startPos = useRef({ x: 0, y: 0 });
  
  const handlers = {
    onTouchStart: (e: TouchEvent) => {
      startPos.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    },
    onTouchEnd: (e: TouchEvent) => {
      const dx = e.changedTouches[0].clientX - startPos.current.x;
      const dy = e.changedTouches[0].clientY - startPos.current.y;
      
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
        onSwipe(dx > 0 ? 'right' : 'left');
      } else if (Math.abs(dy) > 50) {
        onSwipe(dy > 0 ? 'down' : 'up');
      }
    },
  };
  
  return handlers;
}

function useLongPress(callback: () => void, delay = 500) {
  const timeout = useRef<number>();
  return {
    onTouchStart: () => { timeout.current = window.setTimeout(callback, delay); },
    onTouchEnd: () => { clearTimeout(timeout.current); },
  };
}
```

## Responsive Game Layout

```typescript
function useGameScale() {
  const [scale, setScale] = useState(1);
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const updateScale = () => {
      const container = containerRef.current?.parentElement;
      if (!container) return;
      const scaleX = container.clientWidth / 390;  // iPhone design width
      const scaleY = container.clientHeight / 844;
      setScale(Math.min(scaleX, scaleY, 1.5));
    };
    
    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, []);
  
  return { scale, containerRef };
}
```

## Accessibility

```typescript
function useGameAnnouncer() {
  return useCallback((message: string) => {
    const el = document.getElementById('game-announcer');
    if (el) el.textContent = message;
  }, []);
}

// Hidden announcer for screen readers
function GameAnnouncer() {
  return <div id="game-announcer" role="status" aria-live="polite" className="sr-only" />;
}
```

---

*Game UI Patterns Reference - Game Engineering Team*
