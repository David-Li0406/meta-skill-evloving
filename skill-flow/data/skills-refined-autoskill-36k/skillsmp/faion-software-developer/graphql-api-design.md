---
id: graphql-api-design
name: "API Design (GraphQL)"
domain: DEV
skill: faion-software-developer
category: "development"
---

# API Design (GraphQL)

## Overview

GraphQL is a query language for APIs that provides a complete description of data and allows clients to request exactly what they need. It enables powerful developer tools and evolves APIs without versions.

## When to Use

- Complex data relationships
- Mobile applications needing minimal data transfer
- Multiple clients with different data needs
- Rapid frontend development
- APIs requiring real-time updates (subscriptions)

## Key Principles

1. **Client-driven** - Clients specify what data they need
2. **Strongly typed** - Schema defines all types and fields
3. **Single endpoint** - All operations through one URL
4. **Hierarchical** - Query shape matches response shape
5. **Introspective** - Schema is queryable

## Best Practices

### Schema Design

```graphql
# schema.graphql

# Scalar types
scalar DateTime
scalar UUID
scalar Email

# Enums
enum UserRole {
  ADMIN
  MODERATOR
  MEMBER
}

enum OrderStatus {
  DRAFT
  PLACED
  PAID
  SHIPPED
  DELIVERED
  CANCELLED
}

# Interfaces
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Types
type User implements Node & Timestamped {
  id: ID!
  email: Email!
  name: String!
  role: UserRole!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!

  # Relationships
  organization: Organization!
  orders(
    first: Int
    after: String
    status: OrderStatus
  ): OrderConnection!
  posts(first: Int, after: String): PostConnection!
}

type Organization implements Node {
  id: ID!
  name: String!
  users(first: Int, after: String): UserConnection!
  createdAt: DateTime!
}

type Order implements Node & Timestamped {
  id: ID!
  user: User!
  status: OrderStatus!
  items: [OrderItem!]!
  totalAmount: Float!
  shippingAddress: Address
  placedAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  unitPrice: Float!
  totalPrice: Float!
}

type Address {
  street: String!
  city: String!
  state: String
  postalCode: String!
  country: String!
}

# Connection types (Relay spec)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Input types
input CreateUserInput {
  email: Email!
  name: String!
  role: UserRole = MEMBER
  organizationId: ID!
}

input UpdateUserInput {
  email: Email
  name: String
  role: UserRole
}

input UserFilterInput {
  role: UserRole
  isActive: Boolean
  search: String
}

# Payload types (for mutations)
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type UpdateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

# Root types
type Query {
  # Single resource
  user(id: ID!): User
  userByEmail(email: Email!): User
  order(id: ID!): Order
  organization(id: ID!): Organization

  # Collections with filtering/pagination
  users(
    first: Int = 20
    after: String
    filter: UserFilterInput
  ): UserConnection!

  orders(
    first: Int = 20
    after: String
    status: OrderStatus
    userId: ID
  ): OrderConnection!

  # Search
  searchUsers(query: String!, first: Int = 10): [User!]!

  # Current user
  me: User
}

type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeletePayload!

  # Order mutations
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  placeOrder(id: ID!, shippingAddress: AddressInput!): PlaceOrderPayload!
  cancelOrder(id: ID!, reason: String!): CancelOrderPayload!

  # Authentication
  login(email: Email!, password: String!): AuthPayload!
  logout: Boolean!
}

type Subscription {
  orderStatusChanged(orderId: ID!): Order!
  newOrder(userId: ID): Order!
}
```

### Resolver Implementation

