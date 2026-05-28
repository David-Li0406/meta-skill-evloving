# Test Automation Guide

## Setup

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      thresholds: {
        global: {
          branches: 70,
          functions: 70,
          lines: 70,
          statements: 70,
        },
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Test Setup File

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock requestAnimationFrame
global.requestAnimationFrame = vi.fn((cb) => setTimeout(cb, 0));
global.cancelAnimationFrame = vi.fn((id) => clearTimeout(id));
```

## Testing Patterns

### Pure Function Tests

```typescript
// src/lib/game-math.test.ts
import { describe, it, expect } from 'vitest';
import { 
  calculateRTP, 
  calculatePayout, 
  validateBet,
  hexToPixel,
  getHexNeighbors 
} from './game-math';

describe('calculateRTP', () => {
  it('calculates RTP correctly for simple case', () => {
    const outcomes = [
      { probability: 0.4, payout: 2.0 },
      { probability: 0.6, payout: 0 },
    ];
    expect(calculateRTP(outcomes)).toBeCloseTo(0.8, 2);
  });

  it('handles edge case of 100% win rate', () => {
    const outcomes = [{ probability: 1.0, payout: 0.95 }];
    expect(calculateRTP(outcomes)).toBeCloseTo(0.95, 2);
  });

  it('returns 0 for empty outcomes', () => {
    expect(calculateRTP([])).toBe(0);
  });
});

describe('validateBet', () => {
  it('rejects bet exceeding balance', () => {
    expect(validateBet(100, 50)).toEqual({
      valid: false,
      error: 'Insufficient funds',
    });
  });

  it('rejects negative bet', () => {
    expect(validateBet(-10, 100)).toEqual({
      valid: false,
      error: 'Invalid bet amount',
    });
  });

  it('accepts valid bet', () => {
    expect(validateBet(50, 100)).toEqual({ valid: true });
  });
});

describe('hexToPixel', () => {
  it('converts origin hex to center', () => {
    const result = hexToPixel({ q: 0, r: 0 }, 50);
    expect(result).toEqual({ x: 0, y: 0 });
  });

  it('calculates correct offset for adjacent hex', () => {
    const result = hexToPixel({ q: 1, r: 0 }, 50);
    expect(result.x).toBeCloseTo(86.6, 1); // 50 * sqrt(3)
    expect(result.y).toBe(0);
  });
});
```

### Zustand Store Tests

```typescript
// src/stores/gameStore.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { useGameStore } from './gameStore';

describe('gameStore', () => {
  beforeEach(() => {
    // Reset store to initial state
    useGameStore.setState({
      time: { season: 1, day: 1, phase: 'morning' },
      resources: { tulipBulbs: 10, coins: 3000, stamina: 100 },
      score: 0,
    });
  });

  describe('advancePhase', () => {
    it('advances from morning to action', () => {
      useGameStore.getState().advancePhase();
      expect(useGameStore.getState().time.phase).toBe('action');
    });

    it('cycles back to morning after night', () => {
      const store = useGameStore.getState();
      store.advancePhase(); // action
      store.advancePhase(); // resolution
      store.advancePhase(); // night
      store.advancePhase(); // morning
      expect(useGameStore.getState().time.phase).toBe('morning');
    });

    it('increments day after night phase', () => {
      const store = useGameStore.getState();
      store.advancePhase(); // action
      store.advancePhase(); // resolution
      store.advancePhase(); // night
      store.advancePhase(); // morning (next day)
      expect(useGameStore.getState().time.day).toBe(2);
    });
  });

  describe('placeBet', () => {
    it('deducts coins when placing bet', () => {
      useGameStore.getState().placeBet('water', 100);
      expect(useGameStore.getState().resources.coins).toBe(2900);
    });

    it('fails when insufficient coins', () => {
      useGameStore.setState({ resources: { coins: 50 } });
      const result = useGameStore.getState().placeBet('water', 100);
      expect(result.success).toBe(false);
      expect(useGameStore.getState().resources.coins).toBe(50);
    });
  });
});
```

### React Component Tests

```typescript
// src/components/ResourceBar.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ResourceBar } from './ResourceBar';

describe('ResourceBar', () => {
  it('renders label and value', () => {
    render(<ResourceBar label="Coins" value={500} icon="🪙" />);
    
    expect(screen.getByText('Coins')).toBeInTheDocument();
    expect(screen.getByText('500')).toBeInTheDocument();
  });

  it('formats large numbers with commas', () => {
    render(<ResourceBar label="Score" value={1234567} icon="⭐" />);
    
    expect(screen.getByText('1,234,567')).toBeInTheDocument();
  });

  it('shows delta on value increase', async () => {
    const { rerender } = render(
      <ResourceBar label="Coins" value={500} icon="🪙" />
    );
    
    rerender(<ResourceBar label="Coins" value={600} icon="🪙" />);
    
    await waitFor(() => {
      expect(screen.getByText('+100')).toBeInTheDocument();
    });
  });

  it('applies correct color for different resource types', () => {
    const { container } = render(
      <ResourceBar label="Coins" value={500} icon="🪙" color="gold" />
    );
    
    expect(container.firstChild).toHaveClass('gold');
  });
});
```

### Hook Tests

```typescript
// src/hooks/useGameTimer.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useGameTimer } from './useGameTimer';

describe('useGameTimer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('starts paused by default', () => {
    const { result } = renderHook(() => useGameTimer(1000));
    
    expect(result.current.isRunning).toBe(false);
    expect(result.current.timeLeft).toBe(1000);
  });

  it('counts down when started', () => {
    const { result } = renderHook(() => useGameTimer(1000));
    
    act(() => result.current.start());
    
    act(() => vi.advanceTimersByTime(500));
    
    expect(result.current.timeLeft).toBe(500);
  });

  it('calls onComplete when timer reaches 0', () => {
    const onComplete = vi.fn();
    const { result } = renderHook(() => useGameTimer(1000, { onComplete }));
    
    act(() => result.current.start());
    act(() => vi.advanceTimersByTime(1000));
    
    expect(onComplete).toHaveBeenCalledOnce();
  });
});
```

## Playwright E2E Tests

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'bun run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Page Object Pattern

```typescript
// e2e/pages/GamePage.ts
import { Page, Locator } from '@playwright/test';

