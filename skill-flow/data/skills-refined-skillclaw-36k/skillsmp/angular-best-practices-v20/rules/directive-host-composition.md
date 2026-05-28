---
title: Use Host Directives for Behavior Composition
impact: MEDIUM
impactDescription: Reusable behaviors, cleaner components
tags: directives, composition, host-directives
---

## Use Host Directives for Behavior Composition

Host directives compose reusable behaviors into components without inheritance, promoting composition and keeping components focused.

**Incorrect (Repeated behavior across components):**

```typescript
@Component({
  selector: 'app-button',
  template: `<ng-content />`
})
export class ButtonComponent {
  @HostBinding('class.focused') isFocused = false;
  @HostBinding('class.disabled') isDisabled = false;

  @HostListener('focus') onFocus() { this.isFocused = true; }
  @HostListener('blur') onBlur() { this.isFocused = false; }
}

@Component({
  selector: 'app-card',
  template: `<ng-content />`
})
export class CardComponent {
  // Same focus/disable logic duplicated...
  @HostBinding('class.focused') isFocused = false;
  @HostBinding('class.disabled') isDisabled = false;
}
```

**Correct (Reusable behavior directive):**

```typescript
@Directive({
  selector: '[focusable]',
  host: {
    'tabindex': '0',
    '(focus)': 'onFocus()',
    '(blur)': 'onBlur()',
    '[class.focused]': 'isFocused()'
  }
})
export class FocusableDirective {
  isFocused = signal(false);
  onFocus() { this.isFocused.set(true); }
  onBlur() { this.isFocused.set(false); }
}

@Component({
  selector: 'app-button',
  hostDirectives: [FocusableDirective],
  template: `<ng-content />`
})
export class ButtonComponent {}

@Component({
  selector: 'app-card',
  hostDirectives: [FocusableDirective],
  template: `<ng-content />`
})
export class CardComponent {}
```

**Why it matters:**
- Behaviors defined once, reused everywhere
- `hostDirectives` array composes multiple behaviors
- Inputs/outputs can be exposed via directive configuration
- No inheritance hierarchy needed

Reference: [Angular Host Directives](https://angular.dev/guide/directives/directive-composition-api)
