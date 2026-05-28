# Citations Reference

Claude provides detailed citations when answering questions about documents, helping track and verify information sources in responses.

## Table of Contents

- [Supported Models](#supported-models)
- [How Citations Work](#how-citations-work)
- [Document Types](#document-types)
- [Citation Types](#citation-types)
- [Response Structure](#response-structure)
- [Streaming Support](#streaming-support)
- [Token Costs](#token-costs)
- [Feature Compatibility](#feature-compatibility)
- [Prompt Caching with Citations](#prompt-caching-with-citations)

---

## Supported Models

All active Claude models support citations, except Haiku 3.

**Note for Claude Sonnet 3.7:** May be less likely to cite without explicit instructions. Add prompts like:
- `"Use citations to back up your answer."`
- `"Always use citations in your answer, even within <result> tags."`

---

## How Citations Work

### Step 1: Provide Documents and Enable Citations

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": "The grass is green. The sky is blue."
    },
    "title": "My Document",  # optional, not cited from
    "context": "Trustworthy document.",  # optional, not cited from
    "citations": {"enabled": True}
}
```

**Requirements:**
- Set `citations.enabled=true` on each document
- Citations must be enabled on all or none of the documents in a request
- Only text citations are currently supported (not images)

### Step 2: Documents Get Processed

Documents are chunked to define citation granularity:

| Document Type | Chunking Behavior |
|---------------|-------------------|
| PDF | Text extracted, chunked into sentences |
| Plain text | Chunked into sentences |
| Custom content | Uses your content blocks as-is |

### Step 3: Claude Provides Cited Response

Response includes text blocks with citation lists referencing source documents.

---

## Document Types

### Plain Text Documents

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": "Document content here..."
    },
    "title": "Document Title",
    "context": "Context not cited from",
    "citations": {"enabled": True}
}
```

**Citation type:** `char_location` with character index range (0-indexed)

### PDF Documents

**Base64:**
```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": base64_encoded_pdf_data
    },
    "title": "Document Title",
    "citations": {"enabled": True}
}
```

**URL:**
```python
{
    "type": "document",
    "source": {
        "type": "url",
        "url": "https://example.com/document.pdf"
    },
    "citations": {"enabled": True}
}
```

**Files API:**
```python
{
    "type": "document",
    "source": {
        "type": "file",
        "file_id": "file_011CNvxoj286tYUAZFiZMf1U"
    },
    "citations": {"enabled": True}
}
```

**Citation type:** `page_location` with page number range (1-indexed)

### Custom Content Documents

Control citation granularity with your own content blocks:

```python
{
    "type": "document",
    "source": {
        "type": "content",
        "content": [
            {"type": "text", "text": "First chunk"},
            {"type": "text", "text": "Second chunk"}
        ]
    },
    "title": "Document Title",
    "citations": {"enabled": True}
}
```

**Citation type:** `content_block_location` with block index range (0-indexed)

**Use cases:**
- Bullet points or transcripts requiring specific granularity
- RAG chunks where you don't want additional chunking
- Custom document structures

---

## Citation Types

### Character Location (Plain Text)

```json
{
    "type": "char_location",
    "cited_text": "The grass is green.",
    "document_index": 0,
    "document_title": "Example Document",
    "start_char_index": 0,
    "end_char_index": 20
}
```

- Character indices: 0-indexed, exclusive end

### Page Location (PDF)

```json
{
    "type": "page_location",
    "cited_text": "Water is essential for life.",
    "document_index": 1,
    "document_title": "PDF Document",
    "start_page_number": 5,
    "end_page_number": 6
}
```

- Page numbers: 1-indexed, exclusive end

### Content Block Location (Custom)

```json
{
    "type": "content_block_location",
    "cited_text": "These are important findings.",
    "document_index": 2,
    "document_title": "Custom Document",
    "start_block_index": 0,
    "end_block_index": 1
}
```

- Block indices: 0-indexed, exclusive end

---

## Response Structure

Responses include multiple text blocks with citations:

```json
{
    "content": [
        {
            "type": "text",
            "text": "According to the document, "
        },
        {
            "type": "text",
            "text": "the grass is green",
            "citations": [{
                "type": "char_location",
                "cited_text": "The grass is green.",
                "document_index": 0,
                "document_title": "Example Document",
                "start_char_index": 0,
                "end_char_index": 20
            }]
        },
        {
            "type": "text",
            "text": " and "
        },
        {
            "type": "text",
            "text": "the sky is blue",
            "citations": [{
                "type": "char_location",
                "cited_text": "The sky is blue.",
                "document_index": 0,
                "document_title": "Example Document",
                "start_char_index": 20,
                "end_char_index": 36
            }]
        }
    ]
}
```

---

## Streaming Support

Streaming responses include `citations_delta` events:

```json
event: content_block_delta
data: {"type": "content_block_delta", "index": 0,
       "delta": {"type": "citations_delta",
                 "citation": {
                     "type": "char_location",
                     "cited_text": "...",
                     "document_index": 0,
                     "start_char_index": 0,
                     "end_char_index": 20
                 }}}
```

---

## Token Costs

| Aspect | Impact |
|--------|--------|
| **Input tokens** | Slight increase due to system prompt additions and chunking |
| **Output tokens** | Efficient - `cited_text` does NOT count toward output tokens |
| **Multi-turn** | `cited_text` also NOT counted as input tokens when passed back |

---

## Feature Compatibility

| Feature | Compatible |
|---------|------------|
| Prompt caching | Yes |
| Token counting | Yes |
| Batch processing | Yes |
| Structured outputs | **No** - returns 400 error |

**Warning:** Citations and Structured Outputs are incompatible. Enabling citations with `output_format` parameter returns a 400 error because citations require interleaving citation blocks with text output.

---

## Prompt Caching with Citations

Apply `cache_control` to document content blocks:

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "text",
                    "media_type": "text/plain",
                    "data": long_document
                },
                "citations": {"enabled": True},
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": "What does this document say about API features?"
            }
        ]
    }]
)
```

**Note:** Citation blocks in responses cannot be cached directly, but source documents can be cached.

---

## Basic Example

### Python

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "text",
                    "media_type": "text/plain",
                    "data": "The grass is green. The sky is blue."
                },
                "title": "My Document",
                "citations": {"enabled": True}
            },
            {
                "type": "text",
                "text": "What color is the grass and sky?"
            }
        ]
    }]
)

# Process citations
for block in response.content:
    if block.type == "text":
        print(block.text)
        if hasattr(block, "citations") and block.citations:
            for citation in block.citations:
                print(f"  Source: {citation.cited_text}")
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: [
      {
        type: "document",
        source: {
          type: "text",
          media_type: "text/plain",
          data: "The grass is green. The sky is blue."
        },
        title: "My Document",
        citations: { enabled: true }
      },
      {
        type: "text",
        text: "What color is the grass and sky?"
      }
    ]
  }]
});
```

---

## Advantages Over Prompt-Based Citations

| Aspect | Citations Feature |
|--------|-------------------|
| **Cost savings** | `cited_text` doesn't count toward output tokens |
| **Reliability** | Guaranteed valid pointers to documents |
| **Quality** | Significantly more likely to cite relevant quotes |
