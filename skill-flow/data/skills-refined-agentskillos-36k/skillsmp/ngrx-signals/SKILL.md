---
name: ngrx-signals
description: @ngrx/signals state management for Angular 20+ using pure reactive patterns with signalStore, rxMethod, and computed signals. Use when implementing reactive state, creating stores, managing async operations, or building signal-based architecture. Replaces traditional NgRx with simpler, more performant signal-based approach.
license: MIT
---

# @ngrx/signals (v20) Skill

## 🎯 Summary
**@ngrx/signals** provides signal-based reactive state management for Angular 20+, enabling predictable, testable, and scalable reactive stores.  
Designed for the NgRx 20 ecosystem with first-class Signal support.

---

## 🛠️ Installation
```bash
pnpm install @ngrx/signals@latest
# or
ng add @ngrx/signals
```

Ensure your project is upgraded to Angular v20 & NgRx v20.

---

## 🚀 Basic Usage

### 1️⃣ Create a SignalStore

Use `signalStore(...)` to define a store:
- Include `withState` to manage initial state
- Use `withMethods` / `rxMethod` to encapsulate logic
- Signals automatically track dependencies and update UI

**Example:**

```typescript
const CounterStore = signalStore(
  withState({ count: 0 }),
  withMethods((store) => ({
    increment: () => patchState(store, (state) => ({ 
      count: state.count + 1 
    }))
  }))
);
```

---

## 🔄 Core Concepts

### 🧠 Signals & Reactivity
- Signals are callable getter functions
- Automatically track dependencies and trigger updates (OnPush friendly)

### 📦 State Management
- Use `signalStore` + `withState` to define readable/writable state
- `patchState` updates partial state
- Derived signals (`computed`) create derived state

---

## 🚦 Advanced Skills

### 🔹 Entity Management
- Use `@ngrx/signals/entities` plugin
- Methods: `addEntity`, `updateEntity`, `removeEntity`, etc.
- Enhanced collection management

### 🔹 Computed State
- Create derived signals when source signal changes
- Avoid manual effects/subscriptions

---

## 🧪 Testing Skills
- Use `@ngrx/signals/testing` for testing utilities
- Makes stores easier to test with helper functions

---

## ⭐ Advanced Patterns

### 👩‍💻 Event-Driven Architecture
- Experimental Events plugin for Flux-style design
- Use with caution in production

### 📜 Interop with RxJS
- Optional RxJS interoperability
- Use `rxMethod` for async operations

---

## 📁 Recommended Project Structure

```
src/
├── app/
│   ├── stores/
│   │   ├── counter.store.ts       # Single store
│   │   ├── users.store.ts         # Entity store
│   │   └── index.ts               # Exports
│   ├── features/
│   │   └── users/
│   │       ├── ui/
│   │       │   ├── user-list.component.ts
│   │       │   └── user-detail.component.ts
│   │       └── users.store.ts     # Feature store
│   └── services/
│       └── api.service.ts
```

---

## 📚 Learning Path

1. ➤ Learn Angular Signals fundamentals
2. ➤ Install & initialize @ngrx/signals
3. ➤ Build simple feature store
4. ➤ Add entity management
5. ➤ Use advanced patterns (Events, RxJS interop)
6. ➤ Write tests using @ngrx/signals/testing

---

## 📝 Notes

- @ngrx/signals is evolving rapidly
- Events/Flux plugin is experimental
- Official docs: [NgRx Signals API Reference](https://ngrx.io/guide/signals)
