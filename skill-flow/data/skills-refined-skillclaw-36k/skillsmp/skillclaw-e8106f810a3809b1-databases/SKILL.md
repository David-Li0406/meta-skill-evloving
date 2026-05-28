---
name: databases
description: Use this skill when working with MongoDB and PostgreSQL to design schemas, write queries, optimize performance, and manage database operations.
---

# Skill body

Unified guide for working with MongoDB (document-oriented) and PostgreSQL (relational) databases. Choose the right database for your use case and master both systems.

## When to Use This Skill

Use when:
- Designing database schemas and data models
- Writing queries (SQL or MongoDB query language)
- Building aggregation pipelines or complex joins
- Optimizing indexes and query performance
- Implementing database migrations
- Setting up replication, sharding, or clustering
- Configuring backups and disaster recovery
- Managing database users and permissions
- Analyzing slow queries and performance issues
- Administering production database deployments

## Database Selection Guide

### Choose MongoDB When:
- Schema flexibility: frequent structure changes, heterogeneous data
- Document-centric: natural JSON/BSON data model
- Horizontal scaling: need to shard across multiple servers
- High write throughput: IoT, logging, real-time analytics
- Nested/hierarchical data: embedded documents preferred
- Rapid prototyping: schema evolution without migrations

**Best for:** Content management, catalogs, IoT time series, real-time analytics, mobile apps, user profiles

### Choose PostgreSQL When:
- Strong consistency: ACID transactions critical
- Complex relationships: many-to-many joins, referential integrity
- SQL requirement: team expertise, reporting tools, BI systems
- Data integrity: strict schema validation, constraints
- Mature ecosystem: extensive tooling, extensions
- Complex queries: window functions, CTEs, analytical workloads

**Best for:** Financial systems, e-commerce transactions, ERP, CRM, data warehousing, analytics

### Both Support:
- JSON/JSONB storage and querying
- Full-text search capabilities
- Geospatial queries and indexing
- Replication and high availability
- ACID transactions (MongoDB 4.0+)
- Strong security features

## Quick Start

### MongoDB Setup

```bash
# Atlas (Cloud) - Recommended setup
```