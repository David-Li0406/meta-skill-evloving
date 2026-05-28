---
name: dataflow-installation
description: "DataFlow installation and setup guide. Use when asking 'install dataflow', 'dataflow setup', or 'dataflow requirements'."
---

# DataFlow Installation Guide

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`dataflow-specialist`](dataflow-specialist.md), [`dataflow-quickstart`](dataflow-quickstart.md)

## Installation

```bash
# Install DataFlow
pip install kailash-dataflow

# With PostgreSQL support
pip install kailash-dataflow[postgresql]

# With all database drivers
pip install kailash-dataflow[all]
```

## Requirements

- Python 3.9+
- kailash SDK 0.9.25+
- **SQL Databases**: SQLite (included), PostgreSQL 12+, MySQL 5.7+/8.0+
- **Document Database**: MongoDB 4.4+ (optional, for MongoDB support)
- **Vector Search**: PostgreSQL with pgvector extension (optional, for semantic search)

## Quick Setup

```python
from dataflow import DataFlow

# SQLite (default, zero-config)
db = DataFlow("sqlite:///my_app.db")

# PostgreSQL (production recommended)
db = DataFlow("postgresql://user:pass@localhost/mydb")

# MySQL (web hosting)
db = DataFlow("mysql://user:pass@localhost/mydb")

# MongoDB (document database)
from dataflow.adapters import MongoDBAdapter
adapter = MongoDBAdapter("mongodb://localhost:27017/mydb")
db = DataFlow(adapter=adapter)

# Initialize schema (SQL databases only)
db.initialize_schema()
```

## Verification

```python
# Test connection
print(db.connection_string)

# Verify models are loaded
print(db.list_models())
```

## Documentation

- **Installation Guide**: [`sdk-users/apps/dataflow/01-installation.md`](../../../../sdk-users/apps/dataflow/01-installation.md)

<!-- Trigger Keywords: install dataflow, dataflow setup, dataflow requirements, dataflow installation -->
