---
title: Defer Non-Critical Third-Party Scripts
impact: MEDIUM
impactDescription: Loads analytics/tracking after hydration for faster TTI
tags: bundle, defer, third-party, analytics, performance
---

## Defer Non-Critical Third-Party Scripts

Analytics, error tracking, chat widgets, and other non-critical third-party scripts don't need to block initial render. Use `@defer` to load them after hydration completes.

**Incorrect (blocks initial bundle):**

```typescript
// ❌ Analytics component loads in main bundle
import { AnalyticsComponent } from './analytics.component';
import { ChatWidgetComponent } from './chat-widget.component';
import { ErrorTrackingComponent } from './error-tracking.component';

@Component({
  selector: 'app-root',
  template: `
    <app-header />
    <router-outlet />
    <app-footer />

    <!-- These load immediately, blocking TTI -->
    <app-analytics />
    <app-chat-widget />
    <app-error-tracking />
  `,
  imports: [
    AnalyticsComponent,      // Included in main bundle
    ChatWidgetComponent,     // Included in main bundle
    ErrorTrackingComponent   // Included in main bundle
  ]
})
export class AppComponent {}
```

**Correct (defer with @defer):**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <app-header />
    <router-outlet />
    <app-footer />

    <!-- ✅ Loads AFTER hydration completes -->
    @defer (on idle) {
      <app-analytics />
    }

    @defer (on idle) {
      <app-chat-widget />
    }

    @defer (on idle) {
      <app-error-tracking />
    }
  `,
  imports: [HeaderComponent, FooterComponent]
  // Analytics, ChatWidget, ErrorTracking NOT in imports - loaded dynamically
})
export class AppComponent {}
```

**With timer delay:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <router-outlet />

    <!-- Load after 3 seconds idle time -->
    @defer (on idle; when isHydrated) {
      <app-analytics />
      <app-intercom-chat />
    } @placeholder {
      <!-- Nothing shown while waiting -->
    }
  `
})
export class AppComponent {
  isHydrated = signal(false);

  constructor() {
    afterNextRender(() => {
      this.isHydrated.set(true);
    });
  }
}
```

**For heavy libraries (charts, maps):**

```typescript
@Component({
  selector: 'app-dashboard',
  template: `
    <div class="metrics">
      <app-kpi-cards [data]="kpiData()" />
    </div>

    <!-- Heavy chart library deferred until visible -->
    @defer (on viewport) {
      <app-revenue-chart [data]="chartData()" />
    } @placeholder {
      <div class="chart-skeleton">
        <div class="skeleton-bar"></div>
      </div>
    } @loading (minimum 200ms) {
      <app-spinner />
    }

    <!-- Map only loads when user scrolls to it -->
    @defer (on viewport) {
      <app-location-map [markers]="locations()" />
    } @placeholder {
      <div class="map-placeholder">
        <img src="assets/map-preview.webp" alt="Map preview" />
      </div>
    }
  `
})
export class DashboardComponent {}
```

**Third-party script loading pattern:**

```typescript
// Service to load third-party scripts on demand
@Injectable({ providedIn: 'root' })
export class ThirdPartyService {
  private loaded = new Map<string, Promise<void>>();

  loadScript(src: string): Promise<void> {
    if (this.loaded.has(src)) {
      return this.loaded.get(src)!;
    }

    const promise = new Promise<void>((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Failed to load ${src}`));
      document.body.appendChild(script);
    });

    this.loaded.set(src, promise);
    return promise;
  }
}

// Analytics component that loads external script
@Component({
  selector: 'app-analytics',
  template: ``,
  standalone: true
})
export class AnalyticsComponent {
  private thirdParty = inject(ThirdPartyService);

  constructor() {
    afterNextRender(async () => {
      await this.thirdParty.loadScript('https://analytics.example.com/script.js');
      window.analytics?.init({ key: environment.analyticsKey });
    });
  }
}
```

**SSR hydration-aware loading:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <router-outlet />

    <!-- Only load on client, after hydration -->
    @defer (on idle; hydrate never) {
      <app-client-only-widget />
    }

    <!-- Prefetch during idle, hydrate on interaction -->
    @defer (on interaction; prefetch on idle; hydrate on interaction) {
      <app-feedback-widget />
    }
  `
})
export class AppComponent {}
```

**Priority guidelines:**

| Third-party | Priority | Defer Strategy |
|-------------|----------|----------------|
| Analytics | Low | `@defer (on idle)` after 2-3s |
| Error tracking | Low | `@defer (on idle)` |
| Chat widget | Low | `@defer (on idle)` or `(on viewport)` |
| Social embeds | Low | `@defer (on viewport)` |
| Maps | Medium | `@defer (on viewport)` |
| Video players | Medium | `@defer (on viewport)` |
| A/B testing | High | Load in main bundle (affects content) |
| Auth providers | High | Load in main bundle (blocks UX) |

**Why it matters:**
- Third-party scripts often add 100KB+ to initial bundle
- Analytics don't affect user experience - defer them
- Faster Time to Interactive (TTI) improves Core Web Vitals
- Users can interact sooner with the critical UI

Reference: [Angular Deferrable Views](https://angular.dev/guide/defer)
