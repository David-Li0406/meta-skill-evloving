# Agent Memory Systems - Sharp Edges

## Chunking Isolates Information From Its Context

### **Id**
chunking-destroys-context
### **Severity**
critical
### **Situation**
Processing documents for vector storage
### **Symptom**
  Retrieval finds chunks but they don't make sense alone. Agent
  answers miss the big picture. "The function returns X" retrieved
  without knowing which function. References to "this" without
  knowing what "this" refers to.
  
### **Why**
  When we chunk for AI processing, we're breaking connections,
  reducing a holistic narrative to isolated fragments that often
  miss the big picture. A chunk about "the configuration" without
  context about what system is being configured is nearly useless.
  
### **Solution**
  ## Contextual Chunking (Anthropic's approach)
  # Add document context to each chunk before embedding
  # Reduces retrieval failures by 35%
  
  def contextualize_chunk(chunk, document):
      summary = summarize(document)
  
      # LLM generates context for chunk
      context = llm.invoke(f'''
          Document summary: {summary}
  
          Generate a brief context statement for this chunk
          that would help someone understand what it refers to:
  
          {chunk}
      ''')
  
      return f"{context}\n\n{chunk}"
  
  # Embed the contextualized version
  for chunk in chunks:
      contextualized = contextualize_chunk(chunk, full_doc)
      embedding = embed(contextualized)
      # Store original chunk, embed contextualized
      store(original=chunk, embedding=embedding)
  
  ## Hierarchical Chunking
  # Store at multiple granularities
  chunks_small = split(doc, size=256)
  chunks_medium = split(doc, size=512)
  chunks_large = split(doc, size=1024)
  
  # Retrieve at appropriate level based on query
  
### **Detection Pattern**
  - chunk
  - split
  - context
  - retrieval

## Chunk Size Mismatched to Query Patterns

### **Id**
wrong-chunk-size
### **Severity**
high
### **Situation**
Configuring chunking for memory storage
### **Symptom**
  High-quality documents produce low-quality retrievals. Simple
  questions miss relevant information. Complex questions get
  fragments instead of complete answers.
  
### **Why**
  Optimal chunk size depends on query patterns:
  - Factual queries need small, specific chunks
  - Conceptual queries need larger context
  - Code needs function-level boundaries
  
  The sweet spot varies by document type and embedding model.
  Default 1000 characters works for nothing specific.
  
### **Solution**
  ## Test different sizes
  from sklearn.metrics import recall_score
  
  def evaluate_chunk_size(documents, test_queries, chunk_size):
      chunks = split_documents(documents, size=chunk_size)
      index = build_index(chunks)
  
      correct_retrievals = 0
      for query, expected_chunk in test_queries:
          results = index.search(query, k=5)
          if expected_chunk in results:
              correct_retrievals += 1
  
      return correct_retrievals / len(test_queries)
  
  # Test multiple sizes
  for size in [256, 512, 768, 1024]:
      recall = evaluate_chunk_size(docs, test_queries, size)
      print(f"Size {size}: Recall@5 = {recall:.2%}")
  
  ## Size recommendations by content type
  CHUNK_SIZES = {
      "documentation": 512,   # Complete concepts
      "code": 1000,          # Function-level
      "conversation": 256,   # Turn-level
      "articles": 768,       # Paragraph-level
  }
  
  ## Use overlap to prevent boundary issues
  splitter = RecursiveCharacterTextSplitter(
      chunk_size=512,
      chunk_overlap=50,  # 10% overlap
  )
  
### **Detection Pattern**
  - chunk_size
  - split
  - characters
  - tokens

## Semantic Search Returns Irrelevant Results

### **Id**
retrieval-returns-wrong-memories
### **Severity**
high
### **Situation**
Querying memory for context
### **Symptom**
  Agent retrieves memories that seem related but aren't useful.
  "Tell me about the user's preferences" returns conversation
  about preferences in general, not this user's. High similarity
  scores for wrong content.
  
### **Why**
  Semantic similarity isn't the same as relevance. "The user
  likes Python" and "Python is a programming language" are
  semantically similar but very different types of information.
  Without metadata filtering, retrieval is just word matching.
  
