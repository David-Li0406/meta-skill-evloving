---
title: Use Signal Inputs and Outputs
impact: HIGH
impactDescription: Better reactivity, type safety, simpler code
tags: components, inputs, outputs, signals
---

## Use Signal Inputs and Outputs

Signal inputs (`input()`) and outputs (`output()`) replace `@Input()` and `@Output()` decorators, providing better type inference and reactive tracking without `OnChanges`.

**Incorrect (Decorator-based with OnChanges):**

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <h2>{{ name }}</h2>
    <p>{{ email }}</p>
    <button (click)="onSelect()">Select</button>
  `
})
export class UserCardComponent implements OnChanges {
  @Input() name!: string;
  @Input() email = '';
  @Output() selected = new EventEmitter<string>();

  ngOnChanges(changes: SimpleChanges) {
    if (changes['name']) {
      console.log('Name changed:', this.name);
    }
  }

  onSelect() {
    this.selected.emit(this.name);
  }
}
```

**Correct (Signal inputs with effect):**

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <h2>{{ name() }}</h2>
    <p>{{ email() }}</p>
    <button (click)="handleClick()">Select</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  name = input.required<string>();
  email = input('');
  selected = output<string>();

  constructor() {
    effect(() => {
      console.log('Name changed:', this.name());
    });
  }

  handleClick() {
    this.selected.emit(this.name());
  }
}
```

**Why it matters:**
- `input.required<T>()` enforces required inputs at compile time
- `input(defaultValue)` provides type-inferred optional inputs
- `effect()` replaces `ngOnChanges` for reacting to input changes
- Signals integrate with OnPush for optimal performance

Reference: [Angular Signal Inputs](https://angular.dev/guide/signals/inputs)
