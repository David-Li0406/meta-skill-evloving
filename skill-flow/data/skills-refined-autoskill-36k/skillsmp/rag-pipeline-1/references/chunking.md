# Text Chunking Strategies for RAG

## Fixed-Size Chunking (Recommended for Start)

### Basic Implementation
```typescript
function chunkText(text: string, chunkSize = 800, overlap = 200): string[] {
  const chunks: string[] = [];
  let start = 0;
  
  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length);
    chunks.push(text.slice(start, end));
    start += chunkSize - overlap;
  }
  
  return chunks;
}
```

**Pros**: Simple, predictable, works well  
**Cons**: May split paragraphs or code blocks awkwardly

### Parameters
- **Chunk size**: 800 characters (fits in most context windows)
- **Overlap**: 200 characters (preserves context across chunks)

## Semantic Chunking

Split on natural boundaries (paragraphs, sections).

```typescript
function semanticChunk(text: string, maxSize = 1000): string[] {
  const chunks: string[] = [];
  
  // Split on double newlines (paragraphs)
  const paragraphs = text.split(/\n\n+/);
  
  let currentChunk = '';
  
  for (const para of paragraphs) {
    if ((currentChunk + para).length > maxSize && currentChunk) {
      chunks.push(currentChunk.trim());
      currentChunk = para;
    } else {
      currentChunk += (currentChunk ? '\n\n' : '') + para;
    }
  }
  
  if (currentChunk) chunks.push(currentChunk.trim());
  
  return chunks;
}
```

**Pros**: Preserves meaning, respects natural breaks  
**Cons**: Variable chunk sizes

## Markdown-Aware Chunking

Respect headings and code blocks.

```typescript
function markdownChunk(text: string, maxSize = 1000): string[] {
  const chunks: string[] = [];
  const sections = text.split(/^(#{1,6}\s+.+)$/gm);
  
  let currentChunk = '';
  
  for (let i = 0; i < sections.length; i++) {
    const section = sections[i];
    
    // Check if heading
    if (section.match(/^#{1,6}\s+/)) {
      if (currentChunk && currentChunk.length > maxSize / 2) {
        chunks.push(currentChunk.trim());
        currentChunk = section;
      } else {
        currentChunk += '\n\n' + section;
      }
    } else {
      currentChunk += section;
    }
    
    if (currentChunk.length > maxSize) {
      chunks.push(currentChunk.trim());
      currentChunk = '';
    }
  }
  
  if (currentChunk) chunks.push(currentChunk.trim());
  
  return chunks;
}
```

## Code Block Preservation

Don't split code blocks:

```typescript
function chunkWithCodeBlocks(text: string, maxSize = 1000): string[] {
  const codeBlockRegex = /```[\s\S]*?```/g;
  const chunks: string[] = [];
  
  let lastIndex = 0;
  let match;
  
  while ((match = codeBlockRegex.exec(text)) !== null) {
    // Add text before code block
    const beforeCode = text.slice(lastIndex, match.index);
    if (beforeCode) {
      chunks.push(...chunkText(beforeCode, maxSize, 200));
    }
    
    // Add entire code block as one chunk
    chunks.push(match[0]);
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining text
  const remaining = text.slice(lastIndex);
  if (remaining) {
    chunks.push(...chunkText(remaining, maxSize, 200));
  }
  
  return chunks;
}
```

## Token-Based Chunking

For precise token limits:

```typescript
import { encoding_for_model } from 'tiktoken';

function tokenChunk(text: string, maxTokens = 512): string[] {
  const enc = encoding_for_model('gpt-4');
  const tokens = enc.encode(text);
  const chunks: string[] = [];
  
  for (let i = 0; i < tokens.length; i += maxTokens) {
    const chunkTokens = tokens.slice(i, i + maxTokens);
    const chunkText = enc.decode(chunkTokens);
    chunks.push(chunkText);
  }
  
  enc.free();
  return chunks;
}
```

## Recommended Approach for Physical AI Textbook

```typescript
function intelligentChunk(markdownText: string): string[] {
  // 1. Extract frontmatter if exists
  const { content, metadata } = extractFrontmatter(markdownText);
  
  // 2. Split by major sections (## headings)
  const sections = content.split(/^##\s+/gm);
  
  const chunks: string[] = [];
  
  for (const section of sections) {
    if (section.length <= 800) {
      // Small section: keep as is
      chunks.push(section.trim());
    } else {
      // Large section: chunk with overlap, preserving code blocks
      chunks.push(...chunkWithCode Blocks(section, 800));
    }
  }
  
  return chunks;
}
```

## Best Practices

1. **Preserve context**: Use overlap (200-300 chars)
2. **Respect boundaries**: Don't split mid-sentence
3. **Keep code together**: Never split code blocks
4. **Add metadata**: Store chapter/section info
5. **Test chunk quality**: Manually review samples