### **Solution**
  ## Always filter by metadata first
  # Don't rely on semantic similarity alone
  
  # Bad: Only semantic search
  results = index.query(
      vector=query_embedding,
      top_k=5
  )
  
  # Good: Filter then search
  results = index.query(
      vector=query_embedding,
      filter={
          "user_id": current_user.id,
          "type": "preference",
          "created_after": cutoff_date,
      },
      top_k=5
  )
  
  ## Use hybrid search (semantic + keyword)
  from qdrant_client import QdrantClient
  
  client = QdrantClient(...)
  
  # Hybrid search with fusion
  results = client.search(
      collection_name="memories",
      query_vector=semantic_embedding,
      query_text=query,  # Also keyword match
      fusion={"method": "rrf"},  # Reciprocal Rank Fusion
  )
  
  ## Rerank results with cross-encoder
  from sentence_transformers import CrossEncoder
  
  reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
  
  # Initial retrieval (recall-oriented)
  candidates = index.query(query_embedding, top_k=20)
  
  # Rerank (precision-oriented)
  pairs = [(query, c.text) for c in candidates]
  scores = reranker.predict(pairs)
  reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
  
### **Detection Pattern**
  - search
  - query
  - retrieve
  - similarity

## Old Memories Override Current Information

### **Id**
memory-staleness
### **Severity**
high
### **Situation**
User preferences or facts change over time
### **Symptom**
  Agent uses outdated preferences. "User prefers dark mode" from
  6 months ago overrides recent "switch to light mode" request.
  Agent confidently uses stale data.
  
### **Why**
  Vector stores don't have temporal awareness by default. A memory
  from a year ago has the same retrieval weight as one from today.
  Recent information should generally override old information
  for preferences and mutable facts.
  
### **Solution**
  ## Add temporal scoring
  from datetime import datetime, timedelta
  
  def time_decay_score(memory, half_life_days=30):
      age = (datetime.now() - memory.created_at).days
      decay = 0.5 ** (age / half_life_days)
      return decay
  
  def retrieve_with_recency(query, user_id):
      # Get candidates
      candidates = index.query(
          vector=embed(query),
          filter={"user_id": user_id},
          top_k=20
      )
  
      # Apply time decay
      for candidate in candidates:
          time_score = time_decay_score(candidate)
          candidate.final_score = candidate.similarity * 0.7 + time_score * 0.3
  
      # Re-sort by final score
      return sorted(candidates, key=lambda x: x.final_score, reverse=True)[:5]
  
  ## Update instead of append for preferences
  async def update_preference(user_id, category, value):
      # Delete old preference
      await memory.delete(
          filter={"user_id": user_id, "type": "preference", "category": category}
      )
  
      # Store new preference
      await memory.upsert(
          id=f"pref-{user_id}-{category}",
          content={"category": category, "value": value},
          metadata={"updated_at": datetime.now()}
      )
  
  ## Explicit versioning for facts
  await memory.upsert(
      id=f"fact-{fact_id}-v{version}",
      content=new_fact,
      metadata={
          "version": version,
          "supersedes": previous_id,
          "valid_from": datetime.now()
      }
  )
  
### **Detection Pattern**
  - old
  - stale
  - outdated
  - update

## Contradictory Memories Retrieved Together

### **Id**
memory-conflicts
### **Severity**
medium
### **Situation**
User has changed preferences or provided conflicting info
### **Symptom**
  Agent retrieves "user prefers dark mode" and "user prefers light
  mode" in same context. Gives inconsistent answers. Seems confused
  or forgetful to user.
  
### **Why**
  Without conflict resolution, both old and new information coexist.
  Semantic search might return both because they're both about the
  same topic (preferences). Agent has no way to know which is current.
  
### **Solution**
  ## Detect conflicts on storage
  async def store_with_conflict_check(memory, user_id):
      # Find potentially conflicting memories
      similar = await index.query(
          vector=embed(memory.content),
          filter={"user_id": user_id, "type": memory.type},
          threshold=0.9,  # Very similar
          top_k=5
      )
  
      for existing in similar:
          if is_contradictory(memory.content, existing.content):
              # Ask for resolution
              resolution = await resolve_conflict(memory, existing)
              if resolution == "replace":
                  await index.delete(existing.id)
              elif resolution == "version":
                  await mark_superseded(existing.id, memory.id)
  
      await index.upsert(memory)
  
  ## Conflict detection heuristic
  def is_contradictory(new_content, old_content):
      # Use LLM to detect contradiction
      result = llm.invoke(f'''
          Do these two statements contradict each other?
  
          Statement 1: {old_content}
          Statement 2: {new_content}
  
          Respond with just YES or NO.
      ''')
      return result.strip().upper() == "YES"
  
  ## Periodic consolidation
  async def consolidate_memories(user_id):
      all_memories = await index.list(filter={"user_id": user_id})
      clusters = cluster_by_topic(all_memories)
  
      for cluster in clusters:
          if has_conflicts(cluster):
              resolved = await llm.invoke(f'''
                  These memories may conflict. Create one consolidated
                  memory that represents the current truth:
                  {cluster}
              ''')
              await replace_cluster(cluster, resolved)
  
