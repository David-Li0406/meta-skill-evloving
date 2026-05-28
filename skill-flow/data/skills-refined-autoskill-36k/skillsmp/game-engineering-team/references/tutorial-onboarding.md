# Tutorial & Onboarding Reference

## First Five Minutes Design

| Minute | Goal | Approach |
|--------|------|----------|
| 0-1 | Hook | Visual delight, first interaction in 10 seconds |
| 1-2 | Core Loop Taste | Simplified mechanic, guaranteed success |
| 2-4 | Ownership | Name something, make a choice |
| 4-5 | Breadcrumb | Hint at depth, clear next objective |

## Tutorial State Machine

```typescript
interface TutorialStep {
  state: string;
  canSkip: boolean;
  highlight?: string;       // CSS selector
  requiredAction?: string;  // Action to progress
  autoProgress?: number;    // Auto-advance ms
}

class TutorialStateMachine {
  private currentIndex = 0;
  
  constructor(private steps: TutorialStep[], private onStateChange: (s: TutorialStep) => void) {}
  
  handleAction(action: string): void {
    if (this.current.requiredAction === action) this.advance();
  }
  
  advance(): void {
    if (this.currentIndex < this.steps.length - 1) {
      this.currentIndex++;
      this.onStateChange(this.current);
    }
  }
  
  get current() { return this.steps[this.currentIndex]; }
}
```

## Contextual Help

```typescript
interface HelpTooltip {
  id: string;
  target: string;
  content: string;
  triggerOn: 'hover' | 'first-view' | 'confusion';
  confusionThreshold?: number; // Seconds
}

function setupConfusionTrigger(tooltip: HelpTooltip, show: () => void) {
  let timer: number;
  const reset = () => {
    clearTimeout(timer);
    timer = window.setTimeout(show, (tooltip.confusionThreshold || 15) * 1000);
  };
  document.addEventListener('click', reset);
  reset();
}
```

## Progressive Feature Unlocks

```typescript
interface FeatureGate {
  featureId: string;
  name: string;
  unlockCondition: { type: 'level' | 'day' | 'season'; value: number };
  tutorialOnUnlock?: string;
}

const FEATURE_GATES: FeatureGate[] = [
  { featureId: 'betting', name: 'Betting', unlockCondition: { type: 'day', value: 1 } },
  { featureId: 'combos', name: 'Combo Hands', unlockCondition: { type: 'day', value: 3 } },
  { featureId: 'abilities', name: 'Simulin Abilities', unlockCondition: { type: 'level', value: 5 } },
  { featureId: 'market', name: 'Tulip Market', unlockCondition: { type: 'season', value: 2 } },
];
```

## Smart Hints

```typescript
interface HintRule {
  id: string;
  condition: (ctx: GameContext) => boolean;
  message: string;
  cooldown: number;
}

const HINT_RULES: HintRule[] = [
  { id: 'low_coins', condition: ctx => ctx.coins < 50, message: 'Try "Call" for safer bets', cooldown: 300000 },
  { id: 'unused_ability', condition: ctx => ctx.abilityReady, message: 'Tap Simulin to use ability!', cooldown: 120000 },
];
```

## Tutorial Analytics

```typescript
interface TutorialMetrics {
  stepCompletionRates: Record<string, number>;
  averageDuration: number;
  dropoffPoints: string[];
}

// Track: step_started, step_completed, step_skipped, tutorial_abandoned
```

---

*Tutorial & Onboarding Reference - Game Engineering Team*