```python
# Python with Strawberry GraphQL
import strawberry
from strawberry.types import Info
from typing import List, Optional
from uuid import UUID

from services.user_service import UserService
from services.order_service import OrderService


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    async def organization(self, info: Info) -> "Organization":
        loader = info.context.loaders.organization
        return await loader.load(self.organization_id)

    @strawberry.field
    async def orders(
        self,
        info: Info,
        first: int = 20,
        after: Optional[str] = None,
        status: Optional[OrderStatus] = None,
    ) -> "OrderConnection":
        service: OrderService = info.context.services.order
        return await service.get_user_orders(
            user_id=self.id,
            first=first,
            after=after,
            status=status,
        )


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, id: strawberry.ID) -> Optional[User]:
        service: UserService = info.context.services.user
        return await service.get_by_id(UUID(id))

    @strawberry.field
    async def users(
        self,
        info: Info,
        first: int = 20,
        after: Optional[str] = None,
        filter: Optional[UserFilterInput] = None,
    ) -> UserConnection:
        service: UserService = info.context.services.user
        return await service.list(
            first=first,
            after=after,
            filter=filter,
        )

    @strawberry.field
    async def me(self, info: Info) -> Optional[User]:
        user_id = info.context.current_user_id
        if not user_id:
            return None
        service: UserService = info.context.services.user
        return await service.get_by_id(user_id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self,
        info: Info,
        input: CreateUserInput,
    ) -> CreateUserPayload:
        service: UserService = info.context.services.user

        try:
            user = await service.create(
                email=input.email,
                name=input.name,
                role=input.role,
                organization_id=UUID(input.organization_id),
            )
            return CreateUserPayload(user=user, errors=None)

        except ValidationError as e:
            return CreateUserPayload(
                user=None,
                errors=[
                    Error(field=err.field, message=err.message, code="VALIDATION")
                    for err in e.errors
                ],
            )

        except ConflictError as e:
            return CreateUserPayload(
                user=None,
                errors=[Error(field="email", message=str(e), code="CONFLICT")],
            )

    @strawberry.mutation
    async def update_user(
        self,
        info: Info,
        id: strawberry.ID,
        input: UpdateUserInput,
    ) -> UpdateUserPayload:
        service: UserService = info.context.services.user

        user = await service.update(
            user_id=UUID(id),
            data=input.to_dict(),
        )

        return UpdateUserPayload(user=user, errors=None)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def order_status_changed(
        self,
        info: Info,
        order_id: strawberry.ID,
    ) -> AsyncGenerator[Order, None]:
        pubsub = info.context.pubsub
        async for event in pubsub.subscribe(f"order:{order_id}:status"):
            yield Order.from_event(event)
```

### DataLoader for N+1 Prevention

```python
from strawberry.dataloader import DataLoader
from typing import List
from uuid import UUID


class OrganizationLoader(DataLoader[UUID, Organization]):
    """Batch load organizations to prevent N+1 queries."""

    async def batch_load_fn(self, keys: List[UUID]) -> List[Organization]:
        # Fetch all organizations in single query
        organizations = await self.repository.find_by_ids(keys)

        # Return in same order as keys
        org_map = {org.id: org for org in organizations}
        return [org_map.get(key) for key in keys]


class UserLoader(DataLoader[UUID, User]):
    """Batch load users."""

    async def batch_load_fn(self, keys: List[UUID]) -> List[User]:
        users = await self.repository.find_by_ids(keys)
        user_map = {user.id: user for user in users}
        return [user_map.get(key) for key in keys]


# Context setup
from dataclasses import dataclass


@dataclass
class Context:
    current_user_id: Optional[UUID]
    loaders: "Loaders"
    services: "Services"


@dataclass
class Loaders:
    organization: OrganizationLoader
    user: UserLoader
    order: OrderLoader


async def get_context(request: Request) -> Context:
    return Context(
        current_user_id=request.state.user_id,
        loaders=Loaders(
            organization=OrganizationLoader(organization_repo),
            user=UserLoader(user_repo),
            order=OrderLoader(order_repo),
        ),
        services=Services(
            user=UserService(user_repo),
            order=OrderService(order_repo),
        ),
    )
```

### Error Handling

