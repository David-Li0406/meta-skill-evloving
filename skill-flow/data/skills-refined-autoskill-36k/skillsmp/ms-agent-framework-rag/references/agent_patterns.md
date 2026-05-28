# Multi-Agent Design Patterns

## Core Agent Types

### Research Agent

Responsibilities:
- Query expansion and reformulation
- Multi-source document retrieval
- Relevance scoring and ranking

```csharp
public class ResearchAgent
{
    public async Task<List<Document>> SearchAsync(
        string query,
        SearchOptions options)
    {
        // Expand query with related terms
        // Execute hybrid search
        // Rank results by relevance
    }
}
```

### Synthesis Agent

Responsibilities:
- Combine information from multiple documents
- Resolve contradictions
- Generate coherent responses

```csharp
public class SynthesisAgent
{
    public async Task<string> SynthesizeAsync(
        List<Document> documents,
        string query)
    {
        // Extract key points from each doc
        // Identify common themes
        // Generate unified response
    }
}
```

### Validation Agent

Responsibilities:
- Fact-check generated content
- Verify citation accuracy
- Flag uncertain claims

```csharp
public class ValidationAgent
{
    public async Task<ValidationResult> ValidateAsync(
        string response,
        List<Citation> citations)
    {
        // Check each citation exists
        // Verify quotes match source
        // Return confidence score
    }
}
```

## Orchestration Patterns

### Sequential Pipeline

Agents execute in order:
1. Research → 2. Synthesis → 3. Validation

Best for: Simple Q&A systems

### Parallel Research

Multiple research agents query different sources:
1. Research Agents (parallel) → 2. Synthesis → 3. Validation

Best for: Complex, multi-domain queries

### Iterative Refinement

Agents cycle until consensus:
1. Research → 2. Synthesis → 3. Validation
   ↓ (if low confidence)
   Back to Research with refined query

Best for: High-accuracy requirements

## Communication Patterns

### Message Queue (AutoGen)

```csharp
var researchAgent = new ResearchAgent(config);
var synthesisAgent = new SynthesisAgent(config);

var workflow = new Workflow()
    .AddAgent(researchAgent)
    .AddAgent(synthesisAgent)
    .DefineTransition(
        from: researchAgent,
        to: synthesisAgent,
        when: msg => msg.HasDocuments());
```

### Shared State

```csharp
public class RAGContext
{
    public string Query { get; set; }
    public List<Document> FoundDocuments { get; set; }
    public string DraftResponse { get; set; }
    public ValidationResult Validation { get; set; }
}
```
