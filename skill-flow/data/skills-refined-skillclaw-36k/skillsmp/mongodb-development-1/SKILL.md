---
name: mongodb-development
description: MongoDB database exploration, querying, and debugging using MCP tools. Use when writing aggregation pipelines, analyzing schemas, debugging data issues, or exploring collections in ShipitSmarter databases.
---

# MongoDB Development Skill

This skill guides AI-assisted MongoDB development using the official MongoDB MCP server. Use this when working with MongoDB databases in ShipitSmarter services.

## Prerequisites

The MongoDB MCP server must be configured in OpenCode to use this skill.

### Setup for viya-app

Add the MongoDB MCP server to your `viya-app/opencode.json`. If you already have an `mcp` section, just add the `mongodb` entry:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "chrome-devtools": { ... },
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server@latest"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/shipping"
      }
    }
  }
}
```

**Quick copy-paste** - add this to the `mcp` section:

```json
"mongodb": {
  "command": "npx",
  "args": ["-y", "mongodb-mcp-server@latest"],
  "env": {
    "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/shipping"
  }
}
```

Or add to your global config at `~/.config/opencode/opencode.json` to have it available everywhere.

**Verify setup**: After adding, restart OpenCode and check that MongoDB tools appear (find, aggregate, collection-schema, etc.). You can verify by asking: "list all databases"

### Available MCP Tools

The MongoDB MCP server provides:

- `find` - Query documents
- `aggregate` - Run aggregation pipelines
- `collection-schema` - Infer/describe schema
- `collection-indexes` - List indexes
- `count` - Count documents
- `explain` - Query execution plan
- `list-databases` / `list-collections` - Explore structure

### Connecting to Different Databases

Change the connection string to target different databases:

```bash
# Shipping (default)
mongodb://localhost:27017/shipping

# Auditor
mongodb://localhost:27017/auditor

# Rates
mongodb://localhost:27017/rates
```

You can configure multiple MCP servers for different databases:

```json
{
  "mcp": {
    "mongodb-shipping": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server@latest"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/shipping"
      }
    },
    "mongodb-auditor": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server@latest"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/auditor"
      }
    }
  }
}
```

## ShipitSmarter Database Overview

### Local Development

MongoDB runs in Docker via `viya-app/dev/docker-compose.yaml` at `localhost:27017`.

Make sure the dev environment is running:
```bash
cd viya-app/dev
docker compose up -d mongodb
```

### Main Databases

| Database | Service | Purpose |
|----------|---------|---------|
| `shipping` | shipping | Core shipping data: shipments, orders, tracking |
| `auditor` | auditor | Audit logs, invoice data |
| `authorizing` | authorizing | Authorization, permissions |
| `rates` | rates | Rate calculations, carrier rates |
| `hooks` | hooks | Webhook configurations |

### Common Collections (shipping database)

| Collection | Description |
|------------|-------------|
| `shipments` | Main shipment documents |
| `orders` | Order data |
| `trackingEvents` | Tracking status updates |
| `carriers` | Carrier configurations |
| `customers` | Customer data |

## Workflow: Explore Database Structure

When first working with a database:

```
1. Use list-databases to see available databases
2. Use list-collections to see collections in target database
3. Use collection-schema to understand document structure
4. Use collection-indexes to see existing indexes
```

Example sequence:
```javascript
// List all databases
db.adminCommand({ listDatabases: 1 })

// List collections in shipping
use shipping
db.getCollectionNames()

// Infer schema for shipments
// (MCP tool: collection-schema)
```

## Workflow: Query Data

### Basic Find Queries

Use the `find` MCP tool for simple queries:

```javascript
// Find by ID
db.shipments.find({ _id: ObjectId("...") })

// Find by field
db.shipments.find({ customerId: "cust_123" })

// Find with projection (only specific fields)
db.shipments.find(
  { status: "delivered" },
  { _id: 1, trackingNumber: 1, deliveredAt: 1 }
)

// Find with limit and sort
db.shipments.find({ status: "in_transit" })
  .sort({ createdAt: -1 })
  .limit(10)
```

### Date Range Queries

```javascript
// Shipments created in last 7 days
db.shipments.find({
  createdAt: {
    $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  }
})

// Shipments in specific date range
db.shipments.find({
  createdAt: {
    $gte: ISODate("2026-01-01"),
    $lt: ISODate("2026-01-15")
  }
})
```

### Array Queries

```javascript
// Find documents where array contains value
db.shipments.find({ "packages.weight": { $gt: 10 } })

// Find where array element matches multiple conditions
db.shipments.find({
  packages: {
    $elemMatch: { weight: { $gt: 5 }, type: "parcel" }
  }
})
```

## Workflow: Aggregation Pipelines

Use the `aggregate` MCP tool for complex queries. Always build pipelines incrementally.

### Pattern: Count by Status

```javascript
db.shipments.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

### Pattern: Daily Counts

```javascript
db.shipments.aggregate([
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m-%d", date: "$createdAt" } },
      count: { $sum: 1 }
    }
  },
  { $sort: { _id: -1 } },
  { $limit: 30 }
])
```

### Pattern: Lookup (Join)

