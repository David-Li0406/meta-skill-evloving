# Content Ingestion Script for RAG Pipeline

This script reads all Docusaurus markdown files, chunks them, generates embeddings, and stores them in Qdrant.

## Full Ingestion Script

```typescript
// scripts/ingest-content.ts
import fs from 'fs';
import path from 'path';
import { QdrantClient } from '@qdrant/js-client';
import OpenAI from 'openai';

const qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

interface Chunk {
  id: string;
  text: string;
 metadata: {
    file: string;
    chapter: string;
    section: string;
    chunkIndex: number;
  };
}

// 1. Text Chunking
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

// 2. Find All Markdown Files
function getAllMarkdownFiles(dir: string): string[] {
  const files: string[] = [];
  
  function traverse(currentPath: string) {
    const entries = fs.readdirSync(currentPath, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      
      if (entry.isDirectory()) {
        traverse(fullPath);
      } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
        files.push(fullPath);
      }
    }
  }
  
  traverse(dir);
  return files;
}

// 3. Extract Metadata from File Path
function extractMetadata(filePath: string) {
  const parts = filePath.split(path.sep);
  
  // Example: docs/physical-ai-book/chapter2/ros2-architecture.md
  const chapter = parts.find(p => p.startsWith('chapter')) || 'intro';
  const section = path.basename(filePath, path.extname(filePath));
  
  return {
    chapter: chapter.replace('chapter', 'Chapter '),
    section: section.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
  };
}

// 4. Generate Embedding
async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text.trim(),
  });
  
  return response.data[0].embedding;
}

// 5. Batch Upsert to Qdrant
async function upsertBatch(chunks: Chunk[]) {
  const points = await Promise.all(
    chunks.map(async (chunk) => {
      const embedding = await generateEmbedding(chunk.text);
      
      return {
        id: chunk.id,
        vector: embedding,
        payload: {
          text: chunk.text,
          ...chunk.metadata,
        },
      };
    })
  );
  
  await qdrant.upsert('textbook_chunks', { points });
}

// 6. Main Ingestion Function
async function ingestContent() {
  console.log('Starting content ingestion...');
  
  // Ensure collection exists
  try {
    await qdrant.getCollection('textbook_chunks');
  } catch {
    console.log('Creating collection...');
    await qdrant.createCollection('textbook_chunks', {
      vectors: { size: 1536, distance: 'Cosine' },
    });
  }
  
  const docsDir = path.join(__dirname, '../docs');
  const files = getAllMarkdownFiles(docsDir);
  
  console.log(`Found ${files.length} markdown files`);
  
  let totalChunks = 0;
  const batchSize = 10; // Process 10 files at a time
  
  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);
    
    const chunksPromises = batch.map(async (file) => {
      const content = fs.readFileSync(file, 'utf-8');
      const metadata = extractMetadata(file);
      const textChunks = chunkText(content);
      
      return textChunks.map((text, index) => ({
        id: `${path.basename(file)}-chunk-${index}`,
        text,
        metadata: {
          file: path.relative(docsDir, file),
          ...metadata,
          chunkIndex: index,
        },
      }));
    });
    
    const chunks = (await Promise.all(chunksPromises)).flat();
    await upsertBatch(chunks);
    
    totalChunks += chunks.length;
    console.log(`Processed ${i + batch.length}/${files.length} files (${totalChunks} chunks)`);
  }
  
  console.log(`✅ Ingestion complete! Total chunks: ${totalChunks}`);
}

// Run
ingestContent().catch(console.error);
```

## Running the Script

### 1. Add to package.json
```json
{
  "scripts": {
    "ingest": "tsx scripts/ingest-content.ts"
  }
}
```

### 2. Install Dependencies
```bash
npm install tsx @qdrant/js-client openai
```

### 3. Set Environment Variables
```bash
export QDRANT_URL="http://localhost:6333"
export OPENAI_API_KEY="sk-..."
```

### 4. Run Ingestion
```bash
npm run ingest
```

## Incremental Updates

To re-index specific files:

```typescript
async function reindexFile(filePath: string) {
  // 1. Delete old chunks
  await qdrant.delete('textbook_chunks', {
    filter: {
      must: [{ key: 'file', match: { value: filePath } }],
    },
  });
  
  // 2. Re-chunk and re-index
  const content = fs.readFileSync(filePath, 'utf-8');
  const chunks = chunkText(content);
  // ... rest of indexing logic
}
```

## Monitoring

```typescript
async function getIngestionStats() {
  const collection = await qdrant.getCollection('textbook_chunks');
  
  console.log(`Total vectors: ${collection.points_count}`);
  console.log(`Indexed segments: ${collection.segments_count}`);
}
```

## Error Handling

```typescript
async function upsertWithRetry(chunks: Chunk[], maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await upsertBatch(chunks);
      return;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      console.warn(`Attempt ${attempt} failed, retrying...`);
      await new Promise(r => setTimeout(r, 1000 * attempt)); // Exponential backoff
    }
  }
}
```

## Cost Estimation

For a typical textbook (500 pages):
- ~1500 chunks
- Embedding cost: 1500 * $0.0001 / 1K tokens = ~$0.15
- Storage: 1500 * 1536 * 4 bytes = ~9MB
