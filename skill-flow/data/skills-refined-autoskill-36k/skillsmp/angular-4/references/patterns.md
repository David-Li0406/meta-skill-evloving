# Angular

## Patterns


---
  #### **Name**
Standalone Components
  #### **Description**
Self-contained components without NgModules
  #### **When**
All new Angular 17+ development
  #### **Example**
    # STANDALONE COMPONENTS:
    
    """
    Standalone components import their dependencies directly.
    No NgModule needed. Cleaner, more explicit, better tree-shaking.
    """
    
    // Component with imports
    import { Component } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { RouterLink } from '@angular/router';
    import { ButtonComponent } from './button.component';
    
    @Component({
      selector: 'app-header',
      standalone: true,
      imports: [CommonModule, RouterLink, ButtonComponent],
      template: `
        <header>
          <nav>
            <a routerLink="/">Home</a>
            <a routerLink="/about">About</a>
          </nav>
          <app-button (click)="login()">Login</app-button>
        </header>
      `
    })
    export class HeaderComponent {
      login() { /* ... */ }
    }
    
    // Bootstrap standalone application
    // main.ts
    import { bootstrapApplication } from '@angular/platform-browser';
    import { AppComponent } from './app/app.component';
    import { appConfig } from './app/app.config';
    
    bootstrapApplication(AppComponent, appConfig);
    
    // app.config.ts
    import { ApplicationConfig } from '@angular/core';
    import { provideRouter } from '@angular/router';
    import { provideHttpClient } from '@angular/common/http';
    import { routes } from './app.routes';
    
    export const appConfig: ApplicationConfig = {
      providers: [
        provideRouter(routes),
        provideHttpClient()
      ]
    };
    

---
  #### **Name**
Signals for Reactive State
  #### **Description**
Fine-grained reactivity with Angular Signals
  #### **When**
Component state, derived values, effects
  #### **Example**
    # ANGULAR SIGNALS:
    
    """
    Signals are synchronous, fine-grained reactive primitives.
    They replace many uses of BehaviorSubject and enable
    better change detection.
    """
    
    import { Component, signal, computed, effect } from '@angular/core';
    
    @Component({
      selector: 'app-counter',
      standalone: true,
      template: `
        <div>
          <p>Count: {{ count() }}</p>
          <p>Double: {{ double() }}</p>
          <button (click)="increment()">+</button>
          <button (click)="decrement()">-</button>
        </div>
      `
    })
    export class CounterComponent {
      // Writable signal
      count = signal(0);
    
      // Computed signal (derived state)
      double = computed(() => this.count() * 2);
    
      // Effect (side effects when signals change)
      constructor() {
        effect(() => {
          console.log(`Count changed to: ${this.count()}`);
        });
      }
    
      increment() {
        this.count.update(c => c + 1);
        // or: this.count.set(this.count() + 1);
      }
    
      decrement() {
        this.count.update(c => c - 1);
      }
    }
    
    // Signal-based service
    @Injectable({ providedIn: 'root' })
    export class CartService {
      private items = signal<CartItem[]>([]);
    
      readonly items$ = this.items.asReadonly();
      readonly total = computed(() =>
        this.items().reduce((sum, item) => sum + item.price, 0)
      );
      readonly count = computed(() => this.items().length);
    
      addItem(item: CartItem) {
        this.items.update(items => [...items, item]);
      }
    
      removeItem(id: string) {
        this.items.update(items => items.filter(i => i.id !== id));
      }
    }
    

---
  #### **Name**
New Control Flow Syntax
  #### **Description**
Built-in @if, @for, @switch replacing structural directives
  #### **When**
Angular 17+ templates
  #### **Example**
    # NEW CONTROL FLOW:
    
    """
    Angular 17 introduced built-in control flow syntax.
    It's faster, more readable, and enables better optimizations.
    """
    
    @Component({
      selector: 'app-users',
      standalone: true,
      template: `
        <!-- @if replaces *ngIf -->
        @if (loading()) {
          <app-spinner />
        } @else if (error()) {
          <app-error [message]="error()" />
        } @else {
          <ul>
            <!-- @for replaces *ngFor -->
            @for (user of users(); track user.id) {
              <li>{{ user.name }}</li>
            } @empty {
              <li>No users found</li>
            }
          </ul>
        }
    
        <!-- @switch replaces ngSwitch -->
        @switch (status()) {
          @case ('pending') {
            <span class="badge-yellow">Pending</span>
          }
          @case ('approved') {
            <span class="badge-green">Approved</span>
          }
          @case ('rejected') {
            <span class="badge-red">Rejected</span>
          }
          @default {
            <span>Unknown</span>
          }
        }
    
        <!-- @defer for lazy loading -->
        @defer (on viewport) {
          <app-heavy-component />
        } @placeholder {
          <div>Loading...</div>
        } @loading (minimum 500ms) {
          <app-spinner />
        }
      `
    })
    export class UsersComponent {
      loading = signal(false);
      error = signal<string | null>(null);
      users = signal<User[]>([]);
      status = signal<'pending' | 'approved' | 'rejected'>('pending');
    }
    

