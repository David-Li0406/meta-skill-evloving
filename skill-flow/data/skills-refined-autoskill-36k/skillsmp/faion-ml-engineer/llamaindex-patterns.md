---
id: llamaindex-patterns
name: "LlamaIndex Patterns"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# LlamaIndex Patterns

## Overview

LlamaIndex (formerly GPT Index) is a data framework for building LLM applications with a focus on RAG (Retrieval-Augmented Generation). It excels at indexing, retrieving, and querying custom data with LLMs.

## When to Use

- Building RAG systems over custom data
- Document Q&A applications
- Knowledge base construction
- Structured data querying
- Multi-document analysis
- When you need advanced retrieval strategies

## Key Concepts

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    LlamaIndex Stack                          │
├─────────────────────────────────────────────────────────────┤
│  Query Engines    - Question answering interfaces           │
│  Indices          - Data structures for retrieval           │
│  Node Parsers     - Document chunking strategies            │
│  Retrievers       - Retrieval algorithms                    │
│  Response Synth.  - Answer generation                       │
│  Data Connectors  - Load data from sources                  │
└─────────────────────────────────────────────────────────────┘
```

### Index Types

| Index | Use Case | Pros | Cons |
|-------|----------|------|------|
| VectorStoreIndex | Semantic search | Fast, accurate | Needs embeddings |
| SummaryIndex | Sequential access | Simple | Slow for large docs |
| TreeIndex | Hierarchical | Good for summaries | Complex |
| KeywordTableIndex | Keyword search | Fast lookup | Less semantic |

## Implementation

### Basic Setup

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure global settings
Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is the main topic?")
print(response)
```

### Document Loading

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import (
    PDFReader,
    DocxReader,
    MarkdownReader
)
from llama_index.readers.web import SimpleWebPageReader

# Load from directory
documents = SimpleDirectoryReader(
    input_dir="./documents",
    recursive=True,
    required_exts=[".txt", ".md", ".pdf"]
).load_data()

# Load specific files
reader = SimpleDirectoryReader(
    input_files=["doc1.pdf", "doc2.txt"]
)
documents = reader.load_data()

# Load from web
web_reader = SimpleWebPageReader()
web_documents = web_reader.load_data(
    urls=["https://example.com/page1", "https://example.com/page2"]
)

# Custom metadata
from llama_index.core import Document

documents = [
    Document(
        text="This is the content",
        metadata={
            "source": "manual",
            "author": "John",
            "date": "2024-01-01"
        }
    )
]

# Load with metadata extractor
from llama_index.core.extractors import (
    TitleExtractor,
    SummaryExtractor,
    KeywordExtractor
)
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        TitleExtractor(),
        SummaryExtractor(),
        KeywordExtractor()
    ]
)

nodes = pipeline.run(documents=documents)
```

### Node Parsing (Chunking)

```python
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
    HierarchicalNodeParser
)

# Sentence splitter (most common)
splitter = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=200
)
nodes = splitter.get_nodes_from_documents(documents)

# Semantic splitter (chunk by semantic similarity)
semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=95,
    embed_model=Settings.embed_model
)
nodes = semantic_splitter.get_nodes_from_documents(documents)

# Hierarchical parser (for nested retrieval)
hierarchical_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]  # Large -> Medium -> Small
)
nodes = hierarchical_parser.get_nodes_from_documents(documents)

# Custom parser
from llama_index.core.node_parser import NodeParser
from llama_index.core.schema import TextNode

class CustomParser(NodeParser):
    def _parse_nodes(self, documents, **kwargs):
        nodes = []
        for doc in documents:
            # Custom parsing logic
            chunks = doc.text.split("\n\n")
            for i, chunk in enumerate(chunks):
                node = TextNode(
                    text=chunk,
                    metadata={**doc.metadata, "chunk_id": i}
                )
                nodes.append(node)
        return nodes
```

### Vector Store Integration

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
import chromadb

# Chroma
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("documents")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Pinecone
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
pinecone_index = pc.Index("your-index")

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Load existing index
from llama_index.core import load_index_from_storage

storage_context = StorageContext.from_defaults(
    persist_dir="./storage"
)
index = load_index_from_storage(storage_context)
```

