# Agent Memory Systems

## Patterns


---
  #### **Name**
Memory Type Architecture
  #### **Description**
Choosing the right memory type for different information
  #### **When**
Designing agent memory system
  #### **Example**
    # MEMORY TYPE ARCHITECTURE (CoALA Framework):
    
    """
    Three memory types for different purposes:
    
    1. Semantic Memory: Facts and knowledge
       - What you know about the world
       - User preferences, domain knowledge
       - Stored in profiles (structured) or collections (unstructured)
    
    2. Episodic Memory: Experiences and events
       - What happened (timestamped events)
       - Past conversations, task outcomes
       - Used for learning from experience
    
    3. Procedural Memory: How to do things
       - Rules, skills, workflows
       - Often implemented as few-shot examples
       - "How did I solve this before?"
    """
    
    ## LangMem Implementation
    """
    from langmem import MemoryStore
    from langgraph.graph import StateGraph
    
    # Initialize memory store
    memory = MemoryStore(
        connection_string=os.environ["POSTGRES_URL"]
    )
    
    # Semantic memory: user profile
    await memory.semantic.upsert(
        namespace="user_profile",
        key=user_id,
        content={
            "name": "Alice",
            "preferences": ["dark mode", "concise responses"],
            "expertise_level": "developer",
        }
    )
    
    # Episodic memory: past interaction
    await memory.episodic.add(
        namespace="conversations",
        content={
            "timestamp": datetime.now(),
            "summary": "Helped debug authentication issue",
            "outcome": "resolved",
            "key_insights": ["Token expiry was root cause"],
        },
        metadata={"user_id": user_id, "topic": "debugging"}
    )
    
    # Procedural memory: learned pattern
    await memory.procedural.add(
        namespace="skills",
        content={
            "task_type": "debug_auth",
            "steps": ["Check token expiry", "Verify refresh flow"],
            "example_interaction": few_shot_example,
        }
    )
    """
    
    ## Memory Retrieval at Runtime
    """
    async def prepare_context(user_id, query):
        # Get user profile (semantic)
        profile = await memory.semantic.get(
            namespace="user_profile",
            key=user_id
        )
    
        # Find relevant past experiences (episodic)
        similar_experiences = await memory.episodic.search(
            namespace="conversations",
            query=query,
            filter={"user_id": user_id},
            limit=3
        )
    
        # Find relevant skills (procedural)
        relevant_skills = await memory.procedural.search(
            namespace="skills",
            query=query,
            limit=2
        )
    
        return {
            "profile": profile,
            "past_experiences": similar_experiences,
            "relevant_skills": relevant_skills,
        }
    """
    

---
  #### **Name**
Vector Store Selection Pattern
  #### **Description**
Choosing the right vector database for your use case
  #### **When**
Setting up persistent memory storage
  #### **Example**
    # VECTOR STORE SELECTION:
    
    """
    Decision matrix:
    
    |            | Pinecone | Qdrant | Weaviate | ChromaDB | pgvector |
    |------------|----------|--------|----------|----------|----------|
    | Scale      | Billions | 100M+  | 100M+    | 1M       | 1M       |
    | Managed    | Yes      | Both   | Both     | Self     | Self     |
    | Filtering  | Basic    | Best   | Good     | Basic    | SQL      |
    | Hybrid     | No       | Yes    | Best     | No       | Yes      |
    | Cost       | High     | Medium | Medium   | Free     | Free     |
    | Latency    | 5ms      | 7ms    | 10ms     | 20ms     | 15ms     |
    """
    
    ## Pinecone (Enterprise Scale)
    """
    from pinecone import Pinecone
    
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("agent-memory")
    
    # Upsert with metadata
    index.upsert(
        vectors=[
            {
                "id": f"memory-{uuid4()}",
                "values": embedding,
                "metadata": {
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "type": "episodic",
                    "content": memory_text,
                }
            }
        ],
        namespace=namespace
    )
    
    # Query with filter
    results = index.query(
        vector=query_embedding,
        filter={"user_id": user_id, "type": "episodic"},
        top_k=5,
        include_metadata=True
    )
    """
    
    ## Qdrant (Complex Filtering)
    """
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Filter, FieldCondition
    
    client = QdrantClient(url="http://localhost:6333")
    
    # Complex filtering with Qdrant
    results = client.search(
        collection_name="agent_memory",
        query_vector=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(key="user_id", match={"value": user_id}),
                FieldCondition(key="type", match={"value": "semantic"}),
            ],
            should=[
                FieldCondition(key="topic", match={"any": ["auth", "security"]}),
            ]
        ),
        limit=5
    )
    """
    
    ## ChromaDB (Prototyping)
    """
    import chromadb
    
    client = chromadb.PersistentClient(path="./memory_db")
    collection = client.get_or_create_collection("agent_memory")
    
    # Simple and fast for prototypes
    collection.add(
        ids=[str(uuid4())],
        embeddings=[embedding],
        documents=[memory_text],
        metadatas=[{"user_id": user_id, "type": "episodic"}]
    )
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"user_id": user_id}
    )
    """
    

