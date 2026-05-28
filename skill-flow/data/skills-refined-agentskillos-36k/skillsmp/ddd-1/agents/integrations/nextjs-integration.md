---
name: Next.js + DDD Integration
description: |
  Guide d'intégration DDD avec Next.js App Router.
  Structure de projet, API Routes, Server Actions.
workflows:
  - id: nextjs-ddd-setup
    name: Setup Next.js + DDD
    steps:
      - Structurer le projet
      - Configurer les layers
      - Implémenter les API Routes
      - Connecter les Server Actions
---

# Next.js + DDD Integration

## Responsabilité

Tu guides l'**intégration de DDD avec Next.js** (App Router), en respectant la séparation des couches.

### Tu FAIS

- Proposer une structure de projet
- Montrer l'intégration API Routes/Server Actions
- Séparer domain et infrastructure
- Adapter les patterns au contexte Next.js

### Tu NE FAIS PAS

- Détailler les patterns DDD (→ agents tactical)
- Gérer le frontend React (→ `react-expert`)

---

## Structure de Projet

```
my-nextjs-app/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── api/                  # API Routes (REST)
│   │   │   └── orders/
│   │   │       ├── route.ts      # GET /api/orders, POST /api/orders
│   │   │       └── [id]/
│   │   │           └── route.ts  # GET/PATCH /api/orders/:id
│   │   ├── orders/
│   │   │   ├── page.tsx          # UI - Liste commandes
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx      # UI - Détail commande
│   │   │   └── actions.ts        # Server Actions
│   │   └── layout.tsx
│   │
│   ├── domain/                   # 🎯 DOMAIN LAYER (pur)
│   │   ├── ordering/
│   │   │   ├── Order.ts          # Aggregate
│   │   │   ├── OrderLine.ts      # Entity
│   │   │   ├── OrderId.ts        # Value Object
│   │   │   ├── Money.ts          # Value Object
│   │   │   ├── OrderRepository.ts # Interface (port)
│   │   │   └── events/
│   │   │       ├── OrderPlaced.ts
│   │   │       └── OrderShipped.ts
│   │   └── shared/
│   │       ├── Entity.ts
│   │       ├── AggregateRoot.ts
│   │       └── ValueObject.ts
│   │
│   ├── application/              # APPLICATION LAYER
│   │   ├── commands/
│   │   │   ├── PlaceOrderCommand.ts
│   │   │   └── PlaceOrderHandler.ts
│   │   ├── queries/
│   │   │   ├── GetOrderQuery.ts
│   │   │   └── GetOrderHandler.ts
│   │   └── dto/
│   │       ├── OrderDTO.ts
│   │       └── CreateOrderDTO.ts
│   │
│   ├── infrastructure/           # INFRASTRUCTURE LAYER
│   │   ├── persistence/
│   │   │   ├── prisma/
│   │   │   │   └── schema.prisma
│   │   │   ├── PrismaOrderRepository.ts
│   │   │   └── OrderMapper.ts
│   │   └── messaging/
│   │       └── EventBus.ts
│   │
│   └── lib/                      # Shared utilities
│       ├── di/                   # Dependency Injection
│       │   └── container.ts
│       └── errors/
│           └── AppError.ts
│
├── prisma/
│   └── schema.prisma
└── package.json
```

---

## API Routes (REST)

### GET /api/orders

```typescript
// src/app/api/orders/route.ts

import { NextRequest, NextResponse } from 'next/server';
import { container } from '@/lib/di/container';
import { GetOrdersHandler } from '@/application/queries/GetOrdersHandler';
import { PlaceOrderHandler } from '@/application/commands/PlaceOrderHandler';
import { DomainError } from '@/domain/shared/errors/DomainError';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const customerId = searchParams.get('customerId');

  const handler = container.resolve(GetOrdersHandler);

  const orders = await handler.execute({
    customerId: customerId ?? undefined,
    limit: 20
  });

  return NextResponse.json(orders);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const handler = container.resolve(PlaceOrderHandler);

    const orderId = await handler.execute({
      customerId: body.customerId,
      lines: body.lines,
      shippingAddress: body.shippingAddress
    });

    return NextResponse.json(
      { orderId: orderId.value },
      { status: 201 }
    );
  } catch (error) {
    if (error instanceof DomainError) {
      return NextResponse.json(
        { error: error.message, code: error.code },
        { status: 400 }
      );
    }
    throw error;
  }
}
```

### GET/PATCH /api/orders/:id

```typescript
// src/app/api/orders/[id]/route.ts

import { NextRequest, NextResponse } from 'next/server';
import { container } from '@/lib/di/container';
import { GetOrderHandler } from '@/application/queries/GetOrderHandler';
import { ShipOrderHandler } from '@/application/commands/ShipOrderHandler';
import { OrderId } from '@/domain/ordering/OrderId';

type Params = { params: { id: string } };

export async function GET(request: NextRequest, { params }: Params) {
  const handler = container.resolve(GetOrderHandler);

  const order = await handler.execute({
    orderId: OrderId.create(params.id)
  });

  if (!order) {
    return NextResponse.json(
      { error: 'Order not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(order);
}

export async function PATCH(request: NextRequest, { params }: Params) {
  const body = await request.json();

  if (body.action === 'ship') {
    const handler = container.resolve(ShipOrderHandler);

    await handler.execute({
      orderId: OrderId.create(params.id),
      trackingNumber: body.trackingNumber
    });

    return NextResponse.json({ status: 'shipped' });
  }

  return NextResponse.json(
    { error: 'Unknown action' },
    { status: 400 }
  );
}
```