### Retrieval Strategies

```python
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    KeywordTableSimpleRetriever
)
from llama_index.core.postprocessor import (
    SimilarityPostprocessor,
    KeywordNodePostprocessor,
    SentenceTransformerRerank
)

# Basic retriever
retriever = index.as_retriever(
    similarity_top_k=10
)

# With similarity threshold
retriever = index.as_retriever(
    similarity_top_k=10,
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.7)
    ]
)

# With reranking
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-12-v2",
    top_n=5
)

retriever = index.as_retriever(
    similarity_top_k=20,  # Retrieve more initially
    node_postprocessors=[reranker]
)

# Hybrid retrieval
from llama_index.core.retrievers import QueryFusionRetriever

vector_retriever = index.as_retriever(similarity_top_k=10)
keyword_retriever = KeywordTableSimpleRetriever(index)

fusion_retriever = QueryFusionRetriever(
    retrievers=[vector_retriever, keyword_retriever],
    similarity_top_k=10,
    num_queries=4,  # Generate multiple query variations
    mode="reciprocal_rerank"
)

# Auto-merging retriever (for hierarchical)
from llama_index.core.retrievers import AutoMergingRetriever

auto_merging_retriever = AutoMergingRetriever(
    index.as_retriever(similarity_top_k=12),
    storage_context=index.storage_context
)
```

### Query Engines

```python
from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

# Basic query engine
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact"  # or "tree_summarize", "refine"
)

# Custom query engine
retriever = index.as_retriever(similarity_top_k=10)
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize"
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer
)

# With custom prompt
from llama_index.core import PromptTemplate

custom_prompt = PromptTemplate(
    """Context information is below.
---------------------
{context_str}
---------------------
Given the context, answer the question: {query_str}
If the context doesn't contain the answer, say "I don't know".
"""
)

query_engine = index.as_query_engine(
    text_qa_template=custom_prompt
)

# Streaming
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("What is the main topic?")

for text in streaming_response.response_gen:
    print(text, end="", flush=True)
```

### Chat Engine

```python
from llama_index.core.memory import ChatMemoryBuffer

# Simple chat
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    verbose=True
)

response = chat_engine.chat("What is this document about?")
print(response)

response = chat_engine.chat("Can you tell me more?")
print(response)

# With memory
memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt="You are a helpful assistant answering questions about documents."
)

# Chat modes:
# - "condense_question": Condense follow-up with history
# - "context": Add context to each query
# - "condense_plus_context": Both
# - "simple": No context augmentation
# - "react": ReAct agent with tools
```

### Agents

```python
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

# Create tools from indices
wiki_tool = QueryEngineTool(
    query_engine=wiki_index.as_query_engine(),
    metadata=ToolMetadata(
        name="wikipedia",
        description="Use for general knowledge questions"
    )
)

docs_tool = QueryEngineTool(
    query_engine=docs_index.as_query_engine(),
    metadata=ToolMetadata(
        name="documentation",
        description="Use for questions about our product"
    )
)

# Create agent
agent = ReActAgent.from_tools(
    tools=[wiki_tool, docs_tool],
    llm=Settings.llm,
    verbose=True,
    max_iterations=10
)

response = agent.chat("How does our product compare to alternatives?")

# With custom tools
from llama_index.core.tools import FunctionTool

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(eval(expression))

calc_tool = FunctionTool.from_defaults(fn=calculate)

agent = ReActAgent.from_tools(
    tools=[wiki_tool, calc_tool],
    llm=Settings.llm
)
```

### Multi-Document Queries

```python
from llama_index.core import (
    SummaryIndex,
    VectorStoreIndex
)
from llama_index.core.tools import QueryEngineTool

# Create index per document
indices = {}
for doc_name, doc_text in documents.items():
    doc = Document(text=doc_text, metadata={"name": doc_name})
    indices[doc_name] = VectorStoreIndex.from_documents([doc])

# Create tools
tools = [
    QueryEngineTool(
        query_engine=idx.as_query_engine(),
        metadata=ToolMetadata(
            name=name,
            description=f"Use to query {name}"
        )
    )
    for name, idx in indices.items()
]

# Use agent to route
agent = ReActAgent.from_tools(tools, llm=Settings.llm)
response = agent.chat("Compare the main topics across all documents")

# Or use SubQuestionQueryEngine
from llama_index.core.query_engine import SubQuestionQueryEngine

sub_question_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    llm=Settings.llm
)

response = sub_question_engine.query(
    "What are the similarities and differences?"
)
```

