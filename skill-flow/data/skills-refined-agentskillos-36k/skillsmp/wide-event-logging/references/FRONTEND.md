# Frontend Wide Event Patterns

Wide event patterns for frontend applications: page views, interactions,
performance metrics, and error tracking.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Session and User Context](#session-and-user-context)
- [Page View Events](#page-view-events)
- [Interaction Events](#interaction-events)
- [Performance Metrics](#performance-metrics)
- [Error Tracking](#error-tracking)
- [React Integration](#react-integration)
- [Batching and Transport](#batching-and-transport)

## Core Concepts

Frontend wide events differ from backend:

- **Session-scoped**: Events share session context across page views
- **Batched**: Events are queued and sent periodically to reduce requests
- **Best-effort**: Network failures shouldn't block user experience
- **Privacy-aware**: Never log PII in frontend events

## Session and User Context

### Context Manager

```typescript
interface FrontendContext {
  // Session (persists across page views)
  session_id: string;
  session_start: string;
  session_page_views: number;

  // User (when authenticated)
  user_id?: string;
  user_subscription?: string;

  // Device
  device_type: "mobile" | "tablet" | "desktop";
  viewport_width: number;
  viewport_height: number;
  user_agent: string;
  locale: string;
  timezone: string;

  // App
  app_version: string;
  feature_flags: Record<string, boolean>;

  // Page (changes on navigation)
  page_path: string;
  page_title: string;
  referrer: string;
}

class ContextManager {
  private context: FrontendContext;

  constructor() {
    this.context = this.initContext();
  }

  private initContext(): FrontendContext {
    const sessionId =
      sessionStorage.getItem("session_id") || crypto.randomUUID();
    sessionStorage.setItem("session_id", sessionId);

    return {
      session_id: sessionId,
      session_start:
        sessionStorage.getItem("session_start") || new Date().toISOString(),
      session_page_views: parseInt(sessionStorage.getItem("page_views") || "0"),
      device_type: this.getDeviceType(),
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
      user_agent: navigator.userAgent,
      locale: navigator.language,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      app_version: process.env.NEXT_PUBLIC_VERSION || "unknown",
      feature_flags: window.__FEATURE_FLAGS__ || {},
      page_path: window.location.pathname,
      page_title: document.title,
      referrer: document.referrer,
    };
  }

  private getDeviceType(): "mobile" | "tablet" | "desktop" {
    const width = window.innerWidth;
    if (width < 768) return "mobile";
    if (width < 1024) return "tablet";
    return "desktop";
  }

  setUser(user: { id: string; subscription?: string }) {
    this.context.user_id = user.id;
    this.context.user_subscription = user.subscription;
  }

  updatePage(path: string, title: string) {
    this.context.page_path = path;
    this.context.page_title = title;
    this.context.session_page_views++;
    sessionStorage.setItem(
      "page_views",
      String(this.context.session_page_views),
    );
  }

  getContext(): FrontendContext {
    return { ...this.context };
  }
}

export const contextManager = new ContextManager();
```

## Page View Events

### Basic Page View

```typescript
interface PageViewEvent {
  event_type: "page_view";
  timestamp: string;

  // Page context
  page_path: string;
  page_title: string;
  page_referrer: string;
  page_load_id: string;

  // Navigation
  navigation_type: "initial" | "client" | "back_forward" | "reload";
  previous_page?: string;

  // Session context (from ContextManager)
  session_id: string;
  session_page_views: number;
  user_id?: string;

  // Performance (added after load)
  ttfb_ms?: number;
  fcp_ms?: number;
  lcp_ms?: number;
  dom_interactive_ms?: number;
}

function trackPageView(navigationSource: string = "initial") {
  const ctx = contextManager.getContext();
  const pageLoadId = crypto.randomUUID();

  const event: PageViewEvent = {
    event_type: "page_view",
    timestamp: new Date().toISOString(),
    page_path: ctx.page_path,
    page_title: ctx.page_title,
    page_referrer: ctx.referrer,
    page_load_id: pageLoadId,
    navigation_type: getNavigationType(),
    session_id: ctx.session_id,
    session_page_views: ctx.session_page_views,
    user_id: ctx.user_id,
  };

  // Send immediately
  sendEvent(event);

  // Add performance metrics after load
  if (typeof PerformanceObserver !== "undefined") {
    observeWebVitals(pageLoadId);
  }
}

function getNavigationType(): PageViewEvent["navigation_type"] {
  const nav = performance.getEntriesByType(
    "navigation",
  )[0] as PerformanceNavigationTiming;
  if (!nav) return "initial";

  switch (nav.type) {
    case "navigate":
      return "initial";
    case "reload":
      return "reload";
    case "back_forward":
      return "back_forward";
    default:
      return "client";
  }
}
```

### SPA Navigation Tracking

```typescript
// React Router integration
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

export function usePageTracking() {
  const location = useLocation();

  useEffect(() => {
    contextManager.updatePage(location.pathname, document.title);
    trackPageView("client");
  }, [location.pathname]);
}

// Next.js App Router
("use client");
import { usePathname } from "next/navigation";
import { useEffect } from "react";

export function PageTracker() {
  const pathname = usePathname();

  useEffect(() => {
    contextManager.updatePage(pathname, document.title);
    trackPageView("client");
  }, [pathname]);

  return null;
}
```

## Interaction Events

### Click Tracking

```typescript
interface InteractionEvent {
  event_type: "click" | "form_submit" | "scroll" | "focus";
  timestamp: string;

  // Element context
  element_tag: string;
  element_id?: string;
  element_class?: string;
  element_text?: string; // Truncated, no PII
  element_href?: string;
  element_data_track?: string; // data-track attribute

  // Position
  click_x?: number;
  click_y?: number;
  viewport_x?: number;
  viewport_y?: number;

  // Page context
  page_path: string;
  page_load_id: string;
  time_on_page_ms: number;

  // Session
  session_id: string;
  user_id?: string;
}

function trackClick(event: MouseEvent) {
  const target = event.target as HTMLElement;
  const trackable = target.closest("[data-track]");

  if (!trackable) return; // Only track elements with data-track

  const ctx = contextManager.getContext();

  const clickEvent: InteractionEvent = {
    event_type: "click",
    timestamp: new Date().toISOString(),
    element_tag: trackable.tagName.toLowerCase(),
    element_id: trackable.id || undefined,
    element_class: trackable.className || undefined,
    element_text: truncate(trackable.textContent, 50),
    element_href: (trackable as HTMLAnchorElement).href,
    element_data_track: trackable.getAttribute("data-track"),
    click_x: event.clientX,
    click_y: event.clientY,
    viewport_x: event.pageX,
    viewport_y: event.pageY,
    page_path: ctx.page_path,
    page_load_id: getCurrentPageLoadId(),
    time_on_page_ms: performance.now(),
    session_id: ctx.session_id,
    user_id: ctx.user_id,
  };

  sendEvent(clickEvent);
}

// Initialize
document.addEventListener("click", trackClick, { capture: true });
```

### Form Submission Tracking

```typescript
interface FormSubmitEvent {
  event_type: "form_submit";
  timestamp: string;

  // Form context
  form_id?: string;
  form_name?: string;
  form_action?: string;
  form_method?: string;
  field_count: number;
  filled_field_count: number;

  // Timing
  time_to_submit_ms: number;
  time_on_page_ms: number;

  // Validation
  had_validation_errors: boolean;
  validation_error_fields?: string[];

  // Result (if async)
  submit_result?: "success" | "error";
  error_message?: string;

  // Context
  page_path: string;
  session_id: string;
  user_id?: string;
}

function trackFormSubmit(
  form: HTMLFormElement,
  result?: { success: boolean; error?: string },
) {
  const ctx = contextManager.getContext();
  const fields = form.querySelectorAll("input, textarea, select");
  const filledFields = Array.from(fields).filter(
    (f: HTMLInputElement) => f.value,
  );

  const event: FormSubmitEvent = {
    event_type: "form_submit",
    timestamp: new Date().toISOString(),
    form_id: form.id || undefined,
    form_name: form.name || undefined,
    form_action: form.action,
    form_method: form.method,
    field_count: fields.length,
    filled_field_count: filledFields.length,
    time_to_submit_ms: getFormFocusTime(form),
    time_on_page_ms: performance.now(),
    had_validation_errors: !form.checkValidity(),
    page_path: ctx.page_path,
    session_id: ctx.session_id,
    user_id: ctx.user_id,
  };

  if (result) {
    event.submit_result = result.success ? "success" : "error";
    event.error_message = result.error;
  }

  sendEvent(event);
}
```

## Performance Metrics

### Core Web Vitals

```typescript
interface PerformanceEvent {
  event_type: "performance";
  timestamp: string;
  page_load_id: string;
  page_path: string;

  // Core Web Vitals
  lcp_ms?: number; // Largest Contentful Paint
  fid_ms?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  inp_ms?: number; // Interaction to Next Paint

  // Additional metrics
  ttfb_ms?: number; // Time to First Byte
  fcp_ms?: number; // First Contentful Paint
  dom_interactive_ms?: number;
  dom_complete_ms?: number;
  load_complete_ms?: number;

  // Resource metrics
  resource_count?: number;
  transfer_size_bytes?: number;
  js_heap_size_bytes?: number;

  // Context
  connection_type?: string;
  device_memory_gb?: number;
  hardware_concurrency?: number;
}

function observeWebVitals(pageLoadId: string) {
  const metrics: Partial<PerformanceEvent> = {
    event_type: "performance",
    page_load_id: pageLoadId,
    page_path: window.location.pathname,
  };

  // LCP
  new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lastEntry = entries[entries.length - 1];
    metrics.lcp_ms = Math.round(lastEntry.startTime);
  }).observe({ type: "largest-contentful-paint", buffered: true });

  // FID
  new PerformanceObserver((list) => {
    const entry = list.getEntries()[0];
    metrics.fid_ms = Math.round(entry.processingStart - entry.startTime);
  }).observe({ type: "first-input", buffered: true });

  // CLS
  let clsValue = 0;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) {
        clsValue += entry.value;
      }
    }
    metrics.cls = Math.round(clsValue * 1000) / 1000;
  }).observe({ type: "layout-shift", buffered: true });

  // Send after page is fully loaded
  window.addEventListener("load", () => {
    setTimeout(() => {
      metrics.timestamp = new Date().toISOString();
      addNavigationTiming(metrics);
      addResourceMetrics(metrics);
      addDeviceMetrics(metrics);
      sendEvent(metrics as PerformanceEvent);
    }, 3000); // Wait for CLS to stabilize
  });
}

function addNavigationTiming(metrics: Partial<PerformanceEvent>) {
  const nav = performance.getEntriesByType(
    "navigation",
  )[0] as PerformanceNavigationTiming;
  if (nav) {
    metrics.ttfb_ms = Math.round(nav.responseStart);
    metrics.fcp_ms = Math.round(nav.domContentLoadedEventStart);
    metrics.dom_interactive_ms = Math.round(nav.domInteractive);
    metrics.dom_complete_ms = Math.round(nav.domComplete);
    metrics.load_complete_ms = Math.round(nav.loadEventEnd);
  }
}

function addDeviceMetrics(metrics: Partial<PerformanceEvent>) {
  const nav = navigator as any;
  metrics.connection_type = nav.connection?.effectiveType;
  metrics.device_memory_gb = nav.deviceMemory;
  metrics.hardware_concurrency = nav.hardwareConcurrency;

  if (performance.memory) {
    metrics.js_heap_size_bytes = (performance as any).memory.usedJSHeapSize;
  }
}
```

## Error Tracking

### Global Error Handler

```typescript
interface ErrorEvent {
  event_type: "error";
  timestamp: string;

  // Error details
  error_type: string;
  error_message: string;
  error_stack?: string;
  error_source: "runtime" | "promise" | "network" | "react";

  // Context
  component_name?: string;
  component_stack?: string;
  action_name?: string;

  // Page context
  page_path: string;
  page_load_id: string;
  time_on_page_ms: number;

  // User journey
  last_interaction?: string;
  interaction_count: number;

  // Session
  session_id: string;
  user_id?: string;
  user_subscription?: string;
}

function trackError(
  error: Error,
  source: ErrorEvent["error_source"],
  extra?: Partial<ErrorEvent>,
) {
  const ctx = contextManager.getContext();

  const event: ErrorEvent = {
    event_type: "error",
    timestamp: new Date().toISOString(),
    error_type: error.name,
    error_message: error.message,
    error_stack: sanitizeStack(error.stack),
    error_source: source,
    page_path: ctx.page_path,
    page_load_id: getCurrentPageLoadId(),
    time_on_page_ms: performance.now(),
    interaction_count: getInteractionCount(),
    session_id: ctx.session_id,
    user_id: ctx.user_id,
    user_subscription: ctx.user_subscription,
    ...extra,
  };

  // Errors are never sampled
  sendEvent(event, { priority: "high" });
}

// Global handlers
window.onerror = (message, source, line, col, error) => {
  trackError(error || new Error(String(message)), "runtime");
};

window.onunhandledrejection = (event) => {
  trackError(
    event.reason instanceof Error
      ? event.reason
      : new Error(String(event.reason)),
    "promise",
  );
};
```

## React Integration

### Error Boundary

```tsx
interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class TrackedErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    trackError(error, "react", {
      component_name: this.constructor.name,
      component_stack: errorInfo.componentStack,
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}
```

### Tracking Hook

```tsx
export function useTrackedAction<T>(
  actionName: string,
  action: () => Promise<T>,
): [() => Promise<T>, boolean, Error | null] {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = async () => {
    setLoading(true);
    setError(null);
    const start = performance.now();

    try {
      const result = await action();

      sendEvent({
        event_type: "action",
        action_name: actionName,
        action_result: "success",
        duration_ms: performance.now() - start,
        ...contextManager.getContext(),
      });

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);

      trackError(error, "runtime", { action_name: actionName });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return [execute, loading, error];
}
```

## Batching and Transport

### Event Queue

```typescript
class EventQueue {
  private queue: unknown[] = [];
  private flushTimer: number | null = null;
  private readonly endpoint: string;
  private readonly batchSize = 10;
  private readonly flushInterval = 5000;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
    this.setupFlush();
    this.setupBeforeUnload();
  }

  add(event: unknown, options?: { priority?: "high" }) {
    this.queue.push(event);

    if (options?.priority === "high" || this.queue.length >= this.batchSize) {
      this.flush();
    }
  }

  private setupFlush() {
    this.flushTimer = window.setInterval(
      () => this.flush(),
      this.flushInterval,
    );
  }

  private setupBeforeUnload() {
    window.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") {
        this.flush({ useBeacon: true });
      }
    });
  }

  private flush(options?: { useBeacon?: boolean }) {
    if (this.queue.length === 0) return;

    const events = this.queue.splice(0, this.batchSize);
    const payload = JSON.stringify({ events });

    if (options?.useBeacon && navigator.sendBeacon) {
      navigator.sendBeacon(this.endpoint, payload);
    } else {
      fetch(this.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        keepalive: true,
      }).catch(() => {
        // Re-queue on failure (with limit)
        if (this.queue.length < 100) {
          this.queue.unshift(...events);
        }
      });
    }
  }
}

const eventQueue = new EventQueue("/api/events");

export function sendEvent(event: unknown, options?: { priority?: "high" }) {
  eventQueue.add(event, options);
}
```
