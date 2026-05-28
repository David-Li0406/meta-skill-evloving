# Runtime API Reference

## Core Components

### FablePlayer
Main component for executing FableDSL stories.

```typescript
interface FablePlayerProps {
  ast: Fable;
  width?: number;
  height?: number;
  onStateChange?: (state: PlayerState) => void;
}

const player = <FablePlayer ast={fableAst} width={800} height={600} />;
```

### Player State
```typescript
interface PlayerState {
  currentPage: number;
  variables: Record<string, any>;
  pageHistory: number[];
}
```

## Visual Agents

### Text Component
```typescript
interface FableTextProps {
  id?: string;
  content: string;
  position: [number, number];
  style?: TextStyle;
  onClick?: () => void;
}
```

### Button Component
```typescript
interface FableButtonProps {
  id?: string;
  text: string;
  position: [number, number];
  size?: [number, number];
  onClick: () => void;
  disabled?: boolean;
}
```

### Image Component
```typescript
interface FableImageProps {
  id?: string;
  src: string;
  position: [number, number];
  scale?: number;
  onClick?: () => void;
}
```

## Animation System

### Animation Engine
```typescript
class AnimationEngine {
  static animate(
    element: HTMLElement,
    animation: AnimationCommand,
    duration?: number
  ): Promise<void>;
}
```

### Animation Commands
```typescript
interface AnimationCommand {
  type: 'fade_in' | 'slide_left' | 'bounce' | 'scale';
  duration?: number;
  easing?: string;
  [key: string]: any;
}
```

## Control Flow

### If Statement Handler
```typescript
class IfHandler {
  static evaluate(
    condition: Expression,
    variables: Record<string, any>
  ): boolean;

  static execute(
    ifBlock: IfBlock,
    context: RuntimeContext
  ): Promise<void>;
}
```

### Loop Handler
```typescript
class LoopHandler {
  static execute(
    forBlock: ForBlock,
    context: RuntimeContext
  ): Promise<void>;
}
```

## Expression Evaluator

### Supported Operations
```typescript
class ExpressionEvaluator {
  // Arithmetic
  static add(a: number, b: number): number;
  static subtract(a: number, b: number): number;
  static multiply(a: number, b: number): number;
  static divide(a: number, b: number): number;

  // Comparison
  static equals(a: any, b: any): boolean;
  static greaterThan(a: number, b: number): boolean;
  static lessThan(a: number, b: number): boolean;

  // Logical
  static and(a: boolean, b: boolean): boolean;
  static or(a: boolean, b: boolean): boolean;
  static not(value: boolean): boolean;
}
```

## Runtime Context

### Context Interface
```typescript
interface RuntimeContext {
  variables: Map<string, any>;
  currentPage: number;
  pageHistory: number[];
  dom: {
    getElementById(id: string): HTMLElement | null;
    getElementsByClass(className: string): HTMLElement[];
  };
}
```

## Error Handling

### Runtime Errors
```typescript
class RuntimeError extends Error {
  constructor(
    message: string,
    public line?: number,
    public column?: number
  ) {
    super(message);
  }
}
```

### Validation Errors
```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public errors: ValidationIssue[]
  ) {
    super(message);
  }
}
```