```python
# Union types for errors
@strawberry.type
class UserNotFoundError:
    message: str
    user_id: str


@strawberry.type
class ValidationError:
    message: str
    field: str


@strawberry.type
class PermissionDeniedError:
    message: str


UserResult = strawberry.union(
    "UserResult",
    [User, UserNotFoundError, PermissionDeniedError],
)


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, id: strawberry.ID) -> UserResult:
        # Check permissions
        if not info.context.current_user_id:
            return PermissionDeniedError(message="Authentication required")

        user = await info.context.services.user.get_by_id(UUID(id))

        if not user:
            return UserNotFoundError(
                message=f"User not found",
                user_id=id,
            )

        return user


# Alternatively, use payload pattern
@strawberry.type
class GetUserPayload:
    user: Optional[User]
    error: Optional[str]
    error_code: Optional[str]
```

### Query Complexity and Depth Limiting

```python
from strawberry.extensions import QueryDepthLimiter
from strawberry.extensions.query_complexity import QueryComplexityExtension


# Limit query depth
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        QueryComplexityExtension(max_complexity=100),
    ],
)


# Field-level complexity
@strawberry.type
class User:
    @strawberry.field(complexity=1)
    def name(self) -> str:
        return self._name

    @strawberry.field(complexity=10)  # Higher complexity for relationships
    async def orders(self, first: int = 10) -> List[Order]:
        return await self._load_orders(first)


# Pagination limits
@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self,
        first: int = strawberry.argument(default=20, description="Max 100"),
    ) -> UserConnection:
        if first > 100:
            raise ValueError("Cannot request more than 100 users")
        ...
```

### Authentication and Authorization

```python
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        return info.context.current_user_id is not None


class IsAdmin(BasePermission):
    message = "User is not an admin"

    async def has_permission(self, source, info: Info, **kwargs) -> bool:
        if not info.context.current_user_id:
            return False

        user = await info.context.services.user.get_by_id(
            info.context.current_user_id
        )
        return user and user.role == UserRole.ADMIN


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_order(self, info: Info, input: CreateOrderInput) -> Order:
        ...

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def delete_user(self, info: Info, id: strawberry.ID) -> bool:
        ...


# Field-level authorization
@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str

    @strawberry.field
    async def secret_data(self, info: Info) -> Optional[str]:
        # Only return if user is viewing their own profile
        if info.context.current_user_id != self.id:
            return None
        return self._secret_data
```

### Subscriptions

```python
import asyncio
from typing import AsyncGenerator


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def order_status_changed(
        self,
        info: Info,
        order_id: strawberry.ID,
    ) -> AsyncGenerator[Order, None]:
        """Subscribe to order status changes."""
        pubsub = info.context.pubsub

        async with pubsub.subscribe(f"order:{order_id}:status") as subscription:
            async for message in subscription:
                order = await info.context.services.order.get_by_id(
                    UUID(order_id)
                )
                if order:
                    yield order

    @strawberry.subscription
    async def new_message(
        self,
        info: Info,
        chat_id: strawberry.ID,
    ) -> AsyncGenerator[Message, None]:
        """Subscribe to new messages in a chat."""
        async for message in info.context.pubsub.subscribe(f"chat:{chat_id}"):
            yield Message.from_dict(message)
```

## Anti-patterns

### Avoid: Over-fetching in Resolvers

```python
# BAD - always loads all relationships
@strawberry.type
class User:
    @strawberry.field
    def orders(self) -> List[Order]:
        return self._orders  # Loaded in parent query

# GOOD - lazy load only when requested
@strawberry.type
class User:
    @strawberry.field
    async def orders(self, info: Info, first: int = 10) -> List[Order]:
        loader = info.context.loaders.orders_by_user
        return await loader.load((self.id, first))
```

### Avoid: Missing Pagination

```python
# BAD - returns all items
@strawberry.field
async def users(self) -> List[User]:
    return await repo.find_all()  # Could return millions

# GOOD - always paginate
@strawberry.field
async def users(self, first: int = 20, after: str = None) -> UserConnection:
    return await repo.find_paginated(first, after)
```

## References

- [GraphQL Specification](https://spec.graphql.org/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Relay Connection Spec](https://relay.dev/graphql/connections.htm)
- [Strawberry GraphQL](https://strawberry.rocks/)
