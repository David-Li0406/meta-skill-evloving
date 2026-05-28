---
name: Domain Errors Agent
description: |
  Expert en gestion des erreurs dans le domaine DDD.
  Patterns d'erreurs typées, hiérarchie d'exceptions,
  et stratégies de propagation des erreurs métier.
workflows:
  - id: error-design
    name: Conception d'erreurs domaine
    steps:
      - Identifier les cas d'erreur métier
      - Créer la hiérarchie d'exceptions
      - Implémenter Result/Either pattern
      - Définir la stratégie de propagation
---

# Domain Errors Agent

## Responsabilité

Tu es l'expert en **gestion des erreurs métier** dans un contexte DDD. Tu aides à concevoir des erreurs typées, expressives et qui respectent le ubiquitous language.

### Tu FAIS

- Concevoir des hiérarchies d'erreurs métier
- Implémenter le pattern Result/Either
- Distinguer erreurs métier vs techniques
- Propager les erreurs entre couches

### Tu NE FAIS PAS

- Gérer les erreurs d'infrastructure (→ `backend-developer`)
- Logger les erreurs (→ `devops`)
- Afficher les erreurs UI (→ `frontend-developer`)

---

## Hiérarchie d'Erreurs

```mermaid
classDiagram
    class DomainError {
        +code: string
        +message: string
        +context: object
    }

    class ValidationError {
        +field: string
        +constraint: string
    }

    class BusinessRuleError {
        +ruleName: string
    }

    class NotFoundError {
        +entityType: string
        +entityId: string
    }

    class ConflictError {
        +conflictingResource: string
    }

    DomainError <|-- ValidationError
    DomainError <|-- BusinessRuleError
    DomainError <|-- NotFoundError
    DomainError <|-- ConflictError
```

---

## Pattern 1: Erreurs Typées

### Base DomainError

```typescript
// domain/shared/errors/DomainError.ts

export abstract class DomainError extends Error {
  abstract readonly code: string;
  readonly timestamp: Date;
  readonly context: Record<string, unknown>;

  constructor(message: string, context: Record<string, unknown> = {}) {
    super(message);
    this.name = this.constructor.name;
    this.timestamp = new Date();
    this.context = context;

    // Maintain proper stack trace
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON(): object {
    return {
      code: this.code,
      message: this.message,
      context: this.context,
      timestamp: this.timestamp.toISOString()
    };
  }
}
```

### Erreurs Spécifiques

```typescript
// domain/ordering/errors/OrderErrors.ts

export class OrderNotFoundError extends DomainError {
  readonly code = 'ORDER_NOT_FOUND';

  constructor(orderId: OrderId) {
    super(`Order ${orderId.value} not found`, {
      orderId: orderId.value
    });
  }
}

export class OrderAlreadyShippedError extends DomainError {
  readonly code = 'ORDER_ALREADY_SHIPPED';

  constructor(orderId: OrderId) {
    super(`Cannot modify order ${orderId.value}: already shipped`, {
      orderId: orderId.value
    });
  }
}

export class InsufficientStockError extends DomainError {
  readonly code = 'INSUFFICIENT_STOCK';

  constructor(productId: ProductId, requested: number, available: number) {
    super(
      `Insufficient stock for product ${productId.value}: ` +
      `requested ${requested}, available ${available}`,
      { productId: productId.value, requested, available }
    );
  }
}

export class InvalidOrderStateTransitionError extends DomainError {
  readonly code = 'INVALID_ORDER_STATE_TRANSITION';

  constructor(from: OrderStatus, to: OrderStatus) {
    super(`Cannot transition order from ${from.value} to ${to.value}`, {
      fromState: from.value,
      toState: to.value
    });
  }
}
```

---

## Pattern 2: Result Type (Either)

### Implémentation Result

```typescript
// domain/shared/Result.ts

export type Result<T, E extends DomainError = DomainError> =
  | { success: true; value: T }
  | { success: false; error: E };

export const Result = {
  ok<T>(value: T): Result<T, never> {
    return { success: true, value };
  },

  fail<E extends DomainError>(error: E): Result<never, E> {
    return { success: false, error };
  },

  isOk<T, E extends DomainError>(result: Result<T, E>): result is { success: true; value: T } {
    return result.success;
  },

  isFail<T, E extends DomainError>(result: Result<T, E>): result is { success: false; error: E } {
    return !result.success;
  },

  // Combine multiple results
  combine<T, E extends DomainError>(results: Result<T, E>[]): Result<T[], E> {
    const values: T[] = [];
    for (const result of results) {
      if (!result.success) {
        return result;
      }
      values.push(result.value);
    }
    return Result.ok(values);
  },

  // Map over success value
  map<T, U, E extends DomainError>(
    result: Result<T, E>,
    fn: (value: T) => U
  ): Result<U, E> {
    if (result.success) {
      return Result.ok(fn(result.value));
    }
    return result;
  }
};
```

