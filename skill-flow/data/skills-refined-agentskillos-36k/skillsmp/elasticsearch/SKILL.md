---
name: elasticsearch
description: Elasticsearch search and analytics engine operations including CRUD, aggregations, mappings, and reindexing.
---

# Elasticsearch — CRUD Operations

**Create Index**
```bash
curl -X PUT "localhost:9200/index_name"
```

**Add Document**
```bash
curl -X POST "localhost:9200/index_name/_doc" -H 'Content-Type: application/json' -d'
{
  "field": "value"
}'
```

**Search**
```bash
curl -X GET "localhost:9200/index_name/_search?q=field:value"
```

**Delete Index**
```bash
curl -X DELETE "localhost:9200/index_name"
```

## Elasticsearch — Advanced Usage

**Aggregations**
```bash
curl -X GET "localhost:9200/sales/_search" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "avg_price": { "avg": { "field": "price" } }
  }
}'
```

**Mappings**
```bash
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "date": { "type": "date" },
      "text": { "type": "text", "analyzer": "english" }
    }
  }
}'
```

**Reindex API**
```bash
curl -X POST "localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": { "index": "old_index" },
  "dest": { "index": "new_index" }
}'
```