### Structured Data Queries

```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine

# Connect to database
engine = create_engine("sqlite:///database.db")
sql_database = SQLDatabase(engine, include_tables=["users", "orders"])

# Create query engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["users", "orders"]
)

response = query_engine.query(
    "How many orders were placed last month?"
)
print(response.response)
print(response.metadata["sql_query"])  # See generated SQL

# With table descriptions
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_index = ObjectIndex.from_objects(
    objects=table_node_mapping.get_objects(),
    index_cls=VectorStoreIndex
)

query_engine = SQLTableRetrieverQueryEngine(
    sql_database=sql_database,
    table_retriever=table_schema_index.as_retriever()
)
```

### Evaluation

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator
)

# Faithfulness - is answer grounded in context?
faithfulness_evaluator = FaithfulnessEvaluator()
result = faithfulness_evaluator.evaluate_response(response=response)
print(f"Faithfulness: {result.passing}")

# Relevancy - is answer relevant to query?
relevancy_evaluator = RelevancyEvaluator()
result = relevancy_evaluator.evaluate_response(
    query="What is the topic?",
    response=response
)
print(f"Relevancy: {result.score}")

# Correctness - does answer match reference?
correctness_evaluator = CorrectnessEvaluator()
result = correctness_evaluator.evaluate(
    query="What is 2+2?",
    response="4",
    reference="4"
)
print(f"Correctness: {result.score}")

# Batch evaluation
from llama_index.core.evaluation import BatchEvalRunner

eval_runner = BatchEvalRunner(
    evaluators={
        "faithfulness": faithfulness_evaluator,
        "relevancy": relevancy_evaluator
    }
)

eval_results = eval_runner.evaluate_queries(
    query_engine,
    queries=["Q1", "Q2", "Q3"]
)
```

### Production Patterns

```python
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
import logging

# Logging
logging.basicConfig(level=logging.INFO)

# Debug handler
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])

Settings.callback_manager = callback_manager

# Caching
from llama_index.core import set_global_handler

# Enable caching
set_global_handler("simple")

# Or with Redis
from llama_index.storage.kvstore.redis import RedisKVStore

kvstore = RedisKVStore(redis_uri="redis://localhost:6379")

# Async
query_engine = index.as_query_engine()
response = await query_engine.aquery("What is the topic?")

# Batch queries
from llama_index.core import QueryBundle

queries = [
    QueryBundle(query_str="Question 1"),
    QueryBundle(query_str="Question 2")
]

responses = await query_engine.abatch_query(queries)
```

## Best Practices

1. **Index Selection**
   - VectorStoreIndex for most use cases
   - SummaryIndex for full document access
   - Use hierarchical for long documents

2. **Chunking Strategy**
   - Start with SentenceSplitter
   - Use semantic splitter for better coherence
   - Tune chunk size based on query patterns

3. **Retrieval Optimization**
   - Retrieve more, rerank to top-k
   - Use hybrid retrieval for robustness
   - Apply similarity thresholds

4. **Response Quality**
   - Use tree_summarize for long contexts
   - Custom prompts for specific tasks
   - Evaluate with built-in evaluators

5. **Production**
   - Enable caching
   - Use async for concurrent queries
   - Monitor with callbacks

## Common Pitfalls

1. **Wrong Index Type** - Using VectorStore when Summary is better
2. **Poor Chunking** - Chunks too large or too small
3. **No Reranking** - Relying only on vector similarity
4. **Ignoring Metadata** - Not using filters
5. **No Evaluation** - Deploying without testing
6. **Memory Issues** - Loading too many documents at once

## References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaIndex Hub](https://llamahub.ai/)
