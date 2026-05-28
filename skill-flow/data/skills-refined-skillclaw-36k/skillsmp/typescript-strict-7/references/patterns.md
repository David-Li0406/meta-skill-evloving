# TypeScript Strict Mode

## Patterns


---
  #### **Name**
Strict Mode Configuration
  #### **Description**
Enable all strict flags for maximum type safety
  #### **When**
Setting up any TypeScript project
  #### **Example**
    // tsconfig.json
    {
      "compilerOptions": {
        "strict": true,  // Enables all strict flags:
        // - strictNullChecks
        // - strictFunctionTypes
        // - strictBindCallApply
        // - strictPropertyInitialization
        // - noImplicitAny
        // - noImplicitThis
        // - alwaysStrict
    
        // Additional recommended flags
        "noUncheckedIndexedAccess": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true
      }
    }
    

---
  #### **Name**
Type Guards
  #### **Description**
Narrow types safely with type predicates
  #### **When**
Working with union types or unknown values
  #### **Example**
    // Type guard function
    function isUser(value: unknown): value is User {
      return (
        typeof value === 'object' &&
        value !== null &&
        'id' in value &&
        'email' in value
      )
    }
    
    // Usage
    function processData(data: unknown) {
      if (isUser(data)) {
        // data is now typed as User
        console.log(data.email)
      }
    }
    
    // Discriminated union
    type Result<T> = { success: true; data: T } | { success: false; error: string }
    
    function handleResult(result: Result<User>) {
      if (result.success) {
        // result.data is available
        console.log(result.data.email)
      } else {
        // result.error is available
        console.log(result.error)
      }
    }
    

---
  #### **Name**
Generic Constraints
  #### **Description**
Use generics with proper constraints for reusability
  #### **When**
Building reusable functions or components
  #### **Example**
    // Basic constraint
    function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
      return obj[key]
    }
    
    // Multiple constraints
    function merge<T extends object, U extends object>(a: T, b: U): T & U {
      return { ...a, ...b }
    }
    
    // Default type parameter
    function createState<T = string>(initial: T) {
      let state = initial
      return {
        get: () => state,
        set: (value: T) => { state = value }
      }
    }
    
    // React component with generics
    interface ListProps<T> {
      items: T[]
      renderItem: (item: T) => React.ReactNode
    }
    
    function List<T>({ items, renderItem }: ListProps<T>) {
      return <ul>{items.map(renderItem)}</ul>
    }
    

---
  #### **Name**
Utility Types
  #### **Description**
Use built-in utility types for common transformations
  #### **When**
Deriving types from existing types
  #### **Example**
    interface User {
      id: string
      email: string
      name: string
      createdAt: Date
    }
    
    // Make all properties optional
    type PartialUser = Partial<User>
    
    // Make all properties required
    type RequiredUser = Required<User>
    
    // Pick specific properties
    type UserPreview = Pick<User, 'id' | 'name'>
    
    // Omit specific properties
    type UserInput = Omit<User, 'id' | 'createdAt'>
    
    // Make properties readonly
    type ReadonlyUser = Readonly<User>
    
    // Record type for objects
    type UserMap = Record<string, User>
    
    // Extract/Exclude for unions
    type Status = 'pending' | 'active' | 'archived'
    type ActiveStatus = Extract<Status, 'active' | 'pending'>
    

---
  #### **Name**
Const Assertions
  #### **Description**
Use const assertions for literal types and immutability
  #### **When**
Working with configuration objects or fixed values
  #### **Example**
    // Without const - type is string[]
    const colors = ['red', 'green', 'blue']
    
    // With const - type is readonly ['red', 'green', 'blue']
    const colors = ['red', 'green', 'blue'] as const
    
    // Object const assertion
    const config = {
      apiUrl: 'https://api.example.com',
      timeout: 5000,
    } as const
    
    // Type from const
    type Color = typeof colors[number]  // 'red' | 'green' | 'blue'
    
    // Enum-like pattern
    const Status = {
      Pending: 'pending',
      Active: 'active',
      Archived: 'archived',
    } as const
    
    type StatusValue = typeof Status[keyof typeof Status]
    

---
  #### **Name**
Satisfies Operator
  #### **Description**
Use satisfies for type checking without widening
  #### **When**
Want to validate type while preserving literal types
  #### **Example**
    // Without satisfies - loses literal types
    const config: Record<string, string> = {
      home: '/',
      about: '/about',
    }
    // config.home is string, not '/'
    
    // With satisfies - keeps literal types
    const config = {
      home: '/',
      about: '/about',
    } satisfies Record<string, string>
    // config.home is '/'
    
    // Catches typos while preserving types
    const colors = {
      primary: '#007bff',
      secondary: '#6c757d',
      // typo: '#fff',  // Error if not in expected keys
    } satisfies Record<'primary' | 'secondary', string>
    

## Anti-Patterns


---
  #### **Name**
Using 'any'
  #### **Description**
Using 'any' type to bypass type checking
  #### **Why**
Defeats the purpose of TypeScript, hides bugs, spreads through codebase
  #### **Instead**
Use 'unknown' and type guards, or define proper types

---
  #### **Name**
Type Assertions for Convenience
  #### **Description**
Using 'as' to force types instead of fixing the actual issue
  #### **Why**
Lies to the compiler, runtime errors when types don't match
  #### **Instead**
Fix the source of the type mismatch, use type guards

---
  #### **Name**
Disabling Strict Checks
  #### **Description**
Adding // @ts-ignore or disabling strict flags
  #### **Why**
Hides real bugs, creates tech debt, types become untrustworthy
  #### **Instead**
Fix the type error properly, use type guards for edge cases

---
  #### **Name**
Over-Annotating
  #### **Description**
Adding type annotations where TypeScript can infer
  #### **Why**
Verbose, harder to maintain, can cause sync issues
  #### **Instead**
Let TypeScript infer, annotate function signatures and exports

---
  #### **Name**
Non-Null Assertion Abuse
  #### **Description**
Using ! operator without certainty the value exists
  #### **Why**
Runtime errors when value is actually null/undefined
  #### **Instead**
Use optional chaining, nullish coalescing, or proper checks