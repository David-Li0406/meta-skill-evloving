# RAG (Retrieval Augmented Generation) Patterns

**Category**: ai-ml/patterns
**Description**: Detection patterns for RAG implementations and vector database usage

## Overview

RAG combines retrieval systems with generative AI to ground responses in specific knowledge. This pattern detects RAG implementations across various frameworks and vector stores.

## Vector Database Patterns

### Pinecone
**Pattern**: `from pinecone import|import pinecone`
- Pinecone client import
- Example: `from pinecone import Pinecone, ServerlessSpec`

**Pattern**: `pinecone\.init\(|Pinecone\(`
- Client initialization
- Example: `pc = Pinecone(api_key="...")`

**Pattern**: `\.upsert\(|\.query\(`
- Vector operations
- Example: `index.upsert(vectors=[...])`, `index.query(vector=[...], top_k=5)`

### Weaviate
**Pattern**: `import weaviate|from weaviate import`
- Weaviate client import
- Example: `import weaviate`

**Pattern**: `weaviate\.Client\(|weaviate\.connect_to`
- Client connection
- Example: `client = weaviate.connect_to_local()`

**Pattern**: `\.near_vector\(|\.near_text\(`
- Similarity search
- Example: `collection.query.near_text(query="...", limit=5)`

### Qdrant
**Pattern**: `from qdrant_client import|import qdrant_client`
- Qdrant client import
- Example: `from qdrant_client import QdrantClient`

**Pattern**: `QdrantClient\(`
- Client initialization
- Example: `client = QdrantClient(url="...")`

**Pattern**: `\.search\(|\.upsert\(`
- Vector operations
- Example: `client.search(collection_name="...", query_vector=[...])`

### ChromaDB
**Pattern**: `import chromadb|from chromadb import`
- ChromaDB import
- Example: `import chromadb`

**Pattern**: `chromadb\.Client\(|chromadb\.PersistentClient\(`
- Client initialization
- Example: `client = chromadb.PersistentClient(path="./chroma")`

**Pattern**: `\.add\(|\.query\(`
- Collection operations
- Example: `collection.query(query_texts=["..."], n_results=5)`

### pgvector (PostgreSQL)
**Pattern**: `from pgvector|pgvector\.sqlalchemy`
- pgvector extensions
- Example: `from pgvector.sqlalchemy import Vector`

**Pattern**: `<->|<#>|<=>`
- pgvector distance operators
- Example: `ORDER BY embedding <-> query_embedding LIMIT 5`

### FAISS
**Pattern**: `import faiss|from faiss import`
- FAISS import
- Example: `import faiss`

**Pattern**: `faiss\.IndexFlatL2|faiss\.IndexIVF`
- Index creation
- Example: `index = faiss.IndexFlatL2(dimension)`

**Pattern**: `\.search\(.*k=|\.add\(`
- Vector operations
- Example: `distances, indices = index.search(query, k=5)`

## Embedding Patterns

### OpenAI Embeddings
**Pattern**: `text-embedding-ada|text-embedding-3`
- OpenAI embedding models
- Example: `model="text-embedding-3-small"`

**Pattern**: `\.embeddings\.create\(`
- Embedding API call
- Example: `openai.embeddings.create(input="...", model="...")`

### Sentence Transformers
**Pattern**: `from sentence_transformers import|SentenceTransformer\(`
- Sentence transformers library
- Example: `model = SentenceTransformer('all-MiniLM-L6-v2')`

**Pattern**: `\.encode\(`
- Encoding text to vectors
- Example: `embeddings = model.encode(documents)`

### Cohere Embeddings
**Pattern**: `embed_model|co\.embed\(`
- Cohere embedding API
- Example: `response = co.embed(texts=[...], model="embed-english-v3.0")`

### Voyage AI
**Pattern**: `voyageai|voyage\.embed`
- Voyage AI embeddings
- Example: `vo.embed(texts, model="voyage-2")`

## LangChain RAG Patterns

**Pattern**: `from langchain.*vectorstores|from langchain.*embeddings`
- LangChain vector store integrations
- Example: `from langchain_community.vectorstores import Chroma`

**Pattern**: `RetrievalQA|ConversationalRetrievalChain`
- RAG chain implementations
- Example: `qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)`

**Pattern**: `as_retriever\(\)|\.retriever`
- Retriever creation
- Example: `retriever = vectorstore.as_retriever(search_kwargs={"k": 5})`

**Pattern**: `create_retrieval_chain|create_stuff_documents_chain`
- LCEL RAG chains
- Example: `chain = create_retrieval_chain(retriever, document_chain)`

## LlamaIndex RAG Patterns

**Pattern**: `from llama_index|import llama_index`
- LlamaIndex import
- Example: `from llama_index.core import VectorStoreIndex`

**Pattern**: `VectorStoreIndex\.from_documents`
- Index creation
- Example: `index = VectorStoreIndex.from_documents(documents)`

**Pattern**: `\.as_query_engine\(|\.as_chat_engine\(`
- Query/chat engine creation
- Example: `query_engine = index.as_query_engine()`

**Pattern**: `SimpleDirectoryReader|Document\(`
- Document loading
- Example: `documents = SimpleDirectoryReader("./data").load_data()`

## RAG Architecture Components

### Document Processing
**Pattern**: `RecursiveCharacterTextSplitter|CharacterTextSplitter`
- Text chunking
- Example: `splitter = RecursiveCharacterTextSplitter(chunk_size=1000)`

**Pattern**: `chunk_size|chunk_overlap`
- Chunking configuration
- Example: `chunk_size=1000, chunk_overlap=200`

### Retrieval Patterns
**Pattern**: `similarity_search|max_marginal_relevance`
- Search strategies
- Example: `docs = vectorstore.similarity_search(query, k=5)`

**Pattern**: `top_k|n_results|limit`
- Result limiting
- Example: `top_k=5` or `n_results=10`

### Context Assembly
**Pattern**: `format_docs|_combine_documents`
- Document formatting for LLM
- Example: `context = "\n\n".join(doc.page_content for doc in docs)`

## Usage Classification

### RAG Maturity Levels

1. **Basic RAG**: Single vector store, simple retrieval
2. **Advanced RAG**: Hybrid search, re-ranking, metadata filtering
3. **Modular RAG**: Pluggable components, multiple retrievers
4. **Agentic RAG**: Agent-driven retrieval decisions

### Architecture Indicators

- **Naive RAG**: Direct query → retrieve → generate
- **Advanced RAG**: Query rewriting, HyDE, multi-query
- **Production RAG**: Caching, evaluation, monitoring

## Detection Confidence

- **Vector Database Detection**: 95% (HIGH)
- **Embedding Detection**: 90% (HIGH)
- **Framework Detection**: 95% (HIGH)
- **Architecture Analysis**: 75% (MEDIUM)

## Security Considerations

- Vector databases may contain sensitive document embeddings
- API keys for embedding services need protection
- Document sources should be validated
- Query injection attacks possible through retrieval
- PII may be exposed through retrieved context