---
  #### **Name**
Smart and Presentational Components
  #### **Description**
Separate container logic from presentation
  #### **When**
Building component hierarchies
  #### **Example**
    # SMART/PRESENTATIONAL PATTERN:
    
    """
    Smart components: Handle data, inject services, contain logic
    Presentational: Receive data via @Input, emit via @Output, no DI
    """
    
    // Presentational component - pure, testable
    @Component({
      selector: 'app-user-card',
      standalone: true,
      imports: [CommonModule],
      changeDetection: ChangeDetectionStrategy.OnPush,
      template: `
        <div class="card">
          <img [src]="user.avatar" [alt]="user.name" />
          <h3>{{ user.name }}</h3>
          <p>{{ user.email }}</p>
          <button (click)="edit.emit(user)">Edit</button>
          <button (click)="delete.emit(user.id)">Delete</button>
        </div>
      `
    })
    export class UserCardComponent {
      @Input({ required: true }) user!: User;
      @Output() edit = new EventEmitter<User>();
      @Output() delete = new EventEmitter<string>();
    }
    
    // Smart component - orchestrates data
    @Component({
      selector: 'app-users-page',
      standalone: true,
      imports: [CommonModule, UserCardComponent],
      template: `
        @for (user of users(); track user.id) {
          <app-user-card
            [user]="user"
            (edit)="onEdit($event)"
            (delete)="onDelete($event)"
          />
        }
      `
    })
    export class UsersPageComponent {
      private userService = inject(UserService);
      private router = inject(Router);
    
      users = this.userService.users;
    
      onEdit(user: User) {
        this.router.navigate(['/users', user.id, 'edit']);
      }
    
      onDelete(id: string) {
        this.userService.deleteUser(id);
      }
    }
    

---
  #### **Name**
Reactive Forms
  #### **Description**
Form handling with FormBuilder and validators
  #### **When**
Complex forms with validation and dynamic fields
  #### **Example**
    # REACTIVE FORMS:
    
    """
    Reactive forms give you full control over form behavior.
    Use for complex validation, dynamic fields, or when you
    need to test form logic.
    """
    
    import { Component, inject } from '@angular/core';
    import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
    import { CommonModule } from '@angular/common';
    
    @Component({
      selector: 'app-register-form',
      standalone: true,
      imports: [CommonModule, ReactiveFormsModule],
      template: `
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div>
            <label for="email">Email</label>
            <input id="email" formControlName="email" />
            @if (form.controls.email.errors?.['required'] &&
                 form.controls.email.touched) {
              <span class="error">Email is required</span>
            }
            @if (form.controls.email.errors?.['email']) {
              <span class="error">Invalid email format</span>
            }
          </div>
    
          <div>
            <label for="password">Password</label>
            <input id="password" type="password" formControlName="password" />
            @if (form.controls.password.errors?.['minlength']) {
              <span class="error">Minimum 8 characters</span>
            }
          </div>
    
          <div formGroupName="profile">
            <label for="name">Name</label>
            <input id="name" formControlName="name" />
    
            <label for="bio">Bio</label>
            <textarea id="bio" formControlName="bio"></textarea>
          </div>
    
          <button type="submit" [disabled]="form.invalid">
            Register
          </button>
        </form>
      `
    })
    export class RegisterFormComponent {
      private fb = inject(FormBuilder);
    
      form = this.fb.group({
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(8)]],
        profile: this.fb.group({
          name: ['', Validators.required],
          bio: ['']
        })
      });
    
      onSubmit() {
        if (this.form.valid) {
          console.log(this.form.value);
          // { email, password, profile: { name, bio } }
        }
      }
    }
    
    // Custom validator
    function matchPasswords(control: AbstractControl): ValidationErrors | null {
      const password = control.get('password');
      const confirm = control.get('confirmPassword');
    
      if (password?.value !== confirm?.value) {
        return { passwordMismatch: true };
      }
      return null;
    }
    

---
  #### **Name**
HTTP with Interceptors
  #### **Description**
Type-safe HTTP calls with request/response interceptors
  #### **When**
