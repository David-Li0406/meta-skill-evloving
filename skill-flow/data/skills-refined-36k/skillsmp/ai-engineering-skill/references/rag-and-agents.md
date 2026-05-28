## AI Engineering Skill Reference — Chapter 6: RAG and Agents

This reference distills the chapter into practical patterns, decision frameworks, code snippets, and checklists you can apply immediately.

---

## RAG (Retrieval-Augmented Generation) — Essentials

RAG = retrieve relevant external context per query, then generate. Use it to:
- Reduce hallucinations
- Minimize tokens (cost/latency)
- Personalize with per-user data
- Keep models up-to-date

Typical architecture:
- Indexing: chunk → embed → store (vector DB + metadata store)
- Querying: rewrite → retrieve (hybrid) → rerank → assemble prompt → generate
- Optional: caches, guards, memory

### Minimal RAG Pipeline (text)

1) Indexing
- Chunk documents
- Generate embeddings
- Store vectors and metadata (title, tags, timestamps, ids, permissions)
- Build vector index (HNSW or IVF-PQ)
- Build keyword index (BM25/Elasticsearch)

2) Querying
- Rewrite query (from chat history)
- Retrieve candidates (hybrid: BM25 + vector search)
- Rerank top-N with cross-encoder or LLM-Judge
- Build final prompt (instructions + user query + retrieved chunks)
- Generate answer
- Log for evaluation

---

## Retrieval Algorithms — When to Use What

| Dimension | Term-based (BM25/Elasticsearch) | Embedding-based (Vector Search) |
|---|---|---|
| Strengths | Fast, cheap, proven, easy to operate | Semantic match, natural queries, improves with finetuning |
| Weaknesses | Lexical match only, ambiguity | Costly embeddings & vector infra, may miss exact codes |
| Best for | Exact terms, IDs, logs, error codes, legal cites | Ambiguous wording, multi-lingual, paraphrases |
| Cost/Latency | Low | Medium–High (embeddings + ANN search) |
| Tuning | Fewer knobs | Many knobs (model, index, rerankers) |

Best practice: Use hybrid search (term + embedding) with reciprocal rank fusion (RRF) and/or reranking.

### Hybrid Search with RRF (Reciprocal Rank Fusion)

- Retrieve top-M from BM25 and top-M from vector search
- Combine by RRF: score(doc) += 1 / (k + rank), k≈60
- Take top-K fused results to rerank

Python example:
```python
def rrf_rank(bm25_list, vec_list, k=60, top_k=10):
    scores = {}
    for rank, doc_id in enumerate(bm25_list, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank)
    for rank, doc_id in enumerate(vec_list, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank)
    return [doc for doc, _ in sorted(scores.items(), key=lambda x: -x[1])[:top_k]]
```

---

## Chunking Strategy — Defaults and Variants

Why it matters: retrieval quality, token cost, latency, recall/precision.

Recommended defaults:
- Unit: tokens (model’s tokenizer)
- Chunk size: 500–1,500 tokens
- Overlap: 10–20% of chunk size (e.g., 50–150 tokens)
- Preserve structure boundaries (headings/sections/paragraphs)
- Attach metadata: title, section, doc_id, updated_at

Variations:
- Recursive split: sections → paragraphs → sentences (stop when <= chunk_size)
- Domain splitters: code-aware, Q&A pairs, legal clauses, Chinese sentence segmentation
- Contextual augmentation: prepend a concise “chunk explainer” (50–100 tokens)

Context explainer prompt:
```text
{{WHOLE_DOCUMENT}}
Chunk:
{{CHUNK_CONTENT}}

Write a 50–100 token summary that situates this chunk within the whole document for improved retrieval. Return only the context.
```

Pitfalls:
- Too small chunks → lost context, high index/search cost
- Too large chunks → low recall, exceeds model/embedding context
- No overlap → boundary loss (“hot dog” → “hot” + “dog”)

---

## Vector Search — Practical Selection

Common ANN indexes:
- HNSW: high recall, fast queries, larger index; great online retrieval
- IVF-PQ: scalable, compressed, lower memory; slight recall hit acceptable
- Annoy: simple, read-only, good for static catalogs

Quick guidance:
- <5M vectors: HNSW
- 5–200M: IVF-PQ or HNSW with careful memory planning
- >200M: IVF-PQ + sharding; consider hybrid indexing

Key metrics:
- Recall@K (target ≥0.9 for top-K)
- QPS (per shard and aggregate)
- Build time (embedding + index)
- Index size (RAM/SSD requirements)

