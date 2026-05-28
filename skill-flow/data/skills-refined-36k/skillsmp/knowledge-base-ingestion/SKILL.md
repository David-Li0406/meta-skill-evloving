---
id: kb_ingest
name: Knowledge Base Ingestion
version: 1.0.0
category: knowledge
description: Ingest and manage documents in the vector knowledge base

tool_configs:
  - name: kb_ingest_text
    description: Ingest plain text content into the knowledge base
    method: ingest_text
    args:
      - name: text
        type: string
        required: true
        description: The text content to ingest
      - name: title
        type: string
        required: true
        description: Title/name for the document
      - name: collection
        type: string
        required: false
        description: Collection to add the document to
    requires_skill_loaded: true

  - name: kb_ingest_url
    description: Fetch and ingest content from a URL into the knowledge base
    method: ingest_url
    args:
      - name: url
        type: string
        required: true
        description: The URL to fetch content from
      - name: collection
        type: string
        required: false
        description: Collection to add the document to
    requires_skill_loaded: true

  - name: kb_delete_document
    description: Delete a document from the knowledge base
    method: delete_document
    args:
      - name: document_id
        type: string
        required: true
        description: The ID of the document to delete
    requires_skill_loaded: true

  - name: kb_get_document
    description: Get information about a specific document
    method: get_document
    args:
      - name: document_id
        type: string
        required: true
        description: The ID of the document to retrieve
    requires_skill_loaded: true

resource_configs:
  - name: ingestion_guidelines
    description: Guidelines for effective knowledge base ingestion
    content: |
      ## Ingestion Guidelines

      ### Text Content
      - Use descriptive titles that help identify the content
      - Organize related content into collections
      - Keep individual documents focused on a single topic
      - Larger documents are automatically chunked for better search

      ### URL Content
      - Web pages are fetched and converted to plain text
      - JavaScript-heavy pages may not extract well
      - Consider using the text ingestion for better control

      ### Collections
      - Use collections to organize documents by topic or source
      - Collection names should be lowercase with underscores
      - Examples: "company_policies", "technical_docs", "meeting_notes"
---

# Knowledge Base Ingestion Skill

You have the ability to add content to the vector knowledge base. This allows you to build a searchable repository of information that can be retrieved later using semantic search.

## Capabilities

1. **Text Ingestion**: Add plain text content directly to the knowledge base. The text is automatically chunked and embedded for semantic search.

2. **URL Ingestion**: Fetch content from a URL and add it to the knowledge base. Useful for adding web pages, documentation, or online resources.

3. **Document Management**: Delete documents that are no longer needed, or get information about existing documents.

## When to Use This Skill

Use knowledge base ingestion when:
- The user wants to add information for later retrieval
- Building a custom knowledge repository
- Adding reference materials, documentation, or notes
- The user shares content they want to "remember" or store

## Ingestion Guidelines

1. **Use Descriptive Titles**: Choose titles that will help identify the content later. Good titles make it easier to find documents.

2. **Organize with Collections**: Group related documents into collections for better organization:
   - `technical_docs` - Technical documentation
   - `meeting_notes` - Meeting summaries
   - `research` - Research materials
   - `policies` - Company policies

3. **Chunk Size**: Documents are automatically split into smaller chunks for better search relevance. You don't need to worry about document size.

4. **Confirm Success**: After ingestion, confirm the document was added successfully by reporting the document ID and chunk count.

## Example Workflows

### Adding Text Content
1. User provides text to remember
2. Call `kb_ingest_text` with the text and a descriptive title
3. Optionally specify a collection
4. Confirm success with document details

### Adding Web Content
1. User provides a URL
2. Call `kb_ingest_url` with the URL
3. Content is fetched, processed, and stored
4. Confirm success with document details

### Removing Content
1. User requests document removal
2. Use `kb_list_documents` (from KB Search skill) to find the document
3. Call `kb_delete_document` with the document ID
4. Confirm deletion

## Important Notes

- Ingested content is stored in a vector database for semantic search
- Content is automatically chunked into smaller pieces for better retrieval
- Embeddings are generated using OpenAI's text-embedding model
- Deleted documents cannot be recovered