---

## Server Actions

```typescript
// src/app/orders/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { container } from '@/lib/di/container';
import { PlaceOrderHandler } from '@/application/commands/PlaceOrderHandler';
import { CancelOrderHandler } from '@/application/commands/CancelOrderHandler';
import { DomainError } from '@/domain/shared/errors/DomainError';
import { OrderId } from '@/domain/ordering/OrderId';
import { CancellationReason } from '@/domain/ordering/CancellationReason';
import { z } from 'zod';

// Schema de validation
const PlaceOrderSchema = z.object({
  customerId: z.string().uuid(),
  lines: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().positive()
  })).min(1),
  shippingAddress: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
    postalCode: z.string().min(1),
    country: z.string().length(2)
  })
});

export async function placeOrder(formData: FormData) {
  // 1. Parser et valider
  const raw = Object.fromEntries(formData);
  const parsed = PlaceOrderSchema.safeParse({
    customerId: raw.customerId,
    lines: JSON.parse(raw.lines as string),
    shippingAddress: JSON.parse(raw.shippingAddress as string)
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  // 2. Exécuter le use case
  try {
    const handler = container.resolve(PlaceOrderHandler);
    const orderId = await handler.execute(parsed.data);

    // 3. Revalider le cache et rediriger
    revalidatePath('/orders');
    redirect(`/orders/${orderId.value}`);
  } catch (error) {
    if (error instanceof DomainError) {
      return { error: error.message };
    }
    throw error;
  }
}

export async function cancelOrder(orderId: string, reason: string) {
  const handler = container.resolve(CancelOrderHandler);

  try {
    await handler.execute({
      orderId: OrderId.create(orderId),
      reason: CancellationReason.create(reason)
    });

    revalidatePath('/orders');
    revalidatePath(`/orders/${orderId}`);

    return { success: true };
  } catch (error) {
    if (error instanceof DomainError) {
      return { error: error.message };
    }
    throw error;
  }
}
```

---

## Dependency Injection

```typescript
// src/lib/di/container.ts

import { PrismaClient } from '@prisma/client';
import { PrismaOrderRepository } from '@/infrastructure/persistence/PrismaOrderRepository';
import { PlaceOrderHandler } from '@/application/commands/PlaceOrderHandler';
import { GetOrderHandler } from '@/application/queries/GetOrderHandler';

// Simple DI container (ou utiliser tsyringe/inversify)
class Container {
  private instances = new Map<string, unknown>();

  private prisma = new PrismaClient();

  resolve<T>(token: new (...args: unknown[]) => T): T {
    const key = token.name;

    if (!this.instances.has(key)) {
      this.instances.set(key, this.create(token));
    }

    return this.instances.get(key) as T;
  }

  private create<T>(token: new (...args: unknown[]) => T): T {
    switch (token.name) {
      case 'PrismaOrderRepository':
        return new PrismaOrderRepository(this.prisma) as T;

      case 'PlaceOrderHandler':
        return new PlaceOrderHandler(
          this.resolve(PrismaOrderRepository)
        ) as T;

      case 'GetOrderHandler':
        return new GetOrderHandler(this.prisma) as T;

      default:
        throw new Error(`Unknown token: ${token.name}`);
    }
  }
}

export const container = new Container();
```

---

## Read Models (CQRS léger)

```typescript
// src/application/queries/GetOrderHandler.ts

import { PrismaClient } from '@prisma/client';
import { OrderDTO } from '../dto/OrderDTO';

export class GetOrderHandler {
  constructor(private readonly prisma: PrismaClient) {}

  async execute(query: { orderId: OrderId }): Promise<OrderDTO | null> {
    // Lecture directe depuis Prisma (bypass domain)
    const order = await this.prisma.order.findUnique({
      where: { id: query.orderId.value },
      include: {
        lines: {
          include: { product: true }
        },
        customer: true
      }
    });

    if (!order) return null;

    // Mapper vers DTO (pas vers domain entity)
    return {
      id: order.id,
      status: order.status,
      customerName: order.customer.name,
      lines: order.lines.map(l => ({
        productName: l.product.name,
        quantity: l.quantity,
        unitPrice: l.unitPrice,
        subtotal: l.quantity * l.unitPrice
      })),
      total: order.total,
      placedAt: order.placedAt.toISOString()
    };
  }
}
```

---

## Résumé Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        NEXT.JS                               │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │   API Routes    │    │  Server Actions │                 │
│  │   (REST API)    │    │  (Forms/UI)     │                 │
│  └────────┬────────┘    └────────┬────────┘                 │
│           │                      │                           │
│           └──────────┬───────────┘                           │
│                      ▼                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              APPLICATION LAYER                       │    │
│  │  Commands/Queries Handlers, DTOs                     │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           │                                  │
│  ┌────────────────────────▼────────────────────────────┐    │
│  │                 DOMAIN LAYER                         │    │
│  │  Aggregates, Entities, Value Objects, Events         │    │
│  │  (No dependencies on Next.js/Prisma)                 │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           │                                  │
│  ┌────────────────────────▼────────────────────────────┐    │
│  │              INFRASTRUCTURE LAYER                    │    │
│  │  Prisma Repositories, Event Bus                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Mots-clés de routage

`nextjs`, `next.js`, `app router`, `server actions`, `api routes`, `integration`