### **Detection Pattern**
  - conflict
  - contradict
  - inconsistent
  - both

## Retrieved Memories Exceed Context Window

### **Id**
context-window-overflow
### **Severity**
medium
### **Situation**
Retrieving too many memories at once
### **Symptom**
  Token limit errors. Agent truncates important information.
  System prompt gets cut off. Retrieved memories compete with
  user query for space.
  
### **Why**
  Retrieval typically returns top-k results. If k is too high or
  chunks are too large, retrieved context overwhelms the window.
  Critical information (system prompt, recent messages) gets pushed
  out.
  
### **Solution**
  ## Budget tokens for different memory types
  TOKEN_BUDGET = {
      "system_prompt": 500,
      "user_profile": 200,
      "recent_messages": 2000,
      "retrieved_memories": 1000,
      "current_query": 500,
      "buffer": 300,  # Safety margin
  }
  
  def budget_aware_retrieval(query, context_limit=4000):
      remaining = context_limit - TOKEN_BUDGET["system_prompt"] - TOKEN_BUDGET["buffer"]
  
      # Prioritize recent messages
      recent = get_recent_messages(limit=TOKEN_BUDGET["recent_messages"])
      remaining -= count_tokens(recent)
  
      # Then user profile
      profile = get_user_profile(limit=TOKEN_BUDGET["user_profile"])
      remaining -= count_tokens(profile)
  
      # Finally retrieved memories with remaining budget
      memories = retrieve_memories(query, max_tokens=remaining)
  
      return build_context(profile, recent, memories)
  
  ## Dynamic k based on chunk size
  def retrieve_with_budget(query, max_tokens=1000):
      avg_chunk_tokens = 150  # From your data
      max_k = max_tokens // avg_chunk_tokens
  
      results = index.query(query, top_k=max_k)
  
      # Trim if still over budget
      total_tokens = 0
      filtered = []
      for result in results:
          tokens = count_tokens(result.text)
          if total_tokens + tokens <= max_tokens:
              filtered.append(result)
              total_tokens += tokens
          else:
              break
  
      return filtered
  
### **Detection Pattern**
  - token
  - context
  - overflow
  - limit

## Query and Document Embeddings From Different Models

### **Id**
embedding-model-mismatch
### **Severity**
medium
### **Situation**
Upgrading embedding model or mixing providers
### **Symptom**
  Retrieval quality suddenly drops. Relevant documents not found.
  Random results returned. Works for new documents, fails for old.
  
### **Why**
  Embedding models produce different vector spaces. A query embedded
  with text-embedding-3 won't match documents embedded with text-ada-002.
  Mixing models creates garbage similarity scores.
  
### **Solution**
  ## Track embedding model in metadata
  await index.upsert(
      id=doc_id,
      vector=embedding,
      metadata={
          "embedding_model": "text-embedding-3-small",
          "embedding_version": "2024-01",
          "content": content
      }
  )
  
  ## Filter by model version on retrieval
  results = index.query(
      vector=query_embedding,
      filter={"embedding_model": current_model},
      top_k=10
  )
  
  ## Migration strategy for model upgrades
  async def migrate_embeddings(old_model, new_model):
      # Get all documents with old model
      old_docs = await index.list(filter={"embedding_model": old_model})
  
      for doc in old_docs:
          # Re-embed with new model
          new_embedding = await embed(doc.content, model=new_model)
  
          # Update in place
          await index.update(
              id=doc.id,
              vector=new_embedding,
              metadata={"embedding_model": new_model}
          )
  
  ## Use separate collections during migration
  # Old collection: production queries
  # New collection: re-embedding in progress
  # Switch over when complete
  
### **Detection Pattern**
  - embedding
  - model
  - version
  - migrate