API communication
  #### **Example**
    # HTTP CLIENT:
    
    """
    Use HttpClient with typed responses and interceptors
    for auth tokens, error handling, caching.
    """
    
    // Service with typed HTTP
    @Injectable({ providedIn: 'root' })
    export class UserService {
      private http = inject(HttpClient);
      private baseUrl = '/api/users';
    
      getUsers(): Observable<User[]> {
        return this.http.get<User[]>(this.baseUrl);
      }
    
      getUser(id: string): Observable<User> {
        return this.http.get<User>(`${this.baseUrl}/${id}`);
      }
    
      createUser(data: CreateUserDto): Observable<User> {
        return this.http.post<User>(this.baseUrl, data);
      }
    
      updateUser(id: string, data: Partial<User>): Observable<User> {
        return this.http.patch<User>(`${this.baseUrl}/${id}`, data);
      }
    
      deleteUser(id: string): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/${id}`);
      }
    }
    
    // Functional interceptor (Angular 17+)
    export const authInterceptor: HttpInterceptorFn = (req, next) => {
      const authService = inject(AuthService);
      const token = authService.getToken();
    
      if (token) {
        req = req.clone({
          setHeaders: { Authorization: `Bearer ${token}` }
        });
      }
    
      return next(req);
    };
    
    export const errorInterceptor: HttpInterceptorFn = (req, next) => {
      return next(req).pipe(
        catchError((error: HttpErrorResponse) => {
          if (error.status === 401) {
            inject(Router).navigate(['/login']);
          }
          return throwError(() => error);
        })
      );
    };
    
    // Register in app.config.ts
    export const appConfig: ApplicationConfig = {
      providers: [
        provideHttpClient(
          withInterceptors([authInterceptor, errorInterceptor])
        )
      ]
    };
    

## Anti-Patterns


---
  #### **Name**
Logic in Templates
  #### **Description**
Complex expressions or method calls in templates
  #### **Why**
    Templates re-evaluate on every change detection cycle.
    A method call in the template runs repeatedly. Even simple
    getters become performance problems at scale.
    
  #### **Instead**
    // WRONG: Method in template
    <div>{{ getFullName() }}</div>
    
    // RIGHT: Use computed signal or property
    fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
    <div>{{ fullName() }}</div>
    
    // Or for simple cases, a getter with OnPush
    @Component({ changeDetection: ChangeDetectionStrategy.OnPush })
    get fullName() { return `${this.firstName} ${this.lastName}`; }
    

---
  #### **Name**
Subscribe in Components
  #### **Description**
Manual subscription management in components
  #### **Why**
    Every subscribe needs an unsubscribe. Forget one, you have
    a memory leak. Components with multiple subscriptions become
    a maintenance nightmare.
    
  #### **Instead**
    // WRONG: Manual subscribe
    ngOnInit() {
      this.userService.getUser().subscribe(user => {
        this.user = user;
      });
    }
    
    // RIGHT: async pipe (auto-unsubscribes)
    user$ = this.userService.getUser();
    <div>{{ (user$ | async)?.name }}</div>
    
    // RIGHT: toSignal (converts Observable to Signal)
    user = toSignal(this.userService.getUser());
    <div>{{ user()?.name }}</div>
    
    // If you must subscribe, use takeUntilDestroyed
    private destroyRef = inject(DestroyRef);
    
    ngOnInit() {
      this.userService.getUser()
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe(user => this.user = user);
    }
    

---
  #### **Name**
Default Change Detection
  #### **Description**
Using Default change detection on all components
  #### **Why**
    Default change detection checks every component on every
    event. In large apps, this causes performance issues.
    OnPush only checks when inputs change or events fire.
    
  #### **Instead**
    // WRONG: Default (implicit)
    @Component({ ... })
    export class MyComponent {}
    
    // RIGHT: OnPush for all presentational components
    @Component({
      changeDetection: ChangeDetectionStrategy.OnPush,
      ...
    })
    export class MyComponent {}
    

---
  #### **Name**
NgModules for Everything
  #### **Description**
Creating NgModules for every feature in new projects
  #### **Why**
    NgModules add complexity. Standalone components are simpler,
    have better tree-shaking, and are the future of Angular.
    NgModules are still needed for some cases, but shouldn't be default.
    
  #### **Instead**
    // WRONG: Creating modules for everything
    @NgModule({
      declarations: [UserComponent],
      imports: [CommonModule],
      exports: [UserComponent]
    })
    export class UserModule {}
    
    // RIGHT: Standalone component
    @Component({
      standalone: true,
      imports: [CommonModule],
      ...
    })
    export class UserComponent {}
    

---
  #### **Name**
Any Types
  #### **Description**
Using 'any' to bypass TypeScript
  #### **Why**
    Angular's power comes from TypeScript integration. Using 'any'
    defeats the purpose. You lose autocomplete, refactoring safety,
    and catch bugs at runtime instead of compile time.
    
  #### **Instead**
    // WRONG
    data: any;
    onSubmit(form: any) { ... }
    
    // RIGHT
    data: User | null = null;
    onSubmit(form: FormGroup<UserForm>) { ... }
    
    // Enable strict mode in tsconfig.json
    {
      "compilerOptions": {
        "strict": true,
        "noImplicitAny": true
      }
    }
    