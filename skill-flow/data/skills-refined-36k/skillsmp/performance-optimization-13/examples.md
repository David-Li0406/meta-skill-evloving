# Practical Examples

## Example 1: Optimizing a Dashboard Page

### Before (Slow)

```typescript
// app/dashboard/page.tsx - BEFORE
export default async function DashboardPage() {
  const { userId } = await auth();

  // Sequential fetches (waterfall)
  const user = await getUser(userId);
  const budgets = await getBudgets(userId);
  const expenses = await getRecentExpenses(userId);
  const stats = await calculateStats(userId);

  return (
    <div>
      <WelcomeHeader user={user} />
      <StatsCards stats={stats} />
      <BudgetList budgets={budgets} />
      <ExpenseList expenses={expenses} />
    </div>
  );
}
```

### After (Optimized)

```typescript
// app/dashboard/page.tsx - AFTER
import { Suspense } from "react";

export default async function DashboardPage() {
  const { userId } = await auth();

  // Parallel fetch for critical data
  const [user, stats] = await Promise.all([
    getUser(userId),
    calculateStats(userId)
  ]);

  return (
    <div>
      {/* Immediate render */}
      <WelcomeHeader user={user} />
      <StatsCards stats={stats} />

      {/* Streamed components */}
      <Suspense fallback={<BudgetListSkeleton />}>
        <BudgetList userId={userId} />
      </Suspense>

      <Suspense fallback={<ExpenseListSkeleton />}>
        <ExpenseList userId={userId} />
      </Suspense>
    </div>
  );
}

// Separate async components
async function BudgetList({ userId }: { userId: string }) {
  const [, budgets] = await getBudgets(userId);
  return <BudgetCards budgets={budgets} />;
}

async function ExpenseList({ userId }: { userId: string }) {
  const [, expenses] = await getRecentExpenses(userId);
  return <ExpenseTable expenses={expenses} />;
}
```

## Example 2: Virtualized List

### Before (Performance Issues)

```typescript
// components/expense-list.tsx - BEFORE
function ExpenseList({ expenses }: { expenses: Expense[] }) {
  return (
    <div className="h-[600px] overflow-auto">
      {expenses.map(expense => (
        <ExpenseRow key={expense.id} expense={expense} />
      ))}
    </div>
  );
}
// Problem: Renders 500+ items, causes scroll lag
```

### After (Virtualized)

```typescript
// components/expense-list.tsx - AFTER
"use client";

import { useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";

function ExpenseList({ expenses }: { expenses: Expense[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: expenses.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 64,  // Row height
    overscan: 10
  });

  return (
    <div
      ref={parentRef}
      className="h-[600px] overflow-auto"
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: "100%",
          position: "relative"
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => {
          const expense = expenses[virtualRow.index];
          return (
            <div
              key={expense.id}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`
              }}
            >
              <ExpenseRow expense={expense} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

## Example 3: Bundle Size Optimization

### Before (Large Bundle)

```typescript
// Heavy imports
import _ from "lodash";
import moment from "moment";
import { Chart } from "chart.js/auto";

export function AnalyticsDashboard({ data }) {
  const sorted = _.sortBy(data, "date");
  const formatted = sorted.map(d => ({
    ...d,
    date: moment(d.date).format("MMM DD")
  }));

  return <Chart data={formatted} />;
}
```

### After (Optimized)

```typescript
// Tree-shakeable and lighter imports
import { sortBy } from "lodash-es";
import { format } from "date-fns";
import dynamic from "next/dynamic";

// Dynamic import for heavy chart library
const Chart = dynamic(
  () => import("./Chart").then(mod => mod.Chart),
  {
    loading: () => <ChartSkeleton />,
    ssr: false
  }
);

export function AnalyticsDashboard({ data }) {
  // Native sort (even lighter)
  const sorted = [...data].sort((a, b) =>
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const formatted = sorted.map(d => ({
    ...d,
    date: format(new Date(d.date), "MMM dd")
  }));

  return <Chart data={formatted} />;
}
```

## Example 4: Search with Debouncing

### Before (Too Many Requests)

```typescript
// components/search.tsx - BEFORE
function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  // Fires on every keystroke!
  useEffect(() => {
    searchAPI(query).then(setResults);
  }, [query]);

  return (
    <input
      value={query}
      onChange={e => setQuery(e.target.value)}
    />
  );
}
```

### After (Debounced + Deferred)

```typescript
// components/search.tsx - AFTER
"use client";

import { useState, useDeferredValue, useEffect } from "react";

function Search() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (!deferredQuery) {
      setResults([]);
      return;
    }

    const controller = new AbortController();
    setIsSearching(true);

    searchAPI(deferredQuery, { signal: controller.signal })
      .then(setResults)
      .catch(err => {
        if (err.name !== "AbortError") console.error(err);
      })
      .finally(() => setIsSearching(false));

    return () => controller.abort();
  }, [deferredQuery]);

  const isStale = query !== deferredQuery;

  return (
    <div>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search..."
      />
      {(isSearching || isStale) && <LoadingSpinner />}
      <ResultsList results={results} />
    </div>
  );
}
```

