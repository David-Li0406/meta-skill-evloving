---
title: Use SCAM Pattern Instead of Shared Modules
impact: HIGH
impactDescription: Better tree-shaking and smaller bundles by avoiding shared module bloat
tags: scam, modules, tree-shaking, lazy-loading
---

## Use SCAM Pattern Instead of Shared Modules

SCAM (Single Component as Module) pattern creates a dedicated NgModule for each component, directive, or pipe. This enables better tree-shaking and prevents importing unused code through shared modules.

**Incorrect (Shared module with many exports):**

```typescript
// shared.module.ts
@NgModule({
  declarations: [
    ButtonComponent,
    CardComponent,
    ModalComponent,
    TooltipDirective,
    DatePipe,
    CurrencyPipe,
    // 20+ more components...
  ],
  exports: [
    ButtonComponent,
    CardComponent,
    ModalComponent,
    TooltipDirective,
    DatePipe,
    CurrencyPipe,
    // All exported even if only one is used
  ]
})
export class SharedModule {}

// feature.module.ts
@NgModule({
  imports: [SharedModule] // Imports ALL shared components
})
export class FeatureModule {}
```

**Correct (SCAM pattern):**

```typescript
// button/button.component.module.ts
@NgModule({
  declarations: [ButtonComponent],
  imports: [CommonModule],
  exports: [ButtonComponent]
})
export class ButtonComponentModule {}

// card/card.component.module.ts
@NgModule({
  declarations: [CardComponent],
  imports: [CommonModule],
  exports: [CardComponent]
})
export class CardComponentModule {}

// modal/modal.component.module.ts
@NgModule({
  declarations: [ModalComponent],
  imports: [CommonModule, ButtonComponentModule],
  exports: [ModalComponent]
})
export class ModalComponentModule {}

// tooltip/tooltip.directive.module.ts
@NgModule({
  declarations: [TooltipDirective],
  exports: [TooltipDirective]
})
export class TooltipDirectiveModule {}

// feature.module.ts
@NgModule({
  imports: [
    ButtonComponentModule,  // Only import what you need
    CardComponentModule
  ]
})
export class FeatureModule {}
```

**File structure for SCAM:**

```
shared/
├── button/
│   ├── button.component.ts
│   ├── button.component.html
│   ├── button.component.scss
│   ├── button.component.spec.ts
│   └── button.component.module.ts    # SCAM module
├── card/
│   ├── card.component.ts
│   ├── card.component.module.ts
├── modal/
│   ├── modal.component.ts
│   ├── modal.component.module.ts
└── index.ts                          # Barrel exports
```

**Barrel file for clean imports:**

```typescript
// shared/index.ts
export { ButtonComponentModule } from './button/button.component.module';
export { CardComponentModule } from './card/card.component.module';
export { ModalComponentModule } from './modal/modal.component.module';

// Usage in feature module
import { ButtonComponentModule, CardComponentModule } from '@shared';
```

**Benefits of SCAM:**

1. **Tree-shaking** - Unused components are excluded from bundle
2. **Explicit dependencies** - Each component declares its own imports
3. **Lazy loading ready** - Easy to lazy load individual components
4. **Migration path** - Simpler upgrade to standalone components in v17+

Reference: [Angular Module Best Practices](https://v16.angular.io/guide/ngmodule-faq)
