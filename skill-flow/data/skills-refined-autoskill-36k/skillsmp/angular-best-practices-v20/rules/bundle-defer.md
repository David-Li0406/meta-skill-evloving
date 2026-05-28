---
title: Use @defer for Lazy Loading Components
impact: CRITICAL
impactDescription: Defers loading until needed, reduces initial bundle
tags: defer, lazy-loading, template
---

## Use @defer for Lazy Loading Components

`@defer` delays loading of heavy components until a trigger condition is met, reducing initial bundle size without route changes.

**Incorrect (Heavy components loaded immediately):**

```typescript
@Component({
  selector: 'app-dashboard',
  imports: [HeavyChartComponent, DataTableComponent],
  template: `
    <h1>Dashboard</h1>

    <!-- Chart library loaded even if user never scrolls down -->
    <app-heavy-chart [data]="chartData" />

    <!-- Large table always in initial bundle -->
    <app-data-table [rows]="tableData" />
  `
})
export class DashboardComponent {}
```

**Correct (Defer loading until needed):**

```typescript
@Component({
  selector: 'app-dashboard',
  imports: [HeavyChartComponent, DataTableComponent],
  template: `
    <h1>Dashboard</h1>

    @defer (on viewport) {
      <app-heavy-chart [data]="chartData" />
    } @placeholder {
      <div class="chart-skeleton">Loading chart...</div>
    }

    @defer (on interaction) {
      <app-data-table [rows]="tableData" />
    } @placeholder {
      <button>Click to load data table</button>
    }
  `
})
export class DashboardComponent {}
```

**Why it matters:**
- `on viewport` - Loads when element enters viewport (scroll-triggered)
- `on interaction` - Loads on click/focus (user-triggered)
- `on idle` - Loads when browser is idle (background loading)
- `@placeholder` shows fallback content until loaded

Reference: [Angular Defer](https://angular.dev/guide/defer)
