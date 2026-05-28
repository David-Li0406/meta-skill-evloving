---
id: knowledge_base
name: Knowledge Base Search
version: 1.0.0
category: knowledge
description: Search and retrieve information from the vector knowledge base (RAG)

tool_configs:
  - name: kb_search
    description: Search the knowledge base for relevant information
    method: search
    args:
      - name: query
        type: string
        required: true
        description: The search query to find relevant documents
      - name: top_k
        type: integer
        required: false
        description: Number of results to return (default 5)
      - name: collection
        type: string
        required: false
        description: Filter by collection name
    requires_skill_loaded: true

  - name: kb_list_documents
    description: List documents in the knowledge base
    method: list_documents
    args:
      - name: collection
        type: string
        required: false
        description: Filter by collection name
    requires_skill_loaded: true

  - name: kb_list_collections
    description: List all collections in the knowledge base
    method: list_collections
    args: []
    requires_skill_loaded: true

  - name: kb_get_stats
    description: Get knowledge base statistics
    method: get_stats
    args: []
    requires_skill_loaded: false

resource_configs:
  - name: search_tips
    description: Tips for effective knowledge base searches
    content: |
      ## Search Tips
      - Use specific keywords related to your topic
      - Try different phrasings if initial search doesn't return good results
      - Use collection filters to narrow down results
      - Higher top_k values give more context but may include less relevant results
---

# Knowledge Base Skill

You have access to a vector knowledge base that stores documents and enables semantic search. This knowledge base uses embeddings to find contextually relevant information.

## Capabilities

1. **Semantic Search**: Search for documents using natural language queries. The search uses vector similarity to find contextually relevant content, not just keyword matching.

2. **Collection Management**: Documents can be organized into collections. Use collection filters to narrow your search to specific domains or topics.

3. **Context Retrieval**: Retrieve relevant context from documents to help answer user questions. Multiple document chunks may be combined to provide comprehensive information.

## When to Use This Skill

Use the knowledge base when:
- The user asks about specific topics that may be in uploaded documents
- You need factual information from the user's document collection
- Looking for specific details, quotes, or data from stored documents
- The user references documents they've previously uploaded

## Search Guidelines

1. **Be Specific**: Use clear, focused queries. Instead of "tell me about the project", try "project requirements and timeline".

2. **Iterate**: If initial results aren't helpful, rephrase your query or try different keywords.

3. **Use Context**: Combine multiple search results to build a comprehensive answer.

4. **Cite Sources**: When using information from search results, mention the source document.

## Example Workflows

### Finding Specific Information
1. Call `kb_search` with a targeted query
2. Review the returned chunks for relevant information
3. If needed, search again with refined query
4. Synthesize information from multiple results

### Exploring Available Documents
1. Call `kb_list_collections` to see what's available
2. Call `kb_list_documents` to see specific files
3. Search within relevant collections for specific content

### Checking System Status
1. Call `kb_get_stats` to verify the knowledge base is available
2. Check document and chunk counts to understand the knowledge base size