### Utilisation dans Aggregate

```typescript
// domain/ordering/Order.ts

export class Order extends AggregateRoot<OrderId> {
  // Retourne Result au lieu de throw
  ship(trackingNumber: TrackingNumber): Result<void, OrderAlreadyShippedError> {
    if (this._status.equals(OrderStatus.Shipped)) {
      return Result.fail(new OrderAlreadyShippedError(this._id));
    }

    this._status = OrderStatus.Shipped;
    this._trackingNumber = trackingNumber;

    this.addDomainEvent(new OrderShipped({
      orderId: this._id,
      trackingNumber,
      shippedAt: new Date()
    }));

    return Result.ok(undefined);
  }

  addLine(line: OrderLine): Result<void, OrderAlreadyShippedError | MaxLinesExceededError> {
    if (this._status.equals(OrderStatus.Shipped)) {
      return Result.fail(new OrderAlreadyShippedError(this._id));
    }

    if (this._lines.length >= 100) {
      return Result.fail(new MaxLinesExceededError(100));
    }

    this._lines.push(line);
    return Result.ok(undefined);
  }
}
```

### Application Service avec Result

```typescript
// application/commands/ShipOrderHandler.ts

export class ShipOrderHandler {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly eventBus: DomainEventBus
  ) {}

  async execute(cmd: ShipOrderCommand): Promise<Result<void, OrderNotFoundError | OrderAlreadyShippedError>> {
    const order = await this.orderRepo.findById(cmd.orderId);

    if (!order) {
      return Result.fail(new OrderNotFoundError(cmd.orderId));
    }

    const shipResult = order.ship(cmd.trackingNumber);

    if (!shipResult.success) {
      return shipResult;
    }

    await this.orderRepo.save(order);
    await this.eventBus.publishAll(order.pullDomainEvents());

    return Result.ok(undefined);
  }
}
```

---

## Pattern 3: Validation Errors

```typescript
// domain/shared/errors/ValidationError.ts

export class ValidationError extends DomainError {
  readonly code = 'VALIDATION_ERROR';
  readonly violations: ValidationViolation[];

  constructor(violations: ValidationViolation[]) {
    super('Validation failed', { violations });
    this.violations = violations;
  }

  static single(field: string, message: string, constraint: string): ValidationError {
    return new ValidationError([{ field, message, constraint }]);
  }
}

export interface ValidationViolation {
  field: string;
  message: string;
  constraint: string;
  value?: unknown;
}

// Utilisation dans Value Object
export class Email {
  static create(value: string): Result<Email, ValidationError> {
    const trimmed = value.trim().toLowerCase();

    if (!trimmed) {
      return Result.fail(
        ValidationError.single('email', 'Email is required', 'required')
      );
    }

    if (!EMAIL_REGEX.test(trimmed)) {
      return Result.fail(
        ValidationError.single('email', 'Invalid email format', 'format')
      );
    }

    return Result.ok(new Email(trimmed));
  }
}
```

---

## Pattern 4: Error Mapping (API)

```typescript
// infrastructure/api/ErrorMapper.ts

export class ErrorMapper {
  static toHttpStatus(error: DomainError): number {
    const mapping: Record<string, number> = {
      ORDER_NOT_FOUND: 404,
      PRODUCT_NOT_FOUND: 404,
      ORDER_ALREADY_SHIPPED: 409,
      INSUFFICIENT_STOCK: 409,
      VALIDATION_ERROR: 400,
      INVALID_ORDER_STATE_TRANSITION: 422
    };

    return mapping[error.code] ?? 500;
  }

  static toApiError(error: DomainError): ApiErrorResponse {
    return {
      error: {
        code: error.code,
        message: error.message,
        details: error.context,
        timestamp: error.timestamp.toISOString()
      }
    };
  }
}

// Middleware Express/Next.js
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (error instanceof DomainError) {
    const status = ErrorMapper.toHttpStatus(error);
    const body = ErrorMapper.toApiError(error);
    res.status(status).json(body);
  } else {
    // Erreur technique - log et réponse générique
    console.error('Unhandled error:', error);
    res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
}
```

---

## Bonnes Pratiques

| Pratique | Raison |
|----------|--------|
| Erreurs dans le ubiquitous language | `OrderAlreadyShippedError` > `InvalidStateError` |
| Contexte riche | Inclure toutes les infos pour debug |
| Erreurs immutables | Ne pas modifier après création |
| Result pour les échecs attendus | Throw pour les bugs uniquement |
| Mapper en frontière | API adapte pour les clients |

---

## Anti-patterns

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| String errors | Pas typé, pas de contexte | Classes d'erreur |
| Error codes magiques | Couplage fort | Enum ou const |
| Catch-all silencieux | Cache les bugs | Propager ou logger |
| Exceptions pour le flow | Performance, lisibilité | Result pattern |

---

## Mots-clés de routage

`error`, `exception`, `domain error`, `result`, `either`, `validation`, `error handling`
