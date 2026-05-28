# Component Examples

Angular v21 component patterns and examples.

## Table of Contents

- [Basic Component](#basic-component)
- [Input and Output](#input-and-output)
- [Host Bindings](#host-bindings)
- [Reactive Forms](#reactive-forms)
- [Image Optimization](#image-optimization)
- [Control Flow](#control-flow)
- [Testing](#testing)

## Basic Component

### Standard Component Pattern

```typescript
import {
  Component,
  ChangeDetectionStrategy,
  input,
  output,
  computed,
} from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-user-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink],
  template: `
    @if (user(); as u) {
      <article class="card">
        <h2>{{ displayName() }}</h2>
        <p>{{ u.email }}</p>
        <button (click)="onSelect()">Select</button>
      </article>
    }
  `,
})
export class UserCardComponent {
  // WHY: input() for reactive inputs
  readonly user = input.required<User>();

  // WHY: output() replaces @Output()
  readonly selected = output<User>();

  // WHY: computed() for derived state
  protected readonly displayName = computed(() => {
    const u = this.user();
    return `${u.firstName} ${u.lastName}`;
  });

  protected onSelect(): void {
    this.selected.emit(this.user());
  }
}
```

### Component with External Template

```typescript
@Component({
  selector: 'app-dashboard',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent {
  // Component logic
}
```

## Input and Output

### Input Patterns

```typescript
import { input } from '@angular/core';

// Required input
readonly user = input.required<User>();

// Optional input with default
readonly theme = input<'light' | 'dark'>('light');

// Input with transform
readonly count = input(0, {
  transform: (value: string | number) => Number(value),
});

// Input with alias
readonly data = input<Data>(undefined, { alias: 'userData' });
```

### Output Patterns

```typescript
import { output } from '@angular/core';

// Basic output
readonly clicked = output<void>();

// Output with payload
readonly selected = output<User>();

// Output with alias
readonly changed = output<string>({ alias: 'valueChanged' });

// Emitting events
protected onClick(): void {
  this.clicked.emit();
}

protected onSelect(user: User): void {
  this.selected.emit(user);
}
```

## Host Bindings

### Host Object Pattern

```typescript
@Component({
  selector: 'app-tooltip',
  changeDetection: ChangeDetectionStrategy.OnPush,
  // WHY: host object replaces @HostBinding/@HostListener
  host: {
    // Class bindings
    '[class.visible]': 'isVisible()',
    '[class.error]': 'hasError()',

    // Attribute bindings
    '[attr.role]': '"tooltip"',
    '[attr.aria-hidden]': '!isVisible()',

    // Style bindings
    '[style.opacity]': 'isVisible() ? 1 : 0',

    // Event listeners
    '(mouseenter)': 'show()',
    '(mouseleave)': 'hide()',
    '(keydown.escape)': 'hide()',
  },
  template: `<ng-content />`,
})
export class TooltipComponent {
  readonly isVisible = signal(false);
  readonly hasError = signal(false);

  protected show(): void {
    this.isVisible.set(true);
  }

  protected hide(): void {
    this.isVisible.set(false);
  }
}
```

### Directive Host Bindings

```typescript
@Directive({
  selector: '[appHighlight]',
  host: {
    '[class.highlighted]': 'isActive()',
    '[style.backgroundColor]': 'color()',
    '(click)': 'toggle()',
  },
})
export class HighlightDirective {
  readonly color = input('yellow');
  readonly isActive = signal(false);

  protected toggle(): void {
    this.isActive.update((v) => !v);
  }
}
```

## Reactive Forms

### Basic Form

```typescript
import { Component, inject } from '@angular/core';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

@Component({
  selector: 'app-login-form',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" type="email" />
      @if (form.controls.email.errors?.['email']) {
        <span class="error">Invalid email</span>
      }

      <input formControlName="password" type="password" />
      @if (form.controls.password.errors?.['minlength']) {
        <span class="error">Password too short</span>
      }

      <button type="submit" [disabled]="form.invalid">Login</button>
    </form>
  `,
})
export class LoginFormComponent {
  private readonly fb = inject(FormBuilder);

  // WHY: Typed forms provide compile-time safety
  protected readonly form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  protected onSubmit(): void {
    if (this.form.valid) {
      // WHY: getRawValue() includes disabled fields
      const { email, password } = this.form.getRawValue();
      // Handle submission
    }
  }
}
```

### Form with Arrays

```typescript
protected readonly form = this.fb.group({
  name: ['', Validators.required],
  emails: this.fb.array([
    this.fb.control('', [Validators.required, Validators.email]),
  ]),
});

get emailControls() {
  return this.form.controls.emails.controls;
}

addEmail(): void {
  this.form.controls.emails.push(
    this.fb.control('', [Validators.required, Validators.email])
  );
}

removeEmail(index: number): void {
  this.form.controls.emails.removeAt(index);
}
```

## Image Optimization

### NgOptimizedImage Usage

```typescript
import { NgOptimizedImage } from '@angular/common';

@Component({
  selector: 'app-gallery',
  imports: [NgOptimizedImage],
  template: `
    <!-- Basic usage with priority for LCP -->
    <img
      ngSrc="/images/hero.jpg"
      width="800"
      height="600"
      priority
      alt="Hero image"
    />

    <!-- Responsive images -->
    <img
      ngSrc="/images/profile.jpg"
      width="200"
      height="200"
      [ngSrcset]="'320w, 640w, 1280w'"
      sizes="(max-width: 640px) 100vw, 50vw"
      alt="Profile"
    />

    <!-- Fill mode for unknown dimensions -->
    <div class="image-container">
      <img ngSrc="/images/dynamic.jpg" fill alt="Dynamic" />
    </div>

    <!-- Placeholder while loading -->
    <img
      ngSrc="/images/large.jpg"
      width="1200"
      height="800"
      placeholder
      alt="Large image"
    />
  `,
  styles: `
    .image-container {
      position: relative;
      width: 100%;
      height: 300px;
    }
  `,
})
export class GalleryComponent {}
```

## Control Flow

### @if Directive

```html
@if (loading()) {
  <app-spinner />
} @else if (error()) {
  <app-error [message]="error()" />
} @else {
  <app-content [data]="data()" />
}

<!-- With alias -->
@if (user(); as u) {
  <div>{{ u.name }}</div>
}
```

### @for Directive

```html
@for (item of items(); track item.id) {
  <app-item [data]="item" />
} @empty {
  <p>No items found</p>
}

<!-- With index and other context variables -->
@for (item of items(); track item.id; let i = $index, first = $first, last = $last) {
  <div [class.first]="first" [class.last]="last">
    {{ i + 1 }}. {{ item.name }}
  </div>
}
```

### @switch Directive

```html
@switch (status()) {
  @case ('pending') {
    <span class="badge-pending">Pending</span>
  }
  @case ('active') {
    <span class="badge-active">Active</span>
  }
  @case ('completed') {
    <span class="badge-completed">Completed</span>
  }
  @default {
    <span class="badge-unknown">Unknown</span>
  }
}
```

## Testing

### Component Testing

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('UserCardComponent', () => {
  let component: UserCardComponent;
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    component = fixture.componentInstance;
  });

  it('should display user name', () => {
    // WHY: Use fixture.componentRef.setInput for signal inputs
    fixture.componentRef.setInput('user', {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
    });
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('John Doe');
  });

  it('should emit selected event on button click', () => {
    const user = { firstName: 'John', lastName: 'Doe', email: 'john@example.com' };
    fixture.componentRef.setInput('user', user);
    fixture.detectChanges();

    const spy = jest.spyOn(component.selected, 'emit');
    const button = fixture.nativeElement.querySelector('button');
    button.click();

    expect(spy).toHaveBeenCalledWith(user);
  });
});
```

### Service Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        UserService,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should load users', () => {
    const mockUsers = [{ id: 1, name: 'John' }];

    service.loadUsers();

    const req = httpMock.expectOne('/api/users');
    req.flush(mockUsers);

    expect(service.users()).toEqual(mockUsers);
  });
});
```
