# Sections (Angular 20+)

This file defines all sections for Angular 20+ with modern features like Signals, @defer, and new control flow syntax.

---

## 1. Change Detection (change)

**Impact:** CRITICAL
**Description:** Change detection is the #1 performance factor in Angular. Using OnPush strategy, Signals, and proper zone management can dramatically reduce unnecessary checks.

## 2. Bundle & Lazy Loading (bundle)

**Impact:** CRITICAL
**Description:** Standalone components, @defer blocks, and lazy loading improve Time to Interactive. Angular 20+ defaults to standalone.

## 3. RxJS Optimization (rxjs)

**Impact:** HIGH
**Description:** Proper RxJS usage with takeUntilDestroyed, async pipe, and efficient operators prevents memory leaks and reduces computations.

## 4. Template Performance (template)

**Impact:** HIGH
**Description:** New control flow (@for with track, @if) and pure pipes optimize rendering. NgOptimizedImage improves Core Web Vitals.

## 5. Dependency Injection (di)

**Impact:** MEDIUM-HIGH
**Description:** Proper DI with providedIn, InjectionToken, and factory providers enables tree-shaking and testability.

## 6. HTTP & Caching (http)

**Impact:** MEDIUM
**Description:** Functional interceptors, HTTP cache transfer for SSR, and caching strategies reduce network requests.

## 7. Forms Optimization (forms)

**Impact:** MEDIUM
**Description:** Typed reactive forms with NonNullableFormBuilder provide compile-time safety and better DX.

## 8. General Performance (perf)

**Impact:** LOW-MEDIUM
**Description:** Web Workers and additional optimization patterns for specific use cases.
