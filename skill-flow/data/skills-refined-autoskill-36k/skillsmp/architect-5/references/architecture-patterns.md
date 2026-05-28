# Architecture Patterns

Choose the right architecture pattern for your scale and requirements.

## Monolith vs Microservices

### When to Use Monolith

- Small team (< 10 developers)
- New product with unclear requirements
- Tight timeline
- Simple domain

```
┌─────────────────────────────────────┐
│           Monolith                  │
│  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │Users│ │Orders│ │ Pay │           │
│  └─────┘ └─────┘ └─────┘           │
│         ┌──────────┐                │
│         │ Database │                │
│         └──────────┘                │
└─────────────────────────────────────┘
```

**Pros:** Simple, fast to develop, easy to debug, single deployment
**Cons:** Scaling is all-or-nothing, tech stack locked

### When to Use Microservices

- Large team (multiple teams)
- Clear, stable domain boundaries
- Need independent scaling
- Need independent deployment

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Users   │    │ Orders  │    │ Payment │
│ Service │    │ Service │    │ Service │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
┌────┴────┐    ┌────┴────┐    ┌────┴────┐
│Users DB │    │Orders DB│    │Payment DB│
└─────────┘    └─────────┘    └─────────┘
```

**Pros:** Independent scaling, tech flexibility, team autonomy
**Cons:** Operational complexity, distributed debugging, network latency

## Modular Monolith

Best of both worlds for many teams.

```
┌─────────────────────────────────────┐
│        Modular Monolith             │
│  ┌─────────┐ ┌─────────┐ ┌───────┐  │
│  │ Users   │ │ Orders  │ │ Pay   │  │
│  │ Module  │ │ Module  │ │Module │  │
│  └────┬────┘ └────┬────┘ └───┬───┘  │
│       │  API  │        │  API │      │
│  ┌────┴────┬──┴────────┴─────┴────┐ │
│  │              Database           │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

- Strict module boundaries (no cross-module DB queries)
- Well-defined APIs between modules
- Can extract to microservices later

## Hexagonal Architecture (Ports & Adapters)

Isolate business logic from infrastructure.

```
                 ┌─────────────────┐
                 │   HTTP Handler  │
                 └────────┬────────┘
                          │
┌──────────┐    ┌─────────▼─────────┐    ┌──────────┐
│  CLI     │───►│                   │◄───│  Queue   │
└──────────┘    │   Domain Logic    │    └──────────┘
                │   (Pure Business) │
┌──────────┐    │                   │    ┌──────────┐
│  Tests   │───►│                   │◄───│  Timer   │
└──────────┘    └─────────┬─────────┘    └──────────┘
                          │
                 ┌────────▼────────┐
                 │    Repository   │
                 │   (Database)    │
                 └─────────────────┘
```

**Ports:** Interfaces defined by domain (what it needs)
**Adapters:** Implementations (HTTP, DB, Queue)

## Event-Driven Architecture

Decouple services through events.

```
┌─────────┐     Event      ┌─────────────┐
│ Order   │───────────────►│ Event       │
│ Service │  OrderCreated  │ Bus/Broker  │
└─────────┘                └──────┬──────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        ┌─────────┐         ┌─────────┐         ┌─────────┐
        │Inventory│         │ Email   │         │Analytics│
        │ Service │         │ Service │         │ Service │
        └─────────┘         └─────────┘         └─────────┘
```

**Use when:**
- Services need loose coupling
- Actions trigger multiple downstream effects
- Need audit trail of what happened

## Decision Framework

| Factor | Monolith | Modular Monolith | Microservices |
|--------|----------|------------------|---------------|
| Team size | 1-10 | 5-30 | 20+ |
| Domain clarity | Unclear | Moderate | Clear |
| Scaling needs | Uniform | Uniform | Independent |
| Deployment | Simple | Simple | Complex |
| Debugging | Easy | Moderate | Hard |
