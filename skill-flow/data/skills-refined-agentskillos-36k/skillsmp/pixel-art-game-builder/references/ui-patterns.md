# UI Patterns Reference

Complete guide for UI components, layout, and user experience patterns.

## Layout Structure

### Mobile Layout (Primary)

```
┌─────────────────────────────────────┐
│           HEADER                    │  60px
│    [Credits]      [Energy Bar]      │
├─────────────────────────────────────┤
│                                     │
│                                     │
│         MAIN CONTENT                │  flex-1
│         (Tab Content)               │
│                                     │
│                                     │
├─────────────────────────────────────┤
│           TAB BAR                   │  60px + safe-area
│  [Scan] [Collection] [Upgrades]     │
│  [Sectors] [Employees]              │
└─────────────────────────────────────┘
```

### Desktop Layout (≥1024px)

```
┌─────────────────────────────────────────────────────┐
│                    HEADER                           │
├────────────────┬────────────────────────────────────┤
│                │                                    │
│    SIDEBAR     │         MAIN CONTENT               │
│   (Tab Bar)    │                                    │
│                │                                    │
│    [Scan]      │                                    │
│  [Collection]  │                                    │
│  [Upgrades]    │                                    │
│   [Sectors]    │                                    │
│  [Employees]   │                                    │
│                │                                    │
└────────────────┴────────────────────────────────────┘
```

## Breakpoints

```typescript
const BREAKPOINTS = {
  mobile: 320,      // Mobile portrait
  tablet: 768,      // Tablet portrait
  desktop: 1024,    // Desktop
  wide: 1440,       // Wide desktop
};
```

```css
/* Tailwind classes */
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

## Z-Index System

```typescript
const Z_INDEX = {
  background: 0,
  content: 10,
  header: 20,
  tabBar: 20,
  dropdown: 30,
  modal: 40,
  modalContent: 41,
  toast: 50,
  tooltip: 60,
};
```

## Component Patterns

### Button

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({ variant, size, disabled, loading, children, onClick }: ButtonProps) {
  const baseClasses = "font-pixel rounded focus-ring transition-transform active:scale-95";
  
  const variantClasses = {
    primary: "bg-neon-cyan text-deep-black hover:brightness-110",
    secondary: "bg-space-gray text-main-white border border-border-gray hover:bg-border-gray",
    ghost: "bg-transparent text-interactive-cyan hover:bg-space-gray",
  };
  
  const sizeClasses = {
    sm: "px-3 py-1 text-sm min-h-[32px]",
    md: "px-4 py-2 text-base min-h-[44px]",  // Touch-friendly default
    lg: "px-6 py-3 text-lg min-h-[52px]",
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
}
```

### Card

```tsx
interface CardProps {
  rarity?: Rarity;
  selected?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

function Card({ rarity, selected, onClick, children }: CardProps) {
  const rarityBorder = rarity ? `border-${RARITY_COLORS[rarity]}` : 'border-border-gray';
  
  return (
    <div
      className={`
        bg-space-gray rounded-lg p-4
        border ${rarityBorder}
        ${selected ? 'ring-2 ring-neon-cyan' : ''}
        ${onClick ? 'cursor-pointer hover:bg-border-gray transition-colors' : ''}
      `}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
```

### Modal

```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;
  
  return (
    <div 
      className="fixed inset-0 z-modal flex items-center justify-center p-4"
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-deep-black/80 backdrop-blur-sm" />
      
      {/* Modal content */}
      <div 
        className="relative z-modal-content bg-space-gray rounded-lg p-6 max-w-md w-full
                   animate-in fade-in zoom-in-95 duration-200"
        onClick={e => e.stopPropagation()}
      >
        {title && (
          <h2 className="font-pixel text-xl text-main-white mb-4">{title}</h2>
        )}
        
        {children}
        
        <button
          className="absolute top-4 right-4 text-secondary-gray hover:text-main-white"
          onClick={onClose}
        >
          ✕
        </button>
      </div>
    </div>
  );
}
```

### ProgressBar

```tsx
interface ProgressBarProps {
  value: number;
  max: number;
  color?: string;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

function ProgressBar({ value, max, color = 'neon-cyan', showLabel, size = 'md' }: ProgressBarProps) {
  const percentage = Math.min(100, (value / max) * 100);
  
  const heights = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };
  
  return (
    <div className="w-full">
      <div className={`w-full bg-border-gray rounded-full ${heights[size]} overflow-hidden`}>
        <div
          className={`h-full bg-${color} transition-all duration-300 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {showLabel && (
        <div className="flex justify-between mt-1 text-xs text-secondary-gray">
          <span>{formatNumber(value)}</span>
          <span>{formatNumber(max)}</span>
        </div>
      )}
    </div>
  );
}
```

### ResourceDisplay (Header)

```tsx
function ResourceDisplay() {
  const { credits, energy, maxEnergy } = useGameStore();
  const incomePerSecond = useIncomePerSecond();
  
  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-space-gray">
      {/* Credits */}
      <div className="flex items-center gap-2">
        <span className="text-cosmic-gold">💰</span>
        <div className="flex flex-col">
          <span className="font-pixel text-main-white">{formatNumber(credits)}</span>
          <span className="text-xs text-valid-green">+{formatNumber(incomePerSecond)}/s</span>
        </div>
      </div>
      
      {/* Energy */}
      <div className="flex-1 flex items-center gap-2">
        <span className="text-neon-cyan">⚡</span>
        <div className="flex-1">
          <ProgressBar value={energy} max={maxEnergy} color="neon-cyan" />
          <span className="text-xs text-secondary-gray">
            {Math.floor(energy)}/{maxEnergy}
          </span>
        </div>
      </div>
    </div>
  );
}
```

### TabBar

```tsx
const TABS = [
  { id: 'scan', label: 'Scan', icon: '🔍' },
  { id: 'collection', label: 'Collection', icon: '📦' },
  { id: 'upgrades', label: 'Upgrades', icon: '⬆️' },
  { id: 'sectors', label: 'Sectors', icon: '🌌' },
  { id: 'employees', label: 'Staff', icon: '👤' },
];