---

## Retrieval Optimization Tactics

1) Reranking
- Cross-encoder rerank: best precision (e.g., bge-reranker, monoT5)
- Time-decay score: prioritize recent data (news/emails/changelogs)
- Positioning: important docs first/last (model primacy/recency)

2) Query Rewriting
- Expand/clarify user intent from chat context
- Identity resolution and guard against unknowns

Prompt:
```text
Given the conversation and the last user turn, rewrite the final user query to be fully self-contained and precise. If required information is missing, say "INSUFFICIENT CONTEXT: <what is needed>".

Conversation:
{{HISTORY}}
User:
{{LAST_UTTERANCE}}

Rewrite:
```

3) Contextual Retrieval
- Enrich chunks with:
  - Keywords, entities (error codes, product names)
  - Titles, section headings, doc summaries
  - Canonical Q&A phrasings (for FAQs/support)
- Store metadata in keyword index for hybrid search

---

## RAG Evaluation — What to Measure and How

Retriever-level:
- Context Precision: % retrieved that are relevant
- Context Recall: % relevant retrieved (harder; needs exhaustive labels)
- Ranking Metrics: NDCG, MAP, MRR

System-level:
- Answer quality (task metrics or LLM judge)
- Hallucination rate
- Token cost and latency

Practical evaluation loop:
1) Build test set: (query, doc corpus, gold relevant docs)
2) Compute precision/recall (human or LLM judge)
3) Ablate components: chunk sizes, number of chunks, k values, reranker on/off
4) Track tokens, latency, cost per query

LLM judge prompt (pairwise doc relevance):
```text
Query: {{Q}}
Document: {{DOC}}

Is the document sufficient to help answer the query? Respond with one of: "relevant", "partially relevant", "irrelevant". Provide a one-sentence rationale.
```

---

## Cost and Latency Controls

- Reserve retrieval budget (e.g., 20–40% of total tokens)
- Limit top_k retrieved (e.g., 3–8, tune per model)
- Cache query embeddings and retrieval results
- Use reranking to prune aggressively; stream generation
- Embed incrementally on updates (changed chunks only)
- Monitor vector DB spend; compress with PQ where appropriate

---

## Multimodal RAG (Images, Audio, Video)

Pattern:
- Index: multimodal embeddings (e.g., CLIP for image/text)
- Query: text → embedding
- Retrieve: images and text by similarity
- Prompt: include both retrieved captions and images (if model supports)

Example (CLIP-like):
```python
# Pseudocode
image_index.add([img_embeds], metadata=[{"caption": "...", "id": ...}])
q_embed = clip.encode_text(query)
candidates = image_index.search(q_embed, top_k=20)
reranked = rerank_cross_encoder(query, candidates)
```

---

## Tabular RAG (Text-to-SQL)

When queries span structured data:
- Steps: intent → schema selection → text-to-SQL → execute → explain
- Use a SQL execution tool with safe read/write gating
- For many tables: schema retriever first (semantic + metadata)

Text-to-SQL pipeline:
```python
plan = classify_intent(query)
schemas = select_schemas(query, all_schemas)  # vector + rules
sql = text2sql_model.generate(query, schemas)
result = sql_executor.run(sql)
answer = llm.generate(f"Question: {query}\nSQL:\n{sql}\nResult:\n{result}\nExplain the answer.")
```

Safety:
- Sandbox execution
- Read-only by default; writes gated by human approval
- Validate SQL against allowlist

---

## Agents — Practical Architecture

An agent = model + tools + planner. It:
- Understands task (intent)
- Plans (decompose into steps/actions)
- Uses tools (function calling)
- Reflects (verify, correct)
- Acts (optionally write to environment)
- Uses memory (short- and long-term)

### Tool Categories
- Knowledge: retrievers, web/search APIs, internal APIs
- Capability: calculator, code interpreter, unit/timezone converters, translators, OCR/captioning
- Write actions: email/send, DB writes, PR creation; strictly gated

Safety:
- Principle of least privilege
- Human-in-the-loop for risky actions
- Guardrails: input validation, policy checks, content filtering
- Code/Prompt injection defenses

---

## Function Calling — Code Pattern

Declare tool inventory with schemas (name, description, parameters). Let the model decide when to call tools; route calls and post results back to the model.

