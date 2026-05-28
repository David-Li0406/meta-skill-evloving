# LLM Architect

## Patterns


---
  #### **Name**
Two-Stage Retrieval with Reranking
  #### **Description**
Fast first-stage retrieval, accurate second-stage reranking
  #### **When**
Building any RAG system where quality matters
  #### **Example**
    async def retrieve_with_rerank(
        query: str,
        limit: int = 10
    ) -> list[Document]:
        # Stage 1: Fast retrieval - over-retrieve candidates
        query_vector = await embed(query)
        candidates = await vector_store.search(
            query_vector,
            limit=limit * 5  # 5x over-retrieval
        )
    
        # Stage 2: Cross-encoder reranking for precision
        pairs = [(query, doc.content) for doc in candidates]
        scores = reranker.predict(pairs)
    
        # Sort by reranker scores
        ranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )
    
        return [doc for doc, _ in ranked[:limit]]
    

---
  #### **Name**
Hybrid Search with Reciprocal Rank Fusion
  #### **Description**
Combine vector and keyword search for robust retrieval
  #### **When**
Vector-only search misses exact matches (part numbers, names)
  #### **Example**
    def reciprocal_rank_fusion(
        result_lists: list[list[Result]],
        k: int = 60
    ) -> list[Result]:
        """Combine multiple ranked lists using RRF."""
        scores: dict[str, float] = defaultdict(float)
        items: dict[str, Result] = {}
    
        for results in result_lists:
            for rank, result in enumerate(results):
                scores[result.id] += 1.0 / (k + rank + 1)
                items[result.id] = result
    
        sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)
        return [items[id] for id in sorted_ids]
    
    # Usage: Combine vector + BM25 keyword search
    fused = reciprocal_rank_fusion([
        vector_results,
        keyword_results,
    ])
    

---
  #### **Name**
Structured Output with Tool Use
  #### **Description**
Force schema-conformant responses using tool definitions
  #### **When**
Need guaranteed JSON structure from LLM responses
  #### **Example**
    from anthropic import Anthropic
    
    client = Anthropic()
    
    # Define tool with strict schema
    tools = [{
        "name": "extract_entities",
        "description": "Extract structured entities from text",
        "input_schema": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string", "enum": ["person", "org", "location"]},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                        },
                        "required": ["name", "type", "confidence"]
                    }
                }
            },
            "required": ["entities"]
        }
    }]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "extract_entities"},
        messages=[{"role": "user", "content": f"Extract entities: {text}"}]
    )
    
    # Response guaranteed to match schema
    entities = response.content[0].input["entities"]
    

---
  #### **Name**
Orchestrator-Worker Agent Pattern
  #### **Description**
Lead agent coordinates specialized sub-agents
  #### **When**
Complex tasks requiring multiple specialized capabilities
  #### **Example**
    class OrchestratorAgent:
        def __init__(self, workers: dict[str, Agent]):
            self.workers = workers
    
        async def execute(self, task: str) -> str:
            # Plan: decompose into subtasks
            plan = await self.plan(task)
    
            # Dispatch to workers in parallel where possible
            results = {}
            for subtask in plan.subtasks:
                worker = self.workers[subtask.worker_type]
                results[subtask.id] = await worker.execute(
                    subtask.description,
                    context=subtask.context
                )
    
            # Synthesize results
            return await self.synthesize(task, results)
    
        async def plan(self, task: str) -> Plan:
            response = await llm.complete(
                system="You are a task planner. Decompose complex tasks.",
                user=f"Plan this task: {task}\nAvailable workers: {list(self.workers.keys())}"
            )
            return parse_plan(response)
    

---
  #### **Name**
Context Compression for Long Documents
  #### **Description**
Reduce token usage while preserving key information
  #### **When**
Documents exceed context window or costs are high
  #### **Example**
    async def compress_context(
        documents: list[str],
        query: str,
        max_tokens: int = 4000
    ) -> str:
        # Step 1: Extract query-relevant sentences
        relevant_chunks = []
        for doc in documents:
            sentences = split_sentences(doc)
            for sentence in sentences:
                if is_relevant(sentence, query):
                    relevant_chunks.append(sentence)
    
        # Step 2: Summarize if still too long
        combined = "\n".join(relevant_chunks)
        if count_tokens(combined) > max_tokens:
            combined = await llm.complete(
                system="Summarize preserving facts relevant to the query.",
                user=f"Query: {query}\n\nContent:\n{combined}"
            )
    
        return combined
    

## Anti-Patterns


---
  #### **Name**
Stuffing the Context Window
  #### **Description**
Filling context with everything "just in case"
  #### **Why**
    Performance degrades with context length. Studies show LLMs perform worse
    as context grows - the "lost in the middle" problem. You also pay for every
    token. More context != better answers.
    
  #### **Instead**
Use selective retrieval, compress context, include only relevant information

---
  #### **Name**
Prompts as Afterthoughts
  #### **Description**
Writing prompts inline without versioning or testing
  #### **Why**
    Prompts are production code. A small wording change can completely change
    behavior. Without versioning, you can't reproduce issues or rollback.
    
  #### **Instead**
Store prompts in version control, test with evaluation datasets

---
  #### **Name**
Trusting LLM Output Directly
  #### **Description**
Using LLM responses without validation or parsing
  #### **Why**
    LLMs return strings. Even with JSON instructions, they hallucinate formats,
    add markdown, or return partial responses. Production code will break.
    
  #### **Instead**
Use structured output with tool use, validate with schemas, handle failures

---
  #### **Name**
Vector Search Alone
  #### **Description**
Using only semantic search without keyword/hybrid retrieval
  #### **Why**
    Embeddings miss exact matches (product IDs, names, codes). Semantic similarity
    doesn't capture keyword importance. Recall suffers significantly.
    
  #### **Instead**
Always use hybrid search combining vectors + BM25/keyword

---
  #### **Name**
No Reranking Stage
  #### **Description**
Returning first-stage retrieval results directly to LLM
  #### **Why**
    Fast retrieval (ANN) sacrifices precision for speed. Top-k results often
    include irrelevant chunks. This is the #1 cause of RAG hallucinations.
    
  #### **Instead**
Always rerank with cross-encoder before passing to LLM

---
  #### **Name**
Monolithic Agent
  #### **Description**
Single agent with 20+ tools trying to do everything
  #### **Why**
    As tool count increases, selection accuracy decreases. Agent becomes
    "jack of all trades, master of none." Error rates compound.
    
  #### **Instead**
Use orchestrator-worker pattern with specialized sub-agents