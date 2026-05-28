---
name: dojo-indexer
description: Use this skill when you need to set up and configure the Torii indexer for efficient GraphQL queries, gRPC subscriptions, and SQL access to your deployed world.
---

# Skill body

## When to Use This Skill

- "Set up Torii indexer"
- "Configure GraphQL for my world"
- "Create subscriptions for entity updates"
- "Query world state efficiently"

## What This Skill Does

Manages the Torii indexer:
- Start and configure Torii
- Create GraphQL queries
- Set up real-time subscriptions
- Access SQL database directly
- Optimize query performance

## Quick Start

**Start Torii:**
```bash
torii --world <WORLD_ADDRESS>
```
This starts Torii with default settings:
- GraphQL API at `http://localhost:8080/graphql`
- gRPC API at `http://localhost:8081`
- In-memory database (for development)

**Production configuration:**
```bash
torii --world <WORLD_ADDRESS> --database <DATABASE_PATH>
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--world` | World contract address | Required |
| `--rpc` | RPC endpoint URL | Required |
| `--database` | SQLite database path | `torii.db` |
| `--allowed-origins` | CORS origins | `*` |
| `--graphql-port` | GraphQL port | `8080` |
| `--grpc-port` | gRPC port | `8081` |

## What is Torii?

Torii is the Dojo indexer that:
- Watches blockchain for world events
- Indexes model state changes
- Provides GraphQL API for queries
- Provides gRPC API for subscriptions
- Offers SQL access for complex queries

**Why use Torii:**
- Faster than direct RPC queries
- Supports complex queries (filters, pagination)
- Real-time subscriptions
- Type-safe GraphQL schema

## GraphQL API

Torii provides a GraphQL endpoint at `http://localhost:8080/graphql`.

### Basic Queries

**Get all entities of a model:**
```graphql
query {
  positions {
    edges {
      node {
        player
        x
        y
      }
    }
  }
}
```

**Get model metadata:**
```graphql
query {
  models {
    edges {
      node {
        id
        name
        classHash
        contractAddress
      }
    }
    totalCount
  }
}
```

### Pagination

**Cursor-based pagination:**
```graphql
query {
  positions(first: 10) {
    edges {
      node {
        player
        x
        y
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```