Pseudocode:
```python
tools = [
  {
    "name": "lbs_to_kg",
    "description": "Convert pounds to kilograms.",
    "parameters": {"type": "object", "properties": {"lbs": {"type":"number"}}, "required": ["lbs"]}
  },
  {
    "name": "fetch_top_products",
    "description": "Top N products by sales in [start_date, end_date].",
    "parameters": {"type":"object","properties": {
      "start_date":{"type":"string","format":"date"},
      "end_date":{"type":"string","format":"date"},
      "n":{"type":"integer","minimum":1,"maximum":100}
    }, "required":["start_date","end_date","n"]}
  },
]

resp = llm.chat(messages, tools=tools, tool_choice="auto")
if resp.tool_calls:
    for call in resp.tool_calls:
        # Validate parameters against schema
        out = call_tool(call.name, call.arguments)
        messages.append({"role":"tool","name":call.name,"content":json.dumps(out)})
    resp2 = llm.chat(messages, tools=tools)  # Continue with tool results
```

Tips:
- Always log tool name, params, and outputs
- Validate types/ranges; fill defaults
- Return structured outputs (JSON)

---

## Planning — Decouple Plan from Execution

Why: avoid running bad plans; enable validation and parallelization.

Agent loop:
1) Generate plan (natural language or tool sequence)
2) Validate plan (rules + AI judge)
3) Execute steps (sequential/parallel/conditional)
4) Reflect on outcomes and update plan
5) Stop when goal met or max steps reached

Plan schema (natural language, model-agnostic):
```json
{
  "goal": "Find price of last week's best-selling product",
  "steps": [
    {"action": "get_current_date"},
    {"action": "retrieve_best_sellers", "args": {"window": "last_week", "top_k": 1}},
    {"action": "get_product_info", "args": {"product_name": "$.steps[1].output[0].name"}},
    {"action": "answer", "args": {"style": "brief", "include_sources": true}}
  ]
}
```

Translator: map high-level actions → tool calls; easier to maintain across tool API changes.

Validation rules:
- All actions known and allowed
- Arguments well-typed and in-range
- Steps <= max_steps; risky actions gated
- Dependencies exist (no missing outputs)

---

## Control Flows in Agents

Support beyond sequential:
- Parallel: run independent fetches concurrently
- Conditional (if-else): branch on tool outputs
- Loop: iterate until condition met (with safety caps)

Example:
```python
# Parallel
with ThreadPoolExecutor() as ex:
    futs = [ex.submit(fetch_price, p) for p in products]
    results = [f.result() for f in futs]

# Conditional
if earnings['surprise'] < -0.05:
    action = "consider_sell"
else:
    action = "hold_or_buy"

# Loop with guard
attempts = 0
while not done and attempts < 5:
    attempts += 1
    plan = refine_plan(last_feedback)
```

Choose an agent framework that supports these flows natively if your tasks need them.

---

## Reflection and Error Correction

Implement reflection at:
- Pre-execution (plan sanity)
- Step-by-step (after tool outputs)
- Post-execution (goal achieved? constraints satisfied?)

ReAct-style prompt (simplified):
```text
You are solving: {{TASK}}
At each step, produce:
Thought: your reasoning
Action: one of [TOOL_NAME, Finish]
Action Input: JSON arguments

When sufficient, use Action: Finish with the final answer.

History:
{{TRAJECTORY}}
```

Reflexion loop (pseudocode):
```python
for attempt in range(MAX_ATTEMPTS):
    plan = planner.generate(task, memory)
    if not validator.is_valid(plan): continue
    outcome = executor.run(plan)
    score, feedback = evaluator.score(outcome, constraints)
    if score >= PASS:
        return outcome.final_answer
    reflection = llm.generate(f"Why did we fail? Suggest improvements.\n{feedback}")
    memory.update_with_reflection(reflection)
```

Trade-offs:
- + Accuracy and robustness
- – Token and latency overhead; cap steps and token budgets

---

## Tool Selection — Practical Process

- Start minimal; add tools only if they measurably improve success
- Instrument usage: frequencies, error rates, time per tool
- Ablation: remove a tool → does performance drop?
- If a tool is consistently hard to use (invalid params, low success), simplify or replace it
- Keep tool descriptions concise and precise; include parameter constraints and examples

Analytics to track:
- Tool call count and error rate per tool
- Average tokens/latency/cost contribution
- Common invalid parameter patterns
- Tool transition pairs (X→Y) to identify compound tools

---

## Agent Failure Modes — What to Detect

Planning failures
- Invalid tool names
- Invalid parameters (missing/wrong types/ranges)
- Incorrect parameter values (wrong date window)
- Goal failure (wrong target or constraints violated)
- Premature “done” due to faulty reflection

