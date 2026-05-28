# Feature Specification Template

> Copy this structure to `src/features/{name}/docs/spec.md`.

# {Feature Name} Specification

**Status**: 🚧 Drafting | ✅ Approved | 🔨 Implementing | 🚀 Released
**Owner**: {AI Persona / User}
**Last Updated**: {Date}

---

## 1. Context & Goals

### 1.1 Problem Statement
{Why are we building this? What user pain point does it solve?}

### 1.2 User Stories
- As a **{role}**, I want to **{action}**, so that **{benefit}**.

### 1.3 Success Metrics
- [ ] Metric 1 (e.g., Latency < 100ms)
- [ ] Metric 2 (e.g., Zero Type Errors)

---

## 2. Experience Contract

### 2.1 Information Architecture
- **Entry Point**: {Where does the user allow access?}
- **Route**: `/{route-path}`

### 2.2 UI States
| State | Behavior / Visual |
|-------|-------------------|
| **Loading** | {Skeleton / Spinner} |
| **Empty** | {Illustration + CTA} |
| **Error** | {Retry Button + Toast} |

---

## 3. Technical Architecture

### 3.1 Data Model (Zod)
```typescript
const XxxSchema = z.object({
  id: z.string().uuid(),
  // ...
});
```

### 3.2 State Management
- **Server State**: React Query Key `['xxx', 'list']`
- **Client State**: Zustand (if global) or Context (if scoped)

### 3.3 Dependencies
- **New Deps**: {List or None}
- **Reuse**: {Existing components}

---

## 4. Implementation Plan

- [ ] **Phase 1: Core** (Schema, Service, Types)
- [ ] **Phase 2: UI Components** (Presentational)
- [ ] **Phase 3: Integration** (Page, Routing)
- [ ] **Phase 4: Optimization** (Memo, Lazy)
