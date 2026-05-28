---
name: Repository Template
description: |
  Template de scaffolding pour créer des Repositories DDD.
  Interface dans le domaine, implémentation dans l'infrastructure.
workflows:
  - id: scaffold-repository
    name: Scaffolding Repository
    steps:
      - Définir l'interface domaine
      - Créer l'implémentation infrastructure
      - Ajouter les specifications
---

# Repository Template

## Responsabilité

Tu génères des **templates de Repositories** avec séparation interface/implémentation.

### Tu FAIS

- Générer l'interface dans le domaine
- Proposer l'implémentation infrastructure
- Inclure les patterns de query

### Tu NE FAIS PAS

- Définir les aggregates (→ `aggregates`)
- Gérer les transactions (→ `application-services`)

---

## Template: Interface (Domain Layer)

```typescript
// ============================================
// domain/repositories/OrderRepository.ts
// ============================================

export interface OrderRepository {
  // Commands
  save(order: Order): Promise<void>;
  delete(id: OrderId): Promise<void>;

  // Queries
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;

  // Existence check
  exists(id: OrderId): Promise<boolean>;

  // Specification-based
  findMatching(spec: Specification<Order>): Promise<Order[]>;
  countMatching(spec: Specification<Order>): Promise<number>;

  // Generator pour gros volumes
  nextId(): OrderId;
}
```

## Template: Implementation (Infrastructure)

```typescript
// ============================================
// infrastructure/persistence/TypeOrmOrderRepository.ts
// ============================================

@Injectable()
export class TypeOrmOrderRepository implements OrderRepository {
  constructor(
    @InjectRepository(OrderEntity)
    private readonly ormRepo: Repository<OrderEntity>,
    private readonly mapper: OrderMapper
  ) {}

  async save(order: Order): Promise<void> {
    const entity = this.mapper.toPersistence(order);
    await this.ormRepo.save(entity);
  }

  async findById(id: OrderId): Promise<Order | null> {
    const entity = await this.ormRepo.findOne({
      where: { id: id.value },
      relations: ['lines', 'lines.product']
    });

    return entity ? this.mapper.toDomain(entity) : null;
  }

  async findByCustomer(customerId: CustomerId): Promise<Order[]> {
    const entities = await this.ormRepo.find({
      where: { customerId: customerId.value },
      relations: ['lines']
    });

    return entities.map(e => this.mapper.toDomain(e));
  }

  nextId(): OrderId {
    return OrderId.create(uuid());
  }
}
```

## Template: Mapper

```typescript
// ============================================
// infrastructure/persistence/OrderMapper.ts
// ============================================

@Injectable()
export class OrderMapper {
  toDomain(entity: OrderEntity): Order {
    return Order.reconstitute({
      id: OrderId.create(entity.id),
      customerId: CustomerId.create(entity.customerId),
      lines: entity.lines.map(this.mapLineToDomain),
      status: OrderStatus.fromValue(entity.status),
      placedAt: entity.placedAt
    });
  }

  toPersistence(order: Order): OrderEntity {
    const entity = new OrderEntity();
    entity.id = order.id.value;
    entity.customerId = order.customerId.value;
    entity.status = order.status.value;
    entity.placedAt = order.placedAt;
    entity.lines = order.lines.map(this.mapLineToPersistence);
    return entity;
  }

  private mapLineToDomain(entity: OrderLineEntity): OrderLine {
    return new OrderLine(
      OrderLineId.create(entity.id),
      ProductId.create(entity.productId),
      entity.productName,
      Money.of(entity.unitPrice, entity.currency),
      entity.quantity
    );
  }
}
```

---

## Mots-clés de routage

`repository`, `template repository`, `persistence`, `mapper`
