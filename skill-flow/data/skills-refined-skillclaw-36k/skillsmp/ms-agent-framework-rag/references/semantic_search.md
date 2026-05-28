# Semantic Search with Azure AI Search

## Overview

Azure AI Search (formerly Cognitive Search) provides integrated vector search capabilities with optional keyword search (BM25).

## Key Concepts

### Vector Fields

```json
{
  "fields": [
    {
      "name": "content_vector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchConfiguration": "myVectorConfig"
    }
  ]
}
```

### Hybrid Search

Combine vector and keyword search for best results:

```csharp
var searchOptions = new SearchOptions
{
    VectorSearch = new VectorSearchOptions
    {
        Queries = { new VectorQuery { Vector = embedding, KNearestNeighborsCount = 5 } }
    },
    SearchText = query, // BM25 keyword search
    QueryType = SearchQueryType.Semantic
};
```

### Scoring Profiles

Boost recent documents or authoritative sources:

```json
{
  "scoringProfiles": [
    {
      "name": "boost-recency",
      "functions": [
        {
          "type": "freshness",
          "fieldName": "last_modified",
          "boost": 100
        }
      ]
    }
  ]
}
```

## Implementation

### Index Creation

```csharp
await searchService.CreateIndex("documents", new SearchIndex
{
    Fields =
    {
        new SimpleField("id", "string") { IsKey = true },
        new SearchField("content", "string") { IsSearchable = true },
        new SearchField("content_vector", "Collection(Edm.Single)") 
        { 
            IsSearchable = true,
            Dimensions = 1536
        }
    },
    VectorSearch = new VectorSearchConfiguration
    {
        AlgorithmConfigurations =
        {
            new VectorSearchAlgorithmConfiguration("myVectorConfig", "hnsw")
        }
    }
});
```

### Document Upload

```csharp
var batch = new IndexDocumentsBatch<SearchDocument>
{
    Actions =
    {
        IndexDocumentsAction.Upload(new SearchDocument
        {
            Id = Guid.NewGuid().ToString(),
            Content = chunk.Text,
            ContentVector = await embeddingService.GenerateEmbedding(chunk.Text),
            Metadata = new { source = chunk.Source, page = chunk.PageNumber }
        })
    }
};

await searchClient.IndexDocumentsAsync(batch);
```

### Query Execution

```csharp
var embedding = await embeddingService.GenerateEmbedding(query);

var response = await searchClient.SearchAsync<SearchDocument>(
    new SearchOptions
    {
        VectorSearch = new()
        {
            Queries = { new() { Vector = embedding, KNearestNeighborsCount = 5 } }
        },
        Size = 10,
        Select = { "id", "content", "metadata" }
    }
);
```

## Best Practices

1. **Chunk Size**: 512-1024 tokens for most documents
2. **Overlap**: 10-20% between chunks for context continuity
3. **Metadata**: Include source, page, timestamp, tags
4. **Hybrid Search**: Always use vector + keyword for production
5. **Re-Ranking**: Use cross-encoder for top 20 results

## Performance Tips

- Use batch indexing (max 1000 documents per batch)
- Enable caching for frequent queries
- Partition large indices by date or category
- Use query-time filters to reduce search space