Tool failures
- Tool output wrong (captioning/SQL)
- Translation layer errors (plan→tool mismatch)
- Missing tool (agent lacks required capability)

Efficiency failures
- Too many steps/calls (cost blowup)
- Slow tools blocking user experience
- Not using parallelizable steps in parallel

Instrumentation checklist:
- Log: plan, tool calls (name/params/out), tokens, time per step, final answer
- Error taxonomy: plan vs tool vs environment
- Threshold alerts: invalid tool rate, avg steps/query, latency SLOs

---

## Agent Evaluation — Metrics and Benchmarks

Plan validity
- % valid plans
- Avg attempts to valid plan
- % invalid tool calls
- % invalid params
- % incorrect param values

Task success
- Success rate under constraints (budget, time)
- LLM-judge/scorer metrics with rubrics
- End-to-end latency and token cost

Efficiency
- Steps per task; tool calls per step
- Time and cost per tool
- Parallelization coverage

Benchmarking tips:
- Build a representative task set with constraints
- Include time-sensitive tasks if relevant
- Add adversarial cases (missing info, injection attempts)
- Compare against baselines (human operator, simpler agent)

---

## Memory for RAG and Agents — Practical Patterns

Memory layers:
- Internal knowledge (model weights) — slow to update
- Short-term (context window) — fast but limited
- Long-term (external store) — scalable and persistent

Short-term memory budgeting:
- Reserve X% of prompt for retrieved context (e.g., 30%)
- Keep recent conversation turns + task-critical state
- Overflow moves to long-term memory

Eviction strategies:
- FIFO (simple, brittle)
- Summarization + entity tracking (preferred)
- Redundancy removal (keep facts, drop verbose)
- Recency + importance scoring

Summarization prompt:
```text
Summarize the conversation into 150–200 tokens focusing on goals, decisions, constraints, and key facts. Maintain entity names and values. Omit chit-chat.
```

Conflict handling:
- Mark facts with timestamps/sources
- Prefer latest for volatile facts; retain conflicting views if helpful
- Use LLM to adjudicate contradictions when needed

Long-term memory retrieval:
- Treat like RAG: embed summaries, entities, decisions; hybrid search
- Attach memory snippets to prompts when relevant

Data structures:
- Conversation summary store (by thread/user)
- Fact store (key-value with provenance)
- Task state store (plan, step results, reflections)
- Tool output logs (for audit and learning)

---

## Secure Write Actions — Operational Guardrails

- Allowlist tools; deny by default
- Parameter validation + type checks
- Policy evaluation (e.g., spending limits, data access scope)
- Human approval checkpoints for risky actions (DB writes, financial)
- Sandboxed code execution (no network/filesystem unless allowed)
- Prompt and code injection defenses (sanitize inputs; strip HTML/JS where needed)
- Audit trail (immutable logs of actions and approvals)

---

## Ready-to-Use Prompts and Schemas

Query Rewriter (self-contained)
```text
Rewrite the last user request to a fully self-contained, specific query.
If essential information is missing, respond with:
INSUFFICIENT CONTEXT: <list required info>

Conversation:
{{HISTORY}}

User: {{LAST_UTTERANCE}}

Rewrite:
```

LLM Judge (document relevance)
```text
You are grading whether the document helps answer the query.

Query: {{Q}}
Document: {{DOC}}

Respond JSON:
{"label": "relevant|partially_relevant|irrelevant", "rationale": "<short reason>"}
```

ReAct Step Format
```text
Thought: ...
Action: <TOOL_NAME or Finish>
Action Input: <JSON args or final answer>
```

Tool Schema Example (JSON Schema)
```json
{
  "name": "fetch_user_payments",
  "description": "Get user's payments between start_date and end_date.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {"type":"string"},
      "start_date": {"type":"string", "format":"date"},
      "end_date": {"type":"string", "format":"date"}
    },
    "required": ["user_id","start_date","end_date"]
  }
}
```

---

## Default Settings — Sensible Starting Points

- Chunking: 1,000 tokens, 15% overlap
- Top-k retrieval: 5 (tune 3–8)
- Hybrid search: BM25 M=200 + Vector M=200 → RRF → rerank top 50
- Reranking: cross-encoder top 20 → final top 5 in prompt
- Prompt budget: 30–40% retrieval, 60–70% instructions + user + memory
- Embedding model: strong general model (e.g., bge-large, E5-large) or vendor-provided
- Vector index: HNSW ef_search=100, M=32 for ≤5M vectors
- Time-decay: exponential decay with half-life tuned to domain (e.g., 7 days for news)

