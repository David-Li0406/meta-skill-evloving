---
name: datacommons-client
description: Use this skill when working with Data Commons to access and query public statistical data from global sources, including demographic, economic, health, and environmental datasets.
---

# Data Commons Client

## Overview

Provides comprehensive access to the Data Commons Python API v2 for querying statistical observations, exploring the knowledge graph, and resolving entity identifiers. Data Commons aggregates data from census bureaus, health organizations, environmental agencies, and other authoritative sources into a unified knowledge graph.

## Installation

Install the Data Commons Python client with Pandas support:

```bash
pip install "datacommons-client[Pandas]"
```

For basic usage without Pandas:

```bash
pip install datacommons-client
```

## Core Capabilities

The Data Commons API consists of three main endpoints:

### 1. Observation Endpoint - Statistical Data Queries

Query time-series statistical data for entities. 

**Primary use cases:**
- Retrieve population, economic, health, or environmental statistics
- Access historical time-series data for trend analysis
- Query data for hierarchies (e.g., all counties in a state, all countries in a region)
- Compare statistics across multiple entities
- Filter by data source for consistency

**Common patterns:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Get latest population data
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06"],  # California
    date="latest"
)

# Get time series
response = client.observation.fetch(
    variable_dcids=["UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

# Query by hierarchy
response = client.observation.fetch(
    variable_dcids=["MedianIncome_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

### 2. Node Endpoint - Knowledge Graph Exploration

Explore entity relationships and properties within the knowledge graph.