```javascript
db.shipments.aggregate([
  { $match: { customerId: "cust_123" } },
  {
    $lookup: {
      from: "trackingEvents",
      localField: "_id",
      foreignField: "shipmentId",
      as: "events"
    }
  }
])
```

### Pattern: Unwind Arrays

```javascript
// Calculate total package weight per shipment
db.shipments.aggregate([
  { $unwind: "$packages" },
  {
    $group: {
      _id: "$_id",
      trackingNumber: { $first: "$trackingNumber" },
      totalWeight: { $sum: "$packages.weight" },
      packageCount: { $sum: 1 }
    }
  }
])
```

### Pattern: Faceted Search

```javascript
db.shipments.aggregate([
  { $match: { createdAt: { $gte: ISODate("2026-01-01") } } },
  {
    $facet: {
      byStatus: [
        { $group: { _id: "$status", count: { $sum: 1 } } }
      ],
      byCarrier: [
        { $group: { _id: "$carrier", count: { $sum: 1 } } }
      ],
      total: [
        { $count: "count" }
      ]
    }
  }
])
```

## Workflow: Analyze Performance

### Check Query Execution

Use the `explain` MCP tool to understand query performance:

```javascript
db.shipments.find({ customerId: "cust_123" }).explain("executionStats")
```

Look for:
- `COLLSCAN` = No index used (bad for large collections)
- `IXSCAN` = Index scan (good)
- `executionStats.totalDocsExamined` vs `nReturned`

### Check Existing Indexes

Use `collection-indexes` MCP tool:

```javascript
db.shipments.getIndexes()
```

### Index Recommendations

Common indexes for shipping data:

```javascript
// Lookup by tracking number
{ trackingNumber: 1 }

// Customer queries
{ customerId: 1, createdAt: -1 }

// Status queries
{ status: 1, createdAt: -1 }

// Compound for filtering + sorting
{ customerId: 1, status: 1, createdAt: -1 }
```

## Workflow: Schema Analysis

Use `collection-schema` MCP tool to understand document structure.

When analyzing schema:
1. Look for required vs optional fields
2. Identify embedded documents vs references
3. Check for inconsistent field types
4. Note array fields that might need `$unwind`

### ShipitSmarter Schema Conventions

- `_id`: Usually ObjectId, sometimes string
- `createdAt` / `updatedAt`: ISO dates
- `customerId`: String reference to customer
- `tenantId`: Multi-tenant isolation
- Arrays: `packages[]`, `events[]`, `documents[]`
- Nested objects: `address.street`, `address.city`

## Safety Guidelines

### When to Use Read-Only Mode

Always use `--readOnly` flag when:
- Connecting to production or staging
- Exploring unfamiliar databases
- Running ad-hoc analytics queries
- Debugging issues

### Safe Operations

These are safe to run anywhere:
- `find` with limit
- `aggregate` (read-only pipelines)
- `count`
- `collection-schema`
- `collection-indexes`
- `explain`
- `list-databases` / `list-collections`

### Dangerous Operations

These should only run on local dev:
- `insert-many` / `update-many` / `delete-many`
- `drop-collection` / `drop-database`
- `create-index` (can lock collection)

### Query Best Practices

1. **Always use filters**: Never `find({})` on large collections
2. **Use limit**: Always add `.limit()` for exploration
3. **Project fields**: Only request fields you need
4. **Check indexes**: Use `explain()` for new query patterns
5. **Test on dev first**: Always validate queries locally

## Troubleshooting

### Connection Issues

If MCP can't connect:
1. Check Docker is running: `docker compose ps`
2. Check MongoDB container: `docker compose logs mongodb`
3. Verify port: `nc -zv localhost 27017`

### Slow Queries

1. Run `explain("executionStats")`
2. Check for `COLLSCAN`
3. Verify appropriate indexes exist
4. Consider adding compound index

### Schema Mismatches

If queries return unexpected results:
1. Run `collection-schema` to see actual structure
2. Check for null/missing fields
3. Verify field types (string vs ObjectId)

## Quick Reference

### MCP Tool Mapping

| Task | MCP Tool |
|------|----------|
| Simple query | `find` |
| Complex query | `aggregate` |
| Document structure | `collection-schema` |
| Check indexes | `collection-indexes` |
| Query performance | `explain` |
| Count documents | `count` |
| List databases | `list-databases` |
| List collections | `list-collections` |

### Common Connection Strings

```
# Local dev
mongodb://localhost:27017/shipping

# With auth
mongodb://user:pass@localhost:27017/shipping?authSource=admin
```

## Example Prompts

Try these prompts in viya-app to do data analysis:

### Exploration
- "List all collections in the shipping database and show me the schema of shipments"
- "What indexes exist on the shipments collection?"
- "Show me a sample document from the orders collection"

### Analysis
- "How many shipments were created per day in the last 30 days?"
- "What's the distribution of shipments by status?"
- "Show me the top 10 customers by shipment volume this month"
- "Find shipments that have been in 'processing' status for more than 24 hours"

### Debugging
- "Find the shipment with tracking number ABC123 and show all its tracking events"
- "Are there any shipments with missing carrier information?"
- "Show me shipments that failed validation in the last hour"

### Performance
- "Explain the query plan for finding shipments by customerId"
- "What queries would benefit from additional indexes on the shipments collection?"

