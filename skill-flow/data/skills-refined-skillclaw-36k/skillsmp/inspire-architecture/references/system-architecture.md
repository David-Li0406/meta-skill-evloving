# Inspire Team - System Architecture

## Overview

The Inspire platform is a content-driven system delivering personalized inspiring content across web, mobile, and email channels.

## Service Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Web App   │     │  Mobile App  │     │    Email     │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────┬───────┴────────────────────┘
                    ▼
            ┌───────────────┐
            │  API Gateway  │
            └───────┬───────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Content   │ │    User    │ │ Analytics  │
│  Service   │ │  Service   │ │  Service   │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     ▼
            ┌───────────────┐
            │   Event Bus   │
            │  (RabbitMQ)   │
            └───────────────┘
```

## Core Services

### Content Service
- **Responsibility**: Content CRUD, versioning, scheduling
- **Database**: PostgreSQL
- **Cache**: Redis (TTL: 5 min for published content)

### User Service
- **Responsibility**: Authentication, preferences, personalization
- **Database**: PostgreSQL
- **External**: Auth0 for identity

### Analytics Service
- **Responsibility**: Event tracking, engagement metrics
- **Database**: ClickHouse (time-series)
- **Processing**: Async via event bus

## Data Flow

1. Content created → Content Service → `content.created` event
2. User requests content → API Gateway → Content Service (cache-first)
3. User engages → Analytics Service → `user.engaged` event
4. Personalization updated based on engagement patterns

## Infrastructure

| Component | Technology | Environment |
|-----------|------------|-------------|
| Compute | Kubernetes (EKS) | AWS eu-west-1 |
| Database | RDS PostgreSQL | Multi-AZ |
| Cache | ElastiCache Redis | Cluster mode |
| CDN | CloudFront | Global edge |
| Monitoring | Datadog | All environments |
