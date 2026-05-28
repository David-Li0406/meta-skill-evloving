# Example: Dashboard Components Decomposition

## User Request
"Build an analytics dashboard with charts and filters"

## Decomposition Output

### Task Analysis
- Multiple independent UI components
- Shared data fetching layer
- Filter state management

### Tasks

```
Task 1: Create Dashboard Types
- Depends on: none
- Files: types/analytics.ts
- Done when: Types for metrics, charts, filters defined
- Complexity: S

Task 2: Create Data Fetching Hooks
- Depends on: [Task 1]
- Files: hooks/useAnalytics.ts
- Done when: Hook fetches and caches analytics data
- Complexity: M

Task 3: Create Line Chart Component
- Depends on: [Task 1]
- Files: components/charts/LineChart.tsx
- Done when: Component renders time series data
- Complexity: M

Task 4: Create Bar Chart Component
- Depends on: [Task 1]
- Files: components/charts/BarChart.tsx
- Done when: Component renders categorical data
- Complexity: M

Task 5: Create Pie Chart Component
- Depends on: [Task 1]
- Files: components/charts/PieChart.tsx
- Done when: Component renders proportional data
- Complexity: M

Task 6: Create Date Range Filter
- Depends on: none
- Files: components/filters/DateRangeFilter.tsx
- Done when: Filter emits date range selections
- Complexity: S

Task 7: Create Category Filter
- Depends on: none
- Files: components/filters/CategoryFilter.tsx
- Done when: Filter emits category selections
- Complexity: S

Task 8: Create Dashboard Layout
- Depends on: [Task 2, Task 3, Task 4, Task 5, Task 6, Task 7]
- Files: app/dashboard/page.tsx
- Done when: Dashboard assembles all components
- Complexity: L
```

### Execution Strategy

```
Group 1 (Parallel - foundation):
  ├── Task 1: Create Dashboard Types
  ├── Task 6: Create Date Range Filter
  └── Task 7: Create Category Filter

Group 2 (Parallel - depends on Types):
  ├── Task 2: Create Data Fetching Hooks
  ├── Task 3: Create Line Chart Component
  ├── Task 4: Create Bar Chart Component
  └── Task 5: Create Pie Chart Component

Group 3 (Sequential - integration):
  └── Task 8: Create Dashboard Layout
```

### Parallelization Decision

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ Parallelization: ENABLED                                 │
│    Reason: 7 independent components detected                │
│    Strategy: 3 groups (2 parallel, 1 sequential)            │
│    Estimated speedup: 2.5x                                  │
└─────────────────────────────────────────────────────────────┘
```
