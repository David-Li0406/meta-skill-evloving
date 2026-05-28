---
name: langchain
description: Expert LangChain.js - Chains, LCEL, orchestration multi-LLM, agents
---

# LangChain.js Integration

Tu es expert en **LangChain.js** pour l'orchestration de LLMs.

## Setup

```bash
npm install langchain @langchain/openai @langchain/anthropic @langchain/community
```

## LCEL (LangChain Expression Language)

### Basic Chain

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { StringOutputParser } from '@langchain/core/output_parsers';

const model = new ChatOpenAI({ model: 'gpt-4o' });

const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'Tu es un expert en {domain}.'],
  ['user', '{question}'],
]);

const chain = prompt.pipe(model).pipe(new StringOutputParser());

const result = await chain.invoke({
  domain: 'JavaScript',
  question: 'Explique les closures',
});
```

### Streaming

```typescript
const stream = await chain.stream({
  domain: 'JavaScript',
  question: 'Explique les closures',
});

for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

### Structured Output

```typescript
import { z } from 'zod';

const ProductSchema = z.object({
  name: z.string().describe('Nom du produit'),
  price: z.number().describe('Prix en euros'),
  tags: z.array(z.string()).describe('Tags du produit'),
});

const structuredLlm = model.withStructuredOutput(ProductSchema);

const result = await structuredLlm.invoke(
  'Extrais les infos: iPhone 15, 999€, smartphone Apple'
);
// { name: 'iPhone 15', price: 999, tags: ['smartphone', 'Apple'] }
```

## RAG avec LangChain

```typescript
import { ChatOpenAI, OpenAIEmbeddings } from '@langchain/openai';
import { PGVectorStore } from '@langchain/community/vectorstores/pgvector';
import { createRetrievalChain } from 'langchain/chains/retrieval';
import { createStuffDocumentsChain } from 'langchain/chains/combine_documents';

// Embeddings
const embeddings = new OpenAIEmbeddings({
  model: 'text-embedding-3-small',
});

// Vector Store
const vectorStore = await PGVectorStore.initialize(embeddings, {
  postgresConnectionOptions: {
    connectionString: process.env.DATABASE_URL,
  },
  tableName: 'documents',
});

// Retriever
const retriever = vectorStore.asRetriever({
  k: 4,
  searchType: 'similarity',
});

// Chain RAG
const llm = new ChatOpenAI({ model: 'gpt-4o' });

const prompt = ChatPromptTemplate.fromTemplate(`
Reponds a la question en utilisant uniquement le contexte suivant:

{context}

Question: {input}
`);

const documentChain = await createStuffDocumentsChain({
  llm,
  prompt,
});

const retrievalChain = await createRetrievalChain({
  combineDocsChain: documentChain,
  retriever,
});

const result = await retrievalChain.invoke({
  input: 'Quelle est la politique de remboursement ?',
});
```

## Agents

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { tool } from '@langchain/core/tools';
import { z } from 'zod';

// Definir les outils
const weatherTool = tool(
  async ({ city }) => {
    // Appel API meteo
    return `Il fait 20°C a ${city}`;
  },
  {
    name: 'get_weather',
    description: 'Obtenir la meteo pour une ville',
    schema: z.object({
      city: z.string().describe('Nom de la ville'),
    }),
  }
);

const searchTool = tool(
  async ({ query }) => {
    // Appel API recherche
    return `Resultats pour: ${query}`;
  },
  {
    name: 'search',
    description: 'Rechercher sur internet',
    schema: z.object({
      query: z.string().describe('Requete de recherche'),
    }),
  }
);

// Creer l'agent
const model = new ChatOpenAI({ model: 'gpt-4o' });

const agent = createReactAgent({
  llm: model,
  tools: [weatherTool, searchTool],
});

// Executer
const result = await agent.invoke({
  messages: [{ role: 'user', content: 'Quelle est la meteo a Paris ?' }],
});
```

## Document Loaders

```typescript
import { PDFLoader } from '@langchain/community/document_loaders/fs/pdf';
import { TextLoader } from 'langchain/document_loaders/fs/text';
import { DirectoryLoader } from 'langchain/document_loaders/fs/directory';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';

// Charger un PDF
const pdfLoader = new PDFLoader('document.pdf');
const pdfDocs = await pdfLoader.load();

// Charger un dossier
const directoryLoader = new DirectoryLoader('./docs', {
  '.pdf': (path) => new PDFLoader(path),
  '.txt': (path) => new TextLoader(path),
});
const docs = await directoryLoader.load();

// Decouper en chunks
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const chunks = await splitter.splitDocuments(docs);
```

## Memory

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { BufferMemory } from 'langchain/memory';
import { ConversationChain } from 'langchain/chains';

const memory = new BufferMemory();

const chain = new ConversationChain({
  llm: new ChatOpenAI({ model: 'gpt-4o' }),
  memory,
});

await chain.invoke({ input: 'Je m\'appelle Alice' });
const response = await chain.invoke({ input: 'Comment je m\'appelle ?' });
// "Vous vous appelez Alice"
```

## Multi-Provider

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { ChatAnthropic } from '@langchain/anthropic';
import { ChatMistralAI } from '@langchain/mistralai';

// Facile de switcher entre providers
const openai = new ChatOpenAI({ model: 'gpt-4o' });
const claude = new ChatAnthropic({ model: 'claude-sonnet-4-20250514' });
const mistral = new ChatMistralAI({ model: 'mistral-large-latest' });

// Meme interface
const models = [openai, claude, mistral];

for (const model of models) {
  const response = await model.invoke('Hello!');
  console.log(response.content);
}
```

## Callbacks et Tracing

```typescript
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({
  model: 'gpt-4o',
  callbacks: [
    {
      handleLLMStart: (llm, prompts) => {
        console.log('LLM Start:', prompts);
      },
      handleLLMEnd: (output) => {
        console.log('LLM End:', output);
      },
      handleLLMError: (error) => {
        console.error('LLM Error:', error);
      },
    },
  ],
});

// Ou avec LangSmith pour tracing complet
// LANGCHAIN_TRACING_V2=true
// LANGCHAIN_API_KEY=...
```

## Bonnes Pratiques

1. **Utiliser LCEL** plutot que les anciennes chains
2. **Typer avec Zod** pour structured output
3. **Streamer** pour meilleure UX
4. **Activer LangSmith** pour debug
5. **Cacher les embeddings** pour economiser

## Voir Aussi

- `llm/openai` et `llm/claude` pour APIs directes
- `rag/architecture` pour RAG patterns
- `agents/architecture` pour agents complexes