---
  #### **Name**
Chunking Strategy Pattern
  #### **Description**
Breaking documents into retrievable chunks
  #### **When**
Processing documents for memory storage
  #### **Example**
    # CHUNKING STRATEGIES:
    
    """
    The chunking dilemma:
    - Too large: Vector loses specificity
    - Too small: Loses context
    
    Optimal chunk size depends on:
    - Document type (code vs prose vs data)
    - Query patterns (factual vs exploratory)
    - Embedding model (each has sweet spot)
    
    General guidance: 256-512 tokens for most use cases
    """
    
    ## Fixed-Size Chunking (Baseline)
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Characters
        chunk_overlap=50,    # Overlap prevents cutting sentences
        separators=["\n\n", "\n", ". ", " ", ""]  # Priority order
    )
    
    chunks = splitter.split_text(document)
    """
    
    ## Semantic Chunking (Better Quality)
    """
    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_openai import OpenAIEmbeddings
    
    # Splits based on semantic similarity
    splitter = SemanticChunker(
        embeddings=OpenAIEmbeddings(),
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95
    )
    
    chunks = splitter.split_text(document)
    """
    
    ## Structure-Aware Chunking (Documents with Hierarchy)
    """
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    
    # Respect document structure
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
    )
    
    chunks = splitter.split_text(markdown_doc)
    # Each chunk has header metadata for context
    """
    
    ## Contextual Chunking (Anthropic's Approach)
    """
    # Add context to each chunk before embedding
    # Reduces retrieval failures by 35%
    
    def add_context_to_chunk(chunk, document_summary):
        context_prompt = f'''
        Document summary: {document_summary}
    
        The following is a chunk from this document:
        {chunk}
        '''
        return context_prompt
    
    # Embed the contextualized chunk, not raw chunk
    for chunk in chunks:
        contextualized = add_context_to_chunk(chunk, summary)
        embedding = embed(contextualized)
        store(chunk, embedding)  # Store original, embed contextualized
    """
    
    ## Code-Specific Chunking
    """
    from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
    
    # Language-aware splitting
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Respects function/class boundaries
    chunks = python_splitter.split_text(python_code)
    """
    

---
  #### **Name**
Background Memory Formation
  #### **Description**
Processing memories asynchronously for better quality
  #### **When**
You want higher recall without slowing interactions
  #### **Example**
    # BACKGROUND MEMORY FORMATION:
    
    """
    Real-time memory extraction slows conversations and adds
    complexity to agent tool calls. Background processing after
    conversations yields higher quality memories.
    
    Pattern: Subconscious memory formation
    """
    
    ## LangGraph Background Processing
    """
    from langgraph.graph import StateGraph
    from langgraph.checkpoint.postgres import PostgresSaver
    
    async def background_memory_processor(thread_id: str):
        # Run after conversation ends or goes idle
        conversation = await load_conversation(thread_id)
    
        # Extract insights without time pressure
        insights = await llm.invoke('''
            Analyze this conversation and extract:
            1. Key facts learned about the user
            2. User preferences revealed
            3. Tasks completed or pending
            4. Patterns in user behavior
    
            Be thorough - this runs in background.
    
            Conversation:
            {conversation}
        ''')
    
        # Store to long-term memory
        for insight in insights:
            await memory.semantic.upsert(
                namespace="user_insights",
                key=generate_key(insight),
                content=insight,
                metadata={"source_thread": thread_id}
            )
    
    # Trigger on conversation end or idle timeout
    @on_conversation_idle(timeout_minutes=5)
    async def process_conversation(thread_id):
        await background_memory_processor(thread_id)
    """
    
    ## Memory Consolidation (Like Sleep)
    """
    # Periodically consolidate and deduplicate memories
    
    async def consolidate_memories(user_id: str):
        # Get all memories for user
        memories = await memory.semantic.list(
            namespace="user_insights",
            filter={"user_id": user_id}
        )
    
        # Find similar memories (potential duplicates)
        clusters = cluster_by_similarity(memories, threshold=0.9)
    
        # Merge similar memories
        for cluster in clusters:
            if len(cluster) > 1:
                merged = await llm.invoke(f'''
                    Consolidate these related memories into one:
                    {cluster}
    
                    Preserve all important information.
                ''')
                await memory.semantic.upsert(
                    namespace="user_insights",
                    key=generate_key(merged),
                    content=merged
                )
                # Delete originals
                for old in cluster:
                    await memory.semantic.delete(old.id)
    """
    

---
  #### **Name**
Memory Decay Pattern
  #### **Description**
Forgetting old, irrelevant memories
  #### **When**
Memory grows large, retrieval slows down
  #### **Example**
    # MEMORY DECAY:
    
    """
    Not all memories should live forever:
    - Old preferences may be outdated
    - Task details lose relevance
    - Conflicting memories confuse retrieval
    
    Implement intelligent decay based on:
    - Recency (when was it created/accessed?)
    - Frequency (how often is it retrieved?)
    - Importance (is it a core fact or detail?)
    """
    
    ## Time-Based Decay
    """
    from datetime import datetime, timedelta
    
    async def decay_old_memories(namespace: str, max_age_days: int):
        cutoff = datetime.now() - timedelta(days=max_age_days)
    
        old_memories = await memory.episodic.list(
            namespace=namespace,
            filter={"last_accessed": {"$lt": cutoff.isoformat()}}
        )
    
        for mem in old_memories:
            # Soft delete (mark as archived)
            await memory.episodic.update(
                id=mem.id,
                metadata={"archived": True, "archived_at": datetime.now()}
            )
    """
    
    ## Utility-Based Decay (MIRIX Approach)
    """
    def calculate_memory_utility(memory):
        '''
        Composite utility score inspired by cognitive science:
        - Recency: When was it last accessed?
        - Frequency: How often is it accessed?
        - Importance: How critical is this information?
        '''
        now = datetime.now()
    
        # Recency score (exponential decay with 72h half-life)
        hours_since_access = (now - memory.last_accessed).total_seconds() / 3600
        recency_score = 0.5 ** (hours_since_access / 72)
    
        # Frequency score
        frequency_score = min(memory.access_count / 10, 1.0)
    
        # Importance (from metadata or heuristic)
        importance = memory.metadata.get("importance", 0.5)
    
        # Weighted combination
        utility = (
            0.4 * recency_score +
            0.3 * frequency_score +
            0.3 * importance
        )
    
        return utility
    
    async def prune_low_utility_memories(threshold=0.2):
        all_memories = await memory.list_all()
        for mem in all_memories:
            if calculate_memory_utility(mem) < threshold:
                await memory.archive(mem.id)
    """
    

## Anti-Patterns


---
  #### **Name**
Store Everything Forever
  #### **Description**
Never deleting or archiving memories
  #### **Why**
    Memory bloat slows retrieval, increases costs, and introduces
    noise. Outdated memories can conflict with current facts.
    Infinite storage isn't infinite retrieval.
    
  #### **Instead**
    Implement decay policies. Archive old episodic memories.
    Consolidate duplicate semantic memories. Test retrieval
    quality as memory grows.
    

---
  #### **Name**
Chunk Without Testing Retrieval
  #### **Description**
Choosing chunk size without measuring retrieval accuracy
  #### **Why**
    Chunking destroys context. The "right" chunk size varies by
    document type, query pattern, and embedding model. Without
    testing, you're guessing.
    
  #### **Instead**
    Create retrieval test sets. Measure recall@k for different
    chunk sizes. Optimize for your actual queries.
    

---
  #### **Name**
Single Memory Type for All Data
  #### **Description**
Storing everything as generic "memories"
  #### **Why**
    Different information needs different treatment. User profile
    (structured, small) shouldn't be stored like conversation
    history (unstructured, large).
    
  #### **Instead**
    Use CoALA types: semantic for facts, episodic for events,
    procedural for skills. Each has different storage and
    retrieval patterns.
    

---
  #### **Name**
Real-Time Memory Formation
  #### **Description**
Extracting memories during conversation
  #### **Why**
    Real-time extraction adds latency, complicates tool calls,
    and produces lower quality memories under time pressure.
    Users notice the delay.
    
  #### **Instead**
    Use background/subconscious memory formation. Process
    conversations after they end or go idle. Higher quality,
    no latency impact.
    

---
  #### **Name**
Ignoring Memory Conflicts
  #### **Description**
Storing contradictory facts without resolution
  #### **Why**
    "User prefers dark mode" and "user prefers light mode" both
    retrieved creates confusion. Agent gives inconsistent answers.
    
  #### **Instead**
    Detect conflicts on storage. Either replace (for preferences)
    or version (for temporal facts). Consolidate periodically.
    