---

## Common Pitfalls and How to Avoid Them

- Over-indexing tiny chunks → slow, costly searches; increase chunk size
- Losing critical tokens at chunk boundaries → add overlap, augment with titles/summaries
- Missing keyword match (error codes) in semantic-only systems → hybrid search with metadata
- Stale embeddings after content changes → incremental re-embedding; content hash to detect diffs
- Tool misuse (invalid params) → strict schema validation + examples in tool descriptions
- Unbounded agent loops → set step/token caps; require progress checks; watchdog timers
- Security gaps for write tools → least privilege, approvals, sandboxing, audit trails

---

## Quick Decision Frameworks

Should I use RAG or longer context?
- Knowledge base ≤200k tokens and rarely changes → try long-context prompt first
- Otherwise → RAG for scalability and cost control; hybrid retrieval

Term-based vs embedding-based?
- Heavy on IDs/codes/precise keywords → term-based baseline
- Natural language, ambiguity, multilingual → add embeddings
- Best overall → hybrid with reranking

Which ANN index?
- Need high recall, RAM OK → HNSW
- Scale and memory constraints → IVF-PQ (accept slight recall loss)

Do I need agents or just RAG?
- Single-turn Q&A with stable docs → RAG
- Multi-step tasks, tool orchestration, conditional flows → Agents

When to add write actions?
- When read-only automation is valuable and safe; add writes only with explicit safety gates and human approvals

---

## RAG Deployment Checklist

- [ ] Define knowledge sources and access controls
- [ ] Choose retrieval strategy (BM25, embeddings, hybrid)
- [ ] Implement robust chunking + overlap + metadata
- [ ] Build vector index (HNSW/IVF-PQ) and BM25 index
- [ ] Add query rewriting and reranking
- [ ] Assemble prompts with clear system instructions
- [ ] Implement evaluation (precision/recall, answer quality)
- [ ] Add caches (embedding, retrieval)
- [ ] Monitor tokens/cost/latency; optimize top_k and reranking thresholds

---

## Agent Deployment Checklist

- [ ] Define environment, tools (read/write), and constraints
- [ ] Implement function calling with strict schemas
- [ ] Plan/validate/execute loop with step caps
- [ ] Reflection: ReAct/Reflexion for robustness
- [ ] Translator for natural-language plans → tool calls
- [ ] Control flows: sequential, parallel, conditionals, loops
- [ ] Safety: validation, approvals, sandbox, logging, injection defenses
- [ ] Evaluation: plan validity, success rate, cost/latency, tool error rates
- [ ] Tool analytics and ablations for inventory optimization

---

## Memory Management Checklist

- [ ] Budget short-term vs retrieval tokens per prompt
- [ ] Summarize conversations; track entities/facts with provenance
- [ ] Evict using recency + importance + summarization
- [ ] Store reflections, plans, and tool outputs for continuity
- [ ] Retrieve long-term memory via hybrid search when relevant
- [ ] Handle conflicting facts with timestamps and adjudication rules

---

## Example: End-to-End RAG+Agent (Text-to-SQL + Docs)

High-level flow:
1) Rewrite query → detect intent (needs SQL? docs? both?)
2) If SQL:
   - Select schemas → generate SQL → execute → capture results
3) Retrieve docs (hybrid) → rerank
4) Build final prompt with:
   - Instructions
   - Rewritten query
   - SQL result (if applicable)
   - Top-N doc chunks (with sources)
5) Generate answer with citations
6) Reflect: verify units, constraints, and consistency; if uncertain, ask for clarification

Execution skeleton:
```python
query = rewrite(user_input, history)
intent = classify_intent(query)

sql_result = None
if intent.requires_sql:
    schemas = select_schemas(query, schema_catalog)
    sql = text2sql(query, schemas)
    sql_result = safe_sql_execute(sql)

docs = hybrid_retrieve(query, k=200)
reranked = rerank(query, docs, top_n=5)

prompt = assemble_prompt(instructions, query, sql_result, reranked)
answer = llm.generate(prompt)

verified = verify(answer, constraints)
if not verified.ok:
    answer = clarify_or_correct(answer, verified.feedback)

return answer
```

---

This reference is designed for fast decision-making and implementation. Use the defaults to get started, then iterate with evaluation and instrumentation to meet your accuracy, cost, and latency targets.