## Example 5: Image Optimization

### Before (Unoptimized)

```typescript
// BEFORE
function ProductCard({ product }) {
  return (
    <div>
      <img src={product.imageUrl} alt={product.name} />
      <h3>{product.name}</h3>
    </div>
  );
}
```

### After (Optimized)

```typescript
// AFTER
import Image from "next/image";

function ProductCard({ product }) {
  return (
    <div className="relative">
      <Image
        src={product.imageUrl}
        alt={product.name}
        width={300}
        height={200}
        className="object-cover"
        sizes="(max-width: 768px) 100vw, 300px"
        placeholder="blur"
        blurDataURL={product.blurDataUrl}  // Pre-generated tiny placeholder
      />
      <h3>{product.name}</h3>
    </div>
  );
}

// For hero images (LCP)
function HeroImage() {
  return (
    <Image
      src="/hero.webp"
      alt="Hero"
      width={1200}
      height={600}
      priority  // Preload for LCP
      quality={85}
    />
  );
}
```

## Example 6: Context Optimization

### Before (All Consumers Re-render)

```typescript
// BEFORE - Single context, everything re-renders
const AppContext = createContext({
  user: null,
  theme: "light",
  locale: "en",
  notifications: []
});

function App() {
  const [state, setState] = useState(initialState);

  // Any change re-renders ALL consumers
  return (
    <AppContext.Provider value={{ ...state, setState }}>
      <Children />
    </AppContext.Provider>
  );
}
```

### After (Split by Update Frequency)

```typescript
// AFTER - Split contexts
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<Theme>("light");
const NotificationsContext = createContext<Notification[]>([]);

// Memoize values that change together
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<Theme>("light");

  const value = useMemo(() => ({
    theme,
    setTheme,
    isDark: theme === "dark"
  }), [theme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// Notifications change frequently - isolated
function NotificationsProvider({ children }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const value = useMemo(() => ({
    notifications,
    addNotification: (n: Notification) => setNotifications(prev => [...prev, n]),
    clearNotifications: () => setNotifications([])
  }), [notifications]);

  return (
    <NotificationsContext.Provider value={value}>
      {children}
    </NotificationsContext.Provider>
  );
}

// Compose providers
function Providers({ children }) {
  return (
    <UserProvider>
      <ThemeProvider>
        <NotificationsProvider>
          {children}
        </NotificationsProvider>
      </ThemeProvider>
    </UserProvider>
  );
}
```

## Example 7: Database Query Optimization

### Before (N+1 Problem)

```typescript
// BEFORE - N+1 queries
async function getBudgetsWithExpenses(userId: string) {
  const [, budgets] = await getBudgets(userId);

  // N additional queries!
  const budgetsWithExpenses = await Promise.all(
    budgets.map(async (budget) => ({
      ...budget,
      expenses: await getExpensesByBudget(budget.id)
    }))
  );

  return budgetsWithExpenses;
}
```

### After (Batch Query)

```typescript
// AFTER - 2 queries total
async function getBudgetsWithExpenses(userId: string) {
  // Query 1: Get budgets
  const [, budgets] = await getBudgets(userId);

  if (budgets.length === 0) return [];

  // Query 2: Get all expenses for all budgets
  const budgetIds = budgets.map(b => b.id);

  // Firestore "in" query (max 30 items)
  const expensesSnapshot = await db.collection("expenses")
    .where("budgetId", "in", budgetIds.slice(0, 30))
    .orderBy("date", "desc")
    .get();

  // Group expenses by budget
  const expensesByBudget = new Map<string, Expense[]>();
  expensesSnapshot.docs.forEach(doc => {
    const expense = transformExpense(doc);
    const existing = expensesByBudget.get(expense.budgetId) || [];
    expensesByBudget.set(expense.budgetId, [...existing, expense]);
  });

  // Combine
  return budgets.map(budget => ({
    ...budget,
    expenses: expensesByBudget.get(budget.id) || []
  }));
}
```

## Example 8: Skeleton Loaders (CLS Prevention)

```typescript
// Skeleton that matches final layout
function BudgetCardSkeleton() {
  return (
    <div className="p-4 border rounded-lg animate-pulse">
      <div className="h-6 w-1/2 bg-muted rounded mb-2" />
      <div className="h-4 w-1/4 bg-muted rounded mb-4" />
      <div className="h-8 w-full bg-muted rounded" />
    </div>
  );
}

function BudgetListSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: 6 }).map((_, i) => (
        <BudgetCardSkeleton key={i} />
      ))}
    </div>
  );
}

// Usage with Suspense
export default function BudgetsPage() {
  return (
    <div>
      <h1>Budgets</h1>
      <Suspense fallback={<BudgetListSkeleton />}>
        <BudgetList />
      </Suspense>
    </div>
  );
}
```