function TabBar() {
  const { activeTab, setActiveTab } = useUIStore();
  
  return (
    <nav className="flex bg-space-gray border-t border-border-gray safe-area-bottom">
      {TABS.map(tab => (
        <button
          key={tab.id}
          className={`
            flex-1 flex flex-col items-center py-2 min-h-touch
            ${activeTab === tab.id 
              ? 'text-neon-cyan' 
              : 'text-secondary-gray hover:text-main-white'}
          `}
          onClick={() => setActiveTab(tab.id)}
        >
          <span className="text-lg">{tab.icon}</span>
          <span className="text-xs font-pixel">{tab.label}</span>
        </button>
      ))}
    </nav>
  );
}
```

### Toast Notifications

```tsx
interface Toast {
  id: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  duration?: number;
}

function ToastContainer() {
  const { toasts, removeToast } = useUIStore();
  
  return (
    <div className="fixed top-4 right-4 z-toast flex flex-col gap-2">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`
            px-4 py-3 rounded-lg shadow-lg
            animate-in slide-in-from-right duration-300
            ${toast.type === 'success' ? 'bg-valid-green/20 border border-valid-green' : ''}
            ${toast.type === 'error' ? 'bg-alert-red/20 border border-alert-red' : ''}
            ${toast.type === 'info' ? 'bg-neon-cyan/20 border border-neon-cyan' : ''}
          `}
        >
          <p className="text-main-white text-sm">{toast.message}</p>
        </div>
      ))}
    </div>
  );
}
```

## Animation Patterns

### CSS Keyframes

```css
/* Glow animations */
@keyframes glow-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Float animation for sprites */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

/* Modal entrance */
@keyframes modal-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Slide in from right (toasts) */
@keyframes slide-in-right {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Counter increment */
@keyframes count-up {
  from { opacity: 0.5; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Animation Durations

```typescript
const ANIMATION_DURATIONS = {
  instant: 0,
  fast: 100,
  normal: 200,
  slow: 300,
  verySlow: 500,
  sprite: 500,      // Minimum for sprite animations
  glow: 2000,       // Glow pulse cycle
  float: 2000,      // Float animation cycle
};
```

### Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'deep-black': '#0a0a0f',
        'space-gray': '#1a1a2e',
        'border-gray': '#2d2d44',
        'neon-cyan': '#00fff5',
        'soft-magenta': '#ff6bcb',
        'cosmic-gold': '#ffd93d',
        'valid-green': '#39ff14',
        'alert-red': '#ff4757',
        'mystery-purple': '#6c5ce7',
        'main-white': '#e8e8e8',
        'secondary-gray': '#a0a0a0',
        'interactive-cyan': '#7fefef',
      },
      fontFamily: {
        pixel: ['"Press Start 2P"', 'monospace'],
        body: ['"Inter"', 'sans-serif'],
      },
      minHeight: {
        touch: '44px',
      },
      minWidth: {
        touch: '44px',
      },
      animation: {
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite',
        'float': 'float 2s ease-in-out infinite',
        'modal-in': 'modal-in 0.2s ease-out',
      },
      zIndex: {
        'modal': 40,
        'modal-content': 41,
        'toast': 50,
        'tooltip': 60,
      },
    },
  },
  plugins: [],
};
```

## Accessibility Checklist

- [ ] All buttons have visible focus states (`.focus-ring`)
- [ ] Touch targets are ≥44×44px
- [ ] Color contrast ratio ≥4.5:1 for text
- [ ] Animations respect `prefers-reduced-motion`
- [ ] All interactive elements are keyboard accessible
- [ ] Modal traps focus correctly
- [ ] Meaningful alt text for sprites (aria-label)
- [ ] Screen reader announcements for state changes

## Common UI Patterns

### Empty State

```tsx
function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <div className="w-16 h-16 mb-4 opacity-50">
        {/* Placeholder icon */}
      </div>
      <h3 className="font-pixel text-main-white mb-2">{title}</h3>
      <p className="text-secondary-gray text-sm mb-4">{description}</p>
      {action && (
        <Button variant="primary" size="md" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  );
}
```

### Loading State

```tsx
function LoadingState() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="w-8 h-8 border-2 border-neon-cyan border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
```

### Object Grid

```tsx
function ObjectGrid({ objects, onSelect }: ObjectGridProps) {
  return (
    <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-2 p-4">
      {objects.map(obj => (
        <button
          key={obj.id}
          className="aspect-square flex items-center justify-center p-1
                     bg-space-gray rounded hover:bg-border-gray
                     transition-colors focus-ring"
          onClick={() => onSelect(obj)}
        >
          <ObjectSprite object={obj} size={48} />
        </button>
      ))}
    </div>
  );
}
```