export class GamePage {
  readonly page: Page;
  readonly hexGrid: Locator;
  readonly advanceButton: Locator;
  readonly scoreDisplay: Locator;
  readonly dayDisplay: Locator;
  readonly phaseDisplay: Locator;
  readonly coinsDisplay: Locator;
  
  constructor(page: Page) {
    this.page = page;
    this.hexGrid = page.getByTestId('hex-grid');
    this.advanceButton = page.getByRole('button', { name: /advance/i });
    this.scoreDisplay = page.getByTestId('score');
    this.dayDisplay = page.getByTestId('day');
    this.phaseDisplay = page.getByTestId('phase');
    this.coinsDisplay = page.getByTestId('coins');
  }

  async goto() {
    await this.page.goto('/game');
  }

  async getHex(q: number, r: number): Promise<Locator> {
    return this.page.getByTestId(`hex-${q}-${r}`);
  }

  async clickHex(q: number, r: number) {
    const hex = await this.getHex(q, r);
    await hex.click();
  }

  async advancePhase() {
    await this.advanceButton.click();
  }

  async getScore(): Promise<number> {
    const text = await this.scoreDisplay.textContent();
    return parseInt(text?.replace(/,/g, '') || '0');
  }

  async placeBet(potType: string, level: 'fold' | 'call' | 'all_in') {
    await this.page.getByTestId(`${potType}-pot`).click();
    await this.page.getByRole('button', { name: level }).click();
  }
}
```

### E2E Test Examples

```typescript
// e2e/game-flow.spec.ts
import { test, expect } from '@playwright/test';
import { GamePage } from './pages/GamePage';

test.describe('Game Flow', () => {
  let gamePage: GamePage;

  test.beforeEach(async ({ page }) => {
    gamePage = new GamePage(page);
    await gamePage.goto();
  });

  test('starts on day 1 morning', async () => {
    await expect(gamePage.dayDisplay).toHaveText('Day 1');
    await expect(gamePage.phaseDisplay).toHaveText('Morning');
  });

  test('can complete full day cycle', async () => {
    // Morning → Action
    await gamePage.advancePhase();
    await expect(gamePage.phaseDisplay).toHaveText('Action');

    // Action → Resolution
    await gamePage.advancePhase();
    await expect(gamePage.phaseDisplay).toHaveText('Resolution');

    // Resolution → Night
    await gamePage.advancePhase();
    await expect(gamePage.phaseDisplay).toHaveText('Night');

    // Night → Morning (Day 2)
    await gamePage.advancePhase();
    await expect(gamePage.phaseDisplay).toHaveText('Morning');
    await expect(gamePage.dayDisplay).toHaveText('Day 2');
  });

  test('betting affects coins', async ({ page }) => {
    const initialCoins = await gamePage.coinsDisplay.textContent();
    
    await gamePage.placeBet('water', 'call');
    
    const newCoins = await gamePage.coinsDisplay.textContent();
    expect(parseInt(newCoins || '0')).toBeLessThan(parseInt(initialCoins || '0'));
  });

  test('hex selection highlights correctly', async () => {
    const hex = await gamePage.getHex(0, 0);
    
    await hex.click();
    
    await expect(hex).toHaveClass(/selected/);
  });
});

test.describe('Mobile', () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test('touch interactions work', async ({ page }) => {
    const gamePage = new GamePage(page);
    await gamePage.goto();
    
    // Touch a hex
    const hex = await gamePage.getHex(0, 0);
    await hex.tap();
    
    await expect(hex).toHaveClass(/selected/);
  });
});
```

## Test Utilities

### Custom Render with Providers

```typescript
// src/test/utils.tsx
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';

// Add any providers your app needs
const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      {children}
    </>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

### Mock Factories

```typescript
// src/test/factories.ts
import { faker } from '@faker-js/faker';

export const createMockPlayer = (overrides = {}) => ({
  id: faker.string.uuid(),
  name: faker.person.firstName(),
  coins: faker.number.int({ min: 100, max: 10000 }),
  tulipBulbs: faker.number.int({ min: 0, max: 50 }),
  level: faker.number.int({ min: 1, max: 100 }),
  ...overrides,
});

export const createMockHex = (overrides = {}) => ({
  q: 0,
  r: 0,
  s: 0,
  state: 'empty',
  tulipType: null,
  growthStage: 0,
  ...overrides,
});

export const createMockGameState = (overrides = {}) => ({
  time: { season: 1, day: 1, phase: 'morning' },
  resources: { tulipBulbs: 10, coins: 3000, stamina: 100 },
  score: 0,
  hexes: new Map(),
  ...overrides,
});
```
